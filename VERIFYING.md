# 검증 재현 안내서

이 문서는 본 저장소의 **0축 구조공식 리만가설 수치 검증 패키지**를 다른 사람이 동일하게 실행하고 재현할 수 있도록 안내합니다.

본 저장소는 다음을 제공합니다.

```text
Python 검증 코드
CSV 결과 파일
JSON 결과 파일
HTML 대시보드
7단계 통합 검증 실행기
```

---

# 1. 준비 사항

## 1.1 Python 설치 확인

PowerShell에서 다음을 입력합니다.

```powershell
python --version
```

정상이라면 예를 들어 다음과 비슷하게 표시됩니다.

```text
Python 3.x.x
```

---

## 1.2 현재 폴더 확인

검증 코드는 저장소 폴더 안에서 실행해야 합니다.

예시:

```powershell
cd D:\리만증명\한글파일\riemann-zero-axis
```

현재 위치 확인:

```powershell
pwd
```

현재 폴더 안에 다음 파일들이 있어야 합니다.

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

# 2. 필요한 패키지 설치

다음 명령을 PowerShell에 입력합니다.

```powershell
python -m pip install -r requirements.txt
```

필요한 주요 패키지는 다음입니다.

```text
mpmath
```

만약 `requirements.txt`가 없거나 문제가 있다면, 다음 명령으로 직접 설치할 수 있습니다.

```powershell
python -m pip install mpmath
```

---

# 3. 전체 검증 한 번에 실행하기

가장 중요한 명령은 다음입니다.

```powershell
python run_all_verifications.py
```

이 명령은 7단계 전체 검증을 순서대로 실행합니다.

```text
1. 알려진 제타 영점 기본 검증
2. 알려진 제타 영점 대시보드 검증
3. Hardy Z(t) 독립 임계선 스캔
4. 오일러 곱장 검증
5. 함수방정식 중심 대칭 검증
6. 영점 간격 및 0축 상승 정렬 검증
7. 하한 잔차 구조 검증
```

정상 실행 시 마지막에 다음과 비슷하게 표시됩니다.

```text
전체 검증 실행 완료
성공한 명령: 7 / 7
실패한 명령: 0 / 7
요약 파일: verification_run_summary.json

[최종 결과] 모든 실행 대상 검증이 정상 완료되었습니다.
```

---

# 4. 생성되는 결과 파일

전체 검증이 성공하면 다음 결과 파일들이 생성됩니다.

## 4.1 알려진 제타 영점 검증 결과

```text
results/zeta_zeros.csv
results/zeta_zeros.json
results/dashboard.html
```

## 4.2 Hardy Z(t) 독립 임계선 스캔 결과

```text
results_independent/independent_zeta_scan.csv
results_independent/independent_zeta_scan.json
results_independent/independent_scan_dashboard.html
```

## 4.3 오일러 곱장 검증 결과

```text
results_euler/euler_product_verification.csv
results_euler/euler_product_verification.json
results_euler/euler_product_dashboard.html
```

## 4.4 함수방정식 중심 대칭 검증 결과

```text
results_symmetry/functional_symmetry_verification.csv
results_symmetry/functional_symmetry_verification.json
results_symmetry/functional_symmetry_dashboard.html
```

## 4.5 영점 간격 및 0축 상승 정렬 검증 결과

```text
results_spacing/zero_spacing_verification.csv
results_spacing/zero_spacing_verification.json
results_spacing/zero_spacing_dashboard.html
```

## 4.6 하한 잔차 구조 검증 결과

```text
results_residue/lower_residue_verification.csv
results_residue/lower_residue_verification.json
results_residue/lower_residue_dashboard.html
```

## 4.7 통합 실행 요약 파일

```text
verification_run_summary.json
```

이 파일에는 각 검증 명령의 실행 결과, 성공 여부, 생성 파일 확인 결과, SHA256 해시 정보가 저장됩니다.

---

# 5. HTML 대시보드 열기

전체 검증 실행 후 PowerShell에서 다음 명령을 입력하면 각 대시보드를 열 수 있습니다.

```powershell
start results/dashboard.html
start results_independent/independent_scan_dashboard.html
start results_euler/euler_product_dashboard.html
start results_symmetry/functional_symmetry_dashboard.html
start results_spacing/zero_spacing_dashboard.html
start results_residue/lower_residue_dashboard.html
```

---

# 6. 개별 검증 실행 방법

전체 실행 대신 각 검증을 따로 실행할 수도 있습니다.

---

## 6.1 알려진 제타 영점 기본 검증

```powershell
python verify_zeta.py
```

검증 내용:

