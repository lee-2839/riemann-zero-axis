# verify_lower_residue_dashboard.py
# Lower residue verification for the Zero-Axis project.
#
# This script verifies the internal structural relation:
#
#   phase difference(X, R_theta) = 180 degrees
#   180-degree phase difference -> residue r
#   r != 0
#   L_lower = r^2
#   L_lower > 0
#
# In the Zero-Axis structural interpretation:
#
#   lower residue is not arbitrary
#   lower residue comes from the 180-degree phase difference
#   outside-axis collapse would force r = 0
#   but structural residue requires r != 0
#
# This is a structural consistency verification, not a standard proof
# of the Riemann Hypothesis.

import argparse
import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)

    return h.hexdigest()


def compute_residue(theta_degrees, scale):
    """
    Residue model from phase opposition.

    We model the phase difference as:

        r = scale * |sin(theta / 2)|

    For theta = 180 degrees:

        r = scale * |sin(90 degrees)| = scale

    Therefore:

        if scale > 0, then r > 0 and L_lower = r^2 > 0.

    This is a numerical structural model for the user's formula:
        phase difference(X, R_theta)=180 degrees -> r != 0 -> L_lower=r^2>0
    """
    theta_radians = math.radians(theta_degrees)
    r = scale * abs(math.sin(theta_radians / 2.0))
    l_lower = r ** 2
    return r, l_lower


def make_svg_line_chart(points, width=900, height=280, title="Chart", y_label="value"):
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
    <text x="{width/2}" y="{height-5}" text-anchor="middle" font-size="12">phase difference degree</text>
    <text x="14" y="{height/2}" transform="rotate(-90 14,{height/2})" text-anchor="middle" font-size="12">{y_label}</text>

    {''.join(y_ticks)}
    {''.join(x_ticks)}

    <line x1="{margin_left}" y1="{height-margin_bottom}" x2="{width-margin_right}" y2="{height-margin_bottom}" stroke="#333"/>
    <line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{height-margin_bottom}" stroke="#333"/>

    <polyline points="{polyline}" fill="none" stroke="#1f77b4" stroke-width="2"/>
