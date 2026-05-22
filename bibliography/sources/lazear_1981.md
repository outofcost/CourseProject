# Lazear & Rosen (1981) — Rank-Order Tournaments as Optimum Labor Contracts

---

## 1. Citation (APA)

Lazear, E. P., & Rosen, S. (1981). Rank-order tournaments as optimum labor contracts. *Journal of Political Economy, 89*(5), 841–864. https://doi.org/10.1086/261010

---

## 2. Source metadata

- **Type:** theoretical (game-theoretic + microeconomic mechanism design)
- **Sample:** не applicable (theory paper); illustrative examples: tennis, executive compensation, golf tournaments
- **Method:** optimization model — workers choose investment μ in skill, output q = μ + ε (random luck); analyze rank-order prize structure (W₁, W₂) vs piece rate r as compensation schemes; equilibrium prizes derive from worker utility maximization subject to firm zero-profit constraint
- **Pages used in this summary:** 1 (NBER cover), 2 (abstract), 3–4 (Sections I intro), 5–7 (Section II piece rates and tournaments under risk-neutrality, prop 1), 8–13 (Section III N-player + sequential tournaments + skewed prizes), 14–18 (Section IV risk-aversion case), 19–24 (Section V heterogeneity + adverse selection)
- **DOI / URL:** https://doi.org/10.1086/261010 (UC Press paywall); NBER WP 0401 (Nov 1979) freely available at nber.org/papers/w0401
- **Access status:** open access (NBER WP version)
- **Local file:** `bibliography/pdfs/lazear_1981.pdf` (NBER Working Paper 401, Nov 1979 version — 59 pages, includes all sections + appendices)

---

## 3. Use mapping (КРИТИЧНО для интеграции)

- **Stream:** В (классика labor economics) / также связь со Stream 3 (Awards / signaling) — Lazear-Rosen — теоретический микро-foundation для interpretation NBA awards как tournament prizes
- **Section in coursework:** Literature Review §2.3 (Awards stream); Discussion §5 (interpretation H5/H6 через tournament lens); Methods (theoretical motivation для inclusion awards features as separate channel)
- **Supports hypothesis(es):** H5 (All-NBA selection → future salary через signaling); H6 (awards effect lag 2-3 years через contract renewal cycle); косвенно — sub-finding aging-vet penalty (multi_all_nba ≥3 → β = −0.22, который можно интерпретировать как survival selection или tournament-attrition mechanism)
- **Specifically supports argument:** Lazear-Rosen формализует, почему compensation может strongly экспоненциально rise с rank (W₁ ≫ W₂), даже когда marginal product distance между winner and runner-up невелика. В NBA: разница в performance между All-NBA First Team (1st-prize) и All-NBA Third Team (3rd-prize) скромная (e.g., 26 PPG vs 22 PPG), но salary distance гигантская (max contract 35% cap vs 25% cap). Это классический Lazear-Rosen mechanism — prize structure designed для elicit max effort, not для отражать exact MRP. **Our H5 finding β_all_nba_lag1 = +0.185 (p = 0.008)** — direct empirical analogue: All-NBA selection — tournament-style discrete prize, дающее large lag-discontinuity в salary.

---

## 4. Core thesis (3-5 предложений)

Lazear-Rosen показывают, что compensation schemes based on **relative rank** (e.g., contest with fixed prizes W₁ for winner, W₂ for loser) могут implementовать тот же эффективный allocation эффорта, что и piece-rate compensation (basing pay on absolute output) — при условии risk-neutrality workers (Section II, Proposition 1). Это важно, поскольку measurement of rank часто cheaper, чем measurement of absolute output (e.g., easier to say "who won" than "by how much"). Под risk aversion, tournament structure может dominate piece rate для activities with high inherent variability (Section IV) — поскольку tournament risk-pools workers против correlated shocks. Section V показывает critical caveat: under worker heterogeneity, free entry в tournament может lead to adverse selection — low-quality workers "contaminate" high-quality firms — требует non-price screening mechanisms (например, draft, scout networks в NBA). Главный вывод: **observed exponential skewness compensation (W₁ ≫ W₂) consistent с optimal contract design**, не обязательно с MRP-based pay.

---

## 5. Key claims for our text (нумерованный список)

