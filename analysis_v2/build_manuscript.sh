#!/bin/bash
# Build manuscript_master.md from 8 chapter source files in HSE Article (Empirical) order.
# Strips front-matter callouts and footer wordcount/TBD markers.
# Output: analysis_v2/reports/manuscript_master.md
set -e

DIR="$(cd "$(dirname "$0")" && pwd)/reports"
OUT="$DIR/manuscript_master.md"

cat > "$OUT" <<'HEADER_EOF'
---
title: "Эконометрический анализ факторов, определяющих зарплату игрока NBA в эпоху post-2011 CBA"
subtitle: "Курсовая работа 3 курса"
author: "Karolina303"
institute: "НИУ ВШЭ, факультет экономических наук, программа «Экономика»"
year: "2025/2026"
format: HSE term paper — Article (Empirical)
---

HEADER_EOF

strip_chapter() {
    awk '
        /^\[Слов в главе/ { next }
        /^> Драфт под HSE/ { next }
        /^> Цитирования — APA/ { next }
        /^> Этот файл — way/ { next }
        /^> Реорганизация параллельно/ { next }
        /^> Обязательная секция согласно HSE/ { next }
        /^> Заменяет старый драфт/ { next }
        { print }
    ' "$1"
}

TITLE_PAGE="$(cd "$(dirname "$0")"/../coursework && pwd)/title_page.md"
if [ -f "$TITLE_PAGE" ]; then
    strip_chapter "$TITLE_PAGE" >> "$OUT"
    printf "\n\\\\newpage\n\n" >> "$OUT"
fi

strip_chapter "$DIR/abstract.md" >> "$OUT"
printf "\n---\n\n" >> "$OUT"

for f in chapter_1_introduction chapter_2_literature chapter_3_methods chapter_4_results chapter_5_discussion_v2 chapter_6_conclusion_v2; do
    strip_chapter "$DIR/$f.md" >> "$OUT"
    printf "\n---\n\n" >> "$OUT"
done

strip_chapter "$DIR/ai_disclosure.md" >> "$OUT"
printf "\n---\n\n" >> "$OUT"

strip_chapter "$DIR/references_apa.md" >> "$OUT"
printf "\n---\n\n" >> "$OUT"

cat >> "$OUT" <<'FIGTAB_EOF'

## Список рисунков

- **Рисунок 4.1.** Возрастной профиль логарифма реальной заработной платы по спецификации M1c (раздел 4.2).
- **Рисунок 4.2.** Эффект очков за игру внутри каждой категории контракта (раздел 4.3).
- **Рисунок 4.3.** Распределение логарифма реальной заработной платы по восьми категориям контракта (раздел 4.3).
- **Рисунок 4.4.** Событийное исследование вокруг первого попадания в All-NBA (раздел 4.4).
- **Рисунок 4.5.** Водопадная декомпозиция $R^2$ методом значения Шепли по девяти блокам факторов — главный методологический результат работы (раздел 4.9).
- **Рисунок 4.6.** Сравнение последовательной декомпозиции $R^2$ с декомпозицией значения Шепли (раздел 4.9).
- **Рисунок 4.7.** Лесная диаграмма главных эффектов полной спецификации M_full с 95-процентными доверительными интервалами (раздел 4.10).

## Список таблиц

- **Таблица 4.1.** Оценки коэффициентов базового расширения Минсера (раздел 4.2).
- **Таблица 4.2.** Иерархия $R^2$ для спецификаций категорий контракта (раздел 4.3).
- **Таблица 4.3.** Эффекты категорий контракта относительно среднего уровня (раздел 4.3).
- **Таблица 4.4.** Регрессии Минсера внутри категорий контракта (раздел 4.3).
- **Таблица 4.5.** Оценки коэффициентов канала наград (раздел 4.4).
- **Таблица 4.6.** Событийное исследование первого попадания в All-NBA (раздел 4.4).
- **Таблица 4.7.** Тесты гетерогенности эффекта крупного рынка (раздел 4.5).
- **Таблица 4.8.** Командные контроли в спецификации M1c_full (раздел 4.6).
- **Таблица 4.9.** Эффект подоходного налога штата (раздел 4.7).
- **Таблица 4.10.** Эффект устойчивости к травмам (раздел 4.8).
- **Таблица 4.11.** Декомпозиция $R^2$ методом значения Шепли по девяти блокам факторов (раздел 4.9).
- **Таблица 4.12.** Сравнение последовательной и Шепли-декомпозиций (раздел 4.9).
- **Таблица 4.13.** Контроль ошибки множественной проверки гипотез (раздел 4.10).
- **Таблица 4.14.** Иерархия спецификаций по объяснительной силе (раздел 4.11).

---

FIGTAB_EOF

cat >> "$OUT" <<'TAIL_EOF'

## Приложения

### Приложение A. Расширенные регрессионные таблицы

Полный набор регрессионных таблиц (30+ файлов) — `analysis_v2/output/tables/` в репозитории. Включает: M1a–M1d full coefficient panels, M9a/b/M_full tier specifications, M10a/b awards specifications, M11a/b durability specifications, event-study point estimates с pre-trend block, Shapley декомпозиция с эффективностью verified до $10^{-16}$, multiple-testing summary с Bonferroni и BH-FDR markers.

### Приложение B. Описательная статистика

См. `analysis_v2/output/tables/descriptive_stats.csv` — min/max/mean/median/sd для всех 153 переменных по полной выборке и subsamples (rookie / mid-tier / max / supermax; US-born / international; pre-CBA / post-CBA-2017).

### Приложение C. Воспроизводимость и аудит AI-коллаборации

Полная процедура воспроизведения вычислительного pipeline и аудита AI-вклада обеих сессий — `coordination/reproducibility_appendix.md`. Bundles:
- End-to-end run commands (cold cache ~2 часа, warm cache ~3 минуты).
- Hash-snapshots (SHA256) сырого и обработанного датасета.
- Git audit commands для проверки вклада каждой Claude-сессии.
- Lane-дисциплина и substance-affecting agent decisions с git refs.

### Приложение D. AI Disclosure commit log

Атомарный лог 35+ commit'ов обеих сессий — `coordination/ai_disclosure_commits_log.md`. Каждая запись: SHA, timestamp, agent (Claude-K / Claude-A), commit message.

---
TAIL_EOF

wc -l "$OUT" && wc -w "$OUT"
