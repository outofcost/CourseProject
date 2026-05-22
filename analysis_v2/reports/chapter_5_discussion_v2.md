# Глава 5. Обсуждение

> Драфт под HSE term paper, Article (Empirical) format. Объём: ≈ 15% работы (целевые ~1800 слов).
> Заменяет старый драфт `chapter_5_discussion.md` (~3300 слов был сырьём). Здесь — интерпретация Results (Глава 4) в контексте литературы (Глава 2).
> Цифры — только короткие references на §4.X; интерпретация — основное содержание.
> Маркеры `[TBD: см. {author_year}]` помечают cite'ы, которые требуют верификации по шаблонам из `bibliography/sources/`.

---

## 5.1 Главный методологический и содержательный вывод

Результаты Главы 4 §4.9 устанавливают первую axiom-обоснованную количественную иерархию факторов, определяющих $\ln(\text{salary})$ в NBA в post-2011-CBA эпоху. Shapley-декомпозиция $R^2 = 0.649$ по 9 тематическим блокам показывает: **Performance** (36.8%) и **Age + Experience** (28.7%) совокупно объясняют 65.5% дисперсии — что соответствует ожиданиям классической Mincer-литературы (Mincer, 1974 [TBD]; Rosen, 1981). Однако наивная sequential R²-декомпозиция в plan-order приписывает Performance 68.7% (см. §4.9 Таблица «Sequential vs Shapley») — почти вдвое больше, чем axiom-justified Shapley. Это расхождение — главный методологический сюрприз работы: значительная доля variance, которую sequential R² атрибутирует Performance, на самом деле share с Awards-, Durability-, и Tier-блоками, и при honest attribution перераспределяется в эти каналы.

Содержательное значение: **CBA-структурирование** (tier categorization, awards eligibility, supermax mechanism) и **survival effects** (durability) являются не побочными факторами, а независимыми каналами формирования зарплат, экономически и статистически отделимыми от Performance. NBA-salary в современной эпохе формируется не только через continuous performance pricing, но через систему institutional channelling, которая ранее в литературе не quantified.

## 5.2 Институциональная иерархия как доминирующий слой (H3)

Результат, что tier dummies одни объясняют $R^2 = 0.849$ (§4.3), является, насколько нам известно, первым количественным доказательством того, что NBA в post-2011-CBA эпохе функционирует не как continuous-pricing labor market в традиционном Mincer-смысле, а как **discrete institutional categorization**. Игрок попадает в одну из 8 категорий (minimum, rookie_scale, mid-level, high-mid, max-25, max-30, max-35, supermax) преимущественно через institutional pathway (CBA-определённые правила eligibility), и его внутри-tier salary становится практически фиксированной величиной с малыми отклонениями.

Этот результат — нетривиальное extension классической теории Rosen (1986) [TBD] о cap-induced concavity. Rosen предсказывал, что binding cap должен делать reward function concave для top-tier игроков; наши tier-specific Mincer-регрессии (§4.3 Таблица 3) подтверждают это эмпирически: $\beta_{\text{ppg}}$ внутри max_30-tier в 2.3 раза ниже, чем в mid_level. Но более важное наблюдение — что **structure salary не просто concave, а step-function**. Discrete jumps между tiers (e.g., от high-mid к max-25: +56% в expected salary) намного больше, чем continuous variation внутри tier (median within-tier spread ~10%). Это означает, что primary determinant зарплаты NBA-игрока — это вопрос «попадёт ли он в следующий tier», а не «насколько хорошо он играет внутри своего tier».

Эта картина согласуется с Hill & Groothuis (2001) [TBD], которые предсказывали, что cap создаст «institutional layer» поверх Mincer pricing, но идёт дальше: institutional layer не дополнение, а доминирующий механизм. Performance-метрики работают через **institutional bridge** — PPG → All-Star/All-NBA selection → tier eligibility → discrete salary jump — а не через continuous wage adjustment.

## 5.3 Awards channel и contract renewal cycle (H5, H6)

Результаты Главы 4 §4.4 устанавливают, что awards канал работает через два уровня: (а) immediate signaling effect (all_nba_lag1 → +20% к salary при контроле текущего performance, p = 0.008); (б) delayed event-study effect — после первого All-NBA selection salary skip +21% при $\tau = +2$ (p = 0.029) и +22% при $\tau = +3$ (p = 0.037), при отсутствии значимости в $\tau = -2, -1, 0, +1$ (pre-trends чисты).

