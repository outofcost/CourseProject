# Project context — NBA salaries econometrics coursework

Этот файл — контекст для Claude Code / других AI-помощников, работающих над проектом. Автоматически подгружается Claude Code в каждую сессию.

---

## Что это за проект

Курсовая работа 3 курса HSE (Quantitative Economics) по эмпирическому анализу факторов зарплат игроков NBA. Формат: **Article (Empirical)** по гайдлайну HSE term paper.

**Тема:** Эконометрический анализ факторов, определяющих зарплату NBA-игрока в эпоху post-2011 CBA.

**Период:** сезоны 2015/16 – 2023/24 (9 сезонов).

**Сэмпл:** 953 уникальных игрока × 9 сезонов = 3 660 player-seasons.

**Источники данных:**
- Basketball-Reference (statistics, awards, birth metadata, team records) — scraped через curl_cffi для обхода Cloudflare TLS-fingerprint
- Hoopshype (исторические salary snapshots) — через Wayback Machine
- Manual CSV: market_size (Nielsen DMA + MSA population), cba_thresholds (по сезонам)
- Hand-coded: contract tier classifier (8 категорий, rule-based по CBA)

---

## Структура репозитория

```
курсач/
├── CLAUDE.md                    ← этот файл (контекст для AI)
├── README.md                    ← публичный README (для людей)
├── .gitignore
├── data/
│   ├── clean/                   ← v1 и v2 финальные датасеты
│   │   ├── data_analysis_v1.csv (3660 × 100, baseline)
│   │   └── data_analysis_v2.csv (3660 × 153, extended)
│   └── raw/                     ← промежуточные scraped artifacts
├── analysis_v1/                 ← код baseline-итерации (v1)
├── analysis_v2/                 ← код расширенной итерации (v2)
│   ├── data_collection/         ← scrapers + manual CSVs
│   ├── prep_v2.py               ← merge с safe_join + hash check
│   ├── regress_test_v1.py       ← регресс-тест воспроизводимости v1
│   ├── validation_v2.py
│   ├── classify_tier.py
│   ├── derive_*.py              ← awards features, durability
│   ├── m1_full.py               ← M1c-full + 4 варианта
│   ├── h_decomposition.py       ← Sequential + Shapley R²
│   ├── h8_market.py, h9_tier.py, h10_awards.py, h11_durability.py
│   ├── figures.py               ← 7 рисунков × (PDF + PNG)
│   ├── output/
│   │   ├── tables/              ← 30+ regression tables
│   │   └── figures/             ← PDF + PNG @ 300dpi
│   └── reports/                 ← markdown drafts + index
│       ├── SHIPPING_SUMMARY.md  ← главный индекс
│       ├── hypotheses_v2_final.md
│       ├── bibliography_proposal.md
│       ├── chapter_4_new_sections.md
│       ├── chapter_5_discussion.md
│       ├── chapter_6_conclusion.md
│       ├── abstract.md (RU + EN)
│       └── methodology_v2_addendum.md
├── version 3/                   ← план работы (plan3.md + todo3.md)
└── coursework/                  ← финальный .docx/.tex (формируется)
```

---

## Текущий статус (2026-05-22)

**Завершено (Phases 0-5):**
- Сбор данных: 7 источников, все блоки интегрированы
- Регресс-тест воспроизводимости v1 PASSED (max coef diff < 5×10⁻⁵)
- Эконометрика: 23 спецификации, включая Shapley декомпозицию (2⁹=512 фитов)
- Драфты глав 4, 5, 6 в markdown
- 7 рисунков (PDF + PNG)
- Гипотезы H1-H10 зафиксированы (см. `analysis_v2/reports/hypotheses_v2_final.md`)

**Осталось (Phase 6 + текст):**
- Переписать драфты под HSE Article Empirical format (Russian, APA citations)
- Структура: Introduction (15%) → Lit Review (20%, ending with hypotheses) → Methods (25%) → Results (15%, NO interpretation) → Discussion (15%) → Conclusion (10%)
- Bibliography в APA, ~25-30 источников
- AI Disclosure section
- Spell-check, final PDF

---

