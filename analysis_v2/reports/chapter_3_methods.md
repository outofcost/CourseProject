# Глава 3. Данные и методология

> Драфт под HSE term paper, Article (Empirical) format. Объём: ≈ 25% работы (целевые ~3000 слов).
> Цитирования — APA. Источники, помеченные [TBD], уточняются после получения полных текстов от коллеги (см. `bibliography/`).

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

Дополнительно — tier-specific Mincer-регрессии: восемь отдельных регрессий $\ln(\text{salary}) \sim \text{Stats} + \text{Age}$ на подвыборках по tier. Тестируется cap-truncation: ожидаемо, что $\beta_{\text{ppg}}$ в max-tiers ниже, чем в mid-level (Rosen, 1986; [TBD]).

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

На interaction-коэффициентах M8c и M8d применяется wild-cluster bootstrap (Rademacher weights, 1000 реплик; MacKinnon & Webb, 2018) с restricted null-моделью — для робастной инференции при малом числе кластеров «top5 × allstar» (Cameron et al., 2008).

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

При тестировании 10 гипотез H1–H10 (см. §2 [TBD: финальная нумерация в Lit Review]) с одиннадцатью ключевыми коэффициентами (некоторые гипотезы тестируются несколькими спецификациями) применяются две процедуры:

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

[Слов в главе: ≈ 3 200; ссылок APA: 12 шт., все базовые; цели по объёму — выполнены]
