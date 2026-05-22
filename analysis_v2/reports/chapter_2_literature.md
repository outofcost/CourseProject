# Глава 2. Литературный обзор

> Драфт под HSE term paper, Article (Empirical) format. Объём: ≈ 20% работы (целевые ~2400 слов).
> Литературный обзор организован по пяти research streams; в конце главы формулируются 10 эмпирических гипотез (H1–H10) с привязкой к streams и литературе.
> Маркеры `[TBD: см. {author_year}]` помечают cite'ы, которые требуют верификации по шаблонам из `bibliography/sources/` (некоторые ещё не пришли от Claude-A — это будет дополнено в следующей итерации).

---

## 2.1 Подход к литературному обзору

Литература по экономике NBA salary располагается на пересечении пяти содержательных областей: (а) классической labor economics в её Mincer-tradition, (б) теории institutional design коллективных трудовых соглашений, (в) теории signaling и tournaments, (г) теории формирования team-side рыночной премии, (д) теории внешних эффектов (налоги, регуляция, кадровое здоровье). Эта глава следует данной структуре, обозначая ключевые работы в каждой области и формулируя 10 эмпирических гипотез, тестируемых в Главах 3–4.

## 2.2 Stream 1: Производительность и Mincer-формирование зарплат

Основу теоретической рамки нашего исследования составляет Mincer earnings function в её классической форме (Mincer, 1974), согласно которой $\ln(\text{salary}) = f(\text{schooling}, \text{experience})$ с возможным расширением через performance / productivity covariates. В контексте профессионального спорта natural extension этой функции — включение игровых статистик (points per game, assists, rebounds, advanced metrics) как proxy для productivity.

Классическая формальная база для понимания high-tail зарплат в NBA — superstar theory Rosen (1981). Rosen показывает, что при наличии **joint-consumption technology** (один продавец одновременно обслуживает много покупателей — TV-трансляция матча миллионам зрителей) и slight differences in talent, revenue function $R(q)$ становится convex по talent $q$, что даёт экстремальную асимметрию distribution вознаграждения: "There is concentration of output among a few individuals, marked skewness in the associated distributions of income and very large rewards at the top" (Rosen, 1981, p. 845). Формальное следствие при квадратичной cost function — "A person who is twice as talented as another earns four times more money" (Rosen, 1981, p. 849). NBA удовлетворяет двум common elements, которые Rosen отождествляет с superstar markets (p. 845): (а) close connection between personal reward and market size, (б) market size + reward gravitate towards higher-talent individuals.

Эмпирические применения Mincer-расширения к NBA имеют долгую традицию. Hausman & Leonard (1997) первыми quantitatively оценили economic value superstar players в NBA через attendance и TV ratings, документируя что «в дополнение к эффекту, который superstars оказывают на свои команды, они производят tremendous positive externality на other teams» (Hausman & Leonard, 1997, p. 9). Авторы оценивают, что Michael Jordan один поднял Bulls gate revenue на $8.6M в его дебютный сезон (Hausman & Leonard, 1997, p. 18), а Bird увеличил Celtics home attendance на ~50% (p. 17). Совокупный cross-team externality value Jordan'а — порядка $53M/год через TV ratings, road-game attendance и paraphernalia (Section V), что обосновывает upper-tail зарплат как marginal revenue, включая cross-team spillovers. Krautmann (1999) [TBD] предлагает критику Scully-style оценок player's marginal revenue product в team sports, аргументируя, что классические Mincer-spec'ы могут систематически смешивать individual MRP с team-level effects.

Hill & Groothuis (2001) [TBD] анализируют structural effects NBA CBA на distribution зарплат, показывая, что 1995 CBA с её salary cap и max contracts перевела часть salary growth из тонкого хвоста в средний tier. Это положило основу для последующей литературы об институциональном слое.

В современной post-2011-CBA эпохе появились исследования, которые включают расширенные advanced metrics (PER, Win Shares, BPM, VORP) в Mincer-spec'ы. [TBD: см. berri_brook_schmidt_2007.md.] Berri, Brook & Schmidt (2007) формально критикуют naïve performance-Mincer спецификации, аргументируя, что отдельные scoring metrics (PPG) систематически переоценивают свой эффект на salary за счёт корреляции с usage rate; они motivate inclusion advanced metrics типа Win Shares.

