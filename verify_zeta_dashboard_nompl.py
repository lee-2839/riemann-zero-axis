# verify_zeta_dashboard_nompl.py
# No matplotlib version.
# Outputs CSV, JSON, and an HTML dashboard with inline SVG graphs.

import argparse
import csv
import json
import hashlib
import html
import math
import platform
import sys
from pathlib import Path
from datetime import datetime, timezone

import mpmath as mp


def mp_str(x, digits=80):
    return mp.nstr(x, n=digits)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(8192), b""):
            h.update(block)
    return h.hexdigest()


def compute_zeta_zeros(count: int, dps: int, tol_text: str):
    mp.mp.dps = dps
    tol = mp.mpf(tol_text)

    rows = []

    for n in range(1, count + 1):
        rho = mp.zetazero(n)
        zeta_value = mp.zeta(rho)

        real_part = mp.re(rho)
        imag_part = mp.im(rho)

        real_error = abs(real_part - mp.mpf("0.5"))
        zeta_error = abs(zeta_value)

        passed = real_error < tol and zeta_error < tol

        rows.append(
            {
                "n": n,
                "rho": mp_str(rho),
                "real_part": mp_str(real_part),
                "imag_part": mp_str(imag_part),
                "zeta_real": mp_str(mp.re(zeta_value)),
                "zeta_imag": mp_str(mp.im(zeta_value)),
                "real_error": mp_str(real_error),
                "zeta_error": mp_str(zeta_error),
                "tolerance": tol_text,
                "pass": passed,
                "_n_float": float(n),
                "_imag_float": float(imag_part),
                "_real_error_float": float(real_error),
                "_zeta_error_float": float(zeta_error),
            }
        )

    return rows


def save_csv(rows, path: Path):
    fieldnames = [
        "n",
        "rho",
        "real_part",
        "imag_part",
        "zeta_real",
        "zeta_imag",
        "real_error",
        "zeta_error",
        "tolerance",
        "pass",
    ]

    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            writer.writerow({key: row[key] for key in fieldnames})


def save_json(rows, path: Path, dps: int, tol_text: str):
    clean_rows = []

    for row in rows:
        clean_rows.append(
            {
                "n": row["n"],
                "rho": row["rho"],
                "real_part": row["real_part"],
                "imag_part": row["imag_part"],
                "zeta_real": row["zeta_real"],
                "zeta_imag": row["zeta_imag"],
                "real_error": row["real_error"],
                "zeta_error": row["zeta_error"],
                "tolerance": row["tolerance"],
                "pass": row["pass"],
            }
        )

    payload = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "mpmath_dps": dps,
        "tolerance": tol_text,
        "note": "This is a numerical verification of known zeta zeros, not a complete proof of the Riemann Hypothesis.",
        "results": clean_rows,
    }

    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def safe_log10(x: float):
    if x <= 0:
        return None
    return math.log10(x)