1. **Piece rate ≡ rank-order tournament под risk-neutrality** (Prop 1, Section II.B, p. 7): equilibrium prizes (W₁*, W₂*) выбираются так, чтобы expected utility worker = piece-rate utility. Это даёт первый формальный результат: rank-based pay efficient.

2. **Prize spread W₁ − W₂ determines effort incentive** (Section II.B, eq. 8): worker investments μ удовлетворяет первичной order condition g · (W₁ − W₂) = C'(μ), где g — density distribution noise. **Скorrелированный effort response с spread, не с absolute level prizes.** Implication: large salary gaps между tiers — efficient way to generate effort.

3. **Skewness в N-player tournaments** (Section III, p. 11): sequential elimination tournaments (как playoffs или All-NBA tier system: 15 players → 5 First Team → 1 MVP) produce highly skewed reward structure. **Direct analogy:** NBA First Team All-NBA (5 players) → подмножество All-NBA pool (15) → подмножество all-stars (~24). Каждый stage — prize structure с exponential skewness.

4. **Risk aversion preference для tournaments** (Section IV, p. 14): когда output highly variable (random shocks dominant), workers prefer tournament structure (risk-pooling) над piece rate. **Для NBA:** individual game performance highly volatile (PPG variance большая), но season-average smooths; All-NBA voting after full season — robust signal. Tournaments give workers insurance against bad-luck seasons.

5. **Adverse selection при heterogeneity** (Section V, pp. 19–22): if workers vary in quality, low-types try to enter high-type firms (because relative-ranking pay rewards being best in mediocre pool vs middle in elite pool). NBA solves через **draft mechanism** + **rookie scale contracts** — institutional screening, не market price. **Connection to H3 (tier structure):** salary tiers and CBA-mandated max contracts solve heterogeneity-induced adverse selection by capping prizes.

---

## 6. Direct quote candidates (с page numbers)

> "It is sometimes suggested that compensation varies across individuals much more dramatically than would be expected by looking at variations in their marginal products. This paper argues that a compensation scheme based on an individual's relative position within the firm rather than his absolute level of output will, under certain circumstances, be the preferred and natural outcome of a competitive economy." (Abstract, NBER WP p. 2)

> "Differences in the level of output between individuals may be quite small, yet optimal 'prizes' are selected in a way that induces workers to allocate their effort and investment activities efficiently." (Abstract, p. 2)

> "By compensating workers on the basis of their relative position in the firm, one can produce the same incentive structure for risk-neutral workers that the optimal and efficient piece rate produces. It might be less costly however, to observe relative position than to measure the level of each worker's output directly. This results in the payment of prizes, wages which for some workers greatly exceeds their presumed marginal products." (Abstract, p. 2)

> "When risk aversion is introduced, the prize salary structure no longer duplicates the allocation of resources induced by the optimal piece rate. For activities which have a high degree of inherent riskiness, payment based on relative position will dominate." (Abstract, p. 2)

> "Competitive contests which pay workers on the basis of their relative position will not, in general, sort workers in a way which yields an efficient allocation of resources. In particular, low quality workers will attempt to contaminate a firm comprised of high quality workers." (Abstract, p. 2)

---

## 7. Methodological notes

- **Method name:** rank-order tournament theory (game-theoretic optimal labor contract design)
- **Key formula / definition:**
  - Production: qⱼ = μⱼ + εⱼ (effort + noise)
  - Worker utility: P(W₁ − C(μ)) + (1 − P)(W₂ − C(μ)) (eq. 3)
  - First-order condition (eq. 8): g(0) · (W₁ − W₂) = C'(μ*) where g = density noise difference
  - Competitive equilibrium prizes solve: prize spread balances effort efficiency vs participation constraint
- **Key assumption(s):**
  - Identical workers (homogeneity), relaxed in Section V
  - Risk-neutrality (Section II–III) or specific CARA utility (Section IV)
  - Independent noise across workers
  - Common knowledge of contest rules and prizes (no asymmetric info on ε)
  - Zero-profit competitive firms
