# Johnson & Hall (2017/2018) — Do NBA Players Need Higher Salaries to Play in High Tax States? Evidence from Free Agents

> ⚠ **PAYWALL — skeleton only.** PDF не получено: WVU Research Repository защищён AWS WAF (JavaScript challenge), Taylor & Francis published version — paywall. Содержание реконструировано по abstract на IDEAS RePEc, метаданным в WVU Repository, и cross-references из других paper'ов. Все числа в этом шаблоне marked **(from abstract — unverified)** или **(cited in)** — перед финальным цитированием в курсовой проверить по published PDF.

---

## 1. Citation (APA)

Johnson, C., & Hall, J. C. (2018). Do National Basketball Association players need higher salaries to play in high tax states? Evidence from free agents. *Applied Economics Letters, 25*(5), 359–361. https://doi.org/10.1080/13504851.2017.1324194

> **Working paper version:** Johnson, C., & Hall, J. C. (2017). Do National Basketball Association players need higher salaries to play in high tax states? Evidence from free agents (Working Paper 17-11). West Virginia University, Department of Economics. https://researchrepository.wvu.edu/econ_working-papers/3/ (PDF за AWS WAF — недоступен для curl, в task description listed as 2017 working paper)

> **Note:** task description указывает год публикации 2017 (working paper); published version в Applied Economics Letters — 2018. В нашем bibliography file именуем `johnson_2017` per task convention.

---

## 2. Source metadata

- **Type:** empirical
- **Sample:** **576 NBA free agent signings**, 2010–2014 sample period (5-year window, post-2011 CBA effective from 2011-12 onwards; sample includes 2011 lockout-shortened и following seasons)
- **Method:** OLS regression of free agent salary on **Average Tax Rate** (ATR — likely state + local, computed per signed contract location) + performance controls. Details require PDF access. Likely fixed effects on player or team (with FA only sample limited within-player variation).
- **Pages used in this summary:** abstract (IDEAS RePEc + WVU + journal page); Applied Economics Letters published 3-page note (typical for AEL — short).
- **DOI / URL:** https://doi.org/10.1080/13504851.2017.1324194
- **Access status:** **paywall** — both AEL (Taylor & Francis) и WVU WP (AWS WAF). Не получено для текущего batch.
- **Local file:** ❌ нет PDF

---

## 3. Use mapping (КРИТИЧНО для интеграции)

- **Stream:** Б+ (NEW — proposed addition from CSV analysis). **Прямо NBA + tax + individual salary — самый близкий direct precursor to our H9.**
- **Section in coursework:**
  - **Lit Review §2.4 (Market/team/tax context)** — главный empirical NBA+individual salary tax paper. Параллель с Alm 2012 для MLB.
  - **Discussion §5.x (H9 informative null)** — критичен для **direct comparison:** Johnson-Hall находят significant effect (+$60k per pp ATR), мы находим null. Что объясняет разницу? Период (2010-2014 vs 2015-2024), spec (FA-only vs all player-years), or sample composition (FA pool vs full panel)?
- **Supports hypothesis(es):**
  - **H9 (state tax effect on individual NBA salary):** Johnson-Hall = positive significant; наш = null. **Contradiction нужно отрабатывать.** Возможные explanations:
    1. **Sample selection:** их FA-only sample = subset наших player-years, где tax-mobility-on-margin максимум. Наш sample включает rookie scale + extension + supermax — где tax effect should be muted (или zero by construction).
    2. **Period 2010-2014 includes pre-2011 cap structure changes:** 2010 CBA вернутый (Phase 6 lockout 2011), 2011 CBA brand-new. Our period 2015-2024 = post-2017 CBA structure (designated extension, supermax). Possibly tax effect было stronger pre-2017.
    3. **ATR vs MTR specification:** Johnson-Hall использует Average Tax Rate (more realistic for high-income earners), мы — top marginal. Numerical effects могут differ.
- **Specifically supports argument:** "Существование tax effect на individual NBA FA salary documented в pre-2017 CBA period; в нашем post-2017 period — null. Это раскрывает интересный structural question о том, как modern CBA institutional features (supermax substitution, designated extension, max-contract calibration) могут muting tax channel relative to earlier cap regimes."

