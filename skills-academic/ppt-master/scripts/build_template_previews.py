# -*- coding: utf-8 -*-
"""把已渲染的模板页面拼成预览图，放进 confirm_ui 的静态目录。

每个模板一张：成套模板 3 页横排，版式模板 2×2。
"""
import pathlib
from PIL import Image

RUN = pathlib.Path(r'E:\ppt-master-6.7.0\run')
DST = pathlib.Path(r'E:\ppt-master-6.7.0\skills-academic\deck\scripts\confirm_ui\static\template_previews')
DST.mkdir(parents=True, exist_ok=True)

#: 模板 → (渲染目录, 要用的页序号(1-based), 列数)
#: deck 只渲了 1,3,4 三页，输出按顺序编号，所以用 1,2,3。
PLAN = {
    'deck_engineering_blue': (RUN / 'preview-decks' / 'engineering_blue', [1, 2, 3], 3),
    'deck_signal_red':       (RUN / 'preview-decks' / 'signal_red',       [1, 2, 3], 3),
    'layout_report_core':    (RUN / 'preview-layouts' / 'report_core',    [1, 4, 8, 10], 2),
    'layout_presentation_core': (RUN / 'preview-layouts' / 'presentation_core', [1, 2, 4, 13], 2),
    'layout_presentation_core_43': (RUN / 'preview-layouts' / 'presentation_core_43', [1, 2, 4, 13], 2),
    'layout_editorial_bleed': (RUN / 'preview-layouts' / 'editorial_bleed', [1, 2, 3, 7], 2),
}

TARGET_W = 720          # 每格宽度
GAP = 10
BG = (241, 245, 249)

for name, (src, pages, cols) in PLAN.items():
    files = []
    for n in pages:
        p = src / ('page-%04d.png' % n)
        if p.is_file():
            files.append(p)
        else:
            print('  ⚠ 缺页 %s %d' % (name, n))
    if not files:
        print('  ⛔ 无可用页:', name); continue

    thumbs = []
    for p in files:
        im = Image.open(p).convert('RGB')
        h = round(im.height * TARGET_W / im.width)
        thumbs.append(im.resize((TARGET_W, h), Image.LANCZOS))
    cell_h = max(t.height for t in thumbs)
    rows = (len(thumbs) + cols - 1) // cols
    W = cols * TARGET_W + (cols + 1) * GAP
    H = rows * cell_h + (rows + 1) * GAP
    sheet = Image.new('RGB', (W, H), BG)
    for i, t in enumerate(thumbs):
        r, c = divmod(i, cols)
        sheet.paste(t, (GAP + c * (TARGET_W + GAP), GAP + r * (cell_h + GAP)))
    out = DST / (name + '.png')
    sheet.save(out, 'PNG', optimize=True)
    print('  ✓ %-30s %d 页 %dx%d  %5.1f KB' % (name, len(thumbs), W, H, out.stat().st_size / 1024))

print()
print('  目录:', DST)
