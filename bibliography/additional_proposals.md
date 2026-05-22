# Additional source proposals

12 источников найдены в `Промпт 1/Анализ статей - Лист1 (6).csv`, **не указаны** в `analysis_v2/reports/bibliography_proposal.md`. Все обработаны (шаблоны в `sources/`, статус — см. `MASTER_TABLE.md`).

Этот файл — на случай, если Кирилл хочет официально перенести их в `bibliography_proposal.md`.

---

## Tax cluster (5)

### N1. Kleven, Landais & Saez (2013) — *Critical addition*
**APA:** Kleven, H. J., Landais, C., & Saez, E. (2013). Taxation and international migration of superstars: Evidence from the European football market. *American Economic Review, 103*(5), 1892–1924. https://doi.org/10.1257/aer.103.5.1892
**Найден через:** Промпт 1 CSV; rating 10/10
**Зачем нужен:** Top-1-journal study с rigorous identification tax-mobility effects у superstars. Reframing для нашего H9 informative null — tax channel exists in proper setting, our null = sample specifics, not absence of effect.
**Приоритет:** ВЫСШИЙ

### N2. Alm, Kaempfer & Sennoga (2012)
**APA:** Alm, J., Kaempfer, W. H., & Sennoga, E. B. (2012). *Baseball salaries and income taxes: The "home field advantage" of income taxes on free agent salaries* (Working Paper No. 1209). Tulane University, Department of Economics.
**Найден через:** Промпт 1 CSV; rating 6/10
**Зачем нужен:** MLB-аналог Hembre; direct quantitative result (+$21–24K per pp tax → individual FA salary). Контраст с нашим NBA H9 null.
**Приоритет:** ВЫСШИЙ

### N3. Kopkin (2012)
**APA:** Kopkin, N. (2012). Tax avoidance: How income tax rates affect the labor migration decisions of NBA free agents. *Journal of Sports Economics, 13*(6), 571–602. https://doi.org/10.1177/1527002511434967
**Найден через:** Промпт 1 CSV; rating 7/10
**Зачем нужен:** Прямой NBA + tax precursor. Sorting mechanism: tax → destination choice, not salary level (cap-constrained market).
**Приоритет:** ВЫСШИЙ

### N4. Johnson & Hall (2017)
**APA:** Johnson, J., & Hall, J. C. (2017). [Title TBD via HSE proxy]. *Applied Economics Letters*.
**Найден через:** Промпт 1 CSV; rating 7/10
**Зачем нужен:** Direct counter-evidence нашему H9 null: +$60K per pp ATR в NBA FA. Sample differences (FA-only 2010-14 vs наш full 2015-24) объясняют divergence — центральная для Discussion anatomy.
**Приоритет:** ВЫСШИЙ

### N5. Kahn & Sherer (1988)
**APA:** Kahn, L. M., & Sherer, P. D. (1988). Racial differences in professional basketball players' compensation. *Journal of Labor Economics, 6*(1), 40–61. https://doi.org/10.1086/298174
**Найден через:** Промпт 1 CSV; rating 7/10
**Зачем нужен:** Classical NBA discrimination literature; включать только если в Lit Review §2.x будет параграф про historical evolution NBA salary literature.
**Приоритет:** НИЗКИЙ-СРЕДНИЙ

---

## Contract year / shirking / incentives cluster (5)

### N6. White & Sheldon (2014)
**APA:** White, M. H., & Sheldon, K. M. (2014). The contract year syndrome in the NBA and MLB: A classic undermining pattern. *Motivation and Emotion, 38*, 196–205. https://doi.org/10.1007/s11031-013-9389-7
**Найден через:** Промпт 1 CSV; rating 8/10
**Зачем нужен:** NBA + MLB contract year effect, SDT framing; для Limitations §6.x (CY effect как endogeneity concern).
**Приоритет:** СРЕДНИЙ

