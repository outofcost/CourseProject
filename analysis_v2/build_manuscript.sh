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

strip_chapter "$DIR/abstract.md" >> "$OUT"
printf "\n---\n\n" >> "$OUT"

for f in chapter_1_introduction chapter_2_literature chapter_3_methods chapter_4_results chapter_5_discussion_v2 chapter_6_conclusion_v2; do
    strip_chapter "$DIR/$f.md" >> "$OUT"
    printf "\n---\n\n" >> "$OUT"
done

strip_chapter "$DIR/ai_disclosure.md" >> "$OUT"
printf "\n---\n\n" >> "$OUT"

cat >> "$OUT" <<'TAIL_EOF'

## Список литературы

См. отдельный файл `bibliography/references.bib` (BibTeX) и `bibliography/MASTER_TABLE.md` (читаемый список с приоритетами). Финальный APA-bibliography текстом будет добавлен в Phase F при сборке .docx.

---

## Приложения

- **Приложение A.** Расширенные регрессионные таблицы — см. `analysis_v2/output/tables/` (30+ CSV-таблиц).
- **Приложение B.** Описательная статистика по выборке — см. `analysis_v2/output/tables/descriptive_stats.csv`.
- **Приложение C.** Hash-snapshots датасетов и регресс-тест воспроизводимости — см. `analysis_v2/regress_test_v1.py` и репозиторий.
- **Приложение D.** AI-coordination evidence: `coordination/` файлы (PROTOCOL, TASKS, FOR_*, MASTER_PLAN, findings_log) как audit trail двух Claude-инстансов.
TAIL_EOF

wc -l "$OUT" && wc -w "$OUT"
