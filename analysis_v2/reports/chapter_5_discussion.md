# Глава 5 — Дискуссия (драфт v2)

Реорганизация параллельно Главе 4: каждый раздел дискуссии соответствует разделу результатов. Главное новое содержание — обсуждение декомпозиции вариации, market premium null, tier truncation, supermax-eligibility как формального канала awards-механизма.

---

## 5.1 Декомпозиция вариации: что определяет зарплату NBA?

Главная контрибуция работы — **количественная иерархия факторов** salary determination. Shapley-декомпозиция даёт следующую картину:

- **Mincer-ядро (Performance + Age) = 65.5% explained variance.** Это совершенно ожидаемо в эффективном рынке труда: продуктивность игрока и его career arc — фундаментальные детерминанты.
- **Institutional layer (Awards + Demographics + Durability) = 32%.** Здесь главный новый результат: формальные achievements (All-NBA, All-Star history) и измеримый health-history имеют **сравнимый вес** с raw performance metrics.
- **Environmental controls (Market + Team + Structural + International) = ~2.4%.** Surrounding context почти не влияет на индивидуальную цену.

### 5.1.1 Что это значит для модели рынка труда NBA

Стандартный Rosen (1981) "superstar economics" предсказывает, что в продуктовом рынке с returns-to-scale (TV revenue, merchandise) топ-таланты получают непропорциональную долю общей wage bill. Наши данные показывают, что **продуктовый канал работает не через market-size премию или team-revenue redistribution**, а через **institutional channeling**: cap создаёт price tiers, awards дают официальный elite status, и top players попадают в верхние tiers через формальные критерии (supermax, designated rookie extension).

Это **в значительной степени отличает NBA от литературы по другим спортам**: где Berri & Schmidt (2010) показывали для MLB заметную market-size премию ~5%, в NBA эпохи post-2011 CBA этой премии нет. CBA правила, видимо, нейтрализуют рыночные differences (revenue sharing + tax penalties).

### 5.1.2 Order-dependence как методологическая повестка

Sequential R² и Shapley **сильно расходятся** для Awards block (0.6% vs 12.2%) и Durability (0.4% vs 5.7%). Это **не баг, а feature**: показывает, что значительная часть signal в Awards и Durability **корреляционно связана с Performance**. Раннее добавление Performance «съедает» эту общую вариацию.

Shapley разрешает неопределённость через axiomatic approach (efficiency + symmetry + dummy + additivity). Мы следуем рекомендации Lipovetsky & Conklin (2001) и используем Shapley как **главную** декомпозицию, Sequential — как иллюстрацию order-sensitivity.

Этот выбор открыт для критики: Shapley предполагает, что атрибуция должна быть "fair" в Shapley-теоретическом смысле, но не отражает causal pathway. Альтернативный подход — Pratt (1987) или Genizi (1993) approaches — даёт похожие, но не идентичные результаты. Для курсовой Shapley достаточен.

---

## 5.2 Market premium: anti-marketability и проблема selection

H8 ожидаемо была **информативным null**: marketability-гипотеза не подтверждена. Более того, обнаружен **negative coefficient β = −0.098** на top5_market — игроки в крупных рынках получают **дисконт ~9%**, а не премию.

### 5.2.1 Hembre (2021) как реferential anchor

Hembre (2021) на CBA-эпохе данных показал, что market-size премии **не должно быть** — потому что revenue sharing и луксури-tax penalties делают марджинальную revenue от больших рынков нулевой для команды. Наш результат сильнее: дисконт.

### 5.2.2 Что объясняет дисконт?

Marketability-канал (off-court endorsements компенсируют меньшую зарплату для marketable игроков) **предсказывал бы heterogeneity**: дисконт должен быть сильнее у звёзд. Однако M8c (top5 × allstar) interaction NOT significant (wild-CI охватывает 0). Marketability — отвергнут как механизм.

**Selection on unobserved preferences** остаётся единственным согласованным объяснением: top-игроки **сознательно** жертвуют зарплатой ради больших рынков. Известные кейсы:
- LeBron James → LAL 2018: $35.7M vs предложенные Houston/Philadelphia $40+M;
- Kevin Durant → GSW 2016: 1+1 deal стартующий с $26.5M vs возможные $30M+ длинного max;
- Kawhi Leonard → LAC 2019: cap-flexible deal под Paul George trade;
- Anthony Davis → LAL 2019 (trade);

Эта **revealed preference** capturing the welfare component (off-court income, lifestyle, training, family) не идентифицируется без endorsement income data. Forbes Highest-Paid Athletes list для top-15 NBA-игроков мог бы дать эту проверку, но coverage ограничен (приоритет 3 по плану).

