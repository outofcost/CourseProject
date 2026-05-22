# validation_report_v2

Dataset: `data/clean/data_analysis_v2.csv`  
Shape: 3660 × 153

## Birth country / international
- ✅ **share international ∈ [0.22, 0.32]** — observed = 0.230
- ✅ **share international rises 2016 → 2024** — 2016 = 0.212, 2024 = 0.223

Top birth countries (player-seasons):

```
birth_country
USA                       2818
Canada                     127
France                      55
Australia                   50
Serbia                      38
Spain                       35
Germany                     33
Bosnia and Herzegovina      31
Brazil                      29
Italy                       28
```

## Awards (lag, cumsum, supermax)

all_nba_lag1 == 1 per season (player-seasons in panel):

```
2016: 15
2017: 15
2018: 14
2019: 15
2020: 12
2021: 15
2022: 14
2023: 15
2024: 15
```

supermax_eligible_loose count per season:

```
season
2016     0
2017     0
2018    18
2019    19
2020    15
2021    19
2022    16
2023    20
2024    17
```
- ✅ **supermax = 0 in 2016** — observed = 0
- ✅ **supermax > 0 in 2024** — observed = 17

## Contract tier

Distribution by season × tier:

```
contract_tier  high_mid  max_25  max_30  max_35  mid_level  minimum  overpay  rookie_scale  supermax
season                                                                                              
2016                 67      36       6       6        137       47        2            96         0
2017                 87      48       3       1        119       48        1            91         0
2018                 67      32       3       0        126       62        1            93         2
2019                 76      34       3       2        127       58        0            97         3
2020                 60      24       7       1        118       70        0           100         3
2021                 60      20      12       1        143       76        4           100         7
2022                 55      28       9       3        134       89        2            99         8
2023                 62      30      12       3        118       86        2           106         6
2024                 60      24       6       5        122       93        1           103         7
```
- ✅ **supermax tier 5–10 in 2024** — observed = 7

## Market size
- ✅ **|corr(market_size_rank_nba, top5_market)| ≥ 0.5** — observed = -0.585
- ✅ **MEM market_size_rank_nba ≥ 25** — observed = [26.0]
- ✅ **NYK/BRK market_size_rank_nba == 1** — observed = [1]

## Durability
- ✅ **median games_missed_lag1 ∈ [10, 30]** — observed = 15.0

## Team season (win pct, playoffs)
- ✅ **win_pct median ≈ 0.5 (within ±0.05)** — observed = 0.512
- ✅ **win_pct std ≈ 0.15 (within ±0.05)** — observed = 0.145

## Correlation among main regressors

