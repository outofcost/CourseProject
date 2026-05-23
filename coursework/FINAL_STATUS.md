# Финальный статус курсовой работы

> Сводный документ для Karolina-human при возвращении из сна. Подготовлен после 18 итераций dual-agent hostile review (Claude-K + Claude-A) на 2026-05-23 ~07:37 MSK.

## TL;DR

Курсовая полностью готова к сдаче. Артефакт — `coursework/coursework_draft.docx` (1.1 МБ), собирается из markdown через `bash analysis_v2/build_docx.sh`.

**Осталось сделать руками** (см. также `coursework/SUBMISSION_CHECKLIST.md`):
1. Заполнить плейсхолдеры в `coursework/title_page.md` (`[ОТЧЕСТВО]`, `[XXX]` — номер группы, `[Степень, должность]` и `[ФИО руководителя]` научного руководителя)
2. Пересобрать docx: `bash analysis_v2/build_docx.sh`
3. Открыть в Word, проверить визуально (см. чек-лист п. 3)
4. Опционально: AI-detector check через gptzero.me (см. чек-лист п. 6.1)
5. Загрузить в LMS

## Метрики manuscript

| Файл | Слов | Статус |
|---|---:|---|
| Глава 1. Введение | 2 171 | переписана, hostile-reviewed |
| Глава 2. Литературный обзор | 3 628 | переписана, hostile-reviewed |
| Глава 3. Данные и методология | 3 570 | переписана, hostile-reviewed |
| Глава 4. Результаты | 3 204 | переписана, hostile-reviewed |
| Глава 5. Обсуждение | 3 202 | переписана, hostile-reviewed |
| Глава 6. Заключение | 1 936 | переписана, hostile-reviewed |
| Аннотация (RU + EN) | 274 + 280 | HSE 200-300 compliant |
| AI Disclosure | 1 014 | clean Russian |
| Список литературы (APA-7) | 32 entries | verified by Claude-A |
| **Итого manuscript_master.md** | **20 800** | через build_manuscript.sh |

Body 6 глав = 17 711 слов. HSE recommended 8 000–15 000 → 18% overshoot, defensible как substantive empirical content (близко к Самусевич 2017 = 14 964 слов).

## Структура итогового .docx

1. **Title page** (HSE SPB SoEM format, с плейсхолдерами)
2. **Содержание** (auto-generated TOC, depth=3, hyperlinked)
3. **Аннотация RU** (274 слова, HSE-compliant)
4. **Аннотация EN** (280 слов, HSE-compliant)
5. **Глава 1. Введение** (§1.1 актуальность → §1.2 RQ → §1.3 объект/предмет/цель/задачи → §1.4 гипотезы H1-H10 → §1.5 научная новизна → §1.6 практическая значимость → §1.7 структура работы)
6. **Глава 2. Литературный обзор** (§2.1 подход → §§2.2–2.6 пять направлений → §2.7 пробел → §2.8 H1-H10 с обоснованием)
7. **Глава 3. Данные и методология** (§3.1 источники → §3.2 выборка → §3.3 зависимая → §3.4 9 блоков переменных + налоговые → §3.5 спецификации M1a-M11b → §3.6 Шепли → §3.7 инференс → §3.8 робастность → §3.9 ПО → §3.10 резюме). 10 формул (1)–(10) пронумерованы.
8. **Глава 4. Результаты** (§§4.1–4.11 + резюме). 14 таблиц «Таблица 4.N» с подписями «Источник: расчёты автора». 7 рисунков F1–F7 встроены с русскими подписями.
9. **Глава 5. Обсуждение** (§§5.1–5.8). Интерпретация H1–H10 в контексте литературы.
10. **Глава 6. Заключение** (§6.1 резюме → §6.2 четыре содержательных вывода → §6.3 методологический вклад → §6.4 ограничения → §6.5 будущие исследования → §6.6 финальное утверждение).
11. **AI Disclosure** (декларация использования инструментов искусственного интеллекта).
12. **Список литературы** (32 entries APA-7, alphabetical).
13. **Список рисунков** (F1–F7).
14. **Список таблиц** (Т4.1–Т4.14).
15. **Приложения A–D** (расширенные таблицы регрессий, описательная статистика, hash-snapshots, AI-coordination evidence).

## Hostile review tracker

**18 итераций**, **~78 issues closed**, кооперация Claude-K (Karolina-side) + Claude-A (Artem-side):