### 5.2.3 Методологическое замечание

Наш дисконт не противоречит Hembre (2021); он **достраивает** его: cap-нейтрализованная team-side премия + **player-side compensating differential для off-court income** = net negative observed coefficient.

---

## 5.3 Tier-структура: institutional pricing как механизм

### 5.3.1 Главный quantitative result

**Tier dummies одни объясняют R² = 0.85**, против R² = 0.65 для full Mincer-спецификации. Это значит, что **classification of contracts** содержит больше информации о salary, чем все performance metrics вместе взятые.

Это содержательно невозможно интерпретировать как "tier causes salary": tier и salary co-determined через CBA rules. Salary → tier classification, но также tier → salary cap (CBA пороги). **Эта эквивалентность сама по себе является finding**: salary в NBA — это не функция от player attributes, а функция от **классификационного решения** в момент подписания контракта (через какую CBA-нишу игрок подписывается).

### 5.3.2 Cap-truncation в верхнем хвосте

Tier-specific β_ppg показывает классический truncation pattern:

- mid_level β_ppg = +0.078 (рыночная зона) ✓
- max_25 β_ppg = +0.068 ✓
- **max_30 β_ppg = +0.034** — truncation in evidence ✓
- supermax β_ppg = +0.067 (внутри supermax есть градация: Curry > Booker)

В max-tiers cap rules ограничивают верхний потолок зарплаты, поэтому **дополнительная единица PPG не переводится в дополнительную зарплату** — она "просто" подтверждает уже-достигнутый max status. Это прямая иллюстрация cap-induced concavity Rosen (1986), но в **дискретной форме**.

### 5.3.3 Supermax-eligibility как формальный канал

Supermax-eligible_loose в одиночку не значим в M_full (β = +0.078, p = 0.19) — потому что eligible-статус **уже инкорпорирован** в tier classification (supermax tier requires eligibility). Tier_supermax × eligible interaction — perfect collinearity, дропается.

Это правильно: CBA правила institutionalize the awards channel. Игрок получает supermax-tier salary **не "потому что All-NBA"**, а **через formal pathway**: All-NBA → eligibility → designated extension → supermax-tier salary.

### 5.3.4 Институциональная интерпретация

Это **прямой контр-аргумент** против стандартной trader-style модели «player-team bargaining». В NBA bargaining происходит **в пределах строгой институциональной grid'ы**: игрок и команда выбирают **тип** контракта (rookie scale / MLE / max), а внутри типа salary почти-детерминирована. Это ближе к **two-sided matching** model (Roth-Sotomayor), где категории контрактов — это типы matches, и individual prices внутри категории жёстко привязаны к cap-share.

---

## 5.4 Awards channel: timing и aging-vet penalty

### 5.4.1 Immediate vs delayed effect

H10 поддерживает **two-stage awards channel**:

1. **Immediate** (M1c-full): all_nba_lag1 β = +0.185 (p = 0.008). Получение All-NBA в прошлом сезоне → +20% к зарплате.
2. **Delayed** (event study): τ = +2, +3 → β = +0.21, +0.22. Salary jumps **через 2-3 года** после первого All-NBA — когда подписывается новый контракт.

Эти две оценки **согласуются**: immediate β = 20% — это смесь "уже на новом контракте" игроков (τ ≥ 2 эффект) и "ещё на старом контракте" игроков (τ = 0, 1 — где effect близок к нулю). Event study декомпозирует среднее в timing-структуру.

### 5.4.2 Aging-veteran discount

Уникальная находка работы — **multi_all_nba (≥3) coefficient = −0.22** в M1c_full_robust. Это значит: для игроков с 3+ All-NBA selections в истории salary **ниже** на 20% при контроле текущей performance.

**Содержательная интерпретация**: в нашу выборку (gp ≥ 20, mpg ≥ 5) попадают активные игроки. Среди ветеранов с большим списком наград — Carmelo Anthony 2018/19 (Houston, $2.4M; затем Portland minimum), Dwyane Wade 2018/19 (Miami, $2.4M ringer), Pau Gasol 2018/19 (San Antonio buyout), Vince Carter поздних лет. Эти игроки **уже на минимум-контрактах**, потому что их productivity в декаданс не оправдывает high-tier salary.

multi_all_nba → 1 для этих игроков, и их минимум-контракты "тянут" coefficient в отрицательную зону. Это **survival bias**: те же multi_all_nba игроки, которые ещё на peak (Curry, LeBron, Durant) тоже в выборке, но они в supermax-tier с **очень высокой** salary. Net average across both groups gives negative β.

