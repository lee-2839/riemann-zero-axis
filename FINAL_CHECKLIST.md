# 공개 전 최종 점검표

이 문서는 `riemann-zero-axis` 저장소를 GitHub 또는 외부 공개 전에 점검하기 위한 최종 체크리스트입니다.

목표는 다음입니다.

```text
코드 실행 가능
검증 결과 재현 가능
문서 정리 완료
한계 고지 포함
불필요한 파일 제거
GitHub 공개 준비 완료
```

---

# 1. 기본 파일 확인

아래 파일들이 저장소 루트 폴더에 있는지 확인합니다.

```text
README.md
README_EN.md
VERIFYING.md
VERIFYING_EN.md
VERIFICATION_SUMMARY.md
VERIFICATION_SUMMARY_EN.md
FINAL_CHECKLIST.md
PAPER_SUMMARY_EN.md
requirements.txt
run_all_verifications.py
```

확인 명령:

```powershell
dir
```

체크:

```text
[ ] README.md 존재
[ ] README_EN.md 존재
[ ] VERIFYING.md 존재
[ ] VERIFYING_EN.md 존재
[ ] VERIFICATION_SUMMARY.md 존재
[ ] VERIFICATION_SUMMARY_EN.md 존재
[ ] FINAL_CHECKLIST.md 존재
[ ] PAPER_SUMMARY_EN.md 존재
[ ] requirements.txt 존재
[ ] run_all_verifications.py 존재
```

---

# 2. 검증 코드 파일 확인

아래 Python 검증 코드들이 모두 있어야 합니다.

```text
verify_zeta.py
verify_zeta_dashboard_nompl.py
verify_independent_zeta_scan.py
verify_euler_product_dashboard.py
verify_functional_symmetry_dashboard.py
verify_zero_spacing_dashboard.py
verify_lower_residue_dashboard.py
```

체크:

```text
[ ] verify_zeta.py 존재
[ ] verify_zeta_dashboard_nompl.py 존재
[ ] verify_independent_zeta_scan.py 존재
[ ] verify_euler_product_dashboard.py 존재
[ ] verify_functional_symmetry_dashboard.py 존재
[ ] verify_zero_spacing_dashboard.py 존재
[ ] verify_lower_residue_dashboard.py 존재
```

---

# 3. 필수 패키지 설치 확인

설치 명령:

```powershell
python -m pip install -r requirements.txt
```

`requirements.txt` 내용 확인:

```powershell
Get-Content .\requirements.txt
```

기본적으로 다음 항목이 있어야 합니다.

```text
mpmath
```

체크:

```text
[ ] requirements.txt에 mpmath 포함
[ ] python -m pip install -r requirements.txt 실행 성공
```

---

# 4. 전체 검증 실행

공개 전 반드시 전체 검증을 한 번 실행합니다.

```powershell
python run_all_verifications.py
```

성공 기준:

```text
성공한 명령: 7 / 7
실패한 명령: 0 / 7
```

체크:

```text
[ ] python run_all_verifications.py 실행 완료
[ ] 성공한 명령: 7 / 7 확인
[ ] 실패한 명령: 0 / 7 확인
[ ] verification_run_summary.json 생성 확인
```

---

# 5. 결과 폴더 확인

다음 결과 폴더들이 생성되어 있어야 합니다.

```text
results
results_independent
results_euler
results_symmetry
results_spacing
results_residue
```

확인 명령:

```powershell
dir
```

체크:

```text
[ ] results 폴더 존재
[ ] results_independent 폴더 존재
[ ] results_euler 폴더 존재
[ ] results_symmetry 폴더 존재
[ ] results_spacing 폴더 존재
[ ] results_residue 폴더 존재
```

---

# 6. 결과 파일 확인

## 6.1 알려진 제타 영점 검증 결과

```text
results/zeta_zeros.csv
results/zeta_zeros.json
results/dashboard.html
```

체크:

```text
[ ] results/zeta_zeros.csv 존재
[ ] results/zeta_zeros.json 존재
[ ] results/dashboard.html 존재
```

## 6.2 Hardy Z(t) 독립 임계선 스캔 결과

```text
results_independent/independent_zeta_scan.csv
results_independent/independent_zeta_scan.json
results_independent/independent_scan_dashboard.html
```

