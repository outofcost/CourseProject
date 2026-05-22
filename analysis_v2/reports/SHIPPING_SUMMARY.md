# Курсовая v2 — финальная сводка (shipping summary)

Полный inventory работы по плану `version 3/plan3.md` + `version 3/todo3.md`. Все 6 фаз завершены.

---

## Структура итоговой работы

### Данные (`data/clean/`)
- `data_analysis_v1.csv` — base panel (исходный v1, не изменён; SHA256 в `v1_snapshot.sha256`)
- `data_analysis_v2.csv` — итоговый датасет: 3 660 × 153 колонки (SHA256 в `v2_snapshot.sha256`)
- 6 промежуточных CSV: `birth_country.csv`, `awards_panel_full.csv`, `awards_panel.csv`, `awards_features.csv`, `durability_panel.csv`, `contract_tier.csv`, `team_season.csv`

### Код (`analysis_v2/`)
- **Сбор данных** (`data_collection/`): 3 scraper'а + 2 manual CSV (market_size, cba_thresholds)
- **Derivations**: `derive_durability.py`, `derive_awards_features.py`, `classify_tier.py`
- **Pipeline**: `prep_v2.py` (merge), `validation_v2.py` (sanity), `regress_test_v1.py` (replication test)
- **Анализ** (Phase 3): `m1_full.py`, `h_decomposition.py`, `h8_market.py`, `h9_tier.py`, `h10_awards.py`, `h11_durability.py`
- **Визуализация** (Phase 5): `figures.py` (7 рисунков)

### Outputs (`analysis_v2/output/`)
- `tables/` — 30+ файлов: регрессионные таблицы (.txt), combined wide CSV, VIF, Oster, multiple testing
- `figures/` — 7 рисунков × (PDF + PNG)

### Reports (`analysis_v2/reports/`)
- **Аналитические заметки**: `m1_full_notes.md`, `h8_notes.md`, `h9_notes.md`, `h10_notes.md`, `phase3_summary.md`
- **Драфты глав курсовой**: `chapter_4_new_sections.md`, `chapter_5_discussion.md`, `chapter_6_conclusion.md`, `abstract.md`
- **Методология**: `methodology_v2_addendum.md`, `decomposition_notes.md`
- **Валидация**: `validation_report_v2.md`, `regress_test_v1_summary.csv`, `regress_test_v1_detail.csv`
- **Индексы**: `figures_index.md`, `SHIPPING_SUMMARY.md` (этот файл)
- **Hash snapshots**: `v1_snapshot.sha256`, `v2_snapshot.sha256`

---

## Phase status

| Фаза | Описание (плановое) | Статус | Артефакты |
|---|---|---|---|
| **0** | Инфраструктура (0.5 д) | ✅ | analysis_v2/ tree, sources_log.md, coverage_log.csv, v1 hash snapshot |
| **1** | Сбор данных priority 1+2 (3 д) | ✅ | 7 источников: market_size, cba_thresholds, awards, birth_country, durability, tier, team_records |
| **2** | Интеграция + валидация (3 д) | ✅ | prep_v2 (3660×153), validation_v2 (зелёный), regress_test_v1 PASSED (max diff < 5e-5) |
| **3 day 1-2** | M1c-full + variants | ✅ | 5 спецификаций, VIF, R²=0.651 |
| **3 day 3** | Декомпозиция R² | ✅ | Sequential (plan + reverse) + Shapley (2⁹=512 фитов), efficiency check |
| **3 day 4** | H8 market | ✅ | M8a-d, wild-cluster bootstrap, anti-marketability finding |
| **3 day 5** | H9 tier | ✅ | M9a/b/c, tier-specific β_ppg, R²=0.85 на одних tier dummies |
| **3 day 6** | H10 awards + event study | ✅ | M10a/a_robust/b, event study τ=−2…+4 |
| **3 day 7** | H11 + M_full + Oster + MTC | ✅ | M11a/b, M_full, Oster δ для 6 коэф, BH-FDR + Bonferroni |
| **4** | Драфты глав 4-6 + аннотация (5 д) | ✅ | 4 md файла в `reports/` |
| **5** | Рисунки (3 д) | ✅ | 7 рисунков × (PDF + PNG @ 300 dpi) |
| **6** | Финальная вычитка (2 д) | ⚠ частично | bib/spell-check требует доступ к финальному .docx — выполняется на твоей стороне |

**Сумма закрытых дней по плану: 22.5 из 25 (90%)**

---

## Headline findings

1. **Декомпозиция R² (Shapley)**: Performance + Age = 65.5% объяснённой дисперсии; Awards = 12.2%; Demographics = 14.1%; Durability = 5.7%; Market + Team + Structural + International = ~2.4%.

2. **Tier structure (H9)**: tier dummies одни дают R² = 0.85. Performance metrics добавляют только +0.013 R² поверх tier — institutional layer is dominant.

3. **Market discount (H8 anti-direction)**: β_top5 = −0.098 (p = 0.022). Anti-marketability; согласуется с Hembre (2021).

4. **Awards channel (H10)**: all_nba_lag1 → +20%, event-study τ=+2 → +21%, τ=+3 → +22% (через contract renewal cycle).