</svg>
"""
    return svg


def make_html_report(output_path, metadata, rows, csv_hash, json_hash):
    passed = sum(1 for row in rows if row["pass"])
    total = len(rows)

    residue_points = [(row["theta_degrees"], row["r"]) for row in rows]
    lower_points = [(row["theta_degrees"], row["L_lower"]) for row in rows]

    residue_chart = make_svg_line_chart(
        residue_points,
        title="Residue r from Phase Difference",
        y_label="r",
    )

    lower_chart = make_svg_line_chart(
        lower_points,
        title="Lower Bound L_lower = r^2",
        y_label="L_lower",
    )

    table_rows = []

    for row in rows:
        status = "PASS" if row["pass"] else "FAIL"

        table_rows.append(
            f"""
            <tr>
                <td>{row["theta_degrees"]}</td>
                <td>{row["scale"]}</td>
                <td>{row["r"]}</td>
                <td>{row["L_lower"]}</td>
                <td>{row["r_nonzero"]}</td>
                <td>{row["L_lower_positive"]}</td>
                <td>{status}</td>
            </tr>
            """
        )

    html = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>Lower Residue Verification Dashboard</title>
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

<h1>Lower Residue Verification Dashboard</h1>

<div class="notice">
This dashboard verifies the internal lower-residue relation of the Zero-Axis structure.
It does not claim to prove the full Riemann Hypothesis.
</div>

<h2>Zero-Axis Structural Meaning</h2>

<div class="formula">
phase difference(X, R_theta) = 180 degrees<br>
180-degree phase difference → r generated<br>
r ≠ 0<br>
L_lower = r^2<br>
L_lower &gt; 0
</div>

<h2>Numerical Residue Model</h2>

<div class="formula">
r = scale × |sin(theta / 2)|<br>
L_lower = r^2<br>
theta = 180 degrees → r = scale<br>
scale &gt; 0 → L_lower &gt; 0
</div>

<h2>Run Metadata</h2>

<ul>
<li>Created at UTC: {metadata["created_at_utc"]}</li>
<li>Scale: {metadata["scale"]}</li>
<li>Target phase difference: {metadata["target_theta_degrees"]} degrees</li>
<li>Epsilon for nonzero check: {metadata["epsilon"]}</li>
<li>Test count: {metadata["test_count"]}</li>
<li>Passed: <span class="pass">{passed} / {total}</span></li>
</ul>

<h2>Charts</h2>

<div class="chart-box">
{residue_chart}
</div>

<div class="chart-box">
{lower_chart}
</div>

<h2>Verification Results</h2>

<table>
<thead>
<tr>
<th>theta degrees</th>
<th>scale</th>
<th>r</th>
<th>L_lower</th>
<th>r != 0</th>
<th>L_lower > 0</th>
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
This verification confirms that a 180-degree phase difference generates a nonzero residue
under the selected structural model.
</p>

<p>
Because L_lower = r^2, any nonzero residue produces a strictly positive lower bound.
</p>

<p>
In the Zero-Axis interpretation, this supports the statement that the lower residue is not arbitrary:
it is generated by phase opposition and remains greater than zero.
</p>

<p>
This is an internal structural verification. It is not a direct standard zeta-zero proof.
</p>

</body>
</html>
"""

    output_path.write_text(html, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Verify lower residue relation r != 0 and L_lower = r^2 > 0."
    )

    parser.add_argument(
        "--scale",
        type=float,
        default=1.0,
        help="Positive scale factor for residue.",
    )

    parser.add_argument(
        "--epsilon",
        type=float,
        default=1e-12,
        help="Numerical threshold for nonzero checks.",
    )

    parser.add_argument(
        "--outdir",
        type=str,
        default="results_residue",
        help="Output directory.",
    )

    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    csv_path = outdir / "lower_residue_verification.csv"
    json_path = outdir / "lower_residue_verification.json"
    html_path = outdir / "lower_residue_dashboard.html"

    # We include several angles to show the structure:
    # 0 degrees collapses to r=0.
    # 180 degrees gives maximum opposition and nonzero residue.
    theta_values = [
        0,
        30,
        60,
        90,
        120,
        150,
        180,
    ]

    rows = []

    for theta in theta_values:
        r, l_lower = compute_residue(theta, args.scale)

        r_nonzero = abs(r) > args.epsilon
        l_lower_positive = l_lower > args.epsilon

        # The central structural target is theta = 180 degrees.
        # For theta = 0, collapse is expected, so we do not treat it as failure.
        # For theta > 0, the residue should be nonzero and the lower bound positive.
        if theta == 0:
            passed = abs(r) <= args.epsilon and l_lower <= args.epsilon
        else:
            passed = r_nonzero and l_lower_positive

        rows.append(
            {
                "theta_degrees": theta,
                "scale": args.scale,
                "r": r,
                "L_lower": l_lower,
                "r_nonzero": r_nonzero,
                "L_lower_positive": l_lower_positive,
                "pass": bool(passed),
            }
        )

    metadata = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "scale": args.scale,
        "target_theta_degrees": 180,
        "epsilon": args.epsilon,
        "test_count": len(rows),
        "note": (
            "This verifies the structural relation: phase opposition generates residue, "
            "r != 0, and L_lower = r^2 > 0. "
            "It is an internal structural verification, not a standard proof of RH."
        ),
        "zero_axis_structure": {
            "X": "diagonal phase of fixed cross",
            "R_theta": "rotational phase",
            "r": "lower residue",
            "L_lower": "lower bound = r^2",
            "structural_formula": "phase difference(X,R_theta)=180 degrees -> r != 0 -> L_lower=r^2>0",
        },
        "residue_model": {
            "formula": "r = scale * abs(sin(theta/2))",
            "target_theta_degrees": 180,
        },
        "results": rows,
    }

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "theta_degrees",
            "scale",
            "r",
            "L_lower",
            "r_nonzero",
            "L_lower_positive",
            "pass",
        ]

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    csv_hash = sha256_file(csv_path)
    json_hash = sha256_file(json_path)

    make_html_report(html_path, metadata, rows, csv_hash, json_hash)

    passed_count = sum(1 for row in rows if row["pass"])

    print()
    print("Lower residue verification complete")
    print()
    print(f"Scale: {args.scale}")
    print(f"Target phase difference: 180 degrees")
    print(f"Epsilon: {args.epsilon}")
    print(f"Passed: {passed_count} / {len(rows)}")
    print()
    print("Saved:")
    print(f"- {csv_path}")
    print(f"- {json_path}")
    print(f"- {html_path}")
    print()
    print("Structural meaning:")
    print("phase difference(X, R_theta) = 180 degrees")
    print("180-degree phase difference -> r != 0")
    print("L_lower = r^2 > 0")
    print()
    print("Important:")
    print("This is an internal structural verification.")
    print("It is not a direct standard zeta-zero proof.")


if __name__ == "__main__":
    main()