체크:

```text
[ ] results_independent/independent_zeta_scan.csv 존재
[ ] results_independent/independent_zeta_scan.json 존재
[ ] results_independent/independent_scan_dashboard.html 존재
```

## 6.3 오일러 곱장 검증 결과

```text
results_euler/euler_product_verification.csv
results_euler/euler_product_verification.json
results_euler/euler_product_dashboard.html
```

체크:

```text
[ ] results_euler/euler_product_verification.csv 존재
[ ] results_euler/euler_product_verification.json 존재
[ ] results_euler/euler_product_dashboard.html 존재
```

## 6.4 함수방정식 중심 대칭 검증 결과

```text
results_symmetry/functional_symmetry_verification.csv
results_symmetry/functional_symmetry_verification.json
results_symmetry/functional_symmetry_dashboard.html
```

체크:

```text
[ ] results_symmetry/functional_symmetry_verification.csv 존재
[ ] results_symmetry/functional_symmetry_verification.json 존재
[ ] results_symmetry/functional_symmetry_dashboard.html 존재
```

## 6.5 영점 간격 및 상승 정렬 검증 결과

```text
results_spacing/zero_spacing_verification.csv
results_spacing/zero_spacing_verification.json
results_spacing/zero_spacing_dashboard.html
```

체크:

```text
[ ] results_spacing/zero_spacing_verification.csv 존재
[ ] results_spacing/zero_spacing_verification.json 존재
[ ] results_spacing/zero_spacing_dashboard.html 존재
```

## 6.6 하한 잔차 구조 검증 결과

```text
results_residue/lower_residue_verification.csv
results_residue/lower_residue_verification.json
results_residue/lower_residue_dashboard.html
```

체크:

```text
[ ] results_residue/lower_residue_verification.csv 존재
[ ] results_residue/lower_residue_verification.json 존재
[ ] results_residue/lower_residue_dashboard.html 존재
```

---

# 7. 대시보드 열기 확인

다음 명령으로 HTML 대시보드가 열리는지 확인합니다.

```powershell
start results/dashboard.html
start results_independent/independent_scan_dashboard.html
start results_euler/euler_product_dashboard.html
start results_symmetry/functional_symmetry_dashboard.html
start results_spacing/zero_spacing_dashboard.html
start results_residue/lower_residue_dashboard.html
```

체크:

```text
[ ] 알려진 영점 대시보드 열림
[ ] 독립 임계선 스캔 대시보드 열림
[ ] 오일러 곱장 대시보드 열림
[ ] 함수방정식 대칭 대시보드 열림
[ ] 영점 간격 대시보드 열림
[ ] 하한 잔차 대시보드 열림
```

---

# 8. 문서 내용 확인

각 문서의 첫 부분을 확인합니다.

```powershell
Get-Content .\README.md -TotalCount 40
Get-Content .\README_EN.md -TotalCount 40
Get-Content .\VERIFYING.md -TotalCount 40
Get-Content .\VERIFYING_EN.md -TotalCount 40
Get-Content .\VERIFICATION_SUMMARY.md -TotalCount 40
Get-Content .\VERIFICATION_SUMMARY_EN.md -TotalCount 40
```

체크:

```text
[ ] README.md 내용 정상
[ ] README_EN.md 내용 정상
[ ] VERIFYING.md 내용 정상
[ ] VERIFYING_EN.md 내용 정상
[ ] VERIFICATION_SUMMARY.md 내용 정상
[ ] VERIFICATION_SUMMARY_EN.md 내용 정상
```

---

# 9. 한계 고지 확인

공개용 문서에는 반드시 다음 취지의 문장이 포함되어야 합니다.

```text
이 저장소는 유한 계산만으로 리만가설 전체를 완전히 증명했다고 주장하지 않는다.
```

영문 문서에는 다음 취지의 문장이 포함되어야 합니다.

```text
This repository does not claim that finite computation alone proves the full Riemann Hypothesis.
```

체크:

```text
[ ] README.md에 한계 고지 포함
[ ] README_EN.md에 한계 고지 포함
[ ] VERIFYING.md에 한계 고지 포함
[ ] VERIFYING_EN.md에 한계 고지 포함
[ ] VERIFICATION_SUMMARY.md에 한계 고지 포함
[ ] VERIFICATION_SUMMARY_EN.md에 한계 고지 포함
```

