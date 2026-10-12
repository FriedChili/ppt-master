#!/usr/bin/env python3
"""Resolve an upstream Pepper workspace into a flat staging directory.

The resolver is **deterministic** — no model calls. It answers two questions the
consuming skill cannot answer by itself:

1. *Which* upstream artifacts are worth reading (the rest is noise: code,
   contracts, build logs, pipeline-internal notes).
2. What the figures/tables actually are (their names are unpredictable, so they
   are resolved from the paper's own ``\\input{}`` / ``\\includegraphics{}``
   declarations and de-duplicated by stem, with captions taken from the
   surrounding float environment).

Output is a **flat directory** of ordinary files plus one ``resolution.json``.
That is deliberate: the skill's existing intake (``project_manager.py
import-sources``) already consumes a flat directory and copies it into
``sources/``, so this route needs **no change to the skill at all**. The
resolver prepares files; the skill ingests them normally.

Paths inside ``resolution.json`` are bare filenames — exactly what the skill
will see sitting in ``sources/`` after import.

Usage:
    resolve_sources.py <workspace> --json
    resolve_sources.py <workspace> --stage <flat_dir>
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import shutil
import sys
from pathlib import Path

MANIFEST_PATH = Path(__file__).resolve().parent / "source_manifest.json"
RESOLUTION_SCHEMA = "deck.source-resolution.v1"


class ResolveError(RuntimeError):
    """Raised when the upstream workspace cannot be resolved."""


# ── LaTeX 解析 ──────────────────────────────────────────────────────────────

_INPUT_RE = re.compile(r"\\input\s*\{([^}]*)\}")
_INCLUDE_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\s*\{([^}]*)\}")
_ENV_RE = re.compile(
    r"\\begin\s*\{(figure|table|longtable)(\*?)\}(.*?)\\end\s*\{\1\2\}", re.S
)
_CAPTION_RE = re.compile(r"\\caption(?:\[[^\]]*\])?\s*\{")

#: LaTeX 转义 → 字面字符。只做无损替换，不做语义改写。
_UNESCAPE = {
    r"\_": "_", r"\%": "%", r"\&": "&", r"\#": "#", r"\$": "$",
    r"\{": "{", r"\}": "}", r"\textbackslash": "\\",
}
_TEXT_WRAP_RE = re.compile(r"\\(?:text(?:bf|it|rm|tt|sf|sc)|emph|mbox)\s*\{([^{}]*)\}")


def latex_to_text(raw: str) -> str:
    """把 caption 里的 LaTeX 外壳剥掉，得到可以直接上幻灯片的文本。

    只处理**无损**的机械变换：去掉数学 ``$`` 定界、展开常见转义、
    解包 ``\\textbf{}`` 这类纯样式命令。任何需要判断语义的东西都不动 ——
    那属于技能侧。
    """
    text = raw.replace("$", "")
    for src, dst in _UNESCAPE.items():
        text = text.replace(src, dst)
    for _ in range(3):                       # 允许少量嵌套
        text, n = _TEXT_WRAP_RE.subn(r"\1", text)
        if not n:
            break
    return re.sub(r"\s+", " ", text).strip()


def _stem_of(raw: str) -> str:
    """取声明目标的主名：剥路径、剥扩展名。"""
    name = raw.replace("\\", "/").split("/")[-1].strip()
    return name.rsplit(".", 1)[0] if "." in name else name


def _balanced(text: str, open_index: int) -> str:
    """从 ``{`` 起做花括号配平，返回内部文本。"""
    depth, j = 1, open_index + 1
    while j < len(text) and depth > 0:
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
        j += 1
    return text[open_index + 1:j - 1]


def _first_caption(text: str) -> str:
    m = _CAPTION_RE.search(text)
    return latex_to_text(_balanced(text, m.end() - 1)) if m else ""


def parse_declarations(tex_text: str) -> dict:
    """→ {tables, figures, inline_tables, float_captions}。

    ``float_captions`` 按 stem 关联浮动体内的 ``\\caption{}`` —— 图注只在
    ``main.tex`` 里，表注通常在被 ``\\input`` 的 ``.tex`` 里，两者都要取。
    """
    tables = {_stem_of(m) for m in _INPUT_RE.findall(tex_text) if _stem_of(m)}
    figures = {_stem_of(m) for m in _INCLUDE_RE.findall(tex_text) if _stem_of(m)}

    captions: dict[str, str] = {}
    for m in _ENV_RE.finditer(tex_text):
        kind, body = m.group(1), m.group(3)
        cap = _first_caption(body)
        if not cap:
            continue
        if kind == "figure":
            for raw in _INCLUDE_RE.findall(body):
                captions.setdefault(_stem_of(raw), cap)
        else:
            for raw in _INPUT_RE.findall(body):
                captions.setdefault(_stem_of(raw), cap)

    inline = len(re.findall(r"\\begin\s*\{(?:table|table\*|longtable|tabular)\*?\s*\}",
                            tex_text))
    return {"tables": tables, "figures": figures,
            "inline_tables": inline, "float_captions": captions}


def extract_caption(tex_text: str) -> str:
    """取 ``.tex`` 里第一条 ``\\caption{...}``（花括号配平）。"""
    return _first_caption(tex_text)


# ── 目录扫描 / 排除 ─────────────────────────────────────────────────────────

def scan_stems(directory: Path, exts: list[str]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    if not directory.is_dir():
        return out
    for f in sorted(directory.iterdir()):
        if f.is_file() and f.suffix.lower().lstrip(".") in exts:
            out.setdefault(f.stem, []).append(f.suffix.lower().lstrip("."))
    return out


def is_excluded(rel_posix: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(rel_posix, p) for p in patterns)


def pick_ext(available: list[str], preference: list[str]) -> str:
    for ext in preference:
        if ext in available:
            return ext
    return sorted(available)[0]


# ── 解析主流程 ──────────────────────────────────────────────────────────────

class Resolver:
    def __init__(self, root: Path, manifest: dict) -> None:
        self.root = root
        self.manifest = manifest
        self.read: list[str] = []          # 解析器自身打开过的文件
        self.files: dict[str, str] = {}    # basename → 工作区内的相对路径

    def _read_text(self, rel: str) -> str:
        self.read.append(rel)
        return (self.root / rel).read_text(encoding="utf-8", errors="ignore")

    def _note(self, rel: str) -> str:
        """登记一个待暂存文件，返回它在暂存区的 basename。"""
        base = rel.replace("\\", "/").split("/")[-1]
        if base in self.files and self.files[base] != rel:
            raise ResolveError(
                f"扁平暂存区存在同名文件：{self.files[base]} 与 {rel} —— "
                "两者的 basename 都是 %s，摄入时会互相覆盖" % base
            )
        self.files[base] = rel
        return base

    def rel(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    # -- 三段 --
    def resolve_fixed(self) -> dict:
        return {
            rel: {"present": (self.root / rel).is_file(), **spec}
            for rel, spec in self.manifest["fixed"].items()
            if not rel.startswith("_")
        }

    def resolve_conditional(self) -> dict:
        present, missing = {}, []
        for entry in self.manifest["conditional"]:
            if (self.root / entry["path"]).is_file():
                present[entry["id"]] = entry["path"]
            else:
                missing.append(entry["id"])
        return {"present": present, "missing": missing}

    def resolve_assets(self, decl: dict) -> tuple[dict, list[str]]:
        out: dict[str, dict] = {}
        missing: list[str] = []
        for spec in self.manifest["assets"]:
            aid = spec["id"]
            exts = list(spec["ext-preference"])
            stems = scan_stems(self.root / spec["dir"], exts)
            declared = decl["tables"] if aid == "tables" else decl["figures"]
            wanted = "caption" in spec.get("extract", [])

            items, dead = [], []
            for stem in sorted(declared):
                if stem not in stems:
                    missing.append(f"{stem}（{spec['dir']}）")
                    continue
                exts_here = sorted(stems[stem], key=lambda e: exts.index(e))
                ext = pick_ext(exts_here, exts)
                rel = f"{spec['dir']}/{stem}.{ext}"
                item = {"file": self._note(rel), "ext": ext, "stem": stem}

                caption = decl["float_captions"].get(stem, "")
                if not caption and wanted and ext == "tex":
                    caption = extract_caption(self._read_text(rel))
                if caption:
                    item["caption"] = caption
                # 只在清单允许时暂存备选扩展名 —— 图和表的诉求不同：
                # 图要位图本体，多暂存 PDF 会被摄入工具转成一堆 markdown 垃圾；
                # 表要 tex（结构 + 题注）与 csv（原生表格数值），两者都不触发转换。
                if spec.get("stage-alt"):
                    alt = {e: self._note(f"{spec['dir']}/{stem}.{e}")
                           for e in exts_here if e != ext}
                    if alt:
                        item["alt"] = alt
                items.append(item)

            for stem in sorted(stems):
                if stem not in declared:
                    dead.append(f"{spec['dir']}/{stem}.{stems[stem][0]}")

            if items:
                block: dict = {"count": len(items), "mode": "external", "items": items}
            elif spec.get("inline-fallback") and decl["inline_tables"]:
                block = {"count": decl["inline_tables"], "mode": "inline",
                         "items": [], "note": "表格内联在 output/main.tex 中"}
            else:
                block = {"count": 0, "mode": "none", "items": []}
            if dead:
                block["dead"] = dead
            out[aid] = block
        return out, sorted(set(missing))

    def resolve_read(self, cond: dict) -> tuple[dict, list[str]]:
        groups: dict[str, list[str]] = {}
        for need in self.manifest["needs"]:
            groups[need] = [
                self._note(cond["present"][e["id"]])
                for e in self.manifest["conditional"]
                if e["id"] in cond["present"] and need in e["provides"]
            ]
        return groups, [n for n, srcs in groups.items() if not srcs]

    def resolve_unknown(self) -> list[str]:
        scan = self.manifest.get("unknown-scan", {})
        exts = {p.lstrip("*") for p in scan.get("patterns", [])}
        known = set(self.manifest["fixed"]) | {
            e["path"] for e in self.manifest["conditional"]
        }
        exclude = self.manifest["exclude"]
        found = []
        for sub in scan.get("roots", []):
            d = self.root / sub if sub else self.root
            if not d.is_dir():
                continue
            for f in sorted(d.iterdir()):
                if not f.is_file() or f.suffix not in exts:
                    continue
                rel = self.rel(f)
                if rel not in known and not is_excluded(rel, exclude):
                    found.append(rel)
        return found

    def run(self) -> dict:
        fixed = self.resolve_fixed()
        if not fixed.get("output/main.tex", {}).get("present"):
            raise ResolveError("上游未产出 output/main.tex —— 管线未完成，不应产稿")

        decl = parse_declarations(self._read_text("output/main.tex"))
        cond = self.resolve_conditional()
        assets, missing_assets = self.resolve_assets(decl)
        groups, unavailable = self.resolve_read(cond)

        # 恒定路径：技能自己会读，这里只登记进暂存区，不在 resolution 里转述。
        primary = {
            "main_tex": self._note("output/main.tex"),
            "main_pdf": self._note("output/main.pdf"),
            "assignment_profile": self._note("assignment_profile.json"),
        }

        return {
            "schema": RESOLUTION_SCHEMA,
            "manifest_version": self.manifest["version"],
            "source_workspace": str(self.root),
            "primary": primary,
            "read": groups,
            "assets": assets,
            "unavailable": unavailable,
            "missing_assets": missing_assets,
            "unknown": self.resolve_unknown(),
            "audit": {"resolver_read": sorted(set(self.read))},
        }


# ── 暂存 ────────────────────────────────────────────────────────────────────

def stage(root: Path, resolver: Resolver, resolution: dict, dest: Path) -> list[str]:
    """扁平复制到 dest，并写入 resolution.json。"""
    dest.mkdir(parents=True, exist_ok=True)
    staged = []
    for base, rel in sorted(resolver.files.items()):
        src = root / rel
        if not src.is_file():
            continue
        shutil.copy2(src, dest / base)
        staged.append(base)
    payload = dict(resolution)
    payload["staged"] = sorted(staged)
    (dest / "resolution.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return staged


# ── CLI ─────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("workspace", type=Path, help="上游工作区根")
    p.add_argument("--stage", type=Path, default=None,
                   help="扁平暂存目录；写入后交给 project_manager import-sources")
    p.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    p.add_argument("--json", action="store_true", help="只输出 JSON 到 stdout")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"清单读取失败: {exc}", file=sys.stderr)
        return 2

    root = args.workspace.resolve()
    if not root.is_dir():
        print(f"工作区不存在: {root}", file=sys.stderr)
        return 2

    resolver = Resolver(root, manifest)
    try:
        resolution = resolver.run()
    except ResolveError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.json or args.stage is None:
        print(json.dumps(resolution, ensure_ascii=False, indent=2))
        return 0

    staged = stage(root, resolver, resolution, args.stage)
    print(f"已暂存 {len(staged)} 个文件到 {args.stage}")
    print(f"接下来: python3 scripts/project_manager.py import-sources "
          f"<project> \"{args.stage}\" --copy")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
