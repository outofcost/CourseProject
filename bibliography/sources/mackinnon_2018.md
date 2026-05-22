# MacKinnon & Webb (2018) — The Wild Bootstrap for Few (Treated) Clusters

---

## 1. Citation (APA)

MacKinnon, J. G., & Webb, M. D. (2018). The wild bootstrap for few (treated) clusters. *The Econometrics Journal, 21*(2), 114–135. https://doi.org/10.1111/ectj.12107

---

## 2. Source metadata

- **Type:** methodological (econometric theory + extensive Monte Carlo + empirical example)
- **Sample (Monte Carlo):** широкий набор designs варьируя G (5–50) и G₁ (1–25); сравнение пяти методов: CV1 t-test, restricted/unrestricted wild cluster bootstrap (WCB), ordinary wild bootstrap, randomization inference
- **Sample (empirical):** replication с G = 8 clusters
- **Method:** extension wild cluster bootstrap (Cameron, Gelbach & Miller 2008) и его failure mode для few-treated-clusters; introduces **subcluster wild bootstrap** family (включая ordinary wild bootstrap как limiting case); ключевая идея — bootstrap DGP clusters at FINER level чем CRVE
- **Pages used in this summary:** 1 (title), 2 (abstract), 3–4 (intro), 4–7 (Section 2: pure treatment model + why CRVE fails when G₁ small), 7–9 (wild cluster bootstrap failure mode), 9–13 (Section 3: subcluster wild bootstrap theory), 14–25 (simulation results), 26–28 (empirical example), 29 (conclusions and recommendations)
- **DOI / URL:** https://doi.org/10.1111/ectj.12107 (Wiley paywall); QED working paper 1364 freely available at queensu.ca
- **Access status:** open access (QED working paper, Nov 2017 version)
- **Local file:** `bibliography/pdfs/mackinnon_2018.pdf`

---

## 3. Use mapping (КРИТИЧНО для интеграции)

- **Stream:** А (методы)
- **Section in coursework:** Methods §3.x (inference — wild cluster bootstrap for H7 interaction tests); Robustness section
- **Supports hypothesis(es):** не support конкретную гипотезу — это методологическая основа для inference в H7 (top5_market × allstar interaction) и любых spec, где есть **few treated clusters** (e.g., только 6 top-5 markets в нашей выборке: LAL, LAC, NYK, BRK, CHI, GSW)
- **Specifically supports argument:** В наших H7-spec'ах (`analysis_v2/h8_market.py`) interaction-coefficient top5_market × allstar testируется на выборке, где treated cluster count G₁ = 6 (число команд в top-5 market) — это classic few-treated-clusters problem. Standard cluster-robust SE на team_id overreject severely при G₁ = 6 (см. MacKinnon-Webb Section 2.1). Wild cluster bootstrap (CGM 2008) тоже может fail в этой ситуации. MacKinnon-Webb 2018 рекомендуют ordinary wild bootstrap или subcluster wild bootstrap — мы используем wild-cluster bootstrap по SHIPPING_SUMMARY ("Phase 3 day 4 → H8 market → M8a-d, wild-cluster bootstrap, anti-marketability finding"). Цитата нужна в Methods для обоснования procedure inference на small G₁ + в Limitations для caveat про potential overrejection.

---

## 4. Core thesis (3-5 предложений)

Авторы показывают, что cluster-robust variance estimator (CRVE) и wild cluster bootstrap (CGM 2008) **fail dramatically** когда число treated clusters G₁ или untreated clusters G₀ очень мало (e.g., 1–3) — t-statistic либо overreject (CV1) либо underreject/overreject (WCB depending on restricted/unrestricted). Формальное объяснение: при G₁ = 1, denominator t-statistic становится почти полностью функцией untreated residuals, а variance treated-cluster term incorrectly estimated as zero (eq. 7). Авторы предлагают **subcluster wild bootstrap** — bootstrap DGP кластеризуется at finer level чем CRVE (e.g., bootstrap by state-year pair when CRVE clusters by state); крайний случай — **ordinary wild bootstrap** (no clustering в DGP). Симуляции показывают, что ordinary wild bootstrap + CRVE SE часто работает хорошо даже при 1–2 treated clusters, при условии что все clusters approximately равного размера. **CRITICAL caveat** — для difference-in-differences regressions (где cluster sizes по treatment unevenly distributed по времени) условие equal cluster sizes обычно не выполняется, и subcluster bootstrap может всё ещё fail.

