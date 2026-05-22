Хорошо, переходим в режим рабочего плана. Делаю его так, чтобы каждый блок можно было выполнять как отдельную задачу — с источниками, ожидаемыми объёмами, спецификациями и оценкой трудозатрат.План построен под ~5 недель работы (25 рабочих дней) — это реалистичный таймлайн для серьёзной доработки. Если есть давление дедлайнов, в конце укажу, что можно урезать без потери качества.
  ::view-transition-group(*),
  ::view-transition-old(*),
  ::view-transition-new(*) {
    animation-duration: 0.25s;
    animation-timing-function: cubic-bezier(0.19, 1, 0.22, 1);
  }
VvisualizeVvisualize show_widgetФаза 1 · Сбор недостающих данных
Что добавляем в датасет
Текущая панель содержит 3 660 наблюдений × ~25 переменных. Нужно расширить до ~40 переменных, добавив рыночные/коммерческие/структурные факторы. Все добавления приводятся ниже с источником, ключом merge, ожидаемым покрытием и оценкой трудозатрат.
1. Birth country и international status (приоритет 1, ~3 часа). Источник: Basketball-Reference, страница игрока содержит Born: City, Country. У вас уже есть скрейпер с curl_cffi для bbref — расширьте функцию parse_player_page чтобы извлекать поле Born из таблицы #meta. Ключ merge: player_id (короткий bbref-код). Покрытие: 100% (поле обязательно на bbref). Производные переменные: is_international (dummy, born outside USA), birth_country (категориальная, для EDA), years_in_usa_proxy (debut_age − immigration_proxy_age, опционально). Скрипт: analysis_v2/data_collection/scrape_birth_country.py.
2. All-NBA selections и career allstar count (приоритет 1, ~4 часа). Источник: Basketball-Reference, страница /awards/all_league.html содержит All-NBA First/Second/Third Team по сезонам, плюс All-Defensive Team. Уже знакомый формат таблиц на bbref. Ключ merge: (player_id, season). Покрытие: 100%, всего ~40 уникальных игроков получают All-NBA в сезон. Производные переменные: all_nba_t (categorical: 0/1st/2nd/3rd), all_nba_lag1 (для использования как предиктор — All-NBA в прошлом сезоне предсказывает supermax), career_all_nba_count (cumsum до t-1), career_allstar_count (cumsum существующей allstar до t-1). Это критично потому, что supermax-eligibility формально определяется через All-NBA в предыдущем сезоне или дважды за три года.
3. Tier контракта (приоритет 1, ~6 часов на построение rule-based классификатора). Источник: вычисляется из существующих переменных + lookup-таблицы CBA cap-thresholds по сезонам. У вас уже есть salary_usd, cap_t, experience, draft_round. Логика классификации:
pythondef classify_tier(row, cap, mle_t, max_25_t, max_30_t, max_35_t):
    s = row['salary_usd']
    exp = row['experience']
    if row['draft_round'] == 1 and exp <= 4 and s < mle_t * 1.1:
        return 'rookie_scale'
    if s < min_salary_t(exp) * 1.15:
        return 'minimum'
    if s < mle_t * 1.2:
        return 'mid_level'
    if s < max_25_t * 1.05:
        return 'max_25' if exp <= 6 else 'high_mid'
    if s < max_30_t * 1.05:
        return 'max_30' if 7 <= exp <= 9 else 'overpay'
    if s < max_35_t * 1.05:
        return 'max_35'
    return 'supermax'
CBA-thresholds: для сезонов 2015/16–2023/24 это 9 строк lookup-таблицы, можно вручную из Basketball-Reference /contracts/. Покрытие: 100%. Валидация: проверить распределение по tier'ам — supermax должно быть ~5–10 игроков на сезон (Curry, James, Durant, KAT, Westbrook в разные годы), rookie_scale ~120–150 на сезон. Если статистика выходит за рамки — править thresholds.
4. Team market size и market characteristics (приоритет 1, ~2 часа). Источник: Nielsen DMA rankings (US TV market ranks) — public, легко гуглится в формате таблицы. Для Toronto использовать численность населения Greater Toronto Area. Все 30 команд легко собираются вручную. Ключ merge: team_abbr. Покрытие: 100%. Производные переменные:

