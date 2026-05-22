# Onboarding для нового Claude Code на втором компьютере

> Что сделать, чтобы новая сессия Claude Code (на твоём втором компьютере или у Артёма) поняла проект и начала работать в общем процессе.

---

## Шаг 0 — Установить инструменты (на новом компьютере, один раз)

```bash
# Python 3.13+ должен быть установлен
python3 --version

# Установить Claude Code (если ещё нет)
# Инструкции: https://claude.com/claude-code
# либо через npm: npm install -g @anthropic-ai/claude-code

# git должен быть установлен
git --version
```

## Шаг 1 — Склонировать репо

```bash
cd ~/projects  # или куда хочешь
git clone https://github.com/outofcost/CourseProject.git
cd CourseProject
```

## Шаг 2 — Установить зависимости (если будешь запускать код)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Если ты только пишешь текст и не запускаешь регрессии — Шаг 2 можно пропустить.

## Шаг 3 — Открыть Claude Code в папке репо

```bash
cd ~/projects/CourseProject
claude
```

(или открыть папку в VS Code → расширение Claude Code).

CLAUDE.md автоматически подгрузится в каждую сессию — это даёт полный контекст проекта.

## Шаг 4 — Onboarding-prompt (вставить в первое сообщение Claude Code)

Скопируй и вставь этот текст в первое сообщение Claude Code:

```
Я работаю над курсовой работой по NBA salary econometrics на втором
компьютере. Прочитай следующие файлы для понимания контекста и
текущего статуса:

1. CLAUDE.md — общий контекст проекта
2. coordination/PROTOCOL.md — правила взаимодействия двух Claude'ов
3. coordination/TASKS.md — текущая очередь задач
4. coordination/FOR_KAROLINA.md (если есть) или coordination/FOR_ARTEM.md —
   обновления для нашей роли
5. bibliography/findings_log.md — журнал substance-changing находок
6. analysis_v2/reports/SHIPPING_SUMMARY.md — главный индекс работы

Моя роль — [ВЫБРАТЬ: Claude-K (Karolina, главы курсовой) ИЛИ Claude-A
(Artem, библиография)].

После чтения сделай brief summary (5-10 строк): где мы сейчас, какие
TASK'и pending в моей очереди, есть ли HUMAN_REVIEW флаги. Дальше жди
моего prompt'а.
```

Замени `[ВЫБРАТЬ...]` на свою роль:
- **Claude-K** — работа над главами в `analysis_v2/reports/chapter_*.md`, методологией, abstract, финальной редактурой.
- **Claude-A** — работа над библиографией в `bibliography/sources/`, поиск PDF, заполнение шаблонов из `bibliography/TEMPLATE.md`.

## Шаг 5 — (Опционально) Поставить cron для автономного цикла

Если хочешь, чтобы новый Claude Code сам каждые 10 минут pull'ил и обрабатывал задачи (как наш текущий cron 77e17451):

В Claude Code вставь:

```
Поставь CronCreate каждые 10 минут (off-minute schedule, e.g.
"7,17,27,37,47,57 * * * *") с этим prompt'ом:

[Скопируй prompt из примера ниже]
```

**Prompt для Claude-K cron (главы):**

```
Autonomous coursework cycle (Claude-K side). Steps:
1. cd /path/to/CourseProject; git pull origin main
2. Read coordination/TASKS.md, bibliography/findings_log.md
3. If new bibliography/sources/ files — integrate findings, apply
   targeted fixes to chapter_*.md only if critical
4. Pick ONE pending task from coordination/TASKS.md "Claude-K queue"
5. Execute it. Lane: analysis_v2/reports/*.md only.
6. If uncertain → HUMAN_REVIEW flag, no commit
7. If clean → commit with [Claude-K] prefix + push
End cycle after one task.
```

**Prompt для Claude-A cron (библиография):**

```
Autonomous bibliography cycle (Claude-A side). Steps:
1. cd /path/to/CourseProject; git pull origin main
2. Read bibliography/README.md, bibliography/TEMPLATE.md,
   coordination/TASKS.md, coordination/FOR_ARTEM.md
3. Pick ONE pending source from "Claude-A queue" or
   bibliography_proposal.md
4. Find PDF (if missing) → save to bibliography/pdfs/
5. Fill template from bibliography/TEMPLATE.md → save to
   bibliography/sources/{author_year}.md
6. If finding is substance-changing (wrong DOI, NBA-specific
   insignificant, surprising number) — note in
   bibliography/findings_log.md
7. Commit with [Claude-A] prefix + push
End cycle after one source.
```

⚠ Cron job — session-only по умолчанию. Если хочешь, чтобы он переживал restart сессии, попроси Claude `durable: true` при создании.

## Шаг 6 — Lane-дисциплина

| Owner | Может править | НЕ может править |
|---|---|---|
| **Claude-K** | `analysis_v2/reports/chapter_*.md`, `analysis_v2/reports/abstract.md`, `analysis_v2/reports/ai_disclosure.md`, любой код в `analysis_v2/`, `coordination/TASKS.md` (свои строки), `coordination/FOR_ARTEM.md` | `bibliography/sources/*`, `bibliography/pdfs/*` |
| **Claude-A** | `bibliography/sources/*`, `bibliography/pdfs/*`, `bibliography/findings_log.md`, `coordination/TASKS.md` (свои строки), `coordination/FOR_KAROLINA.md` | `analysis_v2/reports/chapter_*.md`, код в `analysis_v2/` |

Полные правила — в `coordination/PROTOCOL.md`.

## Шаг 7 — Git workflow

Перед началом любой работы:
```bash
git pull origin main
```

После каждого смыслового блока:
```bash
git add <specific-files>  # не -A, чтобы не зацепить чужие изменения
git commit -m "[Claude-K|Claude-A] <action> <what>"
git push origin main
```

**НЕ делать:**
- `git push --force` — никогда.
- `git add -A` или `git add .` — стейджит всё, включая чужие изменения.
- Править файлы вне своей lane без явной задачи в TASKS.md.

## Шаг 8 — Если упрусь в нерешаемое

В `coordination/TASKS.md` под раздел `## HUMAN_REVIEW queue` добавить:

```
### TASK-NN: HUMAN_REVIEW
**Owner:** Karolina (или Artem)
**Blocker for:** TASK-MM
**Question:** {конкретный вопрос с контекстом}
**Options I see:** {что я мог бы выбрать}
**My recommendation:** {если есть}
```

Затем останавливаюсь без коммита спорного контента. Жду pull'ом от человека.

---

## Быстрый troubleshooting

| Симптом | Что делать |
|---|---|
| `git pull` — conflict | Не пытайся merge'ить сам. Прочитай конфликтующие файлы, флагуй HUMAN_REVIEW. |
| Cron не fire'ит | Проверь `CronList`. Cron работает только когда Claude idle — если он непрерывно работает, fire откладывается. |
| Артём пушит в analysis_v2/reports/ | Это нарушение lane. Пиши в coordination/TASKS.md в HUMAN_REVIEW, не правь самостоятельно. |
| Не уверен, чьи это правки в TASKS.md | Смотри commit history: `git log -p coordination/TASKS.md` — там видно, какой Claude писал какие строки (по prefix [Claude-K] / [Claude-A]). |
| Контекст переполнен в сессии | Закончи текущий task, commit + push, скажи user'у "context full, halting". Новая сессия подхватит через CLAUDE.md + coordination/. |

---

**Версия:** v1 (2026-05-22). Изменения — через PR с обоснованием.
