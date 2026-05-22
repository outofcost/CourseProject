# Декомпозиция R² — методологические заметки

Этот файл собирает технические детали по поводу sequential R² vs Shapley декомпозиции, для использования в Главе 3.5 (Диагностики) и Главе 5.1 (Дискуссия).

---

## 1. Sequential R²

### Определение

При фиксированном порядке блоков {B₁, B₂, …, B_K}, последовательная атрибуция:

$$\Delta R^2_k = R^2(\{B_1, \ldots, B_k\}) - R^2(\{B_1, \ldots, B_{k-1}\})$$

Где R²(S) — R² OLS-регрессии ln_salary на регрессоры из блоков в S + константа.

### Свойства

- **Простота**: легко вычислить (K фитов).
- **Order-dependent**: ΔR²_k зависит от того, в каком порядке блоки добавлены. Это **серьёзная проблема** для интерпретации.
- **Efficiency**: сумма ΔR²_k = R²(полная модель) — выполняется тривиально.

### Bootstrap CI

Cluster bootstrap (Cameron, Gelbach & Miller, 2008):

1. Resample player_id с заменой, n_c раз (где n_c — число уникальных игроков).
2. Reconstruct полная панель из resampled clusters (повторение клиентов разрешено).
3. Пересчитать ΔR²_k на bootstrap-выборке.
4. Повторить 200 раз.
5. 95% CI = [2.5pct, 97.5pct] от bootstrap distribution.

Это **более консервативно**, чем naive percentile bootstrap, потому что учитывает intra-player correlation.

### Diagnostic value

Запуск sequential R² **в двух порядках** (plan-order и reverse) — диагностика чувствительности к порядку. На наших данных:

| Блок | Sequential plan-order | Sequential reverse |
|---|---|---|
| Awards | 0.006 (5-й) | 0.199 (5-й, считая от конца) |
| Performance | 0.446 (1-й) | 0.115 (9-й) |

**Огромная разница** для Awards (33× амплитуда) и Performance (4× амплитуда) — sequential R² **нельзя** использовать как final attribution.

---

## 2. Shapley R²

### Определение (Shapley 1953, Lipovetsky & Conklin 2001)

Для блока B_i:

$$\phi_i = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|! (|N| - |S| - 1)!}{|N|!} \cdot \left[ R^2(S \cup \{i\}) - R^2(S) \right]$$

где сумма — по всем подмножествам S из {B_1, …, B_K} ∖ {B_i}.

### Свойства (axioms)

1. **Efficiency**: ∑ φ_i = R²(полная модель).
2. **Symmetry**: если B_i и B_j вносят одинаковый marginal вклад в каждое S, то φ_i = φ_j.
3. **Dummy**: если B_i не меняет R² ни в каком S (нулевой блок), то φ_i = 0.
4. **Additivity**: φ_i линейно зависит от R²-функционала.

Shapley value — **единственный** allocation, удовлетворяющий всем четырём axioms.

### Computational cost

Для K блоков нужно 2^K subset-фитов. Для K = 9 это 2⁹ = 512 OLS-фитов. На наших данных (~2 268 строк × ~38 регрессоров max): ~10 секунд total.

### Проверка efficiency

В нашем выводе (см. `analysis_v2/output/tables/r2_shapley.csv`):

```
sum(shapley) = 0.6488
R²(full)    = 0.6488
diff        = 1.4e-16
```

Численная точность ~машинная ε. Efficiency выполнена.

---

## 3. Сравнение sequential и Shapley

### Совпадения

Performance и Age + Experience — крупнейшие блоки в обеих декомпозициях:

- Plan-order: Perf 0.446 (1-й), Age 0.169 (2-й)
- Shapley: Perf 0.239, Age 0.186

Sequential plan-order **завышает** Performance, потому что Performance включает все performance-correlated variance, включая ту, которая делится с Awards (и с Demographics, и с Durability).

### Главные расхождения

| Блок | Plan-order ΔR² | Reverse ΔR² | Shapley | Sequential range / Shapley |
|---|---|---|---|---|
| Performance | 0.446 | 0.115 | 0.239 | 1.4× |
| Awards | 0.006 | 0.199 | 0.079 | 2.5× |
| Demographics | 0.013 | 0.083 | 0.091 | 0.8× |
| Durability | 0.004 | 0.093 | 0.037 | 2.4× |

Awards и Durability — наиболее «спорные» блоки в terms of attribution. Sequential plan-order их недооценивает (потому что Performance, Age, Demographics добавляются первыми и абсорбируют общую вариацию). Reverse-order переоценивает (Awards добавляется до Performance и абсорбирует всю общую вариацию). Shapley даёт **fair** average.

### Альтернативы Shapley

Pratt (1987) и Genizi (1993) — другие order-independent декомпозиции. Не идентичны Shapley, но близки в практике. Для нашего набора блоков различия ≤ 2 п.п. share_of_explained, не меняют ранжирование. **Shapley предпочтительнее** для теоретической чистоты (4 axioms + uniqueness).

---

## 4. Интерпретация для Главы 5

1. **Performance dominates, but not as much as plan-order suggests.** Shapley показывает Performance = 36.8% explained variance, sequential plan-order давал 68.7%. Это **methodological correction** к "наивной" интерпретации Mincer-разбора.

2. **Awards / Demographics / Durability — реально содержательные блоки.** Их совместный shapley вклад = 32% explained variance. В sequential plan-order они кажутся «остаточными» (общий ΔR² ≈ 2%), но это артефакт порядка, не реальной структуры.

3. **Environmental controls (Market + Team + Structural + International) ≤ 2.4%.** Это устойчиво между порядками. **Реальный null**: окружение не влияет на индивидуальную цену после контроля игрока.

---

## 5. Воспроизводимость

Скрипт: `analysis_v2/h_decomposition.py`.

Запуск: `python3 -m analysis_v2.h_decomposition`.

Выводы:
- `output/tables/r2_decomposition.csv` — plan-order sequential
- `output/tables/r2_decomposition_with_ci.csv` — + 200-rep bootstrap CI
- `output/tables/r2_decomposition_reverse.csv` — reverse-order
- `output/tables/r2_shapley.csv` — Shapley decomposition

Время выполнения: ~90 sec (bootstrap dominates, Shapley itself ~10 sec).
