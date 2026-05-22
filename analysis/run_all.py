"""End-to-end orchestrator. Run from project root:

    python3 -m analysis.run_all
"""
from __future__ import annotations

import warnings

from analysis import prep, contract_year, desc, m1, m2, m3, robustness

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


def main() -> None:
    df = prep.run()
    df = contract_year.run(df)
    desc.run(df)
    m1.run(df)
    m2.run(df)
    m3.run(df)
    robustness.run(df)

    print("\n" + "=" * 72)
    print("DONE. Outputs in output/tables/ and data/clean/data_analysis.csv")
    print("=" * 72)


if __name__ == "__main__":
    main()
