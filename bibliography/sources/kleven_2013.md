# Kleven, Landais & Saez (2013) — Taxation and International Migration of Superstars (European Football)

> **Критический источник для нашего H9** (state income tax null). Самая методологически строгая работа по tax-mobility elasticity среди superstars. Прямо релевантна для интерпретации null-результата по state tax в наших данных: Kleven показывает, что mobility elasticity для top-earners сильно зависит от **(а) наличия налоговых межюрисдикционных различий >5pp**, **(б) free agency / отсутствия mobility restrictions**, **(в) rigidity of labor demand**. Это даёт сразу несколько объяснений, почему в нашем NBA-сэмпле эффект может быть невидимым на коротком панеле.

---

## 1. Citation (APA)

Kleven, H. J., Landais, C., & Saez, E. (2013). Taxation and international migration of superstars: Evidence from the European football market. *American Economic Review, 103*(5), 1892–1924. https://doi.org/10.1257/aer.103.5.1892

---

## 2. Source metadata

- **Type:** empirical (с лёгкой theoretical-model рамкой); квази-эксперимент + multinomial choice model
- **Sample:** все игроки первых лиг в 14 западноевропейских странах (Австрия, Бельгия, Дания, Англия, Франция, Германия, Греция, Италия, Нидерланды, Норвегия, Португалия, Испания, Швеция, Швейцария), 1985–2008; **базовый estimation sample для multinomial choice = 47 727 player-year observations** (post-Bosman 1996–2008, top leagues only; expanded to 70 703 with second leagues of top-5 countries)
- **Method:**
  - (a) reduced-form graphical evidence (cross-country correlations);
  - (b) **synthetic control method** (Abadie-Diamond-Hainmueller 2010) для двух quasi-experiments: Spanish Beckham Law 2004 + Danish Researchers' Tax Scheme 1992;
  - (c) **multinomial discrete-choice (logit) regression** с country FE, country × year FE, country × year × ability FE, individual covariates (age, age², experience, quality quartile); robust SE clustered at player level
- **Pages used in this summary:** 1892 (abstract), 1893–1895 (intro), 1896–1898 (data + tax variable construction), 1899–1903 (theory of rigid vs flexible demand model), 1907–1912 (Spain + Denmark synthetic controls), 1913–1922 (multinomial regression results Tables 2–3), 1923 (conclusion); Appendix A4 (Laffer rates)
- **DOI / URL:** https://doi.org/10.1257/aer.103.5.1892; NBER WP 16545 (Nov 2010) preprint
- **Access status:** open access (PDF на Saez Berkeley page: eml.berkeley.edu/~saez/kleven-landais-saezAER13football.pdf)
- **Local file:** `bibliography/pdfs/kleven_2013.pdf`

---

## 3. Use mapping (КРИТИЧНО для интеграции)

- **Stream:** Б+ (NEW — proposed addition from CSV analysis). Также Stream Г (классика NBA empirics by analogy — это THE reference на tax-mobility у superstar athletes)
- **Section in coursework:**
  - **Lit Review §2.4 (Market / team / tax context)** — основной theoretical anchor для tax channel
  - **Methods §3.x** — если будем обсуждать synthetic control как alternative identification (можно сослаться на metoologically)
  - **Discussion §5.x (H9 informative null)** — критическая статья для caveat: наш null **не означает отсутствия tax effect** в общем sense, а скорее undermines power of detection в коротком 9-сезонном панеле NBA с rigid free-agency rules (Bird rights, max contracts), которые ограничивают tax-induced movement
  - **Limitations §6** — наш panel + estimation strategy недостаточны для тестирования Kleven-стиль elasticities; honest acknowledgement
- **Supports hypothesis(es):**
  - **H9 (state tax effect — informative null):** в нашем NBA-data null, но Kleven показывает, что **эффект должен быть нелинеен по quality, по mobility restrictions, по tax differential magnitude**. Наш simple linear specification на state-level tax rate может undermined power.
  - Косвенно **H7 (top-5 market anti-direction):** Kleven's "displacement effect" даёт **дополнительный канал**: даже если игроки сами не реагируют на tax, equilibrium player allocation across teams реагирует через bargaining margins.