- **Where applicable in our work:** не direct method, а theoretical lens для interpretation H5/H6. Для Discussion: цитировать как theory underpinning «awards prize structure» argument. NBA's max contract tiers (super-max 35%, max 30%, max 25% cap) могут быть рассмотрены как rank-order tournament prize ladder.
- **Caveat / pitfall:**
  - Assumes single-period contest; NBA multi-year contracts complicate
  - Assumes prizes fixed ex-ante; NBA salary cap meanwhile fluctuates
  - Heterogeneity case (Section V) — assumes adverse selection through self-selection; NBA institutional layer (draft, scouting) reverses this
  - Not directly testable empirically — observable is salary level, not contest parameters

---

## 8. Limitations / caveats

1. **Theory only:** не дают empirical evidence; cannot directly support claim "NBA awards work as tournaments". Empirical evidence — Hausman-Leonard (1997), Stiroh (2007), Berri-Schmidt (2007).
2. **Risk-neutrality strong assumption** — для high-stakes contests (NBA max contracts) risk aversion likely material; Section IV partially addresses.
3. **Single-period model** — NBA contracts spread эффект prize over 3–5 years, что меняет dynamics (Stiroh 2007 contract-year effect — direct empirical correlate).
4. **No information asymmetry** — NBA awards involve voter committee (sports writers) with subjective bias; pure Lazear-Rosen assumes observable q (objective rank).
5. **Static heterogeneity** — assumes worker quality static; in NBA player skills change with age, injury, peer effects — dynamic version (Holmstrom 1979 career concerns) more applicable.

---

## 9. Connection to our findings

**SUPPORTS (theoretical foundation для awards channel H5/H6).** Lazear-Rosen — единственный теоретический framework, который объясняет, почему compensation в NBA так сильно skewed (top-1% получает > 30% wage bill) и почему All-NBA selection — discrete jump в lifetime earnings, а не smooth function of MRP.

Прямое отображение на наши findings:
- **H5 finding β_all_nba_lag1 = +0.185, p = 0.008** — All-NBA selection как tournament prize; lagged effect отражает contract renewal cycle (player должен exit current contract, чтобы capitalize prize → see H6)
- **H6 finding event study τ=+2: +21%, τ=+3: +22%** — exactly the time-window когда player negotiates new contract on All-NBA "prize"; tournament-induced salary jump
- **Sub-finding aging-vet penalty multi_all_nba ≥3: β = −0.22** — Lazear-Rosen Section V adverse selection: multi-time elite players in late career — high baseline expectation, но при declining performance team negotiating power increase (institutional discount)
- **Tier structure H3:** tier dummies дают R² = 0.85 — NBA salary structure is fundamentally rank-based (max/super-max/MLE/rookie scale = discrete prize tiers), exactly как Lazear-Rosen tournament prize ladder

Для Discussion:
- "Lazear & Rosen (1981) provide theoretical foundation for our finding, что **awards имеют discrete effect on salary беyond pure productivity** — это not anomaly, а efficient contract design"
- "Наш All-NBA premium consistent с tournament-prize interpretation, где W₁ − W₂ spread engineered для elicit max effort, не для reflect marginal product"

---

## 10. Reading notes / questions for follow-up

- **NBER WP 0401 = published JPE 1981** — content identical в основной theory; appendices в NBER version более extensive (всего 59 страниц vs ~24 в JPE).
- **Adjacent theoretical literature:**
  - Holmstrom (1979) "Moral Hazard and Observability" — career concerns dynamic version
  - Rosen (1986) "Prizes and Incentives in Elimination Tournaments" — multi-stage extension; directly applicable to NBA Conference Finals / Finals prize structure
  - Bognanno (2001) — empirical test in CEO compensation context; finds tournament theory supported
- **NBA-specific tests:**
  - Atkinson, Stanley & Tschirhart (1988) "Revenue sharing as an incentive in an agency problem: An example from NFL"
  - Becker & Huselid (1992) — racing context, tournament wages
- **Для нашей курсовой:** Lazear-Rosen цитируется один раз в Lit Review (Awards stream introduction) + один раз в Discussion (interpretation H5/H6). Не нужно повторять.
- В курсовой можно явно сказать: "Lazear & Rosen (1981) provide the theoretical microfoundation: rank-based compensation can be efficient incentive design even when prize spread W₁ − W₂ greatly exceeds marginal product difference between rank positions."

---

**Заполнено:** 2026-05-22
**Заполнил:** Artem (collaborator)