---

## 5. Key claims for our text (нумерованный список)

1. **CRVE failure при G₁ = 1 или G₀ = 1:** "tests based on the cluster-robust t statistic using conventional critical values almost always overreject very severely when G₁ = 1 or G₀ = 1" (p. 6). Формальная причина (eq. 7): denominator t-stat estimates variance of treated-cluster contribution as zero. **Для нас:** в H7 spec'ах top5_market = 6 команд, untreated = 24; G₁ = 6 не «extreme few», но всё ещё на границе, где asymptotic theory тревожит.

2. **Wild cluster bootstrap (CGM 2008) тоже может fail:** "tests based on the restricted WCB can underreject severely, and tests based on the unrestricted WCB can overreject severely" (p. 2). Restricted vs unrestricted — выбор имеет significant inferential consequences.

3. **Ordinary wild bootstrap + CRVE = surprisingly reliable при few treated clusters:** "ordinary wild bootstrap often yield surprisingly reliable inferences even when there are just two treated clusters, and sometimes when there is just one" (Section 4, p. 17 ff.). **Key condition: equal cluster sizes**.

4. **DiD regressions нарушают условие equal cluster sizes:** "the analogue of this requirement is not likely to hold for difference-in-differences regressions" (Abstract, p. 2). Так как наш H7 не строго DiD (просто categorical market dummy), эта caveat для нас менее острая, но всё ещё стоит упомянуть в Limitations.

5. **Recommendation:** для cluster-robust inference с few treated, использовать ordinary wild bootstrap с проверкой условия equal cluster sizes; докладывать robustness под несколько bootstrap procedures (restricted/unrestricted/subcluster).

---

## 6. Direct quote candidates (с page numbers)

> "Inference based on cluster-robust standard errors in linear regression models, using either the Student's t distribution or the wild cluster bootstrap, is known to fail when the number of treated clusters is very small." (Abstract, p. 2)

> "We propose a family of new procedures called the subcluster wild bootstrap, which includes the ordinary wild bootstrap as a limiting case. In the case of pure treatment models, where all observations within clusters are either treated or not, the latter procedure can work remarkably well. The key requirement is that all cluster sizes, regardless of treatment, should be similar." (Abstract, p. 2)

> "t tests based on cluster-robust standard errors tend to overreject severely when the number of clusters is small. How many clusters are required to avoid serious overrejection depends on several things, including how the observations are distributed among clusters and, for the important special case of binary regressors that do not vary within clusters, how many clusters are 'treated'." (Introduction, p. 3)

> "The wild cluster bootstrap (WCB) of Cameron, Gelbach and Miller (2008) often leads to much more reliable inferences, but… this procedure can also fail dramatically. When the regressor of interest is a dummy variable that is nonzero for only a few clusters, tests based on the restricted WCB can underreject severely, and tests based on the unrestricted WCB can overreject severely." (Section 1, pp. 3–4)

> "Bootstrap tests based on the ordinary wild bootstrap often yield surprisingly reliable inferences even when there are just two treated clusters, and sometimes when there is just one." (Section 4, p. 17)

---

## 7. Methodological notes

- **Method name:** subcluster wild bootstrap (family); ordinary wild bootstrap as limiting case
- **Key formula / definition:**
  - Restricted WCB DGP (eq. 9, p. 7): y*ᵢg = β̃₁ + ε̃ᵢg · v*g, where v*g is Rademacher (±1) at cluster level
  - Subcluster DGP: replace v*g with v*ₛ at subcluster s (s ⊂ g)
  - Ordinary wild bootstrap = subcluster при s = single observation (no clustering in DGP, only in CRVE)
  - For G ≤ 11, use Webb (2014) 6-point distribution rather than Rademacher
- **Key assumption(s):**
  - Cluster sizes approximately equal (otherwise variance asymmetry breaks bootstrap calibration)
  - Errors uncorrelated across (top-level) clusters; within-cluster correlation arbitrary
  - For DiD, treatment timing varies → cluster sizes по treatment status unequal → procedure may fail
