# Data Provenance - M33

## Metadata
- **Experiment**: M33. Interferences in the Quincke Tube
- **Source**: `Mecanica/m33.py`, `Mecanica/M33.xlsx`
- **Timestamp**: 2026-05-10T12:00:00Z

## Parameters & Constants
| Quantity | Symbol | Value | Uncertainty | Unit | Source |
|----------|--------|-------|-------------|------|--------|
| Temperature | $\theta$ | 28 | 0.5 | °C | `m33.py:169` |
| Frequency (Exp C) | $f_C$ | 1600 | 80 | Hz | `m33.py:53` |
| Distance uncertainty | $u_d$ | 0.1 | 0.01 | cm | `m33.py:108` |

## Experimental Data

### Table 1: Voltage vs Frequency (Maxima Search - Experiment A)
| Frequency (Hz) | Voltage (V) | Source |
|----------------|-------------|--------|
| $1400 \pm 70$ | $6.9 \pm 0.35$ | `m33.py:44` |
| $1600 \pm 80$ | $11 \pm 0.54$ | `m33.py:44` |
| $1700 \pm 85$ | $2.7 \pm 0.14$ | `m33.py:44` |
| $1900 \pm 95$ | $1.4 \pm 0.071$ | `m33.py:44` |
| $2100 \pm 100$ | $4.4 \pm 0.22$ | `m33.py:44` |
| $2200 \pm 110$ | $2.1 \pm 0.11$ | `m33.py:44` |

### Table 2: Voltage vs Frequency (Minima Search - Experiment B)
| Frequency (Hz) | Voltage (V) | Source |
|----------------|-------------|--------|
| $1300 \pm 65$ | $1.3 \pm 0.068$ | `m33.py:49` |
| $1500 \pm 75$ | $0.93 \pm 0.047$ | `m33.py:49` |
| $1700 \pm 85$ | $4.1 \pm 0.21$ | `m33.py:49` |
| $1800 \pm 90$ | $1.7 \pm 0.086$ | `m33.py:49` |
| $2000 \pm 100$ | $1.0 \pm 0.052$ | `m33.py:49` |
| $2100 \pm 110$ | $1.3 \pm 0.066$ | `m33.py:49` |

### Table 3: Voltage vs Distance (Fixed Frequency $f = 1576$ Hz - Experiment C)
*(First 10 points shown for brevity in provenance, full data in source)*
| Distance (cm) | Voltage (V) | Source |
|---------------|-------------|--------|
| $0.00 \pm 0.1$ | $11 \pm 0.54$ | `m33.py:54` |
| $0.51 \pm 0.1$ | $15 \pm 0.74$ | `m33.py:54` |
| $1.02 \pm 0.1$ | $13 \pm 0.66$ | `m33.py:54` |
| $1.53 \pm 0.1$ | $7.4 \pm 0.37$ | `m33.py:54` |
| $2.04 \pm 0.1$ | $2.6 \pm 0.13$ | `m33.py:54` |
| $2.55 \pm 0.1$ | $1.9 \pm 0.097$ | `m33.py:54` |
| $3.06 \pm 0.1$ | $1.7 \pm 0.088$ | `m33.py:54` |
| $3.57 \pm 0.1$ | $2.0 \pm 0.10$ | `m33.py:54` |
| $4.08 \pm 0.1$ | $0.50 \pm 0.026$ | `m33.py:54` |
| $4.59 \pm 0.1$ | $0.60 \pm 0.031$ | `m33.py:54` |

## Fit Results
- **Sound Speed (Maxima)**: $c = 380 \pm 0.85$ m/s
- **Sound Speed (Minima)**: $c = 370 \pm 1.2$ m/s
- **Theoretical Sound Speed**: $c_{theory} = 347.58$ m/s
- **$\chi^2_{red}$**: TODO_UNCERTAINTY (Not calculated in script)
- **Provenance**: `Mecanica/m33_resultados.txt`
