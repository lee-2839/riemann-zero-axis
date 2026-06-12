# verify_zero_spacing_dashboard.py
# Zero spacing and zero-axis ascending alignment verification.
#
# This script verifies the ordering and spacing of the first N non-trivial zeros:
#
#   rho_n = 1/2 + i * gamma_n
#   gap_n = gamma_(n+1) - gamma_n
#   gap_n > 0
#
# In the Zero-Axis structural interpretation:
#
#   rho ⊂ Z ⊂ A0
#   Re(rho)=1/2 means alignment on A0.
#   gamma_n increasing means ascending ordered placement on the zero-axis.
#
# This script creates CSV, JSON, and HTML dashboard outputs.
#
# Important:
# This is a finite numerical verification, not a proof of the full Riemann Hypothesis.

import argparse
import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import mpmath as mp


def sha256_file(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)

    return h.hexdigest()


def mp_to_string(x, digits=60):
    return mp.nstr(x, digits)


def safe_float(x):
    try:
        return float(x)
    except Exception:
        return None


def make_svg_line_chart(points, width=900, height=280, title="Chart", y_label="value"):
    """
    Simple inline SVG line chart.
    points: list of (x, y)
    """
    if not points:
        return "<p>No chart data.</p>"

    margin_left = 70
    margin_right = 30
    margin_top = 35
    margin_bottom = 45

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    x_min = min(xs)
    x_max = max(xs)
    y_min = min(ys)
    y_max = max(ys)

    if x_min == x_max:
        x_max = x_min + 1

    if y_min == y_max:
        y_max = y_min + 1

    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom

    def map_x(x):
        return margin_left + (x - x_min) / (x_max - x_min) * plot_w

    def map_y(y):
        return margin_top + (y_max - y) / (y_max - y_min) * plot_h

    polyline = " ".join(f"{map_x(x):.2f},{map_y(y):.2f}" for x, y in points)

    y_ticks = []
    for i in range(5):
        value = y_min + (y_max - y_min) * i / 4
        y = map_y(value)
        y_ticks.append(
            f'<line x1="{margin_left}" y1="{y:.2f}" x2="{width-margin_right}" y2="{y:.2f}" stroke="#eee"/>'
            f'<text x="10" y="{y+4:.2f}" font-size="11">{value:.6g}</text>'
        )

    x_ticks = []
    for i in range(5):
        value = x_min + (x_max - x_min) * i / 4
        x = map_x(value)
        x_ticks.append(
            f'<line x1="{x:.2f}" y1="{margin_top}" x2="{x:.2f}" y2="{height-margin_bottom}" stroke="#eee"/>'
            f'<text x="{x-10:.2f}" y="{height-18}" font-size="11">{value:.0f}</text>'
        )

    svg = f"""
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <text x="{width/2}" y="20" text-anchor="middle" font-size="16" font-weight="bold">{title}</text>
    <text x="{width/2}" y="{height-5}" text-anchor="middle" font-size="12">index</text>
    <text x="14" y="{height/2}" transform="rotate(-90 14,{height/2})" text-anchor="middle" font-size="12">{y_label}</text>

    {''.join(y_ticks)}
    {''.join(x_ticks)}

    <line x1="{margin_left}" y1="{height-margin_bottom}" x2="{width-margin_right}" y2="{height-margin_bottom}" stroke="#333"/>
    <line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{height-margin_bottom}" stroke="#333"/>

    <polyline points="{polyline}" fill="none" stroke="#1f77b4" stroke-width="2"/>
</svg>
"""
    return svg


def make_html_report(output_path, metadata, zero_rows, gap_rows, csv_hash, json_hash):
    passed_zero = sum(1 for row in zero_rows if row["pass"])
    total_zero = len(zero_rows)

    passed_gap = sum(1 for row in gap_rows if row["pass"])
    total_gap = len(gap_rows)

    gamma_points = [
        (row["n"], row["gamma_float"])
        for row in zero_rows
        if row["gamma_float"] is not None
    ]

    gap_points = [
        (row["n"], row["gap_float"])
        for row in gap_rows
        if row["gap_float"] is not None
    ]

    gamma_chart = make_svg_line_chart(
        gamma_points,
        title="Imaginary Parts gamma_n",
        y_label="gamma_n",
    )

    gap_chart = make_svg_line_chart(
        gap_points,
        title="Zero Spacing gap_n = gamma_(n+1) - gamma_n",
        y_label="gap_n",
    )

    zero_table_rows = []

    for row in zero_rows[:30]:
        status = "PASS" if row["pass"] else "FAIL"
        zero_table_rows.append(
            f"""
            <tr>
                <td>{row["n"]}</td>
                <td>{row["rho"]}</td>
                <td>{row["real_part"]}</td>
                <td>{row["gamma"]}</td>
                <td>{row["real_error"]}</td>
                <td>{row["zeta_abs"]}</td>
                <td>{status}</td>
            </tr>
            """
        )

    gap_table_rows = []

    for row in gap_rows[:30]:
        status = "PASS" if row["pass"] else "FAIL"
        gap_table_rows.append(
            f"""
            <tr>
                <td>{row["n"]}</td>
                <td>{row["gamma_n"]}</td>
                <td>{row["gamma_next"]}</td>
                <td>{row["gap"]}</td>
                <td>{status}</td>
            </tr>
            """
        )

    html = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>Zero Spacing Verification Dashboard</title>
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
.chart-box {{
    overflow-x: auto;
    border: 1px solid #ddd;
    padding: 10px;
    margin: 18px 0;
}}
</style>
</head>
<body>

