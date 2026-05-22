# Krautmann (1999) — What's Wrong with Scully-Estimates of a Player's Marginal Revenue Product

> ⚠ **Skeleton — paywall:** статья за Wiley paywall (DOI 10.1111/j.1465-7295.1999.tb01435.x); preprint / open access не найден после поиска через SSRN, ResearchGate, MPRA, DePauw University (Krautmann's institution). Шаблон заполнен на основе verified abstract (Wiley + Gale open metadata), follow-up paper Krautmann (2013) "What Is Right With Scully Estimates" (open access в Sage), и summary в Sandy-Sloane-Rosentraub "Economics of Sport". **Перед финальным цитированием — попробовать HSE library proxy.**

---

## 1. Citation (APA)

Krautmann, A. C. (1999). What's wrong with Scully-estimates of a player's marginal revenue product. *Economic Inquiry, 37*(2), 369–381. https://doi.org/10.1111/j.1465-7295.1999.tb01435.x

---

## 2. Source metadata

- **Type:** methodological + empirical (econometric critique с replication)
- **Sample:** MLB players, free-agent contract data (1990s); replication/critique Scully (1974) AER methodology
- **Method:** critique Scully two-stage approach (stage 1: regress team revenue on team performance; stage 2: regress team performance on individual stats; product gives MRP estimate); proposes alternative direct estimation through free agent contract data
- **Pages used in this summary:** abstract; secondary summary via Krautmann (2013) follow-up
- **DOI / URL:** https://doi.org/10.1111/j.1465-7295.1999.tb01435.x
- **Access status:** paywall
- **Local file:** — (не скачано)

---

## 3. Use mapping (КРИТИЧНО для интеграции)

- **Stream:** Г (NBA empirics classic) — primarily MLB, но методологическая критика applicable to NBA Mincer-style estimates
- **Section in coursework:** Methods §3.x (methodological critique productivity-salary regressions); Limitations §6.x (caveat про interpretation β_performance coefficients as MRP); Discussion §5
- **Supports hypothesis(es):** не support — provides methodological warning против over-interpreting performance coefficient
- **Specifically supports argument:** Krautmann critique сigh of standard Scully (1974) approach к estimating player MRP through two-stage team-revenue regression. Argument: Scully's method assumes constant returns to team quality (linear stage 1) which is empirically wrong (concave); estimates therefore systematically biased. Krautmann proposes alternative using free-agent contracts directly (revealed-preference approach: free agent salary ≈ MRP under competitive bidding). **For our work:** important methodological caveat для interpretation наших β_ppg, β_WS, β_BPM — мы не estimate true MRP; мы estimate **regression coefficient на log-salary, conditional on institutional structure** (cap, contract tiers). Это NOT same as MRP. Krautmann's revealed-preference approach via free agent contracts — applicable analogue для NBA: коэффициенты, измеренные исключительно на free-agent transactions, ближе к MRP, чем full-sample regression.

---

## 4. Core thesis (3-5 предложений)

Krautmann argues, что standard Scully (1974) method для estimating player MRP — using two-stage approach (team revenue ~ team performance; team performance ~ individual stats) — produces biased estimates because (a) stage 1 assumes linear revenue-performance relationship (empirically concave: marginal revenue declines with team wins), (b) stage 2 ignores team-specific multipliers и position-specific value, (c) results give MRP estimates где highest-paid players appear grossly underpaid (~50%+ below "MRP") — implausible given competitive free-agent market. Krautmann proposes alternative: **revealed-preference approach** — observe what teams actually pay for free agents in competitive bidding и use this as MRP measurement. Free-agent salaries provide market-clearing prices that should equal MRP under perfect competition. Applied to MLB, his alternative produces «much more reasonable estimates» — closer alignment with observed salaries. **Implication:** prior literature dramatically overstated owner monopsony rents.

---

## 5. Key claims for our text (нумерованный список)

1. **Scully method biased systematically downward:** Scully-style estimates suggest top players paid 50%+ below MRP, which is implausible в competitive free-agent market. **For us:** caveat — our regression coefficients не identify true MRP; they conflate productivity, signaling, institutional rents, and bargaining.

2. **Revealed-preference alternative:** use free-agent salary as MRP measurement; observed transactions = market-clearing prices. **For us:** suggests robustness specification — restrict sample to free-agent year players only, see if β_ppg changes substantially.

3. **Functional form criticism:** team revenue-performance relationship concave (diminishing returns to additional wins); linear stage 1 specification biases downwards. **For us:** parallel concerns — our Mincer linear-in-performance spec may underestimate marginal value at performance tails; нелинейная spec возможна но не центральная.

4. **Free-agent market efficiency assumption:** Krautmann's alternative requires competitive bidding among teams. **For us:** in NBA с cap binding, free-agent market not strictly competitive — top teams cannot exceed cap to bid up max free agents. Krautmann critique partial applicable.

5. **Implication для policy literature:** if salaries closer to MRP (Krautmann), salary cap not solving large monopsony rent — alternative justifications needed (competitive balance, league financial stability). **For us:** parallel к interpretation H7 anti-marketability: if "discount" не reflects monopsony, alternative explanations (Hembre tax, Hausman-Leonard endorsements) more compelling.

---

## 6. Direct quote candidates (с page numbers)

> ⚠ Full text за paywall; verbatim из abstract (verified open):

> "Estimates of baseball players' marginal revenue product, derived from the methodology introduced by Gerald Scully over 20 years ago in the *American Economic Review*, suggest that even the highest-paid players are grossly underpaid. However, given the fiercely competitive bidding process for free agents, it is hard to believe that owners can maintain salaries significantly below marginal revenue product. As an alternative, this paper proposes an approach for estimating a player's economic value that uses market information gleaned from free agent contract negotiations. Applied to the less-mobile segment of the player market, this approach yields much more reasonable estimates of players' marginal revenue products." (Abstract)

> **For our text (safe formulation):**
> "Krautmann (1999) critiques the Scully (1974) MRP estimation framework, arguing that revealed-preference approaches using free-agent transactions yield more reliable estimates than two-stage regressions. Our Mincer-style coefficients should not be interpreted as MRP estimates per se, but as conditional associations within the institutional structure."

---

## 7. Methodological notes

- **Method name:** revealed-preference MRP estimation (Krautmann alternative to Scully)
- **Key formula / definition:** не extracted (full text paywalled); standard description: MRP_player ≈ free-agent-contract-salary, conditional на competitive bidding
- **Key assumption(s):**
  - Competitive bidding among teams for free agents
  - Free-agent market clearing prices = MRP
  - Sample restriction к free-agent players (not extensions / restricted free agents)
- **Where applicable in our work:** не immediately применима; наш main spec uses full-sample (free agent + extension + rookie scale). Robustness possibility: restrict sample к free-agent year players, replicate H1 coefficients.
- **Caveat / pitfall:** в NBA cap binding для top teams → free-agent market не strictly competitive → Krautmann's alternative also biased в high-cap-utilization era

---

## 8. Limitations / caveats

1. **MLB-specific:** Krautmann's empirical analysis on baseball; NBA institutional differences (cap binding, max contracts) limit direct generalizability.
2. **Revealed-preference requires competitive market** — NBA cap restricts; «competitive free-agent market» assumption partially violated.
3. **Free-agent self-selection bias** — players choosing free agency disproportionately high-quality, recently outperforming; sample не representative.
4. **No formal model** — Krautmann's alternative descriptive, не theoretical foundation comparable Scully's stage-1/stage-2 model.
5. **Backlash:** Bradbury (2007) и others have critiqued Krautmann's free-agent approach as similarly biased; debate ongoing (see Krautmann 2013 follow-up).

---

## 9. Connection to our findings

**EXTENDS / CAVEATS (methodological warning для interpretation H1 results).** Krautmann не directly support / contradict наши findings — он provides cautionary framework for interpretation.

Прямое отображение:
- **H1 (β_ppg = +0.04 v1 / +0.07 within mid_level v2):** by Krautmann's logic, this coefficient does NOT identify pure productivity premium — it conflates MRP, signaling value, и institutional rents. Within mid_level tier (more competitive sub-sample), coefficient larger because closer to "free-agent" market.
- **H3 (R² tier-only = 0.85):** Krautmann would likely interpret — institutional layer dominantly determines salaries, not market-pricing; institutional rents much greater than monopsony rents.
- **H5/H6 (awards channel):** Krautmann's free-agent framework — awards (All-NBA) — signal influencing free-agent negotiation outcome; our finding β_all_nba_lag1 = +0.185 may overstate true productivity premium (it conflates productivity ↑ + signaling boost).

Для Limitations:
- "Following Krautmann (1999), мы emphasize, что our performance coefficients are NOT MRP estimates — они are conditional associations within the institutional structure imposed by NBA salary cap"
- "Robustness extension (future work): restrict sample к free-agent year players, where pricing closest to competitive market-clearing"

Для Discussion:
- "Our finding institutional layer (R² tier-only = 0.85) is consistent with Krautmann's (1999) implication, что institutional rules dominantly determine salary structure в NBA — pure productivity-based MRP estimates likely overstate market efficiency role"

---

## 10. Reading notes / questions for follow-up

- **PDF acquisition:** HSE library proxy (Wiley). DePauw University faculty page может host preprint — check faculty.depauw.edu/akrautm.
- **Follow-up paper:** Krautmann (2013) "What Is Right With Scully Estimates of a Player's Marginal Revenue Product" *Journal of Sports Economics* — partially open access; rebuttal to critics; contains updated free-agent analysis. Good alternative citation if original unavailable.
- **Adjacent MRP literature:**
  - Scully (1974) AER — original two-stage paper
  - Bradbury (2007, 2013) — critique Krautmann
  - Berri-Schmidt-Brook (2007) — survey MRP estimation issues
- **Для нашей курсовой:** Krautmann цитируется в Limitations (один абзац) для caveat про MRP interpretation; не central reference. Возможно tangentially в Methods для discussion functional form.

---

**Заполнено:** 2026-05-22 (skeleton; paywall)
**Заполнил:** Artem (collaborator)
