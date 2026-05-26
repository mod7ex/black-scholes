import argparse
import time
import warnings
from datetime import datetime, date

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import yfinance as yf
from scipy.stats import norm

warnings.filterwarnings("ignore")

TICKER       = "QQQ"
REFRESH_SECS = 60
RATE         = 0.05          # risk-free rate (approx)
NUM_EXPIRIES = 4             # how many nearest expirations to aggregate


# ── Black-Scholes gamma ───────────────────────────────────────────────────────
def bs_gamma(S, K, T, r, sigma):
    """Return gamma for a European option (same for calls & puts)."""
    if T <= 0 or sigma <= 0:
        return 0.0
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return norm.pdf(d1) / (S * sigma * np.sqrt(T))


# ── fetch & compute ───────────────────────────────────────────────────────────
def compute_gex(expiry_filter: str | None, top_n: int | None) -> tuple[dict, float]:
    ticker = yf.Ticker(TICKER)
    spot   = ticker.fast_info["last_price"]

    all_exps = ticker.options                         # sorted nearest-first
    if expiry_filter:
        exps = [expiry_filter]
    else:
        exps = list(all_exps[:NUM_EXPIRIES])

    gex_by_strike: dict[float, float] = {}

    today = date.today()
    for exp in exps:
        try:
            chain = ticker.option_chain(exp)
        except Exception:
            continue

        exp_date = date.fromisoformat(exp)
        T = max((exp_date - today).days / 365.0, 1 / 365)

        for df, sign in [(chain.calls, +1), (chain.puts, -1)]:
            df = df.dropna(subset=["strike", "openInterest", "impliedVolatility"])
            df = df[df["openInterest"] > 0]
            df = df[df["impliedVolatility"] > 0]

            for _, row in df.iterrows():
                K    = float(row["strike"])
                oi   = float(row["openInterest"])
                iv   = float(row["impliedVolatility"])
                g    = bs_gamma(spot, K, T, RATE, iv)
                # GEX = gamma × OI × 100 shares × spot² × 0.01 (per 1% move)
                gex  = sign * g * oi * 100 * spot ** 2 * 0.01
                gex_by_strike[K] = gex_by_strike.get(K, 0.0) + gex

    # ── derived levels ────────────────────────────────────────────────────────
    if not gex_by_strike:
        return {}, spot

    sorted_strikes = sorted(gex_by_strike)
    values         = [gex_by_strike[k] for k in sorted_strikes]

    # gamma flip: strike where cumulative GEX crosses zero
    cumulative = np.cumsum(values)
    gamma_flip = None
    for i in range(1, len(cumulative)):
        if cumulative[i - 1] * cumulative[i] <= 0:
            gamma_flip = sorted_strikes[i]
            break

    # call wall: largest positive GEX strike
    pos = {k: v for k, v in gex_by_strike.items() if v > 0}
    call_wall = max(pos, key=pos.get) if pos else None

    # put wall: largest negative GEX strike (most negative)
    neg = {k: v for k, v in gex_by_strike.items() if v < 0}
    put_wall = min(neg, key=neg.get) if neg else None

    net_gex = sum(values)

    # optional: keep only top N strikes by |GEX|
    if top_n:
        top_keys = sorted(gex_by_strike, key=lambda k: abs(gex_by_strike[k]), reverse=True)[:top_n]
        gex_by_strike = {k: gex_by_strike[k] for k in sorted(top_keys)}

    return {
        "gex_by_strike": gex_by_strike,
        "net_gex":       net_gex,
        "gamma_flip":    gamma_flip,
        "call_wall":     call_wall,
        "put_wall":      put_wall,
        "exps_used":     exps,
    }, spot


# ── formatting ────────────────────────────────────────────────────────────────
def fmt(n):
    if n is None:
        return "—"
    prefix = "+" if n > 0 else ""
    a = abs(n)
    if a >= 1e9: return f"{prefix}{n/1e9:.2f}B"
    if a >= 1e6: return f"{prefix}{n/1e6:.1f}M"
    if a >= 1e3: return f"{prefix}{n/1e3:.1f}K"
    return f"{n:.0f}"