---

## 4. Core thesis (3-5 предложений, reconstructed from abstract + IDEAS)

Johnson и Hall тестируют, требуют ли NBA free agents higher pre-tax salary как compensation за higher state income tax (compensating differential). Использовав **576 FA signings за 2010-2014**, авторы находят statistically significant evidence того, что free agents signing в high-tax штатах получают higher salaries. **Один unit (1 pp) увеличения Average Tax Rate → free agent salary higher на over $60 000.** Результат consistent с teories tax incidence (Alm-Kaempfer-Sennoga 2012 MLB analog) и с Kleven framework: free agents — mobile factor, который shifts burden taxes на franchise через compensating differential. Implication: low-tax NBA franchises (TX, FL, TN, WA) платят меньше за same-quality FA.

---

## 5. Key claims for our text (нумерованный список)

> ⚠ **Все числа в этой секции — abstract reconstructed; верифицировать с PDF до финального citing**

1. **β_ATR на FA salary = +$60 000+ per pp ATR**, statistically significant (abstract, IDEAS). Это NBA-equivalent of Alm 2012 MLB result ($21-24k per pp).

2. **Sample = 576 FA signings 2010-2014** (abstract). Sample size suggests OK power for detecting medium effect.

3. **Mechanism = compensating differential** — players value after-tax income; high-tax franchises must offer higher pre-tax to match no-tax franchise offers (abstract). Same Kleven-style mechanism.

4. **NBA cap-constraint partial relaxation:** despite max-contract structure, FA market still has variation на margins — Bird rights renewal, mid-level exception, MLE, vet minimums — позволяет franchises flexibility on pre-tax salary вокруг cap rules. Tax compensation works within these margins. (Inferred — not directly in abstract.)

5. **Cross-validation with Hembre 2021:** Hembre находит team-level NBA tax-performance effect insignificant; Johnson-Hall находят individual-level salary effect significant. **Compatible** — at team level cap aggregates обоих effects; at individual level there's slack для FA market negotiation.

---

## 6. Direct quote candidates (с page numbers)

> ⚠ Не могу процитировать дословно без PDF.

> [Reconstructed from abstract:] "This paper investigates the impact of taxes on the salaries received by National Basketball Association free agents from 2010-2014. High state income tax rates affect the after-tax income received by players from their team as well as on any ancillary income. Using data on 576 free agents, we find statistically significant evidence that free agents signing in high tax states receive higher salaries, ceteris paribus." (Abstract, WVU WP 17-11)

> [Reconstructed from abstract:] "Our results suggest that a one-unit increase in the average tax rate experienced by a free agent in a state leads to free agent salaries being over $60,000 higher." (Abstract, WVU WP 17-11)

> ⚠ Перед финальным citing — get full PDF access for verbatim quotes.

---

## 7. Methodological notes

Не методологическая paper. Стандартный OLS / FE на FA-subset NBA panel. AEL — 3-page note format, методология условно minimal.

**Methodological параллель:** Alm-Kaempfer-Sennoga 2012 (MLB FA + MTR + FE) — same approach, different sport.

---

## 8. Limitations / caveats

> ⚠ Reconstructed from abstract + context

1. **FA-only sample, sample size 576** — limited statistical power для interaction effects. Cannot test heterogeneity по player quality (star vs journeyman tax sensitivity).
2. **Period 2010-2014** = transition period вокруг 2011 CBA. Включает 2011 lockout-shortened season + first 2 years of new cap structure. **Confounded** institutional changes vs tax effect. Это **directly weakens** generalizability to post-2017 era (наш sample).
3. **ATR variable** — авторы used average tax rate, что более realistic для NBA-stars salaries (above top brackets), но measurement могла включать (или не включать) jock tax на away games, что adds measurement error.
4. **No control for endorsement / off-court income** — same caveat как у Kleven, Hembre, Alm.
5. **AEL format (3 pages) limits robustness exposition** — wir не знаем results на alternative specs, sub-samples, или sensitivity tests.
6. **Bird rights не controlled** explicitly — incumbent team имеет structural advantage в FA market; if Bird-rights-restricted FA disproportionately в certain states, sample selection.

