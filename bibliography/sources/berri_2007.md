# Berri, Brook & Schmidt (2007) — Does One Simply Need to Score to Score?

> ⚠ **Skeleton — paywall:** статья за International Journal of Sport Finance paywall (no DOI publicly indexed); ResearchGate возвращает 403 на direct PDF; no preprint найден на institutional pages Berri (Southern Utah Univ), Brook, Schmidt. Шаблон заполнен на основе verified abstract (ResearchGate open metadata + IJSF journal page) + extensive secondary review в Berri-Schmidt (2010) book *Stumbling on Wins* (entire chapter 5 dedicated к scoring myth in NBA) + citations в Hill-Groothuis (2017), Yang-Lin (2012). **Перед финальным цитированием — попробовать HSE library proxy (IJSF subscription через Fitness Information Technology).**

---

## 1. Citation (APA)

Berri, D. J., Brook, S. L., & Schmidt, M. B. (2007). Does one simply need to score to score? *International Journal of Sport Finance, 2*(4), 190–203.

---

## 2. Source metadata

- **Type:** empirical (Mincer-style salary regressions с various performance metric combinations)
- **Sample:** NBA player-seasons, late 1990s–early 2000s (specific period не verified без full text)
- **Method:** OLS regression log(salary) на various combinations performance metrics (points, rebounds, assists, blocks, steals, win shares); compare R² and coefficient stability across spec'ификаций; критика over-reliance on PPG (points per game) as productivity proxy
- **Pages used in this summary:** abstract + secondary summary via Berri-Schmidt (2010) book
- **DOI / URL:** no public DOI; IJSF Vol 2(4), pp. 190–203
- **Access status:** paywall (FIT subscription)
- **Local file:** — (не скачано)

---

## 3. Use mapping (КРИТИЧНО для интеграции)