Эта двухуровневая структура согласуется с теоретическими предсказаниями rank-order tournaments (Lazear & Rosen, 1981 [TBD]): awards служат signaling devices, переводящими noisy individual productivity в discrete rank-based premium. Однако delayed effect (τ = +2, +3) указывает на specific mechanism, не explicitly предсказанный в Lazear-Rosen — **contract renewal cycle**. Awards не переводятся в зарплату мгновенно, потому что большинство активных NBA-контрактов фиксируют salary на 2–4 года forward. Premium реализуется в next renewal event, когда новый контракт подписывается с применением правил designated extension (Coon, n.d., Q24).

Это эмпирическое подтверждение contract-cycle dynamics, теоретически обсуждавшейся в Stiroh (2007) [TBD] для general contract-year effect, но впервые quantified specifically для NBA awards channel. Cycle mechanism — institutional, а не behavioral: оно работает не потому, что игроки «играют лучше» в contract year (хотя это может тоже происходить), а потому, что CBA-правила определяют, в какой момент новая salary structure активируется.

**Aging-veteran sub-finding** (§4.4: multi_all_nba (≥3) β = −0.22, p = 0.038) представляет уникальное observation, ранее не quantified в NBA literature. Игроки с историей нескольких All-NBA selections, находящиеся в declining phase карьеры, несут residual penalty −19.7% против non-veteran игроков с тем же current performance. Содержательная интерпретация — **survival bias**: возрастные «легенды» с ухудшающимся текущим performance непропорционально часто продолжают карьеру (вопреки physical decline), что создаёт residual mismatch между past elite status и current pricing. Этот mechanism нуждается в follow-up исследовании; гипотетический канал — risk-averse team management, готовое overpay'ить за brand value veteran star vs гипотетический канал — career-end transaction frictions.

## 5.4 Anti-marketability и Hembre channel (H7)

Результат, что top-5 NBA cities дают не премию, а discount $\hat{\beta} = -0.098$ (p = 0.022, §4.5), отвергает классическую Rosen-style marketability hypothesis для современной NBA. Heterogeneity-тесты с wild-cluster bootstrap (1000 реплик, Rademacher) показывают, что эффект uniform across звёздности и nationality (interaction × allstar и × intl не значимы), что исключает signal-amplification interpretation.

Hembre (2022) предлагает theoretical channel, совместимый с направлением нашего эффекта: при unrestricted free agency игроки требуют compensating differential за state income tax burden, что снижает spending power команд в high-tax штатах (CA, NY, IL — преимущественно где базируются top-5 NBA cities). Сам Hembre, однако, сообщает, что NBA-specific coefficient в его pooled-sport regression статистически незначим ($\hat{\beta}_{\text{NBA}} \in [-0.143, -0.069]$, SE > 1.1, Table 3, p. 20); pooled effect доминируется NFL и MLB sub-samples (Hembre, 2022, p. 11). Поэтому мы не можем интерпретировать наш result как direct confirmation Hembre's NBA channel; точная формулировка — «consistent direction, although NBA-specific imprecise in pooled-sport setup».

Альтернативное объяснение — **player-side compensating differential** через off-court endorsement доход и lifestyle крупных рынков (cases: LeBron 2018 → LAL под cap, Durant 2016 → GSW на 1+1). Эта interpretation не identifying'нается direct'ом в наших данных (endorsement income не собран; revealed-preference selection не observable), но согласуется с qualitative observations. Comprehensive разрешение направления anti-marketability — между tax-driven (Hembre channel) и preference-driven (off-court substitution) — требует дополнительных данных (endorsement income, individual residence decisions при offers) и оставляется для future research.

В наших данных есть один dimension robustness check, который мы могли бы добавить в follow-up: continuous `state_tax_rate` как control при `top5_market` в joint spec, чтобы посмотреть, «съест» ли он top5 coefficient (см. §6.4 пункт 6). Прямая декомпозиция market vs tax channels — естественная robustness задача для следующей итерации.

## 5.5 Команды и налоговый эффект как informative nulls (H8, H9)

Гипотезы H8 (team success → individual salary) и H9 (state tax → pre-tax salary) обе rejected, но как informative nulls, а не failed tests. По H8 все четыре team-level контроля (win_pct, made_playoffs, playoff_round, over_luxury_tax) дают p > 0.15 с 95% CI, пересекающим ноль (§4.6). По H9 state_tax_rate p = 0.29, и MDE-расчёт показывает, что 21% pre-tax wage shift между low-tax и high-tax штатами был бы детектирован (§4.7).

Содержательная интерпретация: в современной CBA-эпохе **cap mechanism эффективно нейтрализует team-side market power** (Hill & Groothuis, 2001 [TBD]). Bargaining между игроком и командой не происходит «по полной» — оно ограничено CBA-defined категориями (tier eligibility) с малыми deviations. Это согласуется с теоретическим аргументом Kahn (2000) [TBD] о том, что cap-era sports markets создают labor structure, в которой individual talent оценивается approximately uniformly across markets и teams.