Возрастной профиль salary классически имеет inverted-U shape с peak около 28-30 лет — это эмпирический фактор, последовательно подтверждаемый в литературе для most professional team sports. В нашей предыдущей итерации проекта (v1, см. `analysis_v1/`) оценённый peak age = 30.6 лет согласуется с этой литературой.

## 2.3 Stream 2: Институциональная структура (CBA, salary cap)

Второй research stream фокусируется на эффекте institutional rules — salary cap, luxury tax, максимальная зарплата, дизайн extension contracts — на distribution зарплат. NBA отличается от других major leagues наиболее детальной структурой institutional caps, формализованной в серии CBAs (1995, 1999, 2005, 2011, 2017, 2023).

Каноническим практическим reference для деталей CBA является Coon (n.d.) FAQ — детальный практикоориентированный справочник, формализующий все правила соглашения. Согласно Coon (n.d., Q23), maximum salary structure разделена на три tiers по выслуге: 25% of cap (0–6 years), 30% (7–9 years), 35% (10+ years). Designated Player rule (Q24) дополнительно создаёт «supermax» eligibility для игроков, которые удовлетворяют performance criteria (All-NBA / DPOY / MVP selections). Это создаёт **discrete institutional layer** поверх Mincer continuous pricing.

Теоретическая литература о cap-induced concavity начинается с Rosen (1986) [TBD], который показывает, что binding cap создаёт concave reward function для top-tier игроков. Этот мecanism теоретически предсказывает, что $\beta_{\text{performance}}$ in cap-bound tiers должна быть ниже, чем в free-market tiers — что мы эмпирически тестируем через tier-specific Mincer regressions (Глава 4 §4.3).

Прямого quantitative анализа supermax-extension (введённой CBA 2017) в peer-reviewed литературе на момент написания работы обнаружено не было; институциональные детали Designated Veteran Extension доступны через Coon (n.d., Q24) как practitioner-reference, а количественный analysis эффекта supermax на team performance и player retention остаётся открытым gap, частично закрываемым настоящей работой через tier-classifier и H3-test.

Берри, Brook & Schmidt (2010) [TBD] и более раннее Berri (1999) [TBD] доказывают, что традиционные performance-based pay model недооценивают role institutional channelling: игроки с high observable stats но без awards selections могут systematically underprice'ить себя по сравнению с awards-elevated players в той же performance bucket.

## 2.4 Stream 3: Awards channel и signaling

Третий research stream — теория, по которой awards (All-NBA selections, MVP, DPOY) служат **signaling devices**, переводящими productivity в зарплату через институциональную премию. Теоретическая основа простирается на два уровня. На уровне fundamental incentive design — Hölmström (1979) формализует **informativeness principle**: «A signal is valuable if and only if it is informative» (Hölmström, 1979, p. 84, Proposition 3); любая дополнительная информация о действии агента может улучшить optimal contract. Это даёт теоретическое обоснование для inclusion множественных performance signals (PPG, WS, BPM, awards) в Mincer-spec'ах — каждая переменная улавливает свою dimension informativeness, а не дублирует другие.

На втором уровне — Lazear & Rosen (1981) разрабатывают rank-order tournament theory: они показывают, что compensation, основанная на относительном ранге, может implementовать тот же эффективный allocation эффорта, что и piece-rate compensation, при risk-neutral workers (Proposition 1, Section II.B, p. 7). Ключевая интуиция: «differences in the level of output between individuals may be quite small, yet optimal 'prizes' are selected in a way that induces workers to allocate their effort and investment activities efficiently» (Lazear & Rosen, 1981, p. 2). В NBA это формализуется в Designated Player rule (Coon, n.d., Q24): qualification by All-NBA First/Second/Third Team в most recent season, или Defensive Player of the Year, или MVP — даёт right на supermax extension. Это превращает signaling механизм Lazear-Rosen из abstract performance-incentive в concrete contractual eligibility — discrete prize в multi-stage tournament (15 All-NBA → 5 First Team → 1 MVP).

Эмпирически awards channel в NBA исследован в Hausman & Leonard (1997) (см. §2.2) и Stiroh (2007) [TBD]. Stiroh документирует contract-year effect — повышение performance в last year of contract — который мы тестируем через event study вокруг первого All-NBA selection в Главах 4–5.

Возможный counter-mechanism — **aging-veteran selection bias**: игроки с длинной awards-историей (multi-time All-NBA) непропорционально часто продолжают карьеру в declining phase, что создаёт residual penalty за past elite status (cumulative awards count). Эта возможность ранее не quantified в NBA литературе; наш H5/H6 sub-finding (multi_all_nba β = −0.22) делает первую попытку формализовать этот механизм.

