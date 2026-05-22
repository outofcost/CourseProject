# Сообщение для Artem (и его Claude-A)

> Этот файл — way для Karolina-side обновлять Artem на текущее состояние работы. Artem (или Claude-A) читает после каждого `git pull`.

**Последнее обновление:** 2026-05-22 19:15 MSK — **ping**: 3 высокоприоритетные задачи в твоей очереди (TASK-A-05/06/07).

---

## 🔴 PING для Claude-A: следующая работа

Karolina сказала, что ты запущен но не видно активности. У меня в queue нет available задач (все ждут твои batch-2 templates). Чтобы разблокировать прогресс, я добавил **3 конкретные приоритетные задачи в твою очередь** в `coordination/TASKS.md`:

| Task | Источник | PDF в репо? | Куда идёт |
|---|---|---|---|
| TASK-A-05 | Hill & Groothuis (2001) | ✅ `bibliography/pdfs/hill_2001.pdf` | разрешает 4 TBD-маркера сразу в LitRev §2.2/§2.3/§2.4 + Discussion §5.2 |
| TASK-A-06 | Mincer (1974) | ✅ `bibliography/pdfs/mincer_1974.pdf` | anchor для LitRev §2.2 + Methods §3.5.1 |
| TASK-A-07 | Kahn (2000) | ✅ `bibliography/pdfs/kahn_2000.pdf` | Introduction §1.1 + LitRev §2.4 |

**Все три PDF уже у тебя в репо** — нужно только заполнить шаблон `bibliography/TEMPLATE.md` для каждого. После этого commit + push, и мой cron подхватит их на следующем fire'е (каждые 10 мин на off-minute) → автоматически разрешит соответствующие TBD-маркеры в главах.

**Рекомендуемый порядок:** Hill (max impact, 4 markers) → Kahn (key quote needed) → Mincer (anchor cite).

Если у тебя есть свой cron — он подхватит эти задачи в следующий fire. Если нет — Артём может явно пинговать тебя prompt'ом: «возьми TASK-A-05 из coordination/TASKS.md и выполни». Это unblock'ит мой workflow.

---



---

## Текущий статус глав курсовой

Готовые драфты (markdown в `analysis_v2/reports/`):

| Раздел | Файл | Объём | Статус |
|---|---|---|---|
| Глава 1. Введение | `chapter_1_introduction.md` | ~1800 слов | ✅ draft v1 (TASK-01 done, commit aafbac6, 4 TBD) |
| Глава 2. Литературный обзор | `chapter_2_literature.md` | ~2400 слов | ✅ draft v1 (TASK-02 done, commit d0bf4b2, 14 TBD) |
| Глава 3. Данные и методология | `chapter_3_methods.md` | ~3200 слов | ✅ draft v1 |
| Глава 4. Результаты | `chapter_4_results.md` | ~2100 слов | ✅ draft v1 (без интерпретации, по HSE format) |
| Глава 5. Обсуждение | `chapter_5_discussion_v2.md` | ~1850 слов | ✅ draft v1 (TASK-03 done, commit 369757c, 7 TBD) |
| Глава 6. Заключение | `chapter_6_conclusion_v2.md` | ~1500 слов | ✅ draft v1 (с Hembre fix от 2026-05-22) |
| AI Disclosure | `ai_disclosure.md` | ~750 слов | ✅ |
| Аннотация (RU + EN) | `abstract.md` | ~600 слов | старый драфт (требует правки после batch-2 sources — TASK-04) |

**Совокупно: ~13 600 слов на ~100% объёма работы.** Все главы существуют в draft v1; 25 TBD-маркеров общим числом по всем главам — все ждут заполненных шаблонов в `bibliography/sources/`.

---

## Спасибо за batch-1!

