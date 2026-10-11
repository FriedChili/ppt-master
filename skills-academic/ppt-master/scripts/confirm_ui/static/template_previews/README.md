# Template previews

Contact sheets shown under each template selector in the Confirm UI, so a user can
see what a layout or deck actually looks like before installing it.

`app.js` builds the URL as `/static/template_previews/<kind>_<id>.png` for
`kind` in `layout` / `deck`. **Style workspaces have no preview** — a style
workspace ships method and design defaults only, with no SVG prototypes, so
there is nothing to render; the dropdown relies on its name and summary instead.

## Files

| File | Source workspace | Pages shown |
|---|---|---|
| `deck_engineering_blue.png` | `templates/decks/engineering_blue` | cover, chapter, content |
| `deck_signal_red.png` | `templates/decks/signal_red` | cover, chapter, content |
| `layout_report_core.png` | `templates/layouts/report_core` | cover, title+content, chart, process |
| `layout_presentation_core.png` | `templates/layouts/presentation_core` | title, content, two-content, KPI |
| `layout_presentation_core_43.png` | `templates/layouts/presentation_core_43` | title, content, two-content, KPI (4:3) |
| `layout_editorial_bleed.png` | `templates/layouts/editorial_bleed` | hero, hero+scrim, split, triptych |

## Regenerating

These are generated assets. Rebuild them whenever a previewed workspace changes
its SVG prototypes, or when a layout/deck is added or removed.

```sh
# 1. Export the workspace as a review deck (one PPTX per workspace).
python3 scripts/template_preview_pptx.py <workspace> -o <work>/<id>.pptx --force

# 2. Render the review deck to PNGs with the bundled LibreOffice Kit.
"<node>" "<libreoffice-kit-cli>" render \
    --input <work>/<id>.pptx --output-dir <work>/<id> --dpi 100

# 3. Montage the selected pages into one sheet per template.
python3 <build script>     # see the page plan in the table above
```

Step 2 needs the bundled LibreOffice Kit; it is not available from a plain
Python environment. Rendered PNGs are committed here so the Confirm UI never
needs a renderer at runtime.

Page selection is by rendered file order, not by page number: `render --pages`
names its output `page-0001.png`, `page-0002.png`, … in the order requested.
