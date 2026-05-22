# Bodvarsson & Brastow (1998) — Do Employers Pay for Consistent Performance? Evidence from the NBA

> ⚠ **Skeleton only — Wiley paywall.** Verified citation via Crossref 2026-05-22 (DOI `10.1111/j.1465-7295.1998.tb01702.x`); abstract + secondary descriptions сверены через RePEc IDEAS. Full text за Wiley paywall; HSE library proxy будет полезен для verbatim quotes.

---

## 1. Citation (APA)

Bodvarsson, Ö. B., & Brastow, R. T. (1998). Do employers pay for consistent performance?: Evidence from the NBA. *Economic Inquiry, 36*(1), 145–160. https://doi.org/10.1111/j.1465-7295.1998.tb01702.x

---

## 2. Source metadata

- **Type:** empirical (regression analysis on NBA player-season data)
- **Sample:** NBA players late 1980s – mid 1990s (точный период — нужен full text)
- **Method:** OLS regression of salary on player productivity + **variance of performance** measures (variability/consistency)
- **Pages used in this summary:** abstract + Crossref metadata + RePEc secondary description
- **DOI / URL:** https://doi.org/10.1111/j.1465-7295.1998.tb01702.x
- **Access status:** Wiley paywall (403 при direct DOI download)
- **Local file:** — (не скачано)

---

## 3. Use mapping (КРИТИЧНО для интеграции)

- **Stream:** Б+ (NBA, replacement for failed Robst 2011 entry в proposal)
- **Section in coursework:** Discussion §5.x — interpretation of H10 (durability discount); Lit Review §2.6 (Stream 5: health / risk / variability)
- **Supports hypothesis(es):** H10 (durability discount, β = −0.005/game)
- **Specifically supports argument:** Bodvarsson & Brastow первыми эмпирически показали, что **consistency** (низкая variance производительности) положительно вознаграждается в NBA — менеджеры готовы платить premium за предсказуемость. Это **точный theoretical antecedent** для нашего H10 finding: пропуски игр (games_missed) — это форма inconsistency, и наш −0.5% salary per missed game можно интерпретировать как cost of inconsistency, не только risk-discount.

---

## 4. Core thesis (3-5 предложений, на основе abstract + secondary)

Authors test whether NBA managers reward consistent performance (низкую variance в производительности) или valoriize peak / high-output performance независимо от volatility. Используя panel игроков с individual measures of performance variance, они находят, что после контроля основной productivity, players с более консистентным выступлением получают statistically significant premium. Authors суmgest, что inconsistent игроки earn менее потому что менеджмент несёт monitoring cost — нужно отслеживать когда они "на пике" vs "на спаде". Это interpretation согласуется с moral hazard frameworks (Hölmström 1979) и provides empirical foundation для understanding почему predictable players are valued.

---

## 5. Key claims for our text (нумерованный список)

1. **Consistency premium exists in NBA salaries** — players с lower performance variance earn statistically significant premium after controlling for mean performance. (Magnitude: нужен full text для precise number.)

2. **Monitoring cost interpretation** — authors interpret consistency premium как proxy для reduced monitoring/management cost: predictable players require less oversight.

3. **Theoretical link к moral hazard** — взаимосвязь с Hölmström (1979) framework: variability в performance — это signal noise, который complicates incentive contract design.

---

## 6. Direct quote candidates (с page numbers)

> ⚠ Full text за paywall — verbatim quotes недоступны. Для финальной курсовой Кириллу — либо через HSE Wiley proxy, либо парафразный cite с указанием pp. 145-160 общим диапазоном.
>
> Из abstract / secondary sources: "We find that the NBA labor market rewards consistent performance" (paraphrase from RePEc).

---

## 7. Methodological notes

Не применимо — empirical paper, методы стандартные OLS. Не методологическая работа.

---

## 8. Limitations / caveats

1. **Data dated** (late 1980s — mid 1990s) — pre-1995 CBA structure; not directly comparable к нашей post-2011/2017 CBA era. Используется как theoretical anchor, не как direct empirical parallel.
2. **Consistency proxy not equal to durability** — Bodvarsson-Brastow measure variance in performance (statistical inconsistency игры-к-игре); наш durability measure — games missed (отсутствие игры вообще). Concept related, но не identical.
3. **Sample size небольшая** (~10-летний период NBA labor market).

---

## 9. Connection to our findings

**SUPPORTS (theoretical replacement for proposal'd Robst 2011)** — Bodvarsson-Brastow дают **proper empirical anchor** для нашего H10 finding (durability discount).

Наш result: games_missed_lag1 → −0.005/game, что транслируется в −15% salary за 30 пропусков (см. SHIPPING_SUMMARY). B&B 1998 — единственная classical NBA paper, которая прямо тестирует **consistency premium** в зарплатах. Наш H10 — это **расширение** их results на duration dimension (games missed vs game-to-game stats variance):

- **B&B 1998:** managers reward statistical consistency
- **Our H10:** managers reward availability consistency (durability)

В Discussion §5.6 (или соответствующем sub-section) — указать B&B как theoretical predecessor, наш durability finding — extension к durability axis.

---

## 10. Reading notes / questions for follow-up

- **PDF acquisition:** Wiley paywall. Альтернативы: HSE library proxy, contact автора Ö. B. Bodvarsson (был на St. Cloud State University; сейчас может быть в other affiliation), Sci-Hub (если разрешено локально).
- **Replacement justification:** в `bibliography_proposal.md` под Б6 указан Robst et al. (2011) "Skill, performance variability, and salary in the NBA" (JSM 25(5), 510-516) — этот paper НЕ СУЩЕСТВУЕТ в индексированных источниках (verified Crossref/JSTOR/GoogleScholar 2026-05-22). Bodvarsson-Brastow (1998) — **точный замещение по аргументу** (consistency premium в NBA salaries). Claude-K already dropped Robst в commit `2baa0eb`; рекомендую Кириллу добавить B&B 1998 в `bibliography_proposal.md` Б6 entry на место Robst.
- **Alternative replacement:** Deutscher & Büschemann (2016) "Does Performance Consistency Pay Off Financially? Bundesliga" — но это football, не NBA; B&B 1998 — более close match.

---

**Заполнено:** 2026-05-22 (skeleton, paywall)
**Заполнил:** Claude-A (Artem-side)