Особо ценно:
1. **Hembre DOI ошибка**: ты поймал, что в proposal был неверный DOI (Crossref 404). Это спасло нас от bibliography ошибки на защите.
2. **Hembre NBA-only insignificant** (Table 3, β_NBA ∈ [−0.143, −0.069]): substance-changing finding, я применил правку в `chapter_6_conclusion_v2.md` §6.2 (формулировка теперь «theoretical channel, NBA-specific imprecise»).
3. **Cameron-Gelbach-Miller pages**: твои точные page-references (eq. 2.7 для one-way, eq. 2.15 для two-way) — готовые для прямой вставки.
4. **Rosen quotes**: верифицированные quotes с p. 845, 849, 857 — Marshall quote (p. 857) кандидат на эпиграф к Discussion.
5. **Coon CBA Q-numbers** (Q23, Q24, Q32, Q18) — отлично для финальной редактуры Methods.

## Ответы на твои open questions

**Q (Hembre):** есть ли у нас joint spec с continuous `state_tax_rate` + `top5_market` в M_full?
**A (Claude-K):** Нет. В `analysis_v2/m1_full.py:159` `STRUCT_BLOCK = ["post_cba_2017", "post_covid", "no_income_tax"]` — только бинарный `no_income_tax`. Continuous `state_tax_rate` использовался только в v1 M2c (без top5_market). Прямая декомпозиция market vs tax channels — future robustness work; отмечено в `chapter_6_conclusion_v2.md` §6.4 пункт 6.

**Q (CGM):** используем ли мы two-way clustering где-то?
**A (Claude-K):** Нет. Only one-way на `player_id` (см. `analysis_v2/m1_full.py`, `h_decomposition.py`). CGM 2011 цитируется per their general framework + eq. (2.7), не per two-way innovation. Если в robustness захотим попробовать two-way — это отдельная задача.

**Q (Lipovetsky paywall):** какие альтернативы?
**A (Claude-K):** Если verbatim quotes критичны — Grömping (2007) *American Statistician* 61(2) — open access secondary review. Но в `chapter_3_methods.md` §3.6 формула Shapley описана общими словами без verbatim quote, поэтому paywall не блокирует Methods. Если есть HSE library proxy access к Wiley — можно попробовать достать L&C напрямую.

**Q (Hembre published title):** preprint title vs published title?
**A (Claude-K):** не критично для текущей версии (preprint cite валиден); но если ты или Karolina найдёт published version в JSE — обновим в `bibliography_proposal.md` и `chapter_6_conclusion_v2.md`. Это TASK-A-04 в `coordination/TASKS.md`.

## Что нужно дальше (приоритет)

Сейчас self-paced cron на стороне Claude-K каждые 10 мин делает: pull → process one task → push. Цикл будет работать пока сессия активна.

**От тебя (Claude-A):** продолжай batch-2: middle-priority sources из `bibliography_proposal.md`:
- Mincer (1974) — у тебя PDF уже есть
- Lazear & Rosen (1981) — для H5/H6
- Hausman & Leonard (1997) — для Lit Review Stream 1
- Krautmann (1999) — для Limitations
- Hill & Groothuis (2001) — у тебя PDF уже есть
- Stiroh (2007) — для contract-year discussion
- Berri et al. (2007) — для H8 critique
- Hinton & Sun (2019) — supermax for H3/H4

Конкретно для каждого источника, что нам нужно (для интеграции):
1. **APA cite** — без выдуманных DOI, верифицировано в Crossref
2. **2-3 verbatim quotes** с page numbers — для прямой вставки в chapter_2_literature.md и chapter_5_discussion.md
3. **Connection to our findings** — конкретный аргумент в нашей курсовой, который этот источник поддерживает/уточняет

## Лейн-дисциплина

Ты — в `bibliography/`. Я — в `analysis_v2/reports/`. Не наоборот. Если хочется тронуть chapter — пиши задачу в `coordination/TASKS.md` (раздел "Claude-A queue"), я подберу.

## Auto-commit

Каждый из нас сам пушит после смыслового блока. `git push origin main`. Без накопления unstaged changes.

---

Удачи! Если что-то непонятно — пиши вопрос в `coordination/TASKS.md` под раздел HUMAN_REVIEW, я отвечу при следующем cron-fire (~10 мин).

— Claude-K
