# verify_independent_zeta_scan.py
# Independent critical-line scan for non-trivial zeta zeros.
#
# This script does NOT use mpmath.zetazero(n).
# It scans the critical line s = 1/2 + i t using Hardy Z(t),
# detects sign changes, refines roots by bisection,
# then stores CSV, JSON, and an HTML dashboard.
#
# Requirement:
#   python -m pip install mpmath
#
# Example:
#   python verify_independent_zeta_scan.py --target-count 100 --t-max 250 --step 0.05 --dps 80

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


def mp_str(x, digits=90):
    return mp.nstr(x, n=digits)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(8192), b""):
            h.update(block)
    return h.hexdigest()


def riemann_siegel_theta(t):
    """
    Riemann-Siegel theta function.

    theta(t) = Im(log Gamma(1/4 + i t/2)) - (t/2) log(pi)

    Used as fallback if mpmath.siegelz is unavailable.
    """
    t = mp.mpf(t)
    return mp.im(mp.loggamma(mp.mpf("0.25") + mp.j * t / 2)) - (t / 2) * mp.log(mp.pi)


def hardy_z(t):
    """
    Hardy Z function on the critical line.

    Z(t) is real-valued for real t, and its zeros correspond to
    zeta(1/2 + i t) = 0.

    This function avoids mpmath.zetazero(n).
    """
    t = mp.mpf(t)

    if hasattr(mp, "siegelz"):
        return mp.re(mp.siegelz(t))

    theta = riemann_siegel_theta(t)
    s = mp.mpf("0.5") + mp.j * t
    return mp.re(mp.e ** (mp.j * theta) * mp.zeta(s))


def refine_root_by_bisection(a, b, tol_t, max_iter=300):
    """
    Refine a sign-change interval [a, b] for Hardy Z(t) by bisection.
    """
    a = mp.mpf(a)
    b = mp.mpf(b)
    fa = hardy_z(a)
    fb = hardy_z(b)

    if fa == 0:
        return a
    if fb == 0:
        return b

    if fa * fb > 0:
        raise ValueError("Bisection requires a sign-change interval.")

    for _ in range(max_iter):
        m = (a + b) / 2
        fm = hardy_z(m)

        if abs(b - a) < tol_t:
            return m

        if fm == 0:
            return m

        if fa * fm < 0:
            b = m
            fb = fm
        else:
            a = m
            fa = fm

    return (a + b) / 2


def scan_critical_line(t_min, t_max, step, target_count, tol_t):
    """
    Scan Hardy Z(t) on [t_min, t_max] and find sign-change roots.
    """
    roots = []

    t_prev = mp.mpf(t_min)
    z_prev = hardy_z(t_prev)

    steps = int(mp.ceil((mp.mpf(t_max) - mp.mpf(t_min)) / mp.mpf(step)))

    for i in range(1, steps + 1):
        t_curr = mp.mpf(t_min) + i * mp.mpf(step)
        if t_curr > t_max:
            t_curr = mp.mpf(t_max)

        z_curr = hardy_z(t_curr)

        has_sign_change = z_prev * z_curr < 0
        exact_hit = z_curr == 0

        if has_sign_change or exact_hit:
            if exact_hit:
                root_t = t_curr
            else:
                root_t = refine_root_by_bisection(t_prev, t_curr, tol_t)

            if not roots or abs(root_t - roots[-1]) > mp.mpf(step) / 10:
                roots.append(root_t)

            if len(roots) >= target_count:
                break

        t_prev = t_curr
        z_prev = z_curr

    return roots


def compute_rows(roots, dps, tolerance_text):
    mp.mp.dps = dps
    tolerance = mp.mpf(tolerance_text)

    rows = []

    for index, t in enumerate(roots, start=1):
        s = mp.mpf("0.5") + mp.j * t
        zeta_value = mp.zeta(s)
        zeta_error = abs(zeta_value)
        z_value = hardy_z(t)
        real_error = abs(mp.re(s) - mp.mpf("0.5"))

        passed = zeta_error < tolerance and real_error < tolerance

        rows.append(
            {
                "n": index,
                "t": mp_str(t),
                "rho": mp_str(s),
                "real_part": mp_str(mp.re(s)),
                "imag_part": mp_str(mp.im(s)),
                "hardy_z": mp_str(z_value),
                "zeta_real": mp_str(mp.re(zeta_value)),
                "zeta_imag": mp_str(mp.im(zeta_value)),
                "zeta_error": mp_str(zeta_error),
                "real_error": mp_str(real_error),
                "tolerance": tolerance_text,
                "pass": passed,
                "_n_float": float(index),
                "_t_float": float(t),
                "_zeta_error_float": float(zeta_error),
            }
        )

    return rows