---

## 9. Connection to our findings

**DIRECTLY CONTRADICTS our H9 null** — это **the most important** paper для нашего Discussion §5 anatomy of H9 informative null.

**Why Johnson-Hall find effect и мы — не:**

1. **Sample selection:**
   - Johnson-Hall: FA signings only (n=576). Это conditional sample players who **actively chose** to test market — у них tax mobility max.
   - Наш sample: all player-seasons (n=3 660). Включает rookies (tied to draft city, нет mobility), extensions (incumbent team only), supermax (designated player — incumbent team only). 4 из 8 наших contract tiers — **mobility-restricted by design**.
   - **Implication:** наш null может reflect predominantly **non-FA-mobility-restricted observations** где tax cannot exert effect. Если ре-estimate только на FA subset (которые у нас можно tag через contract tier), могли бы replicate Johnson-Hall.

2. **Period:**
   - Johnson-Hall: 2010-2014 (transition era после 2011 CBA).
   - Наш: 2015-2024 (full post-2017 CBA, including supermax era).
   - **Possible structural break:** 2017 CBA introduced **designated extension** (Derrick Rose Rule, Player Option) которая ещё больше bounds incumbent teams to retain stars. Это **further constrains** FA mobility for top players — exactly the demographic где tax effect было strongest в Kleven/Kopkin.

3. **Spec details:**
   - Johnson-Hall: ATR (average tax rate), что more empirically motivated для high earners
   - Наш: state top marginal tax rate (per Karolina's plan)
   - Quantitatively, ATR ≤ MTR for given player (MTR is upper bound). Coefficient на MTR должен быть smaller in magnitude чем на ATR. Это может не объяснить null but reduces expected effect size.

4. **Pooling:** Johnson-Hall pool players по location decisions; мы pool all player-year observations. **Within-player FE** в нашей spec могла absorb игроки-постоянные tax exposures.

**Recommendation для Discussion:** "Johnson-Hall (2018) и Alm (2012) находят significant tax effects на FA salaries в NBA (2010-2014) и MLB (1995-2001) соответственно. Наш null в post-2017 CBA era может reflect (i) sample composition (full panel vs FA-only), (ii) tighter cap structure после 2017 designated extension reform, (iii) statistical power constraints. Это не contradicts existence of tax channel; это refines its scope of activation."

---

## 10. Reading notes / questions for follow-up

- **Recommended for inclusion: ВЫСШИЙ** в final ~25–30 references list. Reason:
  - **PRO:** наиболее прямой NBA + individual salary + tax paper в literature. Direct test of our H9. Essential for Discussion section anatomy.
  - **CON:** PDF inaccessible currently (Cloudflare/AWS WAF + paywall); все числа reconstructed from abstract.
  - **MITIGATING:** AEL via T&F — standardо available через HSE institutional access. Karolina может получить.
- **Action для финальной редакции курсовой:**
  1. **Получить full PDF** через HSE T&F access или Karolina
  2. **Cross-validate $60k число** — abstract говорит "over $60,000", may be specific point estimate (e.g., $63,512). Финал должен иметь точный round number.
  3. **Verify exact spec details** — нужна для Discussion section: ATR vs MTR? Player FE or pooled? Year FE? Other controls?
- **Сценарий "fast path" if PDF недоступен:** использовать abstract paraphrase в Discussion + cite as "Johnson and Hall (2018) document positive significant tax-salary relationship for NBA FAs". Не cite specific β без verification.
- **Бонус reference:** Hall (J.C.) и co-authors имеют другие NBA papers (e.g., Wage discrimination NBA FA, 2020 SEJ). Если решим расширить — параллельные refs от same authors могут быть useful.
- **Specific test для нашего курсача (if Karolina готова):** restrict our sample to **only** observations с `contract_tier == "free_agent"` (если такая tag есть в classify_tier output), run our M_full на subset, проверить, появляется ли significant tax coefficient. Это direct replication Johnson-Hall в нашем period. **Mandatory:** keep main result M_full unchanged (это headline), restricted-sample = robustness check в supplementary table.

---

**Заполнено:** 2026-05-22
**Заполнил:** Artem (collaborator)