```
                          ppg   rpg   apg   per    ws  vorp  usg_pct   age  experience  salary_cap_share_t  all_nba_lag1  career_all_nba_count  career_allstar_count  supermax_eligible_loose  games_missed_lag1  market_size_rank_nba  top5_market  win_pct  made_playoffs  is_international
ppg                      1.00  0.56  0.69  0.70  0.71  0.74     0.81  0.03        0.20                0.68          0.43                  0.36                  0.48                     0.42              -0.26                  0.00        -0.01     0.02           0.02             -0.01
rpg                      0.56  1.00  0.27  0.67  0.67  0.59     0.33  0.03        0.18                0.48          0.31                  0.27                  0.31                     0.30              -0.22                 -0.00         0.00     0.01           0.01              0.14
apg                      0.69  0.27  1.00  0.46  0.50  0.62     0.56  0.11        0.22                0.55          0.38                  0.36                  0.45                     0.37              -0.19                  0.01         0.00     0.02           0.01             -0.04
per                      0.70  0.67  0.46  1.00  0.77  0.79     0.63  0.06        0.20                0.52          0.41                  0.35                  0.40                     0.39              -0.13                  0.01        -0.01     0.14           0.11              0.09
ws                       0.71  0.67  0.50  0.77  1.00  0.91     0.40  0.13        0.24                0.57          0.43                  0.33                  0.38                     0.38              -0.29                  0.02        -0.02     0.33           0.27              0.05
vorp                     0.74  0.59  0.62  0.79  0.91  1.00     0.53  0.14        0.24                0.60          0.52                  0.42                  0.49                     0.47              -0.21                  0.02        -0.01     0.29           0.23              0.03
usg_pct                  0.81  0.33  0.56  0.63  0.40  0.53     1.00 -0.05        0.10                0.50          0.37                  0.32                  0.40                     0.35              -0.11                  0.01        -0.01    -0.02          -0.01              0.01
age                      0.03  0.03  0.11  0.06  0.13  0.14    -0.05  1.00        0.86                0.36          0.10                  0.33                  0.24                     0.11              -0.08                 -0.07         0.08     0.21           0.16              0.01
experience               0.20  0.18  0.22  0.20  0.24  0.24     0.10  0.86        1.00                0.50          0.16                  0.41                  0.33                     0.17              -0.11                 -0.04         0.07     0.21           0.17              0.02
salary_cap_share_t       0.68  0.48  0.55  0.52  0.57  0.60     0.50  0.36        0.50                1.00          0.44                  0.49                  0.59                     0.45              -0.20                 -0.02         0.03     0.15           0.12              0.03
all_nba_lag1             0.43  0.31  0.38  0.41  0.43  0.52     0.37  0.10        0.16                0.44          1.00                  0.52                  0.52                     0.78              -0.12                 -0.01         0.05     0.15           0.12              0.02
career_all_nba_count     0.36  0.27  0.36  0.35  0.33  0.42     0.32  0.33        0.41                0.49          0.52                  1.00                  0.65                     0.52              -0.05                 -0.09         0.12     0.11           0.10             -0.02
career_allstar_count     0.48  0.31  0.45  0.40  0.38  0.49     0.40  0.24        0.33                0.59          0.52                  0.65                  1.00                     0.63              -0.04                 -0.09         0.13     0.14           0.12             -0.02
supermax_eligible_loose  0.42  0.30  0.37  0.39  0.38  0.47     0.35  0.11        0.17                0.45          0.78                  0.52                  0.63                     1.00              -0.10                 -0.02         0.04     0.13           0.11              0.02
games_missed_lag1       -0.26 -0.22 -0.19 -0.13 -0.29 -0.21    -0.11 -0.08       -0.11               -0.20         -0.12                 -0.05                 -0.04                    -0.10               1.00                 -0.01         0.01    -0.11          -0.07             -0.02
market_size_rank_nba     0.00 -0.00  0.01  0.01  0.02  0.02     0.01 -0.07       -0.04               -0.02         -0.01                 -0.09                 -0.09                    -0.02              -0.01                  1.00        -0.58     0.05           0.01              0.01
top5_market             -0.01  0.00  0.00 -0.01 -0.02 -0.01    -0.01  0.08        0.07                0.03          0.05                  0.12                  0.13                     0.04               0.01                 -0.58         1.00    -0.00          -0.04             -0.07
win_pct                  0.02  0.01  0.02  0.14  0.33  0.29    -0.02  0.21        0.21                0.15          0.15                  0.11                  0.14                     0.13              -0.11                  0.05        -0.00     1.00           0.80              0.02
made_playoffs            0.02  0.01  0.01  0.11  0.27  0.23    -0.01  0.16        0.17                0.12          0.12                  0.10                  0.12                     0.11              -0.07                  0.01        -0.04     0.80           1.00             -0.01
is_international        -0.01  0.14 -0.04  0.09  0.05  0.03     0.01  0.01        0.02                0.03          0.02                 -0.02                 -0.02                     0.02              -0.02                  0.01        -0.07     0.02          -0.01              1.00
```

Pairs with |r| > 0.85 (collinearity flag):

- ws ↔ vorp: r = 0.91
- age ↔ experience: r = 0.86