## 2.5 Stream 4: Рыночный и командный контекст

Четвёртый research stream касается влияния external market characteristics — размера телерынка, городского населения, состава medien — на individual zarplaty. Теоретическое ожидание (Rosen 1981 superstar mechanism) — premium для игроков в крупных media markets через amplified individual market exposure.

Однако в post-2011-CBA эпохе с binding salary cap эта премия теоретически нейтрализуется на team-side: cap rules out monopsonistic surplus extraction, делая marginal revenue от больших рынков ≈ 0 для дополнительного спендинга на игрока. Это аргумент Hill & Groothuis (2001) [TBD].

Hembre (2022) предлагает дополнительный теоретический канал: при unrestricted free agency игроки требуют compensating differential за state income tax burden, что снижает spending power команд в high-tax штатах. Hembre находит pooled effect across 4 major US leagues: 1pp увеличение state tax rate → −0.77 до −0.86 pp в team win percentage (Hembre, 2022, p. 1). Важное caveat: **NBA-specific coefficient в Hembre Table 3 статистически незначим** ($\hat{\beta}_{\text{NBA}} \in [-0.143, -0.069]$, SE > 1.1, Table 3, p. 20). То есть Hembre даёт *theoretical channel*, совместимый с anti-marketability finding для NBA, но не direct empirical confirmation; pooled effect доминируется NFL и MLB sub-samples.

Дополнительные эмпирические работы [TBD: berri_brook_schmidt_2007.md, kahn_2000.md] критикуют market-size premium hypothesis: Berri et al. (2007) показывают, что после контроля individual performance team-level controls (revenue, market size, championship status) добавляют мало к explanatory power; Kahn (2000) в обзоре аргументирует, что cap-эпоха sports leagues создаёт labor market structure, в которой individual talent оценивается ≈ uniformly across markets.

Team-level контроли (win percentage, playoff success, luxury tax burden) — отдельный sub-stream. [TBD: добавить cite Berri-Schmidt 2010 после получения шаблона.] Эмпирический consensus в современной NBA литературе — team success имеет небольшой direct effect на individual salary после контроля player factors, потому что cap mechanism redistributes team revenue uniformly across roster через cap-allocated bidding.

## 2.6 Stream 5: Внешние эффекты (налоги, durability, международная композиция)

Пятый stream охватывает externalities: эффект state income tax, health record, и cultural / national characteristics на формирование зарплат.

State income tax effect в spor labor markets теоретически и эмпирически документирован тремя ключевыми работами. Kleven, Landais & Saez (2013) на panel 14 западноевропейских футбольных лиг за 1985–2008 (47,727 player-year observations) находят, что elasticity of foreign players w.r.t. net-of-tax rate ≈ 1.0 — игроки сильно реагируют на tax-induced compensating differentials, когда mobility не ограничена: «the elasticity of the number of foreign players with respect to the net-of-tax rate for foreigners we estimate is around one» (Kleven et al., 2013, p. 1894). Для domestic players elasticity составляет лишь 0.15 — sample fragility выше для locally-rooted игроков. Это foundational evidence того, что tax channel реален у superstar workers в spor labor markets.

Прямой US pro-sport empirical аналог — Alm, Kaempfer & Sennoga (2012) для MLB: на 372 free agents за 1995–2001 они находят, что 1pp увеличение state+local tax rate повышает pre-tax FA salary на $21–24 тыс. (Alm et al., 2012, Table 3, p. 11), что эквивалентно elasticity 0.5–0.66 в log-log spec. Authors интерпретируют это как evidence того, что «income taxes are largely shifted away from mobile players to other factors, such as the franchise itself» (Alm et al., 2012, p. 13). Mechanism — compensating differential через free agency.

Промежуточный NBA-specific empirical step — Kopkin (2012), который тестирует, влияют ли state-level income tax rates на decisions NBA free agents о club destination в сезонах 2001/02 – 2007/08. Kopkin предлагает важное theoretical уточнение для NBA: tax effect реализуется через **quality sorting** (команды в low-tax штатах непропорционально часто signing top-quality FAs), а не через salary level differentiation. Mechanism — players value after-tax income; при условиях binding salary cap (max contract ограничивает nominal pre-tax salary), adjustment margin переходит с salary level на destination choice. Это даёт альтернативное объяснение, почему MLB-style salary-compensation effect (Alm et al., 2012) может не реализоваться в NBA, при том что tax channel сам по себе активен.

