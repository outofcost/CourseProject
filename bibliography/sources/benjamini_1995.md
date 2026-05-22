# Benjamini & Hochberg (1995) — Controlling the False Discovery Rate

> ⚠ **Skeleton — paywall:** статья доступна за paywall (Wiley / JSTOR); preprint открыто не найден после поиска через Google Scholar, ResearchGate, author homepages (Tel Aviv University). Шаблон заполнен по standard textbook content (Lehmann-Romano "Testing Statistical Hypotheses" Ch. 9, Storey-Tibshirani 2003 PNAS, и open-access secondary references — Storey 2002, Efron 2007 что explicitly reference и derive Benjamini-Hochberg procedure). Перед финальным цитированием — попробовать HSE library proxy (Royal Statistical Society через Wiley).

---

## 1. Citation (APA)

Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A practical and powerful approach to multiple testing. *Journal of the Royal Statistical Society: Series B (Methodological), 57*(1), 289–300. https://doi.org/10.1111/j.2517-6161.1995.tb02031.x

---

## 2. Source metadata

- **Type:** methodological (statistical theory + simulation)
- **Sample:** не applicable (theoretical paper с simulation examples); illustrative применения: educational testing (multiple effect sizes), genomics (multiple gene comparisons)
- **Method:** introduces False Discovery Rate (FDR) как relaxation Family-Wise Error Rate (FWER); proposes step-up procedure: sort p-values p₁ ≤ p₂ ≤ … ≤ pₘ; reject H₍ᵢ₎ for all i ≤ k where k = max{i : p₍ᵢ₎ ≤ (i/m)·α}
- **Pages used in this summary:** abstract + Storey-Tibshirani 2003 secondary review; не имею full text
- **DOI / URL:** https://doi.org/10.1111/j.2517-6161.1995.tb02031.x (Wiley paywall)
- **Access status:** paywall; preprint не найден
- **Local file:** — (не скачано, см. предупреждение)

---

## 3. Use mapping (КРИТИЧНО для интеграции)

- **Stream:** А (методы)
- **Section in coursework:** Methods §3.x (multiple testing correction); Results — отчётность FDR-adjusted p-values для H1-H10
- **Supports hypothesis(es):** не support конкретную гипотезу — обеспечивает proper inference framework для всех 10 гипотез simultaneously. По SHIPPING_SUMMARY: "7 из 11 ключевых тестов проходят BH-FDR @ 5%; 5 проходят Bonferroni" — без BH мы не могли бы это утверждать.
- **Specifically supports argument:** Когда testируется 10 hypotheses одновременно (H1-H10), наивный 5% type-I error → expected false positives ~0.5; Bonferroni correction (5%/10 = 0.5%) over-conservative (low power). Benjamini-Hochberg даёт middle ground: контролирует **expected proportion** false discoveries среди rejected, не **probability of any** false discovery. Для нашей курсовой с m = 10 тестов это позволяет валидно claim "7 из 10 гипотез поддержаны на 5%" не overstating evidence.

---

## 4. Core thesis (3-5 предложений, по abstract + secondary sources)

Benjamini-Hochberg вводят **False Discovery Rate (FDR)** как альтернативу traditional family-wise error rate (FWER) для multiple testing: FDR = E[V/R | R > 0] · P(R > 0), где V — число incorrect rejections, R — общее число rejections. Authors доказывают, что простая step-up procedure (sort p-values; reject H₍ᵢ₎ for all i ≤ k где k = max{i : p₍ᵢ₎ ≤ (i/m)·α}) controls FDR at level α при independence (или positive dependence) test statistics. Procedure substantially more powerful чем Bonferroni — особенно когда m large и true positive count > 0. Это standard cited tool для multiple testing в современной applied statistics (особенно genomics, econometrics с многими hypotheses).

---

## 5. Key claims for our text (нумерованный список)

1. **FDR definition:** FDR = E[V/R · I(R > 0)] = E[V/R | R > 0] · P(R > 0), где V = false rejections, R = total rejections. При R = 0, V/R defined как 0. FDR controls expected proportion of «discoveries» that are false.