def make_svg_line_plot(title, x_values, y_values, x_label, y_label, log_y=False):
    width = 900
    height = 420
    margin_left = 80
    margin_right = 30
    margin_top = 50
    margin_bottom = 70

    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom

    clean_points = []

    for x, y in zip(x_values, y_values):
        if log_y:
            y2 = safe_log10(y)
            if y2 is None:
                continue
            clean_points.append((x, y2))
        else:
            clean_points.append((x, y))

    if not clean_points:
        clean_points = [(0, 0), (1, 0)]

    xs = [p[0] for p in clean_points]
    ys = [p[1] for p in clean_points]

    x_min = min(xs)
    x_max = max(xs)
    y_min = min(ys)
    y_max = max(ys)

    if x_min == x_max:
        x_min -= 1
        x_max += 1

    if y_min == y_max:
        y_min -= 1
        y_max += 1

    def sx(x):
        return margin_left + (x - x_min) / (x_max - x_min) * plot_w

    def sy(y):
        return margin_top + plot_h - (y - y_min) / (y_max - y_min) * plot_h

    polyline_points = " ".join(f"{sx(x):.2f},{sy(y):.2f}" for x, y in clean_points)

    circles = "\n".join(
        f'<circle cx="{sx(x):.2f}" cy="{sy(y):.2f}" r="3"></circle>'
        for x, y in clean_points
    )

    y_axis_name = f"log10({y_label})" if log_y else y_label

    svg = f"""
<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{html.escape(title)}">
  <style>
    .axis {{ stroke: #222; stroke-width: 1.5; }}
    .grid {{ stroke: #ddd; stroke-width: 1; }}
    .line {{ fill: none; stroke: #1f4e79; stroke-width: 2; }}
    .point {{ fill: #1f4e79; }}
    .label {{ font-family: Arial, sans-serif; font-size: 13px; fill: #222; }}
    .title {{ font-family: Arial, sans-serif; font-size: 18px; font-weight: bold; fill: #222; }}
    .tick {{ font-family: Arial, sans-serif; font-size: 12px; fill: #444; }}
  </style>

  <text class="title" x="{width / 2}" y="25" text-anchor="middle">{html.escape(title)}</text>

  <line class="axis" x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{margin_top + plot_h}" />
  <line class="axis" x1="{margin_left}" y1="{margin_top + plot_h}" x2="{margin_left + plot_w}" y2="{margin_top + plot_h}" />

  <line class="grid" x1="{margin_left}" y1="{margin_top}" x2="{margin_left + plot_w}" y2="{margin_top}" />
  <line class="grid" x1="{margin_left}" y1="{margin_top + plot_h / 2}" x2="{margin_left + plot_w}" y2="{margin_top + plot_h / 2}" />
  <line class="grid" x1="{margin_left}" y1="{margin_top + plot_h}" x2="{margin_left + plot_w}" y2="{margin_top + plot_h}" />

  <text class="tick" x="{margin_left - 10}" y="{margin_top + 4}" text-anchor="end">{y_max:.3g}</text>
  <text class="tick" x="{margin_left - 10}" y="{margin_top + plot_h / 2 + 4}" text-anchor="end">{((y_min + y_max) / 2):.3g}</text>
  <text class="tick" x="{margin_left - 10}" y="{margin_top + plot_h + 4}" text-anchor="end">{y_min:.3g}</text>

  <text class="tick" x="{margin_left}" y="{margin_top + plot_h + 25}" text-anchor="middle">{x_min:.0f}</text>
  <text class="tick" x="{margin_left + plot_w}" y="{margin_top + plot_h + 25}" text-anchor="middle">{x_max:.0f}</text>

  <text class="label" x="{width / 2}" y="{height - 20}" text-anchor="middle">{html.escape(x_label)}</text>
  <text class="label" x="20" y="{height / 2}" text-anchor="middle" transform="rotate(-90 20 {height / 2})">{html.escape(y_axis_name)}</text>

  <polyline class="line" points="{polyline_points}" />
  <g class="point">
    {circles}
  </g>
</svg>
"""
    return svg


def save_dashboard(rows, out_dir: Path, csv_path: Path, json_path: Path, dps: int, tol_text: str):
    passed_count = sum(1 for row in rows if row["pass"])
    total_count = len(rows)

    csv_hash = sha256_file(csv_path)
    json_hash = sha256_file(json_path)

    first = rows[0]
    last = rows[-1]

    n_values = [row["_n_float"] for row in rows]
    imag_values = [row["_imag_float"] for row in rows]
    real_errors = [row["_real_error_float"] for row in rows]
    zeta_errors = [row["_zeta_error_float"] for row in rows]

    svg_imag = make_svg_line_plot(
        title="Imaginary Parts of Computed Zeta Zeros",
        x_values=n_values,
        y_values=imag_values,
        x_label="Zero index n",
        y_label="Im(rho)",
        log_y=False,
    )

    svg_real_error = make_svg_line_plot(
        title="Real-Part Error from the Critical Line",
        x_values=n_values,
        y_values=real_errors,
        x_label="Zero index n",
        y_label="|Re(rho) - 1/2|",
        log_y=False,
    )

    svg_zeta_error = make_svg_line_plot(
        title="Zeta Value Error at Computed Zeros",
        x_values=n_values,
        y_values=zeta_errors,
        x_label="Zero index n",
        y_label="|zeta(rho)|",
        log_y=True,
    )

    dashboard_path = out_dir / "dashboard.html"

    html_rows = ""

    for row in rows:
        html_rows += f"""
        <tr>
          <td>{row["n"]}</td>
          <td>{html.escape(row["real_part"])}</td>
          <td>{html.escape(row["imag_part"])}</td>
          <td>{html.escape(row["real_error"])}</td>
          <td>{html.escape(row["zeta_error"])}</td>
          <td>{row["pass"]}</td>
        </tr>
"""

    html_text = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Riemann Zero-Axis Numerical Dashboard</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 40px;
      line-height: 1.6;
      color: #222;
    }}
    h1, h2 {{
      border-bottom: 1px solid #ddd;
      padding-bottom: 6px;
    }}
    .box {{
      border: 1px solid #ddd;
      padding: 16px;
      margin: 16px 0;
      border-radius: 8px;
      background: #fafafa;
    }}
    code, pre {{
      background: #f3f3f3;
      padding: 2px 4px;
      border-radius: 4px;
    }}
    pre {{
      padding: 12px;
      overflow-x: auto;
      white-space: pre-wrap;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
      margin-top: 16px;
      font-size: 13px;
    }}
    th, td {{
      border: 1px solid #ddd;
      padding: 6px;
      text-align: left;
      vertical-align: top;
    }}
    th {{
      background: #f0f0f0;
    }}
    .pass {{
      font-weight: bold;
    }}
  </style>
