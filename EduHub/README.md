# EduHub

Учебная одностраничная страница онлайн-курсов по веб-разработке.
Практическая работа 70, 71: основы SEO (метатеги, структура заголовков, `robots.txt`, `sitemap.xml`).

## Структура

```
├── Project/
│   ├── index.html
│   ├── style.css
│   ├── robots.txt
│   ├── sitemap.xml
│   └── docs/seo/        before.png, after.png
└── scripts/             seo-audit.mjs, draw_seo_figures.py
```

## Что сделано

- `lang="ru"`, `charset`, `viewport`, `title` и `description`
- один `<h1>`, остальные разделы — `<h2>`, уровни без пропусков
- `robots.txt` разрешает сканирование страницы и содержит ссылку на карту сайта
- `sitemap.xml` с адресом главной страницы

В `robots.txt` и `sitemap.xml` указан адрес-заглушка `https://example.com`,
при публикации его нужно заменить на реальный домен.

## Запуск и проверка

Нужен любой локальный HTTP-сервер (адрес `file://` не подходит):

```bash
cd Project
npx serve .            # или: python3 -m http.server 3000
```

Файлы `/robots.txt` и `/sitemap.xml` должны открываться в браузере.

SEO-проверка по чек-листу лекции (не Lighthouse):

```bash
node scripts/seo-audit.mjs Project
```

| Состояние | Пройдено проверок |
|---|---|
| До правок | 3 из 11 |
| После правок | 11 из 11 |
