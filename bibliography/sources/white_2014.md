# White & Sheldon (2014) — The Contract Year Syndrome in NBA and MLB

> **НЕ** в `bibliography_proposal.md`; рекомендуется к добавлению как СРЕДНИЙ приоритет (новый источник из CSV-анализа). Прямой эмпирический CY эффект в NBA с psychological lens (Self-Determination Theory).

---

## 1. Citation (APA)

White, M. H., II, & Sheldon, K. M. (2014). The contract year syndrome in the NBA and MLB: A classic undermining pattern. *Motivation and Emotion, 38*(2), 196–205. https://doi.org/10.1007/s11031-013-9389-7

---

## 2. Source metadata

- **Type:** empirical (psychological / sports science; повторные измерения MANOVA)
- **Sample:**
  - **NBA (Study 1):** 170 игроков, сезоны 2003/04 – 2009/10 (8 лет); каждый игрок — 3 наблюдения (pre-CY / CY / post-CY) = **510 player-years**. Mean age в CY = 26.73; pre-CY salary range $350K – $25M (mean $4.77M), post-CY $932K – $20M (mean $6.2M). По позициям: 30 PG, 36 SG, 35 SF, 34 PF, 35 C. Исключения: игроки без back-to-back CY и без двойных CY в периоде (первый CY включён).
  - **MLB (Study 2):** 60+ pitchers и 100+ hitters (точное n в Table 2/3 paper'а)
- **Method:** Repeated-measures MANOVA по 3 measurement points (pre-CY/CY/post-CY); ANCOVA controlling for salary; OLS regression салари на CY-перформанс
- **Pages used in this summary:** 196 (abstract + intro), 197–198 (метод, sample), 199 (Table 1 — main NBA результаты), 199–200 (Salary effects, MLB), 200–203 (Table 2/3, Discussion), 204 (Conclusion)
- **DOI / URL:** https://doi.org/10.1007/s11031-013-9389-7
- **Access status:** open access PDF на Self-Determination Theory archive (https://selfdeterminationtheory.org/wp-content/uploads/2020/10/2014_WhiteSheldon_ContractYearSyndromeNBAandMLB.pdf)
- **Local file:** `bibliography/pdfs/white_2014.pdf`

---

## 3. Use mapping (КРИТИЧНО для интеграции)

- **Stream:** Б+ (NEW — proposed addition from CSV analysis). NBA-specific empirical; psychological framing
- **Section in coursework:** **Lit Review §2.3 (Awards / signaling)** — как параллельный поток к Berri-Krautmann 2006, Stiroh 2007 (shirking); **Limitations §6** — обоснование почему shirking / CY-эффекты вносят endogeneity в MPR-proxy (lagged performance), что объясняет частичное "shrinkage" наших β_ppg/β_awards
- **Supports hypothesis(es):**
  - H1 (performance ↔ salary) — частично контрастно: CY boost эфемерный, post-CY переходит в "undermining"; означает что одна-сезонная performance — biased estimate "true talent"
  - H5/H6 (awards channel) — supports: paper показывает что boosted CY scoring предсказывает post-CY salary raises (b=0.32, p<.01 для points; b=0.25, p<.01 для PER), то есть GM **награждают** CY boost, что вписывается в "awards/signaling" логику
  - Косвенно — даёт основание для **Limitations** про endogeneity: shirking → MPR-proxy ≠ predicted from past performance
- **Specifically supports argument:** Этот paper — empirical evidence что shirking / opportunism цикл в NBA реален (post-CY drop в 4 стат: offensive reb, defensive reb, steals, PER). Для нашей курсовой это даёт **caveat** для интерпретации β_ppg: текущая salary partly reflects CY-inflated performance, не steady-state talent. Прямо релевантно также для нашего **aging-veteran discount** (multi_all_nba ≥3 → −22%): часть этого эффекта может быть пост-CY undermining у veteran-stars, а не чистый survival bias.

---

## 4. Core thesis (3-5 предложений)

Авторы используют panel из 170 NBA-игроков (2003/04 – 2009/10, 510 player-seasons) и аналогичной выборки MLB, отслеживая performance по трёхлетнему окну: pre-CY (baseline), CY (когда финансовый incentive максимально salient), post-CY (incentive снят). По теории extrinsic motivation (Bandura 1997, Vroom 1964) ожидается boost в CY относительно pre-CY; по Self-Determination Theory (Deci et al. 1999) — undermining ("classic undermining pattern") в post-CY ниже baseline для intrinsically-mediated усилий. Главные находки в NBA: (а) Points и FG% и PER значимо выше в CY (Table 1, F(2,167) > 5, p<.05); (б) post-CY drop в offensive rebounding, defensive rebounding, steals и PER ниже pre-CY уровня (undermining); (в) CY scoring → post-CY salary (b=0.32, p<.01), но post-CY salary ≠ post-CY performance — то есть GM "награждают" inflated CY, а игроки потом снижают усилие. Authors интерпретируют это как поддержку SDT: salient extrinsic reward подрывает intrinsic motivation, что проявляется как post-CY "syndrome".

---

## 5. Key claims for our text (нумерованный список)

1. **CY scoring boost — реален в NBA:** Points pre→CY: 14.08 → 14.6 (F(2,167)=7.8, p<.001, η²=0.044); FG%: 0.450 → 0.461 (F=5.2, p<.01); PER: 14.78 → 15.41 (Table 1, p. 199). То есть **single-season performance metrics overstate** steady-state talent для игроков в CY.

2. **Post-CY undermining — четыре стат показателя:** offensive rebounding, defensive rebounding, steals, и PER все значимо ниже **pre-CY baseline** в post-CY (Table 1). Это разрушает чистую "tournament theory" интерпретацию: не просто return-to-baseline, а dip ниже baseline → SDT-style undermining.

3. **Asymmetric scoring vs hustle:** CY-boost концентрируется в "scoring" (offensive points, FG%) — добровольно-управляемые "high-visibility" stats. Post-CY drop в "hustle" stats (rebounds, steals) — менее замечаемые на TV, требуют чистого effort. Это эмпирическая реализация **multitask moral hazard** (Holmström-Milgrom 1991): rewards attached к одной dimension → substitution от других.

4. **GM реагируют на CY boost через salary:** "post-CY salary, relative to CY salary, was significantly predicted by points scored in the CY (relative to pre-CY) at b=0.32, p<.01" (p. 199). То есть signals "работают" — точно как в нашей H5/H6 awards channel, но через single-season performance не cumulative awards.

5. **MLB results слабее:** только near-significant boost RBI в CY (p=.051); никакого CY-boost для batting average, HR, SLG, OBP. Post-CY drop наблюдается, но менее консистентный. То есть **CY syndrome — NBA-strong, MLB-weak**; для NBA это критично.

6. **Sample статистика для контекста NBA:** Mean salary pre-CY = $4.77M, post-CY = $6.2M (30% raise on average). 170 unique players, 510 player-seasons, период 2003–2010 (предкризисный, до designated extension reforms).

---

## 6. Direct quote candidates (с page numbers)

> "We assembled National Basketball Association and Major League Baseball player performance data from recent years, tracking 3 year periods in players' careers: pre-contract year (baseline), contract year (CY; salient external incentive present), and post-contract year (salient external incentive removed)." (Abstract, p. 196)

> "Using extrinsic motivation theories, we predicted and found a boost in some scoring statistics during the CY (relative to the pre-CY), but no change in non-scoring statistics. Using intrinsic motivation theories, we predicted and found an undermining of many statistics in the post-CY, relative to both the CY and the pre-CY baseline." (Abstract, p. 196)

> "Boosted CY scoring performance predicted post-CY salary raises in both sports, but salary raises were largely unrelated to post-CY performance. The CY performance boost is real, but team managers should know that it might be followed by a performance crash — the CY 'syndrome.'" (Abstract, p. 196)

> "post-CY salary, relative to CY salary, was significantly predicted by points scored in the CY (relative to pre-CY points scored) at b = .32, p < .01. Enhanced field goal percentage in the CY also predicted enhanced salary post-CY, (b = .19, p = .020). Enhanced PER in the CY also predicted enhanced salary post-CY at b = .25, p < .01." (p. 199)

> "Our results suggest that any statistical improvements by a player during his CY is unlikely to be maintained in the post-CY, even if the player does get the big payday. This knowledge could help slow the explosive and perhaps unsustainable growth of sports salaries." (Discussion, p. 203)

---

## 7. Methodological notes

Не методологическая paper в эконометрическом смысле — applied psychology / repeated-measures ANOVA. Пропускаю детальное методологическое заполнение.

(Используемые методы — MANOVA, ANCOVA с salary covariates, OLS regression — стандартные; для нашего эконометрического текста этих методов мы не используем напрямую.)

---

## 8. Limitations / caveats

1. **No causal identification:** sample selection (только игроки с pre-CY/CY/post-CY observations и без consecutive CY) исключает молодых rookies и veterans на коротких контрактах — ~30% NBA-population по нашим данным. Selection bias может усиливать observed CY effect (только игроки, которые **получили** новый contract, входят в sample → endogenous filtering).

2. **Small effect sizes:** η² = 0.03–0.05 — это меньше 5% variance объясняется CY-фазой. Effect statistically significant из-за n=510, но economically narrow. Нельзя из этого заявлять "shirking рулит NBA-payroll".

3. **Между-игроцкая heterogeneity не учтена:** ANOVA aggregate effect; нет individual fixed effects (в строгом эконометрическом смысле). Krautmann-Donley (2009), Berri-Krautmann (2006) — более методологически строгие версии тестирования shirking через MRP-comparison.

4. **No within-NBA controls:** team, position, age, opponent — не контролируются в основной MANOVA (только в ANCOVA с salary). Position effects заявлены как "проверены, не moderate", но детали в paper не показаны.

5. **MLB results weak:** авторы интерпретируют CY syndrome как универсальный — но MLB-эмпирика слабая (только RBI marginal). Это контраст с Krautmann-Donley (2009), которые в MLB находят shirking только через MRP-test, не perf-test. Suggests caution в обобщении на cross-sports.

6. **CY проксии — by hand:** авторы определяют CY вручную через salary discontinuities и contract data; нет источника, нет documentation методики — replication затруднена.

---

## 9. Connection to our findings

**EXTENDS / PARALLELS** — White-Sheldon (2014) даёт независимый эмпирический канал для интерпретации наших coefficients как partial signals "noisy with CY-shirking endogeneity".

Наш Shapley результат: Performance + Age = 65.5%; Awards = 12.2%; Durability = 5.7%. Если CY-boost реален и GM "награждают" его (что подтверждается b=0.32 на points в White-Sheldon), то наш β_ppg = +0.04 (v1) / +0.07 (within mid_level v2) частично absorbs CY-inflated performance — то есть **overstated** относительно "true talent → salary" effect; и наоборот, наш durability coef (β_games_missed = −0.005) может быть **understated**, если игроки специально "берегут себя" в pre-CY (consistent с CY shirking hypothesis).

Прямой connection к нашему **aging-veteran discount** (multi_all_nba ≥3 → −22%): часть этого пенальти может быть post-CY undermining цикл, накопленный за 3+ All-NBA selections. То есть наш unique sub-finding и White-Sheldon "post-CY syndrome" — комплементарны.

Best использование для нашего текста — **Limitations §6**: "Reduced-form Mincer-spec estimates association between observable lagged performance and contemporaneous salary; we cannot fully separate `true talent` channel from `signaling-via-CY-boost` channel. White & Sheldon (2014) document that NBA players exhibit measurable CY-boost (Points +3.7%, FG% +2.4%, PER +4.3%) followed by post-CY undermining in hustle stats. To the extent our sample includes CY-affected player-seasons, β_ppg may be biased upward as estimator of structural salary-talent elasticity."

---

## 10. Reading notes / questions for follow-up

- **Predicted impact:** **Рекомендуется к добавлению в финальную bibliography СРЕДНИЙ приоритет.** White-Sheldon — единственная работа, эмпирически документирующая CY-syndrome **в обоих** NBA и MLB с psychological framing. Цитата нужна в Lit Review (как часть awards/signaling stream) и в Limitations (для качественного caveat). Если объём ограничивает — можно сократить до single ref-citation в Limitations.

- **Альтернативная литература:** Berri-Krautmann (2006), Stiroh (2007) — более методологически строгие версии теста shirking в NBA. White-Sheldon более accessible (психологический фрейм, ясные графики), что хорошо для **introductory** обсуждения; B-K и Stiroh — для более formal econometric arguments в Lit Review.

- **Replication concern:** методика identification CY у авторов — не прозрачная. В курсовой не нужно полагаться на их числа как primary source; лучше упомянуть как qualitative evidence одного из нескольких источников по CY-эффекту.

- **Связь с нашими данными:** мы НЕ моделируем CY explicitly (v1 H6 был старая нумерация, выпала в Limitations). Если стоит вопрос о добавлении CY-dummy в robustness — это extra effort post-shipping; пока что White-Sheldon идёт в Limitations и Lit Review.

- **Hölmström-связь:** White-Sheldon — empirical evidence для **multitask moral hazard** (Hölmström-Milgrom 1991) в NBA: CY incentives → effort substitution от "hustle" к "scoring". Это естественный сюжетный мост в Lit Review: theory (Hölmström) → application (White-Sheldon).

---

**Заполнено:** 2026-05-22
**Заполнил:** Artem (collaborator)