### 5.4.3 Альтернативные спецификации

В robust spec с binary indicators:
- has_career_allstar = +0.331 (single-time elite premium)
- multi_all_nba = −0.220 (multi-time post-prime penalty)

Net для "current star": +0.33 ≈ +39%; net для "aging legend": +0.33 − 0.22 = +0.11 ≈ +12%. Иерархия согласована со здравой интерпретацией.

---

## 5.5 Durability: реальный price discount

H11 main effect: games_missed_lag1 = −0.005 (p < 0.001). Каждый пропущенный матч в прошлом сезоне снижает зарплату на 0.5%; 30 пропусков = −15%. Bonferroni-pass.

Shapley даёт durability **5.7% explained variance**, против плановых 1%. Это значит, что **health-history** игрока имеет содержательный вес — больше, чем market/team/structural блоки вместе взятые.

Interaction `games_missed × age` не значима (p = 0.12). Гипотеза "стареющие игроки штрафуются больше" не работает — возможно, потому что для них **base salary уже ниже** (через age и age² controls), и абсолютный эффект пропусков не масштабируется.

---

## 5.6 Team controls null: индивидуальная цена ≠ team success

Все три team-level контроля (`team_win_pct_lag1`, `team_made_playoffs_lag1`, `team_over_luxury_tax_t`) — **null** (p > 0.15 во всех спецификациях). Это значит:

1. Игроки в успешных командах **не получают премию** сверх своих individual attributes.
2. Команды, готовые платить luxury tax, **не платят дополнительно** indivudual игрокам — они просто содержат больше дорогих игроков.
3. `made_playoffs_lag1` slightly negative — намёк на «команды, регулярно пропускающие плей-офф, могут переплачивать ради улучшения», но не значимо.

**Институциональная интерпретация**: индивидуальная цена игрока в NBA определена через CBA tiers, **не через team's бенефит от него**. Это согласуется с tier-structure finding: если salary почти-детерминирован cap-share категорией, team-specific context не имеет места.

---

## 5.7 Ограничения и направления дальнейших исследований

### 5.7.1 Ограничения данных

- **Endorsement income** не наблюдается. Forbes Highest-Paid Athletes list мог бы дать прокси для топ-10 игроков, но coverage ограничен.
- **Agent / agency** данные не собраны (priority 3 по плану). Klutch / CAA / Excel concentration влияния на bargaining не идентифицирована.
- **Contract structure** — мы наблюдаем только current-season salary, не multi-year deal structure (player options, ETOs, trade kickers). H10 event study частично компенсирует через timing-эффект.

### 5.7.2 Ограничения спецификации

- **TOT-rows** (~14% выборки) с pseudo-team `2TM/3TM/4TM` теряются в спецификациях с market_size и team controls. Альтернативная стратегия — weighted attribution — рассматривалась, но требует доп. предположений.
- **Oster δ-sensitivity** все < 1 — это **ожидаемо** для домена с богатыми observables, но означает, что **magnitude каждого β** чувствительна к спецификации. Sign-stability подтверждена, размер — open question.
- **Tier classification** rule-based, не data-driven. Возможна валидация через ручную разметку контрактов из Coon CBA FAQ (priority 4, time-intensive).

### 5.7.3 Дальнейшие направления

1. **Structural model** salary determination как two-sided matching (game-theoretic) — расширение Rosen 1981 + Roth-Sotomayor matching, для NBA-CBA.
2. **Endorsement-augmented Mincer**: с jersey sales / social media followers / Forbes income данных — для прямого теста marketability-канала.
3. **CBA-event analysis**: 2023 CBA introduced second apron — позволяет identify дополнительные shifts в tier behavior.
4. **Counterfactual simulation**: убрать cap-rules и предсказать, как изменится distribution salary — для оценки welfare loss/gain от institutional structure.

---

## 5.8 Финальный итог

Курсовая работа эмпирически устанавливает, что **NBA salary в эпоху post-2011 CBA — это primarily функция от individual performance (37%) и career arc (29%), модулированная institutional channelling через awards (12%) и contract tiers (overall structural effect)**. Окружающий контекст (market, team, macro structure) объясняет менее 3% дисперсии после контроля игрока.

Это согласуется с **Hembre (2021) null on market**, отвергает **Rosen-style market-size premia** для современного NBA, и устанавливает **cap-truncation pattern** в tier-specific β_ppg, прогнозируемый Rosen (1986).

Главный методологический вклад — **Shapley R² decomposition** как order-independent ответ на вопрос темы. Это масштабируемо к другим спортам и трудовым рынкам с rich observables.