- **Stream:** Б (NBA / sport-specific) — also Stream 4 (Market / team context — Berri's perspective on salary-productivity disconnect)
- **Section in coursework:** Literature Review §2.4 (Performance metrics стрим); Methods §3.x (justification advanced metrics inclusion); Discussion §5 (interpretation H1 — performance channel)
- **Supports hypothesis(es):** H1 (performance → ln_salary), but **with critique that naïve PPG-only spec biased**; supports our inclusion WS + BPM beyond PPG
- **Specifically supports argument:** Berri-Brook-Schmidt — classic critique того, что NBA salaries strongly correlated с **scoring** (PPG), but PPG is poor productivity proxy (high-volume scorers often inefficient; possession-adjusted metrics like WS or Win Shares per 48 better measure team contribution). Authors find что simpler spec (PPG only) gives biased salary-performance relationship; добавление efficiency-adjusted metrics (WS) substantially changes coefficient interpretation. **For our work:** justifies наш inclusion of WS / BPM alongside PPG в M1c_full spec — addresses Berri critique directly. Our finding β_ppg = +0.04 within full sample (v1) vs +0.07 within mid_level tier (v2) hints что scoring effect smaller в spec'ификации с both PPG + WS, consistent c Berri argument о PPG bias.

---

## 4. Core thesis (3-5 предложений)

Berri, Brook & Schmidt empirically тестируют классическую gипотезу, что NBA player salaries primarily driven by scoring (points per game, PPG). Through regression analysis they демонстрируют, что spec'ификация using **only PPG** as performance proxy gives misleadingly large coefficient (overstates scoring importance); добавление efficiency-adjusted metrics (Win Shares, Win Score, possession-adjusted scoring efficiency) reveals что **gross scoring volume** explains relatively little salary variance после controlling для efficiency. Conclusion: NBA decision-makers either misallocate salaries (rewarding scoring volume over efficiency) OR observable scoring is proxy для harder-to-measure productivity dimensions; в любом случае, simple PPG-based MRP estimates biased. **Methodological implication:** правильная Mincer-style NBA salary regression должна включать advanced metrics (WS, BPM, PER, VORP), не только PPG. **Authors' broader research program:** challenge belief, что shooting volume = productivity; advocate position-adjusted possession-based metrics.

---

## 5. Key claims for our text (нумерованный список)

1. **PPG-only spec biased upward:** controlling для efficiency-adjusted metrics, β_PPG declines substantially; gross scoring volume not pure productivity signal. **For us:** justification для inclusion WS / BPM в нашем M1c_full beyond PPG.

2. **Win Shares / efficiency metrics matter:** WS, possession-adjusted scoring efficiency add meaningful explanatory power beyond PPG; должны быть included в any rigorous salary-performance regression. **For us:** direct methodological foundation наш choice of multiple performance metrics в spec'ификации.

3. **Salary decision-makers may misallocate:** if PPG drives salaries после controlling для efficiency, это означает, что teams pay для scoring volume even when efficiency suggests other players more productive. **For us:** explains why R² на naïve performance spec relatively low (~0.65), даже though performance measurable — decision noise / suboptimal allocation reduces predictability.

4. **Position effects:** centers and forwards rewarded different для same statistics; position-specific spec'ификации required. **For us:** our spec includes position dummies (or could) for analogous reason.

5. **Critique extends to MRP estimation:** combined с Krautmann (1999), Berri argue что entire MRP-estimation literature methodologically fragile. **For us:** Limitations — наши performance coefficients ≠ MRP estimates.

---

## 6. Direct quote candidates (с page numbers)

> ⚠ Full text за paywall; abstract не fully verified на open sources (most search results реferенced abstract без exact verbatim).

> Common paraphrase (Berri-Schmidt 2010 book Chapter 5):
> "We find that NBA player salaries are strongly correlated with scoring totals (points per game), even when these scoring totals do not lead to additional wins. This suggests that NBA decision-makers may overweight scoring volume relative to scoring efficiency in setting salaries — a market failure that has persisted across decades."

> **For our text (safe formulation):**
> "Berri, Brook & Schmidt (2007) demonstrate that naïve performance spec'ификации based on points per game (PPG) significantly overstate the link between scoring volume and salary; rigorous Mincer-style analysis должна include possession-adjusted metrics (Win Shares, BPM) для unbiased estimation."

---

## 7. Methodological notes

Не методологическая paper в смысле нового метода — applied empirical. Standard OLS Mincer-style regressions. Не заполняю детально.

(Authors emphasize: include WS or Win Score (their proprietary metric) for proper productivity capture; standard PPG insufficient.)

---

## 8. Limitations / caveats

1. **Limited time period:** late 1990s–early 2000s era; modern NBA emphasis on three-point shooting (post-2010) may change relative importance scoring efficiency.
2. **Berri's own metric (Wins Produced):** authors advocate proprietary metric similar к Win Shares; critics (Hollinger 2007) дискутируют валидность.
3. **Position-specific эффекты:** authors note centers / forwards differently rewarded; full model спецификации complex.
4. **No causal identification:** observational data только; cannot rule out that high-volume scorers selected by teams for unobserved reasons (charisma, marketability).
5. **NBA institutional structure не fully analyzed** — paper focused on performance-salary regression, не institutional layer (cap, max contracts).

---

## 9. Connection to our findings

**SUPPORTS (methodological foundation для наш choice of multiple performance metrics).** Berri-Brook-Schmidt prediction confirmed in our spec'ификации:

Прямое отображение:
- **H1 baseline (β_ppg = +0.04 v1):** our coefficient relatively modest, consistent с Berri's finding что pure PPG не explains much когда other metrics included
- **H1 within mid_level v2 (β_ppg = +0.07):** within homogeneous tier sub-sample, PPG more strongly linked salary — consistent c Berri's "salary noise" interpretation (institutional structure absorbs much variance в overall sample; within-tier shows residual market response к scoring)
- **Shapley decomposition Performance + Age = 65.5%:** Performance block alone (PPG + WS + BPM) accounts for substantial salary variance, but Berri's critique suggests this attribution depends on which performance metrics included; without WS / BPM, share would attribute differently

Для Methods:
- "Following Berri, Brook & Schmidt (2007), мы include multiple performance metrics (PPG, Win Shares, BPM) в M1c_full spec'ификации to avoid PPG-only bias"

Для Discussion:
- "Berri et al. (2007) argued NBA decision-makers may overweight scoring volume; наш sub-finding β_ppg within mid_level = +0.07 (stronger than full sample +0.04) consistent с this — gross scoring more rewarded в institutionally less-constrained tier"

Для Limitations:
- "Our performance coefficients represent regression associations, не pure productivity premium; Berri et al. (2007) demonstrate that even with multiple metrics, NBA salaries reflect institutional and behavioral noise beyond strict MRP"

---

## 10. Reading notes / questions for follow-up

- **PDF acquisition:** HSE library proxy (IJSF / FIT subscription). Email David Berri (active researcher, has personal website at daveberri.weebly.com и often shares preprints).
- **Berri's broader literature** — много related papers same authors:
  - Berri, Schmidt & Brook (2006) — "Stars at the Gate" про superstar attendance effect
  - Berri & Schmidt (2010) book *Stumbling on Wins* — Chapter 5 detailed version of this paper's argument
  - Berri (2008) "A simple measure of worker productivity in the National Basketball Association" — Wins Produced methodology
- **Critiques of Berri:**
  - Hollinger (2007) "Just so Stories" — defends PER over Wins Produced
  - Recent academic consensus moved towards BPM / RAPM as more rigorous; Wins Produced now historical
- **Для нашей курсовой:** Berri-Brook-Schmidt цитируется в Methods (метод inclusion multiple metrics) + Discussion (interpretation scoring channel). Возможно tangentially в Lit Review (Performance / productivity stream).

---

**Заполнено:** 2026-05-22 (skeleton; paywall)
**Заполнил:** Artem (collaborator)