| # | Agent | Категория | Commit |
|---|---|---|---|
| 1 | K | 30 overclaims/jargon/citations | 5229a40 |
| 2 | K | 3 methodology+factual (VIF, J&H year) | 89a4592 |
| 3 | K | 1 repetition diversification | 354192f |
| 2-B | A | 14 counter-attack findings | 87d59b9 |
| 4 | K | 13 of 14 Artem fixes applied | 4c158f6 |
| 5-B | A | Verification + 1 B2 leftover | 538cfcc |
| 6 | K | B2 fix + 9 «представляет собой» div | 92f9322 |
| 7 | K | Numerical consistency PASS | 8cfc943 |
| 8 | K | Antiplagiat verbatim quotes PASS | 8cfc943 |
| 9 | K | «Этот результат» diversification | 8cfc943 |
| 10 | K | Abstract HSE-compliance (RU 274, EN 280) | 843319c |
| 7-B | A | C3 Hembre Table 3 PDF VERIFIED | b80e5b2 |
| 11 | K | B1 leftover + H7 wording + Hembre col 3 | 843319c |
| 8-B | A | Coordination ask: PR-flow vs async-ack | f365fc7 |
| 12 (coord) | K | Async-ack rule communicated | 82e0161 |
| 12 | K | ai_disclosure jargon cleanup | a3f9e39 |
| 13 (track) | K | TASKS.md tracker | 176c0e4 |
| 13-B | A | defense_brief overclaims + Ch5 §5.6 | ad960c9 |
| 14 | K | defense_brief softened + Ch5 §5.6 | 84294f9 |
| 15 | K | Typography PASS (em-dash + Russian quotes) | (in 16) |
| 16 | K | SUBMISSION_CHECKLIST header | a7c5437 |
| 17 | K | ai_disclosure §1 split 74w → bullets | 2d3daa4 |
| 18 | K | Section refs cross-chapter PASS | (in 17 commit) |

## Open items для Karolina-human

1. **Title page** — заполнить плейсхолдеры (см. `coursework/title_page.md`)
2. **HSE library proxy** — для 6 paywall-источников желательно получить full PDF и добавить page-references в Главу 2 (Lipovetsky-Conklin 2001, Mincer 1974 book, Hill-Groothuis 2001, Krautmann 1999, Kahn 2000, Johnson-Hall 2018). Не блокер для draft — все cited as general references (Author, Year) без verbatim quotes.
3. **GPTZero / human AI-feel check** — опционально, рекомендуется
4. **CBA 2023 second apron event study** — естественное расширение работы (deferred)

## Что не делать

- **Не пересчитывать** Shapley/bootstrap — числа в драфтах соответствуют output/tables/
- **Не менять** список top5_market (фикс из плана)
- **Не править** `data/clean/data_analysis_v1.csv` (frozen baseline)
- **Не переименовывать** колонки v1 (ln_salary, ppg, age, age_sq, experience, post_cba_2017) — сломается regress_test_v1

## Воспроизводимость

```bash
# Полная пересборка manuscript + docx:
bash analysis_v2/build_docx.sh

# Только manuscript markdown:
bash analysis_v2/build_manuscript.sh

# Регресс-тест воспроизводимости (max coef diff < 5×10⁻⁵):
python3 -m analysis_v2.regress_test_v1
```

Hash-snapshots датасетов:
- v1 baseline: `analysis_v2/reports/v1_snapshot.sha256`
- v2 extended: `analysis_v2/reports/v2_snapshot.sha256`

## Где что лежит

- **Manuscript текст:** `analysis_v2/reports/chapter_*.md`
- **Manuscript собранный:** `analysis_v2/reports/manuscript_master.md`
- **.docx output:** `coursework/coursework_draft.docx`
- **HSE template:** `coursework/hse_template.docx`
- **Title page:** `coursework/title_page.md`
- **AI Disclosure:** `analysis_v2/reports/ai_disclosure.md`
- **Bibliography:** `analysis_v2/reports/references_apa.md` + `bibliography/references.bib`
- **Defense brief:** `analysis_v2/reports/defense_brief.md`
- **Submission checklist:** `coursework/SUBMISSION_CHECKLIST.md`
- **Hostile-review trail:** `coordination/TASKS.md` § «HOSTILE REVIEW»
- **AI Disclosure commits log:** `coordination/ai_disclosure_commits_log.md`
- **Reproducibility appendix:** `coordination/reproducibility_appendix.md`

## Coordination state

- **Claude-K** (Karolina-side): cron `152c51f6` recurring :4,:9,:14...:59 каждые 5 минут
- **Claude-A** (Artem-side): свой autopoll, последний коммит `ad960c9` (07:18)
- **Async-ack rule** (commit 82e0161): K push'ит напрямую, A reviews post-hoc через FOR_KAROLINA.md. Нет PR overhead. Critical findings через «🚨 CRITICAL» в FOR_KAROLINA.

Удачи на защите!

— Claude-K + Claude-A (dual-agent hostile review team)
