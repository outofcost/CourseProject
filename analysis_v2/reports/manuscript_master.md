---
title: "Эконометрический анализ факторов, определяющих зарплату игрока NBA в эпоху post-2011 CBA"
subtitle: "Курсовая работа 3 курса"
author: "Karolina303"
institute: "НИУ ВШЭ, факультет экономических наук, программа «Экономика»"
year: "2025/2026"
format: HSE term paper — Article (Empirical)
---

# Аннотация (HSE-формат: RU 250 + EN 250 слов)

## Русская версия

Работа эмпирически декомпозирует вариацию логарифма реальной зарплаты NBA-игрока на тематические блоки факторов в эпоху post-2011 CBA. Используется собранная автором панель 3 660 player-seasons (953 уникальных игрока × 9 сезонов 2015/16–2023/24) на основе Basketball-Reference и Hoopshype. Панель расширена семью новыми блоками: страна рождения (100% покрытие), история наград (All-NBA / MVP / DPOY лаги и cumulative counts), supermax-eligibility согласно CBA 2017, rule-based contract tier classifier (8 категорий), team season records, размер рынка (Nielsen DMA + MSA population), durability (games missed lag).

Эконометрика включает Mincer-расширения с year fixed effects и cluster-robust SE на player_id, tier-specific регрессии, event study вокруг первого All-NBA, **Shapley-декомпозицию R²** по 9 блокам (order-independent attribution), wild-cluster bootstrap, Oster δ-sensitivity, multiple-testing corrections (Bonferroni и BH-FDR).

Главный методологический результат — количественная иерархия факторов: Performance + Age = 65.5% объяснённой дисперсии; Awards = 12.2%; Demographics = 14.1%; Durability = 5.7%; Market + Team + Structural + International ≈ 2.4%. Из десяти гипотез (H1–H10) семь подтверждены при BH-FDR 5%. Salary cap создаёт near-deterministic institutional layer (tier dummies одни дают R² = 0.85), модулирующий performance-pricing через discrete category jumps. Премии за крупный рынок нет — обнаружен дисконт ≈10% (anti-marketability, направление согласуется с Hembre, 2022). Awards channel работает с 2-3-летней задержкой через contract renewal cycle. Multi-time All-NBA игроки в фазе decline несут residual penalty −22% — sub-finding survival bias.

**Ключевые слова:** NBA, panel data, Mincer regression, salary cap, contract tiers, Shapley decomposition, market size, awards channel, durability discount.

---

## English version

This paper empirically decomposes the variance of log real NBA player salary into thematic factor blocks under the post-2011 CBA. We use a self-scraped panel of 3,660 player-seasons (953 unique players × 9 seasons 2015/16–2023/24) from Basketball-Reference and Hoopshype, extended with seven new blocks: birth country (100% coverage), award history (All-NBA / MVP / DPOY lags and cumulative counts), supermax eligibility under the 2017 CBA, a rule-based contract tier classifier (8 categories), team season records, market size (Nielsen DMA + MSA population), and durability (games missed lag).

Estimation includes Mincer extensions with year fixed effects and cluster-robust SE on player_id, tier-specific regressions, an event study around first All-NBA selection, **Shapley R² decomposition** over 9 blocks (order-independent attribution), wild-cluster bootstrap, Oster δ-sensitivity, and multiple-testing corrections (Bonferroni and BH-FDR).

The headline methodological result is a quantitative factor hierarchy: Performance + Age = 65.5% of explained variance; Awards = 12.2%; Demographics = 14.1%; Durability = 5.7%; Market + Team + Structural + International ≈ 2.4%. Of ten hypotheses (H1–H10), seven survive BH-FDR at 5%. The salary cap creates a near-deterministic institutional layer (tier dummies alone yield R² = 0.85), modulating performance-pricing via discrete category jumps. There is no large-market premium — instead a ≈10% discount (anti-marketability, direction consistent with Hembre, 2022). The awards channel operates with a 2–3 year lag via the contract renewal cycle. Multi-time All-NBA players in decline carry a residual penalty of −22% — a survival-bias sub-finding.

**Keywords:** NBA, panel data, Mincer regression, salary cap, contract tiers, Shapley decomposition, market size, awards channel, durability discount.

---

# Глава 1. Введение


---

## 1.1 Актуальность темы

Профессиональные спортивные лиги представляют собой исключительно ценную лабораторию для исследования рынков труда. Уникальность этой среды состоит в трёх особенностях: (а) полная публичная наблюдаемость зарплат и трудовых контрактов, (б) количественные показатели производительности на уровне отдельного работника, доступные с высокой частотой, и (в) институциональные правила (collective bargaining agreements, salary caps, draft system), которые создают квази-эксперименты для тестирования теоретических предсказаний о labor markets. Эти преимущества аргументированы в обзорной работе Kahn (2000), где спортивная индустрия позиционируется как «лаборатория для labor economics» — место, где можно эмпирически проверять гипотезы о компенсации, дискриминации, тournaments, контрактных циклах и monopsony power, не сталкиваясь с типичными для observational data ограничениями (Kahn, 2000, p. 75).

Национальная баскетбольная ассоциация (NBA) занимает в этой лаборатории особое место по нескольким причинам. Во-первых, NBA характеризуется наиболее выраженным «superstar effect» среди крупных американских лиг: распределение зарплат сильно right-skewed, с верхушкой, концентрирующей непропорционально большую долю общего payroll. Это явление формально объяснено в классической работе Rosen (1981), где конвексность revenue function по talent ($R''(q) > 0$) при наличии joint-consumption technology даёт экстремальную асимметрию distribution вознаграждения: «A person who is twice as talented as another earns four times more money» (Rosen, 1981, p. 849). NBA-игроки, чьи матчи смотрят миллионы зрителей через TV-трансляции, представляют каноничный пример superstar-рынка.

Во-вторых, NBA операционализирована под детальную, периодически пересматриваемую коллективную трудовую структуру (CBA — Collective Bargaining Agreement). С 2011 года действовала CBA с salary cap, luxury tax и системой individual maximum contracts; в 2017 году эта структура была дополнена «Designated Veteran Extension» (известным как supermax), привязывающим highest salary tier к performance criteria (All-NBA / DPOY / MVP selections). В 2023 году CBA снова была пересмотрена с введением second apron. Эти институциональные изменения создают серию natural experiments для тестирования того, как формальные правила влияют на distribution вознаграждения.

В-третьих, NBA характеризуется высокой степенью globalization рынка талантов. По состоянию на сезон 2023/24 около 27% игроков лиги были родом не из США, представляя более 40 стран. Эта международная композиция меняет картину traditional Mincer-models, фокусирующихся на национальном рынке труда: now compensation determinants должны учитывать кроссграничный отбор талантов, разные human capital trajectories, и потенциальные эффекты cultural distance.

Сочетание этих трёх характеристик — публичная наблюдаемость, выраженный superstar-effect, плотная институциональная структура — делает NBA уникальным emprical setting для тестирования теорий формирования зарплат, проверка которых на типичных datasets затруднена (Hausman & Leonard, 1997; Berri & Schmidt, 2010).

## 1.2 Постановка проблемы и Research Question

Несмотря на исключительную привлекательность NBA для labor economics исследований и значительное накопление эмпирической литературы (Hausman & Leonard, 1997; Krautmann, 1999; Hill & Groothuis, 2001; Berri, Brook & Schmidt, 2007; Stiroh, 2007; Yang & Lin, 2012; Hembre, 2022), имеется три не до конца разрешённых вопроса в современной post-2011-CBA эпохе:

**Проблема 1: Количественная иерархия факторов.** Литература по NBA salary в основном тестирует отдельные гипотезы (effect of performance metric X, of award Y, of market size Z) в изолированных спецификациях. Что отсутствует — систематическая, axiomatically-justified декомпозиция variance зарплат по тематическим блокам факторов. Поэтому остаётся открытым вопрос: **какая доля variance ln(salary) объясняется performance, а какая — институциональной категоризацией, awards history, командным контекстом, рыночными условиями, durability?** Без такой декомпозиции невозможно ответственно ranked-prioritize факторы при policy analysis.

**Проблема 2: Влияние институциональной структуры (CBA) на distribution зарплат.** Hill & Groothuis (2001) утверждают, что salary cap создаёт «institutional layer» поверх traditional Mincer mechanism. Но прямой quantitative test — сколько variance объясняется одним только tier-категориями contract (8 уровней: minimum / rookie scale / mid-level / high-mid / max-25 / max-30 / max-35 / supermax), без participation performance-метрик — не проведён в существующей литературе. Это критический gap, потому что наличие near-deterministic institutional categorization меняет интерпретацию pricing функции NBA salary с continuous на discrete.

**Проблема 3: Marketability и off-court доход.** Классическая Rosen-mechanism предполагает, что игроки в больших медиа-рынках должны получать premium за counter-amplified market exposure. Но в современном NBA с salary cap эта премия должна быть нейтрализована (Hill & Groothuis, 2001). Эмпирические работы дают разнородные результаты: Hembre (2022), исследуя effect state tax на performance команд в pooled-cross-sport panel, находит negative effect, хотя NBA-specific coefficient в его Table 3 статистически незначим. Вопрос **направления и магнитуды market-size effect именно для NBA в post-2017-CBA эпоху** остаётся открытым.

Эти три проблемы складываются в формальный исследовательский вопрос:

> **RQ:** Какие факторы и в какой пропорции определяют логарифм реальной зарплаты NBA-игрока в период 2015/16–2023/24, и как post-2011-CBA institutional structure (salary cap, supermax, designated extension) модулирует традиционные detm formation механизмы (Mincer human capital, awards signaling, market context)?

Этот вопрос конкретизируется в 10 эмпирических гипотезах (H1–H10), формулировка которых даётся в конце Главы 2 после литературного обзора по 5 research streams.

## 1.3 Цель и задачи

**Цель работы** — количественно декомпозировать variance ln(salary) NBA-игрока на блоки факторов с использованием axiom-justified метода attribution и протестировать набор гипотез о механизмах формирования зарплаты в современной CBA-эпохе.

**Задачи:**
1. Собрать панельный dataset, охватывающий все игровые и контрактные характеристики игроков NBA за 9 сезонов (2015/16–2023/24), включая 7 новых блоков данных (birth country, awards history, supermax eligibility, contract tier, team season records, market size, durability), не использованных в предыдущих эмпирических работах одной общей панелью.
2. Расширить классическое Mincer-расширение earnings function для professional basketball, контролируя year fixed effects и cluster-robust standard errors (Cameron, Gelbach & Miller, 2011) на уровне игрока.
3. Применить Shapley R²-декомпозицию (Lipovetsky & Conklin, 2001) для axiom-justified attribution variance по 9 тематическим блокам.
4. Тестировать 10 гипотез о механизмах формирования зарплаты с контролем multiple testing через Bonferroni и Benjamini-Hochberg FDR.
5. Обеспечить полную воспроизводимость через регресс-тест с предыдущей итерацией проекта (max coef diff < 5 × 10⁻⁵), hash-snapshots датасета, и публичный репозиторий с открытым исходным кодом.

## 1.4 Научная новизна и contribution

Работа делает следующие contribution к существующей литературе по NBA salary economics:

**Методологический contribution:** Впервые в NBA-salary литературе применяется Shapley R²-декомпозиция (Lipovetsky & Conklin, 2001) для attribution variance по тематическим блокам факторов. В отличие от широко используемой sequential R²-декомпозиции, которая зависит от order включения регрессоров (мы демонстрируем, что атрибуция блока Awards меняется в 33 раза между plan-order и reverse-order в наших данных), Shapley-аллокация удовлетворяет четырём аксиомам — эффективности, симметрии, dummy и аддитивности — и поэтому даёт единственное «справедливое» распределение объяснённой дисперсии. Это даёт NBA-исследованию первый количественный, теоретически обоснованный ответ на вопрос о доле каждого фактора.

**Содержательный contribution 1: Институциональный слой.** Демонстрируется, что tier-категории contract (8 классов от minimum до supermax) объясняют 84.9% variance ln(salary) сами по себе — больше, чем full Mincer-спецификация с 37 регрессорами. Это эмпирически устанавливает, что NBA-salary в современной CBA-эпохе формируется не через continuous performance pricing, а через discrete institutional jumps, что является нетривиальным extension классической Rosen (1986) cap-induced concavity на step-function structure.

**Содержательный contribution 2: Anti-marketability и delayed awards channel.** Документируется два уточнения классических механизмов: (а) в top-5 NBA markets обнаруживается not premium а discount −9.3% (p = 0.022), что согласуется с theoretical channel Hembre (2022) — tax compensating differential under free agency — но не идентифицируется direct'ом в существующих данных; (б) effect All-NBA selection на зарплату проявляется через 2-3-летний lag (event study τ=+2: +21%, τ=+3: +22%), что подтверждает contract renewal cycle mechanism, ранее теоретически обсуждавшийся в Stiroh (2007) но не quantified для NBA в post-2011 эпохе.

**Содержательный contribution 3: Durability как price effect.** Впервые в NBA-литературе показано, что games_missed_lag1 является самостоятельным price discount factor (β = −0.005/game, p < 0.001; Shapley-share 5.7%), независимым от performance-метрик. Это устанавливает, что рынок NBA прайсит риск травм через retrospective health record, а не только через current performance.

**Воспроизводимость:** Полный исходный код, сырые данные, тесты воспроизводимости (max coef diff с предыдущей версией < 5 × 10⁻⁵), hash-snapshots датасета размещены в публичном репозитории `https://github.com/outofcost/CourseProject` под MIT-лицензией. Это делает работу одной из первых полностью открытых эмпирических работ по NBA salary economics с воспроизводимым пайплайном от scraping до figure generation.

## 1.5 Структура работы

Работа структурирована согласно HSE term paper guideline для Article (Empirical) format:

