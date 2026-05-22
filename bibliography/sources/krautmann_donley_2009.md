# Krautmann & Donley (2009) — Shirking in Major League Baseball: Revisited

> ⚠ **Skeleton based on secondary sources:** оригинал статьи (Sage Journal of Sports Economics 2009) за paywall. PDF на DePaul institutional repository (via.library.depaul.edu) ссылается на EBSCOhost (paywalled). Шаблон заполнен на основе детальной реферации в Jean-Neal (Duke DJE 2016 thesis), Fumarco et al. (2024, IZA DP 16836), Krautmann CV 2021 (DePaul). **Перед финальным цитированием Кириллу — добыть оригинал через HSE proxy / Sage Journals / email Krautmann (akrautma@depaul.edu).**

> **НЕ** в `bibliography_proposal.md`; рекомендуется к добавлению как СРЕДНИЙ приоритет (новый источник из CSV-анализа). MLB shirking analog, важный для cross-sport perspective.

---

## 1. Citation (APA)

Krautmann, A. C., & Donley, T. D. (2009). Shirking in Major League Baseball: Revisited. *Journal of Sports Economics, 10*(3), 292–304. https://doi.org/10.1177/1527002508326744

---

## 2. Source metadata

- **Type:** empirical (panel econometrics, MLB player-season)
- **Sample:** MLB players с multi-year contracts (точный период требует проверки в оригинале; CV Krautmann 2021 не даёт детали; по контексту — конец 1990s — начало 2000s)
- **Method:** Two parallel tests of shirking:
  - (i) **Performance-based test** — comparison expected (model-predicted) vs realized player performance после signing
  - (ii) **MRP-based test** — comparison expected (model-predicted) vs realized Marginal Revenue Product (proxy через payroll-weighted dollar value of contribution)
- **Pages used in this summary:** N/A (через secondary sources)
- **DOI / URL:** https://doi.org/10.1177/1527002508326744 ; DePaul repository: https://via.library.depaul.edu/econ_pubs/2/
- **Access status:** paywall (Sage); EBSCOhost link через DePaul library — institutional access required
- **Local file:** — (не скачано)

---

## 3. Use mapping (КРИТИЧНО для интеграции)

- **Stream:** В+ (NEW — proposed addition from CSV analysis). MLB-specific (cross-sport reference); methodological framework
- **Section in coursework:** **Lit Review §2.3 (Awards / signaling / shirking)** — cross-sport extension Berri-Krautmann (2006); **Methods §3** — обоснование почему наш choice MPR-proxy (lagged performance metrics) — это второй-лучший reduced-form measure без direct expected-vs-realized testing; **Limitations §6** — caveat что MPR-based shirking может присутствовать в нашем sample, и наш design не identifies его
- **Supports hypothesis(es):**
  - **H1** — косвенно: K-D показывают, что performance-based vs MRP-based tests дают opposite results, что rules out single-metric interpretation any salary/talent relation
  - **Limitations** — обязательно: для shirking endogeneity caveat
- **Specifically supports argument:** Cross-sport replication / contrast Berri-Krautmann (2006). В NBA shirking finding — metric-sensitive (B-K 2006); в MLB — отдельно methodology-sensitive (K-D 2009: performance test → null; MRP test → significant shirking). Это даёт сильный common message: shirking literature не делает clean identification, и любые "no shirking" заявления должны сопровождаться caveats о выборе measure.

---

## 4. Core thesis (3-5 предложений)

Authors revisit shirking debate в MLB через dual approach: traditional **performance-based test** (Lehn 1984; Sommers 1993) сравнивает expected vs realized player performance после signing multi-year contracts, и novel **MRP-based test** сравнивает expected vs realized marginal revenue product. Theoretical rationale — performance metrics в спорте noisy, но dollar value contribution игрока (MRP) — более прямой measure of "value to firm", что closer matches economists' definition shirking как "agent reduces effort → reduced value to principal". Главное эмпирическое finding — **dichotomy**: performance-based test даёт **no evidence** of shirking; MRP-based test даёт **significant evidence** что players на multi-year deals create less value than expected. Authors интерпретируют это как rehabilitation shirking hypothesis: previous null findings (e.g., Maxcy-Fort-Krautmann 2002 для MLB; Berri-Krautmann 2006 для NBA с wins-based metric) — артефакт incorrect measurement; shirking реальна, но проявляется в dollar terms, не в box-score stats.

