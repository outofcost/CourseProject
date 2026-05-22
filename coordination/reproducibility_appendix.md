# Приложение C — Reproducibility & Process Evidence

> Этот файл предназначен для embed в финальный manuscript как Приложение C. Bundle'ит coordination/ файлы и git-команды, позволяющие воспроизвести и аудитировать как computational pipeline, так и async-сотрудничество AI-агентов.

---

## C.1 Воспроизведение computational pipeline

Полный end-to-end run см. в `analysis_v2/reports/SHIPPING_SUMMARY.md` § Reproducibility. Кратко:

```bash
git clone https://github.com/outofcost/CourseProject.git
cd CourseProject
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Главные команды (warm cache, ~3 мин total):
python3 -m analysis_v2.regress_test_v1     # должен PASS: max coef diff < 5×10⁻⁵
python3 -m analysis_v2.m1_full
python3 -m analysis_v2.h_decomposition     # ~90 sec, 2⁹=512 OLS fits
python3 -m analysis_v2.figures             # 7 рисунков → output/figures/
```

Hash-snapshots датасетов:
- v1 baseline: `analysis_v2/reports/v1_snapshot.sha256`
- v2 extended: `analysis_v2/reports/v2_snapshot.sha256`

Финальный .docx сборка:
```bash
bash analysis_v2/build_docx.sh   # → coursework/coursework_draft.docx
```

---

## C.2 Воспроизведение коллаборативного workflow (AI agents)

Курсовая написана через **async-сотрудничество двух Claude Code сессий** на двух физических машинах:

- **Claude-K** (Karolina, owner): `analysis_v2/reports/chapter_*.md`, `methodology_v2_addendum.md`, `ai_disclosure.md`, `abstract.md`
- **Claude-A** (Artem, collaborator): `bibliography/sources/`, `bibliography/pdfs/`, `references.bib`, `MASTER_TABLE.md`, `bib_check_report.md`

Координация — через git с лейн-дисциплиной (нет file-overlap между Claude'ами) и явным протоколом обмена сообщениями.

### Координационные файлы (содержание этого приложения для аудита)

| Файл | Назначение |
|---|---|
| `coordination/PROTOCOL.md` | 8 правил взаимодействия (lane discipline, verification before claim, auto-commit, HUMAN_REVIEW, pull-before-work, task ownership, cron, stop conditions) |
| `coordination/MASTER_PLAN.md` | План работы на 8 фаз (A–H) с 50+ tasks, разделёнными по lanes |
| `coordination/TASKS.md` | Очередь задач, ownership, статус (✅/⏳/🚫) |
| `coordination/FOR_ARTEM.md` | Канал сообщений Claude-K → Claude-A |
| `coordination/FOR_KAROLINA.md` | Канал сообщений Claude-A → Claude-K |
| `coordination/ONBOARDING.md` | Инструкция для onboarding новой Claude-сессии на втором компьютере |
| `coordination/ai_disclosure_commits_log.md` | Атомарный лог всех commit'ов с указанием agent'а (Claude-K / Claude-A) |
| `bibliography/findings_log.md` | Substance-changing findings (DOI mismatches, paywall caveats) |
| `bibliography/bib_check_report.md` | Cross-reference audit cite'ов в драфтах против `references.bib` |
| `bibliography/MASTER_TABLE.md` | Сегментированная таблица 35 источников с priority + status |

### Аудит git history

```bash
# Все коммиты AI-агентов с описанием:
git log --all --format='%h %ai %s' --grep='Claude'

# Diff каждого commit'а от Claude-K:
git log --author='Karolina303' --all --format='%h %s'

# Diff каждого commit'а от Claude-A:
git log --author='Artem' --all --format='%h %s'

# Полный текст commit message (включая Co-Authored-By):
git show <SHA>
```

### Substance-affecting agent decisions

См. `bibliography/findings_log.md` для:
- Hembre 2021 → 2022 corrections (cite, DOI, journal, NBA-only coefficient insignificance)
- Hinton & Sun 2019 — proposal'd paper does not exist, dropped
- Robst et al. 2011 — proposal'd paper does not exist, replaced by Bodvarsson & Brastow (1998)
- Stiroh 2007 — DOI typo correction
- Kleven, Landais & Saez 2013 + Alm, Kaempfer & Sennoga 2012 + Johnson & Hall 2018 — added to bibliography, used to reframe H9 informative null

---

## C.3 Реплицируемость АI-Disclosure

Полный лог commit'ов в [coordination/ai_disclosure_commits_log.md](../coordination/ai_disclosure_commits_log.md) даёт:
- Кто (какой agent) сделал какую правку
- Когда (timestamp с timezone)
- Что (commit message)
- Где (file changes via `git show`)

Это даёт **полную traceability** для AI Disclosure section (см. §AI Disclosure), и позволяет любому reviewer'у или scientific supervisor'у проверить вклад каждого agent'а независимо.

---

**Файл подготовлен:** Claude-A (Artem-side), 2026-05-22
**Refs:** TASK-A-23 (MASTER_PLAN Phase D, endorsed Artem suggestion #3)
