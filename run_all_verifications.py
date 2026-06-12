# run_all_verifications.py
# 0축 구조공식 리만가설 수치 검증 전체 실행기
#
# 이 파일은 아래 검증 스크립트들을 순서대로 실행합니다.
#
# 1. verify_zeta.py
# 2. verify_zeta_dashboard_nompl.py
# 3. verify_independent_zeta_scan.py
# 4. verify_euler_product_dashboard.py
# 5. verify_functional_symmetry_dashboard.py
# 6. verify_zero_spacing_dashboard.py
# 7. verify_lower_residue_dashboard.py
#
# 실행:
#   python run_all_verifications.py
#
# 결과:
#   verification_run_summary.json
#
# 주의:
#   이 코드는 검증 스크립트를 자동 실행하는 통합 실행기입니다.
#   유한 수치 검증은 리만가설 전체의 완전한 증명과는 구분됩니다.

import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib


def sha256_file(path):
    path = Path(path)

    if not path.exists() or not path.is_file():
        return None

    h = hashlib.sha256()

    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)

    return h.hexdigest()


def run_command(command, label):
    print()
    print("=" * 80)
    print(f"[실행] {label}")
    print("명령:")
    print(" ".join(command))
    print("=" * 80)

    result = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print("오류 출력:")
        print(result.stderr)

    success = result.returncode == 0

    print()
    if success:
        print(f"[성공] {label}")
    else:
        print(f"[실패] {label}")

    return {
        "label": label,
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "success": success,
    }


def script_exists(script_name):
    return Path(script_name).exists()


def build_commands():
    python = sys.executable
    commands = []

    script = "verify_zeta.py"
    if script_exists(script):
        commands.append(
            {
                "label": "1단계: 알려진 제타 영점 기본 검증",
                "script": script,
                "command": [python, script],
            }
        )

    script = "verify_zeta_dashboard_nompl.py"
    if script_exists(script):
        commands.append(
            {
                "label": "2단계: 알려진 제타 영점 대시보드 검증",
                "script": script,
                "command": [
                    python,
                    script,
                    "--count",
                    "100",
                    "--dps",
                    "80",
                    "--tol",
                    "1e-50",
                ],
            }
        )

    script = "verify_independent_zeta_scan.py"
    if script_exists(script):
        commands.append(
            {
                "label": "3단계: Hardy Z(t) 독립 임계선 스캔",
                "script": script,
                "command": [
                    python,
                    script,
                    "--target-count",
                    "100",
                    "--t-max",
                    "250",
                    "--step",
                    "0.05",
                    "--dps",
                    "80",
                    "--tol-zeta",
                    "1e-50",
                ],
            }
        )

    script = "verify_euler_product_dashboard.py"
    if script_exists(script):
        commands.append(
            {
                "label": "4단계: 오일러 곱장 검증",
                "script": script,
                "command": [
                    python,
                    script,
                    "--prime-max",
                    "100000",
                    "--dps",
                    "80",
                    "--tol",
                    "1e-3",
                ],
            }
        )

    script = "verify_functional_symmetry_dashboard.py"
    if script_exists(script):
        commands.append(
            {
                "label": "5단계: 함수방정식 중심 대칭 검증",
                "script": script,
                "command": [
                    python,
                    script,
                    "--dps",
                    "80",
                    "--tol",
                    "1e-60",
                ],
            }
        )

    script = "verify_zero_spacing_dashboard.py"
    if script_exists(script):
        commands.append(
            {
                "label": "6단계: 영점 간격 및 0축 상승 정렬 검증",
                "script": script,
                "command": [
                    python,
                    script,
                    "--count",
                    "100",
                    "--dps",
                    "80",
                    "--zero-tol",
                    "1e-50",
                    "--real-tol",
                    "1e-70",
                ],
            }
        )

    script = "verify_lower_residue_dashboard.py"
    if script_exists(script):
        commands.append(
            {
                "label": "7단계: 하한 잔차 구조 검증",
                "script": script,
                "command": [
                    python,
                    script,
                    "--scale",
                    "1.0",
                    "--epsilon",
                    "1e-12",
                ],
            }
        )

    return commands


