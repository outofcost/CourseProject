# Coordination: bibliography vs. coursework writing

Двое работают одновременно с этим репо:
- **Кирилл (owner, основной автор):** редактирует драфты курсовой (главы, аннотация, методология) — текстовая работа в `analysis_v2/reports/chapter_*.md`, `abstract.md`, `methodology_v2_addendum.md` и т.д.
- **Артем (collaborator):** собирает bibliography — кладёт PDF в `bibliography/pdfs/`, заполняет шаблоны в `bibliography/sources/`. Также готовит `bibliography/MASTER_TABLE.md` и `references.bib`.

Чтобы не перетирать друг друга — **разделяем scope и работаем через PR**.

---

## Правила разделения

### Артем трогает ТОЛЬКО:
```
bibliography/pdfs/           ← скачанные PDF и snapshot'ы (binary-safe)
bibliography/sources/        ← заполненные шаблоны (по одному .md на источник)
bibliography/MASTER_TABLE.md ← большая сегментированная таблица (создаётся в конце)
bibliography/references.bib  ← BibTeX для финального .tex (создаётся в конце)
bibliography/additional_proposals.md  ← если найдены дополнительные источники
```

### Кирилл трогает ВСЁ ОСТАЛЬНОЕ. Конкретно:
```
analysis_v2/reports/chapter_*.md     ← главы драфта
analysis_v2/reports/abstract.md      ← аннотация
analysis_v2/reports/methodology_v2_addendum.md
analysis_v2/reports/*_notes.md       ← analytical notes
analysis_v2/*.py                      ← если правишь анализ (но базовая ветка регрессионного кода frozen — см. CLAUDE.md)
любые новые драфты вне bibliography/
```

### НИ КТО НЕ ТРОГАЕТ без согласования:
```
bibliography/README.md       ← workflow-инструкция от Кирилла (только Кирилл может править)
bibliography/TEMPLATE.md     ← шаблон (только Кирилл)
analysis_v2/reports/bibliography_proposal.md  ← список источников (только Кирилл; Артем пишет заметки про несоответствия в шаблоны источников или в additional_proposals.md)
data/clean/                  ← frozen baseline
CLAUDE.md, README.md         ← корневая документация
```

---

## Workflow для каждой стороны

### Артем (bibliography)
1. Работает на feature branches `bibliography/batch-N` (N = top-5, batch-2, batch-3...).
2. После каждого batch'а: PR в `main` с descriptive body.
3. Большие коммиты PDF могут быть `[interim]` без шаблонов — это нормально, шаблоны догонят.
4. Если нужно изменить файл вне `bibliography/` (например, найдена ошибка в `bibliography_proposal.md`) — НЕ редактирует, а оставляет заметку в `bibliography/sources/{source}.md` секция "Reading notes". Кирилл сам решит, что переносить.

### Кирилл (драфты)
1. Работает в `main` напрямую (своя территория, PR не обязателен — но `git pull` перед началом и `git push` сразу после commit, чтобы Артем видел).
2. Перед началом сессии: `git pull` (получить новые PDF и шаблоны от Артема).
3. После каждого смыслового блока: `git commit` + `git push` (чтобы рабочая копия не разъехалась).
4. Если хочется добавить новый источник, которого нет в `bibliography_proposal.md` — добавляет в `proposal` (это его файл). Артем подтянет.

---

## Что делать с PR от Артема

Каждый batch приходит как PR (#1, #2, #3...) с body:
- summary что добавлено;
- ⚠ важные находки (DOI mismatch, paywall и т.п.).

Что делать:
1. **Прочитать body PR** — там основные находки сжато.
2. **Sanity-check 1-2 шаблонов** — открыть, проверить что секция "Use mapping" имеет смысл, "Connection to our findings" привязан к нашим H1-H10 правильно.
3. **Merge** через GitHub UI ("Squash and merge" если хочется чистую историю; "Create merge commit" если хочется видеть branch — обоим OK).
4. **`git pull` локально** → новые файлы доступны для интеграции в драфт.

---

## Если на одну ветку всё-таки пушим одновременно

Сценарий: оба в `main`, кто-то опоздал с pull.

```bash
# Получаешь reject при push:
$ git push
! [rejected]    main -> main (fetch first)

# Решение:
$ git pull --rebase    # подтянуть чужие коммиты, переписать свои поверх
$ git push             # снова
```

**НЕ ДЕЛАЙ `git push --force`** в `main` — это перетрёт чужие коммиты. `--force-with-lease` ок, но лучше rebase + push.

---

## Конфликт на одном файле

Если оба отредактировали один и тот же файл (например, оба что-то добавили в `additional_proposals.md`):

```bash
$ git pull --rebase
CONFLICT (content): Merge conflict in bibliography/additional_proposals.md
$ # открой файл, разреши конфликт руками (там будут <<<< ===== >>>> markers)
$ git add bibliography/additional_proposals.md
$ git rebase --continue
$ git push
```

Не страшно. Главное — не паниковать и не делать `git reset --hard`.

---

## Текущее состояние (2026-05-22, ~18:00)

- PR #1 открыт: top-5 sources + первый batch PDF
- 3 параллельных Claude-агента на стороне Артема продолжают писать шаблоны для остальных ~22 источников (proposal + новые из CSV)
- Следующие PR придут по мере готовности batch'ей
- Финальные артефакты: `MASTER_TABLE.md` (большая сегментированная таблица всех источников) + `references.bib` (BibTeX для LaTeX) — будут в последнем PR

---

## Контакт

Если что-то неясно или Артем нужен — telegram / звонок. Если конфликт в репо — пиши в issue с тегом `coordination`.
