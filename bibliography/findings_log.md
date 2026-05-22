# Журнал критических находок из bibliography

> Записываются «surprising» находки от коллеги при разборе источников — те, что меняют наши claims, citations или интерпретацию. Это **не** полный лог библиографии (для этого есть `sources/`), а только substance-affecting items.

---

## Batch 1: top-5 источники (2026-05-22, PR #1)

### Hembre (2021) — CITE ERROR + NBA-only INSIGNIFICANT

**Что было:** в `bibliography_proposal.md` источник был обозначен как:
- Title: *Tax Competition in Professional Sports: A Theoretical and Empirical Analysis*
- DOI: 10.1177/1527002520968551

**Что найдено:**
- DOI возвращает 404 в Crossref (проверено 2026-05-22).
- Preprint доступен на SSRN 2946169 под title *State Income Taxes and Team Performance* (revised February 2021).
- Возможно published title в JSE отличается; нужно verify через Sage.

**Что важнее (substance):**
- **NBA-specific coefficient в Hembre НЕ значим** (β_NBA ∈ [−0.143, −0.069], SE > 1.1, Table 3, p. 20).
- Главный effect Hembre — pooled across 4 leagues (NFL/NBA/NHL/MLB), не специфически про NBA.

**Применённые правки в драфтах:**
- `analysis_v2/reports/bibliography_proposal.md` — title + DOI + caveat исправлены.
- `analysis_v2/reports/chapter_6_conclusion_v2.md` §6.2 Вывод 3 — формулировка изменена: теперь не "согласуется с Hembre" а "Hembre даёт theoretical channel, совместимый с направлением; NBA-specific coefficient у него imprecise".
- `analysis_v2/reports/chapter_6_conclusion_v2.md` §6.4 — добавлен пункт 6 про market vs tax channel не разложение.

**Не правлены (исторические/устаревшие):**
- `analysis_v2/reports/SHIPPING_SUMMARY.md`, `phase3_summary.md`, `h8_notes.md`, `chapter_4_new_sections.md` — internal notes, не идут в финальный текст.
- `analysis_v2/reports/chapter_5_discussion.md` — будет переписан целиком при работе над Discussion (после получения остальных источников); править сейчас по точке не имеет смысла.
- `analysis_v2/reports/abstract.md` — потребуется правка перед финалом, отметить в TODO.

**Open question от Артёма:** есть ли у нас joint spec с continuous `state_tax_rate` + `top5_market` в одной модели?
**Ответ:** нет. В `analysis_v2/m1_full.py:159` `STRUCT_BLOCK = ["post_cba_2017", "post_covid", "no_income_tax"]` — только бинарный `no_income_tax`. Continuous `state_tax_rate` использовался только в v1 M2c (без top5_market). Прямая декомпозиция market vs tax channels — future robustness work, отмечена в §6.4 пункт 6.

---

### Lipovetsky & Conklin (2001) — PAYWALL

**Что:** Wiley paywall, preprint / open access version не найден.

**Применённые правки:** пока никаких — методологическое описание Shapley в `chapter_3_methods.md` §3.6 опирается на standard formula (Shapley 1953), не требующую verbatim из L&C 2001. Caveat о paywall будет отмечен при подготовке Bibliography.

**Альтернативный source если verbatim quotes понадобятся:** Grömping, U. (2007). Estimators of relative importance in linear regression based on variance decomposition. *American Statistician, 61*(2), 139–147. — open access secondary review с подробным описанием Shapley R² method.

**Action:** Karolina может попробовать через HSE library proxy (Wiley доступ).

---

### Cameron-Gelbach-Miller (2011) — OPEN QUESTION

**Что:** полный PDF + точные page-references есть. Артём отметил open question: используем ли мы two-way clustering где-то?

**Ответ:** проверено в коде: only one-way clustering на `player_id` (см. `analysis_v2/m1_full.py`, `analysis_v2/h_decomposition.py`). Two-way (player + season) НЕ используется. CGM 2011 цитируется per their **general framework + eq. (2.7) one-way formula**, не per two-way innovation.

**Применённые правки:** в `chapter_3_methods.md` §3.5.1 цитата CGM 2011 уже корректна — обоснование cluster-robust SE. Никаких изменений не требуется.

**Action:** если будет финальное предложение от Артёма попробовать two-way (для robustness), можно добавить как `M1c_full_2wayCluster` спецификацию. Пока — не делаем.

---

### Rosen (1981) — OK

**Что:** полный PDF, верифицированные quotes, p. 845/849/857.

**Применённые правки:** никаких — в Methods/Results я не цитировал Rosen, он пойдёт в Introduction (motivation про superstar economics) и Lit Review Stream 1, когда сяду за них.

**Notes для future use:**
- Quote "A person who is twice as talented as another earns four times more money" (p. 849) — отличный кандидат в Introduction.
- Marshall quote (p. 857) — кандидат на эпиграф к Discussion.

---

### Coon CBA FAQ — OK

**Что:** полный snapshot HTML, Q-numbers (Q23 max tiers, Q24 Designated Player, Q32 Bird rights, Q18 luxury tax).

**Применённые правки:** никаких сейчас. Будут добавлены в Methods §3.4 при финальной редактуре (конкретные ссылки на Q-numbers вместо общего "(Coon, n.d.)" cite).

**Important context:** Larry Coon retired May 2025, FAQ frozen. Snapshot сохранён локально (`bibliography/pdfs/coon_cbafaq_snapshot_2024.html`) для reproducibility.

---

## Batch 2: ожидается ...

Когда придёт следующий push с COLLAB.md + 5 PDF + 6 шаблонов — добавим сюда.