# ── draw ──────────────────────────────────────────────────────────────────────
def draw(ax, result: dict, spot: float, expiry_filter: str | None):
    ax.clear()

    if not result or not result.get("gex_by_strike"):
        ax.text(0.5, 0.5, "No data returned.", ha="center", va="center",
                transform=ax.transAxes, fontsize=12, color="#888")
        return

    gbs     = result["gex_by_strike"]
    strikes = sorted(gbs)
    values  = [gbs[k] for k in strikes]
    colors  = ["#1D9E75" if v >= 0 else "#E24B4A" for v in values]
    x       = np.arange(len(strikes))

    ax.bar(x, values, color=colors, width=0.7, zorder=3)
    ax.axhline(0, color="#aaa", linewidth=0.8, zorder=2)

    # ── key level lines ───────────────────────────────────────────────────────
    def price_to_x(price):
        for i, s in enumerate(strikes):
            if s >= price:
                if i == 0: return 0
                lo, hi = strikes[i-1], strikes[i]
                return i - 1 + (price - lo) / (hi - lo + 1e-9)
        return len(strikes) - 1

    y_max = max(abs(v) for v in values) if values else 1
    levels = [
        (result.get("gamma_flip"), "#F0992B", "Gamma flip"),
        (result.get("call_wall"),  "#1D9E75", "Call wall"),
        (result.get("put_wall"),   "#E24B4A", "Put wall"),
        (spot,                     "#7F77DD", "Spot"),
    ]
    for price, color, label in levels:
        if price is None: continue
        if not (strikes[0] <= price <= strikes[-1]): continue
        xpos = price_to_x(price)
        ax.axvline(xpos, color=color, linewidth=1.4, linestyle="--", zorder=4, alpha=0.9)
        ax.text(xpos + 0.15, y_max * 0.91, f"{label}\n${price:.0f}",
                color=color, fontsize=8.5, va="top", zorder=5)

    # ── axes ──────────────────────────────────────────────────────────────────
    ax.set_xticks(x)
    ax.set_xticklabels([f"{s:.0f}" for s in strikes], rotation=45, ha="right", fontsize=8)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: fmt(v)))
    ax.set_ylabel("GEX ($)", fontsize=10)
    ax.set_xlabel("Strike", fontsize=10)
    ax.grid(axis="y", color="#e0e0e0", linewidth=0.6, zorder=0)
    ax.set_facecolor("#fafafa")

    exps_str    = ", ".join(result.get("exps_used", []))
    net_str     = fmt(result.get("net_gex"))
    regime      = "▲ positive gamma" if (result.get("net_gex") or 0) >= 0 else "▼ negative gamma"
    ts          = datetime.now().strftime("%H:%M:%S")
    ax.set_title(
        f"{TICKER} GEX by Strike   ·   net {net_str}   ·   {regime}\n"
        f"expirations: {exps_str}   [{ts}]",
        fontsize=11, fontweight="normal", pad=10
    )


# ── main loop ─────────────────────────────────────────────────────────────────
def pick_backend():
    for name in ("Qt5Agg", "Qt6Agg", "GTK4Agg", "GTK3Agg", "WXAgg", "MacOSX"):
        try:
            matplotlib.use(name)
            import matplotlib.pyplot as _p  # noqa: F401
            return name
        except Exception:
            continue
    matplotlib.use("Agg")
    return "Agg"


def run(expiry_filter: str | None, top_n: int | None):
    backend = pick_backend()
    if backend == "Agg":
        print("No GUI backend found — saving chart to gex_chart.png on each refresh.")
    plt.ion()
    fig, ax = plt.subplots(figsize=(15, 6))
    fig.patch.set_facecolor("#ffffff")
    if backend != "Agg":
        fig.canvas.manager.set_window_title(f"{TICKER} GEX — live (yfinance)")

    def refresh():
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] Fetching QQQ options chain…", end=" ", flush=True)
        try:
            result, spot = compute_gex(expiry_filter, top_n)
            draw(ax, result, spot, expiry_filter)
            fig.tight_layout(pad=2)
            if backend == "Agg":
                fig.savefig("gex_chart.png", dpi=150)
                print(f"OK  → saved gex_chart.png")
            else:
                fig.canvas.draw()
                fig.canvas.flush_events()
                net = fmt(result.get("net_gex")) if result else "—"
                print(f"OK  net GEX={net}  spot=${spot:.2f}")
        except Exception as e:
            print(f"Error: {e}")

    refresh()
    last = time.time()

    if backend == "Agg":
        print(f"Refreshing every {REFRESH_SECS}s. Press Ctrl+C to stop.")
        while True:
            time.sleep(REFRESH_SECS)
            refresh()
    else:
        while plt.fignum_exists(fig.number):
            plt.pause(0.5)
            if time.time() - last >= REFRESH_SECS:
                refresh()
                last = time.time()
        print("Window closed — exiting.")


def main():
    parser = argparse.ArgumentParser(description="QQQ GEX chart — free, no API key")
    parser.add_argument("--expiry", default=None, help="Single expiry YYYY-MM-DD (default: 4 nearest)")
    parser.add_argument("--top",    default=None, type=int, help="Show only top N strikes by |GEX|")
    args = parser.parse_args()
    run(args.expiry, args.top)


if __name__ == "__main__":
    main()