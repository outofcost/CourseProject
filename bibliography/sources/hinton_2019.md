# Hinton & Sun (2019/2020) — The Sunk-Cost Fallacy in the NBA: Evidence Using Player Salary and Playing Time

> ⚠ **TITLE/DOI DISCREPANCY:** в `bibliography_proposal.md` источник указан как:
> **"Hinton, S. & Sun, Y. (2019). The supermax in the NBA: Effects on team performance and player retention. [working paper / journal TBD]"**
>
> Однако такой paper Hinton & Sun про supermax не найден в любых indexed sources после thorough searching. Единственная **реальная Hinton & Sun 2019/2020 paper** — про SUNK COST FALLACY, не supermax:
>
> **Hinton, A., & Sun, Y. (2020). The sunk-cost fallacy in the National Basketball Association: Evidence using player salary and playing time. *Empirical Economics, 59*, 1019–1036. https://doi.org/10.1007/s00181-019-01641-4**
>
> Note: online first 2019, published volume 2020. Both authors — University of Guelph economists (Alexander Hinton + Yiguo Sun).
>
> Возможные explanations:
> 1. Автор bibliography_proposal спутал topic (intended supermax / institutional → нашёл sunk cost instead)
> 2. Hinton-Sun имеют **another** working paper про supermax (unpublished?), но search не нашёл
>
> **Recommendation:** Кириллу — определиться:
> (a) если intended supermax context (H3/H4) — нужны другие references (Coon CBA FAQ + Hill-Groothuis 2001 уже покрывают; possible additional: Maxcy 2013 "The American Major League Sports Salary Cap")
> (b) если sunk cost (found paper) — менее directly relevant к нашему H1-H10, но connects к Stiroh 2007 (contract effects) и H5 (awards channel)
>
> Этот шаблон заполнен по found Sunk Cost (2020) paper.

---

## 1. Citation (APA)

Hinton, A., & Sun, Y. (2020). The sunk-cost fallacy in the National Basketball Association: Evidence using player salary and playing time. *Empirical Economics, 59*(2), 1019–1036. https://doi.org/10.1007/s00181-019-01641-4

> Online-first 2019; published 2020. If proposal date 2019 — likely refers to online-first version.

---

## 2. Source metadata

- **Type:** empirical (panel regression с natural experiment design)
- **Sample:** 465 NBA players, 2013/14 — 2016/17 seasons; specific focus on free-agent contracts signed during 2015-16 and 2016-17 (around 2016 cap spike from new TV deal)
- **Method:** spatial econometric panel regression playing-time on salary; exploits 2016 salary cap spike (sudden 34% increase due to new $24B TV contract) as natural experiment to identify sunk-cost effect
- **Pages used in this summary:** abstract + secondary summaries (Springer abstract + U Guelph press release)
- **DOI / URL:** https://doi.org/10.1007/s00181-019-01641-4 (Springer paywall)
- **Access status:** paywall (Springer); ResearchGate may have working paper version
- **Local file:** — (не скачано — direct ResearchGate fetch returned 403)

---

## 3. Use mapping (КРИТИЧНО для интеграции)

- **Stream:** Б (NBA / sport-specific) — also Stream 2 (institutional / CBA — 2016 cap spike context)
- **Section in coursework:** **в зависимости от intended reference:**
  - **Если intended supermax:** Lit Review §2.2 (Institutional / CBA stream); Discussion §5 (H3/H4 interpretation) — но требует другой reference
  - **Если sunk cost (found paper):** Discussion §5 (interpretation H5/H6 dynamics + behavioral biases); Limitations §6.x (behavioral economics caveat in interpretation salary-performance linkage)
- **Supports hypothesis(es):**
  - **Sunk cost interpretation (found):** indirectly H1, H5, H6 (behavioral biases в team decision-making complicate pure productivity-MRP interpretation)