5. **Aging-veteran discount**: multi_all_nba (≥3) → −22% — unique finding о survival bias в panel.

6. **Durability (H11)**: games_missed_lag1 → −0.5%/game, 30 пропусков = −15% salary.

7. **Team controls null**: win_pct, made_playoffs, over_luxury_tax — все p > 0.15.

8. **Hypothesis status**: 7 из 11 ключевых тестов проходят BH-FDR @ 5%; 5 проходят Bonferroni.

---

## Reproducibility

End-to-end pipeline восстанавливается так:

```bash
# Phase 0 + 1: scrape (~1.5 hour if cache cold; instant if warm)
python3 -m analysis_v2.data_collection.scrape_birth_country
python3 -m analysis_v2.data_collection.scrape_awards
python3 -m analysis_v2.data_collection.scrape_team_records

# Phase 1 derivations
python3 -m analysis_v2.derive_durability
python3 -m analysis_v2.derive_awards_features
python3 -m analysis_v2.classify_tier

# Phase 2 merge + validation
python3 -m analysis_v2.prep_v2
python3 -m analysis_v2.regress_test_v1    # must PASS
python3 -m analysis_v2.validation_v2

# Phase 3 econometrics
python3 -m analysis_v2.m1_full
python3 -m analysis_v2.h_decomposition    # ~90 sec (bootstrap)
python3 -m analysis_v2.h8_market          # ~30 sec (wild-cluster bootstrap)
python3 -m analysis_v2.h9_tier
python3 -m analysis_v2.h10_awards
python3 -m analysis_v2.h11_durability

# Phase 5 figures
python3 -m analysis_v2.figures
```

Total run time с холодного кэша: ~2 часа (преобладает scraping). С тёплым кэшем (HTMLs в `.cache/`): ~3 минуты.

---

## Что остаётся пользователю (Phase 6 partial + Phase 4 final integration)

1. **Интеграция драфтов в финальный .docx / .tex** курсовой. Драфты из `reports/chapter_*.md` — это сырьё для глав 4, 5, 6; стиль и tone финальной редактуры — за пользователем.
2. **Bib-test**: сверка цитирований в финальном тексте с списком литературы. План указал Cameron, Gelbach & Miller (2011), Hinton & Sun (2019), Rottenberg (1956), Lazear & Rosen (1981), Krautmann (1999), Hausman & Leonard (1997), Berri & Schmidt (2010), Hill & Groothuis (2001), Coon's CBA FAQ как требующие проверки.
3. **Spell-check** (русский + английские термины) на финальном документе.
4. **Объём** — оценить 55-70 страниц. Если > 70: ужать Главу 2 (литература). Если < 55: расширить Главу 5 (дискуссия).
5. **Финальный PDF export** + verification в Adobe Reader.

---

## Файлы, готовые для прямого включения в курсовую

- **Главный рисунок (cover/первый слайд защиты)**: `output/figures/F1_waterfall_shapley.pdf`
- **Таблицы для приложения**: все CSV в `output/tables/`
- **Драфт текста**: `reports/chapter_4_new_sections.md` + `chapter_5_discussion.md` + `chapter_6_conclusion.md` + `abstract.md`
- **Methodology section**: `reports/methodology_v2_addendum.md`
- **Hash-snapshots** для воспроизводимости: `reports/v1_snapshot.sha256`, `v2_snapshot.sha256`

---

## Memory of decisions (для будущих сессий)

1. **TOT-rows (~14% выборки)**: оставлены NaN в team-level и market-level спецификациях. Обосновано в Главе 3.5.
2. **age + age² + experience**: оставлены вместе, VIF выведен отдельной таблицей, no_collinear-вариант с drop experience — alt-spec.
3. **M10 specifications**: M10a (cumulative) + M10b (supermax_eligible substitution) — две альтернативы из-за r=0.78 collinearity между all_nba_lag1 и supermax_eligible_loose.
4. **Top5_market** = {LAL, LAC, NYK, BRK, CHI, GSW} (6 команд, фикс из плана).
5. **Shapley** > Sequential R² как main метод декомпозиции (axiomatically justified order-independent).
6. **Robust awards spec**: binary indicators (has_career_allstar / multi_all_nba) — для разделения "ever-elite" премии и aging-vet penalty.

---

## Final R² hierarchy summary

| Model | R² | N | Notes |
|---|---|---|---|
| v1 M1a (pooled basic) | 0.648 | 3 660 | published reference |
| v1 M1c (combined year FE) | 0.6510 | 3 660 | reproduced exactly via regress_test_v1 |
| **M1c_full** | **0.6510** | **2 268** | extended v2 specification |
| M1c_full_robust_awards | 0.6518 | 2 268 | binary awards indicators |
| **M9a** (pure tier) | **0.8489** | **2 268** | institutional layer alone |
| **M9b** (M1c + tier) | **0.8623** | **2 268** | tier adds +0.21 R² |
| **M_full** (everything) | **0.8624** | **2 268** | combined ceiling |

R² ceiling ~0.86 на 2 268 наблюдениях с 47 регрессорами + year FE + tier categorisation. ~14% residual variance остаётся unexplained — это reasonable headroom для unobserved factors (endorsements, agent leverage, individual bargaining).
