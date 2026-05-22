# Lipovetsky & Conklin (2001) — Analysis of Regression in Game Theory Approach

> ⚠ **Skeleton only — paywall:** статья за paywall (Wiley); preprint / open access version не найден после поиска через Google Scholar, SSRN, ResearchGate, author homepages. Скелет заполнен на основании abstract (открытый), follow-up paper Lipovetsky & Conklin (2010) и Grömping (2007) review в American Statistician, который подробно реферирует метод. **Перед финальным цитированием Кириллу — попытаться получить через HSE library proxy или contact authors.**

---

## 1. Citation (APA)

Lipovetsky, S., & Conklin, M. (2001). Analysis of regression in game theory approach. *Applied Stochastic Models in Business and Industry, 17*(4), 319–330. https://doi.org/10.1002/asmb.446

---

## 2. Source metadata

- **Type:** methodological
- **Sample:** не applicable (algorithmic paper с numerical examples — marketing data)
- **Method:** Shapley value (Shapley 1953 cooperative game theory) применённый к decomposing R² в multiple regression для quantifying relative importance of predictors
- **Pages used in this summary:** abstract + Grömping (2007) secondary review
- **DOI / URL:** https://doi.org/10.1002/asmb.446
- **Access status:** paywall (Wiley Online Library); 403 Forbidden при попытке скачать через DOI
- **Local file:** — (не скачано, см. предупреждение выше)

---

## 3. Use mapping (КРИТИЧНО для интеграции)

- **Stream:** А (методы)
- **Section in coursework:** Methods §3.x (R² decomposition — главный методологический вклад работы); Discussion §5 (interpretation of Shapley results)
- **Supports hypothesis(es):** не support конкретную гипотезу — это методологическая основа главного результата Shapley R²-декомпозиции на 9 блоков
- **Specifically supports argument:** Это first paper, формализовавший применение Shapley value к R² регрессии. Наш main methodological contribution — Shapley decomposition факторов на 9 блоков (Performance, Age+Experience, Demographics, Awards, Durability, International, Team, Structural, Market) с 2⁹ = 512 subset-fits — прямо основан на этом методе. Цитата обязательна в Methods и при первом упоминании метода в Introduction / Discussion.

---

## 4. Core thesis (3-5 предложений, по abstract + secondary sources)

Авторы предлагают применить Shapley value из кооперативной теории игр для решения проблемы quantifying relative importance отдельных предикторов в multiple regression при наличии multicollinearity. Стандартные подходы (standardized β-coefficients, sequential R², partial correlations) дают результаты, зависящие от order включения регрессоров или от specific spec; multicollinearity может приводить к "negative inputs" (когда добавление переменной формально снижает R² из-за деталей parameterization) или к biased ranking важности. Shapley value атрибутирует каждому регрессору его average marginal contribution к total R² по всем возможным subsets (permutations of inclusion), что делает атрибуцию order-independent и axiomatically justified (efficiency, symmetry, dummy/null player, additivity). Для k регрессоров требуется fit всех 2^k subsets, что вычислительно затратно (exponential в k), но даёт consistent decomposition. Численный пример авторов — marketing application с correlated brand attributes — демонстрирует, что Shapley даёт устойчивое ранжирование там, где sequential R² меняется в зависимости от order.

---

## 5. Key claims for our text (нумерованный список)

1. **Problem statement:** standard regression diagnostics (β-coefficients, sequential R²) зависят от order и спецификации; multicollinearity усугубляет проблему. У нас 9 блоков переменных с сильной within-block correlation (Performance metrics, Demographics, и т.д.) → Sequential R² разный при разных planned vs reverse порядках.

2. **Axiomatic foundation:** Shapley value — unique solution, удовлетворяющая efficiency (sum = total R²), symmetry, null player (irrelevant predictor = 0 contribution), additivity. Это motivates использование Shapley в нашей работе как "fair" attribution.

3. **Algorithm:** для каждого регрессора i — average его marginal contribution R²(S ∪ {i}) − R²(S) по всем S ⊆ {predictors} \ {i}, weighted by combinatorial multiplicity. Для k предикторов — 2^k subset fits.

4. **Computational cost:** наша работа делает 2⁹ = 512 OLS fits для main Shapley decomposition (см. `analysis_v2/h_decomposition.py`). Это уже на границе computational feasibility для standard hardware (~90 sec в наших measurements); поэтому Shapley decomposition обычно делается на уровне **блоков** (как у нас), а не отдельных переменных (там было бы 2¹⁵³ fits).

5. **Comparison to Sequential R²:** наша работа отчётливо демонстрирует value Shapley vs Sequential — sequential plan order и sequential reverse дают разные attributions для коррелированных блоков (Awards vs Performance), а Shapley стабилизирует среднее.

---

## 6. Direct quote candidates (с page numbers)

