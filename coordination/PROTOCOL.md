# Coordination protocol — Claude-K ↔ Claude-A

> **Claude-K** = Karolina's Claude Code (работает с главами, методологией, итоговым текстом).
> **Claude-A** = Artem's Claude Code (работает с библиографией, поиском источников, заполнением шаблонов).
> Async-координация через git. Этот файл — единственный source of truth для правил взаимодействия.

---

## Правило 1: Лейн-дисциплина

| Owner | Может править | НЕ может править |
|---|---|---|
| **Claude-K** | `analysis_v2/reports/chapter_*.md`, `analysis_v2/reports/abstract.md`, `analysis_v2/reports/ai_disclosure.md`, `analysis_v2/reports/methodology_v2_addendum.md`, `coordination/TASKS.md` (свои строки), любой код в `analysis_v2/` | `bibliography/sources/*`, `bibliography/pdfs/*` |
| **Claude-A** | `bibliography/sources/*`, `bibliography/pdfs/*`, `bibliography/findings_log.md` (новые batch'и), `coordination/TASKS.md` (свои строки) | `analysis_v2/reports/chapter_*.md`, код в `analysis_v2/` |
| **Любой** | `coordination/PROTOCOL.md`, `coordination/FOR_ARTEM.md`, `coordination/FOR_KAROLINA.md`, `CLAUDE.md`, `README.md` (но с пометкой в commit) | `data/clean/*` (frozen artifacts), `.gitignore` |

Если есть желание тронуть файл вне своей зоны — сначала пиши задачу в `TASKS.md` для другого Claude'а, не делай сам.

## Правило 2: Verification before claim

**Любое cite, число, page reference, DOI, formula** должно быть verifiable из:
- (a) исходного источника (PDF / HTML snapshot), доступного в `bibliography/pdfs/`;
- (b) либо нашего собственного output (`output/tables/`, `output/figures/`);
- (c) либо официальной онлайн-страницы с access date.

**Запрещено:** выдумывать DOI, page numbers, β-коэффициенты, R², прозвища авторов, годы публикаций. Если данных нет — пиши `[TBD: см. {author_year} {что нужно проверить}]` и ставь HUMAN_REVIEW флаг в `TASKS.md`.

**Прецедент:** Hembre (2021) — изначальный DOI в proposal был неверный (Crossref 404). Claude-A проверил и поймал. Этот тип verification — критичен.

## Правило 3: Auto-commit policy

Каждый Claude **сам** делает `git add` + `git commit` + `git push` после каждого смыслового блока работы. Не накапливаем uncommitted changes на дольше одной задачи.

**Commit message format:**
```
[Claude-K|Claude-A] <verb in present tense> <what>

<1-3 sentences about why / context>

Refs: TASK-NN (если работа по задаче из TASKS.md)
Confidence: high|medium|low — explain if not high

Co-Authored-By: Claude <model> <noreply@anthropic.com>
```

**При commit'е после HUMAN_REVIEW флага** — НЕ коммитим спорный контент; вместо этого пишем только в `coordination/TASKS.md` пометку и останавливаемся.

## Правило 4: HUMAN_REVIEW protocol

Когда Claude упирается в:
- неоднозначность интерпретации результата
- противоречие между источниками
- запрос, требующий substance-changing claims без основания
- что-либо, что может пройти всю цепочку как hallucinated fact

— то Claude **останавливается** и пишет в `coordination/TASKS.md`:

```
### TASK-NN: HUMAN_REVIEW
**Owner:** Karolina (требуется human input)
**Blocker for:** TASK-MM, TASK-LL
**Question:** {конкретный вопрос с контекстом}
**Options I see:** {1, 2, 3 — что я могу выбрать, если бы решал сам}
**My recommendation:** {если есть}
**Files touched (uncommitted):** {если были начаты правки}
```

**Не пушим uncommitted spec changes**; ждём ответа человека.

## Правило 5: Pull before work AND at start of every response

Каждый Claude перед началом любого изменения делает:
```bash
git pull origin main
```

**В активной чат-сессии — `git pull` в начале КАЖДОГО ответа user'у**, не только перед изменениями. Cron fires только в idle gaps; в active chat session cron почти не срабатывает, поэтому manual pull обязателен. Если pull показывает новые коммиты от другой стороны — упомянуть в первой строке ответа.

Если pull показывает конфликты (что не должно случиться при соблюдении лейн-дисциплины) — STOP и пиши HUMAN_REVIEW.

## Правило 6: Task ownership in TASKS.md

`coordination/TASKS.md` структурирован по owner:
- `## Claude-K queue` — задачи для Karolina's Claude
- `## Claude-A queue` — задачи для Artem's Claude
- `## HUMAN_REVIEW` — требует ответа человека
- `## Done (last 20)` — недавно завершённые, для контекста

Каждая задача имеет уникальный ID (TASK-01, TASK-02, ...). Не редактируем чужие задачи; не присваиваем себе задачи другого Claude'а без явной пометки от другого Claude.

## Правило 7: Cron + scheduled wakeup

Karolina's сессия использует `CronCreate` каждые 10 минут для self-poke:
- На каждом fire — pull, read TASKS.md, pick ONE pending task, execute, commit/push, end.
- 7-day expiry автоматический по cron tool.

Artem может настроить аналогичный cron в его сессии (опционально). Если не настроит — Claude-A работает только когда Artem явно prompt'ит.

## Правило 8: Когда останавливаться полностью

Claude-K останавливается до следующего ручного prompt'а от Karolina, если:
- Все его задачи в `Claude-K queue` либо `done`, либо в `HUMAN_REVIEW`;
- Или session context переполнен (само-сообщит "context full, halting").

Не выдумываем новые задачи без необходимости. Если queue пуст и нет HUMAN_REVIEW — просто ждём prompt'а.

---

**Версия протокола:** v1 (2026-05-22).
**Изменения:** через `git commit` с пометкой `[PROTOCOL]` в commit message; уведомление обоих Claude'ов через TASKS.md.