def save_csv(rows, path: Path):
    fieldnames = [
        "n",
        "t",
        "rho",
        "real_part",
        "imag_part",
        "hardy_z",
        "zeta_real",
        "zeta_imag",
        "zeta_error",
        "real_error",
        "tolerance",
        "pass",
    ]

    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            writer.writerow({key: row[key] for key in fieldnames})


def save_json(rows, path: Path, args):
    clean_rows = []

    for row in rows:
        clean_rows.append(
            {
                "n": row["n"],
                "t": row["t"],
                "rho": row["rho"],
                "real_part": row["real_part"],
                "imag_part": row["imag_part"],
                "hardy_z": row["hardy_z"],
                "zeta_real": row["zeta_real"],
                "zeta_imag": row["zeta_imag"],
                "zeta_error": row["zeta_error"],
                "real_error": row["real_error"],
                "tolerance": row["tolerance"],
                "pass": row["pass"],
            }
        )

    payload = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "mpmath_dps": args.dps,
        "target_count": args.target_count,
        "t_min": args.t_min,
        "t_max": args.t_max,
        "step": args.step,
        "tol_t": args.tol_t,
        "tol_zeta": args.tol_zeta,
        "method": "Critical-line scan using Hardy Z(t), sign changes, and bisection. Does not use mpmath.zetazero(n).",
        "note": "This is an independent numerical scan on the critical line, not a complete proof of the Riemann Hypothesis.",
        "results": clean_rows,
    }

    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def safe_log10(x):
    if x <= 0:
        return None
    return math.log10(x)


def make_svg_line_plot(title, x_values, y_values, x_label, y_label, log_y=False):
    width = 900
    height = 420
    margin_left = 85
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

    points = " ".join(f"{sx(x):.2f},{sy(y):.2f}" for x, y in clean_points)

    circles = "\n".join(
        f'<circle cx="{sx(x):.2f}" cy="{sy(y):.2f}" r="3"></circle>'
        for x, y in clean_points
    )

    y_axis_name = f"log10({y_label})" if log_y else y_label

    return f"""
<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" xmlns="http://www.w3.org/2000/svg">
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
  <text class="label" x="22" y="{height / 2}" text-anchor="middle" transform="rotate(-90 22 {height / 2})">{html.escape(y_axis_name)}</text>

  <polyline class="line" points="{points}" />
  <g class="point">
    {circles}
  </g>
</svg>
"""