Прямой NBA-specific тест на individual salary level приходится на Johnson & Hall (2018) — paper, ближайший по setup к нашему: на 576 NBA free agent signings за 2010–2014 они находят, что **1pp increase в average tax rate повышает FA salary на over $60 000** (Johnson & Hall, 2018, abstract; full PDF за paywall T&F, текст реконструирован по abstract — verify перед финальной cite). Это **direct counter-evidence** нашему H9 informative null в данных 2015–2024: если Johnson-Hall находят significant tax effect на NBA FA salaries в pre-2017-CBA period, а мы находим null в post-2017 period, нужно объяснить divergence. Возможные explanations включают: (а) sample composition (наш sample содержит rookie scale + extensions + supermax, где mobility ограничена by tier-rule; их sample — FA-only), (б) institutional break после CBA 2017 (designated extension существенно ограничивает mobility top players), (в) spec differences (ATR vs MTR). Детальный разбор — в Discussion §5.5.

В рамках NBA Hembre (2022) предлагает дополнительный theoretical channel для team-side эффекта: при unrestricted free agency игроки требуют compensating differential за state income tax burden, что снижает spending power команд в high-tax штатах. Hembre находит pooled effect across 4 major US leagues: 1pp увеличение state tax rate → −0.77 до −0.86 pp в team win percentage (Hembre, 2022, p. 1). Важное caveat: **NBA-specific coefficient в Hembre Table 3 статистически незначим** ($\hat{\beta}_{\text{NBA}} \in [-0.143, -0.069]$, SE > 1.1, Table 3, p. 20). То есть Hembre даёт *theoretical channel*, совместимый с anti-marketability finding для NBA, но не direct empirical confirmation; pooled effect доминируется NFL и MLB sub-samples.

Совокупно: Kleven + Alm + Johnson-Hall + Hembre дают сильное theoretical + cross-sport empirical evidence существования tax channel в spor labor markets. Наш H9 null в post-2017 NBA — informative deviation, требующая институциональной интерпретации (cap-binds, restricted mobility, off-court endorsement substitution).

Health и durability — наименее разработанный sub-stream в NBA литературе. Ближайший classical antecedent — Bodvarsson & Brastow (1998), которые впервые эмпирически показали, что NBA labor market rewards consistent performance: после контроля mean productivity, players с более консистентной игрой получают statistically significant premium (Bodvarsson & Brastow, 1998, pp. 145–160). Их consistency measure — game-to-game variance в performance metrics; наш durability measure — retrospective games_missed (отсутствие игры вообще). Концепты related но не identical: B&B измеряют statistical inconsistency, мы — availability inconsistency. Прямое quantitative тестирование retrospective games_missed как predictor subsequent salary в post-2011-CBA-эпохе peer-reviewed работами не проведено; наш H10 (β = −0.005/game, см. §4.8) — расширение B&B logic на duration dimension и одна из первых формальных оценок этого специфического эффекта.

International composition NBA — растущая часть литературы. [TBD: yang_lin_2012.md.] Yang & Lin (2012) тестируют salary discrimination по nationality в NBA, контролируя performance; их main finding — после контроля on-court performance no significant salary penalty для foreign-born players. Это обосновывает наше включение continent-dummies (INTL_BLOCK) как control в M1c_full без specific hypothesis о discrimination direction.

## 2.7 Research gap и место настоящей работы

Литература по экономике NBA salary развивалась в виде отдельных эмпирических работ, каждая из которых тестирует один или несколько channel в изоляции. Хотя индивидуальные mechanisms (Mincer-core, awards signaling, institutional layer, market-size effect, durability) хорошо understood по отдельности, **систематического количественного декомпозирования variance ln(salary) по тематическим блокам факторов с использованием axiom-justified метода attribution для NBA в post-2011-CBA эпохе не проводилось**. Существующие работы либо используют sequential R²-декомпозицию (которая, как мы демонстрируем в Главе 4 §4.9, сильно order-dependent — атрибуция блока Awards меняется в 33 раза между plan- и reverse-order), либо ограничиваются точечными coefficient estimates без attribution всей дисперсии.