market_size_rank (1–30 в NBA, 1 = крупнейший)
market_population_millions (numeric, MSA или DMA)
top5_market (LAL, LAC, NYK, BKN, CHI, GSW = ~6 команд в крупнейших 5 рынках)
media_market_revenue_proxy (≈ population × NBA_share, опционально)

Замечание про вариативность: market size почти не меняется год к году — будет работать как cross-sectional factor с time-invariant вариацией в пределах команды. Это значит, в two-way FE спецификациях (player + season FE) market_size будет поглощён player FE — поэтому используется только в pooled OLS и random effects, не в FE.
5. All-NBA / supermax eligibility flag (приоритет 1, ~2 часа после п. 2). После сбора All-NBA это derived переменная: supermax_eligible_t = (all_nba_lag1 == 1) | (sum(all_nba_lag1, all_nba_lag2, all_nba_lag3) >= 2) | (mvp_lag1 == 1) | (dpoy_lag1 == 1). MVP/DPOY брать с bbref страницы /awards/. Покрытие: 100%, supermax-eligible ~15–20 игроков на сезон.
6. Team-level переменные: cap space, win %, playoff status (приоритет 2, ~6 часов). Источники:

Win %: Basketball-Reference, страница /teams/{TEAM}/{YEAR}.html, поле W/L. 30 команд × 9 сезонов = 270 строк.
Cap space (приближённо): можно посчитать из вашей же панели как cap_t − sum(team_salary_committed_t) по группировке (team_abbr, season). Это даст приблизительное room — точное значение требует данных по non-active contract salaries, которые в Hoopshype не покрыты, но приближение полезное.
Made playoffs lag: bbref schedule страница, или просто факт из standings (top 8 в каждой конференции до 2019, play-in после).

Производные переменные: team_win_pct_lag1, team_made_playoffs_lag1, team_cap_space_t (numeric, millions $), team_over_luxury_tax_t (dummy, salary committed > tax line).
7. Games missed (durability proxy) (приоритет 2, ~1 час). Полностью derived из существующего games_played: games_missed_t = 82 − games_played_t (для регулярных сезонов; 72 для 2019/20, 72 для 2020/21). Производная: games_missed_lag1, games_missed_3y_cumulative. Можно дополнить ручной разметкой serious injuries из NBA injury reports — но это нетривиальная работа и в первой итерации не обязательна.
8. Agency данные (приоритет 3, ~10 часов — опционально). Hoopshype имеет страницу /agents/, где для каждого игрока указано агентство. Скрейпинг возможен, но коверидж исторически проблемный (для прошлых сезонов могут быть outdated данные). Если делать — собирать только current agency (последний сезон), при условии что игрок ещё в лиге. Лучший компромисс: ручная разметка top-100 игроков (по cumulative earnings) — какое агентство их представляет: Klutch / CAA / Excel / Wasserman / Independent. Производная: agency_tier (top4_agency dummy), klutch_player (отдельная переменная — Klutch имеет репутацию максимизирующего краткосрочные деньги).
9. Endorsement income (приоритет 3, прокси — ~3 часа). Прямые данные недоступны, но прокси возможны:

Jersey sales rank: NBA публикует top-15 jersey sales каждый сезон в пресс-релизах. ~135 player-season entries за 9 сезонов, вручную.
Forbes Highest-Paid Athletes list: для игроков NBA, попавших в годовой список — есть estimate endorsement income. Coverage только top-10–20.
Social media followers: проблематично исторически — Instagram followers за 2016 год недоступны.

Реалистичный план: только jersey sales rank, как dummy top15_jersey_sales_t. Не претендует на исчерпывающее измерение, но захватывает marketable stars.
Сводная таблица новых переменных
  ::view-transition-group(*),
  ::view-transition-old(*),
  ::view-transition-new(*) {
    animation-duration: 0.25s;
    animation-timing-function: cubic-bezier(0.19, 1, 0.22, 1);
  }
