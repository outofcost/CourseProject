# {Author Year} — {Short title}

> Заполнить все секции. Если данных нет в статье — писать "не указано в статье" (не выдумывать).

---

## 1. Citation (APA)

{Полная APA-ссылка с DOI/URL, например:
Hembre, E. (2021). Tax Competition in Professional Sports: A Theoretical and Empirical Analysis. *Journal of Sports Economics, 22*(3), 280–304. https://doi.org/10.1177/1527002520968551}

---

## 2. Source metadata

- **Type:** [empirical / theoretical / review / methodological / institutional / mixed]
- **Sample (если empirical):** {период, sample size, страна}
- **Method (если empirical/methodological):** {OLS, panel FE, IV, bootstrap, theory model, ...}
- **Pages used in this summary:** {1-15 / first 5 + section 4 / ...}
- **DOI / URL:** {ссылка}
- **Access status:** [open access / institutional / preprint / Sci-Hub]

---

## 3. Use mapping (КРИТИЧНО для интеграции)

- **Stream (из bibliography_proposal):** [А: методы / Б: NBA / В: классика labor / Г: классика NBA empirics / Д: institutional]
- **Section in coursework:** [Introduction / Literature Review §{stream X} / Methods §{X} / Discussion §{X} / Limitations]
- **Supports hypothesis(es):** [список H1-H10, или "none — used for context only"]
- **Specifically supports argument:** {1-2 предложения, какой именно тезис в нашей курсовой эта статья обосновывает}

Пример хорошего заполнения:
> Stream: Б (NBA-specific). Section: Discussion §5.4 (market context). Supports: H7. Argument: "Anti-marketability — игроки в крупных рынках получают discount, а не premium, из-за компенсации через off-court доход и более высокого state tax."

---

## 4. Core thesis (3-5 предложений)

{Что paper claims, какая методология, какой sample, главный finding. Без воды.}

---

## 5. Key claims for our text (нумерованный список)

Конкретные claims с поддерживающими цифрами / выводами из статьи.

1. {Claim} — {evidence, например: "β = -0.08, p < 0.05, n = 4 200, sample 1990-2018"}
2. {Claim} — {evidence}
3. ...

---

## 6. Direct quote candidates (с page numbers)

Verbatim цитаты, которые можно вставить в нашу курсовую. Минимум 1, максимум 4.

> "Quote text here." (p. X)

> "Another quote." (p. Y)

---

## 7. Methodological notes

**Заполняй ТОЛЬКО если статья методологическая** (Cameron-Gelbach-Miller, Lipovetsky-Conklin, Oster, BH, MacKinnon-Webb). Для остальных — пропускай.

- **Method name:** {cluster bootstrap / Shapley value / δ-sensitivity / FDR / wild bootstrap}
- **Key formula / definition:** {если применимо, в LaTeX}
- **Key assumption(s):** {что должно выполняться, чтобы метод работал}
- **Where applicable in our work:** {ссылка на конкретный скрипт в analysis_v2/}
- **Caveat / pitfall:** {типичная ошибка применения}

---

## 8. Limitations / caveats

Что в статье weak. Что НЕЛЬЗЯ из неё заявлять. Это нужно для Discussion и Limitations нашей курсовой.

1. {Limitation 1}
2. {Limitation 2}

---

## 9. Connection to our findings

[supports / contradicts / extends / parallels / not directly relevant]

Объяснение в 2-4 предложениях. Опирайся на наши findings из `analysis_v2/reports/SHIPPING_SUMMARY.md`.

Пример:
> SUPPORTS. Hembre (2021) находит ~5-7% discount для high-tax states; наш результат β_top5 = −0.098 (p=0.022) идёт в ту же сторону, но через market-size, а не state-tax канал. Это позволяет нам интерпретировать anti-marketability как комбинированный эффект tax + cost-of-living + endorsement substitution.

---

## 10. Reading notes / questions for follow-up

Свободные комментарии: что осталось непонятным, на что нужно перепроверить позднее, дополнительные источники из библиографии этой статьи, которые могут быть нам полезны.

---

**Заполнено:** {date YYYY-MM-DD}
**Заполнил:** {colleague's name}