</head>
<body>

<h1>Riemann Zero-Axis Numerical Dashboard</h1>

<div class="box">
  <h2>Purpose</h2>
  <p>
    This dashboard stores reproducible numerical checks for known non-trivial zeros of the Riemann zeta function.
  </p>
  <pre>zeta(rho) ≈ 0
Re(rho) ≈ 1/2</pre>
  <p>
    This dashboard does not claim that finite computation alone proves the full Riemann Hypothesis.
    It records numerical evidence and structural alignment data for the proposed zero-axis interpretation.
  </p>
</div>

<div class="box">
  <h2>Core Formulas</h2>
  <pre>ζ(ρ) = 0  →  Re(ρ) = 1/2

0_f ⊂ 1 → A0 → {{W, H}} → P → C → E → Z → ρ ⊂ A0

ρ ⊂ Z ⊂ A0

E = ∏P = ∏Crit = total orbital field

Z = H(A0)

central rotation ⇔ center = 0.5

phase difference(X, Rθ) = 180°
r ≠ 0
L_lower = r²
L_lower > 0</pre>
</div>

<div class="box">
  <h2>Run Summary</h2>
  <p><strong>Zeros checked:</strong> {total_count}</p>
  <p><strong>Passed:</strong> {passed_count} / {total_count}</p>
  <p><strong>mpmath precision:</strong> {dps} decimal digits</p>
  <p><strong>Tolerance:</strong> {html.escape(tol_text)}</p>
  <p><strong>First zero:</strong> {html.escape(first["rho"])}</p>
  <p><strong>Last zero:</strong> {html.escape(last["rho"])}</p>
</div>

<div class="box">
  <h2>Saved Data Files</h2>
  <p><strong>CSV:</strong> {html.escape(csv_path.name)}</p>
  <p><strong>CSV SHA256:</strong> <code>{csv_hash}</code></p>
  <p><strong>JSON:</strong> {html.escape(json_path.name)}</p>
  <p><strong>JSON SHA256:</strong> <code>{json_hash}</code></p>
</div>

<div class="box">
  <h2>Graph 1: Imaginary Parts</h2>
  {svg_imag}
</div>

<div class="box">
  <h2>Graph 2: Real-Part Error</h2>
  <p>
    In many computed cases, <code>mpmath.zetazero(n)</code> returns the zero directly on the critical line,
    so this graph may appear as a flat zero-error line.
  </p>
  {svg_real_error}
</div>

<div class="box">
  <h2>Graph 3: Zeta Error</h2>
  <p>
    This graph uses log10 scale for <code>|zeta(rho)|</code>.
  </p>
  {svg_zeta_error}
</div>

<div class="box">
  <h2>Result Table</h2>
  <table>
    <tr>
      <th>n</th>
      <th>Re(rho)</th>
      <th>Im(rho)</th>
      <th>|Re(rho)-1/2|</th>
      <th>|zeta(rho)|</th>
      <th>Pass</th>
    </tr>
    {html_rows}
  </table>
</div>

</body>
</html>
"""

    with dashboard_path.open("w", encoding="utf-8") as f:
        f.write(html_text)

    return dashboard_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10, help="Number of zeta zeros to check")
    parser.add_argument("--dps", type=int, default=50, help="mpmath decimal precision")
    parser.add_argument("--tol", type=str, default="1e-40", help="tolerance for pass/fail")
    parser.add_argument("--out", type=str, default="results", help="output directory")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = compute_zeta_zeros(args.count, args.dps, args.tol)

    csv_path = out_dir / "zeta_zeros.csv"
    json_path = out_dir / "zeta_zeros.json"

    save_csv(rows, csv_path)
    save_json(rows, json_path, args.dps, args.tol)

    dashboard_path = save_dashboard(
        rows=rows,
        out_dir=out_dir,
        csv_path=csv_path,
        json_path=json_path,
        dps=args.dps,
        tol_text=args.tol,
    )

    print("Saved:")
    print(f"- {csv_path}")
    print(f"- {json_path}")
    print(f"- {dashboard_path}")
    print()
    print(f"Passed: {sum(1 for row in rows if row['pass'])} / {len(rows)}")


if __name__ == "__main__":
    main()