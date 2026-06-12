# verify_zeta.py

import mpmath as mp

mp.mp.dps = 50


def check_zeta_zero(n: int, tol=mp.mpf("1e-40")):
    """
    n번째 비자명 제타 영점을 수치적으로 확인한다.
    확인 항목:
    1. Re(rho)가 1/2에 가까운가
    2. zeta(rho)가 0에 가까운가
    """
    rho = mp.zetazero(n)
    real_error = abs(mp.re(rho) - mp.mpf("0.5"))
    zeta_value = mp.zeta(rho)
    zeta_error = abs(zeta_value)

    return {
        "n": n,
        "rho": rho,
        "real_part": mp.re(rho),
        "imag_part": mp.im(rho),
        "real_error": real_error,
        "zeta_error": zeta_error,
        "passes": real_error < tol and zeta_error < tol,
    }


def main():
    for n in range(1, 11):
        result = check_zeta_zero(n)
        print(f"zero #{result['n']}")
        print(f"rho        = {result['rho']}")
        print(f"Re(rho)    = {result['real_part']}")
        print(f"Im(rho)    = {result['imag_part']}")
        print(f"|Re-1/2|   = {result['real_error']}")
        print(f"|zeta(rho)|= {result['zeta_error']}")
        print(f"pass       = {result['passes']}")
        print("-" * 60)


if __name__ == "__main__":
    main()