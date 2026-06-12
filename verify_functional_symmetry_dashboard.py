# verify_functional_symmetry_dashboard.py
# Functional equation symmetry verification for the Zero-Axis project.
#
# This script numerically verifies the symmetry of the completed zeta function:
#
#   Lambda(s) = Lambda(1 - s)
#
# where:
#
#   Lambda(s) = pi^(-s/2) * Gamma(s/2) * zeta(s)
#
# In the Zero-Axis structural interpretation:
#
#   1 -> 0.5 | 0.5 = A0
#   A0 = central boundary / zero-axis
#
# The symmetry s <-> 1-s numerically corresponds to reflection around
# the central line Re(s)=1/2.
#
# Important:
# This is not a complete proof of the Riemann Hypothesis.
# It is a reproducible numerical verification of the zeta functional symmetry.

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import mpmath as mp


def completed_zeta(s):
    """
    Completed zeta function:
        Lambda(s) = pi^(-s/2) * Gamma(s/2) * zeta(s)

    This form satisfies:
        Lambda(s) = Lambda(1-s)
    by the functional equation.
    """
    return mp.power(mp.pi, -s / 2) * mp.gamma(s / 2) * mp.zeta(s)


def sha256_file(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)

    return h.hexdigest()


def complex_to_string(z, digits=50):
    return mp.nstr(z, digits)


def make_html_report(output_path, metadata, rows, csv_hash, json_hash):
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
                <td>{row["one_minus_s"]}</td>
                <td>{row["lambda_s"]}</td>
                <td>{row["lambda_1_minus_s"]}</td>
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
<title>Functional Symmetry Verification Dashboard</title>
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

<h1>Functional Symmetry Verification Dashboard</h1>

<div class="notice">
This dashboard verifies the completed zeta symmetry Lambda(s) = Lambda(1-s).
It does not claim to prove the full Riemann Hypothesis.
</div>

<h2>Zero-Axis Structural Meaning</h2>

<div class="formula">
1 → 0.5 | 0.5 = A0<br>
A0 = central boundary / zero-axis<br>
s ↔ 1-s = reflection around Re(s)=1/2
</div>

<h2>Standard Functional Symmetry</h2>

<div class="formula">
Lambda(s) = pi^(-s/2) Gamma(s/2) zeta(s)<br>
Lambda(s) = Lambda(1-s)
</div>

<h2>Run Metadata</h2>

<ul>
<li>Created at UTC: {metadata["created_at_utc"]}</li>
<li>mpmath decimal precision: {metadata["mpmath_dps"]}</li>
<li>Tolerance: {metadata["tolerance"]}</li>
<li>Test count: {metadata["test_count"]}</li>
<li>Passed: <span class="pass">{passed} / {total}</span></li>
</ul>

<h2>Verification Results</h2>

<table>
<thead>
<tr>
<th>Label</th>
<th>s</th>
<th>1-s</th>
<th>Lambda(s)</th>
<th>Lambda(1-s)</th>
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
This verification checks the symmetry of the completed zeta function
under the transformation s ↔ 1-s.
</p>

<p>
In the zero-axis structural interpretation, this corresponds to
the central boundary 0.5 | 0.5 = A0.
The symmetry is centered around Re(s)=1/2.
</p>

<p>
This numerical verification supports the structural role of the 1/2 axis,
but it is not by itself a complete proof that all non-trivial zeros lie on that axis.
</p>

</body>
</html>
"""

    output_path.write_text(html, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Verify completed zeta functional symmetry Lambda(s)=Lambda(1-s)."
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
        default=1e-60,
        help="Relative error tolerance.",
    )

    parser.add_argument(
        "--outdir",
        type=str,
        default="results_symmetry",
        help="Output directory.",
    )

    args = parser.parse_args()

    mp.mp.dps = args.dps

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    csv_path = outdir / "functional_symmetry_verification.csv"
    json_path = outdir / "functional_symmetry_verification.json"
    html_path = outdir / "functional_symmetry_dashboard.html"

    # Test points avoid poles and numerically unstable special points.
    # The symmetry is checked across the central line Re(s)=1/2.
    test_points = [
        ("s_2_plus_3i", mp.mpc(2, 3)),
        ("s_2_plus_10i", mp.mpc(2, 10)),
        ("s_1_5_plus_14i", mp.mpc(1.5, 14)),
        ("s_0_25_plus_5i", mp.mpc(0.25, 5)),
        ("s_0_75_plus_7i", mp.mpc(0.75, 7)),
        ("s_minus_1_plus_4i", mp.mpc(-1, 4)),
        ("s_3_plus_20i", mp.mpc(3, 20)),
        ("s_0_4_plus_30i", mp.mpc(0.4, 30)),
    ]

    rows = []

    for label, s in test_points:
        one_minus_s = 1 - s

        lambda_s = completed_zeta(s)
        lambda_1_minus_s = completed_zeta(one_minus_s)

        absolute_error = abs(lambda_s - lambda_1_minus_s)
        relative_error = absolute_error / max(mp.mpf(1), abs(lambda_s), abs(lambda_1_minus_s))

        passed = relative_error <= args.tol

        rows.append(
            {
                "label": label,
                "s": complex_to_string(s),
                "one_minus_s": complex_to_string(one_minus_s),
                "lambda_s": complex_to_string(lambda_s),
                "lambda_1_minus_s": complex_to_string(lambda_1_minus_s),
                "absolute_error": mp.nstr(absolute_error, 40),
                "relative_error": mp.nstr(relative_error, 40),
                "pass": bool(passed),
            }
        )

    metadata = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "mpmath_dps": args.dps,
        "tolerance": args.tol,
        "test_count": len(rows),
        "note": (
            "This verifies the completed zeta functional symmetry Lambda(s)=Lambda(1-s). "
            "It is a numerical verification, not a complete proof of RH."
        ),
        "zero_axis_structure": {
            "A0": "zero-axis",
            "central_boundary": "0.5 | 0.5",
            "structural_formula": "1 -> 0.5 | 0.5 = A0",
            "symmetry": "s <-> 1-s reflection around Re(s)=1/2",
        },
        "results": rows,
    }

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "label",
                "s",
                "one_minus_s",
                "lambda_s",
                "lambda_1_minus_s",
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

    make_html_report(html_path, metadata, rows, csv_hash, json_hash)

    passed_count = sum(1 for row in rows if row["pass"])

    print()
    print("Functional symmetry verification complete")
    print()
    print(f"mpmath dps: {args.dps}")
    print(f"Tolerance: {args.tol}")
    print(f"Passed: {passed_count} / {len(rows)}")
    print()
    print("Saved:")
    print(f"- {csv_path}")
    print(f"- {json_path}")
    print(f"- {html_path}")
    print()
    print("Structural meaning:")
    print("1 -> 0.5 | 0.5 = A0")
    print("s <-> 1-s reflection around Re(s)=1/2")
    print()
    print("Important:")
    print("This verifies the functional symmetry numerically.")
    print("It is not a finite-computation proof of the full Riemann Hypothesis.")


if __name__ == "__main__":
    main()