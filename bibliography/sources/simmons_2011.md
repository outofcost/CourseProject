# Simmons & Berri (2011) — Mixing the Princes and the Paupers: Pay and Performance in the NBA

> **НЕ** в `bibliography_proposal.md`; рекомендуется к добавлению как СРЕДНИЙ приоритет (новый источник из CSV-анализа). Прямой mainstream NBA-labor paper о pay inequality и productivity.

---

## 1. Citation (APA)

Simmons, R., & Berri, D. J. (2011). Mixing the princes and the paupers: Pay and performance in the National Basketball Association. *Labour Economics, 18*(3), 381–388. https://doi.org/10.1016/j.labeco.2010.11.012

---

## 2. Source metadata

- **Type:** empirical (panel econometrics + natural experiment via 1996 CBA change)
- **Sample:** NBA, 1990/91 – 2007/08 (18 сезонов); team-level Gini coefficients + player-level panel. 29 NBA teams; для team-level — ~520 team-seasons; player-level выборка по сезонам после 1996 (post-CBA).
- **Method:** (1) team-level OLS на win% с decomposed Gini (predicted vs residual inequality); (2) difference-in-differences с TREAT × POST_1996 interaction (treated teams = increased inequality ≥20% после 1995–96); (3) player-level OLS на ADJP48 (Berri's wins-based metric per 48 min) с individual + team FE; (4) Salary equation как первое stage для разложения Gini на "justified" (predicted) и "unjustified" (residual) components
- **Pages used in this summary:** preprint pp. 1–10 (intro, conceptual), 12–15 (natural experiment, DiD), 15–18 (player model, eq. 6), 19–22 (results), 22–25 (Conclusions)
- **DOI / URL:** https://doi.org/10.1016/j.labeco.2010.11.012
- **Access status:** preprint open access (Lancaster University Management School WP 2010/041; https://www.lancaster.ac.uk/media/lancaster-university/content-assets/documents/lums/economics/working-papers/PayPerformance.pdf)
- **Local file:** `bibliography/pdfs/simmons_2011.pdf` (preprint, ноябрь 2010)

---

## 3. Use mapping (КРИТИЧНО для интеграции)

- **Stream:** Б+ (NEW — proposed addition from CSV analysis). NBA-specific empirical
- **Section in coursework:** **Lit Review §2.3 (awards / signaling)** или §2.4 (market / team context) — как контекст для inequality vs productivity взаимосвязи; **Methods §3 / Discussion §5** — обоснование Berri's productivity metric (ADJP48) как альтернативы PPG и PER; **Discussion §5.x** — если зайти в тему дисперсии payroll по teams
- **Supports hypothesis(es):**
  - **H1** (performance ↔ salary) — косвенно: salary equation как первое stage показывает что PPG доминирует над wins-based metrics — параллель нашему observation что PPG-coefficient устойчив (β_ppg = +0.04 в v1)
  - **H8** (team success → individual premium) — extends: paper показывает что tournament-style inequality (expected/predicted Gini) положительно связана с player productivity, но conditional Gini (residual) — null. Это нюанс для интерпретации нашего team-controls null
- **Specifically supports argument:** (1) Эта статья — один из канонических Berri NBA-labor papers, на основе которого построена productivity metric ADJP48 = wins per 48 min. Цитируется в нашем v2 для обоснования почему PPG ≠ единственный proxy таланта. (2) Главный нативный вывод — "salary primarily driven by points scored, not wins" — это ровно та же мысль, что в нашем H1 и Berri-Krautmann (2006); образует устойчивый эмпирический пласт. (3) Discussion о CBA 1996 watershed — это парallel наш H4 (CBA 2017 break).

---

## 4. Core thesis (3-5 предложений)

Авторы исследуют эффект внутрикомандной pay inequality (Gini coefficient зарплат) на team-level и player-level performance в NBA, используя CBA 1996 как natural experiment (часть teams резко увеличили inequality, часть нет). Главный методологический ход — декомпозиция Gini на **predicted** ("justified" by player skill) и **residual** ("unjustified") компоненты через salary equation на основе performance metrics. Через player-level panel regression (ADJP48 на personal X-controls + decomposed Gini + treatment interaction) находят: (а) **predicted Gini** имеет positive effect на player productivity — consistent с tournament theory (Lazear-Rosen 1981); (б) **residual Gini** essentially orthogonal к performance — counter к "fairness/cohesion" hypotheses Levine (1991), Bloom (1999), Akerlof-Yellen (1990) для general occupations; (в) **CBA 1996 change** не имел significant treatment effect на team performance — change в pay distribution был largely "absorbed" по правилам cap, не по реальной reorganisation talent. Также подтверждается канонический Berri-finding: "salary primarily driven by points scored, not wins" — то есть GM "overpay" scoring vs win-contribution.

---

## 5. Key claims for our text (нумерованный список)

1. **Salary primarily driven by points, not wins:** "we find that player salary in the NBA is primarily driven by points scored. Fundamental factors that determine team wins (i.e. shooting efficiency, rebounds, and turnovers) are less important for player salaries" (Conclusions, p. 22). Это прямое supports наш H1 finding и raises **caveat** что β_ppg overstates "true marginal product" — PPG включает inefficient shooting.

2. **Decomposed Gini results:** "expected pay dispersion has a positive effect on team and individual performance. We find that team and individual performances are essentially orthogonal to conditional pay inequality, counter to the hypotheses of fairness and cohesion proposed in the literature" (Abstract). 

3. **Tournament theory partially supported:** "both team and player performances appear to respond positively to changes in justified inequality based on expected salaries over the whole sample period. We interpret these results as confirmation of tournament theory" (Conclusions, p. 22).

4. **CBA 1996 weak treatment:** "the effects of the natural experiment of a radical change in collective bargaining agreement implemented in 1996 were primarily to raise unjustified (conditional) pay inequality" (Conclusions, p. 22). Important параллель для нашего H4 (CBA 2017 break — но мы находим +26% effect on top tail; Simmons-Berri нашли null на performance side, что consistent если cap change → редистрибутивный, не productivity-стимулирующий).

5. **Productivity metric ADJP48 ≠ PER:** Simmons-Berri используют wins-per-48 (ADJP48), не PER. У них критика PER (NBA EFFICIENCY): "rewards shooting attempts rather than shooting efficiency" — что в свою очередь обосновывает почему в наших v2 спецификациях мы используем mix (PPG, WS, BPM), а не одну метрику.

6. **Negative teammate productivity effect:** "Berri and Krautmann (2006) offer evidence, albeit with marginal significance, that such a negative effect exists in basketball" (p. 17). Релевантно для интерпретации нашего team_win_pct null (H8) — частично потому, что individual production падает на лучших командах.

---

## 6. Direct quote candidates (с page numbers)

> "We investigate how team and individual performances of players in the National Basketball Association respond to variations in intra-team pay inequality. By breaking down team dispersion into conditional and expected components, we find that expected pay dispersion has a positive effect on team and individual performance. We find that team and individual performances are essentially orthogonal to conditional pay inequality." (Abstract, p. 1)

> "As has been demonstrated previously in the literature, we find that player salary in the NBA is primarily driven by points scored. Fundamental factors that determine team wins (i.e. shooting efficiency, rebounds, and turnovers) are less important for player salaries. In sum, there appears to be a difference between teams' perceptions of productivity and a player's actual production of wins in the determination of player salaries." (Conclusions, p. 22)

> "Both team and player performances appear to respond positively to changes in justified inequality based on expected salaries over the whole sample period. We interpret these results as confirmation of tournament theory." (Conclusions, p. 22)

> "The effects of the natural experiment of a radical change in collective bargaining agreement implemented in 1996 were primarily to raise unjustified (conditional) pay inequality." (Conclusions, p. 22)

---

## 7. Methodological notes

Не методологическая paper — applied panel econometrics. Главное методологическое заимствование, релевантное нам:

- **Two-stage Gini decomposition** — Predicted Gini estimated через player salary equation; Residual Gini — observed minus predicted. Аналогичный подход у Frick et al. (2003) для football. Идея применима к нашей работе если мы захотим декомпозировать team-payroll dispersion на "fair" и "noise" компоненты — но это extra effort post-shipping.

- **Berri's ADJP48 = Wins per 48 min** — calculated as linear combination 14 box-score stats. Не используется напрямую у нас в v2 (мы используем стандартные PPG, WS, BPM), но дает теоретическую основу: разные metrics → разные β-pattern → cap challenge of "salary cap based on PPG inflates wrong skills".

---

## 8. Limitations / caveats

1. **Endogeneity decomposed Gini:** "predicted Gini" исчисляется из salary equation, где performance — RHS. Циклическая зависимость может смещать оценки tournament effect вверх (sample selection — лучшие игроки выживают в выборке, у них больше salary spread).

2. **NBA EFFICIENCY критика — внутренняя:** authors используют ADJP48 (Berri's metric), а не PER. Это делает результаты sensitive к выбору productivity proxy. Если использовать PER (как у нас в v2 robustness), tournament effect может ослабнуть.

3. **No causal mechanism для positive tournament effect:** authors интерпретируют positive coef на predicted Gini как "tournament theory", но альтернативное объяснение — "better teams attract better players" (positive sorting), что mechanistic, не behavioural.

4. **CBA 1996 как "natural experiment":** treatment группа выбирается по post-hoc эндогенному критерию (>20% Gini increase). Это **не** exogenous variation — те же teams, которые увеличили inequality, могли иметь other unobservable изменения (новый GM, изменения coaching).

5. **Pre-2017 data:** Sample 1990–2007. До designated player (supermax) extensions; до 2011 lockout. Применимость к нашему 2015–2023 периоду — нужна с caveat.

6. **Team-level results weak DiD:** "Hence, the impact of increased pay inequality on team performance cannot be identified from our suggested natural experiment" (p. 13–14). Authors сами признают, что team-level estimation noisy.

---

## 9. Connection to our findings

**SUPPORTS / EXTENDS** — Simmons-Berri (2011) даёт два инструмента для нашей дискуссии:

(1) **Точка опоры для интерпретации β_ppg:** их вывод "salary primarily driven by points scored, not wins" — это **independent replication** того, что мы находим для post-2011 CBA: β_ppg доминирует over efficiency-based metrics. Это укрепляет внешнюю валидность нашего H1.

(2) **Reference для team-level null:** их CBA 1996 effect null + Berri-Krautmann negative teammate productivity effect — дают консистентный pattern, что **team-level controls weak predictors** individual salary (наш H8 null: win%, playoffs, luxury tax p>0.15). Можно цитировать как "consistent with established NBA literature on team-level orthogonality".

(3) **Tournament hypothesis для inequality:** Simmons-Berri находят positive effect predicted Gini → productivity. Мы это **не тестируем** (наш unit observation = player-season, не team-payroll-distribution); это идёт в **Limitations** или **Future research**: "Pay dispersion within team — potentially fruitful extension, not addressed in our specification".

(4) **CBA structural change:** наш H4 (CBA 2017 → +26% top tail) и их CBA 1996 null on performance — два разных канала: 2011/2017 CBA меняли тиерную структуру (salary caps + supermax), 1996 CBA — переход к salary cap в первый раз. Discussion может сравнить два waves: первый CBA wave (1996) → redistribution; второй wave (2011/2017) → tail-thickening.

---

## 10. Reading notes / questions for follow-up

- **Predicted impact:** **Рекомендуется к добавлению в финальную bibliography СРЕДНИЙ приоритет.** Simmons-Berri (2011) — solid NBA-labor paper, опубликован в top labor journal (Labour Economics). Полезен в Lit Review §2.4 (как backup для team-context discussion) и в Discussion §5 (если затрагиваем inequality / dispersion вопросы). Не критичен — если объём ограничивает, можно сократить до 1-line citation.

- **Возможная замена / комплементарность:**
  - Berri & Krautmann (2006) для shirking — параллельная Berri-cooperation
  - Hill (2004), Hill & Groothuis (2001) для basic salary determinants
  - Bloom (1999) для inequality-performance debate (general HR literature)
  - Frick et al. (2003) для inequality в football (методологический template)

- **Связь с нашими v2 results:** напрямую не пересекается с Shapley decomposition (это уникальный метод нашей работы). Но Simmons-Berri показывает, что NBA-literature эмпирически устоявшаяся: "PPG driven, wins не считаются". Это даёт нам spirit-уверенность что наши findings — не aberration.

- **Если будет нужно** — Simmons имеет много follow-up NBA papers с Frick, Bryson и др.; cv его проектов на Lancaster.

- **Hölmström-связь:** инuversed connection — Simmons-Berri показывает, что NBA-salary system эмпирически inefficient (rewards wrong metric). Hölmström-perspective: optimal contract под imperfect observability должен использовать ВСЕ informative signals; то, что NBA "rewards points not wins" — empirical departure от theoretical optimality, что является интересной discussion для нашего Conclusions.

---

**Заполнено:** 2026-05-22
**Заполнил:** Artem (collaborator)