Team success null также согласуется с эмпирической литературой Berri, Brook & Schmidt (2007) [TBD], которые показывают, что после контроля individual performance team-level controls добавляют мало к explanatory power individual salary. Этот результат можно интерпретировать так: в NBA, individual contribution to team success (measurable через player stats) уже captured в performance метриках; остаточный effect team success (championship status, playoff appearances) — это в основном luck/team-composition factor, не translated в individual salary.

Tax null более тонкий. Поскольку нам известно из Hembre (2022), что для pooled sports tax effect значим, отсутствие effect в NBA после контроля cap-share может означать одно из двух: (а) NBA-specific labor market features (smaller rosters, larger individual contracts) делают tax effect недетектируемым в наших данных; (б) cap-share contol уже абсорбировал tax effect через косвенный channel (high-tax states имеют команды с особой cap-allocation pattern). Без more refined panel design разделить эти возможности не получается; это — limitation, отмеченная в §5.8.

## 5.6 Durability как уникальный price effect (H10)

Результат, что каждый пропущенный матч в прошлом сезоне снижает зарплату на 0.49% (β = −0.005/game, p < 0.001, §4.8), и что Shapley-share Durability = 5.7% — значительно больше планового ожидания ≈ 1% — устанавливает, что NBA-рынок прайсит **retrospective health record** как самостоятельный factor, независимо от текущего performance.

Это empirically первое systematic quantification durability discount в NBA. Retrospective games_missed как direct predictor subsequent salary в peer-reviewed литературе post-2011-CBA-эпохи формально не тестировался; ближайший антецедент — обсуждение performance consistency в Bodvarsson & Brastow (1998) [TBD], но не durability как такового. Mechanism — рынок воспринимает игроков с длинной injury history как риски для будущего performance reliability; этот воспринимаемый risk премий цены через discount в next contract negotiation.

Интересное негативное finding — interaction games_missed × age не значима (M11b, p = 0.12, §4.8). Гипотеза «травмы стоят больше для стареющих игроков» (intuitive, основанная на physiological recovery decline) не подтверждается в наших данных. Альтернативная interpretation: команды одинаково penalize injury risk вне зависимости от age, потому что прецедент injured young player создаёт ту же стратегическую неопределённость, что прецедент injured veteran.

## 5.7 Методологические ограничения и threats to internal validity

Несколько methodological caveats требуют explicit обсуждения.

**Oster (2019) δ-sensitivity** ограничена в нашем setup. Все $\delta < 1$ для key coefficients (§3.8.3), что в богатых-наблюдательных данных не означает робастности к OVB. Sign-стабильность подтверждена, magnitude чувствительна к спецификации; формальный $\delta$-based confidence interval не строится. Это — известная limitation метода Oster для panels с high $R^2$ baseline.

**Shapley R² — descriptive, не causal** (Lipovetsky & Conklin, 2001). Декомпозиция variance ≠ identification causal effects. Shapley даёт «справедливую» attribution explained variance, но не утверждает что блок $i$ causally определяет $\phi_i$ долю salary. Это accounting-style декомпозиция, полезная для priority ranking, но не для policy intervention design.

**TOT-attribution problem** (§3.2). Около 14% выборки получают NaN в team/market-зависимых спецификациях (игроки, поменявшие команду внутри сезона). Альтернативная импутация (взвешенная по доле игр) была рассмотрена и отвергнута; результаты H7 и H8 строятся на 2 268 obs из 3 660. Это потенциальный selection bias, но направление и магнитуда unknown; sensitivity к разным attribution схемам — future robustness work.

**Endorsement доход не наблюдается.** Маркетинговый доход NBA-звёзд может составлять до $30M/год для top players; этот компонент дохода полностью отсутствует в наших данных. Анти-marketability finding (H7) и aging-veteran sub-finding могут частично reflect substitution между observable salary и unobservable endorsement income. Identification причинного direction требует данных из Forbes Power 50 rankings или NBA jersey sales — оставляется на future work.

**Период замкнут на 2015/16–2023/24.** Выводы применимы к salary cap structure 2011–2017 + 2017–2023 CBA-эпохам. CBA 2023 с second apron и updated supermax thresholds может изменить dynamics; sample на 2023/24 включает первый год CBA 2023, но multi-year contracts подписанные ранее всё ещё под 2017 правилами. Полная оценка CBA 2023 эффекта — естественное направление для следующей итерации работы (с накоплением больше observations post-2023).

---

[Слов в главе: ≈ 1 850; TBD-маркеров: 7; commit + push готов к следующему cycle.]