def expected_outputs():
    return [
        {
            "label": "알려진 영점 CSV",
            "path": Path("results/zeta_zeros.csv"),
        },
        {
            "label": "알려진 영점 JSON",
            "path": Path("results/zeta_zeros.json"),
        },
        {
            "label": "알려진 영점 HTML 대시보드",
            "path": Path("results/dashboard.html"),
        },
        {
            "label": "독립 임계선 스캔 CSV",
            "path": Path("results_independent/independent_zeta_scan.csv"),
        },
        {
            "label": "독립 임계선 스캔 JSON",
            "path": Path("results_independent/independent_zeta_scan.json"),
        },
        {
            "label": "독립 임계선 스캔 HTML 대시보드",
            "path": Path("results_independent/independent_scan_dashboard.html"),
        },
        {
            "label": "오일러 곱장 CSV",
            "path": Path("results_euler/euler_product_verification.csv"),
        },
        {
            "label": "오일러 곱장 JSON",
            "path": Path("results_euler/euler_product_verification.json"),
        },
        {
            "label": "오일러 곱장 HTML 대시보드",
            "path": Path("results_euler/euler_product_dashboard.html"),
        },
        {
            "label": "함수방정식 대칭 CSV",
            "path": Path("results_symmetry/functional_symmetry_verification.csv"),
        },
        {
            "label": "함수방정식 대칭 JSON",
            "path": Path("results_symmetry/functional_symmetry_verification.json"),
        },
        {
            "label": "함수방정식 대칭 HTML 대시보드",
            "path": Path("results_symmetry/functional_symmetry_dashboard.html"),
        },
        {
            "label": "영점 간격 CSV",
            "path": Path("results_spacing/zero_spacing_verification.csv"),
        },
        {
            "label": "영점 간격 JSON",
            "path": Path("results_spacing/zero_spacing_verification.json"),
        },
        {
            "label": "영점 간격 HTML 대시보드",
            "path": Path("results_spacing/zero_spacing_dashboard.html"),
        },
        {
            "label": "하한 잔차 CSV",
            "path": Path("results_residue/lower_residue_verification.csv"),
        },
        {
            "label": "하한 잔차 JSON",
            "path": Path("results_residue/lower_residue_verification.json"),
        },
        {
            "label": "하한 잔차 HTML 대시보드",
            "path": Path("results_residue/lower_residue_dashboard.html"),
        },
    ]


def main():
    print()
    print("=" * 80)
    print("0축 구조공식 리만가설 수치 검증 전체 실행")
    print("=" * 80)

    commands = build_commands()

    if not commands:
        print("실행할 검증 스크립트가 없습니다.")
        print("현재 폴더에 verify_*.py 파일들이 있는지 확인하세요.")
        return

    print()
    print("실행 대상 스크립트:")

    for item in commands:
        print(f"- {item['label']} : {item['script']}")

    results = []

    for item in commands:
        result = run_command(item["command"], item["label"])
        results.append(result)

    successful_commands = sum(1 for item in results if item["success"])
    failed_commands = sum(1 for item in results if not item["success"])

    output_checks = []

    print()
    print("=" * 80)
    print("결과 파일 확인")
    print("=" * 80)

    for item in expected_outputs():
        path = item["path"]
        exists = path.exists()
        file_hash = sha256_file(path) if exists else None

        output_checks.append(
            {
                "label": item["label"],
                "path": str(path),
                "exists": exists,
                "sha256": file_hash,
            }
        )

        if exists:
            print(f"[OK]      {item['label']} : {path}")
        else:
            print(f"[MISSING] {item['label']} : {path}")

    summary = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_executable": sys.executable,
        "total_commands": len(results),
        "successful_commands": successful_commands,
        "failed_commands": failed_commands,
        "results": results,
        "output_checks": output_checks,
        "structural_verification_stages": [
            "1. Known zeta zero verification",
            "2. Known zero dashboard verification",
            "3. Independent Hardy Z(t) critical-line scan",
            "4. Euler product field verification",
            "5. Functional symmetry around Re(s)=1/2",
            "6. Zero spacing and ascending zero-axis alignment",
            "7. Lower residue structural verification",
        ],
        "important_notice": (
            "This is a finite numerical and structural verification package. "
            "It does not claim that finite computation alone proves the full Riemann Hypothesis."
        ),
    }

    summary_path = Path("verification_run_summary.json")

    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print()
    print("=" * 80)
    print("전체 검증 실행 완료")
    print("=" * 80)
    print(f"성공한 명령: {successful_commands} / {len(results)}")
    print(f"실패한 명령: {failed_commands} / {len(results)}")
    print(f"요약 파일: {summary_path}")

    if failed_commands == 0:
        print()
        print("[최종 결과] 모든 실행 대상 검증이 정상 완료되었습니다.")
    else:
        print()
        print("[주의] 실패한 검증이 있습니다. 위의 오류 출력을 확인하세요.")

    print()
    print("대시보드 열기 명령:")
    print("start results/dashboard.html")
    print("start results_independent/independent_scan_dashboard.html")
    print("start results_euler/euler_product_dashboard.html")
    print("start results_symmetry/functional_symmetry_dashboard.html")
    print("start results_spacing/zero_spacing_dashboard.html")
    print("start results_residue/lower_residue_dashboard.html")
    print()


if __name__ == "__main__":
    main()