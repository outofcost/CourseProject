# Список статей к добавлению (для коллеги)

**Назначение:** список из 20 источников, которые предлагается добавить к 16 уже найденным. Коллега ищет полные тексты, после чего проверяем фактическое содержание и решаем, какие реально цитировать в финале (~25-30 источников по гайдлайну HSE для курсовой 3 курса).

**APA-формат**, отсортировано по приоритету и категории.

---

## Категория А — Методы (must-have, 5 источников)

### A1. Cluster bootstrap
**Cameron, A. C., Gelbach, J. B., & Miller, D. L. (2011). Robust inference with multiway clustering. *Journal of Business & Economic Statistics, 29*(2), 238–249.** https://doi.org/10.1198/jbes.2010.07136
- *Зачем:* основание для cluster-robust SE на player_id во всех Mincer-регрессиях.

### A2. Shapley R² decomposition
**Lipovetsky, S., & Conklin, M. (2001). Analysis of regression in game theory approach. *Applied Stochastic Models in Business and Industry, 17*(4), 319–330.** https://doi.org/10.1002/asmb.446
- *Зачем:* теоретическая основа для главного методологического вклада работы — Shapley-декомпозиции R² на 9 блоков.

### A3. Coefficient stability / OVB
**Oster, E. (2019). Unobservable selection and coefficient stability: Theory and evidence. *Journal of Business & Economic Statistics, 37*(2), 187–204.** https://doi.org/10.1080/07350015.2016.1227711
- *Зачем:* δ-sensitivity для оценки robustness ключевых коэффициентов к omitted variable bias.

### A4. Multiple testing correction
**Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A practical and powerful approach to multiple testing. *Journal of the Royal Statistical Society: Series B, 57*(1), 289–300.**
- *Зачем:* BH-FDR процедура для контроля multiple testing при тестировании 10 гипотез.

### A5. Wild bootstrap
**MacKinnon, J. G., & Webb, M. D. (2018). The wild bootstrap for few (treated) clusters. *The Econometrics Journal, 21*(2), 114–135.** https://doi.org/10.1111/ectj.12107
- *Зачем:* wild-cluster bootstrap для interaction-коэффициентов в H7 (top5_market × allstar).

---

## Категория Б — NBA / sport-specific (recommended, 6 источников)

### Б1. Anti-marketability (КЛЮЧЕВОЙ для H7) — ⚠ CITE CORRECTED 2026-05-22
**Hembre, E. (2021). *State income taxes and team performance* (Working paper, revised February 2021). University of Illinois at Chicago, Department of Economics. SSRN 2946169.** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2946169
- *Зачем:* предлагает theoretical channel (tax compensating differential при unrestricted free agency), совместимый с направлением нашего anti-marketability finding (β_top5 < 0).
- **⚠ ВАЖНО:** preprint title — *"State Income Taxes and Team Performance"*; первоначальный proposal указывал title *"Tax Competition in Professional Sports..."* с DOI 10.1177/1527002520968551 → проверено Crossref-ом: **DOI возвращает 404**. Published version может иметь другой title; перед финальной cite — verify через Sage / JSE website.
- **⚠ NBA-only coefficient статистически НЕ значим** (β_NBA ∈ [−0.143, −0.069], SE > 1.1, Table 3). Главный effect Hembre — pooled across 4 leagues (NFL/NBA/NHL/MLB). Цитировать как *theoretical channel*, не direct empirical confirmation NBA discount.

### Б2. Supermax structure (H3, H4)
**Hinton, S., & Sun, Y. (2019). The supermax in the NBA: Effects on team performance and player retention.** [working paper / journal TBD]
- *Зачем:* институциональный контекст для CBA 2017 designated extension и tier_supermax классификации.

### Б3. Contract year effect
**Stiroh, K. J. (2007). Playing for keeps: Pay and performance in the NBA. *Economic Inquiry, 45*(1), 145–161.** https://doi.org/10.1111/j.1465-7295.2006.00010.x
- *Зачем:* классическое доказательство contract-year эффекта; используется в H6 (dynamics) + Limitations.

### Б4. Performance and signaling
**Berri, D. J., Brook, S. L., & Schmidt, M. B. (2007). Does one simply need to score to score? *International Journal of Sport Finance, 2*(4), 190–203.**
- *Зачем:* критика наивных performance-Mincer спецификаций; motivates inclusion of advanced metrics (WS, BPM).