def save_dashboard(rows, out_dir: Path, csv_path: Path, json_path: Path, args):
    dashboard_path = out_dir / "independent_scan_dashboard.html"

    passed_count = sum(1 for row in rows if row["pass"])
    total_count = len(rows)

    csv_hash = sha256_file(csv_path)
    json_hash = sha256_file(json_path)

    first = rows[0] if rows else None
    last = rows[-1] if rows else None

    n_values = [row["_n_float"] for row in rows]
    t_values = [row["_t_float"] for row in rows]
    zeta_errors = [row["_zeta_error_float"] for row in rows]

    svg_t = make_svg_line_plot(
        title="Independently Scanned Critical-Line Zeros",
        x_values=n_values,
        y_values=t_values,
        x_label="Detected zero index",
        y_label="t in rho = 1/2 + i t",
        log_y=False,
    )

    svg_error = make_svg_line_plot(
        title="Zeta Error at Independently Scanned Zeros",
        x_values=n_values,
        y_values=zeta_errors,
        x_label="Detected zero index",
        y_label="|zeta(1/2 + i t)|",
        log_y=True,
    )

    table_rows = ""

    for row in rows:
        table_rows += f"""
        <tr>
          <td>{row["n"]}</td>
          <td>{html.escape(row["t"])}</td>
          <td>{html.escape(row["real_part"])}</td>
          <td>{html.escape(row["zeta_error"])}</td>
          <td>{html.escape(row["hardy_z"])}</td>
          <td>{row["pass"]}</td>
        </tr>
"""

    first_text = html.escape(first["rho"]) if first else "None"
    last_text = html.escape(last["rho"]) if last else "None"

    html_text = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Independent Zeta Scan Dashboard</title>
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
    pre, code {{
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
  </style>
</head>
<body>

<h1>Independent Zeta Critical-Line Scan Dashboard</h1>

<div class="box">
  <h2>Purpose</h2>
  <p>
    This dashboard records an independent numerical scan on the critical line.
    It does not use <code>mpmath.zetazero(n)</code>.
  </p>
  <pre>s = 1/2 + i t
Hardy Z(t) sign changes are scanned.
Each sign-change interval is refined by bisection.
Then zeta(1/2 + i t) is evaluated.</pre>
  <p>
    This is numerical evidence only. It does not prove the full Riemann Hypothesis.
  </p>
</div>

<div class="box">
  <h2>Core Formulas</h2>
  <pre>ζ(ρ) = 0  →  Re(ρ) = 1/2

ρ = 1/2 + i t

Z_Hardy(t) = real-valued critical-line function

Z_Hardy(t) = 0  ⇔  ζ(1/2 + i t) = 0

0_f ⊂ 1 → A0 → {{W, H}} → P → C → E → Z → ρ ⊂ A0

ρ ⊂ Z ⊂ A0</pre>
</div>

<div class="box">
  <h2>Run Summary</h2>
  <p><strong>Target count:</strong> {args.target_count}</p>
  <p><strong>Detected count:</strong> {total_count}</p>
  <p><strong>Passed:</strong> {passed_count} / {total_count}</p>
  <p><strong>t range:</strong> {args.t_min} to {args.t_max}</p>
  <p><strong>scan step:</strong> {args.step}</p>
  <p><strong>mpmath precision:</strong> {args.dps} decimal digits</p>
  <p><strong>zeta tolerance:</strong> {html.escape(args.tol_zeta)}</p>
  <p><strong>t bisection tolerance:</strong> {html.escape(args.tol_t)}</p>
  <p><strong>First detected zero:</strong> {first_text}</p>
  <p><strong>Last detected zero:</strong> {last_text}</p>
</div>

<div class="box">
  <h2>Saved Data Files</h2>
  <p><strong>CSV:</strong> {html.escape(csv_path.name)}</p>
  <p><strong>CSV SHA256:</strong> <code>{csv_hash}</code></p>
  <p><strong>JSON:</strong> {html.escape(json_path.name)}</p>
  <p><strong>JSON SHA256:</strong> <code>{json_hash}</code></p>
</div>

<div class="box">
  <h2>Graph 1: Detected Critical-Line Zeros</h2>
  {svg_t}
</div>

<div class="box">
  <h2>Graph 2: Zeta Error</h2>
  <p>This graph uses log10 scale for <code>|zeta(1/2 + i t)|</code>.</p>
  {svg_error}
</div>

<div class="box">
  <h2>Result Table</h2>
  <table>
    <tr>
      <th>n</th>
      <th>t</th>
      <th>Re(rho)</th>
      <th>|zeta(rho)|</th>
      <th>Hardy Z(t)</th>
      <th>Pass</th>
    </tr>
    {table_rows}
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

    parser.add_argument("--target-count", type=int, default=100)
    parser.add_argument("--t-min", type=str, default="0")
    parser.add_argument("--t-max", type=str, default="250")
    parser.add_argument("--step", type=str, default="0.05")
    parser.add_argument("--dps", type=int, default=80)
    parser.add_argument("--tol-t", type=str, default="1e-60")
    parser.add_argument("--tol-zeta", type=str, default="1e-50")
    parser.add_argument("--out", type=str, default="results_independent")

    args = parser.parse_args()

    mp.mp.dps = args.dps

    t_min = mp.mpf(args.t_min)
    t_max = mp.mpf(args.t_max)
    step = mp.mpf(args.step)
    tol_t = mp.mpf(args.tol_t)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Independent critical-line scan")
    print("This script does not use mpmath.zetazero(n).")
    print(f"Scanning t from {args.t_min} to {args.t_max} with step {args.step}")
    print(f"Target count: {args.target_count}")
    print()

    roots = scan_critical_line(
        t_min=t_min,
        t_max=t_max,
        step=step,
        target_count=args.target_count,
        tol_t=tol_t,
    )

    if len(roots) < args.target_count:
        print(f"Warning: only {len(roots)} roots detected.")
        print("Try increasing --t-max or decreasing --step.")

    rows = compute_rows(
        roots=roots,
        dps=args.dps,
        tolerance_text=args.tol_zeta,
    )

    csv_path = out_dir / "independent_zeta_scan.csv"
    json_path = out_dir / "independent_zeta_scan.json"

    save_csv(rows, csv_path)
    save_json(rows, json_path, args)

    dashboard_path = save_dashboard(
        rows=rows,
        out_dir=out_dir,
        csv_path=csv_path,
        json_path=json_path,
        args=args,
    )

    print()
    print("Saved:")
    print(f"- {csv_path}")
    print(f"- {json_path}")
    print(f"- {dashboard_path}")
    print()
    print(f"Detected: {len(rows)}")
    print(f"Passed: {sum(1 for row in rows if row['pass'])} / {len(rows)}")

    if rows:
        print()
        print("First detected zero:")
        print(rows[0]["rho"])
        print()
        print("Last detected zero:")
        print(rows[-1]["rho"])


if __name__ == "__main__":
    main()