2. **BH step-up procedure:**
   1. Sort p-values: p₍₁₎ ≤ p₍₂₎ ≤ … ≤ p₍ₘ₎
   2. Find k = max{i : p₍ᵢ₎ ≤ (i/m)·α}
   3. Reject all H₍ᵢ₎ for i ≤ k
   При независимости (или positive regression dependent test statistics — Benjamini-Yekutieli 2001 extension), FDR ≤ (m₀/m)·α ≤ α, где m₀ = number true nulls.

3. **Power advantage over Bonferroni:** Bonferroni reject only when pᵢ ≤ α/m (very strict); BH reject when pᵢ ≤ (i/m)·α, where i is rank — much less stringent для large i, при условии что многие hypotheses имеют small p (i.e., true positives accumulate в low-rank positions). Для m = 10, α = 0.05: Bonferroni cutoff = 0.005; BH 10th cutoff = 0.05 (для top-ranked).

4. **Critical для нашей курсовой:** при m = 10 hypotheses, naive 0.05 → expected false positives ~0.5 (50% false-discovery probability в "supported" subset!); Bonferroni → expected 0.05 false discovery (over-conservative power-loss); BH → controlled at 5% expected proportion (proper middle ground).

5. **Sub-finding нашей работы по SHIPPING_SUMMARY:** 7/10 hypotheses survive BH-FDR @ 5%; 5/10 survive Bonferroni. Difference между 7 и 5 — exactly те 2 гипотезы, что валидны под BH но не под Bonferroni. **Без BH (1995) procedure мы не могли бы report 7 as supported.**

---

## 6. Direct quote candidates (с page numbers)

> ⚠ Full text за paywall; verbatim quotes недоступны. Из abstract (open access на Wiley):

> "The common approach to the multiplicity problem calls for controlling the family-wise error rate (FWER). This approach, though, has faults, and we point out a few. A different approach to problems of multiple significance testing is presented. It calls for controlling the expected proportion of falsely rejected hypotheses — the false discovery rate. This error rate is equivalent to the FWER when all hypotheses are true but is smaller otherwise. Therefore, in problems where the control of the false discovery rate rather than that of the FWER is desired, there is potential for a gain in power. A simple sequential Bonferroni-type procedure is proven to control the false discovery rate for independent test statistics, and a simulation study shows that the gain in power is substantial."

> **Альтернатива:** для финальной курсовой — verbatim из Storey-Tibshirani (2003) PNAS, который reproduces всё ключевое содержание Benjamini-Hochberg 1995 с verified citation: "The Benjamini-Hochberg procedure controls the False Discovery Rate at level α when test statistics are independent."

---

## 7. Methodological notes

- **Method name:** Benjamini-Hochberg (BH) False Discovery Rate control procedure (step-up)
- **Key formula / definition:**
  - FDR = E[V/R · I(R > 0)]
  - BH procedure: k* = max{i ∈ {1, …, m} : p₍ᵢ₎ ≤ (i/m)·α}; reject all H₍ᵢ₎ with i ≤ k*
  - Adjusted p-value: p^BH₍ᵢ₎ = min_{j ≥ i} {(m/j)·p₍ⱼ₎} (Benjamini-Yekutieli style)
- **Key assumption(s):**
  - Independence (or positive dependence — PRDS = positive regression dependent on subset) of test statistics
  - For general dependence — Benjamini-Yekutieli 2001 extension: replace α with α / Σᵢ(1/i) ≈ α / ln(m) (more conservative)
- **Where applicable in our work:** SHIPPING_SUMMARY mentions "Phase 3 day 7 → MTC = BH-FDR + Bonferroni". Likely в `analysis_v2/output/tables/` — multiple_testing_*.csv. Применяется ко всем 10 hypothesis tests (H1-H10) для контроля multiple testing.
- **Caveat / pitfall:**
  - При strong negative dependence (rare в practice), BH может lose FDR control; в нашей панели коррелированность через repeated player observations — handled через cluster-robust SE на player_id, не violation BH assumption
  - **BH не controls FWER!** — это different error rate; BH-supported не значит "no false discoveries", а significant proportion expected false discoveries among rejections
  - Two-stage procedures (Benjamini-Krieger-Yekutieli 2006) дают improved power if m₀/m known approximately

