# NBA Salaries — эмпирический анализ (курсовая 3 курс HSE)

Эконометрический анализ факторов, определяющих зарплаты игроков NBA в эпоху post-2011 CBA.

**Период:** сезоны 2015/16 – 2023/24
**Сэмпл:** 953 уникальных игрока × 9 сезонов = 3 660 player-seasons
**Финальный датасет:** 153 переменных в 7 тематических блоках

---

## Главный результат

Декомпозиция Shapley R² на 9 блоков факторов:

| Блок | Доля объяснённой дисперсии |
|---|---|
| Performance | 36.8% |
| Age + Experience | 28.7% |
| Demographics | 14.1% |
| Awards | 12.2% |
| Durability | 5.7% |
| International / Team / Structural / Market | ≈ 2.4% |

Salary cap создаёт quasi-deterministic institutional layer: tier dummies одни дают R² = 0.85.
Market-size premium отсутствует — обнаружен дисконт ~10% для крупных рынков (anti-marketability, согласуется с Hembre 2021).

Из 10 ключевых гипотез 7 подтверждаются при контроле multiple testing (BH-FDR 5%).

---

## Структура

```
курсач/
├── data/clean/                  Финальные датасеты (v1 baseline + v2 extended)
├── analysis_v1/                 Код v1 (baseline)
├── analysis_v2/                 Код v2 (extended)
│   ├── data_collection/         Скрейперы Basketball-Reference + manual CSV
│   ├── *.py                     Pipeline: prep, validation, m1_full, h_*, figures
│   ├── output/                  Таблицы регрессий + рисунки
│   └── reports/                 Драфты глав + аналитические заметки
├── version 3/                   План работы (plan3.md, todo3.md)
└── CLAUDE.md                    Контекст для AI-помощников
```

---

## Быстрый старт

```bash
# Виртуальное окружение
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Регресс-тест воспроизводимости v1 (должен PASS с max diff < 5e-5)
python3 -m analysis_v2.regress_test_v1

# Главная аналитика
python3 -m analysis_v2.m1_full
python3 -m analysis_v2.h_decomposition    # Shapley + bootstrap, ~90 sec
python3 -m analysis_v2.figures            # 7 рисунков → output/figures/
```

Полный pipeline с холодного кэша — ~2 часа (преобладает scraping). С тёплым кэшем — ~3 минуты. Полный список команд в `analysis_v2/reports/SHIPPING_SUMMARY.md`.

---

## Воспроизводимость

- v1 датасет: SHA256 в `analysis_v2/reports/v1_snapshot.sha256`
- v2 датасет: SHA256 в `analysis_v2/reports/v2_snapshot.sha256`
- Регресс-тест: `regress_test_v1.py` гарантирует, что v2-расширение не ломает v1 baseline (max coef diff < 5×10⁻⁵ на M1a-M1d)

---

## Ключевые методы

- Mincer earnings function с year fixed effects и cluster-robust SE (на player_id)
- Two-way fixed effects panel models (player + season)
- Shapley R² декомпозиция (2⁹ = 512 subset-фитов, axiom-justified)
- Sequential R² + cluster bootstrap CI (200 reps)
- Wild-cluster bootstrap (Rademacher, 1000 reps) для interaction коэффициентов
- Event study вокруг первого All-NBA (τ ∈ {−2 ... +4})
- Oster (2019) δ-sensitivity для OVB robustness
- Multiple testing corrections: Bonferroni + BH-FDR

---

## Дисциплина / специализация

3 курс бакалавриата HSE, Quantitative Economics. Формат: HSE term paper, Article (Empirical).

---

## Лицензия

MIT — свободное использование с указанием авторства.