## Headline findings (для контекста)

1. **Shapley R² декомпозиция (главный методологический вклад):**
   - Performance + Age = 65.5% объяснённой дисперсии
   - Awards = 12.2%, Demographics = 14.1%, Durability = 5.7%
   - Market + Team + Structural + International ≈ 2.4%

2. **Tier dummies одни дают R² = 0.85** — institutional layer near-deterministic (H3 ✅)

3. **Anti-marketability:** β_top5 = −0.098 (p = 0.022), не premium а discount (H7 ❌ rejected anti-direction; consistent with Hembre 2021)

4. **Awards channel с лагом:** event study τ=+2 → +21%, τ=+3 → +22% — contract renewal cycle (H6 ✅)

5. **Aging-veteran discount:** multi_all_nba (≥3) β = −0.22 (sub-finding)

6. **Durability:** −0.5% salary за пропущенный матч (H10 ✅)

7. **Team controls null:** W%, playoffs, luxury tax все p > 0.15 (H8 ❌ informative null)

8. **Hypothesis status:** 7/10 проходят BH-FDR @ 5%; 5/10 проходят Bonferroni.

---

## Ключевые методологические решения

- **TOT-rows (~14% сэмпла):** оставлены NaN в team/market спецификациях; объяснено в Methods
- **age + age² + experience:** оставлены вместе; альтернатива no_collinear с drop experience доступна как robust spec
- **M10 awards specifications:** M10a (cumulative) + M10b (supermax substitution) — две альтернативы (collinearity r=0.78 между all_nba_lag1 и supermax_eligible_loose)
- **Top5_market** = {LAL, LAC, NYK, BRK, CHI, GSW} — фикс из плана, 6 команд
- **Shapley** предпочтительнее Sequential R² как main метод декомпозиции (axiomatically justified order-independent)
- **Robust awards spec:** binary indicators (has_career_allstar / multi_all_nba) — для разделения "ever-elite" премии и aging-vet penalty

---

## Reproducibility

End-to-end pipeline восстанавливается командами в `analysis_v2/reports/SHIPPING_SUMMARY.md`. Cold cache ~2 часа (scraping доминирует), warm cache ~3 минуты.

**КРИТИЧНО:** перед любыми изменениями в analysis_v2 запускать `python3 -m analysis_v2.regress_test_v1` — он должен PASS с max diff < 5×10⁻⁵. Это гарантия, что v2-расширение не ломает v1 baseline.

---

## Окружение

- Python 3.13 + `requirements.txt` в корне
- Ключевые пакеты: `pandas`, `numpy`, `statsmodels`, `linearmodels`, `curl_cffi`, `beautifulsoup4`, `matplotlib`
- Виртуальное окружение в `.venv/` (gitignored — пересоздать через `pip install -r requirements.txt`)

---

## Что НЕ нужно делать без согласования

- **Не пересчитывать** Shapley/bootstrap — это headline result, числа в драфтах уже соответствуют output/tables/
- **Не менять** список Top5_market — фикс из плана
- **Не выкидывать** TOT-rows полностью — они в основной спецификации (M1c_full), исключаются только в team/market spec
- **Не переименовывать** колонки v1 (`ln_salary`, `ppg`, `age`, `age_sq`, `experience`, `post_cba_2017`) — иначе сломается regress_test_v1
- **Не вносить** правки в `data/clean/data_analysis_v1.csv` — он frozen baseline; v2 строится на копии

---

## Стиль текста

- **Язык курсовой:** русский
- **Цитирование:** APA
- **Тон:** академический, без overclaiming, без эмоций
- **Уровень:** 3 курс бакалавриата, не PhD — методы оставляем (они корректно применены), но **экспозиция** простая, без формальных теорем; Shapley объясняется словами "axiom-обоснованная справедливая атрибуция", а не через теорему Шепли 1953
- **Объёмы по гайдлайну HSE:** 55-70 страниц финального текста

---

## Контакт / ownership

- Owner: Karolina303 / kohanov.kirill@gmail.com
- Collaborator работает над bibliography (полные тексты статей из `bibliography_proposal.md`) и финальной редактурой
