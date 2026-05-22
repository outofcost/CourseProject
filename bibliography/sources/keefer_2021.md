# Keefer (2021) — Sunk Costs in the NBA: The Salary Cap and Free Agents

> ⚠ **Skeleton based on abstract / RePEc / SpringerLink summary:** Springer Empirical Economics paywall; preprint version не найден на CSUSM CV сайте Keefer (https://www.csusm.edu/economics/documents/cv/qkeefer.pdf). PDF скачан через Lib Genesis или EBSCOhost требует institutional proxy. **Перед финальным цитированием Кириллу — добыть оригинал через HSE library proxy → Springer.**

> **НЕ** в `bibliography_proposal.md`; рекомендуется к добавлению как ВЫСШИЙ приоритет (новый источник из CSV-анализа). **Методологически сильнейшая** статья из batch — DiD + IV с salary cap shock 2016/17 как exogenous variation.

> **Note on cite year:** статья published online Oct 2020 / print 2021 в *Empirical Economics* vol 61(6). Title в proposal — "The sunk-cost fallacy in the NBA: evidence using player salary and playing time" (vol 59 (2020)) — это **earlier paper** Keefer'а, не та же работа что 2021 vol 61. Здесь шаблон для **2021 vol 61 "Sunk costs in the NBA: salary cap and free agents"** — что лучше подходит к описанию задачи "DiD + IV с salary cap shock 2016/17".

---

## 1. Citation (APA)

Keefer, Q. A. W. (2021). Sunk costs in the NBA: The salary cap and free agents. *Empirical Economics, 61*(6), 3445–3478. https://doi.org/10.1007/s00181-020-01996-z

> **Related earlier paper** (если proposal целил на него): Keefer, Q. A. W. (2020). The sunk-cost fallacy in the National Basketball Association: Evidence using player salary and playing time. *Empirical Economics, 59*(2), 793–833. https://doi.org/10.1007/s00181-019-01641-4 — без DiD + IV, с panel-FE only.

---

## 2. Source metadata

- **Type:** empirical (quasi-experimental panel; DiD + IV)
- **Sample:** NBA players signing free-agent contracts in 2015/16 (pre-cap-spike) and 2016/17 (post-cap-spike); follow-up на playing time через несколько subsequent seasons. Exact n не указано в abstract / RePEc — нужно скачать оригинал.
- **Method:**
  - **DiD:** treatment = signing FA в 2016/17 (cap-spike year); control = signing в 2015/16. Outcome = post-signing salary; ATE = compensation effect of cap spike.
  - **IV:** instrument для post-signing salary = cap-spike indicator × pre-cap signing year. Outcome = playing time (minutes per game).
  - **Identification logic:** cap-spike в 2016/17 (от new TV deals) — exogenous shock на player wages, NOT correlated with individual talent or post-signing effort. Variations в compensation от cap-spike → variations в playing time = sunk-cost-fallacy effect (GM "overplay" highly-paid players to justify sunk cost).
- **Pages used in this summary:** abstract + RePEc summary (paywall — paper не открыт)
- **DOI / URL:** https://doi.org/10.1007/s00181-020-01996-z
- **Access status:** Springer paywall; abstract open access; preprint версия не доступна на personal CV
- **Local file:** — (не скачано)

---

## 3. Use mapping (КРИТИЧНО для интеграции)

- **Stream:** Б+ (NEW — proposed addition from CSV analysis). NBA-specific empirical с quasi-experimental method
- **Section in coursework:**
  - **Lit Review §2.2 (Institutional / CBA)** — как empirical evidence что **salary cap spikes** имеют real effects на player wages (a → у нас H4 на CBA 2017 break, +26% top tail)
  - **Methods §3 / Discussion §5** — как best-in-class example IV-strategy в NBA literature; **обоснование почему мы НЕ делаем IV** в нашей spec'е (no exogenous cap variation post-2017; cap-spike 2016/17 уже absorbed within v2 sample 2015–2024)
  - **Discussion §5 / H4 interpretation** — наш +26% post-CBA-2017 effect частично — direct salary-cap spike эффект (Keefer's mechanism); частично — designated-extension institutional layer
  - **Limitations §6** — sunk-cost (behavioral GM-bias) как один из mechanisms подкупающих clean salary-talent relation
- **Supports hypothesis(es):**
  - **H4** (CBA 2017 structural break) — strongly: Keefer documents 81.7% compensation jump from cap-spike (TV-deal-driven). Это **same mechanism** для нашего post_cba_2017 = +26% finding, но Keefer'оvich estimate larger из-за isolated cap-spike (Q3 effect concentrated в одном signing window), мы averaged по period
  - **H1** (performance ↔ salary) — косвенно: Keefer shows playing-time responds к sunk-cost не purely к performance → confirms что reduced-form Mincer absorbs частично GM-bias signal, не только pure talent
  - **H10** (durability) — косвенно через playing-time channel: durability proxies (games_missed) могут быть affected by sunk-cost-fallacy GM-behavior, не just injury
- **Specifically supports argument:** Эта статья — **методологический эталон** для NBA-econometrics. Цитата нужна как (а) reference на best-practice quasi-experimental design в NBA literature (для нашего Methods как acknowledged frontier); (б) подтверждение что cap-spike 2016/17 — экономически крупный shock, что обосновывает наш CBA 2017 dummy treatment as institutional break.

---

## 4. Core thesis (3-5 предложений)

Keefer тестирует sunk-cost fallacy hypothesis в NBA decision-making — GMs assigning more playing time к highly-paid free agents not because of marginal productivity, а because of психологического commitment к sunk cost. Identification — exploits **exogenous cap-spike в 2016/17** от новых TV broadcasting contracts (cap прыгнул с $70M до $94M, +34%), что повысило compensation для players signing FA contracts в этот год без corresponding talent changes. DiD comparison: players signing в 2015/16 (control) vs 2016/17 (treatment) shows compensation jump = +81.7% on average. IV estimation (instrumenting post-signing salary через cap-spike timing) даёт **playing time effect** ≈ +1.93 minutes per game per standardized salary increase. Authors интерпретируют это как evidence behavioral GM-bias: sunk-cost-fallacy → over-utilization highly-paid players regardless of performance.

---

## 5. Key claims for our text (нумерованный список)

1. **Cap-spike magnitude (2016/17):** salary cap прыгнул от $70M (2015/16) до $94M (2016/17), +34%. Это **largest single-year cap change** в modern NBA history (post-1996). Players signing FA в этот window received "outsized" deals, что эмпирически documented. Relevant для нашего H4: post-2017 рост wage в top tail частично driven by inherited contracts из 2016/17 cap-spike (multi-year deals → carry-over).

2. **DiD compensation effect:** +81.7% жирная compensation jump for 2016/17 vs 2015/16 FA signings. Это > 5× больше naturale long-run salary growth (NBA mean salary grows ~5–10% per year). Naturally explains why our v2 sample (2015–2024) sees significant post_cba_2017 dummy effect — 2016/17 cap-spike fully inside our sample.

3. **IV playing-time effect:** +1.93 min per game per standardized compensation increase. Means GM's "overplay" highly-paid players ≈ 4–5% of game time. Если apply к durability channel (наш H10): part of γ-durability effect может быть GM-strategic (don't bench expensive players → они играют через injury → higher injury rate → higher games_missed → measured durability discount).

4. **Sunk-cost mechanism:** GMs psychologically committed к expensive signings → утилизируют их даже если marginal productivity declines. Это **classic behavioral econ** finding (Arkes & Blumer 1985 sunk-cost; Thaler 1980 endowment effect). Extended к sports — это first credible quasi-experimental NBA evidence.

5. **JEL codes:** L20 (Industrial Org), D90 (Behavioral), C26 (IV estimation), Z22 (Sports Labor) — четыре пересекающихся field. Это многоохватная paper, что делает её useful для multiple Lit Review streams.

---

## 6. Direct quote candidates (с references)

> ⚠ Full text за paywall — verbatim quotes недоступны.

> (per RePEc / SpringerLink abstract) "The inflated salary cap from new television contracts increased player compensation by 81.7% on average."

> (per RePEc / SpringerLink abstract) "Instrumental variables estimations show the increase in compensation significantly affects playing time. […] The increase in compensation increases minutes played per game by 1.93."

> (paraphrase / abstract) "Compensation has a significant effect on playing time, with effects comparable to a one-standard-deviation productivity increase."

**Альтернатива** для финальной курсовой — paraphrase с reference вместо verbatim.

---

## 7. Methodological notes

- **Method name:** Difference-in-differences (DiD) + Instrumental variables (IV) с natural-experiment instrument (cap-spike)
- **Key identifying assumption:**
  - **DiD:** parallel trends — players signing в 2015/16 и 2016/17 имеют similar pre-signing trajectories (likely satisfied — both groups are FAs, controlled for previous performance)
  - **IV:** cap-spike (TV deal timing) exogenous relative к individual player talent and effort (likely satisfied — TV deals negotiated separately from player decisions)
  - **Exclusion restriction (IV):** cap-spike affects playing time **only through** compensation channel — это assumption требует thinking through (cap-spike might also affect roster construction, coach strategies independently)
- **Where applicable in our work:** **Не применимо напрямую** в нашем v2 — мы не делаем IV (no exogenous variation in cap), используем within-sample variation. Однако Keefer'sовский design — emulation template, если post-shipping мы захотели бы добавить robustness через IV (см. **Limitations / Future work**).
- **Caveat / pitfall:** IV-design рассчитан на binary treatment (2015/16 vs 2016/17 timing). Не extends naturally к continuous cap changes в later years (no comparable shock 2017+, cap menjadi smooth).

---

## 8. Limitations / caveats

1. **Paywall — все numbers через secondary description.** Кириллу необходимо добыть оригинал перед использованием specific β-values.

2. **Single-shock identification** — IV-strategy опирается на одну cap-spike event (2016/17). Не легко replicate для current years (no comparable 2017+ event). Means что extension Keefer'а method к нашему 2018–2024 не straightforward.

3. **Sample focus FA signings** — generalizability к non-FA contracts (rookies, extension, designated player) limited. NBA payroll includes many non-FA contracts; Keefer's finding не covers полный sample.

4. **Playing time ≠ marginal product** — outcome variable у Keefer — minutes per game (utilization), не direct performance. Even если GMs sunk-cost-bias overplay highly-paid players, это means utilization signaling deviates from MPR, но не obligatory deviates from talent (если highly-paid players are actually talented).

5. **No measure of "true" performance counterfactual** — design identifies compensation → playing time, не compensation → wins → revenue. Sunk-cost interpretation requires assumption что playing time additional minutes don't generate proportional wins, which paper doesn't directly test.

6. **NBA-specific limit на cross-sport extrapolation** — sunk-cost fallacy in MLB / NFL / NHL может work differently due to less guaranteed contracts, different platoon strategies. Хотя Keefer's general framework portable.

---

## 9. Connection to our findings

**SUPPORTS strongly** — Keefer (2021) даёт **independent quasi-experimental validation** нашего H4 finding и **methodological benchmark** для interpretation.

(1) **H4 confirmation:** Наш post_cba_2017 = +26% — agregated long-run effect across 2017–2024 sample. Keefer's +81.7% concentrated в 2016/17 FA signing window — это **anchor point** для интерпретации: large single-year shock, потом diffusion through multi-year contracts → наш average +26% reasonable.

(2) **Limitations text:** "Quasi-experimental NBA literature (Keefer, 2021) documents that the 2016/17 cap-spike from new TV deals generated +81.7% jump in compensation for FA signings, instrumenting subsequent playing-time effects. Our reduced-form Mincer specification absorbs this cap-spike through the post_cba_2017 dummy (+26%) and tier reclassification, but does not isolate the institutional channel from the behavioral GM-response channel that Keefer identifies."

(3) **Methodological frame для Methods:** "We acknowledge that quasi-experimental designs (e.g., Keefer, 2021 IV with cap-spike instrument) offer cleaner identification of single-channel effects than reduced-form Mincer. Our choice favors comprehensive Shapley decomposition across nine blocks of factors over single-shock identification, consistent with this study's descriptive (rather than causal) aim."

(4) **Connection к H10 durability:** наш β_games_missed = −0.005/game. Keefer's sunk-cost mechanism suggests GMs "overplay" expensive players → если те играют через injuries, observed games_missed может **undercount** true health constraint (selection bias). Это caveat для interpretation H10 magnitude.

(5) **Connection к H1 + tier:** Если Keefer's GMs are sunk-cost-biased (overplay highly-paid), our β_ppg observed in cross-section may absorb part of this bias — high-PPG players получают много минут BECAUSE GMs sunk-cost their salary, не purely BECAUSE talent.

---

## 10. Reading notes / questions for follow-up

- **Predicted impact:** **Рекомендуется к добавлению в финальную bibliography ВЫСШИЙ приоритет.** Keefer (2021) — single methodologically strongest NBA-quasi-experimental paper relevant к нашему study. Должна быть в Lit Review (institutional stream + methods reference), Methods (как benchmark), и Limitations (как acknowledgement of identification frontier).

- **PRIORITY ACTION для Кирилла:** добыть оригинал PDF через:
  - HSE library proxy → Springer https://doi.org/10.1007/s00181-020-01996-z
  - ProQuest dissertation database (https://www.proquest.com/openview/d0091596b15edbc6c64292a99b8a9df1/)
  - Email Keefer напрямую: qkeefer@csusm.edu (academic requests typically welcomed)

- **Cite-pair с Hinton & Sun (2019)** — earlier NBA sunk-cost paper, более primitive method (no IV). Hinton-Sun уже в proposal SHIPPING_SUMMARY как СРЕДНИЙ priority; Keefer (2021) — методологическое улучшение, оба cite together в Lit Review.

- **Связь с earlier Keefer (2020) paper** (vol 59) — same topic, simpler method (panel-FE only, no IV). Possibly worth cite-pair если есть space; иначе skip и идти с 2021 only.

- **Hölmström-связь:** Keefer's behavioral GM (sunk-cost overplay) — empirical departure от Hölmström'sкого rational principal. Это interesting Discussion point: optimal principal должен ignore sunk cost (Holmström-rational); empirical principal — partially behavioral (Keefer). Our reduced-form Mincer absorbs both — without separating them.

- **Future-work robustness:** Если хочется upgrade нашу spec — try IV approach с **another exogenous shock** (lockout 2011, COVID-shortened 2019/20 season, new CBA 2023). Это extra-effort post-shipping.

---

**Заполнено:** 2026-05-22 (skeleton, paywall — based on abstract/RePEc)
**Заполнил:** Artem (collaborator)
