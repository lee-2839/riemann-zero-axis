# Zero-Axis Structural Interpretation of the Riemann Hypothesis

This repository provides a reproducible verification package for the proposed **Zero-Axis structural interpretation of the Riemann Hypothesis**.

- `papers/리만가설 구조공식.pdf` : Korean version
- `papers/리만가설 구조공식(EN).pdf` : English version

It includes:

```text
Python verification scripts
CSV and JSON result files
HTML dashboards
Korean and English documentation
A seven-stage integrated verification runner
```

The core structural flow used in this project is:

```text
0_f ⊂ 1 → A0 → {W,H} → P → C → E → Z → ρ ⊂ A0
```

where:

```text
A0 = zero-axis
0.5 | 0.5 = A0
ρ = zeta zero
Z = zeta field
E = Euler product field
P = prime self-rotation
C = orbital field
L_lower = lower residue bound
```

This repository connects the Zero-Axis structure with the Riemann zeta function, Euler product, functional equation, zeta zeros, zero spacing, and lower-residue structure.

---

# 1. Core Claim

The standard statement of the Riemann Hypothesis is:

```text
If ζ(ρ)=0 and ρ is a non-trivial zero, then Re(ρ)=1/2.
```

In the Zero-Axis structural interpretation, this is expressed as:

```text
ρ ⊂ Z ⊂ A0
A0 = 0.5 | 0.5
Therefore, ρ is aligned on the zero-axis A0.
```

Thus, the standard statement:

```text
Re(ρ)=1/2
```

corresponds structurally to:

```text
ρ ⊂ A0
```

---

# 2. Overall Verification Result

Integrated runner:

```powershell
python run_all_verifications.py
```

Latest reproduced result:

```text
Successful commands: 7 / 7
Failed commands: 0 / 7
Summary file: verification_run_summary.json
```

All seven verification stages completed successfully.

---

# 3. Installation

Install the required Python package:

```powershell
python -m pip install -r requirements.txt
```

Main required package:

```text
mpmath
```

---

# 4. Run All Verifications

Run the full verification package with:

```powershell
python run_all_verifications.py
```

This executes the following seven verification stages:

```text
1. Known zeta zero verification
2. Known zeta zero dashboard verification
3. Independent Hardy Z(t) critical-line scan
4. Euler product field verification
5. Functional symmetry verification
6. Zero spacing and ascending zero-axis alignment verification
7. Lower residue structural verification
```

---

# 5. Seven Verification Stages

## 5.1 Known Zeta Zero Verification

Script:

```text
verify_zeta.py
```

Verified relation:

```text
ζ(ρ) ≈ 0
Re(ρ) = 1/2
```

This script uses:

```python
mpmath.zetazero(n)
```

to retrieve known non-trivial zeta zeros and verify that they lie on the critical line.

---

## 5.2 Known Zeta Zero Dashboard Verification

Script:

```text
verify_zeta_dashboard_nompl.py
```

Example command:

```powershell
python verify_zeta_dashboard_nompl.py --count 100 --dps 80 --tol 1e-50
```

Generated outputs:

```text
results/zeta_zeros.csv
results/zeta_zeros.json
results/dashboard.html
```

Verification result:

```text
Checked zeros: 100
Passed: 100 / 100
Precision: 80 decimal digits
Tolerance: 1e-50
```

Structural meaning:

```text
ζ(ρ)=0 → Re(ρ)=1/2
ρ ⊂ A0
```

---

## 5.3 Independent Hardy Z(t) Critical-Line Scan

Script:

```text
verify_independent_zeta_scan.py
```

Example command:

```powershell
python verify_independent_zeta_scan.py --target-count 100 --t-max 250 --step 0.05 --dps 80 --tol-zeta 1e-50
```

Generated outputs:

```text
results_independent/independent_zeta_scan.csv
results_independent/independent_zeta_scan.json
results_independent/independent_scan_dashboard.html
```

Verification method:

```text
Does not use mpmath.zetazero(n)
Scans Hardy Z(t) directly
Detects sign changes
Refines zeros by bisection
Evaluates ζ(1/2 + it)
```

Verification result:

```text
Detected zeros: 100
Passed: 100 / 100
Scan range: 0 ≤ t ≤ 250
Step size: 0.05
```

Structural meaning:

```text
ρ = 1/2 + it
ρ ⊂ A0
```

This stage is stronger than simply retrieving known zeros, because it independently detects zeros on the critical line.

---

## 5.4 Euler Product Field Verification

Script:

```text
verify_euler_product_dashboard.py
```

Example command:

```powershell
python verify_euler_product_dashboard.py --prime-max 100000 --dps 80 --tol 1e-3
```

Generated outputs:

```text
results_euler/euler_product_verification.csv
results_euler/euler_product_verification.json
results_euler/euler_product_dashboard.html
```

Verified relation:

```text
ζ(s) ≈ ∏p 1 / (1 - p^(-s)),  Re(s) > 1
```

Verification result:

```text
Prime max: 100000
Prime count: 9592
Test points: 6
Passed: 6 / 6
```

Structural meaning:

```text
P = prime self-rotation
E = ∏P = ∏Crit = total orbital field
Z = generation(E)
```

Important note:

```text
The Euler product converges in the region Re(s)>1.
Therefore, this stage verifies the connection between E=∏P and Z=ζ(s),
not the critical-line statement Re(ρ)=1/2 directly.
```

---

## 5.5 Functional Symmetry Verification

Script:

```text
verify_functional_symmetry_dashboard.py
```

Example command:

```powershell
python verify_functional_symmetry_dashboard.py --dps 80 --tol 1e-60
```

Generated outputs:

```text
results_symmetry/functional_symmetry_verification.csv
results_symmetry/functional_symmetry_verification.json
results_symmetry/functional_symmetry_dashboard.html
```

Verified relation:

```text
Λ(s) = Λ(1-s)
```

where:

```text
Λ(s) = π^(-s/2) Γ(s/2) ζ(s)
```

Verification result:

```text
Test points: 8
Passed: 8 / 8
Precision: 80 decimal digits
Tolerance: 1e-60
```

Structural meaning:

```text
1 → 0.5 | 0.5 = A0
s ↔ 1-s
Reflection around Re(s)=1/2
```

This stage numerically confirms the structural role of the line `Re(s)=1/2` as the central symmetry axis.

---

## 5.6 Zero Spacing and Ascending Zero-Axis Alignment Verification

Script:

```text
verify_zero_spacing_dashboard.py
```

Example command:

```powershell
python verify_zero_spacing_dashboard.py --count 100 --dps 80 --zero-tol 1e-50 --real-tol 1e-70
```

Generated outputs:

```text
results_spacing/zero_spacing_verification.csv
results_spacing/zero_spacing_verification.json
results_spacing/zero_spacing_dashboard.html
```

Verified relations:

```text
ρ_n = 1/2 + iγ_n
γ_(n+1) - γ_n > 0
```

Verification result:

```text
Zero alignment passed: 100 / 100
Spacing passed: 99 / 99
```

Structural meaning:

```text
ρ ⊂ Z ⊂ A0
γ_n = height position on the zero-axis
γ_(n+1) > γ_n = ascending alignment on the zero-axis
```

This stage confirms that the first 100 zeta zeros are aligned on the zero-axis and ordered by increasing imaginary height.

---

## 5.7 Lower Residue Structural Verification

Script:

```text
verify_lower_residue_dashboard.py
```

Example command:

```powershell
python verify_lower_residue_dashboard.py --scale 1.0 --epsilon 1e-12
```

Generated outputs:

```text
results_residue/lower_residue_verification.csv
results_residue/lower_residue_verification.json
results_residue/lower_residue_dashboard.html
```

Verified structural relation:

```text
phase difference(X, Rθ) = 180 degrees
180-degree phase difference → r generated
r ≠ 0
L_lower = r²
L_lower > 0
```

Numerical model used:

```text
r = scale × |sin(theta / 2)|
L_lower = r²
```

Verification result:

```text
Test points: 7
Passed: 7 / 7
At theta = 180 degrees:
r = 1.0
L_lower = 1.0
```

Structural meaning:

```text
The lower residue is not arbitrary.
The lower residue is generated by 180-degree phase opposition.
Since r ≠ 0, L_lower = r² > 0.
```

This stage is an internal structural verification of the Zero-Axis framework.
It is not a standard zeta-zero computation.

---

# 6. Open HTML Dashboards

After running the full verification package, open the dashboards with:

```powershell
start results/dashboard.html
start results_independent/independent_scan_dashboard.html
start results_euler/euler_product_dashboard.html
start results_symmetry/functional_symmetry_dashboard.html
start results_spacing/zero_spacing_dashboard.html
start results_residue/lower_residue_dashboard.html
```

---

# 7. Recommended Repository Structure