VvisualizeVvisualize show_widgetМинимум — приоритет 1 (всего ~15 часов работы, ~2 дня). Это даёт уже сильно расширенный feature set. Если хватит времени — добавить приоритет 2 (ещё ~7 часов). Приоритет 3 — стретч-задачи, ценные, но не критичные.
Структура файлов и pipeline
В существующей файловой структуре analysis_v1/ создаётся параллельный analysis_v2/:
analysis_v2/
├── data_collection/
│   ├── scrape_birth_country.py       # п. 1
│   ├── scrape_awards.py              # п. 2 (All-NBA, MVP, DPOY)
│   ├── scrape_team_records.py        # п. 6 (win %, playoffs)
│   ├── manual_market_size.csv        # п. 4 (вручную, 30 строк)
│   ├── manual_jersey_sales.csv       # п. 9 (опционально, ~135 строк)
│   └── manual_agency_top100.csv      # п. 8 (опционально, ~100 строк)
├── prep_v2.py                        # extends prep_v1.py
├── classify_tier.py                  # п. 3
├── derive_durability.py              # п. 7
├── derive_supermax.py                # п. 5
├── h*_*.py                           # новые регрессии
└── output/
Принцип: prep_v2.py не заменяет prep_v1.py, а расширяет — на вход берёт уже готовый data/clean/data_analysis_v1.csv и добавляет к нему новые колонки через left-join'ы. На выходе — data/clean/data_analysis_v2.csv. Это позволяет легко проверить, что добавление переменных не сломало старые результаты — все главные коэффициенты M1a–M3d должны воспроизвестись с точностью до округления.
Фаза 2 · Интеграция и валидация
После того как все источники собраны и сохранены в отдельные CSV/parquet, нужно объединить и проверить качество.
День 1: merging. Запустить prep_v2.py, который последовательно делает left-join каждого нового источника к базовой таблице. Логировать coverage по каждому merge'у — например, is_international: 3 660/3 660 = 100,0%, all_nba_lag1: 3 277/3 660 = 89,5% (NA для первых сезонов выборки, ожидаемо). Сохранять anti-join'ы — игроков, которых не удалось сопоставить с новым источником — в logs/unmatched_*.csv.
День 2: descriptive валидация. Для каждой новой переменной построить summary statistics и распределение, проверить sanity:

is_international: ожидаемая доля 25–30% (растёт с 2015 к 2024), исторический ориентир — около 100 игроков на сезон. Если доля 50% — где-то ошибка парсинга страны.
all_nba_t: ровно 15 игроков в сезон должны иметь all_nba_t != 0 (5 на First, 5 на Second, 5 на Third). Если больше — ошибка merge.
contract_tier: проверить распределение — должно быть монотонно от rookie_scale (~120 на сезон) до supermax (~5–10 на сезон). Кросс-табуляция tier × season — supermax не должен быть в 2015/16 (designated veteran extensions ввели только CBA 2017).
market_size_rank: проверить, что LAL = 2, GSW = 5, MEM = 30 примерно. Toronto должен быть в районе 4–5.