> ⚠ Full text за paywall — точные verbatim цитаты с page numbers недоступны.
>
> Из abstract: "Working with multiple regression analysis a researcher usually wants to know a comparative importance of predictors in the model. However, the analysis can be made difficult because of multicollinearity among regressors, which produces biased coefficients and negative inputs to multiple determination from presumably useful regressors. To solve this problem we apply a tool from the co-operative games theory, the Shapley Value imputation. We demonstrate the theoretical and practical advantages of the Shapley Value and show that it provides consistent results in the presence of multicollinearity."
>
> **Альтернатива:** для финальной курсовой Кириллу — либо verbatim цитата из этого abstract (с пометкой "abstract"), либо ссылка на Grömping (2007) или Lipovetsky (2021) [Game theory in regression modeling: a brief review on Shapley Value regression] для парафразной цитаты с p. numbers.

---

## 7. Methodological notes

- **Method name:** Shapley value regression (Shapley value R² decomposition)
- **Key formula / definition:** для регрессора i из набора N = {1, ..., k}:
  - φ_i(R²) = Σ_{S ⊆ N\{i}} [|S|! · (k − |S| − 1)! / k!] × [R²(S ∪ {i}) − R²(S)]
  - где сумма по всем подмножествам S не содержащим i; вес — комбинаторный
  - Свойства: Σ_i φ_i = R²(N) (efficiency); симметрия; null player → 0; additivity (decomposable through sums of models)
- **Key assumption(s):** стандартные предпосылки OLS на каждом из 2^k subset-fits; нет дополнительных distributional assumptions сверх baseline
- **Where applicable in our work:** `analysis_v2/h_decomposition.py` (computes 2⁹ = 512 subset OLS fits для main Shapley R² decomposition на 9 блоков; cluster bootstrap CI; efficiency check Σ φ_block = R²_full с tolerance 1e-6)
- **Caveat / pitfall:** (a) computational complexity 2^k → block-level decomposition стандартная стратегия для больших k; (b) Shapley value не учитывает structural information (например, awards = downstream от performance) — это limitation для causal interpretation; наш Discussion должен явно отметить, что Shapley даёт *descriptive* attribution, не causal effect

---

## 8. Limitations / caveats

1. **Computational explosion:** 2^k subset fits → impractical для k > 25 (в наших measurements 2⁹ = 512 уже занимает ~90 sec на M2 laptop)
2. **No causal interpretation:** Shapley — purely accounting-style decomposition variance explained; не identifies causal effect each block
3. **Sensitive к group definition** (block decomposition): если блок состоит из collinear variables → attribution внутри блока неопределённа (Shapley в этом смысле "решает" multicollinearity между блоками, но не внутри)
4. **Не информативен про non-linearities / interactions** между блоками — Shapley value по R² ≠ interaction decomposition; для последнего нужны methods like Owen (1972)

---

## 9. Connection to our findings

**SUPPORTS (theoretical foundation для главного методологического вклада)** — без Lipovetsky-Conklin 2001 у нас не было бы axiomatic justification для главного результата работы.

Наш headline finding "Performance + Age = 65.5%; Awards = 12.2%; Demographics = 14.1%; Durability = 5.7%; Market + Team + Structural ≈ 2.4%" — это **прямой выход Shapley R² decomposition на 9 блоков**. Без axiomatic foundation (efficiency, symmetry, etc.) этот результат был бы просто one of many possible attribution orderings (Sequential R² с plan order даёт другие числа из-за collinearity Performance ↔ Awards). Lipovetsky-Conklin даёт основание утверждать, что наша атрибуция — **canonical, order-independent**.

Это означает, что цитата abs absolutely essential в:
- Methods (introduction of method);
- Discussion (interpretation of decomposition headline);
- Conclusion (мы могли бы написать "Shapley decomposition даёт первую axiomatically-justified attribution of variance в NBA salary literature" — это claim about novelty methodology, который опирается на Lipovetsky-Conklin как foundation).

---

## 10. Reading notes / questions for follow-up

- **PDF acquisition:** попробовать HSE university library proxy (Wiley доступ обычно есть в крупных универсамах), или contact автора S. Lipovetsky напрямую — он часто отвечает на email requests за свои paper'ы (last known affiliation: GfK Custom Research).
- **Alternative citations** если paywall не преодолим:
  - Grömping, U. (2007). Estimators of relative importance in linear regression based on variance decomposition. *American Statistician, 61*(2), 139–147. — open access на BHT Berlin sites, содержит детальный survey Shapley regression подходов
  - Lipovetsky, S. (2021). Game theory in regression modeling: A brief review on Shapley Value regression. *Modeling Assistance for Decision Sciences*. — открытый журнал, может содержать полное описание метода
- **Связь с другими методами:** Owen (1972) value для interaction-decomposition мог бы быть future work для нашей курсовой (decomposing not just block contributions but cross-block interactions) — упомянуть в Limitations или Conclusion.

---

**Заполнено:** 2026-05-22 (skeleton, paywall)
**Заполнил:** Artem (collaborator)
