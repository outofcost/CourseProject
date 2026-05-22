"""V1 end-to-end orchestrator. Запуск:

    python -m analysis_v1.run_all_v1

Порядок:
    1. prep_v1            — фикс A2, A3, C13 (data_analysis_v1.csv)
    2. contract_year_v1   — cy_A_up/down, cy_B_off/trade, cy_C, composite
    3. m1_v1, m2_v1, m3_v1, robustness_v1  — 17+ моделей в output/tables_v1/
    4. compare_v0_v1       — changes_summary.csv
    5. m1_alternatives     — §2 альтернативные спецификации
    6. diagnostics         — VIF, BP, power, FDR, influence, attrition
    7. bootstrap           — two-way clustering + wild cluster bootstrap
    8. quantile            — quantile regression M1a
    9. event_study         — CBA 2017 event-study
    10. spec_tests         — F-test poolability, year FE, player FE
    11. figures            — 14 фигур в output/figures_v1/
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from analysis_v1 import (bootstrap, compare_v0_v1, contract_year_v1,  # noqa: E402
                          diagnostics, event_study, figures,
                          m1_alternatives, m1_v1, m2_v1, m3_v1, prep_v1,
                          quantile, robustness_v1, spec_tests)

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


def main() -> None:
    print("\n" + "█" * 72)
    print("V1 PIPELINE — full run")
    print("█" * 72)

    # Stage 1 — data fixes + cy
    df = prep_v1.run()
    df = contract_year_v1.run(df)

    # Stage 2 — main 17 models
    m1_v1.run(df)
    m2_v1.run(df)
    m3_v1.run(df)
    robustness_v1.run(df)

    # Stage 3 — V0↔V1 comparison
    compare_v0_v1.main()

    # Stage 4 — §2 alternatives + §4 diagnostics
    m1_alternatives.main()
    diagnostics.main()
    bootstrap.main()

    # Stage 5 — §5 extensions
    quantile.main()
    event_study.main()
    spec_tests.main()

    # Stage 6 — figures
    figures.main()

    print("\n" + "█" * 72)
    print("V1 PIPELINE — done. Outputs:")
    print("  data/clean/data_analysis_v1.csv")
    print("  output/tables_v1/  (25+ tables)")
    print("  output/figures_v1/ (14 figures)")
    print("  analysis_v1/METHODOLOGY_v1.md")
    print("█" * 72)


if __name__ == "__main__":
    main()
