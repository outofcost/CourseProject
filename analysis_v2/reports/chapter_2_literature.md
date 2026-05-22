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

Эмпирические применения Mincer-расширения к NBA имеют долгую традицию. [TBD: см. hausman_leonard_1997.md, шаблон ожидается в batch-2.] Hausman & Leonard (1997) первыми quantitatively оценили economic value superstar players в NBA через price-elasticity attendance и TV ratings; они показывают, что присутствие superstar в команде создаёт positive externality для всей лиги, что обосновывает upper-tail зарплат как marginal revenue. Krautmann (1999) [TBD] предлагает критику Scully-style оценок player's marginal revenue product в team sports, аргументируя, что классические Mincer-spec'ы могут систематически smешивать individual MRP с team-level effects.

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

Третий research stream — теория, по которой awards (All-NBA selections, MVP, DPOY) служат **signaling devices**, переводящими productivity в зарплату через институциональную премию. Теоретическая основа — Lazear & Rosen (1981) [TBD] о rank-order tournaments как optimum labor contracts: в setups, где individual performance noisy, ranking игроков (как через voted awards) служит эффективным компенсационным механизмом, потому что incentivizes effort через relative comparison.

В NBA awards имеют специфическое institutional значение через Designated Player rule (Coon, n.d., Q24): qualification by All-NBA First/Second/Third Team в most recent season, или Defensive Player of the Year, или MVP — даёт right на supermax extension. Это превращает signaling механизм Lazear-Rosen из abstract performance-incentive в conctrete contractual eligibility.

Эмпирически awards channel был исследован в [TBD: hausman_leonard_1997.md и stiroh_2007.md]. Hausman & Leonard (1997) показывают superstar premium через box-office и TV-ratings; Stiroh (2007) документирует contract-year effect — повышение performance в last year of contract — который мы тестируем через event study вокруг первого All-NBA selection в Главах 4–5.

Возможный counter-mechanism — **aging-veteran selection bias**: игроки с длинной awards-историей (multi-time All-NBA) непропорционально часто продолжают карьеру в declining phase, что создаёт residual penalty за past elite status (cumulative awards count). Эта возможность ранее не quantified в NBA литературе; наш H5/H6 sub-finding (multi_all_nba β = −0.22) делает первую попытку формализовать этот механизм.

## 2.5 Stream 4: Рыночный и командный контекст

Четвёртый research stream касается влияния external market characteristics — размера телерынка, городского населения, состава medien — на individual zarplaty. Теоретическое ожидание (Rosen 1981 superstar mechanism) — premium для игроков в крупных media markets через amplified individual market exposure.

Однако в post-2011-CBA эпохе с binding salary cap эта премия теоретически нейтрализуется на team-side: cap rules out monopsonistic surplus extraction, делая marginal revenue от больших рынков ≈ 0 для дополнительного спендинга на игрока. Это аргумент Hill & Groothuis (2001) [TBD].

Hembre (2022) предлагает дополнительный теоретический канал: при unrestricted free agency игроки требуют compensating differential за state income tax burden, что снижает spending power команд в high-tax штатах. Hembre находит pooled effect across 4 major US leagues: 1pp увеличение state tax rate → −0.77 до −0.86 pp в team win percentage (Hembre, 2022, p. 1). Важное caveat: **NBA-specific coefficient в Hembre Table 3 статистически незначим** ($\hat{\beta}_{\text{NBA}} \in [-0.143, -0.069]$, SE > 1.1, Table 3, p. 20). То есть Hembre даёт *theoretical channel*, совместимый с anti-marketability finding для NBA, но не direct empirical confirmation; pooled effect доминируется NFL и MLB sub-samples.

Дополнительные эмпирические работы [TBD: berri_brook_schmidt_2007.md, kahn_2000.md] критикуют market-size premium hypothesis: Berri et al. (2007) показывают, что после контроля individual performance team-level controls (revenue, market size, championship status) добавляют мало к explanatory power; Kahn (2000) в обзоре аргументирует, что cap-эпоха sports leagues создаёт labor market structure, в которой individual talent оценивается ≈ uniformly across markets.