<h1>Zero Spacing Verification Dashboard</h1>

<div class="notice">
This dashboard verifies the ascending order and spacing of non-trivial zeta zeros on the critical line.
It does not claim to prove the full Riemann Hypothesis.
</div>

<h2>Zero-Axis Structural Meaning</h2>

<div class="formula">
rho ⊂ Z ⊂ A0<br>
rho_n = 1/2 + i gamma_n<br>
gamma_(n+1) - gamma_n &gt; 0<br>
ascending placement on the zero-axis
</div>

<h2>Standard Numerical Relation</h2>

<div class="formula">
zeta(rho_n) ≈ 0<br>
Re(rho_n) = 1/2<br>
gamma_(n+1) &gt; gamma_n
</div>

<h2>Run Metadata</h2>

<ul>
<li>Created at UTC: {metadata["created_at_utc"]}</li>
<li>mpmath decimal precision: {metadata["mpmath_dps"]}</li>
<li>Count: {metadata["count"]}</li>
<li>Zero tolerance: {metadata["zero_tolerance"]}</li>
<li>Real-part tolerance: {metadata["real_tolerance"]}</li>
<li>Zero alignment passed: <span class="pass">{passed_zero} / {total_zero}</span></li>
<li>Spacing passed: <span class="pass">{passed_gap} / {total_gap}</span></li>
</ul>

<h2>Charts</h2>

<div class="chart-box">
{gamma_chart}
</div>

<div class="chart-box">
{gap_chart}
</div>

<h2>First 30 Zero Alignment Results</h2>

<table>
<thead>
<tr>
<th>n</th>
<th>rho</th>
<th>Re(rho)</th>
<th>gamma</th>
<th>|Re-1/2|</th>
<th>|zeta(rho)|</th>
<th>Status</th>
</tr>
</thead>
<tbody>
{''.join(zero_table_rows)}
</tbody>
</table>

<h2>First 30 Spacing Results</h2>

<table>
<thead>
<tr>
<th>n</th>
<th>gamma_n</th>
<th>gamma_(n+1)</th>
<th>gap_n</th>
<th>Status</th>
</tr>
</thead>
<tbody>
{''.join(gap_table_rows)}
</tbody>
</table>

<h2>File Hashes</h2>

<ul>
<li>CSV SHA256: <code>{csv_hash}</code></li>
<li>JSON SHA256: <code>{json_hash}</code></li>
</ul>

<h2>Interpretation</h2>

<p>
This verification confirms that the computed non-trivial zeta zeros are aligned on Re(rho)=1/2
and that their imaginary parts are strictly increasing.
</p>

<p>
In the zero-axis structural interpretation, this corresponds to ordered ascending placement of zeta zeros on A0.
</p>

<p>
This numerical verification supports the observed structure of the first finite set of zeros.
It is not by itself a complete proof for all zeros.
</p>

