# Verification Guide

This document explains how to reproduce the numerical and structural verification results in this repository.

This repository provides:

```text
Python verification scripts
CSV result files
JSON result files
HTML dashboards
A seven-stage integrated verification runner
```

---

# 1. Requirements

## 1.1 Check Python Installation

Run the following command in PowerShell:

```powershell
python --version
```

A normal result should look like:

```text
Python 3.x.x
```

---

## 1.2 Move to the Repository Folder

The verification scripts must be run inside the repository folder.

Example:

```powershell
cd D:\리만증명\한글파일\riemann-zero-axis
```

Check the current folder:

```powershell
pwd
```

The folder should contain files such as:

```text
run_all_verifications.py
verify_zeta.py
verify_zeta_dashboard_nompl.py
verify_independent_zeta_scan.py
verify_euler_product_dashboard.py
verify_functional_symmetry_dashboard.py
verify_zero_spacing_dashboard.py
verify_lower_residue_dashboard.py
requirements.txt
```

---

# 2. Install Required Package

Run:

```powershell
python -m pip install -r requirements.txt
```

The main required package is:

```text
mpmath
```

If `requirements.txt` is missing or does not work, install `mpmath` directly:

```powershell
python -m pip install mpmath
```

---

# 3. Run the Full Verification Package

The main command is:

```powershell
python run_all_verifications.py
```

This command runs all seven verification stages:

```text
1. Known zeta zero verification
2. Known zeta zero dashboard verification
3. Independent Hardy Z(t) critical-line scan
4. Euler product field verification
5. Functional symmetry verification
6. Zero spacing and ascending zero-axis alignment verification
7. Lower residue structural verification
```

A successful run should end with output similar to:

```text
Full verification run complete
Successful commands: 7 / 7
Failed commands: 0 / 7
Summary file: verification_run_summary.json
```

---

# 4. Generated Output Files

After a successful run, the following result files are generated.

## 4.1 Known Zeta Zero Verification

```text
results/zeta_zeros.csv
results/zeta_zeros.json
results/dashboard.html
```

## 4.2 Independent Hardy Z(t) Critical-Line Scan

```text
results_independent/independent_zeta_scan.csv
results_independent/independent_zeta_scan.json
results_independent/independent_scan_dashboard.html
```

## 4.3 Euler Product Field Verification

```text
results_euler/euler_product_verification.csv
results_euler/euler_product_verification.json
results_euler/euler_product_dashboard.html
```

## 4.4 Functional Symmetry Verification

```text
results_symmetry/functional_symmetry_verification.csv
results_symmetry/functional_symmetry_verification.json
results_symmetry/functional_symmetry_dashboard.html
```

## 4.5 Zero Spacing and Ascending Zero-Axis Alignment Verification

```text
results_spacing/zero_spacing_verification.csv
results_spacing/zero_spacing_verification.json
results_spacing/zero_spacing_dashboard.html
```

## 4.6 Lower Residue Structural Verification

```text
results_residue/lower_residue_verification.csv
results_residue/lower_residue_verification.json
results_residue/lower_residue_dashboard.html
```

## 4.7 Integrated Summary File

```text
verification_run_summary.json
```

This file records command results, success status, generated output checks, and SHA256 hashes.

---

# 5. Open the HTML Dashboards

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

# 6. Run Each Verification Individually

Each verification script can also be executed separately.

---

## 6.1 Known Zeta Zero Verification

```powershell
python verify_zeta.py
```

Verified relation:

```text
ζ(ρ) ≈ 0
Re(ρ) = 1/2
```

---

## 6.2 Known Zeta Zero Dashboard Verification

```powershell
python verify_zeta_dashboard_nompl.py --count 100 --dps 80 --tol 1e-50
```

Generated outputs:

```text
results/zeta_zeros.csv
results/zeta_zeros.json
results/dashboard.html
```

---

## 6.3 Independent Hardy Z(t) Critical-Line Scan

```powershell
python verify_independent_zeta_scan.py --target-count 100 --t-max 250 --step 0.05 --dps 80 --tol-zeta 1e-50
```

Method:

```text
Does not use mpmath.zetazero(n)
Scans Hardy Z(t) directly
Detects sign changes
Refines zeros by bisection
Evaluates ζ(1/2 + it)
```

---

## 6.4 Euler Product Field Verification

```powershell
python verify_euler_product_dashboard.py --prime-max 100000 --dps 80 --tol 1e-3
```

Verified relation:

```text
ζ(s) ≈ ∏p 1 / (1 - p^(-s)),  Re(s) > 1
```

Important note:

```text
The Euler product converges in the region Re(s)>1.
Therefore, this verification checks the connection between E=∏P and Z=ζ(s),
not the critical-line statement Re(ρ)=1/2 directly.
```

---

## 6.5 Functional Symmetry Verification

```powershell
python verify_functional_symmetry_dashboard.py --dps 80 --tol 1e-60
```

Verified relation:

```text
Λ(s) = Λ(1-s)
```

where:

```text
Λ(s) = π^(-s/2) Γ(s/2) ζ(s)
```

Structural meaning:

```text
1 → 0.5 | 0.5 = A0
s ↔ 1-s
Reflection around Re(s)=1/2
```

---

## 6.6 Zero Spacing and Ascending Zero-Axis Alignment Verification

```powershell
python verify_zero_spacing_dashboard.py --count 100 --dps 80 --zero-tol 1e-50 --real-tol 1e-70
```

Verified relations:

```text
ρ_n = 1/2 + iγ_n
γ_(n+1) - γ_n > 0
```