```text
ζ(ρ) ≈ 0
Re(ρ) = 1/2
```

---

## 6.2 알려진 제타 영점 대시보드 검증

```powershell
python verify_zeta_dashboard_nompl.py --count 100 --dps 80 --tol 1e-50
```

생성 결과:

```text
results/zeta_zeros.csv
results/zeta_zeros.json
results/dashboard.html
```

---

## 6.3 Hardy Z(t) 독립 임계선 스캔

```powershell
python verify_independent_zeta_scan.py --target-count 100 --t-max 250 --step 0.05 --dps 80 --tol-zeta 1e-50
```

특징:

```text
mpmath.zetazero(n)을 사용하지 않음
Hardy Z(t)를 직접 스캔
부호 변화 탐지
이분법으로 영점 정밀화
ζ(1/2+it) 값 확인
```

---

## 6.4 오일러 곱장 검증

```powershell
python verify_euler_product_dashboard.py --prime-max 100000 --dps 80 --tol 1e-3
```

검증 내용:

```text
ζ(s) ≈ ∏p 1 / (1 - p^(-s)),  Re(s) > 1
```

주의:

```text
오일러 곱은 Re(s)>1 영역에서 수렴합니다.
따라서 이 검증은 임계선 Re(s)=1/2 자체의 직접 검증이 아니라,
E=∏P와 Z=ζ(s)의 연결 검증입니다.
```

---

## 6.5 함수방정식 중심 대칭 검증

```powershell
python verify_functional_symmetry_dashboard.py --dps 80 --tol 1e-60
```

검증 내용:

```text
Λ(s) = Λ(1-s)
```

여기서:

```text
Λ(s) = π^(-s/2) Γ(s/2) ζ(s)
```

구조적 의미:

```text
1 → 0.5 | 0.5 = A0
s ↔ 1-s
Re(s)=1/2 중심 반사
```

---

## 6.6 영점 간격 및 0축 상승 정렬 검증

```powershell
python verify_zero_spacing_dashboard.py --count 100 --dps 80 --zero-tol 1e-50 --real-tol 1e-70
```

검증 내용:

```text
ρ_n = 1/2 + iγ_n
γ_(n+1) - γ_n > 0
```

---

## 6.7 하한 잔차 구조 검증

```powershell
python verify_lower_residue_dashboard.py --scale 1.0 --epsilon 1e-12
```

검증 내용:

```text
위상차(X, Rθ) = 180도
180도 위상차 → r 발생
r ≠ 0
L_하 = r²
L_하 > 0
```

사용한 수치 모델:

```text
r = scale × |sin(theta / 2)|
L_하 = r²
```

주의:

```text
이 검증은 표준 제타 함수 계산이 아니라,
0축 구조공식 내부의 하한 잔차 일관성 검증입니다.
```

---

# 7. 검증 결과 확인 방법

## 7.1 PowerShell에서 결과 파일 확인

```powershell
dir
```

결과 폴더 확인:

```powershell
dir results
dir results_independent
dir results_euler
dir results_symmetry
dir results_spacing
dir results_residue
```

---

## 7.2 통합 요약 파일 확인

```powershell
Get-Content .\verification_run_summary.json -TotalCount 80
```

---

## 7.3 README 확인

```powershell
Get-Content .\README.md -TotalCount 40
```

영문 README 확인:

```powershell
Get-Content .\README_EN.md -TotalCount 40
```

---

# 8. 자주 발생하는 문제와 해결법

## 8.1 mpmath가 설치되지 않은 경우

오류:

```text
ModuleNotFoundError: No module named 'mpmath'
```

해결:

```powershell
python -m pip install mpmath
```

또는:

```powershell
python -m pip install -r requirements.txt
```

---

## 8.2 PowerShell에서 mpmath.zetazero(n)을 직접 입력한 경우

잘못된 입력:

```powershell
mpmath.zetazero(n)
```

이것은 PowerShell 명령이 아닙니다.
`mpmath.zetazero(n)`은 Python 코드 안에서 사용하는 함수입니다.

올바른 PowerShell 입력:

```powershell
python -c "import mpmath as mp; print(mp.zetazero(1))"
```

---

## 8.3 Python 파일에 Markdown 문서를 붙여넣은 경우

오류 예시:

```text
SyntaxError: invalid syntax
```

가능한 원인:

```text
README.md 내용
VERIFYING.md 내용
--- 같은 Markdown 구분선
설명 문장
코드블록 표시
```

이런 내용이 `.py` 파일 안에 들어가면 오류가 납니다.

정확한 구분:

