# Глава 4 — новые разделы (Результаты)

Драфт разделов 4.5–4.10 курсовой. Реорганизация **по факторам, а не по моделям** (per plan3.md). Каждый раздел — самостоятельный story, выводит один substantive finding.

---

## 4.5 Рыночный фактор (H8): null vs anti-marketability

### 4.5.1 Гипотеза

H8: игроки в крупных медиа-рынках (top-5 NBA cities по DMA) получают премию через два канала — (а) marketability premium (off-court endorsement potential), (б) bargaining premium (большие команды чаще near luxury tax line).

### 4.5.2 Результаты

Спецификация M8a (M1c + top5_market) даёт:

$$\hat\beta_{\text{top5}} = -0.098, \quad \text{SE} = 0.043, \quad p = 0.022$$

**Знак отрицательный и статистически значим** (BH-FDR @ 5% проходит). Игроки в top-5 рынках зарабатывают **на 9.3% меньше** при контроле performance, age, awards, durability. M8b с непрерывной переменной `market_size_rank_nba` подтверждает направление (β = +0.004 на единицу ранга; больший ранг = меньший рынок = выше salary).

### 4.5.3 Heterogeneity тесты

M8c (top5 × allstar): interaction β = +0.157, wild-cluster CI95 = [−0.198, +0.194] — **не значимо**. Marketability-гипотеза предсказывала бы более сильный дисконт для звёзд (они могут компенсировать через endorsements), но данные этого не подтверждают.

M8d (top5 × is_international): interaction β = +0.058, wild-cluster CI95 = [−0.237, +0.233] — не значимо.

### 4.5.4 Интерпретация

Дисконт ~10% применяется **равномерно ко всем игрокам** в top-5 рынках, без heterogeneity по звёздности или происхождению. Это согласуется с **Hembre (2021)**: в эпоху salary cap правила игры исключают monopolistic surplus extraction командой; market-size премия экономически не реализуется.

Anti-marketability направление эффекта объясняется через **selection on revealed preferences**: топ-игроки (LeBron 2018→LAL под cap, Durant 2016→GSW на 1+1, и т.д.) сознательно жертвуют ~$5-10M зарплаты ради большего рынка / off-court дохода / lifestyle. Это compensating differential, не поддающийся прямой эконометрической идентификации, но проявляющийся в residual дисконте top5_market.

**H8 — частично подтверждена, но с обратным знаком**: премии нет, есть дисконт. Marketability как механизм отвергнут (нет heterogeneity); selection-эффект на rev. preferences — единственное объяснение, совместимое с данными.

---

## 4.6 Структура контракта (H9): институциональный слой

### 4.6.1 Гипотеза

H9: tier контракта объясняет существенную часть salary вариации, недетерминируемую через текущий performance. Max-контракт — это **institutional category**, а не функция от PPG.

### 4.6.2 Результаты

| Спецификация | R² |
|---|---|
| M1c_full (Performance + Age + Demo + Awards + Durability + Team + Market) | 0.651 |
| **M9a** — pure tier dummies, без performance | **0.849** |
| **M9b** — M1c + tier dummies | **0.862** |
| ΔR² от tier поверх M1c | **+0.21** |

**Tier dummies одни объясняют 85% дисперсии ln(salary)** — больше, чем full M1c-спецификация с 37 регрессорами. Performance metrics добавляют только +1.3 пп R² поверх tier.

### 4.6.3 Tier-эффекты (M_full, reference = mid_level)

| Tier | β | p | Интерпретация |
|---|---|---|---|
| **minimum** | **−0.905** | <0.001 | minimum-contract игроки на 60% ниже mid_level (e^{-0.91} = 0.40) |
| rookie_scale | −0.088 | 0.051 | rookie-scale близок к mid_level |
| high_mid | +0.301 | <0.001 | high_mid +35% над mid_level |
| **max_25** | **+0.811** | <0.001 | +125% |
| **max_30** | **+1.001** | <0.001 | +172% |
| **max_35** | **+1.279** | <0.001 | +260% |
| **supermax** | **+1.188** | <0.001 | +228% |
| overpay | +0.40 | (n=10, low power) | residual category |

Иерархия tier'ов **монотонна и почти-детерминистична**. Salary внутри tier практически фиксирована институциональными правилами CBA.

### 4.6.4 Tier-specific Mincer-регрессии (cap-truncation pattern)

β_ppg внутри каждого tier'а:

| Tier | n | β_ppg | p | R²_within |
|---|---|---|---|---|
| minimum | 307 | +0.093 | 0.004 | 0.42 |
| rookie_scale | 484 | +0.094 | <0.001 | 0.31 |
| **mid_level** | 717 | **+0.078** | 0.017 | 0.46 |
| high_mid | 442 | +0.071 | <0.001 | 0.47 |
| max_25 | 209 | +0.068 | 0.001 | 0.49 |
| **max_30** | 50 | **+0.034** | 0.012 | 0.49 |
| supermax | 33 | +0.067 | 0.001 | 0.67 |

В max_30 β_ppg падает **в 2.3 раза** по сравнению с mid_level — отчётливый **cap-truncation эффект**. В supermax β_ppg обратно растёт, но это в значительной мере артефакт нелинейности (внутри supermax есть градация по cap-share — Curry > Lillard > Booker).

В rookie_scale и minimum β_ppg формально высок, но это потому что эти tier'ы включают неоднородные группы (топ-пик vs late-первый-раунд; min-зарплата зависит от experience). Cap-truncation в верхнем хвосте — это надёжная находка.

### 4.6.5 Интерпретация

**H9 подтверждена.** Salary в NBA — это во много большей мере **функция от категориальной позиции в CBA-структуре**, чем от непрерывного performance. Performance ↔ salary связь работает через institutional bridge: PPG → All-Star/All-NBA selection → tier eligibility → discrete jump в зарплате.

Это содержательное обобщение Rosen (1986) о cap-induced concavity: cap создаёт не просто плавную concavity, а **ступенчатую структуру** salary distribution.

---

## 4.7 Awards channel (H10): пост-event premium

### 4.7.1 Гипотеза

H10: All-NBA selections значимо повышают зарплату даже при контроле текущей performance — это premium за «verified elite» статус, формализованный supermax-criteria.

### 4.7.2 M10a и robust-spec

| Регрессор | β (M10a) | p | β (robust) | p |
|---|---|---|---|---|
| all_nba_lag1 | **+0.185** | 0.008 | +0.159 | 0.044 |
| career_all_nba_count | −0.045 | 0.018 | — | — |
| career_allstar_count | **+0.122** | <0.001 | — | — |
| has_career_all_nba | — | — | +0.025 | 0.79 |
| **has_career_allstar** | — | — | **+0.331** | <0.001 |
| **multi_all_nba** | — | — | **−0.220** | 0.038 |

**Чистый result:**
- All-NBA в предыдущем сезоне (`all_nba_lag1`): **+20.3% (e^{0.185})** к зарплате после контроля текущей performance.
- Бывший All-Star (`has_career_allstar`): **+39.2%** premium — гигантский эффект.
- Multi-time All-NBA (≥3 selections): **−19.7%** discount — aging-veteran effect.

Net effect для текущей All-NBA звезды (Curry, LeBron): +20.3% + 39.2% − 19.7% ≈ **+40%**. Для бывшей звезды на декаданс-контракте (Carmelo, Wade поздних лет): −19.7% + 39.2% = **+19.5%** (премия меньше, но не отрицательная).

### 4.7.3 Event study вокруг первого All-NBA

Динамика salary относительно года первого All-NBA в карьере:

| τ | β | 95% CI | Значимость |
|---|---|---|---|
| −2 | −0.21 | [−0.54, +0.12] | p = 0.21 (нет anticipation) |
| −1 | −0.15 | [−0.47, +0.16] | p = 0.34 (pre-trend чистый) |
| 0 | −0.24 | [−0.51, +0.03] | p = 0.08 (текущий контракт не реагирует) |
| +1 | +0.17 | [−0.04, +0.37] | p = 0.11 (частичный bump) |
| **+2** | **+0.21** | [+0.02, +0.40] | **p = 0.029** |
| **+3** | **+0.22** | [+0.01, +0.43] | **p = 0.037** |
| ≥4 | −0.11 | [−0.33, +0.11] | p = 0.33 (затухание) |

**Чистая contract-cycle dynamics:** salary не реагирует мгновенно на All-NBA, а **скачет на 22% через 2-3 года** — когда подписывается следующий контракт. Эта картина прямо иллюстрирует механизм H10: awards переводятся в зарплату через discrete institutional event (new contract negotiation), а не непрерывно.

### 4.7.4 Интерпретация

**H10 подтверждена.** Awards channel работает через два слоя: (а) immediate effect через all_nba_lag1 в M1c-full (=+20%); (б) delayed effect через contract renewal cycle (=+22% при τ=+2, +3). Negative coefficient на multi_all_nba — это уникальная находка работы: aging-vet penalty при контроле age и performance.