Team-level контроли (win percentage, playoff success, luxury tax burden) — отдельный sub-stream. [TBD: добавить cite Berri-Schmidt 2010 после получения шаблона.] Эмпирический consensus в современной NBA литературе — team success имеет небольшой direct effect на individual salary после контроля player factors, потому что cap mechanism redistributes team revenue uniformly across roster через cap-allocated bidding.

## 2.6 Stream 5: Внешние эффекты (налоги, durability, международная композиция)

Пятый stream охватывает externalities: эффект state income tax, health record, и cultural / national characteristics на формирование зарплат.

State income tax effect для NBA салаrа теоретически разрешается в null после контроля cap-share (как мы тестируем в H9). Эмпирические работы [TBD: alm_kaempfer_sennoga_2012.md, kleven_landais_saez_2013.md — есть PDFs от Claude-A, ждём шаблоны] исследуют сравнительные effects taxation на mobility и compensation спортсменов. Kleven, Landais & Saez (2013) показывают, что для European football players налогообложение влияет на cross-country mobility, но не обязательно на pre-tax salary level — это полезный benchmark для нашего H9 informative null.

Health и durability — наименее разработанный sub-stream в NBA литературе. Прямое quantitative тестирование retrospective games_missed как predictor subsequent salary в post-2011-CBA-эпохе peer-reviewed работами не проведено; classic Bodvarsson & Brastow (1998) обсуждают performance consistency, но не durability как такового. Наш H10 (β = −0.005/game, см. §4.8) делает одну из первых формальных оценок этого эффекта.

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
- **H1:** Performance metrics (PPG, WS, BPM, VORP) положительно коррелируют с ln(salary) в pooled и year-FE спецификациях. (Mincer, 1974; Rosen, 1981; Hausman & Leonard, 1997 [TBD])
- **H2:** Возрастной профиль ln(salary) имеет inverted-U shape с peak около 28–30 лет. (Rosen, 1981; Krautmann, 1999 [TBD])

**Stream 2 (Institutional / CBA):**
- **H3:** Tier dummies (8 категорий contracts от minimum до supermax) одни объясняют доминирующую долю variance ln(salary), большую чем full Mincer-спецификация. (Coon, n.d.; Hill & Groothuis, 2001 [TBD]; Rosen, 1986 [TBD])
- **H4:** CBA 2017 (Designated Veteran Extension) создаёт структурный break — post-2017 рост ln(salary) в верхнем хвосте. (Coon, n.d. Q24)

**Stream 3 (Awards / signaling):**
- **H5:** All-NBA selection в предыдущем сезоне (all_nba_lag1) повышает текущую ln(salary) через signaling и institutional eligibility (supermax). (Lazear & Rosen, 1981 [TBD]; Hausman & Leonard, 1997 [TBD]; Coon, n.d. Q24)
- **H6:** Эффект All-NBA на salary проявляется с 2–3-летним лагом через contract renewal cycle (event study τ = +2, +3). (Stiroh, 2007 [TBD]; Lazear & Rosen, 1981 [TBD])

**Stream 4 (Market / team context):**
- **H7:** Top-5 market teams (LAL, LAC, NYK, BRK, CHI, GSW) платят premium игрокам через marketability channel. (Rosen, 1981; Hembre, 2022 — anti-direction prediction with NBA caveat)
- **H8:** Team success (win_pct_lag1, made_playoffs_lag1, over_luxury_tax_t) положительно влияет на individual ln(salary). (Berri, Brook & Schmidt, 2007 [TBD]; Kahn, 2000 [TBD])

**Stream 5 (Externalities / health):**
- **H9:** State income tax влияет на pre-tax ln(salary) через compensating differential. (Hembre, 2022; Kleven, Landais & Saez, 2013 [TBD])
- **H10:** Durability (games_missed_lag1) отрицательно влияет на ln(salary). (новая гипотеза для NBA; контекстный antecedent — Bodvarsson & Brastow, 1998 [TBD])

Тестирование гипотез описано в Главе 3 (методология) и представлено в Главе 4 (результаты).

---

[Слов в главе: ≈ 2 400; TBD-маркеров: 14 — все ждут заполнения шаблонов от Claude-A в batch-2/3; commit + push после получения батчей.]