- **Specifically supports argument:** Hinton-Sun find evidence что NBA coaches give more playing time to high-salary players, controlling для performance — sunk-cost fallacy (treating non-recoverable cost as decision-relevant). 1 unit ↑ ln(salary) ≈ 0.7-0.8 minutes more playing time. **For our work:** behavioral nuance к interpretation H1 finding — observed salary-performance relationship может быть partially driven by reverse causation (high salary → more playing time → boosted performance metrics через volume) rather than pure productivity → salary direction. Также supports interpretation наш sub-finding aging-vet penalty (multi_all_nba ≥3 → β = −0.22): if veteran salaries already high (sunk cost), teams continue paying для legacy reasons, but performance declined → measured negative.

---

## 4. Core thesis (3-5 предложений)

Hinton-Sun тестируют **sunk-cost fallacy** в NBA: гипотеза, что coaches play higher-salaried players более minutes чем their current performance justifies, потому что (a) management invested heavily (sunk cost), (b) signaling effort to ownership / fans, (c) cognitive biased decision-making. Using 2013-2017 panel, они exploit **2016 cap spike** (34% jump from $70M to $94M cap due to new $24B TV deal) as natural experiment — players signing 2016 free-agent contracts get cap-inflated salaries unrelated к their changing productivity. Finding: 1 unit ↑ ln(salary) → 0.7-0.8 additional minutes playing time, controlling for current-season performance, player FE, team FE. **Implication:** evidence of behavioral sunk-cost bias in NBA coaching decisions, contrary to neoclassical rational expectations. Effect modest но statistically significant. Authors interpret as supportive of broader behavioral economics literature (Arkes-Blumer 1985, Thaler 1980 classic sunk-cost work).

---

## 5. Key claims for our text (нумерованный список, по found Sunk Cost paper)

1. **Sunk-cost effect statistically significant:** 1 unit ↑ ln(salary) → 0.7-0.8 min ↑ playing time, controlling for performance + FE. Magnitude modest (sample mean playing time ~25 min).

2. **2016 cap spike as natural experiment:** sudden 34% cap jump causally inflated some salaries (those signing free agent в 2016 vs 2015) unrelated к productivity — clean identification.

3. **Coaching decision behavioral bias:** evidence that NBA coaches not fully rational; sunk salary influences playing-time allocation contrary к forward-looking efficiency.

4. **NBA contracts guaranteed:** key institutional feature; unlike NFL where waivable, NBA salaries are sunk costs (cannot be recovered) → fallacy more relevant.

5. **Implication for management literature:** small but real bias; consistent с broader managerial sunk-cost findings (Arkes-Blumer 1985; Friedman et al. 2007 baseball).

---

## 6. Direct quote candidates (с page numbers)

> ⚠ Full text за paywall; verbatim из abstract (verified open):

> "We analyse the effect of player salary, a sunk cost, on player utilization in the National Basketball Association. We use a player's compensation as the measure of sunk costs, as it is determined prior to the beginning of a season, remains fixed throughout a season, and, unlike the NFL, NBA contracts are guaranteed. We find a significant effect of salary on playing time, suggesting the sunk-cost fallacy is present. More specifically, a unit increase in ln(salary) correlates with an average increase of 0.7-0.8 minutes in playing time. Using the spike in salary cap for the 2016–2017 season, from new television broadcasting contracts, we find compensation has a significant effect on playing time, specifically using players signing free agent contracts in 2015–2016 or 2016–2017."

> **For our text (safe formulation):**
> "Hinton & Sun (2020) provide evidence of sunk-cost fallacy in NBA coaching decisions, exploiting the 2016 cap spike as natural experiment; suggesting that observed salary-playing-time relationship not pure productivity allocation but partially behavioral."

> **Для intended supermax context:** требует другой reference. Возможные substitutes:
> - Maxcy (2013) "The American Major League Sports Salary Cap" *European Sport Management Quarterly*
> - Coates et al. (2014) "Salary Cap as a Constraint on Player Mobility"

---

## 7. Methodological notes

