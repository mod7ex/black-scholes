import numpy as np
from scipy.stats import norm
import pandas as pd

def bs_gamma(S, K, T, r, sigma):
    """Gamma is identical for calls and puts."""
    if T <= 0 or sigma <= 0: return 0.0
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.pdf(d1) / (S * sigma * np.sqrt(T))


def compute_gex_df(df, spot, T, sign, _Rate=0.05):
    rows = []
    for _, row in df.iterrows():
        K  = float(row["strike"])
        oi = float(row["openInterest"])
        iv = float(row["impliedVolatility"])
        if oi <= 0 or iv <= 0: continue # skip zero OI or IV rows
        g = bs_gamma(spot, K, T, _Rate, iv)
        # gex = sign * g * oi * 100 * spot**2 * 0.01
        gex = sign * g * oi * 100
        rows.append({"strike": K, "oi": oi, "iv": iv, "gamma": g, "gex": gex})
    return pd.DataFrame(rows)

def fmt(n):
    a = abs(n)
    p = "+" if n > 0 else ""
    if a >= 1e9: return f"{p}{n/1e9:.2f}B"
    if a >= 1e6: return f"{p}{n/1e6:.1f}M"
    if a >= 1e3: return f"{p}{n/1e3:.1f}K"
    return f"{p}{n:.0f}"