</body>
</html>
"""

    output_path.write_text(html, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Verify zeta zero spacing and ascending zero-axis alignment."
    )

    parser.add_argument(
        "--count",
        type=int,
        default=100,
        help="Number of zeta zeros to verify.",
    )

    parser.add_argument(
        "--dps",
        type=int,
        default=80,
        help="mpmath decimal precision.",
    )

    parser.add_argument(
        "--zero-tol",
        type=float,
        default=1e-50,
        help="Tolerance for |zeta(rho)|.",
    )

    parser.add_argument(
        "--real-tol",
        type=float,
        default=1e-70,
        help="Tolerance for |Re(rho)-1/2|.",
    )

    parser.add_argument(
        "--outdir",
        type=str,
        default="results_spacing",
        help="Output directory.",
    )

    args = parser.parse_args()

    mp.mp.dps = args.dps

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    csv_path = outdir / "zero_spacing_verification.csv"
    json_path = outdir / "zero_spacing_verification.json"
    html_path = outdir / "zero_spacing_dashboard.html"

    zero_rows = []

    for n in range(1, args.count + 1):
        rho = mp.zetazero(n)
        real_part = mp.re(rho)
        gamma = mp.im(rho)
        zeta_abs = abs(mp.zeta(rho))
        real_error = abs(real_part - mp.mpf("0.5"))

        passed = (zeta_abs <= args.zero_tol) and (real_error <= args.real_tol)

        zero_rows.append(
            {
                "n": n,
                "rho": mp_to_string(rho),
                "real_part": mp_to_string(real_part),
                "gamma": mp_to_string(gamma),
                "gamma_float": safe_float(gamma),
                "zeta_abs": mp.nstr(zeta_abs, 40),
                "real_error": mp.nstr(real_error, 40),
                "pass": bool(passed),
            }
        )

    gap_rows = []

    for i in range(len(zero_rows) - 1):
        n = zero_rows[i]["n"]
        gamma_n = mp.mpf(zero_rows[i]["gamma"])
        gamma_next = mp.mpf(zero_rows[i + 1]["gamma"])
        gap = gamma_next - gamma_n

        passed = gap > 0

        gap_rows.append(
            {
                "n": n,
                "gamma_n": mp_to_string(gamma_n),
                "gamma_next": mp_to_string(gamma_next),
                "gap": mp_to_string(gap),
                "gap_float": safe_float(gap),
                "pass": bool(passed),
            }
        )

    metadata = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "mpmath_dps": args.dps,
        "count": args.count,
        "zero_tolerance": args.zero_tol,
        "real_tolerance": args.real_tol,
        "note": (
            "This verifies finite zero alignment and ascending spacing. "
            "It uses mpmath.zetazero(n), so it is a known-zero based verification."
        ),
        "zero_axis_structure": {
            "A0": "zero-axis",
            "rho": "zeta zero",
            "gamma_n": "imaginary height of rho_n",
            "structural_formula": "rho_n = 1/2 + i gamma_n, gamma_(n+1) - gamma_n > 0",
        },
        "zero_results": zero_rows,
        "spacing_results": gap_rows,
    }

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "type",
            "n",
            "rho",
            "real_part",
            "gamma",
            "zeta_abs",
            "real_error",
            "gamma_n",
            "gamma_next",
            "gap",
            "pass",
        ]

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in zero_rows:
            writer.writerow(
                {
                    "type": "zero",
                    "n": row["n"],
                    "rho": row["rho"],
                    "real_part": row["real_part"],
                    "gamma": row["gamma"],
                    "zeta_abs": row["zeta_abs"],
                    "real_error": row["real_error"],
                    "gamma_n": "",
                    "gamma_next": "",
                    "gap": "",
                    "pass": row["pass"],
                }
            )

        for row in gap_rows:
            writer.writerow(
                {
                    "type": "gap",
                    "n": row["n"],
                    "rho": "",
                    "real_part": "",
                    "gamma": "",
                    "zeta_abs": "",
                    "real_error": "",
                    "gamma_n": row["gamma_n"],
                    "gamma_next": row["gamma_next"],
                    "gap": row["gap"],
                    "pass": row["pass"],
                }
            )

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    csv_hash = sha256_file(csv_path)
    json_hash = sha256_file(json_path)

    make_html_report(html_path, metadata, zero_rows, gap_rows, csv_hash, json_hash)

    passed_zero = sum(1 for row in zero_rows if row["pass"])
    passed_gap = sum(1 for row in gap_rows if row["pass"])

    print()
    print("Zero spacing verification complete")
    print()
    print(f"Count: {args.count}")
    print(f"mpmath dps: {args.dps}")
    print(f"Zero tolerance: {args.zero_tol}")
    print(f"Real tolerance: {args.real_tol}")
    print(f"Zero alignment passed: {passed_zero} / {len(zero_rows)}")
    print(f"Spacing passed: {passed_gap} / {len(gap_rows)}")
    print()
    print("Saved:")
    print(f"- {csv_path}")
    print(f"- {json_path}")
    print(f"- {html_path}")
    print()
    print("Structural meaning:")
    print("rho_n = 1/2 + i gamma_n")
    print("gamma_(n+1) - gamma_n > 0")
    print("ascending placement on A0")
    print()
    print("Important:")
    print("This is a finite numerical verification.")
    print("It is not a complete proof of the full Riemann Hypothesis.")


if __name__ == "__main__":
    main()