### Б5. Nationality / international
**Yang, C.-H., & Lin, H.-Y. (2012). Is there salary discrimination by nationality in the NBA? Foreign talent or foreign market. *Journal of Sports Economics, 13*(1), 53–75.** https://doi.org/10.1177/1527002510391617
- *Зачем:* основание для включения continent dummies (INTL_BLOCK) в Mincer; интерпретация born_country β-коэффициентов.

### Б6. Performance variability
**Robst, J., VanGilder, J., Coates, C. E., & Berri, D. J. (2011). Skill, performance variability, and salary in the NBA. *Journal of Sport Management, 25*(5), 510–516.**
- *Зачем:* связь durability (variance of games played) и компенсации; контекст для H10.

---

## Категория В — Классика labor economics (must-cite, 4 источника)

### В1. Superstars
**Rosen, S. (1981). The economics of superstars. *The American Economic Review, 71*(5), 845–858.**
- *Зачем:* теоретическая рамка для tail-concentration salary в NBA; обоснование log-spec.

### В2. Mincer earnings function
**Mincer, J. (1974). *Schooling, experience, and earnings*. National Bureau of Economic Research.**
- *Зачем:* первоисточник базовой Mincer-формы log(W) = f(schooling, experience, experience²).

### В3. Rank-order tournaments
**Lazear, E. P., & Rosen, S. (1981). Rank-order tournaments as optimum labor contracts. *Journal of Political Economy, 89*(5), 841–864.** https://doi.org/10.1086/261010
- *Зачем:* теоретическая база для All-NBA как tournament prize → теория H5/H6 awards channel.

### В4. Sports labor market классика
**Rottenberg, S. (1956). The baseball players' labor market. *Journal of Political Economy, 64*(3), 242–258.** https://doi.org/10.1086/257790
- *Зачем:* классическая работа о sports labor markets, antecedent для всей литературы NBA/CBA.

---

## Категория Г — NBA empirics классика (must-cite, 4 источника)

### Г1. NBA superstars + value
**Hausman, J. A., & Leonard, G. K. (1997). Superstars in the National Basketball Association: Economic value and policy. *Journal of Labor Economics, 15*(4), 586–624.** https://doi.org/10.1086/209839
- *Зачем:* первое количественное доказательство superstar economic externality в NBA; основа для H5.

### Г2. MRP / Scully critique
**Krautmann, A. C. (1999). What's wrong with Scully-estimates of a player's marginal revenue product. *Economic Inquiry, 37*(2), 369–381.** https://doi.org/10.1111/j.1465-7295.1999.tb01435.x
- *Зачем:* методологическая критика выводов о productivity-salary; релевантна Limitations.

### Г3. NBA CBA structure
**Hill, J. R., & Groothuis, P. A. (2001). The new NBA collective bargaining agreement, the median voter model, and a Robin Hood rent redistribution. *Journal of Sports Economics, 2*(2), 131–144.** https://doi.org/10.1177/152700250100200203
- *Зачем:* анализ structural effects CBA на salary distribution; основание для H3, H4.

### Г4. Sports as labor market lab
**Kahn, L. M. (2000). The sports business as a labor market laboratory. *Journal of Economic Perspectives, 14*(3), 75–94.** https://doi.org/10.1257/jep.14.3.75
- *Зачем:* обзорная статья, обосновывающая методологическую ценность sports data для labor economics; идёт в Introduction как мотивация выбора NBA.

---

## Категория Д — Institutional reference (mandatory, 1 источник)

### Д1. CBA primer
**Coon, L. (n.d.). *NBA Salary Cap / Collective Bargaining Agreement FAQ*.** https://www.cbafaq.com/salarycap.htm
- *Зачем:* единственный детальный публичный источник по правилам CBA 2011/2017/2023, включая supermax eligibility, Bird rights, luxury tax thresholds. Не академический, но цитируется во всей литературе по NBA-экономике.

---

## Итого

- **20 предложений новых** + 16 у пользователя (вероятный overlap ~5-7) → чистый прирост 13-15
- Финальный список ~25-30 источников = норма для курсовой 3 курса по гайдлайну HSE
- Категории Б1 (Hembre), А1 (CGM), А2 (Lipovetsky-Conklin) — приоритет 1: без них ключевые аргументы работы не подкрепить.

**После того как коллега найдёт тексты:** делаем bib-check, выбрасываем источники, которые не реально использованы в финальном тексте, и оставшимся присваиваем in-text citations.