- **Where applicable in our work:** `analysis_v2/h8_market.py` — H7 (top5_market) tests with G₁ = 6 treated team-clusters. Currently uses wild-cluster bootstrap; might consider robustness with ordinary wild bootstrap per MacKinnon-Webb recommendation.
- **Caveat / pitfall:**
  - При G₁ = 1: даже ordinary wild bootstrap может dramatically fail если cluster sizes сильно различаются
  - Для G ≤ 11, обязательно использовать 6-point Webb distribution вместо Rademacher (иначе только 2^G ≤ 2048 unique bootstrap samples)
  - Tests should report symmetric AND equal-tail P-values если distribution skewed
  - При наличии continuous covariates (как у нас в H7: market dummy × continuous PPG interaction) — wild bootstrap асимптотически валиден, но проверка симуляцией крайне рекомендована

---

## 8. Limitations / caveats

1. **No universal solution:** authors прямо говорят, что для DiD с very uneven cluster sizes ни один из методов wild bootstrap не работает reliably; в этих случаях рекомендуют randomization inference (MacKinnon-Webb 2018a) или вообще другие data designs
2. **G_1 = 1 cases:** even ordinary wild bootstrap can fail; sometimes need 2+ treated clusters minimum
3. **No formal coverage guarantee** для finite-sample; все результаты — simulation-based + asymptotic theory
4. **Computational cost:** для B = 999 bootstrap reps в spec'е с 3 660 наблюдений и cluster-bootstrap-aware Stata — несколько minutes per regression; для full Shapley + bootstrap CI на 9 блоках уже становится материально
5. **Не учитывает treatment heterogeneity** within cluster — assumes pure treatment model (everyone in cluster either treated or not)

---

## 9. Connection to our findings

**SUPPORTS (methodological foundation for H7 inference).** Наш H7 finding β_top5 = −0.098, p = 0.022 опирается на cluster-robust SE на player_id (с G ≈ 953) и wild-cluster bootstrap на team_id (с G = 30, G₁ = 6 top-5 markets). С G₁ = 6, мы находимся в "few treated clusters" regime, где MacKinnon-Webb предостерегают про potential overrejection как через standard CRVE, так и через restricted WCB.

В нашем контексте wild-cluster bootstrap критически важен для credibility H7 finding — без него p = 0.022 могла бы быть artifact CRVE under-estimation вариансы. MacKinnon-Webb даёт solid theoretical и empirical foundation для нашего выбора этой procedure.

Для Discussion / Limitations можно написать:
- "Following MacKinnon & Webb (2018), мы используем wild cluster bootstrap для H7 inference, признавая, что с G₁ = 6 treated clusters стандартный CRVE может overreject."
- "В качестве robustness, рекомендуется (future work) повторить H7 с ordinary wild bootstrap (MacKinnon-Webb p. 17), при условии approximately equal cluster sizes."

---

## 10. Reading notes / questions for follow-up

- **Open question:** какой именно variant wild bootstrap используется в `h8_market.py`? Restricted? Unrestricted? Subcluster? Это важно для precise citation MacKinnon-Webb. Если restricted WCB — может underreject; если unrestricted — overreject. Recommended check.
- **Alternative procedures** в paper (Section 5 + appendix):
  - Hansen (2007) cluster-bootstrap-t
  - Bell-McCaffrey (2002) bias-reduced CRVE (CV2)
  - Imbens-Kolesar (2016) с alternative degrees-of-freedom calc
- **Software:** authors recommend Stata `boottest` package (Roodman et al. 2019) — implements all WCB variants efficiently. В Python — `wildboottest` package (Alessandro Faure / Alex Fischer fork).
- **MacKinnon-Webb 2018 vs Cameron-Gelbach-Miller 2011:** complementary, не competing — CGM 2011 = general multiway clustering theory; MW 2018 = specific failure modes + remedies для **few treated clusters** within one-way cluster framework. Цитировать обоих в Methods.
- В нашей курсовой top-5 market — это 6 команд (фикс). Если бы мы делали top-3 (3 команды) или top-10 (10 команд) sensitivity — bootstrap procedure choice была бы ещё более critical.

---

**Заполнено:** 2026-05-22
**Заполнил:** Artem (collaborator)