Методологический gap — недостаточное применение order-independent decomposition methods (Shapley R², Lipovetsky & Conklin, 2001) в NBA salary литературе. Эти методы — стандарт в machine learning interpretability и нескольких labor economics applications, но в спорт-экономике практически не используются.

Содержательный gap — недостаточное quantification разлинамики между continuous performance-pricing (Mincer-core) и discrete institutional categorization (CBA tier structure). Без этого не возможен принципиальный ответ на вопрос: NBA-salary — это «правда» функция от продуктивности с small cap-bound noise, или это «правда» institutional categorization с performance в качестве determinant категории? Наш H3 — первый формальный test этой dichotomy.

Третий gap — adequate treatment of anti-marketability в современной NBA. После пионерской работы Hembre (2022), которая даёт pooled-sport theoretical channel но не precise NBA estimate, нет систематического NBA-specific тестирования market-size effects с контролем wild-cluster bootstrap inference для heterogeneity-проверки.

Настоящая работа закрывает все три gaps: (а) применяет Shapley R²-декомпозицию к 9 блокам факторов с axiom-verification (efficiency $\sum_i \phi_i = R^2$ с точностью $10^{-16}$); (б) формально quantified tier dummies vs Mincer-core contribution ($R^2_{tier-only} = 0.849$ vs $R^2_{M1c} = 0.651$); (в) тестирует market discount с wild-cluster bootstrap (1000 реплик) на heterogeneity по звёздности и nationality.

## 2.8 Эмпирические гипотезы (H1–H10)

На основе обзора в §2.2–2.6 формулируются 10 эмпирических гипотез, организованных по пяти streams. Каждая гипотеза привязана к соответствующей литературе и тестируется в Главе 4.

**Stream 1 (Productivity / Mincer):**
- **H1:** Performance metrics (PPG, WS, BPM, VORP) положительно коррелируют с ln(salary) в pooled и year-FE спецификациях. (Mincer, 1974 [TBD]; Rosen, 1981; Hausman & Leonard, 1997)
- **H2:** Возрастной профиль ln(salary) имеет inverted-U shape с peak около 28–30 лет. (Rosen, 1981; Krautmann, 1999 [TBD])

**Stream 2 (Institutional / CBA):**
- **H3:** Tier dummies (8 категорий contracts от minimum до supermax) одни объясняют доминирующую долю variance ln(salary), большую чем full Mincer-спецификация. (Coon, n.d.; Hill & Groothuis, 2001 [TBD]; Rosen, 1986 [TBD])
- **H4:** CBA 2017 (Designated Veteran Extension) создаёт структурный break — post-2017 рост ln(salary) в верхнем хвосте. (Coon, n.d. Q24)

**Stream 3 (Awards / signaling):**
- **H5:** All-NBA selection в предыдущем сезоне (all_nba_lag1) повышает текущую ln(salary) через signaling и institutional eligibility (supermax). (Hölmström, 1979; Lazear & Rosen, 1981; Hausman & Leonard, 1997; Coon, n.d. Q24)
- **H6:** Эффект All-NBA на salary проявляется с 2–3-летним лагом через contract renewal cycle (event study τ = +2, +3). (Stiroh, 2007 [TBD]; Lazear & Rosen, 1981)

**Stream 4 (Market / team context):**
- **H7:** Top-5 market teams (LAL, LAC, NYK, BRK, CHI, GSW) платят premium игрокам через marketability channel. (Rosen, 1981; Hembre, 2022 — anti-direction prediction with NBA caveat)
- **H8:** Team success (win_pct_lag1, made_playoffs_lag1, over_luxury_tax_t) положительно влияет на individual ln(salary). (Berri, Brook & Schmidt, 2007 [TBD]; Kahn, 2000 [TBD])

**Stream 5 (Externalities / health):**
- **H9:** State income tax влияет на pre-tax ln(salary) через compensating differential. (Kleven, Landais & Saez, 2013; Alm, Kaempfer & Sennoga, 2012; Johnson & Hall, 2018; Hembre, 2022)
- **H10:** Durability (games_missed_lag1) отрицательно влияет на ln(salary). (новая гипотеза для NBA; контекстный antecedent — Bodvarsson & Brastow, 1998)

Тестирование гипотез описано в Главе 3 (методология) и представлено в Главе 4 (результаты).

---

[Слов в главе: ≈ 2 400; TBD-маркеров: 14 — все ждут заполнения шаблонов от Claude-A в batch-2/3; commit + push после получения батчей.]
