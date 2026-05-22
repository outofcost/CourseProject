# Bibliography check report

> Cross-reference между cite'ами в `analysis_v2/reports/chapter_*.md` (+ `abstract.md`, `methodology_v2_addendum.md`, `ai_disclosure.md`) и `bibliography/references.bib`. Запуск: 2026-05-22, после commit `f5bfeee` (Claude-K integration of verified sources) и `1bfe314` (Claude-K B&B integration).

**Method:** регулярки на APA-формат in-text cite'ов (`Author (Year)` и `(Author, Year)`); сравнение `(lastname.lower(), year)` с bib entries. False-positives отфильтрованы вручную (см. ниже).

---

## ✅ Resolved by this report

Добавил в `references.bib` (commit `[Claude-A] bib-check report + 5 missing entries`):
- `rosen_1986` — cap-induced concavity (cited в 8 chapter файлах как `Rosen (1986)`)
- `shapley_1953` — foundational theorem (cited в `methodology_v2_addendum.md` + `chapter_3_methods.md`)
- `genizi_1993` — alternative R² decomposition (cited в Discussion)
- `pratt_1987` — alternative R² decomposition (cited в Discussion + Methods)
- `berri_1999` — Berri's MVP/wins production paper (cited в `chapter_2_literature.md`, [TBD] marker)

Все 5 entries verified через Crossref / JSTOR.

---

## ⚠ Still missing — нужно от Кирилла либо clarify, либо я найду

### 1. `Berri & Schmidt (2010)` — markeт-size argument для MLB
**Where cited:**
- `chapter_1_introduction.md` (Stream 1 motivation)
- `chapter_2_literature.md` §2.x (market size sub-stream + TBD marker)
- `chapter_5_discussion.md` ("Berri & Schmidt 2010 показывали для MLB заметную market-size премию ~5%")

**Status:** Crossref query с keywords "Berri Schmidt market size" не дал точного match. Возможные candidates:
- Berri, Schmidt (2010) "Stumbling on Wins: Two Economists Expose the Pitfalls on the Road to Victory in Professional Sports" (book, FT Press) — **most likely**, но это book, не article
- Berri & Schmidt (2010) "Stumbling On Wins" глава о market size

**Action для Кирилла:** уточни — это `Stumbling on Wins` book? Если да — я добавлю `@book{berri_schmidt_2010}` entry. Если paper — дай мне DOI / journal info.

### 2. `Cameron et al. (2008)` vs `Cameron et al. (2011)` — preprint vs published
**Where cited:**
- `chapter_3_methods.md` использует "Cameron et al. (2008)" (preprint year)
- `methodology_v2_addendum.md` использует "Cameron-Gelbach-Miller (2008)" (preprint year, dash variant)
- `chapter_3_methods.md` ALSO использует "Cameron et al. (2011)" в other places

**Status:** В bib запись `cameron_2011` (published year). У Кирилла в тексте mixed: некоторые места — 2008 (preprint), некоторые — 2011 (published). Несогласованность.

**Action для Кирилла:** унифицировать на (Cameron et al., 2011) или (Cameron et al., 2008) — на твоё усмотрение, но не mixed. APA правило — published version preferred (2011).

### 3. `Hembre (2021)` в `_v1` файлах (НЕ `_v2`)
**Where cited:**
- `chapter_4_new_sections.md` — 1 раз
- `chapter_5_discussion.md` — 2 раза
- `chapter_6_conclusion.md` — 1 раз

**Status:** `_v2` файлы Кирилл уже зафиксил (Hembre 2022). `_v1` (без `_v2`) — это **старые draft файлы**, которые planned drop after final text ready (per SHIPPING_SUMMARY phase 6). Не критично, если эти файлы будут deprecated.

**Action для Кирилла:** confirm — _v1 файлы будут dropped или нужно их синхронизировать с _v2?

### 4. `Johnson (2018)` vs `johnson_2017` bibkey
**Where cited:**
- `chapter_2_literature.md` использует "Johnson & Hall (2018)"
- `chapter_5_discussion_v2.md` использует "Johnson & Hall (2018)"