- **Глава 1.** Введение (текущая глава) — мотивация, постановка проблемы, RQ, цель, contribution preview.
- **Глава 2.** Литературный обзор — критический обзор пяти research streams (Mincer / productivity, Institutional / CBA, Awards / signaling, Market / team context, Externalities / health) с формулировкой 10 эмпирических гипотез в конце.
- **Глава 3.** Данные и методология — описание источников данных, выборки, переменных, эконометрических спецификаций и Shapley R²-декомпозиции.
- **Глава 4.** Результаты — эмпирические результаты по каждой гипотезе, главный finding (Shapley-декомпозиция), и multiple testing summary.
- **Глава 5.** Обсуждение — интерпретация результатов в контексте существующей литературы, методологические caveats, ограничения.
- **Глава 6.** Заключение — суммирование основных выводов (сгруппированных в 4 содержательных кластера), методологический contribution, ограничения и направления для будущих исследований.
- **AI Disclosure** — декларация использования AI-инструментов, верификации и intellectual responsibility (по HSE guideline §1.3).
- **Список литературы** — APA-format, около 25 источников.
- **Приложения** — расширенные таблицы регрессий, описательная статистика, hash-snapshots.

---


---

# Глава 2. Литературный обзор

> Литературный обзор организован по пяти research streams; в конце главы формулируются 10 эмпирических гипотез (H1–H10) с привязкой к streams и литературе.
> Маркеры `[TBD: см. {author_year}]` помечают cite'ы, которые требуют верификации по шаблонам из `bibliography/sources/` (некоторые ещё не пришли от Claude-A — это будет дополнено в следующей итерации).

---

## 2.1 Подход к литературному обзору

Литература по экономике NBA salary располагается на пересечении пяти содержательных областей: (а) классической labor economics в её Mincer-tradition, (б) теории institutional design коллективных трудовых соглашений, (в) теории signaling и tournaments, (г) теории формирования team-side рыночной премии, (д) теории внешних эффектов (налоги, регуляция, кадровое здоровье). Эта глава следует данной структуре, обозначая ключевые работы в каждой области и формулируя 10 эмпирических гипотез, тестируемых в Главах 3–4.

## 2.2 Stream 1: Производительность и Mincer-формирование зарплат

Основу теоретической рамки нашего исследования составляет Mincer earnings function в её классической форме (Mincer, 1974), согласно которой $\ln(\text{salary}) = f(\text{schooling}, \text{experience})$ с возможным расширением через performance / productivity covariates. В контексте профессионального спорта natural extension этой функции — включение игровых статистик (points per game, assists, rebounds, advanced metrics) как proxy для productivity.

Классическая формальная база для понимания high-tail зарплат в NBA — superstar theory Rosen (1981). Rosen показывает, что при наличии **joint-consumption technology** (один продавец одновременно обслуживает много покупателей — TV-трансляция матча миллионам зрителей) и slight differences in talent, revenue function $R(q)$ становится convex по talent $q$, что даёт экстремальную асимметрию distribution вознаграждения: "There is concentration of output among a few individuals, marked skewness in the associated distributions of income and very large rewards at the top" (Rosen, 1981, p. 845). Формальное следствие при квадратичной cost function — "A person who is twice as talented as another earns four times more money" (Rosen, 1981, p. 849). NBA удовлетворяет двум common elements, которые Rosen отождествляет с superstar markets (p. 845): (а) close connection between personal reward and market size, (б) market size + reward gravitate towards higher-talent individuals.

Эмпирические применения Mincer-расширения к NBA имеют долгую традицию. Hausman & Leonard (1997) первыми quantitatively оценили economic value superstar players в NBA через attendance и TV ratings, документируя что «в дополнение к эффекту, который superstars оказывают на свои команды, они производят tremendous positive externality на other teams» (Hausman & Leonard, 1997, p. 9). Авторы оценивают, что Michael Jordan один поднял Bulls gate revenue на $8.6M в его дебютный сезон (Hausman & Leonard, 1997, p. 18), а Bird увеличил Celtics home attendance на ~50% (p. 17). Совокупный cross-team externality value Jordan'а — порядка $53M/год через TV ratings, road-game attendance и paraphernalia (Section V), что обосновывает upper-tail зарплат как marginal revenue, включая cross-team spillovers. Krautmann (1999) предлагает критику Scully-style оценок player's marginal revenue product в team sports, аргументируя, что классические Mincer-spec'ы могут систематически смешивать individual MRP с team-level effects.

Hill & Groothuis (2001) анализируют structural effects NBA CBA на distribution зарплат, показывая, что 1995 CBA с её salary cap и max contracts перевела часть salary growth из тонкого хвоста в средний tier. Это положило основу для последующей литературы об институциональном слое.

В современной post-2011-CBA эпохе появились исследования, которые включают расширенные advanced metrics (PER, Win Shares, BPM, VORP) в Mincer-spec'ы. Berri, Brook & Schmidt (2007) формально критикуют naïve performance-Mincer спецификации, аргументируя, что отдельные scoring metrics (PPG) систематически переоценивают свой эффект на salary за счёт корреляции с usage rate; они motivate inclusion advanced metrics типа Win Shares.

Возрастной профиль salary классически имеет inverted-U shape с peak около 28-30 лет — это эмпирический фактор, последовательно подтверждаемый в литературе для most professional team sports. В нашей текущей оценке (v2) peak age = 29.5 лет (95% CI [28.4, 30.6]) согласуется с этой литературой и с оценкой v1 (30.6 лет).

## 2.3 Stream 2: Институциональная структура (CBA, salary cap)

Второй research stream фокусируется на эффекте institutional rules — salary cap, luxury tax, максимальная зарплата, дизайн extension contracts — на distribution зарплат. NBA отличается от других major leagues наиболее детальной структурой institutional caps, формализованной в серии CBAs (1995, 1999, 2005, 2011, 2017, 2023).

Каноническим практическим reference для деталей CBA является Coon (n.d.) FAQ — детальный практикоориентированный справочник, формализующий все правила соглашения. Согласно Coon (n.d., Q23), maximum salary structure разделена на три tiers по выслуге: 25% of cap (0–6 years), 30% (7–9 years), 35% (10+ years). Designated Player rule (Q24) дополнительно создаёт «supermax» eligibility для игроков, которые удовлетворяют performance criteria (All-NBA / DPOY / MVP selections). Это создаёт **discrete institutional layer** поверх Mincer continuous pricing.

Теоретическая литература о cap-induced concavity начинается с Rosen (1986), который показывает, что binding cap создаёт concave reward function для top-tier игроков. Этот мecanism теоретически предсказывает, что $\beta_{\text{performance}}$ in cap-bound tiers должна быть ниже, чем в free-market tiers — что мы эмпирически тестируем через tier-specific Mincer regressions (Глава 4 §4.3).

Прямого quantitative анализа supermax-extension (введённой CBA 2017) в peer-reviewed литературе на момент написания работы обнаружено не было; институциональные детали Designated Veteran Extension доступны через Coon (n.d., Q24) как practitioner-reference, а количественный analysis эффекта supermax на team performance и player retention остаётся открытым gap, частично закрываемым настоящей работой через tier-classifier и H3-test.

Берри, Brook & Schmidt (2010) и более раннее Berri (1999) доказывают, что традиционные performance-based pay model недооценивают role institutional channelling: игроки с high observable stats но без awards selections могут systematically underprice'ить себя по сравнению с awards-elevated players в той же performance bucket.

## 2.4 Stream 3: Awards channel и signaling

Третий research stream — теория, по которой awards (All-NBA selections, MVP, DPOY) служат **signaling devices**, переводящими productivity в зарплату через институциональную премию. Теоретическая основа простирается на два уровня. На уровне fundamental incentive design — Hölmström (1979) формализует **informativeness principle**: «A signal is valuable if and only if it is informative» (Hölmström, 1979, p. 84, Proposition 3); любая дополнительная информация о действии агента может улучшить optimal contract. Это даёт теоретическое обоснование для inclusion множественных performance signals (PPG, WS, BPM, awards) в Mincer-spec'ах — каждая переменная улавливает свою dimension informativeness, а не дублирует другие.

На втором уровне — Lazear & Rosen (1981) разрабатывают rank-order tournament theory: они показывают, что compensation, основанная на относительном ранге, может implementовать тот же эффективный allocation эффорта, что и piece-rate compensation, при risk-neutral workers (Proposition 1, Section II.B, p. 7). Ключевая интуиция: «differences in the level of output between individuals may be quite small, yet optimal 'prizes' are selected in a way that induces workers to allocate their effort and investment activities efficiently» (Lazear & Rosen, 1981, p. 2). В NBA это формализуется в Designated Player rule (Coon, n.d., Q24): qualification by All-NBA First/Second/Third Team в most recent season, или Defensive Player of the Year, или MVP — даёт right на supermax extension. Это превращает signaling механизм Lazear-Rosen из abstract performance-incentive в concrete contractual eligibility — discrete prize в multi-stage tournament (15 All-NBA → 5 First Team → 1 MVP).

Эмпирически awards channel в NBA исследован в Hausman & Leonard (1997) (см. §2.2) и Stiroh (2007). Stiroh документирует contract-year effect — повышение performance в last year of contract — который мы тестируем через event study вокруг первого All-NBA selection в Главах 4–5.

Возможный counter-mechanism — **aging-veteran selection bias**: игроки с длинной awards-историей (multi-time All-NBA) непропорционально часто продолжают карьеру в declining phase, что создаёт residual penalty за past elite status (cumulative awards count). Эта возможность ранее не quantified в NBA литературе; наш H5/H6 sub-finding (multi_all_nba β = −0.22) делает первую попытку формализовать этот механизм.

## 2.5 Stream 4: Рыночный и командный контекст

Четвёртый research stream касается влияния external market characteristics — размера телерынка, городского населения, состава medien — на individual zarplaty. Теоретическое ожидание (Rosen 1981 superstar mechanism) — premium для игроков в крупных media markets через amplified individual market exposure.

Однако в post-2011-CBA эпохе с binding salary cap эта премия теоретически нейтрализуется на team-side: cap rules out monopsonistic surplus extraction, делая marginal revenue от больших рынков ≈ 0 для дополнительного спендинга на игрока. Это аргумент Hill & Groothuis (2001).

Hembre (2022) предлагает дополнительный теоретический канал: при unrestricted free agency игроки требуют compensating differential за state income tax burden, что снижает spending power команд в high-tax штатах. Hembre находит pooled effect across 4 major US leagues: 1pp увеличение state tax rate → −0.77 до −0.86 pp в team win percentage (Hembre, 2022, p. 1). Важное caveat: **NBA-specific coefficient в Hembre Table 3 статистически незначим** ($\hat{\beta}_{\text{NBA}} \in [-0.143, -0.069]$, SE > 1.1, Table 3, p. 20). То есть Hembre даёт *theoretical channel*, совместимый с anti-marketability finding для NBA, но не direct empirical confirmation; pooled effect доминируется NFL и MLB sub-samples.

Дополнительные эмпирические работы критикуют market-size premium hypothesis: Berri et al. (2007) показывают, что после контроля individual performance team-level controls (revenue, market size, championship status) добавляют мало к explanatory power; Kahn (2000) в обзоре аргументирует, что cap-эпоха sports leagues создаёт labor market structure, в которой individual talent оценивается ≈ uniformly across markets.

Team-level контроли (win percentage, playoff success, luxury tax burden) — отдельный sub-stream. Эмпирический consensus в современной NBA литературе — team success имеет небольшой direct effect на individual salary после контроля player factors, потому что cap mechanism redistributes team revenue uniformly across roster через cap-allocated bidding.

## 2.6 Stream 5: Внешние эффекты (налоги, durability, международная композиция)

Пятый stream охватывает externalities: эффект state income tax, health record, и cultural / national characteristics на формирование зарплат.

State income tax effect в spor labor markets теоретически и эмпирически документирован тремя ключевыми работами. Kleven, Landais & Saez (2013) на panel 14 западноевропейских футбольных лиг за 1985–2008 (47,727 player-year observations) находят, что elasticity of foreign players w.r.t. net-of-tax rate ≈ 1.0 — игроки сильно реагируют на tax-induced compensating differentials, когда mobility не ограничена: «the elasticity of the number of foreign players with respect to the net-of-tax rate for foreigners we estimate is around one» (Kleven et al., 2013, p. 1894). Для domestic players elasticity составляет лишь 0.15 — sample fragility выше для locally-rooted игроков. Это foundational evidence того, что tax channel реален у superstar workers в spor labor markets.

Прямой US pro-sport empirical аналог — Alm, Kaempfer & Sennoga (2012) для MLB: на 372 free agents за 1995–2001 они находят, что 1pp увеличение state+local tax rate повышает pre-tax FA salary на $21–24 тыс. (Alm et al., 2012, Table 3, p. 11), что эквивалентно elasticity 0.5–0.66 в log-log spec. Authors интерпретируют это как evidence того, что «income taxes are largely shifted away from mobile players to other factors, such as the franchise itself» (Alm et al., 2012, p. 13). Mechanism — compensating differential через free agency.

Промежуточный NBA-specific empirical step — Kopkin (2012), который тестирует, влияют ли state-level income tax rates на decisions NBA free agents о club destination в сезонах 2001/02 – 2007/08. Kopkin предлагает важное theoretical уточнение для NBA: tax effect реализуется через **quality sorting** (команды в low-tax штатах непропорционально часто signing top-quality FAs), а не через salary level differentiation. Mechanism — players value after-tax income; при условиях binding salary cap (max contract ограничивает nominal pre-tax salary), adjustment margin переходит с salary level на destination choice. Это даёт альтернативное объяснение, почему MLB-style salary-compensation effect (Alm et al., 2012) может не реализоваться в NBA, при том что tax channel сам по себе активен.

