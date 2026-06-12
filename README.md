
# 0축 구조공식에 의한 리만가설 해석 및 수치 검증 패키지

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20656275.svg)](https://doi.org/10.5281/zenodo.20656275)

이 저장소는 **0축 구조공식에 의한 리만가설 해석**을 코드, 수치 결과, 대시보드, 문서로 정리한 재현 가능한 검증 패키지입니다.

- `papers/리만가설 구조공식.pdf` : Korean version
- `papers/리만가설 구조공식(EN).pdf` : English version

본 프로젝트는 다음 구조를 중심으로 합니다.

```text
0_f ⊂ 1 → A0 → {W,H} → P → C → E → Z → ρ ⊂ A0
```

여기서 핵심 해석은 다음과 같습니다.

```text
A0 = 0축
0.5 | 0.5 = A0
ρ = 제타 영점
Z = 제타장
E = 오일러 곱장
P = 소수 자전
C = 공전장
L_하 = 하한 잔차
```

본 저장소는 이 구조를 리만 제타 함수, 오일러 곱, 함수방정식, 제타 영점, 영점 간격, 하한 잔차 구조와 연결하여 단계별로 검증합니다.

---

# 1. 핵심 주장

리만가설의 표준 표현은 다음입니다.

```text
ζ(ρ)=0 이고 ρ가 비자명 영점이면 Re(ρ)=1/2
```

0축 구조공식에서는 이를 다음과 같이 해석합니다.

```text
ρ ⊂ Z ⊂ A0
A0 = 0.5 | 0.5
따라서 ρ는 0축 A0 위에 정렬된다.
```

즉, 표준 표현:

```text
Re(ρ)=1/2
```

은 0축 구조공식에서는 다음과 대응됩니다.

```text
ρ ⊂ A0
```

---

# 2. 전체 검증 결과

통합 실행기:

```powershell
python run_all_verifications.py
```

최근 실행 결과:

```text
성공한 명령: 7 / 7
실패한 명령: 0 / 7
요약 파일: verification_run_summary.json
```

현재 7단계 전체 검증이 정상 통과되었습니다.

---

# 3. 설치 방법

먼저 필요한 Python 패키지를 설치합니다.

```powershell
python -m pip install -r requirements.txt
```

필요한 주요 패키지:

```text
mpmath
```

---

# 4. 전체 검증 한 번에 실행하기

다음 명령 하나로 전체 검증을 실행할 수 있습니다.

```powershell
python run_all_verifications.py
```

이 명령은 아래 7개 검증을 순서대로 실행합니다.

```text
1. 알려진 제타 영점 기본 검증
2. 알려진 제타 영점 대시보드 검증
3. Hardy Z(t) 독립 임계선 스캔
4. 오일러 곱장 검증
5. 함수방정식 중심 대칭 검증
6. 영점 간격 및 0축 상승 정렬 검증
7. 하한 잔차 구조 검증
```

---

# 5. 7단계 검증 구조

## 5.1 알려진 제타 영점 기본 검증

파일:

```text
verify_zeta.py
```

검증 내용:

```text
ζ(ρ) ≈ 0
Re(ρ) = 1/2
```

이 검증은 `mpmath.zetazero(n)`을 사용하여 알려진 비자명 제타 영점을 확인합니다.

---

## 5.2 알려진 제타 영점 대시보드 검증

파일:

```text
verify_zeta_dashboard_nompl.py
```

실행 예시:

```powershell
python verify_zeta_dashboard_nompl.py --count 100 --dps 80 --tol 1e-50
```

생성 결과:

```text
results/zeta_zeros.csv
results/zeta_zeros.json
results/dashboard.html
```

검증 결과:

```text
100개 영점 검증
100 / 100 PASS
```

---

## 5.3 Hardy Z(t) 독립 임계선 스캔

파일:

```text
verify_independent_zeta_scan.py
```

실행 예시:

```powershell
python verify_independent_zeta_scan.py --target-count 100 --t-max 250 --step 0.05 --dps 80 --tol-zeta 1e-50
```

생성 결과:

```text
results_independent/independent_zeta_scan.csv
results_independent/independent_zeta_scan.json
results_independent/independent_scan_dashboard.html
```

이 검증은 `mpmath.zetazero(n)`을 사용하지 않고 Hardy Z(t)를 직접 스캔하여 영점을 찾습니다.

검증 결과:

```text
검출 영점: 100개
통과: 100 / 100
```

---

## 5.4 오일러 곱장 검증

파일:

```text
verify_euler_product_dashboard.py
```

실행 예시:

```powershell
python verify_euler_product_dashboard.py --prime-max 100000 --dps 80 --tol 1e-3
```

생성 결과:

```text
results_euler/euler_product_verification.csv
results_euler/euler_product_verification.json
results_euler/euler_product_dashboard.html
```

검증 내용:

```text
ζ(s) ≈ ∏p 1 / (1 - p^(-s)),  Re(s) > 1
```

구조적 의미:

```text
P = 소수 자전
E = ∏P = ∏Crit = 전체 공전장
Z = 발생(E)
```

주의: 오일러 곱은 `Re(s)>1`에서 수렴합니다.
따라서 이 검증은 임계선 자체의 직접 검증이 아니라, `E=∏P`와 `Z=ζ(s)`의 연결 검증입니다.

---

## 5.5 함수방정식 중심 대칭 검증

파일:

```text
verify_functional_symmetry_dashboard.py
```

실행 예시:

```powershell
python verify_functional_symmetry_dashboard.py --dps 80 --tol 1e-60
```

생성 결과:

```text
results_symmetry/functional_symmetry_verification.csv
results_symmetry/functional_symmetry_verification.json
results_symmetry/functional_symmetry_dashboard.html
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

## 5.6 영점 간격 및 0축 상승 정렬 검증

파일:

```text
verify_zero_spacing_dashboard.py
```

실행 예시:

```powershell
python verify_zero_spacing_dashboard.py --count 100 --dps 80 --zero-tol 1e-50 --real-tol 1e-70
```

생성 결과:

```text
results_spacing/zero_spacing_verification.csv
results_spacing/zero_spacing_verification.json
results_spacing/zero_spacing_dashboard.html
```

검증 내용:

```text
ρ_n = 1/2 + iγ_n
γ_(n+1) - γ_n > 0
```

검증 결과:

```text
영점 정렬 통과: 100 / 100
간격 검증 통과: 99 / 99
```

구조적 의미:

```text
ρ ⊂ Z ⊂ A0
γ_n = 0축 위의 높이 위치
γ_(n+1) > γ_n = 0축 위 상승 정렬
```

---

## 5.7 하한 잔차 구조 검증

파일:

```text
verify_lower_residue_dashboard.py
```

실행 예시:

```powershell
python verify_lower_residue_dashboard.py --scale 1.0 --epsilon 1e-12
```

생성 결과:

```text
results_residue/lower_residue_verification.csv
results_residue/lower_residue_verification.json
results_residue/lower_residue_dashboard.html
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

구조적 의미:

```text
하한 잔차는 임의값이 아니다.
하한 잔차는 180도 위상차에서 발생한다.
r ≠ 0 이므로 L_하 = r² > 0 이다.
```

이 검증은 표준 제타 함수 계산이 아니라, 0축 구조공식 내부의 일관성 검증입니다.

---

# 6. 대시보드 열기

전체 검증 실행 후 다음 명령으로 HTML 대시보드를 열 수 있습니다.

```powershell
start results/dashboard.html
start results_independent/independent_scan_dashboard.html
start results_euler/euler_product_dashboard.html
start results_symmetry/functional_symmetry_dashboard.html
start results_spacing/zero_spacing_dashboard.html
start results_residue/lower_residue_dashboard.html
```

---

# 7. 저장소 파일 구조

권장 파일 구조는 다음과 같습니다.

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

# 8. 구조공식 요약

본 프로젝트에서 사용하는 핵심 구조는 다음과 같습니다.

```text
0 = {0_∞, 0_f}
0_f ⊂ 1
D < 1
D → 1
1 → 0.5 | 0.5
0.5 | 0.5 = A0
A0 = upper-lower boundary
```

소수 및 오일러 곱장 구조:

```text
P = 소수 자전
C = 공전장
E = ∏P = ∏Crit
Z = 발생(E)
ρ = zero(Z)
ρ ⊂ Z ⊂ A0
```

리만가설 대응:

```text
ζ(ρ)=0 → Re(ρ)=1/2
Re(s)=1/2 = 0.5 | 0.5 = A0
```

하한 잔차 구조:

```text
위상차(X, Rθ)=180도
180도 위상차 → r 발생
r ≠ 0
L_하 = r²
L_하 > 0
```

---

# 9. 전체 검증 결과 요약

```text
단계 | 검증 이름 | 결과
-----|-----------|------
1 | 알려진 제타 영점 기본 검증 | PASS
2 | 알려진 제타 영점 대시보드 검증 | 100 / 100 PASS
3 | Hardy Z(t) 독립 임계선 스캔 | 100 / 100 PASS
4 | 오일러 곱장 검증 | 6 / 6 PASS
5 | 함수방정식 중심 대칭 검증 | 8 / 8 PASS
6 | 영점 간격 및 0축 상승 정렬 검증 | 100 / 100, 99 / 99 PASS
7 | 하한 잔차 구조 검증 | 7 / 7 PASS
```

---

# 10. 중요한 한계 고지

본 저장소는 다음을 제공합니다.

```text
수치 검증
구조 일관성 검증
재현 가능한 연구 기록
HTML 대시보드
CSV/JSON 결과 데이터
```

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

즉, 이 저장소는 **리만가설 전체의 표준 수학적 완전 증명**을 유한 계산만으로 주장하지 않습니다.

---

# 11. 공개용 설명 문장

GitHub 설명에는 다음 문장을 사용할 수 있습니다.

```text
0축 구조공식에 의한 리만가설 해석과 제타 영점 수치 검증 자료
```

영문 설명:

```text
Reproducible numerical verification data for a Zero-Axis structural interpretation of the Riemann Hypothesis.
```

---

# 12. 최종 결론

7단계 전체 검증 결과, 본 저장소는 다음 구조를 일관되게 지지합니다.

```text
E = ∏P → Z
Λ(s)=Λ(1-s)
ζ(ρ)=0 → Re(ρ)=1/2
ρ_n = 1/2 + iγ_n
γ_(n+1) > γ_n
r ≠ 0 → L_하 = r² > 0
```

따라서 본 저장소는 다음과 같이 정리됩니다.

```text
0축 구조공식에 의한 리만가설 해석을
코드, 수치 결과, 대시보드, 문서로 정리한
재현 가능한 검증 패키지
```