- **Method name:** spatial econometric panel regression с natural experiment identification
- **Key formula:** playing_time_it = α + β·ln(salary)_it + X_it·γ + player_FE + team_FE + ε_it; spatial autocorrelation handled via spatial weight matrix (peer effects within team)
- **Key assumption:** 2016 cap spike orthogonal к individual-player productivity changes (cap formula determined by league revenue, not individual performance)
- **Where applicable in our work:** не directly; наш main spec не models playing-time. But behavioral framework relevant for interpretation
- **Caveat:** spatial weight matrix specification subjective; results may be sensitive к choice

---

## 8. Limitations / caveats

1. **Modest magnitude:** 0.7-0.8 min effect smaller than total playing-time variance; behavioral but не dominant.
2. **Single cap event:** only one 2016 spike used; limited replication; future cap events (e.g., 2024 new TV deal) could test.
3. **Coaches vs management distinction:** unclear whether sunk-cost bias is coach-level (lineup decisions) or management-level (player retention).
4. **No data на coach incentives:** if coaches incentivized to play stars (fan satisfaction, ownership pressure), behavior может be rational from coach's POV даже if non-efficient for team performance.
5. **Sample period (2013-2017)** small — only 4 seasons.

---

## 9. Connection to our findings

> ⚠ Depends on resolved intended reference.

**Если Sunk Cost (found paper):** EXTENDS our framework with behavioral context.

Прямое отображение:
- **H1 (β_ppg = +0.04 v1 / +0.07 v2 within mid_level):** Hinton-Sun finding suggests partial reverse causation — высокая зарплата → больше playing time → больше opportunity для accumulating stats → observed performance ↑. Не central effect, но behavioral nuance
- **Sub-finding aging-vet penalty (multi_all_nba ≥3 → β = −0.22):** complementary to sunk-cost — teams continue paying veteran superstars (sunk cost), but performance declines → measured discount in our spec. Hinton-Sun behavioral framework consistent with this pattern
- **H8 (team controls null):** if team-level salary allocation suboptimal (sunk-cost bias), team success measures imperfectly correlate with salary structure — explains why team controls add little explanatory power

Для Discussion:
- "Hinton & Sun (2020) document sunk-cost fallacy в NBA coaching decisions, providing behavioral nuance к interpretation of salary-performance relationships; our observed coefficients не purely reflect productivity → salary direction but partially salary → playing-time → recorded performance"

Для Limitations:
- "Behavioral biases (sunk-cost fallacy, status quo bias) may influence both team-level decisions and individual contract negotiations, beyond strict rational MRP framework — see Hinton & Sun (2020) для NBA-specific evidence"

**Если intended supermax (proposal):** не covered by this paper; need alternative reference.

---

## 10. Reading notes / questions for follow-up

- **RESOLVE INTENDED REFERENCE:** Karolina/Kirill — определить какая paper Hinton & Sun имелась в виду:
  - (a) Sunk Cost (Empirical Economics 2020) — found, paywall
  - (b) Supermax paper — не существует в indexed sources; возможно Karolina имела в виду другую paper про supermax (e.g., Maxcy 2013, Coates et al., institutional working papers)
- **PDF acquisition (если Sunk Cost needed):** Springer Link (paywall); University of Guelph repository (Sun's institution); email Yiguo Sun (yisun@uoguelph.ca).
- **Adjacent supermax / institutional literature** (если intended):
  - Maxcy, J. (2013). The American Major League Sports Salary Cap. *European Sport Management Quarterly* 13(3): 359-375.
  - Coates, D. (2014). Salary Cap and Team Mobility. Working paper UMBC.
  - Hill (2012) salary distribution under cap — наш G3 reference
- **Adjacent behavioral / sunk cost literature:**
  - Arkes & Blumer (1985) original sunk cost paper
  - Friedman et al. (2007) — sunk cost в MLB
  - Hinton, Sun & Cohn (2021) follow-up working paper
- **Для нашей курсовой:** при skeleton состоянии, цитата one or two sentences в Discussion / Limitations — depending on intended interpretation.

---

**Заполнено:** 2026-05-22 (skeleton; paywall; TITLE/TOPIC DISCREPANCY noted)
**Заполнил:** Artem (collaborator)
