# Canvas Format Specification

> See [`shared-standards-core.md`](./shared-standards-core.md) §4.1 for the normative root `viewBox` grammar, compatibility spellings, and fail-closed validation rules.

## Format Quick Reference

| ID | Format | Size | viewBox | Ratio | Use Case |
|----|--------|------|---------|-------|----------|
| `ppt169` | PPT 16:9 | `1280x720` | `0 0 1280 720` | 16:9 | Business presentations, meetings, modern devices |
| `ppt43` | PPT 4:3 | `1024x768` | `0 0 1024 768` | 4:3 | Traditional projectors, academic talks |
| `a4` | A4 Print | `1240x1754` | `0 0 1240 1754` | 1:sqrt(2) | Print posters, flyers |

Custom canvases likewise use `0 0 W H` with positive integer pixels; a fractional canvas is accepted only as compatible input for an imported custom PowerPoint slide size. All pages and internal Layout prototypes in one export share one numeric canvas within PowerPoint's slide range (914,400–51,206,400 EMU per side, about 96–5,376 SVG px). `ppt169` is exactly `1280x720`; `banner` shares the ratio, not the coordinate system.

```xml
<svg viewBox="0 0 1280 720">   <!-- PPT 16:9 -->
```


## Typography Scale Start

**Hard rule — normative owner**: this section owns the initial body-size anchor and sanity band for every registered or custom canvas. Strategist and Quick consume it directly; Confirm UI maintains an exact executable mirror and must not infer alternate canvas classes or values. Values are unitless SVG px.

| Canvas | Reading mode | Advisory body band | Initial body |
|---|---|---:|---:|
| `ppt169` / `ppt43` | `text` | 18–21 | 20 |
| `ppt169` / `ppt43` | `balanced` | 22–25 | 24 |
| `ppt169` / `ppt43` | `presentation` | 28–32 | 32 |

Non-PPT registered and custom canvases derive one effective span from `W x H`:

```text
short = min(W, H); long = max(W, H); span = min(long, 3 * short)
low = round(span * 0.025); start = round(span * 0.029); high = round(span * 0.033)
```

| Canvas | Effective span | Advisory body band | Initial body |
|---|---:|---:|---:|
| `a4` | 1754 | 44–58 | 51 |

Executor's layout values and icon sizes are 1280-wide: scale by canvas width ÷ 1280, and stack regions instead of splitting once a column holds under about 30 body characters.

**Default — starting anchor, not a floor (confirmed identity, source fidelity, or viewing conditions may override)**: start from the table or formula, then resolve the role ramp and page density from content and delivery context; the band only flags unusual values and is not a validation gate. Apply the viewing-distance baseline in [`shared-standards-core.md`](./shared-standards-core.md) instead of silently shrinking a recurring role to make content fit.