Прямой NBA-specific тест на individual salary level приходится на Johnson & Hall (2018) — paper, ближайший по setup к нашему: на 576 NBA free agent signings за 2010–2014 они находят, что **1pp increase в average tax rate повышает FA salary на over $60 000** (Johnson & Hall, 2018, abstract; full PDF за paywall T&F, текст реконструирован по abstract — verify перед финальной cite). Это **direct counter-evidence** нашему H9 informative null в данных 2015–2024: если Johnson-Hall находят significant tax effect на NBA FA salaries в pre-2017-CBA period, а мы находим null в post-2017 period, нужно объяснить divergence. Возможные explanations включают: (а) sample composition (наш sample содержит rookie scale + extensions + supermax, где mobility ограничена by tier-rule; их sample — FA-only), (б) institutional break после CBA 2017 (designated extension существенно ограничивает mobility top players), (в) spec differences (ATR vs MTR). Детальный разбор — в Discussion §5.5.

В рамках NBA Hembre (2022) предлагает дополнительный theoretical channel для team-side эффекта: при unrestricted free agency игроки требуют compensating differential за state income tax burden, что снижает spending power команд в high-tax штатах. Hembre находит pooled effect across 4 major US leagues: 1pp увеличение state tax rate → −0.77 до −0.86 pp в team win percentage (Hembre, 2022, p. 1). Важное caveat: **NBA-specific coefficient в Hembre Table 3 статистически незначим** ($\hat{\beta}_{\text{NBA}} \in [-0.143, -0.069]$, SE > 1.1, Table 3, p. 20). То есть Hembre даёт *theoretical channel*, совместимый с anti-marketability finding для NBA, но не direct empirical confirmation; pooled effect доминируется NFL и MLB sub-samples.

Совокупно: Kleven + Alm + Johnson-Hall + Hembre дают сильное theoretical + cross-sport empirical evidence существования tax channel в spor labor markets. Наш H9 null в post-2017 NBA — informative deviation, требующая институциональной интерпретации (cap-binds, restricted mobility, off-court endorsement substitution).

Health и durability — наименее разработанный sub-stream в NBA литературе. Ближайший classical antecedent — Bodvarsson & Brastow (1998), которые впервые эмпирически показали, что NBA labor market rewards consistent performance: после контроля mean productivity, players с более консистентной игрой получают statistically significant premium (Bodvarsson & Brastow, 1998, pp. 145–160). Их consistency measure — game-to-game variance в performance metrics; наш durability measure — retrospective games_missed (отсутствие игры вообще). Концепты related но не identical: B&B измеряют statistical inconsistency, мы — availability inconsistency. Прямое quantitative тестирование retrospective games_missed как predictor subsequent salary в post-2011-CBA-эпохе peer-reviewed работами не проведено; наш H10 (β = −0.005/game, см. §4.8) — расширение B&B logic на duration dimension и одна из первых формальных оценок этого специфического эффекта.

International composition NBA — растущая часть литературы. Yang & Lin (2012) тестируют salary discrimination по nationality в NBA, контролируя performance; их main finding — после контроля on-court performance no significant salary penalty для foreign-born players. Это обосновывает наше включение continent-dummies (INTL_BLOCK) как control в M1c_full без specific hypothesis о discrimination direction.

## 2.7 Research gap и место настоящей работы

Литература по экономике NBA salary развивалась в виде отдельных эмпирических работ, каждая из которых тестирует один или несколько channel в изоляции. Хотя индивидуальные mechanisms (Mincer-core, awards signaling, institutional layer, market-size effect, durability) хорошо understood по отдельности, **систематического количественного декомпозирования variance ln(salary) по тематическим блокам факторов с использованием axiom-justified метода attribution для NBA в post-2011-CBA эпохе не проводилось**. Существующие работы либо используют sequential R²-декомпозицию (которая, как мы демонстрируем в Главе 4 §4.9, сильно order-dependent — атрибуция блока Awards меняется в 33 раза между plan- и reverse-order), либо ограничиваются точечными coefficient estimates без attribution всей дисперсии.

Методологический gap — недостаточное применение order-independent decomposition methods (Shapley R², Lipovetsky & Conklin, 2001) в NBA salary литературе. Эти методы — стандарт в machine learning interpretability и нескольких labor economics applications, но в спорт-экономике практически не используются.

Содержательный gap — недостаточное quantification разлинамики между continuous performance-pricing (Mincer-core) и discrete institutional categorization (CBA tier structure). Без этого не возможен принципиальный ответ на вопрос: NBA-salary — это «правда» функция от продуктивности с small cap-bound noise, или это «правда» institutional categorization с performance в качестве determinant категории? Наш H3 — первый формальный test этой dichotomy.

Третий gap — adequate treatment of anti-marketability в современной NBA. После пионерской работы Hembre (2022), которая даёт pooled-sport theoretical channel но не precise NBA estimate, нет систематического NBA-specific тестирования market-size effects с контролем wild-cluster bootstrap inference для heterogeneity-проверки.

Настоящая работа закрывает все три gaps: (а) применяет Shapley R²-декомпозицию к 9 блокам факторов с axiom-verification (efficiency $\sum_i \phi_i = R^2$ с точностью $10^{-16}$); (б) формально quantified tier dummies vs Mincer-core contribution ($R^2_{tier-only} = 0.849$ vs $R^2_{M1c} = 0.651$); (в) тестирует market discount с wild-cluster bootstrap (1000 реплик) на heterogeneity по звёздности и nationality.

## 2.8 Эмпирические гипотезы (H1–H10)

На основе обзора в §2.2–2.6 формулируются 10 эмпирических гипотез, организованных по пяти streams. Каждая гипотеза привязана к соответствующей литературе и тестируется в Главе 4.

**Stream 1 (Productivity / Mincer):**
- **H1:** Performance metrics (PPG, WS, BPM, VORP) положительно коррелируют с ln(salary) в pooled и year-FE спецификациях. (Mincer, 1974; Rosen, 1981; Hausman & Leonard, 1997)
- **H2:** Возрастной профиль ln(salary) имеет inverted-U shape с peak около 28–30 лет. (Rosen, 1981; Krautmann, 1999)

**Stream 2 (Institutional / CBA):**
- **H3:** Tier dummies (8 категорий contracts от minimum до supermax) одни объясняют доминирующую долю variance ln(salary), большую чем full Mincer-спецификация. (Coon, n.d.; Hill & Groothuis, 2001; Rosen, 1986)
- **H4:** CBA 2017 (Designated Veteran Extension) создаёт структурный break — post-2017 рост ln(salary) в верхнем хвосте. (Coon, n.d. Q24)

**Stream 3 (Awards / signaling):**
- **H5:** All-NBA selection в предыдущем сезоне (all_nba_lag1) повышает текущую ln(salary) через signaling и institutional eligibility (supermax). (Hölmström, 1979; Lazear & Rosen, 1981; Hausman & Leonard, 1997; Coon, n.d. Q24)
- **H6:** Эффект All-NBA на salary проявляется с 2–3-летним лагом через contract renewal cycle (event study τ = +2, +3). (Stiroh, 2007; Lazear & Rosen, 1981)

**Stream 4 (Market / team context):**
- **H7:** Top-5 market teams (LAL, LAC, NYK, BRK, CHI, GSW) платят premium игрокам через marketability channel. (Rosen, 1981; Hembre, 2022 — anti-direction prediction with NBA caveat)
- **H8:** Team success (win_pct_lag1, made_playoffs_lag1, over_luxury_tax_t) положительно влияет на individual ln(salary). (Berri, Brook & Schmidt, 2007; Kahn, 2000)

**Stream 5 (Externalities / health):**
- **H9:** State income tax влияет на pre-tax ln(salary) через compensating differential. (Kleven, Landais & Saez, 2013; Alm, Kaempfer & Sennoga, 2012; Johnson & Hall, 2018; Hembre, 2022)
- **H10:** Durability (games_missed_lag1) отрицательно влияет на ln(salary). (новая гипотеза для NBA; контекстный antecedent — Bodvarsson & Brastow, 1998)

Тестирование гипотез описано в Главе 3 (методология) и представлено в Главе 4 (результаты).

---


---

# Глава 3. Данные и методология


---

## 3.1 Источники данных

Анализ опирается на собственноручно собранную панельную базу из четырёх типов источников.

**(1) Basketball-Reference (bbref).** Основной источник игровой статистики и метаданных. Скрапер написан на Python с использованием библиотеки `curl_cffi` для воспроизведения TLS-fingerprint реального браузера, что необходимо для обхода Cloudflare TLS-фильтрации на современных версиях сайта. Сбор охватывает страницы `per_game`, `advanced`, `awards/all_league`, `awards/all_defense`, `awards/mvp`, `awards/dpoy`, `teams/{abbr}/{year}`, `players/{letter}/{slug}.html` (для birth metadata).

**(2) Hoopshype salary database.** Источник исторических зарплат игроков. Текущая версия сайта недоступна без аутентификации, поэтому данные собраны через Wayback Machine (archive.org) с snapshot-датами в межсезонье каждого сезона.

**(3) Ручные таблицы.** Два CSV, составленные вручную из публичных открытых источников:
- `manual_market_size.csv` — размер рынка для 30 команд: Nielsen DMA rank (рейтинг телерынка) и MSA population (численность населения столичного округа) по US Census 2020 и StatCan для Торонто.
- `cba_thresholds.csv` — пороговые величины из Коллективного трудового соглашения (CBA): salary cap, luxury tax, mid-level exception, максимальная зарплата по категориям выслуги, минимальная зарплата по 9 сезонам. Источник — Coon's CBA FAQ (Coon, n. d.) и официальный bbref salary-cap-history.

**(4) Производные блоки.** Три CSV, рассчитанных программно из источников 1–3:
- `awards_features.csv` — лаги наград (`all_nba_lag1`, `mvp_lag1`, `dpoy_lag1`), кумулятивные счётчики (`career_all_nba_count`, `career_allstar_count`) и переменная supermax-eligibility согласно правилам CBA 2017 (Designated Veteran Extension).
- `durability_panel.csv` — лаги пропущенных матчей (`games_missed_lag1`, `games_missed_3y_cum`).
- `contract_tier.csv` — категория контракта (8 уровней от `rookie_scale` до `supermax`), приписываемая правило-ориентированным классификатором на основе зарплаты и CBA-порогов.

Все три скрапера и три derive-скрипта хранят промежуточные результаты в кэше `.cache/` для воспроизводимости; cold-cache пайплайн занимает ≈ 2 часа, warm-cache — ≈ 3 минуты. Hash-snapshot финального датасета зафиксирован в `analysis_v2/reports/v2_snapshot.sha256`.

## 3.2 Выборка и временной период

Финальная панель содержит **3 660 наблюдений (player-season)** по **953 уникальным игрокам** за 9 сезонов **2015/16–2023/24** и 153 переменных. Выбор периода обусловлен тремя соображениями:
1. Начало 2015/16 — это первый полный сезон в эпоху значительного роста salary cap, обусловленного телеконтрактом ESPN/Turner (2014); до этого структура зарплат NBA принципиально отличалась.
2. Период включает структурный break — CBA 2017 (вступило в силу 1 июля 2017 г.), что позволяет тестировать гипотезу о реакции зарплат на институциональные изменения (H4).
3. Период оканчивается на 2023/24 — последний сезон, для которого все источники Bbref/Hoopshype содержат финализированные данные на момент сбора (январь 2026 г.).

После применения фильтров, необходимых для основной спецификации (наличие лаговых переменных, valid awards history, валидное team-attribution), рабочая выборка сокращается до **2 268 наблюдений**. Потери распределяются так:
- 508 строк с pseudo-team `2TM/3TM/4TM/TOT` — игроки, поменявшие команду внутри сезона; для них team-level и market-level переменные неопределены. Эти строки сохраняются в датасете, но получают `NaN` в team/market-зависимых спецификациях.
- ≈ 880 строк сезона 2015/16 (нет лагов) и игроков-новичков (нет games_missed_lag1).

Решение оставить TOT-строки в датасете и обрабатывать их NaN-обработкой, а не удалять, обосновано стремлением сохранить максимальный sample для спецификаций без team-переменных (см. M1c_full ниже). Альтернатива — взвешенная импутация (доля игр в каждой команде × team-метрики) — была рассмотрена и отвергнута как расширяющая идентификационные предположения без статистически значимой пользы.

## 3.3 Зависимая переменная

Зависимая переменная во всех спецификациях — **натуральный логарифм реальной зарплаты** игрока в сезоне:

$$y_{i,t} = \ln(\text{salary}_{i,t} / \text{CPI}_{t})$$

где `salary` — номинальная зарплата в долларах США (без подоходного налога), а `CPI` — годовой индекс потребительских цен США (Federal Reserve, базисный год 2015). Логарифмическая спецификация обоснована: (а) сильной правосторонней асимметрией исходного распределения зарплат (медиана / среднее ≈ 0.42), (б) теоретическими соображениями о суперстарной структуре рынка (Rosen, 1981), которая порождает мультипликативные эффекты по факторам производительности, и (в) стандартом в литературе об экономике спорта (Hausman & Leonard, 1997; Krautmann, 1999; Kahn, 2000).

## 3.4 Независимые переменные

Независимые переменные сгруппированы в **9 тематических блоков**. Это деление будет использовано в R²-декомпозиции в §3.6.

**(1) Performance.** `ppg` (очки за игру), `rpg`, `apg`, `mpg`, `gp`, `vorp`, `bpm`, `usg_pct`, `ws`, `per`, `ts_pct`. Включён полный набор «traditional» и «advanced» статистик; редундантность контролируется через VIF (см. §3.8).

**(2) Age and experience.** `age`, `age^2` (для тестирования inverted-U профиля), `experience` (число сезонов в NBA до текущего, исправлено для undrafted игроков, см. §3.2 и приложение A.2).

**(3) Demographics.** `draft_pick` (номер выбора на драфте, NaN для undrafted), `undrafted` (дамми), `position` (5 категорий, дамми с PG как reference).

**(4) Continent dummies (international).** `born_canada`, `born_europe`, `born_latam`, `born_africa`, `born_asia_oceania`; США = reference. Производная переменная `is_international = Σ born_*` исключена из основной спецификации (perfect multicollinearity), используется только в альтернативной спецификации без continent dummies.