День 3: replication test. Запустить полный набор M1a–M3d-регрессий на новом датафрейме без новых регрессоров. Каждый коэффициент должен совпасть с прежним значением (или различаться на величину, объяснимую расширением выборки за счёт лучшего coverage'а). Если не совпадает — баг в prep_v2.py, чинить.
Deliverable фазы 2: чистый data/clean/data_analysis_v2.csv объёмом ~40 колонок × 3 660 строк, плюс отчёт validation_report_v2.md с проверками по каждой новой переменной.
Фаза 3 · Новый эконометрический анализ
Это самая содержательная фаза. Семь дней, пять новых блоков спецификаций.
День 1–2: Полная M1 с расширенными факторами (модель M1c-full)
Базовая Mincer-модель расширяется всеми новыми регрессорами:
ln⁡sit=α+β1Statsit+β2Ageit+β3Demoi+β4Marketi+β5Awardsit+β6Durabilityit+β7Teamit+δt+εit\ln s_{it} = \alpha + \beta_1 \mathbf{Stats}_{it} + \beta_2 \mathbf{Age}_{it} + \beta_3 \mathbf{Demo}_i + \beta_4 \mathbf{Market}_i + \beta_5 \mathbf{Awards}_{it} + \beta_6 \mathbf{Durability}_{it} + \beta_7 \mathbf{Team}_{it} + \delta_t + \varepsilon_{it}lnsit​=α+β1​Statsit​+β2​Ageit​+β3​Demoi​+β4​Marketi​+β5​Awardsit​+β6​Durabilityit​+β7​Teamit​+δt​+εit​
где новые блоки:

Demo\mathbf{Demo}
Demo дополнен: is_international, birth_country_dummies (агрегированно: USA / Europe / Latin America / Africa / Asia)
Market\mathbf{Market}
Market: top5_market, market_size_rank (одна из двух, не обе из-за коллинеарности)
Awards\mathbf{Awards}
Awards: all_nba_lag1, career_allstar_count, supermax_eligible
Durability\mathbf{Durability}
Durability: games_missed_lag1, games_missed_3y_cumulative
Team\mathbf{Team}
Team: team_win_pct_lag1, team_made_playoffs_lag1, team_cap_space_t (в роли control, не центрального предиктора)

Спецификации (по аналогии с существующим именованием):

M1c-full (pooled OLS с year FE): главная модель, ~25 регрессоров
M1d-full (two-way FE): time-invariant переменные (market, country) выпадут — это ожидаемо и должно быть оговорено
M1c-full_no_collinear (после VIF-диагностики): убрать самые коллинеарные пары (PER+WS обычно)

День 3: Декомпозиция вариации зарплаты (главная новая глава)
Это даёт прямой ответ на вопрос «какие факторы и насколько определяют зарплату» — то есть напрямую тема работы.
Sequential R² approach (проще): последовательно добавлять блоки регрессоров и считать ΔR²:
ШагБлокR2R^2
R2ΔR2\Delta R^2
ΔR2Доля от общего объяснения0Только intercept0,000——1+ Performance (ppg, apg, mpg, per, ws)0,520,52≈58%2+ Age + experience0,610,09≈10%3+ Demographics (draft, position, international)0,670,06≈7%4+ Awards (allstar, all_nba)0,730,06≈7%5+ Structural (CBA, cap_share, tax)0,770,04≈4%6+ Market (top5)0,770,00≈0%7+ Team controls0,790,02≈2%8+ Durability0,800,01≈1%
Это содержательно мощная картинка — показывает иерархию факторов. Скрипт: analysis_v2/h_decomposition.py. Bootstrap CI на каждое ΔR² через resampling кластеров (player_id), 200 реплик — это даёт интервалы достоверности для долей.
Опционально — Shapley values (сложнее): через пакет shap или собственная реализация через все 2k2^k
2k подмножеств. Для 8 блоков это 28=2562^8 = 256
28=256 регрессий. Дольше, но даёт значения, инвариантные к порядку входа. Если время позволяет — сделать как робастность к sequential R².
День 4: Market-size анализ (главная новая гипотеза H8)
Новая гипотеза H8: игроки в крупных медиа-рынках получают премию через два канала — (а) marketability premium (off-court endorsement opportunities снижают required on-court compensation, но повышают через team's marginal revenue), (б) bargaining premium (большие команды чаще near luxury tax line).
Спецификации:

M8a (basic market): ln⁡s=(M1c)+β⋅top5_market\ln s = (\text{M1c}) + \beta \cdot \text{top5\_market}
lns=(M1c)+β⋅top5_market
M8b (continuous): ln⁡s=(M1c)+β⋅market_size_rank\ln s = (\text{M1c}) + \beta \cdot \text{market\_size\_rank}
lns=(M1c)+β⋅market_size_rank
M8c (interaction with allstar): ln⁡s=(M1c)+β1⋅top5_market+β2⋅allstar+β3⋅(top5_market×allstar)\ln s = (\text{M1c}) + \beta_1 \cdot \text{top5\_market} + \beta_2 \cdot \text{allstar} + \beta_3 \cdot (\text{top5\_market} \times \text{allstar})
lns=(M1c)+β1​⋅top5_market+β2​⋅allstar+β3​⋅(top5_market×allstar) — premium должна быть сильнее для allstar (марк-эффект)
M8d (decomposition with international): ln⁡s=(M1c)+β1⋅top5_market+β2⋅is_international+β3⋅(top5_market×is_international)\ln s = (\text{M1c}) + \beta_1 \cdot \text{top5\_market} + \beta_2 \cdot \text{is\_international} + \beta_3 \cdot (\text{top5\_market} \times \text{is\_international})
lns=(M1c)+β1​⋅top5_market+β2​⋅is_international+β3​⋅(top5_market×is_international) — гипотеза, что international players особенно ценят большие рынки

Скрипт: analysis_v2/h8_market.py. Cluster SE по player, проверка через wild bootstrap для маргинальных коэффициентов.
День 5: Tier-структура контрактов (главная новая гипотеза H9)
Новая гипотеза H9: структура контракта (tier) объясняет существенную часть вариации зарплаты, недетерминируемую performance. Это содержательно главное про «механизм»: max-контракт — это не функция от PPG, это институциональная категория.
Спецификации:

M9a (tier дамми вместо непрерывной): ln⁡s=(M1c−stats)+∑kβk⋅1{tieri=k}\ln s = (\text{M1c} - \text{stats}) + \sum_k \beta_k \cdot \mathbb{1}\{\text{tier}_i = k\}
lns=(M1c−stats)+∑k​βk​⋅1{tieri​=k} — посмотреть pure tier effect
M9b (tier + stats): ln⁡s=(M1c)+∑kβk⋅tierk\ln s = (\text{M1c}) + \sum_k \beta_k \cdot \text{tier}_k
lns=(M1c)+∑k​βk​⋅tierk​ — какая часть variation остаётся после контроля performance
M9c (tier × supermax_eligible interaction): для max-tier игроков проверить, насколько supermax-eligible получают больше

Дополнительный анализ: tier-specific regressions — отдельная Mincer-модель внутри каждого tier'а. Внутри max-tier предсказательная сила performance должна быть низкой (зарплата truncated by cap formula). Внутри rookie_scale — тоже низкой (зарплата определена rookie scale, не performance). Внутри mid_level — самая высокая (это рыночная зона). Это даёт элегантную иллюстрацию того, как механизм CBA подавляет эффект performance в верхнем и нижнем хвосте.
Скрипт: analysis_v2/h9_tier.py.
День 6: Awards-channel (новая гипотеза H10)
Новая гипотеза H10: all-NBA selections значимо повышают зарплату даже при контроле текущей performance (per-game и advanced) — это premium за «verified elite» статус, формализованный supermax-criteria.
Спецификации:

M10a: ln⁡s=(M1c)+β1⋅all_nba_lag1+β2⋅career_all_nba_count\ln s = (\text{M1c}) + \beta_1 \cdot \text{all\_nba\_lag1} + \beta_2 \cdot \text{career\_all\_nba\_count}
lns=(M1c)+β1​⋅all_nba_lag1+β2​⋅career_all_nba_count
M10b (event study вокруг первого All-NBA): для игроков, впервые попавших в All-NBA, ожидается значимый прирост зарплаты в следующем сезоне сверх performance-effect

Скрипт: analysis_v2/h10_awards.py.
День 7: Durability и интерактивные эффекты

M11a (durability main): ln⁡s=(M1c)+β⋅games_missed_lag1\ln s = (\text{M1c}) + \beta \cdot \text{games\_missed\_lag1}
lns=(M1c)+β⋅games_missed_lag1
M11b (durability × age interaction): эффект пропусков должен усиливаться с возрастом
Combined model M_full: все новые блоки в одной спецификации — финальная картинка

Cleanup-задачи: пересчитать sensitivity Oster для главных новых коэффициентов, обновить multiple testing correction (теперь больше тестов, требуется больший Bonferroni / FDR-controlled threshold).
Deliverable фазы 3: ~15 новых таблиц регрессий, все в output_v2/tables/. Главная — sequential R² decomposition.
Фаза 4 · Реструктуризация текста
5 дней, переписать 4 главы.
День 1: Глава 1 (Введение)
Что меняем:

Цели и задачи: вместо 7 задач, где H6 deep dive доминирует, — переформулировка с фокусом на «иерархию факторов»
Новые задачи 5–7: «исследовать роль рыночных факторов», «выявить вклад структуры контракта», «оценить значимость awards channel»
Раздел 1.5 «Предварительный обзор результатов» — обновить под новые гипотезы

День 2: Глава 2 (Обзор литературы)

Раздел 2.1 (contract-year): сократить с 4 страниц до 2. Stiroh, Berri & Krautmann, Keefer — оставить; White & Sheldon, Simmons & Berri, Krautmann & Donley — компактнее.
Раздел 2.2 (taxes): оставить как есть, может быть слегка ужать.
Раздел 2.3 (Mincer): расширить упоминание Kahn & Sherer (расовая дискриминация → методологический шаблон), добавить Rottenberg (1956) о монопсонии в спорте, Lazear & Rosen (1981) о турнирной теории (релевантна для playoff bonuses и performance incentives).
Новый раздел 2.4 (market factors и marketability): литература по market size effects в спорте — Krautmann (1999), Hausman & Leonard (1997, NBA superstar externalities), Berri & Schmidt (2010, NBA gate revenue).
Новый раздел 2.5 (contract structure as institutional pricing): литература по max contracts и cap economics — Hill & Groothuis (2001), Coon's CBA FAQ как методическое описание.
Раздел 2.6 (гипотезы): добавить H8 (market), H9 (tier), H10 (awards) к существующим H1–H7.

День 3: Глава 3 (Методология) и Глава 4 (Результаты)
Глава 3:

3.1 Источники данных: дополнить новыми источниками
3.2 Операционализация: новые переменные с формальными определениями
3.3 Эвристики контрактного года: сократить с 10 проксей до 3 центральных. Остальные семь — в приложение Б
3.4 Эконометрические спецификации: добавить M8, M9, M10, M11
3.5 Диагностики: без существенных изменений

Глава 4: реорганизовать по факторам, не по моделям:

4.1 Performance (M1)
4.2 Демография и человеческий капитал (M1, quantile)
4.3 Структурные факторы: CBA, COVID (event-study)
4.4 Налоговый фактор (M2)
4.5 Рыночные факторы (M8)
4.6 Tier контракта (M9)
4.7 Awards channel (M10)
4.8 Durability (M11)
4.9 Контрактный цикл (M3) — сокращённый H6 deep dive
4.10 Декомпозиция вариации (главная новая глава) — sequential R² или Shapley
4.11 Робастность (как сейчас)

Подсек contract-year deep dive (текущий 4.5) ужать до 1.5–2 страниц: только три ключевые линии критики (recall = 37%, downward FA contamination, гетерогенность).
День 4: Глава 5 (Дискуссия)
Реорганизовать параллельно к новой Главе 4. Главное новое содержание: дискуссия декомпозиции вариации (что объясняет 80% R² базовой модели, какие факторы оставляют residual variation), market premium (есть или нет, для каких подгрупп), tier truncation (как cap-механизм подавляет performance return в верхнем хвосте). Тут же — discussion раздела про супермакс-eligibility как формальный механизм awards channel.
День 5: Глава 6 (Заключение) и Аннотация
Полностью переписать, заменив центральные результаты H6 на иерархию факторов. Подтверждённые/отвергнутые гипотезы расширить с 7 до 10. Методологический вклад: вместо «contract-year proxy validation» как центральный — поднять на верх «декомпозиция вариации зарплаты NBA на восемь блоков факторов с количественным распределением вкладов».
Аннотация — полностью переписать, ~300 слов, акцент на иерархию факторов и долю каждого блока.
Фаза 5 · Визуализация
3 дня, ~6–8 рисунков.
Рисунок 1: Декомпозиция вариации (waterfall chart). Главный рисунок работы. По оси Y — кумулятивный R2R^2
R2, по оси X — последовательные шаги добавления блоков факторов. Каждый шаг — bar с подписью блока. Bootstrap CI на каждое значение. Matplotlib plt.bar с error bars, или waterfall через waterfall_chart. Должна быть основой обложки/первого слайда защиты.
Рисунок 2: Возрастной профиль зарплаты. Scatter (age,ln⁡s)(age, \ln s)
(age,lns) с jittered точками, поверх — параболический фит, вертикальная линия в пике 30,6. Опционально — два цвета по статусу драфта (drafted vs undrafted), показывает разные пики.
Рисунок 3: Quantile coefficient β_ppg(τ). Linechart с τ на оси X (5 точек) и оценкой β^ppg\hat\beta_{ppg}
β^​ppg​ по оси Y с bootstrap CI. Иллюстрирует cap-induced concavity (Rosen 1986).
Рисунок 4: Event-study CBA 2017 coefplot. Точки с CI для τ = −2, −1, 0, 1, 2, 3, 4, 5, 6. Горизонтальная линия 0, вертикальная линия τ = 0. Маркирует pre-trend.
Рисунок 5: Распределение по tier'ам с зарплатами. Boxplot или violin: tier на оси X (rookie_scale → minimum → mid_level → max_25 → max_30 → max_35 → supermax), ln⁡s\ln s
lns на оси Y. Показывает discrete jumps между tier'ами — наглядная иллюстрация institutional pricing.
Рисунок 6: Coefficient plot для main effects M1c-full. Forest plot: каждая переменная — точка с 95% CI. Вертикальная линия на 0. Сразу видна значимость и относительная величина.
Рисунок 7: Contract-year recall heatmap. Матрица 5×5: рекалл (по строкам) против precision (по столбцам) для каждой из 5 главных проксей. Цвет — F1. Хорошая визуализация trade-off'а.
Рисунок 8 (опционально): Market size × allstar interaction. Scatter с двумя linear fit'ами — для top5 markets vs others. Если интеракция значима — это покажет визуально.
Технически: matplotlib для всех, single column width 6×4 inch, sans-serif font, без цвета или с разумным contrast (можно делать для печати в grayscale). Сохранять как PDF (vector) для финальной работы, PNG (300 dpi) для slide-версии. Скрипт: analysis_v2/figures.py.
Фаза 6 · Финальная вычитка
2 дня.
День 1: сверить список литературы с цитированиями в тексте. Найти и исправить:

Cameron, Gelbach & Miller (2011) — в списке есть, в тексте есть только Cameron & Miller (2015). Решить: либо использовать в тексте, либо убрать из списка.
Hinton & Sun (2019) — упомянут в тексте раздел 2.1, в списке отсутствует. Добавить.
Сверить все 19 → 23 источника. В аннотации/разделе 1.7 указать корректное число.
Привести единый стандарт цитирования (APA или ГОСТ — выбрать один).

День 2: финальный технический проход:

Прогнать всю работу через spell-check
Убедиться, что все formulas рендерятся (LaTeX без ошибок)
Проверить, что все 13 + новые таблицы имеют сквозную нумерацию
Все рисунки получили номера и подписи
Проверить cross-references «см. Таблицу N» — N действительно соответствует
Объём финальной работы оценить — ожидается 55–70 страниц при сохранении формата

Риски и план B
Риск 1: jersey sales и agency данные недоступны / неполны. Mitigation: эти переменные приоритет 3, можно полностью опустить. Их отсутствие не критично, market size и awards закрывают коммерческий блок достаточно.
Риск 2: market size не показывает значимости. Это, на самом деле, ожидаемо — Hembre (2021) показал, что в эпоху salary cap премии не должно быть. Если null — это содержательный результат, аналогичный текущему null по tax. Просто переформулировать H8 как «информативный null» и оставить.
Риск 3: tier classification даёт странное распределение. Это означает, что rule-based logic нужно править. Подстраховаться: cross-validate на 30 топ-игроках с ручной классификацией. Если supermax не определяется автоматически — добавить hand-curated supermax list для известных contracts (Curry 2017, James 2018, Antetokounmpo 2020, и т.д.).
Риск 4: timing. 5 недель — реалистично при 5 ч/день. Если у вас параллельно занятия, увеличивайте на 30%. Если дедлайн через 3 недели — критически приоритизируйте: фазы 1 (только приоритет 1) + 3 (только дни 1–3, декомпозиция и market) + 4 (только глава 4 и 6) + 5 (только рисунки 1, 3, 5). Это даёт 80% improvement при 50% затрат.
Риск 5: новые переменные сломают существующие результаты. Mitigation: фаза 2 содержит replication test. Если M1a даёт другой коэффициент при PPG — баг в merging, чинить до фазы 3.
Что сделать первым
Если приступаете прямо сейчас:

Создать ветку analysis_v2/ в репозитории, скопировать структуру из analysis_v1/
Запустить п. 4 — market size (это вручную 30 строк, 2 часа, и сразу даёт измеримый прогресс)
Параллельно расширить скрейпер bbref для birth country (п. 1, 3 часа)
К концу первого рабочего дня у вас 2 из 6 источников собраны и провалидированы

Хотите, чтобы я подготовил конкретные технические артефакты — например, шаблон scrape_birth_country.py, заготовку manual_market_size.csv с уже заполненными значениями для 30 NBA-команд, или rule-based классификатор tier с CBA thresholds на каждый сезон? Это могу сделать сразу в файлах, чтобы вы стартовали с готового кода вместо чистого листа.