В сочетании с H9: 12.2% explained variance (по Shapley) для Awards block — больше, чем Demographics (14.1%) при подобном содержательном весе.

---

## 4.8 Durability (H11)

### 4.8.1 Результаты

| Спецификация | β_{games_missed_lag1} | SE | p |
|---|---|---|---|
| M11a (main) | **−0.0049** | 0.0011 | <0.001 |
| M11b (× age interaction) | β_main = −0.0010, β_int = −0.0004 | — | 0.12 |

Каждый пропущенный матч в прошлом сезоне снижает зарплату на **0.49%**. За 30 пропусков (тяжёлая травма) = **−14.7%** к salary — экономически и статистически значимый эффект (BH-FDR pass, Bonferroni pass).

Interaction `games_missed × age` не значима (p = 0.12). Гипотеза «травмы стоят больше для стареющих игроков» не подтверждается на нашей выборке.

### 4.8.2 Интерпретация

**H11 (main) подтверждена.** Durability — реальный price discount. Это **уникальная находка** работы, потому что v1 моделей не включали games_missed как контроль. По Shapley декомпозиции durability даёт **5.7% explained variance** — больше плановых 1% ожиданий.

---

## 4.10 Декомпозиция вариации salary (главный новый раздел)

### 4.10.1 Подход

Два метода декомпозиции `R² ≈ 0.65` на блоки факторов:

1. **Sequential R²**: блоки добавляются в фиксированном порядке, ΔR² на каждом шаге + 95% cluster-bootstrap CI.
2. **Shapley R²**: order-independent attribution через формулу Shapley (1953), 2⁹ = 512 subset-фитов.

### 4.10.2 Shapley декомпозиция (главная таблица)

| Блок | Shapley R² | Доля объяснённой дисперсии |
|---|---|---|
| Performance (ppg/rpg/apg/per/ws/vorp/usg/mpg/gp) | 0.239 | **36.8%** |
| Age + Experience | 0.186 | **28.7%** |
| Demographics (allstar, undrafted, log_draft_pick, pos_*) | 0.091 | **14.1%** |
| Awards (all_nba_lag1, career_all_nba_count, career_allstar_count) | 0.079 | **12.2%** |
| Durability (games_missed_lag1, games_missed_3y_cum) | 0.037 | **5.7%** |
| International (born_*) | 0.005 | 0.8% |
| Team (win_pct_lag1, made_playoffs_lag1, over_luxury_tax) | 0.005 | 0.8% |
| Structural (post_cba_2017, post_covid, no_income_tax) | 0.004 | 0.6% |
| Market (top5_market) | 0.001 | 0.2% |
| **Total (= R²_full)** | **0.649** | **100.0%** |

Проверка: `sum(shapley) = 0.6488 = R²_full` (efficiency property выполнена с точностью до 1e-10).

### 4.10.3 Sequential vs Shapley (order-dependence diagnostic)

| Блок | Sequential (plan-order) | Sequential (reverse) | Shapley |
|---|---|---|---|
| Performance | 0.446 | 0.115 | 0.239 |
| Age | 0.169 | 0.139 | 0.186 |
| Demographics | 0.013 | 0.083 | 0.091 |
| **Awards** | **0.006** | **0.199** | **0.079** |
| Structural | 0.004 | 0.003 | 0.004 |
| Market | 0.001 | 0.000 | 0.001 |
| Team | 0.002 | 0.010 | 0.005 |
| Durability | 0.004 | 0.093 | 0.037 |

Sequential R² **сильно зависит от порядка**: Awards «съедает» 30% при первом добавлении (потому что коррелирован с Performance), но даёт всего 0.6% при добавлении пятым. **Shapley** разрешает эту неопределённость, давая Awards **12.2%** — устойчивую долю.

### 4.10.4 Содержательные выводы

1. **Performance + Age = 65.5%** explained variance — Mincer-ядро **доминирует**.
2. **Awards + Demographics + Durability = 32%** — институциональный/контекстный слой имеет реальный вес, не шум.
3. **Market + Team + Structural + International = ~2%** — после контроля игрока, **окружение почти не влияет на цену**.

Это эмпирическое подтверждение того, что **NBA в эпоху salary cap — это рынок индивидуального таланта**, а не рынок team revenue redistribution. Этот вывод напрямую отвечает на вопрос темы курсовой работы: что и насколько определяет зарплату NBA-игрока.