**(5) Market.** `top5_market` ∈ {NYK, BRK, LAL, LAC, CHI, GSW} (фиксированный список из плана исследования, 6 команд), `market_size_rank_nba` (dense-rank по MSA population с тай-брейками по DMA), `dma_rank_us`.

**(6) Awards.** `all_nba_lag1`, `career_all_nba_count`, `career_allstar_count`, `mvp_lag1`, `dpoy_lag1`, `supermax_eligible_loose` (бинарный индикатор согласно CBA 2017). В альтернативной spec `M1c_full_robust_awards` кумулятивные счётчики заменяются бинарными `has_career_all_nba`, `has_career_allstar`, `multi_all_nba` (≥3 selections) для устранения contamination со стороны aging-veteran selection bias.

**(7) Durability.** `games_missed_lag1` (число пропущенных матчей в предыдущем сезоне, относительно нормы 82 или 72 для COVID-сезонов 2019/20 и 2020/21), `games_missed_3y_cum`, `gp_pct_t`.

**(8) Team.** `team_win_pct_lag1`, `team_made_playoffs_lag1`, `team_playoff_round_reached`, `team_salary_committed_t` (внутри-панельная агрегация по команде × сезон), `team_over_luxury_tax_t`.

**(9) Structural.** `post_cba_2017` (дамми для сезонов ≥ 2017/18), `post_covid` (дамми для сезонов 2019/20 и 2020/21), `is_canada` (для Торонто).

Формальное определение supermax-eligibility (CBA 2017, Designated Veteran Extension):

$$\text{supermax\_eligible}_{i,t} = 1 \iff \big[\text{all\_nba}_{i,t-1} = 1\big] \lor \big[|\{s \in \{t-1, t-2, t-3\}: \text{all\_nba}_{i,s} = 1\}| \geq 2\big] \lor \big[\text{mvp}_{i,t-1} = 1\big] \lor \big[\text{dpoy}_{i,t-1} = 1\big]$$

маскируется к 0 для сезонов < 2018 (первое supermax-расширение оформлено летом 2017 г.). Контрактные «tiers» приписываются rule-based классификатором с шестью приоритетными правилами (полный алгоритм — в `analysis_v2/classify_tier.py`, включая Rose Rule для designated rookie extension); классификация валидирована вручную на 30 топ-игроках с расхождением ≤ 10%.

## 3.5 Эконометрическая спецификация

### 3.5.1 Базовое Mincer-расширение

Отправная точка анализа — расширение функции заработной платы Mincer (1974) для условий профессионального спорта:

$$\ln(\text{salary}_{i,t}) = \alpha + X'_{i,t} \beta + \gamma_t + u_{i,t}$$

где $X_{i,t}$ — вектор регрессоров из блоков 1–9, $\gamma_t$ — year fixed effect (сезонный дамми), $u_{i,t}$ — ошибка. Stand error кластеризуются на уровне `player_id` (Cameron et al., 2011): это допускает произвольную внутри-игроковую корреляцию ошибок (карьерные траектории, постоянные индивидуальные характеристики), но предполагает независимость между игроками.

Четыре базовые спецификации, унаследованные из v1-итерации проекта:

- **M1a** — pooled OLS без year FE.
- **M1b** — pooled OLS + year FE.
- **M1c** — combined performance metrics (только не-коллинеарное подмножество) + year FE.
- **M1d** — two-way fixed effects (player + season).

Тестирование гипотезы воспроизводимости (см. §3.8.1) показывает, что эти четыре модели на расширенном датасете v2 (без новых регрессоров) дают коэффициенты, отличающиеся от опубликованной v1-версии на максимальную абсолютную разницу 5 × 10⁻⁵. Это означает, что добавление новых данных не нарушает базовые соотношения и расширения корректно «настраиваются» поверх v1.

### 3.5.2 Расширенная спецификация M1c_full

Главная спецификация работы — **M1c_full** — включает все 9 блоков регрессоров:

$$\ln(\text{salary}_{i,t}) = \alpha + \text{Stats}'_{i,t} \beta_1 + \text{Age}'_{i,t} \beta_2 + \text{Demo}'_{i,t} \beta_3 + \text{Cont}'_{i,t} \beta_4 + \text{Mkt}'_{i,t} \beta_5$$
$$+ \text{Awd}'_{i,t} \beta_6 + \text{Dur}'_{i,t} \beta_7 + \text{Team}'_{i,t} \beta_8 + \text{Str}'_{i,t} \beta_9 + \gamma_t + u_{i,t}$$

с year FE и cluster-robust SE. К M1c_full строятся четыре альтернативные спецификации:

- **M1c_full_alt_mkt** — `top5_market` заменяется на `market_size_rank_nba` (непрерывная альтернатива).
- **M1c_full_robust_awards** — кумулятивные счётчики наград заменяются бинарными индикаторами.
- **M1c_full_no_collinear** — исключены `experience` и `ws` (VIF > 10) для проверки устойчивости.
- **M1d_full** — two-way FE; time-invariant переменные (drafted, continent, post_cba_2017) дропаются автоматически.

### 3.5.3 Тематические спецификации по гипотезам

К каждой из четырёх новых гипотез (H3, H5–H6, H7, H10) строится отдельная группа моделей:

**M9 (тестирование H3 — институциональная иерархия).** Tier-структура tested тремя моделями:
- M9a — только tier dummies (без Performance).
- M9b — M1c_full + tier dummies.
- M9c — M9b + `supermax_eligible_loose` + interaction `tier_max_30 × eligible`. (Interactions с `tier_supermax` и `tier_max_35` опускаются — у первой нулевая вариация по eligible by classifier design, у второй perfect collinearity.)

Дополнительно — tier-specific Mincer-регрессии: восемь отдельных регрессий $\ln(\text{salary}) \sim \text{Stats} + \text{Age}$ на подвыборках по tier. Тестируется cap-truncation: ожидаемо, что $\beta_{\text{ppg}}$ в max-tiers ниже, чем в mid-level (Rosen, 1986;).

**M10 (тестирование H5 — awards channel) и event study (тестирование H6).** Спецификации:
- M10a (cumulative) — M1c_full с `all_nba_lag1 + career_all_nba_count + career_allstar_count`.
- M10a_robust — бинарные индикаторы вместо кумулятивных.
- M10b — substitution `supermax_eligible_loose` вместо `all_nba_lag1` (избегая collinearity r = 0.78).

Event study вокруг первого All-NBA selection в карьере:

$$\ln(\text{salary}_{i,t}) = \alpha + \sum_{\tau \neq -1} \beta_\tau \cdot \mathbf{1}\{t - t^*_i = \tau\} + X'_{i,t} \delta + \gamma_t + u_{i,t}$$

где $t^*_i$ — сезон первого All-NBA selection игрока $i$, $\tau \in \{-2, -1, 0, +1, +2, +3, \geq +4\}$, never-treated игроки — baseline. $\tau = -1$ — reference period. Эта спецификация позволяет визуализировать timing salary jump относительно события (H6: ожидаем jump в $\tau \in \{+2, +3\}$ через contract renewal cycle).

**M8 (тестирование H7 — market hypothesis).** Четыре спецификации:
- M8a — M1c_full с `top5_market` (main).
- M8b — `market_size_rank_nba` (непрерывная).
- M8c — `top5_market + allstar + top5 × allstar` (heterogeneity по звездности).
- M8d — `top5_market + is_international + top5 × is_international`.

На interaction-коэффициентах M8c и M8d применяется wild-cluster bootstrap (Rademacher weights, 1000 реплик; MacKinnon & Webb, 2018) с restricted null-моделью — для робастной инференции при малом числе кластеров «top5 × allstar» (Cameron et al., 2011).

**M11 (тестирование H10 — durability).** Спецификации:
- M11a — M1c_full + `games_missed_lag1`.
- M11b — M11a + interaction `games_missed_lag1 × age` (age-mediated discount).

### 3.5.4 Полная спецификация M_full

«Kitchen sink» спецификация, объединяющая всё:

$$\ln(\text{salary}) = \alpha + X'_{\text{M1c\_full}} \beta + \text{Tier} + \text{SuperMax} + \gamma_t + u$$

на 2 268 наблюдениях с ≈ 47 регрессорами. Используется для финальной форест-диаграммы и сравнения c M1c_full / M9b в иерархии R² (см. §4).

## 3.6 Декомпозиция объяснённой дисперсии (Shapley R²)

Главный методологический вклад работы — декомпозиция $R^2$ полной модели по 9 блокам переменных с использованием значения Шепли (Shapley, 1953; Lipovetsky & Conklin, 2001).

**Sequential R²** (наивный подход) определяется как:

$$\Delta R^2_k = R^2(\{B_1, \ldots, B_k\}) - R^2(\{B_1, \ldots, B_{k-1}\})$$

где $B_k$ — k-й блок. Этот метод прост, но **зависит от порядка** добавления блоков: для нашего датасета атрибуция блока Awards меняется в 33 раза между plan-order и reverse-order. Для робастной диагностики мы запускаем sequential R² в двух порядках и сообщаем оба результата (см. §4.2).

**Shapley R²** — order-independent атрибуция, в которой вклад блока $B_i$ определяется как средний marginal contribution по всем возможным порядкам:

$$\phi_i = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|! (|N| - |S| - 1)!}{|N|!} \cdot \left[ R^2(S \cup \{B_i\}) - R^2(S) \right]$$

где сумма по всем подмножествам $S$ блоков, не включающих $B_i$. Значение Шепли удовлетворяет четырём аксиомам: efficiency ($\sum_i \phi_i = R^2_{\text{full}}$), symmetry, dummy и additivity (Shapley, 1953). Это единственная аллокация, удовлетворяющая всем четырём аксиомам одновременно, что делает Shapley предпочтительным методом «справедливой атрибуции» вкладов.

Вычислительная сложность для 9 блоков — $2^9 = 512$ OLS-фитов; на нашей выборке (2 268 строк, до 38 регрессоров) — ≈ 10 секунд. Аксиома efficiency верифицируется численно: $|\sum_i \phi_i - R^2_{\text{full}}| \approx 1.4 \times 10^{-16}$ (машинная точность). Для оценки неопределённости применяется cluster bootstrap на player_id (200 повторов), 95% CI = [2.5-й, 97.5-й перцентили].

Альтернативные order-independent декомпозиции — Pratt (1987) и Genizi (1993) — близки к Shapley в практике (различия ≤ 2 п.п. share-of-explained), но не удовлетворяют efficiency-аксиоме одновременно с symmetry; в нашей работе используется Shapley как теоретически наиболее обоснованный.

## 3.7 Инференс и контроль multiple testing

### 3.7.1 Cluster-robust SE

Все стандартные ошибки в pooled и year-FE спецификациях кластеризуются на `player_id` (Cameron et al., 2011). Это эквивалентно предположению о произвольной автокорреляции внутри карьеры одного игрока и независимости между игроками. Для two-way FE используется HC3-робастные SE внутри `linearmodels.PanelOLS`.

### 3.7.2 Wild-cluster bootstrap

Для interaction-коэффициентов в M8c и M8d стандартный cluster-robust SE может быть искажён из-за малого числа эффективных кластеров в подгруппе `top5 × allstar` (≈ 40 игроков-сезонов). Применяется wild-cluster bootstrap (MacKinnon & Webb, 2018): null-restricted residuals × Rademacher weights ($\pm 1$ с p=0.5) на уровне кластера × 1000 реплик. 95% CI на interaction-коэффициенте позволяет проверить heterogeneity без зависимости от asymptotic approximation.

### 3.7.3 Multiple testing correction

При тестировании 10 гипотез H1–H10 (см. §2) с одиннадцатью ключевыми коэффициентами (некоторые гипотезы тестируются несколькими спецификациями) применяются две процедуры:

- **Bonferroni** при $\alpha = 0.05$: $\alpha^* = 0.05 / 11 = 0.0045$ — наиболее консервативная коррекция.
- **Benjamini-Hochberg False Discovery Rate (BH-FDR)** при $q = 0.05$: контроль ожидаемой доли ложных открытий среди всех отвергнутых гипотез (Benjamini & Hochberg, 1995).

Обе процедуры применяются ex post к ключевым коэффициентам новых гипотез (H3 tier, H5–H6 awards, H7 market, H10 durability); гипотезы v1 (H1–H2, H4, H8–H9) считаются предзарегистрированными и в multiple testing не входят.

## 3.8 Робастность и валидация

### 3.8.1 Тест воспроизводимости v1

Скрипт `analysis_v2/regress_test_v1.py` запускает четыре базовые спецификации M1a–M1d на расширенном датасете v2, используя только переменные, доступные в v1-итерации. Сравнение с опубликованными v1-таблицами показывает максимальное абсолютное расхождение коэффициентов **< 5 × 10⁻⁵**. Это гарантирует, что новые блоки данных (раздел 3.1) не контаминировали базовые соотношения и расширения «настраиваются» поверх валидной v1-основы.

### 3.8.2 VIF

Проверка мультиколлинеарности — variance inflation factor для всех регрессоров основной спецификации. Высокие значения (VIF > 10):
- $age, age^2$: ≈ 150 (ожидаемо by construction для polynomial Mincer);
- $ppg$: 44.6, $mpg$: 26.0, $ws$: 20.5 — кластер коллинеарности performance-метрик.

Альтернативная спецификация `M1c_full_no_collinear` (drop `experience` и `ws`) теряет в R² только −0.011, что свидетельствует об избыточности (а не зависимости) отдельных регрессоров.

### 3.8.3 Oster (2019) δ-sensitivity

Для оценки чувствительности коэффициентов к omitted variable bias применяется closed-form формула Oster (2019, eq. 3):

$$\delta \approx \frac{(\tilde{\beta} - \hat{\beta})(R_{\max} - \hat{R}^2)}{(\dot{\beta} - \tilde{\beta})(\hat{R}^2 - \dot{R}^2)}$$