---

# 10. 불필요한 파일 제거 확인

공개 전에 임시 파일이나 캐시 파일을 확인합니다.

제거하거나 `.gitignore`에 포함할 항목:

```text
__pycache__/
*.pyc
.env
.venv/
venv/
.DS_Store
Thumbs.db
```

확인 명령:

```powershell
dir -Force
```

체크:

```text
[ ] __pycache__ 공개 제외
[ ] *.pyc 공개 제외
[ ] .env 공개 제외
[ ] 가상환경 폴더 공개 제외
[ ] 임시 파일 공개 제외
```

---

# 11. .gitignore 권장 내용

`.gitignore` 파일이 없다면 생성하는 것을 권장합니다.

```powershell
notepad .gitignore
```

권장 내용:

```gitignore
__pycache__/
*.pyc
.env
.venv/
venv/
.DS_Store
Thumbs.db
```

체크:

```text
[ ] .gitignore 존재
[ ] __pycache__/ 포함
[ ] *.pyc 포함
[ ] .env 포함
[ ] .venv/ 포함
[ ] venv/ 포함
```

---

# 12. 공개용 설명 문장 준비

GitHub 저장소 설명에는 다음 문장을 사용할 수 있습니다.

한글:

```text
0축 구조공식에 의한 리만가설 해석과 제타 영점 수치 검증 자료
```

영문:

```text
Reproducible numerical verification data for a Zero-Axis structural interpretation of the Riemann Hypothesis.
```

체크:

```text
[ ] GitHub 저장소 설명 한글 문장 준비
[ ] GitHub 저장소 설명 영문 문장 준비
```

---

# 13. Git 초기화 및 커밋

아직 Git 저장소가 아니라면 다음을 실행합니다.

```powershell
git init
```

파일 추가:

```powershell
git add .
```

커밋:

```powershell
git commit -m "Initial zero-axis Riemann verification package"
```

체크:

```text
[ ] git init 실행
[ ] git add . 실행
[ ] git commit 실행
```

---

# 14. GitHub 업로드 전 최종 명령

공개 전 마지막으로 아래 명령을 실행합니다.

```powershell
python -m pip install -r requirements.txt
python run_all_verifications.py
dir
```

성공 기준:

```text
성공한 명령: 7 / 7
실패한 명령: 0 / 7
```

체크:

```text
[ ] 최종 전체 검증 재실행 완료
[ ] 성공한 명령: 7 / 7 확인
[ ] 실패한 명령: 0 / 7 확인
[ ] 모든 결과 폴더 존재 확인
```

---

# 15. 최종 공개 판단

아래 항목이 모두 만족되면 공개 가능합니다.

```text
[ ] 코드 파일이 모두 존재한다.
[ ] 문서 파일이 모두 존재한다.
[ ] requirements.txt가 정상이다.
[ ] python run_all_verifications.py가 성공한다.
[ ] 성공한 명령: 7 / 7 이다.
[ ] 실패한 명령: 0 / 7 이다.
[ ] HTML 대시보드가 열린다.
[ ] CSV/JSON 결과 파일이 생성되어 있다.
[ ] README 한글/영문이 정리되어 있다.
[ ] VERIFYING 한글/영문이 정리되어 있다.
[ ] VERIFICATION_SUMMARY 한글/영문이 정리되어 있다.
[ ] 한계 고지가 포함되어 있다.
[ ] 불필요한 임시 파일이 제거되어 있다.
[ ] .gitignore가 준비되어 있다.
[ ] GitHub 설명 문장이 준비되어 있다.
```

---

# 16. 최종 상태 선언

모든 항목이 완료되면 저장소 상태는 다음과 같습니다.

```text
0축 구조공식에 의한 리만가설 해석을
코드, 수치 결과, 대시보드, 문서로 정리한
재현 가능한 공개 검증 패키지
```

영문 상태 선언:

```text
A reproducible public verification package consisting of code,
numerical results, dashboards, and documentation
for the Zero-Axis structural interpretation of the Riemann Hypothesis.
```
