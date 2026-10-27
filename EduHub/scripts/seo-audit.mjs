// Простая SEO-проверка страницы по чек-листу лекции 70-71.
// Запуск: node scripts/seo-audit.mjs <папка_с_index.html> [--json файл.json]
// Это не Lighthouse: скрипт читает исходники и проверяет базовые пункты.
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const ji = args.indexOf('--json');
const jsonOut = ji >= 0 ? args[ji + 1] : null;
const root = path.resolve(args[0] && args[0] !== '--json' ? args[0] : '.');
const read = (p) => { try { return fs.readFileSync(path.join(root, p), 'utf8'); } catch { return null; } };

const results = [];
const add = (group, title, ok, detail = '') => results.push({ group, title, ok, detail });

const html = read('index.html') ?? '';
const G1 = 'Метатеги и язык', G2 = 'Структура заголовков', G3 = 'robots.txt и sitemap.xml';

const lang = html.match(/<html[^>]*\slang="([^"]+)"/i)?.[1];
add(G1, 'У <html> указан атрибут lang="ru"', lang === 'ru', lang ? `сейчас lang="${lang}"` : 'атрибут отсутствует');
add(G1, 'Есть <meta charset="UTF-8">', /<meta\s+charset="utf-8"/i.test(html));
add(G1, 'Есть <meta name="viewport">', /<meta\s+name="viewport"/i.test(html));
const title = html.match(/<title>([^<]*)<\/title>/i)?.[1]?.trim() ?? '';
add(G1, 'Заголовок title указывает название страницы', !!title && !/^document$/i.test(title), `сейчас: «${title}»`);
add(G1, 'Есть meta description', /<meta\s+name="description"\s+content="[^"]{20,}"/i.test(html));

const levels = [...html.matchAll(/<h([1-6])[\s>]/gi)].map((m) => +m[1]);
add(G2, 'На странице ровно один <h1>', levels.filter((l) => l === 1).length === 1, `найдено <h1>: ${levels.filter((l) => l === 1).length}`);
const skip = levels.some((l, i) => i > 0 && l > levels[i - 1] + 1);
add(G2, 'Уровни заголовков идут без пропусков', !skip, skip ? 'есть пропуск уровня' : '');
const fake = /<(div|p|span)[^>]*class="[^"]*(title|heading)[^"]*"/i.test(html) && !/<h1/i.test(html.replace(/<h1[^>]*class="logo"[\s\S]*?<\/h1>/i, ''));
add(G2, 'Главный заголовок сделан элементом, а не <div>', !fake, fake ? 'заголовок оформлен через <div>' : '');

const robots = read('robots.txt');
add(G3, 'robots.txt лежит в корне и содержит User-agent', !!robots && /^user-agent:/im.test(robots), robots === null ? 'файла нет' : '');
add(G3, 'В robots.txt указана строка Sitemap', !!robots && /^sitemap:\s*https?:\/\//im.test(robots));
const sm = read('sitemap.xml');
const locs = sm ? [...sm.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]) : [];
add(G3, 'sitemap.xml есть, адреса абсолютные', locs.length > 0 && locs.every((u) => /^https?:\/\//.test(u)), sm === null ? 'файла нет' : '');

const passed = results.filter((r) => r.ok).length;
const summary = { total: results.length, passed, score: Math.round((passed / results.length) * 100), results };
if (jsonOut) fs.writeFileSync(jsonOut, JSON.stringify(summary, null, 2));
for (const r of results) console.log(`${r.ok ? 'PASS' : 'FAIL'}  [${r.group}] ${r.title}${!r.ok && r.detail ? ' — ' + r.detail : ''}`);
console.log(`\nПройдено ${passed} из ${results.length} (${summary.score}%)`);