где $\dot{\beta}$, $\dot{R}^2$ — коэффициенты в spec без controls; $\tilde{\beta}$, $\hat{R}^2$ — в spec с controls; $R_{\max} = 1.3 \cdot \hat{R}^2$. $\delta$ интерпретируется как отношение силы пропущенных переменных к силе включённых, необходимое для аннулирования эффекта; $\delta > 1$ означает робастность к OVB.

Метод применяется к шести ключевым новым коэффициентам. **Знак коэффициентов стабилен**, magnitude может сдвигаться; ограничения метода в богатых-наблюдательными переменными датасетах обсуждаются в §5.

### 3.8.4 Альтернативные определения переменных

Для проверки чувствительности к операционализации:
- top5_market vs market_size_rank_nba (M8a vs M8b).
- Кумулятивные vs бинарные индикаторы наград (M1c_full vs M1c_full_robust_awards).
- supermax_eligible_loose vs strict (только в robustness-spec).

## 3.9 Программная реализация

Весь пайплайн реализован в Python 3.13 с использованием:
- `pandas` 2.x — манипуляции с данными;
- `statsmodels` — pooled OLS, cluster-robust SE;
- `linearmodels` — PanelOLS для year FE и two-way FE;
- `numpy` — численные операции;
- `scipy.stats` — bootstrap inference;
- `matplotlib` + `seaborn` — визуализация;
- `curl_cffi` — TLS-fingerprint спуфинг для bbref скрапинга;
- `beautifulsoup4` — HTML-парсинг.

Исходный код, данные и репродукционные команды размещены в публичном репозитории GitHub (см. Раздел «Декларация открытого кода» в конце работы). Регресс-тест воспроизводимости v1 в `analysis_v2/regress_test_v1.py` запускается перед каждой пере-сборкой и обязан возвращать PASS.

---

## Резюме главы 3

Использована собственноручно собранная панель 3 660 player-seasons (953 игрока × 9 сезонов) с 153 переменными в 9 тематических блоках. Зависимая переменная — логарифм реальной зарплаты. Основная спецификация — расширенная Mincer-функция с year fixed effects и cluster-robust SE на уровне игрока. Главный методологический вклад — Shapley R²-декомпозиция объяснённой дисперсии по 9 блокам, удовлетворяющая axioms эффективности, симметрии и аддитивности. Робастность обеспечивается: (а) тестом воспроизводимости v1 (max diff < 5×10⁻⁵), (б) VIF-диагностикой и no_collinear-спецификацией, (в) Oster δ-sensitivity, (г) wild-cluster bootstrap для interaction-коэффициентов, (д) Bonferroni и BH-FDR multiple testing corrections. Полная воспроизводимость пайплайна гарантируется hash-snapshot датасета и публичным репозиторием.


---

# Глава 4. Результаты

> Объём: ≈ 15% работы (целевые ~1800 слов; в драфте чуть больше, сократим на финальном этапе).
> **Важно:** этот раздел содержит только эмпирические результаты. Интерпретация и обсуждение — в Главе 5. Гипотезы пронумерованы согласно `hypotheses_v2_final.md` (H1–H10, единая нумерация).

---

## 4.1 Описательная статистика

Финальная выборка: 3 660 player-season за 2015/16–2023/24, 953 уникальных игрока. Медианная номинальная зарплата 2023/24 — \$2.85 млн, средняя — \$8.74 млн, максимум — \$51.9 млн (Стеф Карри). Логарифм реальной зарплаты $\ln(\text{salary}/\text{CPI})$ имеет почти-нормальное распределение с асимметрией +0.16 и эксцессом 2.31 (см. Приложение D.1 для гистограммы и Q-Q).

Распределение по другим ключевым переменным: средний возраст 26.3 года, средняя experience 4.4 сезона, доля игроков-неамериканцев 26.8% (доминируют Канада 4.1% и Европа 13.4%). Доля строк с TOT-attribution — 13.9%. Доля сезонов post-CBA-2017 — 77.8%.

Описательные статистики полной таблицы — Приложение D.2 (output/tables/descriptive_stats.csv).

## 4.2 Базовое Mincer-расширение (H1, H2, H4)

Четыре спецификации M1a–M1d (см. §3.5.1) запускаются на полной выборке n = 3 660.

| Спецификация | $\beta_{\text{ppg}}$ | $\beta_{\text{age}}$ | $\beta_{\text{age}^2}$ | $\beta_{\text{post\_cba\_2017}}$ | $R^2$ |
|---|---|---|---|---|---|
| M1a (pooled basic) | +0.031*** | +0.413*** | −0.0070*** | +0.219*** | 0.648 |
| M1b (basic + year FE) | +0.031*** | +0.420*** | −0.0071*** | (absorbed) | 0.647 |
| M1c (combined + year FE) | +0.034*** | +0.408*** | −0.0070*** | (absorbed) | 0.651 |
| M1d (player + year FE) | +0.011 | (collinear) | (collinear) | (absorbed) | 0.151 (within) |

*** p < 0.001, ** p < 0.01, * p < 0.05. Cluster-robust SE на `player_id`. Полные таблицы — `output/tables_v1/M1a_pooled_basic.txt` и др.

Полученный возрастной пик (рассчитан как $-\beta_{\text{age}} / 2\beta_{\text{age}^2}$): **29.5 года** (95% CI [28.4, 30.6]).

`post_cba_2017` коэффициент в M1a: +0.219, означает рост реальной зарплаты в среднем на $e^{0.219} - 1 = +24.5\%$ после реформы. Эффект устойчив к разным спецификациям, но поглощается year FE (логично — он сезонный).

**Статус гипотез:** H1 (Performance ↑ → salary ↑) подтверждается на всех спецификациях; H2 (inverted-U возрастной профиль с пиком ≈29) подтверждается; H4 (CBA 2017 структурный break) подтверждается.

## 4.3 Институциональная иерархия (H3)

Тестирование иерархии контрактных tier'ов через спецификации M9a, M9b и M_full (§3.5.3).

| Спецификация | Регрессоры | $R^2$ | $N$ |
|---|---|---|---|
| M1c_full | Performance + Age + Demo + Awards + Durability + Team + Market + Structural | 0.651 | 2 268 |
| **M9a** | **Только tier dummies** | **0.849** | 2 268 |
| **M9b** | M1c_full + tier dummies | **0.862** | 2 268 |
| M_full | M9b + supermax_eligible | 0.862 | 2 268 |

Tier-коэффициенты в M_full (reference = `mid_level`, n = 717):

| Tier | $\beta$ | SE | p | $e^{\beta} - 1$ |
|---|---|---|---|---|
| minimum | −0.905 | 0.045 | <0.001 | −59.6% |
| rookie_scale | −0.088 | 0.045 | 0.051 | −8.4% |
| high_mid | +0.301 | 0.034 | <0.001 | +35.1% |
| max_25 | +0.811 | 0.058 | <0.001 | +125.0% |
| max_30 | +1.001 | 0.087 | <0.001 | +172.1% |
| max_35 | +1.279 | 0.151 | <0.001 | +259.4% |
| supermax | +1.188 | 0.116 | <0.001 | +228.0% |

Tier-specific Mincer-регрессии ($\ln(\text{salary}) \sim \text{Performance} + \text{Age}$ на подвыборках по tier):

| Tier | $n$ | $\beta_{\text{ppg}}$ | p | $R^2_{\text{within}}$ |
|---|---|---|---|---|
| mid_level | 717 | +0.078** | 0.017 | 0.46 |
| high_mid | 442 | +0.071*** | <0.001 | 0.47 |
| max_25 | 209 | +0.068*** | 0.001 | 0.49 |
| max_30 | 50 | +0.034* | 0.012 | 0.49 |
| supermax | 33 | +0.067*** | 0.001 | 0.67 |

$\beta_{\text{ppg}}$ в max_30-tier в 2.3 раза ниже, чем в mid_level (Δ = 0.044, p сравнения < 0.05 — bootstrap, 1000 реплик).

**Статус H3:** подтверждается. Tier dummies одни объясняют 84.9% дисперсии $\ln(\text{salary})$; добавление performance-метрик к ним увеличивает $R^2$ только на +1.3 п.п.

## 4.4 Awards channel (H5, H6)

### Спецификация M10a и robust-вариант

| Регрессор | $\beta$ (M10a) | p | $\beta$ (M10a_robust) | p |
|---|---|---|---|---|
| all_nba_lag1 | +0.185 | 0.008 | +0.159 | 0.044 |
| career_all_nba_count | −0.045 | 0.018 | — | — |
| career_allstar_count | +0.122 | <0.001 | — | — |
| has_career_all_nba | — | — | +0.025 | 0.79 |
| has_career_allstar | — | — | +0.331 | <0.001 |
| multi_all_nba | — | — | −0.220 | 0.038 |

Численные интерпретации (в процентах от средней зарплаты):
- All-NBA в предыдущем сезоне → +20.3% ($e^{0.185} - 1$).
- Бывший All-Star (когда-либо в карьере) → +39.2%.
- Multi-time All-NBA (≥3 selections) → −19.7%.

### Event study вокруг первого All-NBA selection (M10 event)

| $\tau$ | $\beta_\tau$ | 95% CI | p |
|---|---|---|---|
| −2 | −0.21 | [−0.54, +0.12] | 0.21 |
| −1 | 0 | reference | — |
| 0 | −0.24 | [−0.51, +0.03] | 0.08 |
| +1 | +0.17 | [−0.04, +0.37] | 0.11 |
| +2 | +0.21 | [+0.02, +0.40] | 0.029 |
| +3 | +0.22 | [+0.01, +0.43] | 0.037 |
| ≥4 | −0.11 | [−0.33, +0.11] | 0.33 |

Визуализация — Рисунок F4 (`output/figures/F4_event_study_all_nba.pdf`).

**Статус H5:** подтверждается. Контрольный коэффициент $\beta_{\text{all\_nba\_lag1}}$ положителен и значим (p = 0.008, BH-FDR pass).

**Статус H6:** подтверждается. Event study показывает значимые положительные коэффициенты при $\tau = +2$ ($\beta = +0.21$, p = 0.029) и $\tau = +3$ ($\beta = +0.22$, p = 0.037), при отсутствии значимости в $\tau = -2, -1, 0, +1, \geq 4$. Pre-trends чисты (CI в $\tau = -2, -1$ включает 0).

## 4.5 Рыночные эффекты (H7)

Спецификация M8a (M1c_full + `top5_market`):

$$\hat\beta_{\text{top5}} = -0.098, \quad \text{SE} = 0.043, \quad p = 0.022$$

Знак отрицательный и статистически значим. Игроки в командах top-5 NBA markets (LAL, LAC, NYK, BRK, CHI, GSW) получают на $e^{-0.098} - 1 = -9.3\%$ меньше при контроле всех остальных факторов.

M8b с непрерывной переменной `market_size_rank_nba`: $\hat\beta = +0.004$ на единицу ранга (больший ранг = меньший рынок), что согласуется с направлением M8a.

Heterogeneity-тесты (M8c, M8d) с wild-cluster bootstrap (1000 реплик, Rademacher):

| Спецификация | Interaction | $\beta_{\text{int}}$ | wild-cluster CI95 |
|---|---|---|---|
| M8c | top5 × allstar | +0.157 | [−0.198, +0.194] |
| M8d | top5 × is_international | +0.058 | [−0.237, +0.233] |

Ни одна interaction не значима.

**Статус H7:** **отвергается в anti-направлении**. Премия за крупный рынок отсутствует; вместо неё обнаруживается дисконт ~9% без heterogeneity по звёздности или происхождению.

## 4.6 Командный контекст (H8)

Спецификация M1c_full с командными контролями:

| Регрессор | $\beta$ | SE | p |
|---|---|---|---|
| team_win_pct_lag1 | +0.062 | 0.061 | 0.31 |
| team_made_playoffs_lag1 | +0.034 | 0.041 | 0.41 |
| team_playoff_round_reached | +0.012 | 0.018 | 0.50 |
| team_over_luxury_tax_t | −0.045 | 0.040 | 0.26 |

Все четыре коэффициента не значимы (p > 0.15). 95% доверительные интервалы пересекают ноль.

**Статус H8:** **отвергается, informative null**. Командные контексты не определяют индивидуальную зарплату после контроля игроковых факторов.

## 4.7 Налог штата (H9)

Спецификация M2c (восстановлена из v1, расширена включением Toronto после A3-фикса):

| Регрессор | $\beta$ | SE | p |
|---|---|---|---|
| state_tax_rate (M2c) | +0.150 | 0.140 | 0.29 |
| no_income_tax (M2b) | −0.019 | 0.039 | 0.63 |

$n = 3 152$ (включая Toronto, 107 obs).

MDE-расчёт (minimum detectable effect, мощность 80%, $\alpha = 0.05$): $|\beta| \geq 0.40$ был бы детектируем. То есть, если бы существовал ≥21% pre-tax wage shift между низконалоговыми штатами (TX, FL, TN, NV) и высоконалоговыми (CA, NY, ON), мы бы его обнаружили. Не обнаруживаем.

**Статус H9:** **отвергается, informative null**. После контроля игроковых факторов и cap-share, налог штата не влияет на pre-tax salary.

## 4.8 Durability (H10)

Спецификация M11a (M1c_full + `games_missed_lag1`):

| Регрессор | $\beta$ | SE | p |
|---|---|---|---|
| games_missed_lag1 (M11a) | −0.0049 | 0.0011 | <0.001 |
| games_missed_lag1 (M11b) | −0.0010 | — | 0.13 |
| games_missed_lag1 × age (M11b) | −0.00038 | — | 0.12 |

В main-спецификации M11a: каждый пропущенный матч в прошлом сезоне снижает зарплату на $e^{-0.0049} - 1 = -0.49\%$. За 30 пропусков (тяжёлая травма) — −14.7%.

Interaction `× age` в M11b не значима (p = 0.12).

**Статус H10:** подтверждается. Эффект durability экономически и статистически значим (p < 0.001; проходит BH-FDR @ 5% и Bonferroni).

## 4.9 Декомпозиция объяснённой дисперсии (главный результат)

### Shapley-декомпозиция $R^2$ по 9 блокам

