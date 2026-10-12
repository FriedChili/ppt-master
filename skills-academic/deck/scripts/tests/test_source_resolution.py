#!/usr/bin/env python3
"""Tests for resolve_sources.py.

Fixtures are **constructed** in temporary directories — one tree per rule —
rather than snapshotted from real runs. The four test samples used during
research are limited in scope and cannot validate the rules; they are smoke
inputs only (see PIPELINE-INTEGRATION.md §8.4).
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from resolve_sources import (  # noqa: E402
    MANIFEST_PATH,
    ResolveError,
    Resolver,
    extract_caption,
    main,
    parse_declarations,
)

MANIFEST = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
ALL_NEEDS = set(MANIFEST["needs"])


def build(root: Path, *, main_tex: str, profile: bool = True,
          logs: dict[str, str] | None = None,
          figures: dict[str, str] | None = None,
          tables: dict[str, str] | None = None,
          excluded: dict[str, str] | None = None,
          extra: dict[str, str] | None = None) -> Path:
    """构造一个上游工作区目录树。"""
    (root / "output").mkdir(parents=True, exist_ok=True)
    (root / "output" / "main.tex").write_text(main_tex, encoding="utf-8")
    (root / "output" / "main.pdf").write_bytes(b"%PDF-1.4 stub")
    if profile:
        (root / "assignment_profile.json").write_text(
            json.dumps({"deliverableType": "paper", "language": "zh"},
                       ensure_ascii=False), encoding="utf-8")
    for name, body in (logs or {}).items():
        p = root / "refine-logs" / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
    for sub, files in (("figures", figures), ("tables", tables)):
        if not files:
            continue
        d = root / "necessary_materials" / sub
        d.mkdir(parents=True, exist_ok=True)
        for name, body in files.items():
            (d / name).write_text(body, encoding="utf-8")
    for rel, body in list((excluded or {}).items()) + list((extra or {}).items()):
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
    return root


def resolve(root: Path) -> dict:
    return Resolver(root, MANIFEST).run()


ALL_LOGS = {
    "DECISION_LOG.md": "## D1 决定了 X，因为 Y",
    "VERIFICATION_REPORT.md": "VERDICT: ISSUES",
    "LITERATURE_REVIEW.md": "综述",
    "METHOD_UNDERSTANDING.md": "方法",
    "EXPERIMENT_PLAN.md": "设计书",
}


class DeclarationParsingTests(unittest.TestCase):
    def test_input_and_includegraphics(self) -> None:
        d = parse_declarations(
            r"\input{../necessary_materials/tables/tab1.tex}"
            r"\includegraphics[width=\linewidth]{fig_a.png}")
        self.assertEqual(d["tables"], {"tab1"})
        self.assertEqual(d["figures"], {"fig_a"})
        self.assertEqual(d["inline_tables"], 0)

    def test_path_and_extension_stripped(self) -> None:
        d = parse_declarations(r"\input{table2}\includegraphics{../figures/fig3.pdf}")
        self.assertEqual(d["tables"], {"table2"})
        self.assertEqual(d["figures"], {"fig3"})

    def test_figure_caption_taken_from_float(self) -> None:
        tex = (r"\begin{figure}\centering"
               r"\includegraphics[width=\linewidth]{fig1.png}"
               r"\caption{图一的题注}\label{fig:1}\end{figure}")
        self.assertEqual(parse_declarations(tex)["float_captions"]["fig1"],
                         "图一的题注")

    def test_table_caption_taken_from_input_float(self) -> None:
        tex = (r"\begin{table}\caption{表一的题注}"
               r"\input{../necessary_materials/tables/t1.tex}\end{table}")
        self.assertEqual(parse_declarations(tex)["float_captions"]["t1"],
                         "表一的题注")

    def test_inline_table_env_counted(self) -> None:
        tex = r"\begin{table}\caption{a}\end{table}\begin{longtable}b\end{longtable}"
        self.assertEqual(parse_declarations(tex)["inline_tables"], 2)

    def test_caption_brace_balanced(self) -> None:
        self.assertEqual(extract_caption(r"\caption{含 \textbf{嵌套} 的题注}"),
                         "含 嵌套 的题注")
        self.assertEqual(extract_caption("无题注"), "")

    def test_caption_latex_shell_stripped(self) -> None:
        """题注不能带着 LaTeX 外壳上幻灯片。"""
        self.assertEqual(
            extract_caption(r"\caption{核心变量 $x_{it}$ 的系数与95\%置信区间}"),
            "核心变量 x_{it} 的系数与95%置信区间")
        self.assertEqual(extract_caption(r"\caption{a\_b \& c \# d}"),
                         "a_b & c # d")

    def test_caption_keeps_unrecognized_commands(self) -> None:
        """不认识的命令原样保留 —— 不做猜测性改写。"""
        self.assertIn(r"\cite{ref}", extract_caption(r"\caption{见 \cite{ref} 处}"))


class CoreResolutionTests(unittest.TestCase):
    def test_missing_t0_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "ws"
            root.mkdir()
            with self.assertRaises(ResolveError):
                Resolver(root, MANIFEST).run()

    def test_minimal_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            r = resolve(build(Path(tmp) / "ws", main_tex="正文"))
            self.assertEqual(set(r["unavailable"]), ALL_NEEDS)
            self.assertEqual(r["assets"]["figures"]["mode"], "none")
            self.assertEqual(r["assets"]["tables"]["mode"], "none")

    def test_primary_files_are_named_not_relayed(self) -> None:
        """恒定路径只登记，不在 resolution 里展开内容。"""
        with tempfile.TemporaryDirectory() as tmp:
            r = resolve(build(Path(tmp) / "ws", main_tex="正文"))
            self.assertEqual(r["primary"], {
                "main_tex": "main.tex",
                "main_pdf": "main.pdf",
                "assignment_profile": "assignment_profile.json",
            })

    def test_read_groups_use_basenames(self) -> None:
        """read 分组按 manifest 的 conditional 声明顺序返回。

        该顺序**不代表优先级**；技能拿到的是「与该需求相关的全部来源」。
        路径是**纯文件名** —— 摄入后它们就平铺在 sources/ 下。
        """
        with tempfile.TemporaryDirectory() as tmp:
            r = resolve(build(Path(tmp) / "ws", main_tex="正文", logs=ALL_LOGS))
            self.assertEqual(r["read"]["positioning"], ["LITERATURE_REVIEW.md"])
            self.assertEqual(r["read"]["mechanism"],
                             ["LITERATURE_REVIEW.md", "METHOD_UNDERSTANDING.md"])
            self.assertEqual(r["read"]["design_rationale"],
                             ["DECISION_LOG.md", "EXPERIMENT_PLAN.md"])
            self.assertEqual(r["unavailable"], [])

    def test_partial_conditional_yields_unavailable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            r = resolve(build(Path(tmp) / "ws", main_tex="正文",
                              logs={"DECISION_LOG.md": "决策"}))
            self.assertIn("reliability", r["unavailable"])
            self.assertIn("positioning", r["unavailable"])
            self.assertNotIn("communication_intent", r["unavailable"])


class AssetResolutionTests(unittest.TestCase):
    def test_declared_assets_resolved_with_preference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            r = resolve(build(
                Path(tmp) / "ws",
                main_tex=(r"\input{../necessary_materials/tables/t1.tex}"
                          r"\includegraphics{f1.png}"),
                figures={"f1.png": "x", "f1.pdf": "x"},
                tables={"t1.tex": r"\caption{表一}", "t1.csv": "a,b"},
            ))
            fig = r["assets"]["figures"]["items"][0]
            self.assertEqual(fig["file"], "f1.png")
            # 图不暂存备选：多暂存 PDF 会被摄入工具转成 markdown 垃圾
            self.assertNotIn("alt", fig)

            tab = r["assets"]["tables"]["items"][0]
            self.assertEqual(tab["file"], "t1.tex")
            self.assertEqual(tab["caption"], "表一")
            self.assertEqual(tab["alt"], {"csv": "t1.csv"})

    def test_figure_caption_extracted_from_main_tex(self) -> None:
        """图注只在 main.tex 的浮动体里 —— 必须提取，否则图没有题注。"""
        with tempfile.TemporaryDirectory() as tmp:
            r = resolve(build(
                Path(tmp) / "ws",
                main_tex=(r"\begin{figure}\centering"
                          r"\includegraphics[width=\linewidth]{f1.png}"
                          r"\caption{折线图题注}\end{figure}"),
                figures={"f1.png": "x"},
            ))
            self.assertEqual(r["assets"]["figures"]["items"][0]["caption"],
                             "折线图题注")

    def test_no_empty_alt_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            r = resolve(build(Path(tmp) / "ws",
                              main_tex=r"\includegraphics{f1.png}",
                              figures={"f1.png": "x"}))
            self.assertNotIn("alt", r["assets"]["figures"]["items"][0])

    def test_stem_dedup_counts_once(self) -> None:
        """同 stem 多扩展名不得重复计数（否则 4 张图会变成 8 张）。"""
        with tempfile.TemporaryDirectory() as tmp:
            r = resolve(build(
                Path(tmp) / "ws",
                main_tex=r"\includegraphics{f1.png}\includegraphics{f2.png}",
                figures={"f1.png": "x", "f1.pdf": "x",
                         "f2.png": "x", "f2.pdf": "x"},
            ))
            self.assertEqual(r["assets"]["figures"]["count"], 2)

    def test_dead_assets_not_resolved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            r = resolve(build(Path(tmp) / "ws", main_tex=r"\input{t1.tex}",
                              tables={"t1.tex": "x", "dead1.tex": "x",
                                      "dead2.tex": "x"}))
            block = r["assets"]["tables"]
            self.assertEqual(block["count"], 1)
            self.assertEqual(len(block["dead"]), 2)

    def test_missing_assets_reported(self) -> None:
        """正文声明了但磁盘上没有 —— 必须显式报告，不能静默略过。"""
        with tempfile.TemporaryDirectory() as tmp:
            r = resolve(build(Path(tmp) / "ws",
                              main_tex=(r"\includegraphics{here.png}"
                                        r"\includegraphics{gone.png}"),
                              figures={"here.png": "x"}))
            self.assertEqual(r["assets"]["figures"]["count"], 1)
            self.assertEqual(len(r["missing_assets"]), 1)
            self.assertIn("gone", r["missing_assets"][0])

    def test_inline_tables_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            r = resolve(build(
                Path(tmp) / "ws",
                main_tex=(r"\begin{table}a\end{table}"
                          r"\begin{table}b\end{table}"
                          r"\begin{longtable}c\end{longtable}"),
                tables={"t1.tex": "x", "t2.tex": "x"},
            ))
            block = r["assets"]["tables"]
            self.assertEqual(block["mode"], "inline")
            self.assertEqual(block["count"], 3)
            self.assertEqual(block["items"], [])
            self.assertEqual(len(block["dead"]), 2)


class FlatteningTests(unittest.TestCase):
    """暂存区必须是扁平的 —— 现有摄入工具只展开顶层文件。"""

    def test_stage_is_flat_and_complete(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = build(
                Path(tmp) / "ws",
                main_tex=(r"\input{../necessary_materials/tables/t1.tex}"
                          r"\includegraphics{f1.png}"),
                logs=ALL_LOGS, figures={"f1.png": "IMG"},
                tables={"t1.tex": r"\caption{甲}"},
            )
            dest = Path(tmp) / "stage"
            self.assertEqual(main([str(root), "--stage", str(dest)]), 0)

            names = sorted(p.name for p in dest.iterdir())
            self.assertIn("resolution.json", names)
            self.assertIn("main.tex", names)
            self.assertIn("main.pdf", names)
            self.assertIn("assignment_profile.json", names)
            self.assertIn("DECISION_LOG.md", names)
            self.assertIn("f1.png", names)
            self.assertIn("t1.tex", names)
            # 扁平：没有任何子目录
            self.assertFalse(any(p.is_dir() for p in dest.iterdir()))

            res = json.loads((dest / "resolution.json").read_text(encoding="utf-8"))
            self.assertIn("staged", res)
            self.assertIn("f1.png", res["staged"])

    def test_basename_collision_raises(self) -> None:
        """扁平化会撞名 —— 必须报错，不能静默覆盖。

        真实场景：某张表恰好叫 ``main.tex``，与 ``output/main.tex`` 同名。
        """
        with tempfile.TemporaryDirectory() as tmp:
            root = build(Path(tmp) / "ws",
                         main_tex=r"\input{main.tex}",
                         tables={"main.tex": r"\caption{与论文同名的表}"})
            with self.assertRaises(ResolveError) as ctx:
                Resolver(root, MANIFEST).run()
            self.assertIn("同名", str(ctx.exception))


class ExclusionTests(unittest.TestCase):
    def test_excluded_paths_are_never_read_or_staged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            r = resolve(build(
                Path(tmp) / "ws", main_tex="正文", logs=ALL_LOGS,
                excluded={
                    "codes/src/analysis.py": "print(1)",
                    "codes/results/out.csv": "a",
                    "contracts/experiment.json": "{}",
                    "refine-logs/ORCHESTRATOR_COMPACT.md": "内部编排",
                    "refine-logs/VIZ_DATA_NOTES.md": "列统计",
                    "refine-logs/experiment_run_report.md": "运行日志",
                    "output/main.log": "log",
                    "dois/paper.pdf": "x",
                    "logs/telemetry.txt": "x",
                },
            ))
            read = set(r["audit"]["resolver_read"])
            blob = json.dumps(r, ensure_ascii=False)
            for bad in ("codes/src/analysis.py", "contracts/experiment.json",
                        "refine-logs/ORCHESTRATOR_COMPACT.md",
                        "refine-logs/VIZ_DATA_NOTES.md",
                        "refine-logs/experiment_run_report.md",
                        "output/main.log", "dois/paper.pdf", "logs/telemetry.txt"):
                self.assertNotIn(bad, read, f"{bad} 不应被解析器读取")
                self.assertNotIn(bad, blob, f"{bad} 不应出现在产物里")

    def test_unknown_files_logged_not_staged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            r = resolve(build(
                Path(tmp) / "ws", main_tex="正文", logs=ALL_LOGS,
                extra={"refine-logs/BRAND_NEW_ARTIFACT.md": "新产物",
                       "SOME_NEW.json": "{}"},
            ))
            self.assertIn("refine-logs/BRAND_NEW_ARTIFACT.md", r["unknown"])
            self.assertIn("SOME_NEW.json", r["unknown"])
            self.assertNotIn("refine-logs/BRAND_NEW_ARTIFACT.md",
                             r["audit"]["resolver_read"])


class PayloadHygieneTests(unittest.TestCase):
    """产物里不该有噪音 —— 消费方是模型，多余的键就是多余的上下文。"""

    NOISE_KEYS = ("declared", "conditional_missing", "materialized",
                  "excluded_patterns", "base")

    def test_no_noise_keys(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            r = resolve(build(Path(tmp) / "ws", main_tex=r"\includegraphics{f.png}",
                              logs=ALL_LOGS, figures={"f.png": "x"}))
            blob = json.dumps(r, ensure_ascii=False)
            for key in self.NOISE_KEYS:
                self.assertNotIn(key, r, f"噪音键 {key} 不应出现")
                self.assertNotIn(f'"{key}"', blob)

    def test_exact_top_level_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            r = resolve(build(Path(tmp) / "ws", main_tex="正文", logs=ALL_LOGS))
            self.assertEqual(set(r), {
                "schema", "manifest_version", "source_workspace", "primary",
                "read", "assets", "unavailable", "missing_assets", "unknown",
                "audit",
            })
            self.assertEqual(set(r["audit"]), {"resolver_read"})


class InvariantTests(unittest.TestCase):
    def test_determinism(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = build(Path(tmp) / "ws",
                         main_tex=r"\input{t1.tex}\includegraphics{f1.png}",
                         logs=ALL_LOGS, figures={"f1.png": "x"},
                         tables={"t1.tex": r"\caption{甲}"})
            self.assertEqual(resolve(root), resolve(root))

    def test_no_stem_appears_twice(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            r = resolve(build(Path(tmp) / "ws",
                              main_tex=(r"\includegraphics{a.png}"
                                        r"\includegraphics{b.png}"),
                              figures={"a.png": "x", "a.pdf": "x",
                                       "b.png": "x", "b.pdf": "x"}))
            stems = [i["stem"] for i in r["assets"]["figures"]["items"]]
            self.assertEqual(len(stems), len(set(stems)))


class CliTests(unittest.TestCase):
    def test_json_mode_no_side_effects(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = build(Path(tmp) / "ws", main_tex="正文")
            self.assertEqual(main([str(root), "--json"]), 0)
            self.assertFalse((root / "stage").exists())

    def test_missing_t0_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "ws"
            root.mkdir()
            self.assertEqual(main([str(root), "--json"]), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
