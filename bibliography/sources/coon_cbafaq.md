# Coon (n.d.) — NBA Salary Cap / CBA FAQ

---

## 1. Citation (APA)

Coon, L. (n.d.). *NBA salary cap / collective bargaining agreement FAQ* (2017 CBA edition). Retrieved May 22, 2026, from http://www.cbafaq.com/salarycap17.htm

> Note: текущая основная страница `cbafaq.com/salarycap.htm` редиректит на `salarycap17.htm` — Larry Coon официально завершил поддержку FAQ в мае 2025 г. (вышел на пенсию). Версия для CBA 2017 — последняя полностью поддерживаемая.

---

## 2. Source metadata

- **Type:** institutional reference / practitioner FAQ (non-academic)
- **Sample:** не applicable (документ-справочник)
- **Method:** не applicable
- **Pages used in this summary:** Q1, Q5, Q18 (luxury tax), Q22 (min salary), Q23 (max salary tiers), Q24 (Designated Player rule), Q32 (Bird rights)
- **DOI / URL:** http://www.cbafaq.com/salarycap17.htm
- **Access status:** open access (web)
- **Last revision (per page):** 11/5/2022 — revised questions 12, 14–25, 31, 82, 98 with figures for 2021–22 and 2022–23 seasons
- **Local snapshot:** `bibliography/pdfs/coon_cbafaq_snapshot_2024.html` (downloaded 2026-05-22)

---

## 3. Use mapping (КРИТИЧНО для интеграции)

- **Stream:** Д (institutional reference)
- **Section in coursework:** Methods §3 (data and institutional context) + Lit Review §2.2 (Institutional / CBA) — обоснование классификатора tier и cap-thresholds; Discussion §5 — institutional layer interpretation
- **Supports hypothesis(es):** H3 (tier dummies → R² = 0.85), H4 (CBA 2017 structural break), косвенно H5/H6 (через Designated Player rule, который связывает All-NBA selections с supermax eligibility)
- **Specifically supports argument:** Этот источник — единственный детальный публично доступный референс по правилам CBA 2017, на основании которого построен `analysis_v2/classify_tier.py` (8-category rule-based classifier) и определены пороги supermax_eligible_loose. Цитируется во всей NBA-экономической литературе как канонический practitioner source.

---

## 4. Core thesis (3-5 предложений)

FAQ — детальное описание правил NBA Collective Bargaining Agreement редакции 2017 года. Документ структурирован как 130+ вопрос-ответ секций: salary cap mechanics, luxury tax, max/min salary scales, Designated Player rules (supermax), exceptions (Bird, mid-level, bi-annual), trade rules, free agency. Это не академическая работа, а practitioner-oriented справочник, написанный человеком вне NBA на основе анализа полного текста CBA. Используется как стандартная ссылка в публикациях по экономике NBA, так как полный текст CBA — длинный юридический документ без публичного "user manual".

---

## 5. Key claims for our text (нумерованный список)

1. **Max salary tiers (Q23) — основание для классификатора tier:**
   - 0–6 years experience: 25% of cap
   - 7–9 years experience: 30% of cap
   - 10+ years experience: 35% of cap
   - Конкретные суммы 2022–23: $30.91M / $37.10M / $43.28M соответственно

2. **Designated Player rule (Q24) — supermax eligibility criteria:**
   - Player must qualify by ONE of: (a) All-NBA First/Second/Third Team в most recent season, либо в обоих из двух предыдущих сезонов; (b) Defensive Player of the Year в most recent season, либо в обоих из двух предыдущих сезонов; (c) NBA MVP в любом из трёх последних сезонов.
   - Этот критерий + 7–9 years experience → 30% of cap (Designated Rookie extension); 8–9 years + criteria → 35% cap (Designated Veteran "supermax")

3. **Bird rights (Q32) — основание для веса player tenure в Mincer:**
   - Full Bird rights: 3 seasons с same team (или сумма из коротких контрактов)
   - Early Bird rights: 2 seasons
   - Bird rights позволяют команде превышать salary cap при подписании своего FA → ключевой механизм для veteran salary tier