| Блок | Shapley $\phi$ | Доля от $R^2_{\text{full}}$ |
|---|---|---|
| Performance | 0.239 | 36.8% |
| Age + Experience | 0.186 | 28.7% |
| Demographics | 0.091 | 14.1% |
| Awards | 0.079 | 12.2% |
| Durability | 0.037 | 5.7% |
| International | 0.005 | 0.8% |
| Team | 0.005 | 0.8% |
| Structural | 0.004 | 0.6% |
| Market | 0.001 | 0.2% |
| **Σ (= $R^2_{\text{full}}$)** | **0.649** | **100.0%** |

Эффективность Шепли (efficiency axiom): $|\sum_i \phi_i - R^2_{\text{full}}| = 1.4 \times 10^{-16}$ (машинная точность). Визуализация — Рисунок F1 (`output/figures/F1_waterfall_shapley.pdf`), главный рисунок работы.

### Sequential R² (диагностика order-dependence)

| Блок | Plan-order | Reverse-order | Shapley |
|---|---|---|---|
| Performance | 0.446 | 0.115 | 0.239 |
| Age | 0.169 | 0.139 | 0.186 |
| Demographics | 0.013 | 0.083 | 0.091 |
| Awards | 0.006 | 0.199 | 0.079 |
| Structural | 0.004 | 0.003 | 0.004 |
| Market | 0.001 | 0.000 | 0.001 |
| Team | 0.002 | 0.010 | 0.005 |
| Durability | 0.004 | 0.093 | 0.037 |
| International | 0.005 | 0.007 | 0.005 |

Sequential R² показывает большую чувствительность к порядку: атрибуция блока Awards меняется в 33 раза между plan- и reverse-order (0.006 → 0.199). Shapley даёт устойчивую оценку 0.079. Визуализация различий — Рисунок F7 (`output/figures/F7_seq_vs_shapley.pdf`).

## 4.10 Контроль multiple testing

Применение Bonferroni ($\alpha^* = 0.05/11 = 0.0045$) и BH-FDR (q = 0.05) к одиннадцати ключевым тестам новых гипотез:

| Гипотеза | Ключевой $\beta$ | $p$-value | Bonferroni @ 5% | BH-FDR @ 5% |
|---|---|---|---|---|
| H3 (tier_supermax) | +1.188 | <0.001 | ✓ | ✓ |
| H3 (tier_max_35) | +1.279 | <0.001 | ✓ | ✓ |
| H3 (tier_minimum) | −0.905 | <0.001 | ✓ | ✓ |
| H5 (all_nba_lag1) | +0.185 | 0.008 | — | ✓ |
| H5 (career_allstar_count) | +0.122 | <0.001 | ✓ | ✓ |
| H6 (event_study τ=+2) | +0.21 | 0.029 | — | ✓ |
| H6 (event_study τ=+3) | +0.22 | 0.037 | — | — |
| H7 (top5_market) | −0.098 | 0.022 | — | ✓ |
| H7 (top5 × allstar) | +0.157 | 0.84 (wild-cluster) | — | — |
| H10 (games_missed_lag1) | −0.0049 | <0.001 | ✓ | ✓ |
| H10 (games_missed × age) | −0.00038 | 0.12 | — | — |

Из одиннадцати тестов:
- 5 проходят консервативную Bonferroni-коррекцию;
- 7 проходят BH-FDR @ 5%.

С учётом гипотез v1 (H1, H2, H4), которые тестировались в предзарегистрированной v1-итерации и поэтому не входят в multiple testing pool новых гипотез, общий итог: **из 10 гипотез H1–H10 семь подтверждены при контроле multiple testing**.

## 4.11 Иерархия моделей $R^2$ (сводная)

| Модель | $R^2$ | $N$ | Описание |
|---|---|---|---|
| M1a (v1 baseline) | 0.648 | 3 660 | pooled OLS, basic stats |
| M1c (v1 reference) | 0.651 | 3 660 | combined stats + year FE |
| M1c_full | 0.651 | 2 268 | M1c + 9 v2 блоков |
| M9a | 0.849 | 2 268 | только tier dummies |
| M9b (M_full без supermax) | 0.862 | 2 268 | M1c_full + tier dummies |
| **M_full** | **0.862** | **2 268** | **полная спецификация** |

Прирост $R^2$ от M1c_full (только переменные) к M9b (+ tier) — **+0.21 п.п.**; от M9b к M_full (+ supermax) — < 0.001. Институциональная категоризация (tier) даёт существенно больший прирост, чем расширение списка регрессоров.

---

## Резюме главы 4

Из 10 гипотез H1–H10 семь подтверждаются (H1, H2, H3, H4, H5, H6, H10), три отвергаются в anti-направлении или как informative null (H7, H8, H9). Главный методологический результат — Shapley-декомпозиция $R^2 = 0.649$ по 9 блокам с эффективностью, верифицированной до машинной точности: Performance (36.8%) и Age (28.7%) доминируют, Awards (12.2%), Demographics (14.1%) и Durability (5.7%) формируют значимый второй уровень, Market + Team + Structural + International дают совокупно ≈ 2.4%. Институциональная категоризация (tier dummies) одна объясняет $R^2 = 0.85$, что превышает full M1c-спецификацию.

Содержательное обсуждение этих результатов — Глава 5.


---

# Глава 5. Обсуждение

> Цифры — только короткие references на §4.X; интерпретация — основное содержание.
> Маркеры `[TBD: см. {author_year}]` помечают cite'ы, которые требуют верификации по шаблонам из `bibliography/sources/`.

---

## 5.1 Главный методологический и содержательный вывод

Результаты Главы 4 §4.9 устанавливают первую axiom-обоснованную количественную иерархию факторов, определяющих $\ln(\text{salary})$ в NBA в post-2011-CBA эпоху. Shapley-декомпозиция $R^2 = 0.649$ по 9 тематическим блокам показывает: **Performance** (36.8%) и **Age + Experience** (28.7%) совокупно объясняют 65.5% дисперсии — что соответствует ожиданиям классической Mincer-литературы (Mincer, 1974; Rosen, 1981). Однако наивная sequential R²-декомпозиция в plan-order приписывает Performance 68.7% (см. §4.9 Таблица «Sequential vs Shapley») — почти вдвое больше, чем axiom-justified Shapley. Это расхождение — главный методологический сюрприз работы: значительная доля variance, которую sequential R² атрибутирует Performance, на самом деле share с Awards-, Durability-, и Tier-блоками, и при honest attribution перераспределяется в эти каналы.

Содержательное значение: **CBA-структурирование** (tier categorization, awards eligibility, supermax mechanism) и **survival effects** (durability) являются не побочными факторами, а независимыми каналами формирования зарплат, экономически и статистически отделимыми от Performance. NBA-salary в современной эпохе формируется не только через continuous performance pricing, но через систему institutional channelling, которая ранее в литературе не quantified.

## 5.2 Институциональная иерархия как доминирующий слой (H3)

Результат, что tier dummies одни объясняют $R^2 = 0.849$ (§4.3), является, насколько нам известно, первым количественным доказательством того, что NBA в post-2011-CBA эпохе функционирует не как continuous-pricing labor market в традиционном Mincer-смысле, а как **discrete institutional categorization**. Игрок попадает в одну из 8 категорий (minimum, rookie_scale, mid-level, high-mid, max-25, max-30, max-35, supermax) преимущественно через institutional pathway (CBA-определённые правила eligibility), и его внутри-tier salary становится практически фиксированной величиной с малыми отклонениями.

Этот результат — нетривиальное extension классической теории Rosen (1986) о cap-induced concavity. Rosen предсказывал, что binding cap должен делать reward function concave для top-tier игроков; наши tier-specific Mincer-регрессии (§4.3 Таблица 3) подтверждают это эмпирически: $\beta_{\text{ppg}}$ внутри max_30-tier в 2.3 раза ниже, чем в mid_level. Но более важное наблюдение — что **structure salary не просто concave, а step-function**. Discrete jumps между tiers (e.g., от high-mid к max-25: +56% в expected salary) намного больше, чем continuous variation внутри tier (median within-tier spread ~10%). Это означает, что primary determinant зарплаты NBA-игрока — это вопрос «попадёт ли он в следующий tier», а не «насколько хорошо он играет внутри своего tier».

Эта картина согласуется с Hill & Groothuis (2001), которые предсказывали, что cap создаст «institutional layer» поверх Mincer pricing, но идёт дальше: institutional layer не дополнение, а доминирующий механизм. Performance-метрики работают через **institutional bridge** — PPG → All-Star/All-NBA selection → tier eligibility → discrete salary jump — а не через continuous wage adjustment.

## 5.3 Awards channel и contract renewal cycle (H5, H6)

Результаты Главы 4 §4.4 устанавливают, что awards канал работает через два уровня: (а) immediate signaling effect (all_nba_lag1 → +20% к salary при контроле текущего performance, p = 0.008); (б) delayed event-study effect — после первого All-NBA selection salary skip +21% при $\tau = +2$ (p = 0.029) и +22% при $\tau = +3$ (p = 0.037), при отсутствии значимости в $\tau = -2, -1, 0, +1$ (pre-trends чисты).

Эта двухуровневая структура согласуется с теоретическими предсказаниями rank-order tournaments. Lazear & Rosen (1981) формализуют, что «differences in the level of output between individuals may be quite small, yet optimal 'prizes' are selected in a way that induces workers to allocate their effort and investment activities efficiently» (Lazear & Rosen, 1981, p. 2) — то есть spread W₁ − W₂ может значительно превышать marginal product difference между rank positions, и это является не аномалией, а характеристикой efficient contract design. На более fundamental уровне Hölmström (1979) informativeness principle обосновывает inclusion разных performance signals (PPG, awards, durability) в Mincer-spec'ах: «A signal is valuable if and only if it is informative» (Hölmström, 1979, p. 84, Proposition 3). Однако delayed effect (τ = +2, +3) указывает на specific mechanism, не explicitly предсказанный в Lazear-Rosen — **contract renewal cycle**. Awards не переводятся в зарплату мгновенно, потому что большинство активных NBA-контрактов фиксируют salary на 2–4 года forward. Premium реализуется в next renewal event, когда новый контракт подписывается с применением правил designated extension (Coon, n.d., Q24).

Это эмпирическое подтверждение contract-cycle dynamics, теоретически обсуждавшейся в Stiroh (2007) для general contract-year effect, но впервые quantified specifically для NBA awards channel. Cycle mechanism — institutional, а не behavioral: оно работает не потому, что игроки «играют лучше» в contract year (хотя это может тоже происходить), а потому, что CBA-правила определяют, в какой момент новая salary structure активируется.

**Aging-veteran sub-finding** (§4.4: multi_all_nba (≥3) β = −0.22, p = 0.038) представляет уникальное observation, ранее не quantified в NBA literature. Игроки с историей нескольких All-NBA selections, находящиеся в declining phase карьеры, несут residual penalty −19.7% против non-veteran игроков с тем же current performance. Содержательная интерпретация — **survival bias**: возрастные «легенды» с ухудшающимся текущим performance непропорционально часто продолжают карьеру (вопреки physical decline), что создаёт residual mismatch между past elite status и current pricing. Этот mechanism нуждается в follow-up исследовании; гипотетический канал — risk-averse team management, готовое overpay'ить за brand value veteran star vs гипотетический канал — career-end transaction frictions.

## 5.4 Anti-marketability и Hembre channel (H7)

Результат, что top-5 NBA cities дают не премию, а discount $\hat{\beta} = -0.098$ (p = 0.022, §4.5), отвергает классическую Rosen-style marketability hypothesis для современной NBA. Heterogeneity-тесты с wild-cluster bootstrap (1000 реплик, Rademacher) показывают, что эффект uniform across звёздности и nationality (interaction × allstar и × intl не значимы), что исключает signal-amplification interpretation.

Hembre (2022) предлагает theoretical channel, совместимый с направлением нашего эффекта: при unrestricted free agency игроки требуют compensating differential за state income tax burden, что снижает spending power команд в high-tax штатах (CA, NY, IL — преимущественно где базируются top-5 NBA cities). Сам Hembre, однако, сообщает, что NBA-specific coefficient в его pooled-sport regression статистически незначим ($\hat{\beta}_{\text{NBA}} \in [-0.143, -0.069]$, SE > 1.1, Table 3, p. 20); pooled effect доминируется NFL и MLB sub-samples (Hembre, 2022, p. 11). Поэтому мы не можем интерпретировать наш result как direct confirmation Hembre's NBA channel; точная формулировка — «consistent direction, although NBA-specific imprecise in pooled-sport setup».

Альтернативное объяснение — **player-side compensating differential** через off-court endorsement доход и lifestyle крупных рынков (cases: LeBron 2018 → LAL под cap, Durant 2016 → GSW на 1+1). Эта interpretation не identifying'нается direct'ом в наших данных (endorsement income не собран; revealed-preference selection не observable), но согласуется с qualitative observations. Comprehensive разрешение направления anti-marketability — между tax-driven (Hembre channel) и preference-driven (off-court substitution) — требует дополнительных данных (endorsement income, individual residence decisions при offers) и оставляется для future research.

В наших данных есть один dimension robustness check, который мы могли бы добавить в follow-up: continuous `state_tax_rate` как control при `top5_market` в joint spec, чтобы посмотреть, «съест» ли он top5 coefficient (см. §6.4 пункт 6). Прямая декомпозиция market vs tax channels — естественная robustness задача для следующей итерации.

## 5.5 Команды и налоговый эффект как informative nulls (H8, H9)

Гипотезы H8 (team success → individual salary) и H9 (state tax → pre-tax salary) обе rejected, но как informative nulls, а не failed tests. По H8 все четыре team-level контроля (win_pct, made_playoffs, playoff_round, over_luxury_tax) дают p > 0.15 с 95% CI, пересекающим ноль (§4.6). По H9 state_tax_rate p = 0.29, и MDE-расчёт показывает, что 21% pre-tax wage shift между low-tax и high-tax штатами был бы детектирован (§4.7).

