# Hembre (2021) — Tax Competition in Professional Sports / State Income Taxes and Team Performance

> ⚠ **Title / DOI discrepancy:** в `bibliography_proposal.md` источник указан как "Tax Competition in Professional Sports: A Theoretical and Empirical Analysis" с DOI 10.1177/1527002520968551. DOI возвращает 404 в Crossref (проверено 2026-05-22). Реальная статья Hembre, доступная как preprint (Feb 2021, SSRN 2946169), называется **"State Income Taxes and Team Performance"** и охватывает тот же контент (state tax effects in pro sports). Скорее всего proposal содержит ошибку в title и/или DOI; этот шаблон заполнен по preprint версии. **Рекомендация:** перед финальным цитированием — проверить точный published title и DOI через journal of sports economics website (Sage).

---

## 1. Citation (APA)

Hembre, E. (2021). *State income taxes and team performance* (Working paper, revised February 2021). University of Illinois at Chicago, Department of Economics. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2946169

> Если published version отличается — заменить на: Hembre, E. (2021). [Published title]. *Journal of Sports Economics, 22*(?), ?–?. https://doi.org/[verified DOI]

---

## 2. Source metadata

- **Type:** empirical
- **Sample:** 4 major US pro leagues (NBA, NFL, NHL, MLB), 1995–2017 main analysis (extended to 1977 for free-agency placebo); 1,931 team-year observations excluding expansion teams, 2,525 incl. expansion (Table 3)
- **Method:** within-team fixed-effects panel; outcome = win percentage; main regressor = top state marginal income tax rate; team FE + league-by-year FE; cluster-robust SE
- **Pages used in this summary:** 1 (abstract), 2 (intro), 6 (model eq. 1), 10–11 (main results), 15–16 (discussion), 20–21 (Table 3 — league-specific coefficients), 25–26 (event study figure)
- **DOI / URL:** SSRN 2946169 (preprint); published version DOI per proposal — НЕ ВАЛИДЕН (см. предупреждение выше)
- **Access status:** preprint (open access на SSRN + личном сайте UW Madison)
- **Local file:** `bibliography/pdfs/hembre_2021_preprint.pdf`

---

## 3. Use mapping (КРИТИЧНО для интеграции)

- **Stream:** Б (NBA / sport-specific). Также tangentially Stream 5 (externalities — потому что Hembre изучает tax externality).
- **Section in coursework:** Discussion §5.x — interpretation of anti-marketability finding (H7); Lit Review §2.4 (market / team context); Limitations §6.x — caveat про канал (tax vs market-size)
- **Supports hypothesis(es):** H7 (top-5 market discount). Косвенно — H9 (state tax effect, который у нас informative null).
- **Specifically supports argument:** Hembre показывает, что в high-tax states (которые сильно overlap с top-5 market cities) команды испытывают competitive penalty, потому что игроки требуют compensating differential за tax burden, что снижает spending power и/или quality of talent. Это даёт *альтернативный канал* для нашего anti-marketability finding β_top5 = −0.098: top-5 markets — это в основном CA (LAL, LAC, GSW), NY (NYK, BRK), IL (CHI) — все с высокими state taxes. Скрытый tax mechanism может быть driver, который мы интерпретируем как market-size.

---

## 4. Core thesis (3-5 предложений)

Hembre тестирует, влияет ли уровень state income tax на performance профессиональных спортивных команд. Через panel-FE регрессию win% на top marginal state tax rate (плюс controls: population, income, quality of life, franchise age + team and league-by-year FE), он находит negative effect: 1pp увеличение state tax → −0.77 до −0.86 pp в win%; стандартное отклонение увеличения tax rate → −0.71 до −0.80 pp. Главный effect — pooled across all 4 leagues; **NBA-specific coefficient в Table 3 не статистически значим** (β = −0.069 до −0.143, SE > 1.1). Механизм: при unrestricted free agency игроки могут переключать tax burden на команды через compensating wage differential, что даёт teams в high-tax states меньше spending power per dollar of value. Placebo до 1977 (до free agency) не показывает effect, подтверждая каузальность.

---

## 5. Key claims for our text (нумерованный список)

1. **Negative state tax → team performance link (pooled):** β_pooled = −0.85 (Column 1), −0.77 to −0.86 across specs (Cols 2–4), все стат. значимы на p<0.10 или выше (Table 1, p. 10).
2. **Mechanism = compensating wage differential under free agency** — placebo до 1977 (no free agency) → null effect; mechanism активируется только когда labor может торговаться (p. 14, Figure ~).
3. **NBA-specific effect insignificant (NBA-only):** β_NBA = −0.069 to −0.143, SE = 1.1–1.3 (Table 3, p. 20). **ВАЖНО** для нас: Hembre сам по себе не доказывает state-tax discount именно в NBA — главный effect статистически значим в NFL (−1.4) и MLB (−1.4 нестат.) но не в NBA.
4. **Cost-per-win estimate для NBA = $1.5M** (Appendix Table A.3, p. 11) — 1pp tax increase → $0.634M менее spending power → ≈ 0.4 fewer wins/year (small effect, согласуется с insignificant NBA coefficient).
5. **Career-long top earners face larger discount** — высокий veteran salary + free agent → выше absolute compensating differential.