```text
.py 파일      → Python 코드만 넣습니다.
.md 파일      → 설명 문서, Markdown 내용, 명령 예시를 넣습니다.
PowerShell   → python ..., notepad ..., start ..., dir ... 같은 명령만 입력합니다.
```

해결:

```text
문서 내용이 Python 파일에 들어갔다면 삭제하고,
정상 Python 코드만 다시 붙여넣습니다.
```

---

## 8.4 대시보드가 열리지 않는 경우

먼저 파일이 존재하는지 확인합니다.

```powershell
dir results
dir results_independent
dir results_euler
dir results_symmetry
dir results_spacing
dir results_residue
```

파일이 존재하면 다음처럼 다시 엽니다.

```powershell
start results/dashboard.html
```

예를 들어 오일러 곱장 대시보드는 다음으로 엽니다.

```powershell
start results_euler/euler_product_dashboard.html
```

---

## 8.5 검증 시간이 오래 걸리는 경우

가장 시간이 걸릴 수 있는 검증은 다음입니다.

```text
Hardy Z(t) 독립 임계선 스캔
오일러 곱장 검증
영점 간격 검증
```

기본 설정은 다음입니다.

```text
영점 개수: 100
정밀도: 80 decimal digits
오일러 곱 소수 범위: 100000
```

빠르게 시험하려면 개수를 줄일 수 있습니다.

예시:

```powershell
python verify_zeta_dashboard_nompl.py --count 20 --dps 50 --tol 1e-30
```

단, 공개용 최종 결과는 기존 설정을 권장합니다.

---

# 9. 재현된 최종 결과

현재 통합 실행 결과:

```text
성공한 명령: 7 / 7
실패한 명령: 0 / 7
```

주요 결과:

```text
알려진 제타 영점 대시보드 검증: 100 / 100 PASS
Hardy Z(t) 독립 임계선 스캔: 100 / 100 PASS
오일러 곱장 검증: 6 / 6 PASS
함수방정식 중심 대칭 검증: 8 / 8 PASS
영점 간격 및 상승 정렬 검증: 100 / 100, 99 / 99 PASS
하한 잔차 구조 검증: 7 / 7 PASS
```

---

# 10. 검증의 의미

본 검증 패키지는 다음 구조를 수치적으로 확인합니다.

```text
E = ∏P → Z
Λ(s)=Λ(1-s)
ζ(ρ)=0 → Re(ρ)=1/2
ρ_n = 1/2 + iγ_n
γ_(n+1) > γ_n
r ≠ 0 → L_하 = r² > 0
```

0축 구조공식에서는 이를 다음 흐름으로 해석합니다.

```text
0_f ⊂ 1 → A0 → {W,H} → P → C → E → Z → ρ ⊂ A0
```

---

# 11. 중요한 한계 고지

본 저장소는 재현 가능한 수치 검증과 구조 일관성 검증을 제공합니다.

그러나 다음을 명확히 구분해야 합니다.

허용되는 설명:

```text
이 저장소는 0축 구조공식에 의한 리만가설 해석을
재현 가능한 수치 검증 자료와 함께 정리한 것이다.
```

피해야 할 설명:

```text
이 저장소는 유한 계산만으로 리만가설 전체를 완전히 증명했다.
```

즉, 본 검증 패키지는 수치 검증 및 구조 검증 패키지이며, 유한 계산만으로 리만가설 전체의 표준 수학적 완전 증명을 주장하지 않습니다.

---

# 12. 공개 전 권장 확인 명령

GitHub 업로드 전 다음을 실행하는 것을 권장합니다.

```powershell
python -m pip install -r requirements.txt
python run_all_verifications.py
dir
```

README 확인:

```powershell
Get-Content .\README.md -TotalCount 40
Get-Content .\README_EN.md -TotalCount 40
```

검증 안내서 확인:

```powershell
Get-Content .\VERIFYING.md -TotalCount 40
Get-Content .\VERIFYING_EN.md -TotalCount 40
```

검증 요약 확인:

```powershell
Get-Content .\VERIFICATION_SUMMARY.md -TotalCount 40
Get-Content .\VERIFICATION_SUMMARY_EN.md -TotalCount 40
```

---

# 13. 최종 결론

다음 명령이 성공하면 저장소의 검증 재현은 완료된 것입니다.

```powershell
python run_all_verifications.py
```

성공 기준:

```text
성공한 명령: 7 / 7
실패한 명령: 0 / 7
```

이 결과가 나오면 본 저장소는 다음 상태입니다.

```text
0축 구조공식에 의한 리만가설 해석을
코드, 수치 결과, 대시보드, 문서로 정리한
재현 가능한 검증 패키지
```
