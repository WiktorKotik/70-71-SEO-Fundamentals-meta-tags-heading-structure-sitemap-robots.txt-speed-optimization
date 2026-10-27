"""Рисует схемы «до» и «после» по результатам scripts/seo-audit.mjs.
Запуск: python3 scripts/draw_seo_figures.py
Это рисунки-схемы, а не скриншоты Lighthouse."""
import json, math
from PIL import Image, ImageDraw, ImageFont

FD = '/usr/share/fonts/truetype/dejavu/'
f = lambda n, s: ImageFont.truetype(FD + n, s)
REG, BOLD = 'DejaVuSans.ttf', 'DejaVuSans-Bold.ttf'
BG, PANEL, TEXT, MUTED = (32, 33, 36), (41, 42, 45), (232, 234, 237), (154, 160, 166)
GREEN, ORANGE, RED = (12, 206, 107), (255, 164, 0), (255, 78, 66)

def color(score): return GREEN if score >= 90 else ORANGE if score >= 50 else RED

def draw(json_path, out_path, label, caption):
    data = json.load(open(json_path, encoding='utf-8'))
    W, row_h, grp_h = 1100, 38, 52
    groups = {}
    for r in data['results']: groups.setdefault(r['group'], []).append(r)
    H = 330 + sum(grp_h + len(v) * row_h for v in groups.values()) + 70
    img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, 54], fill=(20, 20, 22))
    d.text((24, 15), 'SEO-проверка страницы EduHub', font=f(BOLD, 20), fill=TEXT)
    d.text((W - 24, 17), label, font=f(REG, 16), fill=MUTED, anchor='ra')

    # шкала-«спидометр»
    cx, cy, R = W // 2, 170, 62
    sc = data['score']; col = color(sc)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=(70, 72, 76), width=10)
    d.arc([cx - R, cy - R, cx + R, cy + R], -90, -90 + 360 * sc / 100, fill=col, width=10)
    d.text((cx, cy), str(sc), font=f(BOLD, 44), fill=col, anchor='mm')
    d.text((cx, cy + R + 28), 'SEO', font=f(BOLD, 26), fill=TEXT, anchor='mm')
    d.text((cx, cy + R + 56), f"пройдено проверок: {data['passed']} из {data['total']}", font=f(REG, 15), fill=MUTED, anchor='mm')

    y = 330
    for g, rows in groups.items():
        ok = sum(r['ok'] for r in rows)
        d.text((40, y + 12), g, font=f(BOLD, 16), fill=MUTED)
        d.text((W - 40, y + 12), f'{ok}/{len(rows)}', font=f(BOLD, 16), fill=GREEN if ok == len(rows) else RED, anchor='ra')
        d.line([40, y + 42, W - 40, y + 42], fill=(70, 72, 76), width=1)
        y += grp_h
        for r in rows:
            c = GREEN if r['ok'] else RED
            cx0, cy0 = 58, y + row_h // 2
            d.ellipse([cx0 - 9, cy0 - 9, cx0 + 9, cy0 + 9], fill=c)
            if r['ok']:  # галочка
                d.line([(cx0 - 4, cy0), (cx0 - 1, cy0 + 4), (cx0 + 5, cy0 - 4)], fill=BG, width=3)
            else:        # крестик
                d.line([(cx0 - 4, cy0 - 4), (cx0 + 4, cy0 + 4)], fill=BG, width=3)
                d.line([(cx0 - 4, cy0 + 4), (cx0 + 4, cy0 - 4)], fill=BG, width=3)
            d.text((84, cy0), r['title'], font=f(REG, 16), fill=TEXT, anchor='lm')
            if not r['ok'] and r['detail']:
                d.text((W - 40, cy0), r['detail'], font=f(REG, 13), fill=ORANGE, anchor='rm')
            y += row_h
    d.text((W // 2, H - 30), caption, font=f(REG, 13), fill=MUTED, anchor='mm')
    img.save(out_path)

draw('Project/docs/seo/audit-before.json', 'Project/docs/seo/before.png', 'Рисунок 1 — состояние «до»',
     'Схема построена по результатам scripts/seo-audit.mjs (не скриншот Lighthouse)')
draw('Project/docs/seo/audit-after.json', 'Project/docs/seo/after.png', 'Рисунок 2 — состояние «после»',
     'Схема построена по результатам scripts/seo-audit.mjs (не скриншот Lighthouse)')
print('ok')