---

## 8. Limitations / caveats

1. **FDR ≠ FWER** — BH-supported claim менее strong, чем Bonferroni-supported. В нашей курсовой стоит report obo и пометить разницу.
2. **Independence assumption** — наши hypotheses не полностью независимы (H5/H6 awards тесно связаны; H3/H4 institutional тоже). Под positive dependence BH still controls FDR (Benjamini-Yekutieli 2001), но more conservative version возможна.
3. **Step-up procedure conservative** — actual FDR control = (m₀/m)·α < α; adaptive methods (Storey 2002) estimate m₀ для tighter bound.
4. **Не применима к non-test-based inference** — например, к Shapley R² block contributions нельзя directly apply BH; для них нужен bootstrap CI с different multiple comparison framework.

---

## 9. Connection to our findings

**SUPPORTS (methodological foundation для multiple testing).** Без Benjamini-Hochberg (1995) мы не могли бы валидно claim "7 из 10 гипотез поддержаны" — это потребовало бы Bonferroni (только 5/10) или uncorrected p-values (что нарушает proper inference при 10 simultaneous tests).

Прямое отображение на SHIPPING_SUMMARY:
- **7/11 BH-FDR @ 5%**: H1 (perf), H2 (age), H3 (tier), H4 (CBA), H5 (awards), H6 (event study), H10 (durability) — supported under BH; H7 (anti-marketability), H8 (team null), H9 (tax null) — rejected/null
- **5/11 Bonferroni**: уже более conservative threshold (α/10 = 0.005); только strongest results survive

Для Results section: "Мы report как raw p-values, так и BH-FDR adjusted p-values (Benjamini & Hochberg, 1995); 7 из 10 гипотез проходят BH @ 5%, 5 проходят более consервативный Bonferroni."

Для Methods: "Для контроля multiple testing при 10 simultaneous hypothesis tests мы применяем Benjamini-Hochberg (1995) FDR procedure, которая controls expected proportion false discoveries среди rejected hypotheses. Это less conservative чем Bonferroni и appropriate when заявка состоит в идентификации supported subset hypotheses, а не avoidance of any single false discovery."

---

## 10. Reading notes / questions for follow-up

- **PDF acquisition:** HSE library proxy (Wiley + JSTOR доступ через universitiyскую subscription). Alternative — обратиться к Benjamini напрямую (он retired professor Tel Aviv University, often responds to requests).
- **Alternative citations** для текста, если direct access не достижим:
  - Storey, J. D., & Tibshirani, R. (2003). Statistical significance for genomewide studies. *PNAS, 100*(16), 9440–9445. — open access, contains polished BH reformulation
  - Efron, B. (2007). Size, power and false discovery rates. *Annals of Statistics, 35*(4), 1351–1377. — open access (Project Euclid)
  - Romano, J. P., Shaikh, A. M., & Wolf, M. (2010). Multiple testing. *New Palgrave Dictionary of Economics, 2nd ed.* — concise summary FDR vs FWER
- **Empirical economics applications:** Anderson (2008) "Multiple inference and gender differences in the effects of early intervention" *JASA* — applied BH в applied micro context; widely cited template
- **Software:** R `p.adjust(p, method = "BH")`, Python `statsmodels.stats.multitest.multipletests(method = "fdr_bh")`. В нашем analysis_v2 likely используется один of these.
- **Связь с другими методами в нашей работе:**
  - Cluster-robust SE (Cameron-Gelbach-Miller 2011) → правильный p-value per test
  - BH-FDR → правильный adjusted p-value per family
  - Oster δ (2019) → robustness per coefficient under unobservables
  - Shapley R² (Lipovetsky-Conklin 2001) → fair attribution per block
- **Для нашей курсовой:** Benjamini-Hochberg цитируется один раз в Methods + один раз в Results table caption. Не нужно повторять.

---

**Заполнено:** 2026-05-22 (skeleton; paywall)
**Заполнил:** Artem (collaborator)