---

## 5. Key claims for our text (нумерованный список)

1. **Dichotomy между performance- и MRP-based tests** — "we find no evidence of shirking" with performance tests, but "tests suggest that players signing multi-year contracts create less value than they were expected to generate" with MRP tests (per Abstract / RePEc summary). Это означает, что **shirking может существовать но не detected** через стандартные performance metrics — relevant для нашего Mincer-spec'а.

2. **Methodological framework для shirking tests** — К-D outline standard approach: (a) modelpredicted expected MPR/performance pre-signing; (b) сompare с realized post-signing; (c) negative residual = shirking. Применимо к нашему data, но мы не используем (post-shipping extension).

3. **MLB-NBA contrast** — В NBA contracts полностью guaranteed (Berri & Krautmann 2006); в MLB — partially guaranteed (incentive clauses, performance bonuses common). Despite less guarantee → MRP-based shirking всё равно detected, что shows shirking ≠ pure guarantee-driven phenomenon. Для НБА (где guarantee total), expected shirking strength должна быть minimum equally large.

4. **"Players on multi-year deals create less value":** quantitative magnitude в paper'е (через secondary description) — unspecified в reference sources, требует проверки оригинала. Но direction unambiguous — negative.

5. **Cited 49+ times** по Google Scholar; foundational secondary reference для MLB shirking literature после Maxcy-Fort-Krautmann (2002).

---

## 6. Direct quote candidates (с references)

> ⚠ Full text за paywall — direct verbatim цитаты с page numbers недоступны. Reference-based phrases:

> (per RePEc abstract / Krautmann CV) "The authors outline a novel approach for testing opportunistic behavior, beginning with a standard test of shirking based on comparing a player's expected to realized performance, and then introducing a new approach based on a comparison of a player's expected to realized Marginal Revenue Product."

> (per RePEc abstract) "When testing for opportunistic behavior using performance, [the authors] found no evidence of shirking. However, when conducting the test based on MRP, their tests suggest that players signing multi-year contracts create less value than they were expected to generate."

> (per Jean-Neal 2016 description, p. 5) "Ex post opportunistic behavior, or shirking, is defined as a decrease in effort expended by the agent once the contract is signed. Since compensation is then guaranteed, regardless of effort level, the agent has no incentive to continue performing with maximal effort."

**Альтернатива** — если оригинал недоступен, в курсовой использовать paraphrase с reference, не verbatim citation.

---

## 7. Methodological notes

Не сугубо methodological paper, но **methodologically instructive** через introduction MRP-based test framework:

- **Two-stage testing approach:**
  - Stage 1: estimate expected performance / expected MRP through pre-signing model (typically reduced-form Mincer-like spec на pre-signing data)
  - Stage 2: regress observed post-signing residuals on contract characteristics (length, salary, guarantee level)
  - Negative residual = shirking