---

## 6. Direct quote candidates (с page numbers)

> "Higher income tax rates lower team performance with a percentage point increase in state income tax rates decreasing team win percentage between 0.77 to 0.86 points." (Abstract, p. 1)

> "The income tax effect did not exist prior to players gaining unrestricted free agency which allowed players to shift the income tax burden to teams." (Abstract, p. 1)

> "Unrestricted free agency allows every team to compete on an equal footing for eligible players, a key element in the salary competition that allows players to be compensated for higher income tax rates. Hence, the income tax effect would be expected to [appear]." (p. 6)

> "A team moving from a high income tax state to a no income tax state, such as the recent relocation of the Raiders from Oakland, CA to Las Vegas, NV, could expect to win 11.1 percent more of its games." (p. 11)

---

## 7. Methodological notes

Не методологическая paper — empirical applied. Пропускаю детали.

(Используемые методы — panel FE + clustered SE — стандарт; цитировать Cameron-Gelbach-Miller 2011 как методологическую основу, не Hembre.)

---

## 8. Limitations / caveats

1. **NBA-specific effect not significant** — Table 3 показывает β_NBA = −0.069 с SE >1.1. Нельзя цитировать Hembre как доказательство state-tax discount именно в NBA; его main result — pooled across sports.
2. **Outcome = winning %, не player salary directly** — Hembre изучает team-level performance, а не individual-level compensation. Применимость к нашему H7 (где outcome = individual ln_salary) — косвенная: tax влияет на spending → на talent quality → на salary distribution.
3. **Top marginal state tax — proxy, не actual tax paid** — звёзды NBA с multistate income (away games, endorsements) имеют сложные tax situations; Hembre использует state of team residence как proxy.
4. **Confounders:** top-5 markets и high-tax states overlap, но также coincide с big media markets, cost-of-living, weather, off-court endorsement opportunities. Hembre контролирует location amenities (Albouy 2015), но не market-size напрямую. Отсюда — наш H7 и Hembre измеряют **переплетающиеся каналы**, не один.

---

## 9. Connection to our findings

**SUPPORTS partially / EXTENDS** — Hembre даёт независимый канал (tax compensation) для нашего β_top5 = −0.098 (p = 0.022), но не подтверждает напрямую.

Наш H7 ("top-5 market premium") rejected anti-direction — мы находим discount, а не premium. Hembre offers одно из возможных объяснений: top-5 markets (LAL, LAC, GSW в CA, NYK, BRK в NY, CHI в IL) — преимущественно high-tax states, и наблюдаемый "market discount" может быть на самом деле tax-driven compensating differential, который мы атрибутируем market size из-за коллинеарности. Хорошо для нашего Discussion: вместо одного channel ("anti-marketability") можно говорить про **bundle of channels** — tax + cost-of-living + perceived endorsement substitution.

Однако строго scientific:
- Hembre's NBA-only coefficient — null. Так что мы не можем сказать, что наш result "follows Hembre" без caveat.
- Лучшая формулировка для Discussion: "Hembre (2021) provides a *theoretical channel* (tax compensating differential under free agency) consistent with our finding direction, although his NBA-specific estimates are imprecise."

---

## 10. Reading notes / questions for follow-up

- **Title / DOI mismatch** (см. предупреждение в начале). Возможно, в JSE 2021 published version называется иначе ("Tax Competition in Professional Sports: A Theoretical and Empirical Analysis") и содержит **theoretical extension** (нет в preprint), что объясняет разный title. Кириллу — проверить через Sage/Sage Plus или email автору.
- Альтернативный fallback к данным: Kahn (2007) или Alm, Kaempfer & Sennoga (2012) — также про tax effects в MLB; могут быть добавлены в `additional_proposals.md` если Hembre для NBA окажется недостаточным.
- В Discussion стоит подчеркнуть, что наш канал — market-size dummy, не tax rate directly. Если есть время, попробовать robustness spec: добавить в M_full state tax rate как continuous control и посмотреть, "съедает" ли он top-5 coefficient. Это была бы более прямая проверка Hembre channel против market-size channel. (Если такой spec уже есть в analysis_v2 — указать на неё.)

---

**Заполнено:** 2026-05-22
**Заполнил:** Artem (collaborator)
