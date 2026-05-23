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
