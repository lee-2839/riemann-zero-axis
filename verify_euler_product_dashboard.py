# verify_euler_product_dashboard.py
# Euler product verification for the Zero-Axis project.
#
# This script numerically verifies the relation:
#
#   zeta(s) ≈ product over primes p of 1 / (1 - p^(-s))
#
# in the convergence region Re(s) > 1.
#
# In the Zero-Axis structural interpretation:
#
#   P = prime self-rotation
#   E = product of P = Euler product field
#   Z = generation(E)
#
# Therefore this script checks the numerical link:
#
#   E = ∏P  -->  Z = ζ(s)
#
# Important:
# This is not a proof of the Riemann Hypothesis.
# It is a reproducible numerical verification of the Euler product structure
# in the region where the Euler product converges.

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import mpmath as mp


def primes_upto(n):
    """Return all primes <= n using a simple sieve."""
    if n < 2:
        return []

    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"

    limit = int(n ** 0.5) + 1

    for i in range(2, limit):
        if sieve[i]:
            step = i
            start = i * i
            sieve[start:n + 1:step] = b"\x00" * (((n - start) // step) + 1)

    return [i for i in range(2, n + 1) if sieve[i]]


def euler_product(s, primes):
    """Compute partial Euler product over the given primes."""
    product = mp.mpc(1)

    for p in primes:
        p_mpf = mp.mpf(p)
        product *= 1 / (1 - mp.power(p_mpf, -s))

    return product


def sha256_file(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)

    return h.hexdigest()


def complex_to_string(z, digits=40):
    return mp.nstr(z, digits)


def make_html_report(
    output_path,
    metadata,
    rows,
    csv_hash,
    json_hash,
):
    passed = sum(1 for row in rows if row["pass"])
    total = len(rows)

    table_rows = []

    for row in rows:
        status = "PASS" if row["pass"] else "FAIL"

        table_rows.append(
            f"""
            <tr>
                <td>{row["label"]}</td>
                <td>{row["s"]}</td>
                <td>{row["zeta_s"]}</td>
                <td>{row["euler_product"]}</td>
                <td>{row["absolute_error"]}</td>
                <td>{row["relative_error"]}</td>
                <td>{status}</td>
            </tr>
            """
        )

    html = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>Euler Product Verification Dashboard</title>
<style>
body {{
    font-family: Arial, sans-serif;
    margin: 32px;
    line-height: 1.55;
}}
h1, h2 {{
    color: #222;
}}
code, pre {{
    background: #f4f4f4;
    padding: 2px 4px;
}}
table {{
    border-collapse: collapse;
    width: 100%;
    margin-top: 20px;
}}
th, td {{
    border: 1px solid #ccc;
    padding: 8px;
    vertical-align: top;
    font-size: 13px;
}}
th {{
    background: #f0f0f0;
}}
.pass {{
    color: green;
    font-weight: bold;
}}
.notice {{
    background: #fff8dc;
    border: 1px solid #e6d28a;
    padding: 12px;
    margin: 16px 0;
}}
.formula {{
    background: #f7f7f7;
    border-left: 4px solid #777;
    padding: 12px;
    margin: 14px 0;
    font-family: monospace;
}}
</style>
</head>
<body>

<h1>Euler Product Verification Dashboard</h1>

<div class="notice">
This dashboard verifies the Euler product relation in the convergence region Re(s) &gt; 1.
It does not claim to prove the full Riemann Hypothesis.
</div>

<h2>Zero-Axis Structural Meaning</h2>

<div class="formula">
P = prime self-rotation<br>
E = ∏P = ∏Crit = total orbital field<br>
Z = generation(E)
</div>

<h2>Standard Numerical Relation</h2>

<div class="formula">
ζ(s) ≈ ∏p 1 / (1 - p^(-s)), &nbsp; Re(s) &gt; 1
</div>

<h2>Run Metadata</h2>

<ul>
<li>Created at UTC: {metadata["created_at_utc"]}</li>
<li>mpmath decimal precision: {metadata["mpmath_dps"]}</li>
<li>Prime max: {metadata["prime_max"]}</li>
<li>Prime count: {metadata["prime_count"]}</li>
<li>Tolerance: {metadata["tolerance"]}</li>
<li>Passed: <span class="pass">{passed} / {total}</span></li>
</ul>

<h2>Verification Results</h2>

<table>
<thead>
<tr>
<th>Label</th>
<th>s</th>
<th>ζ(s)</th>
<th>Euler Product</th>
<th>Absolute Error</th>
<th>Relative Error</th>
<th>Status</th>
</tr>
</thead>
<tbody>
{''.join(table_rows)}
</tbody>
</table>

<h2>File Hashes</h2>

<ul>
<li>CSV SHA256: <code>{csv_hash}</code></li>
<li>JSON SHA256: <code>{json_hash}</code></li>
</ul>

<h2>Interpretation</h2>

<p>
This verification confirms that finite prime products approximate ζ(s)
in the region Re(s) &gt; 1. In the proposed zero-axis structure,
this supports the numerical connection between the prime self-rotation field
and the zeta generation field.
</p>

<p>
However, because the Euler product converges only for Re(s) &gt; 1,
this verification is structurally connected to the Euler product field,
not a direct proof of the critical-line statement Re(ρ)=1/2.
</p>

</body>
</html>
"""

    output_path.write_text(html, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Verify Euler product approximation to zeta(s) for Re(s) > 1."
    )

    parser.add_argument(
        "--prime-max",
        type=int,
        default=100000,
        help="Use all primes up to this value.",
    )

    parser.add_argument(
        "--dps",
        type=int,
        default=80,
        help="mpmath decimal precision.",
    )

    parser.add_argument(
        "--tol",
        type=float,
        default=1e-3,
        help="Relative error tolerance.",
    )

    parser.add_argument(
        "--outdir",
        type=str,
        default="results_euler",
        help="Output directory.",
    )

    args = parser.parse_args()

    mp.mp.dps = args.dps

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    csv_path = outdir / "euler_product_verification.csv"
    json_path = outdir / "euler_product_verification.json"
    html_path = outdir / "euler_product_dashboard.html"

    primes = primes_upto(args.prime_max)

    # Test points are chosen in Re(s) > 1,
    # where the Euler product converges.
    test_points = [
        ("real_s_2", mp.mpc(2, 0)),
        ("real_s_3", mp.mpc(3, 0)),
        ("complex_2_plus_5i", mp.mpc(2, 5)),
        ("complex_2_plus_10i", mp.mpc(2, 10)),
        ("complex_1_5_plus_5i", mp.mpc(1.5, 5)),
        ("complex_1_5_plus_14i", mp.mpc(1.5, 14)),
    ]

    rows = []

    for label, s in test_points:
        zeta_s = mp.zeta(s)
        product_s = euler_product(s, primes)

        absolute_error = abs(zeta_s - product_s)
        relative_error = absolute_error / max(mp.mpf(1), abs(zeta_s))

        passed = relative_error <= args.tol

        rows.append(
            {
                "label": label,
                "s": complex_to_string(s),
                "zeta_s": complex_to_string(zeta_s),
                "euler_product": complex_to_string(product_s),
                "absolute_error": mp.nstr(absolute_error, 30),
                "relative_error": mp.nstr(relative_error, 30),
                "pass": bool(passed),
            }
        )

    metadata = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "mpmath_dps": args.dps,
        "prime_max": args.prime_max,
        "prime_count": len(primes),
        "tolerance": args.tol,
        "note": (
            "Euler product verification is performed only in Re(s) > 1, "
            "where the Euler product converges. This is not a proof of RH."
        ),
        "zero_axis_structure": {
            "P": "prime self-rotation",
            "E": "Euler product field = product of prime self-rotations",
            "Z": "zeta generation field",
            "structural_formula": "E = product(P) = product(Crit), Z = generation(E)",
        },
        "results": rows,
    }

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "label",
                "s",
                "zeta_s",
                "euler_product",
                "absolute_error",
                "relative_error",
                "pass",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    csv_hash = sha256_file(csv_path)
    json_hash = sha256_file(json_path)

    make_html_report(
        html_path,
        metadata,
        rows,
        csv_hash,
        json_hash,
    )

    passed_count = sum(1 for row in rows if row["pass"])

    print()
    print("Euler product verification complete")
    print()
    print(f"Prime max: {args.prime_max}")
    print(f"Prime count: {len(primes)}")
    print(f"mpmath dps: {args.dps}")
    print(f"Tolerance: {args.tol}")
    print(f"Passed: {passed_count} / {len(rows)}")
    print()
    print("Saved:")
    print(f"- {csv_path}")
    print(f"- {json_path}")
    print(f"- {html_path}")
    print()
    print("Important:")
    print("This verifies the Euler product only in Re(s) > 1.")
    print("It is not a finite-computation proof of the full Riemann Hypothesis.")


if __name__ == "__main__":
    main()