- **MRP-proxy construction в MLB** обычно: contribution to wins × team revenue per win. В NBA-application было бы analogous (Berri's wins per 48 × revenue per win) — это direction, к которому Berri и Krautmann sustainably двигались.

- **Replication template** для нашей курсовой: если post-shipping extension — мы могли бы construct expected ln_salary через v2 spec, посмотреть residuals для players в post-contract years, и протестировать systematic negative. Но это **уже extra-effort work**, не в scope текущего coursework.

---

## 8. Limitations / caveats

1. **Paywall — все claims через secondary.** Кириллу необходимо добыть оригинал перед использованием specific numbers / methodology details.

2. **MRP construction sensitive** — построение dollar-value MRP требует assumptions о team revenue function, что неустойчиво в эмпирике. Critics могут утверждать что K-D finding артефакт revenue-function specification, не реальный shirking.

3. **Selection в "multi-year contract" group** — players signing multi-year deals systematically отличаются (higher reputation, higher prior performance), что вводит endogeneity. K-D presumably control for это, но без оригинала нельзя verify.

4. **Period limit** — paper 2009 → данные ~ 1990s — 2000s. Pre-modern free agency era; не reflects 2010s+ data dynamics в MLB.

5. **Cross-sport extrapolation** к NBA — limited. MLB shirking via reduced effort plausibly differs от NBA (NBA — more skill-displayed-per-touch sport; MLB — more random-noise sport). Direct transplant findings не валиден.

6. **No causal identification** — K-D как и B-K (2006) — observational; нет experimental или quasi-experimental variation для clean causal claim.

---

## 9. Connection to our findings

**PARALLELS** — Krautmann-Donley (2009) даёт **cross-sport reference point** для нашего NBA empirical exercise.

(1) **Methodological framing для our Limitations:** "Cross-sport shirking literature (Berri & Krautmann, 2006 for NBA; Krautmann & Donley, 2009 for MLB; Stiroh, 2007 for NBA) consistently documents that opportunistic behavior post-signing is detectable in some specifications and absent in others, depending on choice of productivity measure (NBA EFFICIENCY vs wins-based ADJP48 vs MRP-proxy)."

(2) **Why we don't directly test shirking:** Наш sample dimension — player-season с lagged performance → contemporaneous salary. Мы НЕ дисagregate post-signing year-1 vs steady-state. Это conscious scope decision: shirking — отдельный sub-literature, который требует contract-data linkage (что у нас нет). К-D даёт permission говорить, что even при ideal data testing shirking finds **mixed** evidence — не critically affecting нашу main Mincer narrative.

(3) **MRP-bias в нашем β_ppg:** K-D suggests, что post-signing players underperform в dollar-value terms (MRP) даже когда box-score стабилен. Это означает, что наш β_ppg (estimated through cross-section + lag) **overstates true talent → MPR → salary causal chain** by absorbing some post-signing inflation of performance metrics. Limitations caveat: "Reduced-form coefficients should be interpreted as upper bounds on structural talent-salary elasticity."

(4) **Cross-sport context для Discussion:** Мы можем написать "NBA-specific evidence (B-K 2006) and MLB-comparison (K-D 2009) suggest that contract dynamics introduce non-trivial residual variation in performance-salary linkage. Our Shapley decomposition attributes 65.5% of variance to performance + age, but absent direct contract-year identification, some of this attribution conflates pure-talent and signaling-dynamics channels."

---

## 10. Reading notes / questions for follow-up

- **Predicted impact:** **Рекомендуется к добавлению в финальную bibliography СРЕДНИЙ приоритет.** K-D (2009) — cross-sport benchmark для shirking literature; цитата нужна для context Berri-Krautmann (2006). Если объём ограничивает — можно сократить до 1-line ссылки в Limitations.

- **PRIORITY ACTION:** добыть оригинал PDF через:
  - HSE library proxy → Sage Journals
  - DePaul EBSCOhost (via.library.depaul.edu/econ_pubs/2/)
  - Email Krautmann: akrautma@depaul.edu
  - Альтернативный similar paper: Solow & Krautmann (2020) "Do You Get What You Pay For? Salary and Ex Ante Player Value in MLB" JSE — более recent, может содержать updated MRP-test

- **Цитата pair:** в курсовой K-D (2009) и B-K (2006) должны цитироваться **вместе** как methodological cluster. Если K-D недоступен — можно опустить с reference только на B-K, потеря не критичная.

- **Hölmström-связь:** K-D подтверждают theoretical prediction Hölmström (1979) — observable signals (performance metrics) **insufficient** для detecting underlying effort changes; дополнительные informative signals (MRP/dollar-value, peer comparison) — улучшают detection. Это естественный мост в Lit Review framework.

- **Если нашёл новые сведения по B-K 2006 — они автоматически relevant для K-D 2009 тоже** (same Krautmann coauthor); cross-reference.

---

**Заполнено:** 2026-05-22 (skeleton, paywall — based on secondary sources)
**Заполнил:** Artem (collaborator)