---

## 6.7 Lower Residue Structural Verification

```powershell
python verify_lower_residue_dashboard.py --scale 1.0 --epsilon 1e-12
```

Verified structural relation:

```text
phase difference(X, Rθ) = 180 degrees
180-degree phase difference → r generated
r ≠ 0
L_lower = r²
L_lower > 0
```

Numerical model:

```text
r = scale × |sin(theta / 2)|
L_lower = r²
```

Important note:

```text
This is an internal structural verification of the Zero-Axis framework.
It is not a standard zeta-zero computation.
```

---

# 7. Check the Results

## 7.1 Check Files in PowerShell

```powershell
dir
```

Check result folders:

```powershell
dir results
dir results_independent
dir results_euler
dir results_symmetry
dir results_spacing
dir results_residue
```

---

## 7.2 Check the Integrated Summary File

```powershell
Get-Content .\verification_run_summary.json -TotalCount 80
```

---

## 7.3 Check README Files

```powershell
Get-Content .\README.md -TotalCount 40
```

```powershell
Get-Content .\README_EN.md -TotalCount 40
```

---

# 8. Troubleshooting

## 8.1 mpmath is not installed

Error:

```text
ModuleNotFoundError: No module named 'mpmath'
```

Solution:

```powershell
python -m pip install mpmath
```

or:

```powershell
python -m pip install -r requirements.txt
```

---

## 8.2 PowerShell Does Not Recognize mpmath.zetazero(n)

Wrong PowerShell input:

```powershell
mpmath.zetazero(n)
```

This is not a PowerShell command.
`mpmath.zetazero(n)` is a Python function used inside Python code.

Correct PowerShell input:

```powershell
python -c "import mpmath as mp; print(mp.zetazero(1))"
```

---

## 8.3 SyntaxError in a Python File

Error example:

```text
SyntaxError: invalid syntax
```

Possible cause:

```text
README.md content
VERIFYING.md content
Markdown separator lines
Explanation text
Markdown code block markers
```

These belong in Markdown files, not Python files.

Correct distinction:

```text
.py files      → Python code only
.md files      → Documentation, explanations, and command examples
PowerShell     → Commands such as python ..., notepad ..., start ..., dir ...
```

Solution:

```text
If documentation text was pasted into a Python file,
delete the invalid content and replace it with valid Python code only.
```

---

## 8.4 Dashboard Does Not Open

First check that the file exists:

```powershell
dir results
dir results_independent
dir results_euler
dir results_symmetry
dir results_spacing
dir results_residue
```

If the file exists, open it again:

```powershell
start results/dashboard.html
```

Example for the Euler product dashboard:

```powershell
start results_euler/euler_product_dashboard.html
```

---

## 8.5 Verification Takes a Long Time

The following stages may take more time:

```text
Independent Hardy Z(t) critical-line scan
Euler product field verification
Zero spacing verification
```

The default public settings are:

```text
Zero count: 100
Precision: 80 decimal digits
Euler product prime range: 100000
```

For a quick test, smaller settings can be used.

Example:

```powershell
python verify_zeta_dashboard_nompl.py --count 20 --dps 50 --tol 1e-30
```

For public final results, the default settings are recommended.

---

# 9. Reproduced Final Result

Current integrated verification result:

```text
Successful commands: 7 / 7
Failed commands: 0 / 7
```

Main results:

```text
Known zeta zero dashboard verification: 100 / 100 PASS
Independent Hardy Z(t) critical-line scan: 100 / 100 PASS
Euler product field verification: 6 / 6 PASS
Functional symmetry verification: 8 / 8 PASS
Zero spacing and ascending alignment verification: 100 / 100 and 99 / 99 PASS
Lower residue structural verification: 7 / 7 PASS
```

---

# 10. Meaning of the Verification

This verification package numerically and structurally checks the following relations:

```text
E = ∏P → Z
Λ(s)=Λ(1-s)
ζ(ρ)=0 → Re(ρ)=1/2
ρ_n = 1/2 + iγ_n
γ_(n+1) > γ_n
r ≠ 0 → L_lower = r² > 0
```

In the Zero-Axis structural interpretation, these are understood through the flow:

```text
0_f ⊂ 1 → A0 → {W,H} → P → C → E → Z → ρ ⊂ A0
```

---

# 11. Important Limitation Notice

This repository provides reproducible numerical verification and structural consistency checks.

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

# 12. Recommended Pre-Publication Check

Before publishing the repository, run:

```powershell
python -m pip install -r requirements.txt
python run_all_verifications.py
dir
```

Check README files:

```powershell
Get-Content .\README.md -TotalCount 40
Get-Content .\README_EN.md -TotalCount 40
```

Check verification guides:

```powershell
Get-Content .\VERIFYING.md -TotalCount 40
Get-Content .\VERIFYING_EN.md -TotalCount 40
```

Check verification summaries:

```powershell
Get-Content .\VERIFICATION_SUMMARY.md -TotalCount 40
Get-Content .\VERIFICATION_SUMMARY_EN.md -TotalCount 40
```

---

# 13. Final Conclusion

The verification is successfully reproduced when the following command completes:

```powershell
python run_all_verifications.py
```

Success criterion:

```text
Successful commands: 7 / 7
Failed commands: 0 / 7
```

When this result is obtained, the repository is in the following state:

```text
A reproducible verification package consisting of code,
numerical results, dashboards, and documentation
for the Zero-Axis structural interpretation of the Riemann Hypothesis.
```
