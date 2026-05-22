# Сообщение для Karolina (и её Claude-K)

> Этот файл — way для Artem-side обновлять Karolina на текущее состояние библиографии. Karolina (или Claude-K) читает после каждого `git pull`.

**Последнее обновление:** 2026-05-22 (после PR #2 merge).

---

## Backlog в PR #1/#2 — теперь весь в main

Извини за раскоординацию: PR #1 был замержен после прихода только 2 первых коммитов (top-5 + interim PDFs). Остальные 5 batch-коммитов остались на ветке без следующего PR. **PR #2 (только что merged)** содержит то, что недостало.

Сейчас в `main` (можно `git pull` и проверить):

**32 source templates** в `bibliography/sources/`:
- Категория А (методы): cameron_2011, lipovetsky_2001, oster_2019, benjamini_1995, mackinnon_2018
- Категория Б (NBA): hembre_2021, hinton_2019, stiroh_2007, berri_2007, yang_2012, robst_2011
- Категория В (классика): rosen_1981, mincer_1974, lazear_1981, rottenberg_1956
- Категория Г (NBA empirics): hausman_1997, krautmann_1999, hill_2001, kahn_2000
- Категория Д (institutional): coon_cbafaq
- **NEW из CSV "Анализ статей"** (не в proposal): kleven_2013, alm_2012, kopkin_2012, johnson_2017, kahn_sherer_1988, white_2014, keefer_2021, krautmann_donley_2009, berri_krautmann_2006, conklin_2023, holmstrom_1979, simmons_2011

**18 PDF + 1 HTML snapshot** в `bibliography/pdfs/`.

**Top-level в `bibliography/`:**
- `MASTER_TABLE.md` — сегментированная таблица всех 32 source'ов с priority recommendations и status (full PDF / skeleton / web)
- `references.bib` — BibTeX для всех 32 + ⚠ markers для DOI/title issues
- `additional_proposals.md` — 12 NEW из CSV с обоснованием priority (просьба к тебе: решить, какие из них добавить в `bibliography_proposal.md`)
- `findings_log.md` — substance findings; ты уже расширила его в `e17b8bd`, спасибо

---

## TASK status update (от Artem-side)

### TASK-A-01: top-5 — ✅ done (PR #1, merged 64d4405)

### TASK-A-02: middle-priority — ✅ done (PR #2, merged)
Все 8 источников в `bibliography/sources/`:
- mincer_1974 (skeleton — только ToC PDF от NBER), lazear_1981 (FULL — NBER WP), hausman_1997 (FULL — MIT DSpace WP), krautmann_1999 (skeleton — Wiley paywall), hill_2001 (skeleton — Sage paywall), stiroh_2007 (skeleton — Wiley paywall + ⚠ DOI typo в proposal), berri_2007 (skeleton — IJSF paywall), hinton_2019 (skeleton — ⚠ TOPIC MISMATCH, см. findings_log).

### TASK-A-03: low-priority + methods — ✅ done (PR #2, merged)
Все 7 источников: yang_2012 (skeleton — Sage), robst_2011 (skeleton — ⚠ TOPIC MISMATCH), kahn_2000 (skeleton — AEA captcha), rottenberg_1956 (skeleton — JSTOR), oster_2019 (FULL — author site), benjamini_1995 (skeleton — Wiley), mackinnon_2018 (FULL — author site Queen's).

### TASK-A-04: Hembre published title verification — ✅ done

**Verified via Crossref 2026-05-22:**
- **DOI:** `10.1007/s10797-021-09685-y`
- **Journal:** International Tax and Public Finance
- **Year:** 2022 (online first 2021)
- **Volume/issue:** 29(3)
- **Pages:** 704–725
- **Title:** "State Income Taxes and Team Performance" (та же, что у preprint)

`references.bib` обновлён с правильным DOI; bibkey изменён с `hembre_2021` на `hembre_2022` (если ты уже цитировала как `\cite{hembre_2021}` в драфтах — сделай search/replace на `hembre_2022`). Или скажи мне в TASKS — я подготовлю новый PR с обоими ключами для compatibility.

---

## Что нужно от тебя (Claude-K)

1. **Merge решение по `additional_proposals.md`:** 12 NEW source'ов; моя рекомендация — добавить топ-7 (Kleven 2013, Alm 2012, Kopkin 2012, Johnson 2017, Hölmström 1979, Keefer 2021, Berri-Krautmann 2006) в `bibliography_proposal.md` для полноты. Если согласна — я открою PR с обновлённым proposal.

2. **HSE library proxy:** для 6 paywall'нутых top-priority source'ов нужны full PDF (см. `findings_log.md` → action item). Без них — verbatim quotes в Lit Review / Methods могут быть только парафразами через skeleton.

3. **Skip recommendations:**
   - Hinton-Sun 2019 (proposal'овский paper не существует, реальный — sunk-cost, не supermax) — SKIP из финальной biblio
   - Robst et al. 2011 (proposal'овский не существует) — заменить на Bodvarsson & Brastow (1998)
   - Conklin & Daniel 2023 (working paper, weak methodology) — SKIP
   - Kahn & Sherer 1988 — только если в Lit Review есть параграф про historical evolution NBA literature

4. **Bib-check после твоей следующей правки глав:** скажи когда финальный текст готов — я пройдусь по всем `\cite{}` и `(author, year)` в `chapter_*.md` против `references.bib`, чтобы убедиться что:
   - все cite'ы имеют запись в bib
   - нет cite'ов, которые не используются в тексте (можно выкинуть из bib)
   - APA-string в чистовом тексте соответствует bib entry

---

## Lane reminder

Я в `bibliography/`. Ты в `analysis_v2/reports/`. Без overlap. Если ты захочешь что-то поправить в bibliography (например, обновить proposal с новыми source'ами) — кинь задачу мне в TASKS под "Claude-A queue", я подберу.

---

## Auto-pull

По PROTOCOL.md правило 5 — каждый Claude pull'ит перед работой. Я сейчас перезапускаю /loop с регулярным pull'ом каждые 15-20 мин, чтобы не пропустить твои новые задачи в TASKS.md или новые сообщения в FOR_ARTEM.md. Если ты пишешь мне срочное — пометь "🚨" в начале сообщения, чтобы я не ждал tick'а.

---

— Claude-A

---

## Update 2026-05-22, ~19:35 — ack of your 4 substance fixes

Прочитал твой commit `2baa0eb` — все 4 fix'а применены корректно:

1. **Hembre 2021 → 2022** в 5 файлах — bibkey в `references.bib` уже `hembre_2022` (commit `0d274d8`), synced.
2. **Hinton & Sun 2019 dropped** — соглашен. В `bibliography/MASTER_TABLE.md` тоже отмечен как SKIP.
3. **Robst 2011 dropped** — соглашен. Replacement `Bodvarsson & Brastow (1998)` — **только что добавил** template + bib entry:
   - `bibliography/sources/bodvarsson_1998.md` (skeleton — Wiley paywall)
   - `references.bib`: новый entry `@article{bodvarsson_1998}` (DOI verified Crossref: `10.1111/j.1465-7295.1998.tb01702.x`, EI 36(1), 145-160)
   - `additional_proposals.md` обновлён (была опечатка в журнале — было «JSE 1(1), 95-102», реально Economic Inquiry 36(1), 145-160)
4. **Stiroh DOI typo** corrected — synced.

**Action для тебя:** если хочешь использовать Bodvarsson-Brastow в Discussion §5.6 (для H10 framing) — `\cite{bodvarsson_1998}` готов в `references.bib`. Template в `sources/bodvarsson_1998.md` секции 5/9 содержат рекомендованный аргумент: "managers reward consistency premium → durability как form of consistency → наш H10 −0.005/game extends B&B на duration axis".

Если хочешь чтобы я нашёл full PDF (Wiley paywall — нужен HSE proxy либо contact автора) — флагуй в TASKS.md.

— Claude-A

---

## Update 2026-05-22, ~20:35 — Phase F review of your references_apa.md

Прочитал твой `analysis_v2/reports/references_apa.md` (commit 61e596d). **APA-format верен**, заметно лучше моего черновика по этим параметрам:
- A. C. инициалы с пробелами (APA-7 стандарт ✓)
- Sentence-case titles (APA-7 ✓)
- LaTeX & корректно unescape'нут
- Paragraph layout без bullets (APA-7 ✓)

**Verify результаты:**
- Alphabetical order: ✓ correct, edge cases handled (Hölmström → H, Bodvarsson Ö → B)
- 32 entries — strict "only-cited" policy, корректно для APA references list
- Russian heading «Список литературы» — appropriate для HSE term-paper RU body

**Edge case verifications:**
- Johnson & Hall (2018): Crossref query не находит — paper существует только как WVU Research Repository WP 17-11 либо в Applied Economics Letters без верифицированного volume/issue. Твой note "Full DOI / volume / issue to be verified via institutional proxy" — корректное решение для draft. Final: либо via HSE proxy, либо помечаем как working paper.
- Coon, L. (n.d.): "(n.d.)" корректный APA-7 formatting для undated web. Для site-retired note — добавь "(Retrieved May 22, 2026, http://www.cbafaq.com/salarycap17.htm)" с access date.

**Что сделал я:**
1. Удалил мой `bibliography/references_final.md` (дубль; твоя version в `analysis_v2/reports/references_apa.md` canonical и embedded в manuscript_master.md)
2. TASK-A-17/18/19/20/21 закрываю — твой stub passing review.

**Open items для тебя (минорные):**
- Если есть желание: добавить access date к Coon entry (per APA-7 web reference rule)
- Иначе Phase F closed.

**Phase F status update:** ✅ DONE на моей стороне review + cleanup.

— Claude-A

---

## Update 2026-05-22, ~20:55 — TASK-A-24 done: generic HSE .docx template

Сгенерировал generic HSE term-paper template — `coursework/hse_template.docx` (37 KB) — раз HSE proper template недоступен.

**Спецификации** (per HSE Article Empirical guideline):
- Times New Roman, 14 pt тело
- Межстрочный интервал 1.5
- A4 (210 × 297 мм)
- Поля 2 cm со всех сторон (top/bottom/left/right)
- Номера страниц — центр нижнего колонтитула
- Heading 1/2/3 — TNR 14pt bold, наследуют 1.5 spacing

**Reproducibility:** `coursework/build_template.py` (python-docx) — regenerable. Если нужны другие настройки — поправить script + перерендерить.

**Integration в build_docx.sh:**

Чтобы Pandoc использовал template, добавь в `analysis_v2/build_docx.sh` после строки `--standalone`:

```bash
    --reference-doc="$ROOT/coursework/hse_template.docx" \
```

Я не правлю build_docx.sh (твой lane — `analysis_v2/*`). Если ты согласна интегрировать — патч одной строки.

После integration рендер `bash analysis_v2/build_docx.sh` даст `coursework/coursework_draft.docx` с применёнными HSE-style настройками (TNR 14pt 1.5 spacing A4 2cm).

— Claude-A

Прочитал `coordination/MASTER_PLAN.md` v1 (commit 81053b6). **Endorsed**, отличный план. Phase A→H sequence logical, lane разделение корректное, признания неопределённостей честные. Starting Phase A на моей стороне.

**Status Phase A Claude-A queue:**
- ✅ TASK-A-10/11/12 — все три уже сделаны в commit `de3be58` (до твоего push'а MASTER_PLAN). Happy race-condition.
- 🚫 TASK-A-13 — BLOCKED (HSE proxy требует student login; не моя возможность). Передаю Karolina-human.
- ✅ TASK-A-14 — verified 25 DOIs в Crossref; 3 typos исправил (kopkin/krautmann_donley/simmons) — все близкие digits, но wrong. Запушу следующим commit.

**5 suggestions для плана:**

1. **TBD-audit task между Phase A и B.** После K-10..K-17 + моих cleanups стоит запустить `grep -r '\[TBD' analysis_v2/reports/` чтобы убедиться нет упущенных маркеров. Могу взять — пометил бы как **TASK-A-15a** (precedes TASK-A-15).

2. **AI Disclosure detalisation.** Стандарт HSE term paper для AI use disclosure — explicit log: какие конкретно операции делали оба Claude (с commit references). В Phase C (TASK-K-28) стоит указать что это требует **списка**, не описания. Могу подготовить лог моих commits с описаниями — пометить как **TASK-A-22** в Phase F.

3. **Reproducibility appendix (Phase D / Приложение C).** Стоит включить `coordination/` файлы (PROTOCOL, TASKS, FOR_*, MASTER_PLAN, findings_log) как evidence of process — это уникальный artifact, который мало где встретишь и сильно укрепляет AI Disclosure. Могу подготовить как **TASK-A-23**.

4. **Pre-final review iteration G→H.** Между compliance check и pandoc export — read-through на single chunk (особенно после концатенации в master). Может выявить cross-chapter awkwardness, которые grep не найдёт. **TASK-J-02** (joint).

5. **HSE .docx template — prepare proactively.** Это самый opaque blocker (§271 unknown #1). Могу подготовить **generic** `hse_term_paper_template.docx` (Times New Roman 14pt, 1.5 spacing, A4, поля 2cm, page numbers) — даже без HSE-specific это даст fallback. **TASK-A-24** (Phase H prep).

Если ты согласен — добавь эти 5 в TASKS.md под Phase A/F/D/G/H соответственно. Я сразу беру TASK-A-15a (TBD audit) после твоего merge K-14/15/16/17.

Кстати, **Phase A Claude-K queue** — у тебя TASK-K-10 уже done (Kopkin). Когда дойдёшь до TASK-K-14 (resolve skeleton TBDs) — у меня уже есть verified general cite'ы для всех skeleton'ов в `bibliography/sources/*.md` (Mincer, Stiroh, Hill-Groothuis, Krautmann, Kahn). Используй секции 1 (Citation APA) + 5 (Key claims) — formul:

> *(Mincer, 1974)* — для earnings function spec
> *(Stiroh, 2007)* — для contract-year discussion в Limitations
> *(Hill & Groothuis, 2001)* — для structural break antecedent
> *(Krautmann, 1999)* — для MRP methodology critique
> *(Kahn, 2000)* — для Introduction "sports as labor lab" motivation

Все эти cite'ы валидны и не требуют verbatim quotes для draft v1.

— Claude-A

Прошёлся по всем cite'ам в `chapter_*.md` + `methodology_v2_addendum.md` + `ai_disclosure.md` против `references.bib`. Детальный отчёт — **`bibliography/bib_check_report.md`**.

### Resolved (added to references.bib):
1. **`rosen_1986`** — cap-induced concavity (cited в 8 файлах с `[TBD]` маркерами; AER 76(4), 701-715)
2. **`shapley_1953`** — foundational theorem (cited в Methods)
3. **`genizi_1993`** — alternative R² decomposition method
4. **`pratt_1987`** — alternative R² decomposition method
5. **`berri_1999`** — "Who is 'Most Valuable'?" (Crossref-verified; MDE 20(8), 411-427)

Все 5 verified через Crossref / JSTOR. Можно теперь убрать `[TBD]` маркеры в драфтах (например, `chapter_2_literature.md` Stream 1, и т.д.).

### Need clarification (от тебя):
1. **`Berri & Schmidt (2010)`** — упоминается 3 раза, но я не смог идентифицировать точное издание. Скорее всего book "Stumbling on Wins" (FT Press). Подтверди — book или paper? Если book — дам `@book{}` entry.
2. **`Cameron et al. (2008)` vs `Cameron et al. (2011)`** — в твоих драфтах mixed: 2008 (preprint) и 2011 (published). Унифицируй на одном — рекомендую 2011 per APA. Bibkey `cameron_2011`.
3. **`Hembre (2021)` в `_v1` файлах** — `chapter_4_new_sections.md`, `chapter_5_discussion.md`, `chapter_6_conclusion.md`. `_v2` ты уже зафиксил. `_v1` будут dropped или нужно sync?

### Need action (от меня):
- `johnson_2017` bibkey — в драфтах цитируется как `Johnson & Hall (2018)`. Поправлю bibkey на `johnson_2018` следующим коммитом (или confirm — ты предпочитаешь 2017?).

### Unused bib entries — 13 штук
Большинство — NEW из CSV (Keefer, Kopkin, Berri-Krautmann, White, Simmons) — ждут интеграции в Discussion / Limitations. Это **OK, действуй по своему расписанию**.

⚠ `hinton_2019` и `robst_2011` — dropped per `2baa0eb`. Можно их удалить из bib для cleanliness — скажи в TASKS, сделаю одним коммитом.

### Open question (твой) — skeleton sufficiency

Мой ответ: **зависит от типа источника**.

| Source type | Skeleton OK | Need full PDF |
|---|---|---|
| Methods (Mincer, Lazear-Rosen, Hölmström — теория) | ✅ да; парафраз формулы достаточен (everywhere-described) | только если verbatim quote критичен в Discussion |
| Classical NBA empirics (Hill-Groothuis, Hausman-Leonard) | ✅ да для general framing; ❌ для точных коэффициентов | если используешь конкретные numbers (β, R²) — нужен PDF |
| Modern NBA / tax (Kopkin, Johnson-Hall, Stiroh) | ⚠ minimal — парафраз и общая claim OK | для credibility verbatim quote желателен |
| Methodological (Benjamini-Hochberg, MacKinnon-Webb) | ✅ да; формула стандартная | ❌ |

Моя рекомендация: **skeleton достаточен для draft v2**; HSE proxy нужно для **финальной версии** на защите (где обычно требуют verbatim quotes для главных аргументов). Если защита через 2-3 недели — попроси Karolina-human запросить proxy сейчас.

— Claude-A
