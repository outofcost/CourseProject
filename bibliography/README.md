# Bibliography — инструкция для коллеги

**Контекст:** курсовая работа 3 курса HSE по эмпирическому анализу факторов зарплат NBA-игроков. Полный обзор проекта — в `CLAUDE.md` в корне репо.

**Твоя задача:**
1. Найти полные тексты ~20 статей из `analysis_v2/reports/bibliography_proposal.md`
2. Сохранить PDF в `bibliography/pdfs/{author_year}.pdf`
3. По каждой статье заполнить шаблон `TEMPLATE.md` и сохранить как `bibliography/sources/{author_year}.md`

**Зачем это нужно:** автор курсовой (я / Karolina) переписывает главы под HSE Article Empirical format. Заполненные шаблоны позволяют мне быстро интегрировать ссылки, цитаты и аргументы в текст БЕЗ повторного чтения каждой статьи.

---

## Workflow

### Шаг 1. Найти PDF
- Источники: Google Scholar, JSTOR, Sci-Hub, библиотека HSE, Researcher's личный сайт
- Если pay-walled — проверь preprint на SSRN / NBER / author's webpage
- Если совсем недоступно — отметь в `sources/{author_year}.md` в секции "Reading notes" и оставь скелет шаблона

### Шаг 2. Сохранить PDF
- Имя файла: `{firstauthor_lastname}_{year}.pdf` строчными буквами
  - Пример: `hembre_2021.pdf`, `lipovetsky_2001.pdf`, `cameron_2011.pdf`
- Положить в `bibliography/pdfs/`

### Шаг 3. Заполнить шаблон через Claude Code (или вручную)

**Вариант A — через Claude Code (рекомендую):**

Открой Claude Code в корне репо. Вставь промпт из секции "Claude Code prompt" ниже, замени `{filename}` на имя PDF. Claude прочитает статью + контекст проекта (CLAUDE.md, гипотезы) и заполнит шаблон.

**Вариант B — вручную:**

Скопируй `TEMPLATE.md` в `sources/{author_year}.md`, читай статью и заполняй секции.

### Шаг 4. Commit + push

```bash
git add bibliography/
git commit -m "Add {author_year} source analysis"
git push
```

---

## Приоритеты (по важности для нашей работы)

**ВЫСШИЙ — без них нельзя обойтись:**
1. **Hembre (2021)** — Tax Competition in Professional Sports → прямое объяснение нашего anti-marketability finding (β_top5 < 0); KEY для Discussion
2. **Lipovetsky & Conklin (2001)** — Shapley R² → главный метод декомпозиции
3. **Cameron, Gelbach & Miller (2011)** — cluster-robust inference → методология SE
4. **Rosen (1981)** — Economics of Superstars → теоретическая рамка
5. **Coon CBA FAQ** — институциональный reference (онлайн, не PDF)

**СРЕДНИЙ — для Lit Review streams:**
6. Mincer (1974), Lazear & Rosen (1981), Hausman & Leonard (1997)
7. Krautmann (1999), Hill & Groothuis (2001), Stiroh (2007)
8. Berri et al. (2007), Hinton & Sun (2019)

**НИЗКИЙ — nice-to-have, для context:**
9. Yang & Lin (2012), Robst et al. (2011)
10. Kahn (2000), Rottenberg (1956)
11. Oster (2019), Benjamini & Hochberg (1995), MacKinnon & Webb (2018)

**Делай в порядке приоритета.** Если время ограничено — top 5 критичны, остальное можно доделать после первой версии текста.

---

## Что НЕ нужно делать

- ❌ Не пересказывай статью целиком (это не реферат)
- ❌ Не выдумывай факты, если их нет в статье — пиши "не указано"
- ❌ Не цитируй из abstract без проверки в основном тексте
- ❌ Не оценивай качество статьи (это не peer review)
- ❌ Не меняй файлы вне `bibliography/` без согласования с владельцем репо

---

## Claude Code prompt (копируй и вставляй в Claude Code)

```
Прочитай /Users/{your_path}/курсач/bibliography/pdfs/{author_year}.pdf и заполни шаблон bibliography/TEMPLATE.md по этой статье. Сохрани результат как bibliography/sources/{author_year}.md.

Контекст проекта — в CLAUDE.md (корень репо). Главные гипотезы — в analysis_v2/reports/hypotheses_v2_final.md. Описание методов — в analysis_v2/reports/methodology_v2_addendum.md. Headline findings — в analysis_v2/reports/SHIPPING_SUMMARY.md.

Требования:
1. Все секции шаблона обязательны. Если данных нет — пиши "не указано в статье" (не выдумывай).
2. Прямые цитаты — verbatim, с номерами страниц. Если PDF без номеров — указывай section heading.
3. Секция "Use mapping" — критически важна. Опирайся на CLAUDE.md и hypotheses_v2_final.md, чтобы точно определить:
   - в какой раздел курсовой (Introduction/Lit Review/Methods/Discussion/Limitations) идёт статья
   - какие именно гипотезы (H1-H10) она поддерживает
   - какой конкретный аргумент она обосновывает
4. Секция "Connection to our findings" — обязательно проверь по SHIPPING_SUMMARY.md или chapter_5_discussion.md, какие наши результаты релевантны.
5. APA-формат цитирования (с DOI, если есть).
6. Будь точен в цифрах: β-коэффициенты, p-values, R², sample sizes — цитируй буквально.

После сохранения файла — выведи короткое summary (3-5 строк) о том, как эта статья поможет в нашем тексте.
```

---

## Если найдёшь дополнительные источники

При чтении статьи могут попасться важные ссылки, которых нет в нашем `bibliography_proposal.md`. Если они выглядят критическими (часто цитируются в нескольких приоритетных статьях, или прямо релевантны нашим гипотезам), добавь их в новый файл `bibliography/additional_proposals.md` в формате:

```markdown
## {Author Year} — {Short title}
**APA:** Full citation
**Найден через:** {статья, где упоминается}
**Зачем нужен:** {1-2 предложения}
**Приоритет:** ВЫСШИЙ / СРЕДНИЙ / НИЗКИЙ
```

Не ищи PDF сразу — сначала собираем список, потом я решу что брать.

---

## Связь с владельцем репо

- Если что-то непонятно по проекту — читай `CLAUDE.md` и `analysis_v2/reports/SHIPPING_SUMMARY.md`
- Если непонятно по конкретной гипотезе — `analysis_v2/reports/hypotheses_v2_final.md`
- Если что-то блокирует — создавай GitHub Issue с тегом `bibliography`

---

## Структура папки

```
bibliography/
├── README.md                       ← этот файл
├── TEMPLATE.md                     ← шаблон для каждой статьи
├── additional_proposals.md         ← (если найдёшь новые источники)
├── pdfs/                           ← скачанные PDF
│   ├── hembre_2021.pdf
│   ├── lipovetsky_2001.pdf
│   └── ...
└── sources/                        ← заполненные шаблоны
    ├── hembre_2021.md
    ├── lipovetsky_2001.md
    └── ...
```
