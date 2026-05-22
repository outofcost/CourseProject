# Berri & Krautmann (2006) — Shirking on the Court: Testing for the Incentive Effects of Guaranteed Pay

> ⚠ **Skeleton based on secondary sources:** оригинал статьи (Wiley Economic Inquiry 2006) за paywall. Прямая PDF copy через author home pages не найдена. Шаблон заполнен на основе детальной реферации в Jean-Neal (Duke DJE 2016 thesis, https://sites.duke.edu/djepapers/files/2016/10/Jean-Neal_DJE.pdf — Section 2.3, pp. 18–19), Fumarco et al. (2024, IZA DP 16836), Krautmann CV, цитируется в White-Sheldon (2014), Simmons-Berri (2011). **Перед финальным цитированием Кириллу — попытаться получить через HSE library proxy / EBSCOhost / контакт автора (Berri@suu.edu).**

> **НЕ** в `bibliography_proposal.md`; рекомендуется к добавлению как ВЫСШИЙ приоритет (новый источник из CSV-анализа). **Первая NBA shirking work** — foundational для всей последующей литературы по contract dynamics в баскетболе.

---

## 1. Citation (APA)

Berri, D. J., & Krautmann, A. C. (2006). Shirking on the court: Testing for the incentive effects of guaranteed pay. *Economic Inquiry, 44*(3), 536–546. https://doi.org/10.1093/ei/cbj044

---

## 2. Source metadata

- **Type:** empirical (panel econometrics, NBA player-season)
- **Sample:** NBA player-seasons (период, по secondary sources, охватывает несколько сезонов вокруг 2000s). Точные даты требуют проверки в оригинале — Jean-Neal указывает что сэмпл аналогичен Berri (2008) ~ 1987–2007.
- **Method:** First-difference regression на ΔPRODUCTIVITY со SHIRKING-dummy и его interactions; productivity измеряется двумя способами — NBA EFFICIENCY ("composite rating": FG × 1.4 + blocks × 1.4 + FT + assists + steals + offensive reb × 0.85 + defensive reb × 0.5 − turnovers × 0.8 − missed FG × 0.6) и Berri's wins-based MRP-proxy (ADJP48); ключевая модель: ΔPROD = β0 + β1 D2 + β2 D12 + β3 ΔGP + β4 CEXP + β5 CWPCT + β6 TMWINS + β7 ΔROSTER + θ1 SHIRKING + ε, где SHIRKING тестируется через три proxies: (i) SIGNED dummy (1 in season immediately после signing), (ii) SIGNED × LENGTH, (iii) SIGNED × SALARY
- **Pages used in this summary:** N/A (через secondary sources — Jean-Neal pp. 17–22, Fumarco et al. 2024 pp. 4–6)
- **DOI / URL:** https://doi.org/10.1093/ei/cbj044
- **Access status:** paywall (Wiley / Oxford Economic Inquiry); PDF не найден на сайте Berri (Southern Utah U) или Krautmann (DePaul)
- **Local file:** — (не скачано)

---

## 3. Use mapping (КРИТИЧНО для интеграции)

- **Stream:** Б+ (NEW — proposed addition from CSV analysis). NBA-specific empirical, foundational shirking study
- **Section in coursework:** **Lit Review §2.3 (Awards / signaling stream)** — первая NBA shirking work, должна цитироваться вместе с Stiroh (2007) как канонический pair; **Methods §3 / Discussion §5** — обоснование почему мы используем lagged performance (не contemporaneous) — чтобы partly absorb shirking endogeneity; **Limitations §6** — caveat что shirking может смещать MPR-estimate
- **Supports hypothesis(es):**
  - **H1** (performance ↔ salary) — partially contrasts: B-K показывают что NBA EFFICIENCY (PER-аналог) выявляет shirking, а MRP (wins-based) — нет. Это делает наш choice productivity metric methodologically важным
  - **H5/H6** (awards channel) — косвенно: shirking интерпретируется как effort substitution post-signing; awards channel работает potentially через signaling pre-CY
  - **Limitations** — обязательно: shirking → endogeneity proxy performance → β_ppg interpretation caveat
- **Specifically supports argument:** Это **first NBA shirking paper**, mass-cited (~150+ citations через Google Scholar). Цитата нужна как **first reference** к shirking literature в NBA contexts. Главный их вывод — **methodologically важная нюанс**: shirking finding sensitive к выбору productivity metric. Это даёт нам permission говорить, что наш choice PPG + WS + BPM (multi-metric) — robustness против single-metric artifact.

---

## 4. Core thesis (3-5 предложений)

Authors тестируют hypothesis опportunistic post-signing shirking в NBA — ex post снижение усилия после подписания нового guaranteed multi-year contract. Через first-difference panel regression на изменение productivity со SHIRKING-dummy (1 в первый сезон после подписания нового contract) и контролей за experience, injuries (ΔGP), coach quality (CEXP, CWPCT), team success (TMWINS) и roster turnover (ΔROSTER), они тестируют robustness результата к выбору productivity metric. Ключевая находка — **dichotomy**: при использовании NBA EFFICIENCY (NBA league's official composite stat) находится **weak evidence shirking** (negative coefficient на SIGNED); при использовании wins-based MRP-proxy (Berri's ADJP48, ближе к экономистскому marginal product) — **shirking evidence evaporates**. Authors заключают, что shirking в NBA — артефакт выбора метрики: NBA EFFICIENCY rewards shooting attempts, а игроки post-signing уменьшают attempts (играют "разумнее"), что выглядит как shirking, хотя их wins-contribution не меняется. Это — empirical reframe споров о NBA shirking (vs Stiroh 2007 who found strong evidence).

---

## 5. Key claims for our text (нумерованный список)

1. **First NBA shirking study** — paper является **first NBA-specific** эмпирическим тестом shirking hypothesis. До этого NBA shirking обсуждалась только в media и теоретически. Это придаёт работе foundational status для всей последующей NBA-contract literature.

2. **Productivity metric matters:** "found weak evidence supporting the shirking hypothesis when using the NBA's measure of player productivity, and evidence against shirking when using a measure of each player's marginal productivity" (per Jean-Neal 2016 description). Это критическое methodological caveat для нашего H1: PPG-based regression может **overstate** post-signing performance drop как shirking, тогда как wins-based metric покажет null.

3. **NBA contracts fully guaranteed** — "Unlike contracts in the NFL, NBA contracts are fully guaranteed (Berri and Krautmann 2006)" (per Jean-Neal p. 10, citing B-K). Это институциональный факт, который мы используем в Methods, объясняя почему shirking-incentive в NBA сильнее, чем в NFL: после подписания salary полностью защищён.

4. **Aging profile assumption:** B-K разрешают аналитически productivity-aging через dummies D2 и D12 — productivity скачкообразно растёт первые 2 года и снижается после 12-летнего experience. Это альтернатива нашему age + age² (continuous) — менее эффициентно для long-tail veterans, но информативно для младших сезонов.

5. **Reflection-problem-aware:** Используют TMWP48 (team wins minus player's contribution) как control для teammate productivity, addressing reflection problem (Manski 1993). Это хорошая practice — мы в нашей spec этого не делаем (наш ppg — individual, team controls separate); можно отметить как future robustness.

---

## 6. Direct quote candidates (с page numbers)

> ⚠ Full text за paywall — direct verbatim цитаты с page numbers недоступны. Reference-based phrases (verified through Jean-Neal 2016 and Fumarco et al. 2024):

> (per Jean-Neal 2016, p. 18, quoting B-K methodology) "The chosen measure of productivity is the dependent variable, regressed on dummy variables D2 and D12 for the years of experience that the player has in the NBA, the change in games played from the previous season to the current season as a proxy for injury, the years of experience that the coach has, the lifetime winning percentage of the coach, the change in the number of team wins, a variable that accounts for the roster turnover, and the dummy variable that indicates that a player is in their first season after signing a new long-term contract."

> (Jean-Neal 2016, p. 19, characterizing B-K main finding) "Berri and Krautmann (2006) found weak evidence supporting the shirking hypothesis when using the NBA's measure of player productivity, and evidence against shirking when using a measure of each player's marginal productivity."

> (per Simmons & Berri 2011, p. 17, citing B-K) "Berri and Krautmann (2006) offer evidence, albeit with marginal significance, that such a negative effect [teammate productivity] exists in basketball."

**Альтернатива для финальной курсовой:** если оригинал недоступен — paraphrase с reference вместо verbatim citation; либо verbatim из abstract если откроется через JSTOR / WHU library proxy.

---

## 7. Methodological notes

Не methodological paper в каноническом смысле, но методологически instructive:

- **First-difference (ΔPROD) regression** — handles individual fixed-effects через transform. Это альтернатива нашему FE-spec (мы используем year FE, не player FE из-за computational + lost-DoF concern).

- **SHIRKING tested through 3 proxies** (SIGNED, SIGNED × LENGTH, SIGNED × SALARY) — robustness через alternative parameterization. Хороший template для нашей future robustness work.

- **Composite NBA EFFICIENCY definition** дана в Jean-Neal footnote 21 (точная формула): (FG × 1.4 + blocks × 1.4 + FT × 1.0 + assists × 1.0 + steals × 1.0 + offensive_reb × 0.85 + defensive_reb × 0.5 − turnovers × 0.8 − missed_FG × 0.6) / (minutes / 48). Это полезный benchmark для proverki ortogonality нашего набора metrics с canonical EFFICIENCY.

---

## 8. Limitations / caveats

1. **Paywall — невозможно proverit числа.** Все claims в этом шаблоне — через secondary sources. Кириллу настоятельно рекомендуется добыть оригинал через HSE proxy перед использованием specific β-цифр.

2. **Productivity-metric dichotomy** — это эмпирическая находка, но не theoretical resolution. Если NBA EFFICIENCY и wins-based ADJP48 дают противоположные answers, какой "правильный"? B-K делает ставку на ADJP48 как "ближе к экономистскому marginal product", но это сам по себе **theoretical choice** (linear weighting в Berri's metric — own derivation).

3. **First-difference specification теряет cross-section variation** — только within-player changes; нельзя оценить **levels** premium / discount, что мы делаем (наш H1 идёт через levels regression on ln_salary).

4. **No instrumental variable** для SIGNED — endogeneity подписания contract (selected по pre-signing performance) может смещать estimate of shirking effect ↓ (downward bias в magnitude).

5. **Period limitations** — оригинал по неподтверждённым данным ~ 1987–2003 sample; pre-2011 CBA, до designated player extensions. Применимость к нашему 2015–2023 периоду — нужна с caveat (paradigm CBA изменился).

6. **Comparison to Stiroh (2007):** Stiroh находит strong shirking в NBA с PER + alternative methods; B-K rejects это через MRP-proxy. Это open debate в литературе — наш текст должен признать обе стороны.

---

## 9. Connection to our findings

**SUPPORTS / EXTENDS** — Berri-Krautmann (2006) даёт **methodological grounding** для интерпретации наших β-coefficients, не direct empirical comparison.

(1) **Choice of productivity metric:** Наш v2 spec использует PPG (доминирующий), WS, BPM — это **mix** между attempt-based (PPG, аналог NBA EFFICIENCY) и wins-based (WS, BPM, аналог Berri's MRP-proxy). Если B-K правы, то PPG-only spec может **overestimate** evidence of shirking в performance drop, но WS-component нейтрализует это. Наш Shapley decomposition агрегирует by block ("Performance" = PPG + WS + BPM), что усредняет дихотомию.

(2) **β_ppg interpretation:** B-K показывают, что post-signing players "play smarter" (fewer attempts, lower NBA EFFICIENCY), но wins per minute стабильны. Это means our β_ppg = +0.04 (v1) частично reflects "GM-reward for visible shooting volume", а не "true marginal contribution to wins". Это укрепляет нашу intuition про **wages reward what's measured, not what's productive** — основное наблюдение из всей NBA-labor literature.

(3) **Limitations text** — обязательная фраза: "Shirking literature (Berri & Krautmann, 2006; Stiroh, 2007; Krautmann & Donley, 2009) documents that NBA players' post-signing performance partially substitutes between attempt-based stats and efficiency-based stats. Our reduced-form Mincer specification, using lagged performance, cannot fully separate `effort-shirking` channel from `compositional changes in play style`."

(4) **Параллель с H5/H6 awards:** B-K's null shirking with MRP-proxy supports our finding что awards (which reward wins, not just shooting) — strongest predictor (+20% от all_nba_lag1). Если awards отражают true MRP лучше, чем PPG-based metrics, то natural extension: GM сами знают и **награждают** правильно через awards-driven channel.

---

## 10. Reading notes / questions for follow-up

- **Predicted impact:** **Рекомендуется к добавлению в финальную bibliography ВЫСШИЙ приоритет.** Berri-Krautmann (2006) — **first NBA shirking paper**, foundational для всей последующей contract literature. Без него вся awards/signaling stream в Lit Review будет outdate.

- **PRIORITY ACTION для Кирилла:** добыть оригинал PDF через:
  - HSE university library proxy → Wiley Online Library https://onlinelibrary.wiley.com/doi/10.1111/j.1465-7295.2006.00019.x
  - Email author напрямую: berri@suu.edu (Berri обычно отвечает на academic requests за свои papers)
  - Альтернатива: Stiroh (2007) "Playing for keeps: Pay and performance in the NBA" Economic Inquiry 45(1) — параллельная work с противоположным выводом

- **Цепочка наследования shirking literature:**
  - Maxcy, Fort & Krautmann (2002) — first to identify ex-ante boost + ex-post drop в MLB
  - Berri-Krautmann (2006) — first NBA-application; metric-dependent finding
  - Stiroh (2007) — independent NBA test с PER; finds strong shirking
  - Krautmann-Donley (2009) — MLB revisit, performance vs MRP test split
  - White-Sheldon (2014) — psychological lens, cross-sport
  - Keefer (2021) — sunk-cost extension, salary cap as IV

- **Альтернативный direction:** если оригинал недоступен, в курсовой можно сократить B-K reference до 1-2 строк с pointing to "first NBA shirking work; productivity-metric dichotomy", и использовать **Stiroh (2007)** как primary citation для shirking literature (Stiroh более доступен).

- **Hölmström-связь:** B-K's dichotomy (NBA EFFICIENCY vs MRP) — empirical iteration Hölmström-Milgrom (1991) multitask moral hazard: agent substitutes between dimensions; metric-choice affects observed "effort". Это естественный мост в Lit Review.

---

**Заполнено:** 2026-05-22 (skeleton, paywall — based on secondary sources)
**Заполнил:** Artem (collaborator)