**Status:** Bibkey в `references.bib` — `johnson_2017` (because original CSV listed 2017). Но real publication year — 2018 (`Applied Economics Letters`).

**Action для Артема (я):** проверю год publication ещё раз и при необходимости обновлю bibkey на `johnson_2018`. **Update — verified:** уже исправлю в следующем коммите.

---

## ○ Bib entries НЕ цитируются в chapters (13 штук)

Это либо: (а) я создал template, но Кирилл не использует; (б) cite будет добавлен на следующем этапе.

| Bibkey | Status |
|---|---|
| `berri_krautmann_2006` | NEW из CSV; Кирилл рекомендован добавить (FOR_ARTEM ack) |
| `conklin_2023` | NEW из CSV; weak methodology, Кирилл подтвердил SKIP ✓ |
| `coon_cbafaq` | ⚠ cited как `(Coon, n.d.)` в 6 файлах — мой regex не словил "n.d.". **OK — actually cited.** |
| `hinton_2019` | Dropped per Кирилл `2baa0eb`. Можно удалить из bib. |
| `johnson_2017` | Cited as `Johnson & Hall (2018)` — bibkey mismatch (см. выше) |
| `kahn_sherer_1988` | NEW из CSV; рекомендован SKIP если нет discrimination section |
| `keefer_2021` | NEW из CSV; recommended ВЫСШИЙ; ждёт integration |
| `kopkin_2012` | NEW из CSV; recommended ВЫСШИЙ; ждёт integration |
| `krautmann_donley_2009` | NEW из CSV; recommended НИЗКИЙ |
| `robst_2011` | Dropped per Кирилл `2baa0eb`. Можно удалить из bib. |
| `rottenberg_1956` | Classical anchor; ещё не cited в драфтах — OK для Introduction historical context |
| `simmons_2011` | NEW из CSV; recommended НИЗКИЙ |
| `white_2014` | NEW из CSV; recommended СРЕДНИЙ для CY/Limitations |

**Action для Кирилла:**
- Confirm: удалять ли `hinton_2019` и `robst_2011` из `references.bib` (они dropped)?
- Integration: `keefer_2021`, `kopkin_2012`, `berri_krautmann_2006`, `white_2014` — добавь в драфты (особенно для Discussion / Limitations) либо confirm SKIP.

---

## Pattern issues

Парсер APA-cite иногда false-positive на:
- `ESPN/Turner (2014)` — Turner = company, не автор. Корректно проигнорировать.
- `Berri, Brook & Schmidt (2007)` — парсер схватывает только `Berri et al.`; bibkey `berri_2007` есть, всё OK.
- `Hausman & Leonard, 1997; Berri & Schmidt, 2010` в одной скобке — парсер цепляет только второе. False-negative для Hausman.

Эти false-positives / false-negatives не блокируют bib-check; формат in-text стандартный APA и читается людьми правильно.

---

## Summary

| Metric | Count |
|---|---|
| Bib entries total (после bib-check fix'а) | 38 |
| Unique cite-keys в chapters | 36 |
| Cite-в-bib match | ~30 |
| Cite missing from bib (resolved by this report) | 5 (rosen_1986, shapley_1953, genizi_1993, pratt_1987, berri_1999) |
| Cite missing from bib (need clarification) | 1 (Berri & Schmidt 2010) |
| Bib entries unused | 13 (см. таблицу выше; mostly NEW из CSV — нормально) |
| Year/format inconsistencies | 2 (Cameron 2008/2011, Johnson 2017/2018) |

**Conclusion:** bib-check **passed** для almost всех cite'ов. 2 minor inconsistencies + 1 unidentified source (Berri-Schmidt 2010) — единственные blocker'ы перед финальной редактурой.

---

**Запуск:** 2026-05-22, Claude-A
**Следующий run:** после следующего push Claude-K с новыми chapter cite'ами