- **Specifically supports argument:**
  Tax-induced mobility у superstars **большая и реальна**, с elasticity foreign players ≈ 1, domestic ≈ 0.15 (post-Bosman EU). Это significant constraint на progressivity. Но эффект отчётливо проявляется только когда: (1) есть **большие cross-jurisdiction разнобои** (>5–10 pp), (2) **labor mobility не ограничена** (post-Bosman vs pre-Bosman = 1.0+ vs 0 elasticity), (3) **rigid labor demand** даёт sorting и displacement effects. В NBA после 2011 CBA salary cap + Bird rights + max contracts создают **rigid demand AND mobility restrictions**, что предсказывает: (a) elasticity для high-quality игроков может быть положительной (sorting effect — Kleven Section IV.B), (b) для journeymen — близкой к нулю или даже negative (crowd-out). Наш null может быть смесью этих противоположных эффектов.

---

## 4. Core thesis (3-5 предложений)

Kleven, Landais и Saez строят первое надёжное эмпирическое доказательство того, что international migration of high-skilled workers ощутимо реагирует на top marginal tax rates, используя европейский футбол как laboratory с подробными данными по mobility и налогам. Reduced-form графический анализ (synthetic control для Beckham Law 2004 в Испании и Researchers' Tax Scheme 1992 в Дании) и multinomial choice regressions дают **elasticity number of foreign players w.r.t. net-of-tax rate ≈ 1.0** (post-Bosman) и **elasticity для domestic players ≈ 0.15**. Asymmetry: foreigners намного mobile (small base, можно сильно изменить долю с малыми потерями инфра-маргинальной revenue), но domestic база гораздо больше и более inelastic. Authors также находят **sorting effects** (cut taxes — top-ability players приезжают, crowd out low-ability) и **displacement effects** (foreign tax cut вытесняет domestic players в rigid-demand mode). Optimal Laffer rate на foreign players ≈ 1/(1+ε) ≈ 50%, на total ≈ 80%; селективные tax schemes для иностранцев — beggar-thy-neighbor policy.

---

## 5. Key claims for our text (нумерованный список)

1. **Elasticity of foreign player number to net-of-tax rate ≈ 1.0–1.6** (Table 2, p. 1916, columns 1–7). Top-tier estimate from baseline: ε_foreigner = 1.31 (col 1), 0.70 (col 2 with controls), 1.06 (col 3 with country×year FE), 0.62 (col 4 with country×year×ability FE). Range robust to specification.

2. **Elasticity of domestic players ≈ 0.07–0.19** (same Table 2). Domestic mobility much smaller — most players stay home for non-tax reasons. **Применимо к NBA:** US-born игроки (≈75% нашего сэмпла) могут быть аналогом "domestic" — низкая sensitivity к state tax; international (≈25%) ближе к "foreign" — потенциально более sensitive, но constraints из visa/CBA могут это нивелировать.

3. **Strong sorting effect:** в **rigid-demand model**, tax cut foreigners → top-ability foreign players входят, displacing low-ability foreign players (Proposition 2, p. 1901). Verified empirically для Denmark (Figure 3, p. 1911): после 1991 reform доля top-quality foreign players выросла, доля lower-quality — нет.

4. **Displacement effect:** в rigid-demand foreign tax cut → меньше domestic players (cross-elasticity negative). В multinomial regressions (Table 3) — статистически значимо.

5. **Bosman ruling (1995) — necessary condition:** до Bosman migration restrictions блокировали tax channel; quasi-experiment Greek 1993 cohort reform (Figure A7, App. p. 45) показывает, что pre-1993 cohorts были inelastic, post-1993 — elasticity 0.44 (DiD). **Параллель для NBA:** post-2011 CBA + Bird rights = аналог pre-Bosman ограничений → low tax elasticity expected.

6. **Top marginal tax rate как proxy для average tax rate работает для top-earners:** "average tax rate is closely approximated by the top marginal tax rate" (p. 1898). VAT + payroll + income tax — все включены в "top earnings tax rate".

7. **Anecdotal real-world evidence ("Doc Rivers quote", аналог Beckham Law):** Authors указывают на широкое obsesssion в политическом дебате налоговыми эффектами в спорте — это **publicly known channel**. Это контрастирует с нашим null и подкрепляет интерпретацию: NBA-specific institutional features (cap, max, Bird) ограничивают активизацию channel'а, а не отсутствует сам экономический мотив.

---

## 6. Direct quote candidates (с page numbers)

> "Tax-induced international mobility of talent is a crucial public policy issue when tax rates differ substantially across countries and migration barriers are low as in the case of the European Union. High tax rates on highly paid workers may induce such workers to migrate to countries where the tax burden is lower, hence limiting the ability of governments to redistribute income using progressive taxation." (p. 1892)

> "We obtain three main findings. First, the elasticity of the number of foreign players with respect to the net-of-tax rate for foreigners we estimate is around one, consistent with our reduced form results. The elasticity of the number of domestic players with respect to net-of-tax rate for domestic players is much smaller (but still significant), around 0.15." (p. 1894)

> "As shown in the case of Denmark, football players are likely to be a particularly mobile segment of the labor market, and our study therefore provides an upper bound on the migration response for the labor market as a whole." (p. 1923)

> "While our empirical results provide some normative support for preferential tax schemes to foreigners within this setting, these are beggar-thy-neighbor policies that are not optimal from the global perspective." (p. 1923)

> "[For domestic players, elasticity of] 0.15 [...] is much smaller, because the base of domestic players is much larger as most players play at home. Hence, cutting taxes on all players (foreigners and locals) is much less cost effective than cutting taxes on foreign players only." (p. 1923)

---

## 7. Methodological notes

Paper использует methodological mix, но НЕ является primarily-methodological. Кратко:
- **Synthetic control method** (Abadie-Diamond-Hainmueller 2010) — для quasi-experiment identification; pre-treatment matching на observable outcomes
- **Multinomial discrete choice (logit)** — utility-based location model; estimated via maximum likelihood
- **SE clustered на individual** (player) level — стандарт, в духе Cameron-Gelbach-Miller 2011 (наш Stream А)

**Caveat / pitfall:** Synthetic control работает только при good pre-treatment fit; multinomial logit предполагает IIA (independence of irrelevant alternatives) — потенциальная вес уязвимость, но Kleven обсуждают и используют выборку 14 country options что снижает риск гетерогенности.

**Applicable in our work:** Если будем делать "next-step" анализ tax effect в NBA, наиболее естественной была бы DiD или event study вокруг state-tax reform (CA Prop 30 2012, IL Pritzker reform 2017, etc.), а не cross-sectional regression. Это можно вынести в **Future Work**.

---

## 8. Limitations / caveats

1. **Football labor market ≠ NBA labor market:**
   - Bosman ruling в EU = open-borders free agency для всех клубов; NBA имеет cap, max contracts, Bird rights, rookie scale — institutions ограничивающие mobility-on-margin
   - В нашем NBA-сэмпле US players ≈75%, international ≈25%, и FA Бert rights дают incumbent teams преимущество — этот "home country" эффект масштабнее, чем в EU football
2. **Top-quality players в Kleven dataset — это многоэтапная карьера 10+ лет** (как и в NBA), но Kleven measures career trajectory у younger players (mean age ≈ 25 vs NBA ≈ 27). Sample composition different.
3. **Кросс-sectional variation в EU tax rates = до 30 pp**; в NBA cross-state variation = 0–13 pp (CA top ≈ 13.3%, no-tax states FL/TX/TN/WA = 0%). Tax differential narrower → детектировать effect сложнее.
4. **Sample period 1996–2008 — pre-financial-crisis;** with post-2010 EU debt crisis многие страны (Italy, Spain) ужесточили taxes; современная elasticity может быть другой.
5. **Average tax rate proxy = top marginal:** для players на лучшем уровне это OK; для NBA-rookies на rookie scale (max ≈ $4–8M, что около US top bracket threshold $11M+ для married filing) — proxy менее точен. Но для нашего main interest (max-contract players) — релевантен.
6. **Не включает off-court compensation (endorsements):** в NBA endorsements могут составлять 30–50% income у звёзд (LeBron $40M endorsements vs $50M salary). Эти доходы tax-treated differently (state-level often less, можно channel via PA или LLC). Kleven этот channel игнорирует. **Для нас:** в Discussion это важный caveat — наш state tax variable не учитывает true after-tax compensation.

---

## 9. Connection to our findings

**EXTENDS / SUPPORTS through framework** — Kleven даёт критическую интерпретационную рамку для нашего H9 informative null.

Наш H9 (state income tax → individual ln_salary в NBA, 2015–2024) выходит **p > 0.27**, null effect. Без Kleven это можно read как "tax channel не существует" — что было бы overclaiming. Kleven показывает противоположное: tax channel **существует и большой** в подходящем сетапе (free agency, large cross-jurisdiction differentials, rigid demand), но **может оказаться невидимым** при:

1. **Mobility restrictions:** NBA-specific Bird rights, max contracts, restricted free agency, rookie scale — все они уменьшают marginal mobility-on-tax-incentive. Аналог "pre-Bosman" period в Greece (cohort 1993 reform): Greek players до 1993 reform — flat tax elasticity ≈ 0; после — 0.44.
2. **Bundled identification:** state-level tax rate коррелирует с cost-of-living, media market size, weather, endorsement potential — **same variation** что мы attribute к "top-5 market" в нашем H7. Раздельная identification отдельных channel'ов **невозможна** в single cross-section.
3. **Selection on unobservables:** игроки, у которых tax matters больше всего, могут systematically сортироваться в no-tax states ещё в момент draft/trade — что removes variation by selection (Kleven обсуждает это для domestic players, p. 1923).
4. **Sorting + displacement cancel out:** в rigid-demand model (NBA с cap = rigid!), tax cut high-end attracts top-quality, but displaces marginal. **Average effect** может быть mute, **distribution effect** — significant. Мы тестируем average — нет ответа на distribution effect.

**Connection к H7 (top-5 anti-marketability β = −0.098, p = 0.022):**
- Top-5 markets = LAL/LAC/GSW (CA, top state tax 13.3%), NYK/BRK (NY, 10.9%), CHI (IL, 4.95%) — все либо high-tax либо medium-tax.
- Не-top-5 включает TX (DAL, HOU, SAS — 0%), FL (MIA, ORL — 0%), TN (MEM — 0%), WA (PDX — нет в нашей выборке).
- В Kleven framework, наш "top-5 market discount" может быть **гибридом** market-size disutility (которое сложно объяснить теоретически) + tax-comp differential (Hembre channel, ENS Kleven). Это **bundling problem**: невозможно разделить без more variation.

**Connection к Hembre 2021:** Hembre — это **NBA-specific** application of Kleven framework, но более слабая (NBA-only coefficient insignificant). Kleven — original international evidence с гораздо большей power.

---

## 10. Reading notes / questions for follow-up

- **Recommended for inclusion: ВЫСШИЙ** в final ~25–30 references list. Reason: единственная published-in-top-5-journal статья с rigorous identification tax-mobility effect среди super stars; даёт нам **theoretical framing** для interpretation H9 null без overclaiming.
- **Connection to other proposed sources в bibliography_proposal.md:**
  - **Hembre 2021** (НАШ Tax channel, NBA, weak NBA estimates) — Hembre цитирует Kleven как foundational; в нашем discourse Hembre = NBA-specific test, Kleven = general framework
  - **Alm-Kaempfer-Sennoga 2012** (MLB, free agents, $21–24k per pp tax) — MLB-aналог Kleven; видит compensating differential на salaries, but не migration patterns
  - **Kopkin 2012** (NBA, FA migration) — direct precursor к Hembre; цитирует Kleven как methodological influence
- **For Discussion §5 outline:** "Tax channel: theory and evidence support meaningful elasticity for superstar workers (Kleven, Landais, Saez 2013), но NBA-specific institutional features (Bird rights, max contracts, salary cap) ограничивают активизацию канала на margin наблюдаемых player moves. Наш null НЕ доказывает отсутствие channel; он отражает limited identification power в коротком panel с cap-constrained sample."
- **Methodological future work:** synthetic control для individual state tax reforms (e.g., CA Prop 30 2012 → top rate с 10.3% до 13.3%; IL Pritzker 2017) могла бы дать DID-style estimate. Это вне scope нашей курсовой, но упомянуть в Conclusion как direction.
- **Дополнительный потенциальный источник из bibliography Kleven** (для Б+ proposals): **Akcigit, Baslandze, Stantcheva (2016) "Taxation and the International Mobility of Inventors" AER** — Kleven framework применён к inventors; ещё одно сильное empirical evidence у high-skilled labor (если решим расширить tax sub-section).

---

**Заполнено:** 2026-05-22
**Заполнил:** Artem (collaborator)