Содержательная интерпретация: в современной CBA-эпохе **cap mechanism эффективно нейтрализует team-side market power** (Hill & Groothuis, 2001). Bargaining между игроком и командой не происходит «по полной» — оно ограничено CBA-defined категориями (tier eligibility) с малыми deviations. Это согласуется с теоретическим аргументом Kahn (2000) о том, что cap-era sports markets создают labor structure, в которой individual talent оценивается approximately uniformly across markets и teams.

Team success null также согласуется с эмпирической литературой Berri, Brook & Schmidt (2007), которые показывают, что после контроля individual performance team-level controls добавляют мало к explanatory power individual salary. Этот результат можно интерпретировать так: в NBA, individual contribution to team success (measurable через player stats) уже captured в performance метриках; остаточный effect team success (championship status, playoff appearances) — это в основном luck/team-composition factor, не translated в individual salary.

Tax null значительно более тонкий, чем выглядит на первом взгляде. Cross-sport и international evidence доказывает существование tax channel у профессиональных спортсменов: Kleven, Landais & Saez (2013) находят elasticity foreign-player count w.r.t. net-of-tax rate ≈ 1.0 для европейского футбола; Alm, Kaempfer & Sennoga (2012) находят +$21–24 тыс. на pp tax rate для MLB free agent salaries в 1995–2001. Особенно критично — Johnson & Hall (2018) на 576 NBA free agent signings за 2010–2014 находят significant positive effect: +$60K на pp average tax rate. Это **direct counter-evidence** нашему H9 null.

Дополнительный mechanism для понимания нашего null даёт Kopkin (2012): на 2001/02–2007/08 NBA FA-данных он показывает, что tax effect реализуется через **quality sorting** (top-FA destinations skewed towards low-tax штатов), а не через salary level. При binding salary cap NBA-команды не могут freely повышать nominal pre-tax compensation в high-tax штатах; adjustment margin переходит на **destination choice**, а не на **price**. Это согласуется с нашим null on salary, но не противоречит существованию tax channel — он работает через distortion of player allocation across teams, неvisible в pooled OLS на ln_salary.

Расхождение с Johnson & Hall можно объяснить тремя факторами. (1) **Sample composition.** Johnson-Hall ограничивают sample только free-agent signings (n=576), где tax mobility-on-margin максимальна. Наш panel включает rookie-scale, extension и supermax contracts, где tier-rules ограничивают mobility by design; 4 из 8 наших contract tiers — mobility-restricted. (2) **Institutional break после CBA 2017.** Их период 2010–2014 — pre-supermax era; designated extension reform 2017 года ещё больше связывает top players с инкумбент-командами, exactly демографию где tax channel сильнее. (3) **Spec details.** Johnson-Hall используют Average Tax Rate (более реалистичный для high-income earners), мы — top marginal; на одних и тех же данных coefficient на ATR должен быть larger чем на MTR. Прямая декомпозиция этих факторов требует replication Johnson-Hall spec на FA-only subset нашего sample — это естественная robustness задача для следующей итерации.

Совокупно: наш H9 null **не доказывает отсутствие tax channel** в NBA — он отражает ограниченную identification power в коротком 9-сезонном panel с cap-constrained mobility-restricted sample. Этот «informative null» согласуется с Kleven-framework: tax-induced mobility у superstars большая и реальна, но активизируется только при наличии free agency и больших cross-jurisdiction разниц (Kleven et al., 2013, pp. 1894, 1923).

## 5.6 Durability как уникальный price effect (H10)

Результат, что каждый пропущенный матч в прошлом сезоне снижает зарплату на 0.49% (β = −0.005/game, p < 0.001, §4.8), и что Shapley-share Durability = 5.7% — значительно больше планового ожидания ≈ 1% — устанавливает, что NBA-рынок прайсит **retrospective health record** как самостоятельный factor, независимо от текущего performance.

Это empirically первое systematic quantification durability discount в NBA. Bodvarsson & Brastow (1998) ранее показали, что NBA labor market rewards statistical consistency в performance (consistency premium после контроля mean productivity); наш H10 — расширение этого логического принципа на **availability consistency** (durability). Mechanism — рынок воспринимает игроков с длинной injury history как риски для будущего performance reliability; этот воспринимаемый risk премий цены через discount в next contract negotiation. Theoretical foundation — Hölmström (1979) informativeness principle: durability — informative signal об underlying health/availability, и rational compensation contract должен incorporate его как distinct dimension от current-period performance.

Интересное негативное finding — interaction games_missed × age не значима (M11b, p = 0.12, §4.8). Гипотеза «травмы стоят больше для стареющих игроков» (intuitive, основанная на physiological recovery decline) не подтверждается в наших данных. Альтернативная interpretation: команды одинаково penalize injury risk вне зависимости от age, потому что прецедент injured young player создаёт ту же стратегическую неопределённость, что прецедент injured veteran.

## 5.7 Связь с литературой о shirking и contract-cycle dynamics

Наша event-study спецификация и H6 finding (awards effect через 2-3-year lag) пересекаются с более широкой литературой о shirking и contract-year (CY) syndrome в NBA, что заслуживает отдельного обсуждения.

Berri & Krautmann (2006) — первая NBA empirical работа, документирующая shirking-эффект через first-difference regression на post-signing change в performance: после подписания нового контракта observable performance metrics (особенно NBA Efficiency, PER-аналог) систематически снижаются, что интерпретируется как effort-substitution moral hazard. Authors показывают, что shirking-finding **sensitive к выбору productivity metric** (NBA Efficiency выявляет shirking, wins-based MRP — нет), что обосновывает наш methodological choice multi-metric Performance block (PPG + WS + BPM + VORP в M1c_full) как robustness против single-metric artifact.

White & Sheldon (2014) предлагают complementary psychological framing CY-эффекта через Self-Determination Theory: на 510 player-year observations (170 NBA-игроков × 3 measurement points pre-CY/CY/post-CY за 2003/04–2009/10) они документируют значимый pre-CY → CY scoring boost с последующим post-CY drop в 4 защитных метриках. Критично: они показывают, что **boosted CY scoring предсказывает post-CY salary raises** (b = 0.32 для PPG, b = 0.25 для PER, p < .01), то есть GM **награждают** CY-inflated performance, не distinguishing его от steady-state talent. Это даёт прямую интерпретацию нашего aging-veteran sub-finding (multi_all_nba ≥3 → β = −0.22): часть penalty может отражать post-CY undermining у veteran-stars, а не чистый survival bias.

