# Hölmström (1979) — Moral Hazard and Observability

> **Фундаментальная теоретическая работа** Нобелевского лауреата (2016). Содержит **informativeness principle** — основу всей последующей литературы по контрактам, включая incentive дизайн в спорте. **НЕ** в `bibliography_proposal.md`; рекомендуется к добавлению как ВЫСШИЙ приоритет (новый источник из CSV-анализа).

---

## 1. Citation (APA)

Hölmström, B. (1979). Moral hazard and observability. *The Bell Journal of Economics, 10*(1), 74–91. https://doi.org/10.2307/3003320

---

## 2. Source metadata

- **Type:** theoretical (formal microeconomic model — principal-agent с moral hazard)
- **Sample:** не applicable (теоретическая работа; иллюстративный numerical example — "repairman" в Section 2 с конкретными G(w), U(w), V(a))
- **Method:** partial-equilibrium principal-agent model; first-order approach (агентское IC ограничение заменяется FOC); pointwise optimization; characterization теорема через Likelihood Ratio
- **Pages used in this summary:** 74–75 (Introduction, problem statement), 75–80 (Sec 2: optimal sharing rules when payoff alone observed), 81–82 (Sec 3: insurance deductibles application), 82–84 (Sec 4: optimal use of imperfect information), 84–87 (Sec 5: когда additional информация ценна — главный результат), 87 (Sec 6: heterogeneous beliefs), 88 (Sec 7: summary)
- **DOI / URL:** https://doi.org/10.2307/3003320 ; JSTOR stable URL: https://www.jstor.org/stable/3003320
- **Access status:** JSTOR paywall; open access PDF доступен на gwern.net (https://gwern.net/doc/economics/1979-holmstrom.pdf — selectable text version, использован в этом summary)
- **Local file:** `bibliography/pdfs/holmstrom_1979.pdf`

---

## 3. Use mapping (КРИТИЧНО для интеграции)

- **Stream:** В+ (NEW — proposed addition from CSV analysis). Theoretical foundation для **Stream 3 (Awards / signaling)** и **Limitations** (контракт-shirking endogeneity). Также имплицитно поддерживает методологический выбор Mincer-spec'и (продуктивные сигналы → reward).
- **Section in coursework:** **Lit Review §2 Framework** (теоретическая рамка для всей литературы по contract design в спорте; обязательно как первый теоретический anchor вместе с Rosen 1981 и Lazear-Rosen 1981); **Methods §3** (обоснование почему observable performance metrics, awards, durability входят в Mincer как контракт-relevant signals); **Limitations §6.x** (endogeneity caveat — shirking → MPR ≠ predicted, что объясняет почему наш H1 даёт β_ppg ниже потенциального "true" effort coefficient).
- **Supports hypothesis(es):** не support конкретную empirical гипотезу — даёт **theoretical scaffolding** для всех H, опирающихся на observable signals (H1 performance, H5/H6 awards channel, H10 durability). Косвенно — supports методологическое решение использовать lagged performance (как информативный сигнал prior effort, не только current talent).
- **Specifically supports argument:** Информативность принцип Hölmström говорит: **любой informative signal об усилии агента имеет positive value в optimal contract**. Это даёт нам канонический аргумент почему GM NBA включают **множество** performance метрик в salary (PPG, WS, BPM, awards, durability) — не для двойного подсчёта, а потому что каждый дополнительный сигнал информативен об ненаблюдаемых компонентах effort/talent. Наша Shapley декомпозиция на 9 блоков — эмпирическая реализация этой идеи (каждый блок ловит свою dimension информативности). Цитата нужна в Lit Review как первый-блок основания всей последующей дискуссии о contract dynamics, shirking (Berri-Krautmann 2006, Krautmann-Donley 2009), CY syndrome (White-Sheldon 2014), sunk-cost (Keefer 2021).

---

## 4. Core thesis (3-5 предложений)

Hölmström формализует principal-agent проблему с moral hazard: агент выбирает скрытое действие a (effort) с дизутилитой V(a), которое влияет на распределение наблюдаемого payoff x; принципал должен спроектировать sharing rule s(x), которое одновременно (а) обеспечивает агенту резервную полезность, (б) индуцирует второй-лучший выбор effort (constrained Pareto-optimum). Главное содержание — **informativeness principle** (Sec 4–5, Proposition 3): дополнительный сигнал y (помимо payoff x) **строго улучшает** контракт **тогда и только тогда**, когда y несёт информацию о действии a, не содержащуюся в x. Формально, y бесполезен если и только если likelihood ratio f(x,y;a)/f(x,y;a') факторизуется как h(x;a)/h(x;a') × g(x,y) (Hölmström даёт точную formula 17, p. 84). Этот результат — необходимое и достаточное условие — обобщает Harris-Raviv (1976) и стал каноническим для проектирования incentive contracts; в Sec 3 показано приложение к insurance deductibles (которые оптимальны при moral hazard); в Sec 6 — обобщение на heterogeneous beliefs.

---

## 5. Key claims for our text (нумерованный список)

1. **Moral hazard determinant:** "individuals engage in risk sharing under conditions such that their privately taken actions affect the probability distribution of the outcome" (p. 74). Это прямое описание NBA principal-agent setup: GM/owner = принципал, игрок = агент, action = unobservable effort/training/conditioning, outcome = observable stats (PPG, durability) → salary.

2. **Pareto-optimal risk sharing precluded под moral hazard:** "only a second-best solution, which trades off some of the risk-sharing benefits for provision of incentives, can be achieved" (p. 74). Обоснование для нашего интерпретирования reward function NBA как нелинейной (cap tiers + supermax) — это институциональный second-best, не optimal full-information contract.

3. **Informativeness principle (Proposition 3, p. 84):** "a signal is valuable if and only if it is informative". Прямое теоретическое обоснование почему MVP / All-NBA / DPOY формально включены в Designated Player (supermax) criteria — это informative signals о квази-непосредственно неизмеримой "elite talent" dimension; и почему наш H5/H6 (awards → +20% salary через 2-3 года) — реализация этого принципа.

4. **Sufficient statistic характеристика optimal contract** (Sec 4, eq. 16–17): если y "достаточная статистика" об a при данном x — она бесполезна; иначе её надо включить в s(x,y). Это даёт критерий для **необусловливания** salary на дополнительных переменных, которые уже агрегированы внутри performance — например, если PPG уже включает FG%, отдельно FG% не несёт информации (наш H1 одного PPG достаточно).

5. **Numerical illustration (repairman example, p. 79–80):** при G(w)=w, U(w)=2√w, V(a)=a², x ~ exp(1/a) — оптимальная s(x) выпукла, не линейна. То есть optimal incentive contract — нелинейный, что обосновывает почему NBA salary не линейна в performance, а кусочно-параметрическая через tier-структуру cap (наш headline finding H3, R²=0.85 на одних tier dummies).

---

## 6. Direct quote candidates (с page numbers)

> "It has long been recognized that a problem of moral hazard may arise when individuals engage in risk sharing under conditions such that their privately taken actions affect the probability distribution of the outcome." (p. 74)

> "Pareto-optimal risk sharing is generally precluded, because it will not induce proper incentives for taking correct actions. Instead, only a second-best solution, which trades off some of the risk-sharing benefits for provision of incentives, can be achieved." (p. 74)

> "It is shown that any additional information about the agent's action, however imperfect, can be used to improve the welfare of both the principal and the agent." (p. 75)

> "A signal is valuable if and only if it is informative." (Proposition 3, p. 84)

---

## 7. Methodological notes

Не методологическая работа в смысле эконометрики — это теоретическая модель. Для пояснений в Lit Review достаточно вербального изложения; формальные detail (likelihood ratio, FOC approach) — для Discussion / Limitations с ссылкой на p. 78–84.

---

## 8. Limitations / caveats

1. **First-order approach** — Hölmström предполагает, что IC ограничение агента можно заменить first-order condition. Это валидно при monotone likelihood ratio property (MLRP) и concavity; в общем случае может приводить к ошибкам (см. Mirrlees 1974, Rogerson 1985). Для NBA это второстепенно, но критично для academic strictness в Methods.

2. **Single action, single period** — нет dynamic dimension. Сontract year syndrome (White-Sheldon 2014) — это явно multi-period с opt-out timing, что требует более сложной модели (Lazear 1979 на ratchet, или Holmström-Milgrom 1987 для dynamics).

3. **Risk-aversion агента критична** — при risk-neutral агенте moral hazard исчезает (sell-the-firm contract). NBA-игроки очевидно risk-averse (guaranteed contracts → preference for stability), что обосновывает наблюдаемые конкретные структуры.

4. **Одна "action" dimension** — реальный NBA-effort multidimensional (offense effort vs defensive effort vs conditioning), что даёт effort-substitution каналы (Holmström-Milgrom 1991). White-Sheldon 2014 эмпирически документируют такое substitution: CY-boost в scoring, post-CY drop в "hustle" stats — это именно multidimensional moral hazard.

5. **Не институциональный** — модель не учитывает cap, max-contract limits, free-agency rules; для NBA это надо overlaynaging через Coon CBA FAQ.

---

## 9. Connection to our findings

**SUPPORTS (theoretical foundation)** — Hölmström даёт каноническое теоретическое обоснование для:

(а) **дизайна нашей Mincer-спецификации** — почему мы включаем PPG, WS, BPM, awards (lagged), games_missed (durability), tier — каждая переменная informative signal о разных скрытых dimension effort/talent (informativeness principle);

(б) **наблюдаемой нелинейности reward** (H3, tier dummies R²=0.85) — это empirical artifact second-best contract в институциональной обстановке cap;

(в) **Limitations нашего empirical exercise** — мы оцениваем reduced-form association MPR-proxy (lagged stats) с salary, **не** причинно identifying contract design parameters. Hölmström-perspective даёт нам язык для четкой формулировки этой границы.

(г) **Aging-veteran discount** (multi_all_nba ≥3 → −22%) можно интерпретировать как rebalancing второй-лучшего contract: GM знают, что у veteran star меньше будущих сезонов под risk → optimal contract сдвигает risk-sharing назад к owner, снижая marginal reward за past awards. Без Hölmström-фрейма это просто эмпирический шум.

---

## 10. Reading notes / questions for follow-up

- **Predicted impact:** **Рекомендуется к добавлению в финальную bibliography ВЫСШИЙ приоритет.** Hölmström 1979 — обязательный теоретический anchor наряду с Rosen 1981 и Lazear-Rosen 1981 для Lit Review framework. Без него все последующие работы по contract dynamics в спорте (Berri-Krautmann 2006, Krautmann-Donley 2009, Stiroh 2007, Keefer 2021, White-Sheldon 2014) висят без теоретического основания. Нобелевский лауреат (2016) — придаёт solidity цитируемой литературе.

- **Цепочка наследования для нашего текста:**
  - Hölmström (1979) → теория информативности сигналов и second-best contracts
  - → Lazear-Rosen (1981) → tournament theory как частный случай (relative performance evaluation)
  - → Rosen (1981) → superstar phenomenon как market amplification of talent
  - → Berri-Krautmann (2006), Stiroh (2007) → эмпирическая проверка shirking в NBA
  - → White-Sheldon (2014) → psychological lens на CY эффект
  - → наш H1, H5/H6, H10, и Limitations про endogeneity MPR-proxy

- **Альтернативные citation candidates для теоретической рамки:** если объём ограничивает, можно сжать до сводной ссылки на Hölmström через **Hölmström & Milgrom (1991)** "Multitask Principal-Agent Analyses" — это более прямо про эффект substitution dimensions (применимо к White-Sheldon CY scoring vs hustle stats).

- **Связь с Limitations:** обязательно в Discussion / Limitations написать "Our reduced-form Mincer specification estimates association between observable performance proxies and salary; it does not identify deep moral-hazard contract parameters (Hölmström, 1979). Endogeneity of effort allocation (shirking, contract-year boost) is partially absorbed by lagged structure and tier dummies but cannot be fully ruled out without instrumental variation."

- **Нет ли confusion** между Hölmström (1979) Bell J. и Hölmström (1982) "Moral Hazard in Teams" Bell J. — обе работы fundamental, но (1979) — про single-agent multi-signal, (1982) — про peer monitoring и free-riding. Для наших NBA-целей **(1979) релевантнее**, потому что игрок ≠ team в Hölmström'овском смысле (NBA-салари индивидуальны).

---

**Заполнено:** 2026-05-22
**Заполнил:** Artem (collaborator)