```text
riemann-zero-axis/
├── README.md
├── README_EN.md
├── VERIFYING.md
├── VERIFYING_EN.md
├── VERIFICATION_SUMMARY.md
├── VERIFICATION_SUMMARY_EN.md
├── PAPER_SUMMARY_EN.md
├── requirements.txt
├── run_all_verifications.py
├── verify_zeta.py
├── verify_zeta_dashboard_nompl.py
├── verify_independent_zeta_scan.py
├── verify_euler_product_dashboard.py
├── verify_functional_symmetry_dashboard.py
├── verify_zero_spacing_dashboard.py
├── verify_lower_residue_dashboard.py
├── results/
│   ├── zeta_zeros.csv
│   ├── zeta_zeros.json
│   └── dashboard.html
├── results_independent/
│   ├── independent_zeta_scan.csv
│   ├── independent_zeta_scan.json
│   └── independent_scan_dashboard.html
├── results_euler/
│   ├── euler_product_verification.csv
│   ├── euler_product_verification.json
│   └── euler_product_dashboard.html
├── results_symmetry/
│   ├── functional_symmetry_verification.csv
│   ├── functional_symmetry_verification.json
│   └── functional_symmetry_dashboard.html
├── results_spacing/
│   ├── zero_spacing_verification.csv
│   ├── zero_spacing_verification.json
│   └── zero_spacing_dashboard.html
└── results_residue/
    ├── lower_residue_verification.csv
    ├── lower_residue_verification.json
    └── lower_residue_dashboard.html
```

---

# 8. Structural Formula Summary

Core Zero-Axis structure:

```text
0 = {0_∞, 0_f}
0_f ⊂ 1
D < 1
D → 1
1 → 0.5 | 0.5
0.5 | 0.5 = A0
A0 = upper-lower boundary
```

Prime and Euler product structure:

```text
P = prime self-rotation
C = orbital field
E = ∏P = ∏Crit
Z = generation(E)
ρ = zero(Z)
ρ ⊂ Z ⊂ A0
```

Riemann Hypothesis correspondence:

```text
ζ(ρ)=0 → Re(ρ)=1/2
Re(s)=1/2 = 0.5 | 0.5 = A0
```

Lower residue structure:

```text
phase difference(X, Rθ)=180 degrees
180-degree phase difference → r generated
r ≠ 0
L_lower = r²
L_lower > 0
```

---

# 9. Overall Verification Table

| Stage | Verification Name                              | Result                     |
| ----: | ---------------------------------------------- | -------------------------- |
|     1 | Known zeta zero verification                   | PASS                       |
|     2 | Known zeta zero dashboard verification         | 100 / 100 PASS             |
|     3 | Independent Hardy Z(t) critical-line scan      | 100 / 100 PASS             |
|     4 | Euler product field verification               | 6 / 6 PASS                 |
|     5 | Functional symmetry verification               | 8 / 8 PASS                 |
|     6 | Zero spacing and ascending zero-axis alignment | 100 / 100 and 99 / 99 PASS |
|     7 | Lower residue structural verification          | 7 / 7 PASS                 |

---

# 10. Important Limitation Notice

This repository provides:

```text
Numerical verification
Structural consistency verification
Reproducible research records
HTML dashboards
CSV/JSON result data
```

However, the following distinction must be made clearly.

Acceptable statement:

```text
This repository presents a reproducible numerical and structural verification package
for the Zero-Axis structural interpretation of the Riemann Hypothesis.
```

Statement to avoid:

```text
This repository proves the full Riemann Hypothesis by finite computation alone.
```

This repository does **not** claim that finite computation alone constitutes a complete standard mathematical proof of the full Riemann Hypothesis.

---

# 11. Public Repository Description

Korean description:

```text
0축 구조공식에 의한 리만가설 해석과 제타 영점 수치 검증 자료
```

English description:

```text
Reproducible numerical verification data for a Zero-Axis structural interpretation of the Riemann Hypothesis.
```

---

# 12. Final Conclusion

The seven-stage verification package consistently supports the following structural relations:

```text
E = ∏P → Z
Λ(s)=Λ(1-s)
ζ(ρ)=0 → Re(ρ)=1/2
ρ_n = 1/2 + iγ_n
γ_(n+1) > γ_n
r ≠ 0 → L_lower = r² > 0
```

Thus, this repository presents the Zero-Axis structural interpretation of the Riemann Hypothesis as:

```text
A reproducible verification package consisting of code,
numerical results, dashboards, and documentation
for the Zero-Axis structural interpretation of the Riemann Hypothesis.
```