4. **Luxury tax (Q18) — основание для team-level over_luxury_tax индикатора:**
   - Tax level = 53.51% × projected BRI − projected benefits, ÷ 30 teams
   - Прогрессивная шкала: $0–$5M over → $1.50/$ для non-repeater, $2.50/$ для repeater (3 из 4 предыдущих сезонов)
   - $20M+ over → $3.75/$ + $0.50 за каждые $5M (non-repeater), $4.75/$ + $0.50 (repeater)

5. **Minimum salary (Q22) — нижний bound для bottom-tier:**
   - Шкала по years in NBA: $1.02M (rookie 0 years) → $3.49M (10+ years, Year 5)
   - Привязка к salary cap: при росте cap на X% минимумы растут на X%

---

## 6. Direct quote candidates (с section references)

> "The performance criteria. At least one of the following must be true: The player was named to the All-NBA First, Second or Third team in the most recent season, or both of the two seasons that preceded the most recent season. The player was named the Defensive Player of the Year in the most recent season, or both of the two seasons that preceded the most recent season. The player was named the NBA Most Valuable Player in any of the three most recent seasons." (Q24, Designated Player rule)

> "Here are the league-wide maximum salaries for the first season of a new contract: 0–6 years in NBA: 25% of cap; 7–9 years: 30% of cap; 10+ years: 35% of cap." (Q23, max salary)

> "The basic idea is that a player must play for the same team for three seasons for his team to gain full Bird rights (two seasons for Early Bird rights)." (Q32, Bird rights)

> "The tax level is determined prior to the season, and is computed by taking 53.51% of projected BRI, subtracting projected benefits, and dividing by the number of teams in the league." (Q18, luxury tax)

---

## 7. Methodological notes

Не применимо — institutional reference, не методологическая работа.

---

## 8. Limitations / caveats

1. **Non-academic source:** не peer-reviewed; цитируется в академической литературе как practitioner reference, но не как первичная теоретическая работа.
2. **Возможен information drift:** правила CBA 2017 заменены CBA 2023, ряд параметров (luxury tax progressivity, supermax thresholds) изменились. Наша работа охватывает 2015/16–2023/24 → последние сезоны панели формально под действием CBA 2023, но в данных за 2023/24 supermax-extensions подписывались по CBA 2017 (контракты multi-year).
3. **Author retired:** обновление страницы прекращено; для CBA 2023 official details нужны другие источники (NBA league memos, journalism Bobby Marks / Mark Madden).

---

## 9. Connection to our findings

**SUPPORTS** — institutional foundation для H3 и H4.

Q23 (max tiers 25/30/35%) и Q24 (Designated Player criteria) — это первичный источник, из которого построены наши tier-категории в `classify_tier.py`. Headline finding H3 (tier dummies одни → R² = 0.85) интерпретируется в Discussion как доказательство того, что cap создаёт quasi-deterministic institutional layer; Coon FAQ — единственный детальный документ, формализующий эти правила, поэтому ссылка на него обязательна. Также Q24 (All-NBA / DPOY / MVP criteria) — это institutional mechanism, через который работает H5/H6 (awards channel): supermax eligibility — это формальное звено между awards и salary, не просто signaling.

---

## 10. Reading notes / questions for follow-up

- Larry Coon ушёл на пенсию в мае 2025; sites станут "frozen". Для воспроизводимости — снимок сохранён локально 2026-05-22.
- Для финальной курсовой стоит включить как ссылку в Methods §3.x (классификатор tier) И в Lit Review §2.2 (institutional). По стилю HSE — APA Web format с access date.
- Q31 (average salary), Q20 (apron / hard cap), Q53 (raises/extensions) могут пригодиться для Limitations / Methods notes; не разобраны в этом summary, но раздел в snapshot есть.

---

**Заполнено:** 2026-05-22
**Заполнил:** Artem (collaborator)