### N7. Keefer (2021)
**APA:** Keefer, Q. A. W. (2021). The sunk-cost fallacy in the NBA: Evidence using player salary and playing time. *Empirical Economics*. https://doi.org/10.1007/s00181-020-01957-6
**Найден через:** Промпт 1 CSV; rating 8/10
**Зачем нужен:** DiD + IV с salary cap shock 2016/17; методологически сильнейшая работа таблицы по contract year / sunk-cost. Direct citation для Methods + Limitations.
**Приоритет:** СРЕДНИЙ-ВЫСШИЙ

### N8. Krautmann & Donley (2009)
**APA:** Krautmann, A. C., & Donley, T. D. (2009). Shirking in Major League Baseball: Revisited. *Journal of Sports Economics, 10*(3), 292–304. https://doi.org/10.1177/1527002508327395
**Найден через:** Промпт 1 CSV; rating 7/10
**Зачем нужен:** MLB shirking analog; для cross-sport contrast в Limitations.
**Приоритет:** НИЗКИЙ

### N9. Berri & Krautmann (2006)
**APA:** Berri, D. J., & Krautmann, A. C. (2006). Shirking on the court: Testing for the incentive effects of guaranteed pay. *Economic Inquiry, 44*(3), 536–546. https://doi.org/10.1093/ei/cbj033
**Найден через:** Промпт 1 CSV; rating 8/10
**Зачем нужен:** Первая NBA shirking work; relevant для Limitations §6.x обсуждения endogeneity post-contract performance.
**Приоритет:** СРЕДНИЙ

### N10. Conklin & Daniel (2023)
**APA:** Conklin, M., & Daniel, J. (2023). *State income tax effects on NBA player free throws* (SSRN Working Paper No. 4474724).
**Найден через:** Промпт 1 CSV; rating 5/10
**Зачем нужен:** Working paper, simple t-test без controls; weak methodologically.
**Приоритет:** SKIP

---

## Theory / inequality cluster (2)

### N11. Hölmström (1979) — *Foundational*
**APA:** Hölmström, B. (1979). Moral hazard and observability. *The Bell Journal of Economics, 10*(1), 74–91. https://doi.org/10.2307/3003320
**Найден через:** Промпт 1 CSV; rating 9/10
**Зачем нужен:** Nobel-prize-winning theoretical foundation для всей литературы по principal-agent contracts в спорте. Для Lit Review §2.x — теоретическая основа discussion incentive effects of guaranteed contracts (relevant для interpretation H10 durability discount).
**Приоритет:** ВЫСШИЙ

### N12. Simmons & Berri (2011)
**APA:** Simmons, R., & Berri, D. J. (2011). Mixing the princes and the paupers: Pay and performance in the National Basketball Association. *Labour Economics, 18*(3), 381–388. https://doi.org/10.1016/j.labeco.2010.11.013
**Найден через:** Промпт 1 CSV
**Зачем нужен:** NBA salary inequality and performance; tangential — useful для context в Discussion если обсуждается inequality / Gini.
**Приоритет:** НИЗКИЙ

---

## Также рекомендую к замене из proposal:

### Bodvarsson & Brastow (1998) — replacement for failed Robst 2011 — ✅ template added
**APA (verified via Crossref 2026-05-22):** Bodvarsson, Ö. B., & Brastow, R. T. (1998). Do employers pay for consistent performance?: Evidence from the NBA. *Economic Inquiry, 36*(1), 145–160. https://doi.org/10.1111/j.1465-7295.1998.tb01702.x

⚠ Earlier note here had wrong journal: было «JSE 1(1), 95-102», реально — **Economic Inquiry**, vol 36(1), pp. 145–160, 1998 (per Crossref + RePEc IDEAS).

**Найден через:** Agent A research + Crossref verification 2026-05-22
**Зачем нужен:** Заменяет несуществующий Robst-et-al-2011-perf-var paper из bibliography_proposal. Прямо тестирует premium за consistency в NBA salaries — proper theoretical anchor для H10 (durability как форма consistency). Шаблон уже в `bibliography/sources/bodvarsson_1998.md` (skeleton — Wiley paywall).
**Приоритет:** СРЕДНИЙ (recommended если consistency/perf-variability аргумент сохраняется в Discussion §5.6)

---

**Обновлено:** 2026-05-22
**Автор:** Artem (collaborator). Для решения о включении / выкидывании из финальной библиографии — Кириллу.
