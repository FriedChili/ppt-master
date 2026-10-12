#!/usr/bin/env python3
"""Tests for apply_template.py against the bundled template library."""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from apply_template import (  # noqa: E402
    ApplyTemplateError,
    _receipt,
    apply_templates,
)

TEMPLATES = SCRIPTS_DIR.parent / "templates"
STYLE_ROOT = TEMPLATES / "styles" / "incident-postmortem"
LAYOUT_ROOT = TEMPLATES / "layouts" / "presentation_core"
DECK_ROOT = TEMPLATES / "decks" / "signal_red"


class ApplyTemplateTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.project = self.tmp / "proj"
        (self.project / "templates").mkdir(parents=True)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _apply(self, *roots: Path | str, **kwargs):
        kwargs.setdefault("validate", False)
        return apply_templates(self.project, [str(root) for root in roots], **kwargs)

    def test_library_style_installs_one_qualified_spec_with_provenance(self) -> None:
        plan = self._apply(STYLE_ROOT, validate=True)
        installed = self.project / "templates" / "design_spec.style.incident-postmortem.md"
        self.assertTrue(installed.is_file())
        text = installed.read_text(encoding="utf-8")
        h1 = text.index("# Incident Postmortem")
        self.assertIn(
            "\n\n> **Installed from**: `skills-academic/ppt-master/templates/styles/"
            "incident-postmortem/` (library)\n",
            text[h1:],
        )
        self.assertEqual(text.count("**Installed from**"), 1)
        self.assertEqual(sorted(p.name for p in self.project.iterdir()), ["template_install.json", "templates"])
        receipt = _receipt(plan)
        self.assertIn("sources=library", receipt)
        self.assertIn("kinds=style", receipt)
        self.assertIn("direction:style", receipt)
        self.assertIn("structure:free-design", receipt)
        self.assertIn("active_roster=none", receipt)
        self.assertIn("install=copied", receipt)

    def test_rerun_is_idempotent(self) -> None:
        self._apply(STYLE_ROOT)
        plan = self._apply(STYLE_ROOT)
        self.assertEqual([m.status for m in plan.mappings], ["identical"])

    def test_layout_owns_structure_over_deck(self) -> None:
        plan = self._apply(LAYOUT_ROOT, DECK_ROOT)
        svgs = sorted(p.name for p in (self.project / "templates").glob("*.svg"))
        layout_svgs = sorted(p.name for p in (LAYOUT_ROOT / "templates").glob("*.svg"))
        self.assertEqual(svgs, layout_svgs)
        self.assertFalse((self.project / "templates" / "01_cover.svg").exists())
        receipt = _receipt(plan)
        self.assertIn("structure:layout", receipt)
        self.assertIn("application_context:deck", receipt)
        self.assertIn("active_roster=layout:", receipt)
        self.assertIn(
            "installed_specs=design_spec.layout.presentation_core.md,"
            "design_spec.deck.signal_red.md",
            receipt,
        )

    def test_deck_alone_installs_its_roster(self) -> None:
        self._apply(DECK_ROOT)
        self.assertTrue((self.project / "templates" / "01_cover.svg").is_file())
        spec = self.project / "templates" / "design_spec.deck.signal_red.md"
        self.assertIn("(library)", spec.read_text(encoding="utf-8"))

    def test_duplicate_kind_is_rejected_before_writing(self) -> None:
        with self.assertRaises(ApplyTemplateError) as ctx:
            self._apply(STYLE_ROOT, TEMPLATES / "styles" / "technical-deepdive")
        self.assertIn("one root per kind", str(ctx.exception))
        self.assertEqual(list((self.project / "templates").iterdir()), [])

    def test_destination_collision_is_rejected_before_writing(self) -> None:
        templates = self.project / "templates"
        (templates / "01_cover.svg").write_text("<svg/>", encoding="utf-8")
        with self.assertRaises(ApplyTemplateError) as ctx:
            self._apply(DECK_ROOT)
        self.assertIn("destination collision", str(ctx.exception))
        self.assertFalse(
            (templates / "design_spec.deck.signal_red.md").exists()
        )

    def test_explicit_root_keeps_its_path_as_provenance(self) -> None:
        explicit = self.tmp / "my_style"
        shutil.copytree(STYLE_ROOT, explicit)
        plan = self._apply(explicit)
        spec = self.project / "templates" / "design_spec.style.incident-postmortem.md"
        self.assertIn(
            f"> **Installed from**: `{explicit.resolve()}/` (explicit)",
            spec.read_text(encoding="utf-8"),
        )
        self.assertIn("sources=explicit", _receipt(plan))

    def test_inner_templates_directory_is_refused(self) -> None:
        with self.assertRaises(ApplyTemplateError) as ctx:
            self._apply(STYLE_ROOT / "templates")
        self.assertIn("workspace root", str(ctx.exception))

    def test_dry_run_writes_nothing(self) -> None:
        plan = self._apply(DECK_ROOT, STYLE_ROOT, dry_run=True)
        self.assertGreaterEqual(len(plan.mappings), 1)
        self.assertEqual(list((self.project / "templates").iterdir()), [])

    def test_in_place_deck_roster_is_replaced_by_selected_layout(self) -> None:
        # The project already consumed a Deck in place; a Layout then owns structure.
        self._apply(DECK_ROOT)
        plan = self._apply(self.project, LAYOUT_ROOT)
        self.assertFalse((self.project / "templates" / "01_cover.svg").exists())
        self.assertTrue((self.project / "templates" / "01_title_slide.svg").is_file())
        self.assertTrue(
            (self.project / "templates" / "design_spec.deck.signal_red.md").is_file()
        )
        self.assertIn("structure:layout", _receipt(plan))
        self.assertIn("install=copied", _receipt(plan))


if __name__ == "__main__":
    unittest.main()