Keefer (2021) предлагает методологически сильнейший identification: на DiD + IV setup с cap-spike 2016/17 как exogenous shock на player wages, он показывает, что cap-driven нестандартные wage increases влияют на post-signing playing time через sunk-cost-fallacy mechanism (GM "overplay" highly-paid players). Для нашей курсовой Keefer релевантен в двух аспектах: (а) **H4 interpretation** — наш post-CBA-2017 effect (+24.5%) частично — direct salary-cap spike эффект (Keefer's mechanism через 2016/17 reform), а не только designated-extension institutional layer; (б) **methodological antecedent** — Keefer's IV approach для cap-driven variation эксогенно identifying treatment, что обосновывает почему мы не делаем IV в нашей spec'е (cap-spike 2016/17 уже absorbed within sample 2015–2024 без out-of-sample control).

Совокупно: shirking + CY-syndrome литература создаёт important caveat для наших Mincer-style proxies. Текущая salary partly reflects boosted CY performance, не steady-state talent; lagged structure (lag1 для awards и durability) частично absorbs это, но полностью не устраняет (см. ограничение 4 в §5.8 Limitations).

## 5.8 Методологические ограничения и threats to internal validity

Несколько methodological caveats требуют explicit обсуждения.

**Oster (2019) δ-sensitivity** ограничена в нашем setup. Все $\delta < 1$ для key coefficients (§3.8.3), что в богатых-наблюдательных данных не означает робастности к OVB. Sign-стабильность подтверждена, magnitude чувствительна к спецификации; формальный $\delta$-based confidence interval не строится. Это — известная limitation метода Oster для panels с high $R^2$ baseline.

**Shapley R² — descriptive, не causal** (Lipovetsky & Conklin, 2001). Декомпозиция variance ≠ identification causal effects. Shapley даёт «справедливую» attribution explained variance, но не утверждает что блок $i$ causally определяет $\phi_i$ долю salary. Это accounting-style декомпозиция, полезная для priority ranking, но не для policy intervention design.

**TOT-attribution problem** (§3.2). Около 14% выборки получают NaN в team/market-зависимых спецификациях (игроки, поменявшие команду внутри сезона). Альтернативная импутация (взвешенная по доле игр) была рассмотрена и отвергнута; результаты H7 и H8 строятся на 2 268 obs из 3 660. Это потенциальный selection bias, но направление и магнитуда unknown; sensitivity к разным attribution схемам — future robustness work.

**Endorsement доход не наблюдается.** Маркетинговый доход NBA-звёзд может составлять до $30M/год для top players; этот компонент дохода полностью отсутствует в наших данных. Анти-marketability finding (H7) и aging-veteran sub-finding могут частично reflect substitution между observable salary и unobservable endorsement income. Identification причинного direction требует данных из Forbes Power 50 rankings или NBA jersey sales — оставляется на future work.

**Период замкнут на 2015/16–2023/24.** Выводы применимы к salary cap structure 2011–2017 + 2017–2023 CBA-эпохам. CBA 2023 с second apron и updated supermax thresholds может изменить dynamics; sample на 2023/24 включает первый год CBA 2023, но multi-year contracts подписанные ранее всё ещё под 2017 правилами. Полная оценка CBA 2023 эффекта — естественное направление для следующей итерации работы (с накоплением больше observations post-2023).

---


---

# Глава 6. Заключение

> Заменяет ранний драфт `chapter_6_conclusion.md` — там 10 потоковых гипотез; здесь те же выводы перегруппированы в 4 содержательных кластера + методологический вклад + ограничения.

---

## 6.1 Резюме исследования

В работе эмпирически исследован вопрос: **какие факторы и в какой пропорции определяют зарплату NBA-игрока в современной эпохе salary cap (post-2011 CBA)**. На самостоятельно собранной панели — 3 660 player-season за 2015/16–2023/24, 953 уникальных игрока, 153 переменных в 9 тематических блоках — построена расширенная функция заработной платы Mincer и применены три методологических инструмента: (а) decomposition объяснённой дисперсии $R^2$ по блокам факторов с использованием значения Шепли, (б) event study вокруг момента первого попадания в All-NBA, (в) wild-cluster bootstrap для проверки heterogeneity в подгруппах. Тест воспроизводимости предыдущей итерации проекта дал максимальное расхождение коэффициентов 5 × 10⁻⁵, что подтверждает корректность расширения базовой структуры данных.

Из 10 пред-сформулированных гипотез семь подтверждены при контроле multiple testing (BH-FDR @ 5%), три — отвергнуты или информативно нулевые. Главный новый результат — количественная иерархия факторов через Shapley-декомпозицию.

## 6.2 Главные содержательные выводы

Все эмпирические находки группируются в четыре содержательных кластера. Этот срез отвечает на тематический вопрос работы и формирует основу для возможных экономико-политических рекомендаций.

### Вывод 1. Mincer-ядро доминирует, но не настолько, как предполагала наивная Mincer-литература (поддерживает H1, H2, H4)

Performance и Age + Experience совокупно объясняют **65.5% дисперсии** $\ln(\text{salary})$ по Shapley-декомпозиции. Это соответствует классической Mincer-литературе (Mincer, 1974; Rosen, 1981) и устанавливает индивидуальный талант игрока как первый и доминирующий фактор. Возрастной пик зарплаты — 29.5 лет (95% CI: 28.4–30.6) — правдоподобен для NBA и согласуется с физиологическим peak performance.

Однако наивная sequential R²-декомпозиция в plan-order приписывает Performance 68.7% дисперсии — почти в два раза больше, чем Shapley. Это указывает на **значительную долю shared variance** между Performance и Awards / Durability / Tier-блоками, которая при честной (axiom-justified) атрибуции перераспределяется к этим блокам. Содержательный смысл: **CBA-структурирование** (tier-категории, awards-eligibility) и **survival-эффекты** (durability) являются не побочными факторами, а независимыми каналами формирования зарплаты, экономически и статистически отделимыми от Performance.

Структурный break после CBA 2017 — +24.5% к реальной зарплате — устойчив ко всем спецификациям и согласуется с известной литературой о реакции зарплат на cap-relaxation (Hill & Groothuis, 2001).

### Вывод 2. Институциональная иерархия — реальный второй слой формирования зарплат (поддерживает H3, H5, H6)

Tier-категория контракта одна объясняет **84.9% дисперсии $\ln(\text{salary})$** — больше, чем full Mincer-спецификация с 37 регрессорами (M1c_full: $R^2$ = 0.651). Это означает, что зарплата в NBA в значительной мере **детерминируется институциональной позицией** игрока в CBA-grid (minimum / mid-level / max-25 / max-30 / max-35 / supermax), а не непрерывной функцией от продуктивности.

$\beta_{\text{ppg}}$-коэффициент Performance внутри max_30-tier в 2.3 раза ниже, чем в mid_level — отчётливый **cap-truncation эффект**: верхний predel salary связывает зависимость от performance даже среди топ-игроков. Это эмпирическое уточнение классической работы Rosen (1986) о cap-induced concavity: cap создаёт не плавную concavity, а ступенчатую структуру salary distribution.

Канал наград работает с **2-3-летним лагом**: event study вокруг первого All-NBA selection показывает значимый jump зарплаты при $\tau = +2$ (+21%, p = 0.029) и $\tau = +3$ (+22%, p = 0.037), при отсутствии значимости в окрестности самого события. Это указывает на механизм **contract renewal cycle**: All-NBA признание переводится в зарплату не мгновенно, а через дискретное институциональное событие — переподписание контракта с применением правил designated extension. Уникальная находка работы — **anti-aging-veteran discount**: multi-time All-NBA игроки в декаданс-фазе (≥3 selections) несут penalty −19.7% против non-veteran All-Star, что объясняется survival-bias селектированием возрастных «легенд» с ухудшающимся текущим перформансом.

### Вывод 3. Окружение игрока не влияет на индивидуальную зарплату (поддерживает H7 anti-direction, H8 null, H9 null)

После контроля игроковых факторов (performance, age, awards, durability) окружающий контекст — рыночные характеристики команды, командные успехи, налог штата — **не имеет значимого эффекта** на индивидуальную зарплату. Все четыре командных контроля (win_pct_lag1, made_playoffs_lag1, playoff_round_reached, over_luxury_tax) дают p > 0.15; налог штата p = 0.29 (MDE = 21% pre-tax shift не достигается).

Парадоксальный результат для рынка: top-5 NBA cities (LAL, LAC, NYK, BRK, CHI, GSW) дают не премию, а **дисконт −9.3%** (p = 0.022). Heterogeneity-тесты с wild-cluster bootstrap отвергают marketability-канал — interaction × allstar не значима. Hembre (2022) даёт *theoretical channel*, совместимый с направлением нашего эффекта: при unrestricted free agency игроки требуют compensating differential за tax burden, что снижает spending power команд в high-tax штатах (CA, NY, IL — преимущественно где базируются top-5 NBA cities). Сам Hembre, однако, находит pooled effect на 4 лиги и сообщает, что NBA-specific coefficient статистически незначим ($\hat{\beta}_{\text{NBA}} \in [-0.143, -0.069]$, SE > 1.1, Table 3); поэтому мы не можем интерпретировать наш результат как direct confirmation Hembre, а только как consistent direction. Альтернативное объяснение — player-side **compensating differential** через off-court endorsement потенциал и lifestyle крупных рынков (примеры: LeBron 2018 → LAL под cap, Durant 2016 → GSW на 1+1) — не идентифицируется direct'ом в наших данных, но согласуется с revealed preference.

Совокупно: Market + Team + Structural + International объясняют по Shapley только **2.4% дисперсии**. NBA в post-2011 CBA — это **рынок индивидуального таланта**, а не рынок team revenue redistribution. Salary cap эффективно нейтрализует team-side market power.

### Вывод 4. Durability — реальный price discount (поддерживает H10)

Каждый пропущенный матч в прошлом сезоне снижает зарплату на 0.49%; за 30 пропусков — потеря −14.7%. Эффект устойчив (p < 0.001, проходит Bonferroni и BH-FDR). По Shapley декомпозиции durability даёт **5.7% объяснённой дисперсии** — больше, чем плановое ожидание (≈1%). Это указывает на то, что **рынок прайсит риск травм отдельно от текущей продуктивности**: 30-минутный matchup с травматизирующим противником не отражается в текущем PPG, но отражается в games_missed_lag1 и далее в следующем контракте.

## 6.3 Главный методологический вклад

**Shapley-декомпозиция объяснённой дисперсии по 9 блокам факторов** — наиболее значимый методологический вклад работы. В отличие от широко используемой sequential R²-декомпозиции, Shapley-аллокация удовлетворяет axioms эффективности, симметрии, dummy и аддитивности (Lipovetsky & Conklin, 2001) и поэтому даёт единственное «справедливое» распределение объяснённой дисперсии по блокам. На наших данных: эффективность axioma верифицирована до машинной точности ($|\sum_i \phi_i - R^2| \approx 1.4 \times 10^{-16}$).

Применение этого метода к labor-economics данным NBA даёт **количественный, axiom-обоснованный ответ** на исследовательский вопрос: «что и насколько определяет зарплату игрока». Sequential R² в plan-order, использовавшийся в более ранней литературе по NBA-salary (Hill & Groothuis, 2001), систематически завышает вклад performance-блока за счёт shared variance с awards / durability / tier; Shapley разрешает эту проблему теоретически чисто.

Дополнительные методологические вклады: применение wild-cluster bootstrap (MacKinnon & Webb, 2018) для inference в heterogeneity-тестах при малом числе кластеров; event-study спецификация вокруг первого All-NBA как способ идентифицировать contract-renewal-канал; интеграция rule-based contract tier classifier с CBA-правилами, валидированная на топ-30 игроках.

## 6.4 Ограничения

1. **Endorsement income не наблюдается.** Маркетинговый и эндорсмент-доход игроков (≈ $30 млн/год для LeBron) собран не был; marketability-канал идентифицирован только через residual selection. Это ограничивает причинный интерпретацию anti-marketability findings.

2. **TOT-attribution problem.** Игроки, поменявшие команду внутри сезона (≈ 14% выборки), получают NaN в team/market-зависимых спецификациях. Альтернативная импутация (взвешенная по доле игр) была отвергнута как расширяющая идентификационные предположения; результаты H7 и H8 строятся на 2 268 obs из 3 660.

3. **Oster δ-sensitivity ограничена.** Все δ < 1 для ключевых коэффициентов, что в богатых-наблюдательными переменными данных не означает робастности к OVB. Sign-стабильность подтверждена; magnitude чувствительна к спецификации.

4. **Rule-based tier classifier.** Категоризация контрактов основана на CBA-порогах с эвристическими допущениями (Rose Rule, ±5% pro-rate absorption). Полностью data-driven подход (через manual Coon-метки) был бы более строгим, но требует ручной разметки ≈ 2 268 строк.

5. **Период замкнут на post-2011 CBA.** Выводы применимы к salary cap structure 2011–2023 гг. CBA 2023 (с second apron) может изменить динамику; этот период в выборку не входит.

6. **Market vs tax channels не разложены direct'ом.** В нашей основной спецификации `no_income_tax` входит как бинарный structural контроль, а `top5_market` — как отдельный регрессор; continuous `state_tax_rate` не включён в joint M_full спецификации. Прямое разложение market-size channel vs tax compensating differential channel (через continuous state_tax_rate как control при top5_market) — естественная robustness check для будущей итерации.

## 6.5 Дальнейшие направления

1. **Two-sided matching model** для NBA: текущий анализ редуцирован к hedonic regression; полная structural модель учла бы выбор команды игроком и наоборот.
2. **Endorsement-augmented Mincer**: пополнение datasets по эндорсмент-доходам (Forbes Power 50, NBA jersey sales rankings) позволит decompose marketability vs salary каналы напрямую.
3. **CBA 2023 second-apron event study**: новые ограничения для over-luxury-tax команд создают natural experiment для testing того, ослабляет ли salary cap элиту-команд (warrying-tax dynamics).
4. **Counterfactual cap simulation**: что произошло бы с distribution salary, если бы cap-правила были отменены? Это можно simulate в structural model on calibrated parameters.

## 6.6 Финальное утверждение

Зарплата NBA-игрока в эпоху post-2011 CBA — это **в 65% случаев Mincer-функция** от продуктивности и возрастной траектории, **в 32% — институциональная категоризация** через award-eligibility, contract-tier и health record, и **менее 3% — окружающий контекст** (market size, team success, налоги). Salary cap эффективно нейтрализует team-side market power, превращая bargaining в выбор **типа** контракта в пределах CBA-grid, а не непрерывный price-setting процесс.

Насколько нам известно, это первое исследование, которое **количественно и через axiom-обоснованную декомпозицию** разлагает дисперсию зарплат NBA на блоки факторов на данных современного CBA-режима.

---


---

# Декларация использования инструментов искусственного интеллекта


---

## Использованные инструменты

В ходе подготовки данной курсовой работы автор использовал следующие инструменты искусственного интеллекта на основе больших языковых моделей:

- **Claude (Anthropic)** — версии Sonnet 4.6, Opus 4.7 (1M context), Haiku 4.5 — через интерфейсы Claude Code (CLI и VS Code extension) и веб-приложение Claude.ai.
- Других AI-инструментов (GPT-4, Gemini, Copilot и т. п.) не использовалось.

## Виды задач, в которых AI применялся

AI применялся как инструмент-ассистент в следующих категориях задач:

**(1) Программная реализация (assistant role).** Написание Python-скриптов для:
- скрейпинга Basketball-Reference и Hoopshype с обходом Cloudflare TLS-fingerprint;
- merge-операций между блоками данных с safe-join проверками;
- эконометрических спецификаций на основе `statsmodels` и `linearmodels`;
- Shapley R²-декомпозиции (генерация всех $2^9 = 512$ subset-фитов);
- cluster bootstrap, wild-cluster bootstrap и event study спецификаций;
- генерации matplotlib / seaborn визуализаций.

Весь сгенерированный код был запущен, его выводы (коэффициенты, p-values, R²) сравнены с независимыми расчётами в R (для v1-итерации) и с теоретическими ожиданиями (efficiency axiom для Shapley, hash-snapshot reproducibility test для v1 panel). Регресс-тест воспроизводимости подтверждает, что числовые результаты идентичны независимым расчётам с точностью до 5 × 10⁻⁵.

**(2) Литературное оформление (drafting role).** Подготовка драфтов аналитических заметок (`analysis_v2/reports/*.md`), разделов глав, аннотации и итогового conclusion. Все драфты были вычитаны автором; стиль, структура аргументов, выбор формулировок и финальная редактура — за автором.

**(3) Структурирование гипотез.** Синтез H1–H10 из исходных гипотез v1 (4 шт.) и v2 (4 шт.) с группировкой по 5 research streams. AI помог в формальном изложении и mapping на конкретные спецификации; концептуальная связь гипотез с литературой и тематическим вопросом работы — за автором.

**(4) Документирование.** Заполнение reports markdown-файлов, генерация tables (CSV), оформление figures.

## Виды задач, в которых AI НЕ участвовал

- **Постановка исследовательского вопроса.** Тема и research question сформулированы автором до начала работы.
- **Выбор источников данных и периода.** Решения о работе с Basketball-Reference + Hoopshype, о выборе сезонов 2015/16–2023/24, о структуре 7 новых блоков данных — приняты автором на основе плана `plan3.md`.
- **Содержательная интерпретация результатов.** Все экономические интерпретации в Главе 5 (Дискуссия) и Главе 6 (Заключение) — оригинальные авторские выводы, основанные на знании литературы. AI помогал в литературном оформлении, но не в концептуальной интерпретации.
- **Методологические решения.** Выбор Shapley vs Sequential R², решение использовать wild-cluster bootstrap, выбор Oster (2019) для OVB-sensitivity — приняты автором на основе изучения соответствующей литературы.
- **Подбор и оценка цитированных источников.** Список литературы и оценка релевантности каждого источника к конкретным гипотезам — за автором, в сотрудничестве с коллегой (см. `bibliography/`).

## Верификация AI-сгенерированных результатов

Применены следующие процедуры независимой проверки:

1. **Регресс-тест воспроизводимости v1**: запуск всех v1-спецификаций (M1a–M1d) на расширенном v2-датасете показывает максимальное расхождение коэффициентов с опубликованной v1-итерацией < 5 × 10⁻⁵. Это исключает гипотетическое введение AI-артефактов в базовые соотношения.

2. **Аксиоматическая проверка Shapley R²**: efficiency property $\sum_i \phi_i = R^2_{\text{full}}$ верифицирована численно до машинной точности (диф. 1.4 × 10⁻¹⁶); это математическое равенство, выполнение которого исключает реализацию-зависимые ошибки.

3. **Hash-snapshot датасетов**: SHA256 v1-panel зафиксирован в `analysis_v2/reports/v1_snapshot.sha256` и проверяется при каждой пере-сборке.

4. **Sample-size и degrees-of-freedom**: для каждой регрессионной таблицы число наблюдений и регрессоров проверено и согласуется с теоретическим расчётом (см. §4.2).

5. **Параллельный счёт ключевых коэффициентов в R**: спецификации M1a, M1c, M2c независимо запущены в R (`scripts/*.R`) и сравнены с Python-версиями.

## Открытый исходный код

В целях обеспечения воспроизводимости и прозрачности AI-использования весь исходный код, сырые данные, промежуточные таблицы и markdown-драфты размещены в публичном репозитории GitHub:

**https://github.com/outofcost/CourseProject**

Репозиторий включает:
- Полный пайплайн от scraping до figure generation (`analysis_v2/` package);
- Регресс-тест воспроизводимости (`analysis_v2/regress_test_v1.py`);
- Hash-snapshots датасетов;
- Контекстный файл `CLAUDE.md` для AI-инструментов;
- Markdown-драфты всех аналитических заметок.

Любой исследователь может воспроизвести все числовые результаты работы за ≈ 3 минуты на теплом кэше или ≈ 2 часа на холодном.

## Intellectual responsibility

Автор сохраняет **полную ответственность** за содержание работы. Все экономические интерпретации, выбор гипотез, методологические решения и содержательные выводы являются результатом авторского анализа. AI-инструменты использовались исключительно как ассистент для рутинных задач (code generation, drafting, formatting), а все critical decisions и interpretations верифицированы и подтверждены автором.

В случае обнаружения ошибок или artifacts в сгенерированном коде или текстах ответственность лежит на авторе, а не на AI-инструменте.

---

**Подпись автора:** {Karolina303}
**Дата:** {YYYY-MM-DD финальная дата защиты}

---


## Список литературы

См. отдельный файл `bibliography/references.bib` (BibTeX) и `bibliography/MASTER_TABLE.md` (читаемый список с приоритетами). Финальный APA-bibliography текстом будет добавлен в Phase F при сборке .docx.

---

## Приложения

- **Приложение A.** Расширенные регрессионные таблицы — см. `analysis_v2/output/tables/` (30+ CSV-таблиц).
- **Приложение B.** Описательная статистика по выборке — см. `analysis_v2/output/tables/descriptive_stats.csv`.
- **Приложение C.** Hash-snapshots датасетов и регресс-тест воспроизводимости — см. `analysis_v2/regress_test_v1.py` и репозиторий.
- **Приложение D.** AI-coordination evidence: `coordination/` файлы (PROTOCOL, TASKS, FOR_*, MASTER_PLAN, findings_log) как audit trail двух Claude-инстансов.
