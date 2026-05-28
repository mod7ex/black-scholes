# Black–Scholes Model

## Call Option Price

$$
C = S_0 N(d_1) - K e^{-rT} N(d_2)
$$

## Put Option Price

$$
P = K e^{-rT} N(d_2) - S_0 N(d_1)
$$

---

# Core Quantities

$$
d_1 = \frac{\ln(S_0/K) + \left(r + \frac{1}{2}\sigma^2\right)T}{\sigma\sqrt{T}}
$$

$$
d_2 = d_1 - \sigma\sqrt{T}
$$

---

## Definitions (Inputs)

* $S_0$ current underlying asset price
* $K$ strike price
* $T$ time to maturity (in years)
* $r$ continuously compounded risk-free interest rate
* $\sigma$ volatility of returns (annualized standard deviation)
* $N(x)$ cumulative distribution function of standard normal distribution
* $\phi(x)$ probability density function of standard normal distribution
* $\ln(\cdot)$ natural logarithm

---

# First-Order Greeks

---

## Delta ($\Delta$)

### Definition

Sensitivity of option price to small changes in underlying price.

$$
\Delta = \frac{\partial V}{\partial S}
$$

Call:
$$
\Delta_c = N(d_1)
$$

Put:
$$
\Delta_p = N(d_1) - 1
$$

### Interpretation

* Measures directional exposure (“shares equivalent”)
* Positive for calls, negative for puts

---

## Gamma ($\Gamma$)

### Definition

Rate of change of Delta with respect to underlying price.

$$
\Gamma = \frac{\partial^2 V}{\partial S^2}
$$

$$
\Gamma = \frac{\phi(d_1)}{S_0 \sigma \sqrt{T}}
$$

### Interpretation

* Measures convexity of option price
* Same for calls and puts

---

## Vega ($nu$)

### Definition

Sensitivity of option price to volatility.

$$
\nu = \frac{\partial V}{\partial \sigma}
$$

$$
\nu = S_0 \phi(d_1)\sqrt{T}
$$

### Interpretation

* Higher when option is ATM
* Measures exposure to implied volatility changes

---

## Theta ($\Theta$)

### Definition

Sensitivity of option price to time decay.

$$
\Theta = \frac{\partial V}{\partial T}
$$

Call:
$$
\Theta_c =
-\frac{S_0 \phi(d_1)\sigma}{2\sqrt{T}}

* rK e^{-rT} N(d_2)
  $$

Put:
$$
\Theta_p =
-\frac{S_0 \phi(d_1)\sigma}{2\sqrt{T}}

* rK e^{-rT} N(-d_2)
  $$

### Interpretation

* Measures daily time decay (“theta burn”)
* Usually negative for long options

---

## Rho ($\rho$)

### Definition

Sensitivity to interest rates.

$$
\rho = \frac{\partial V}{\partial r}
$$

Call:
$$
\rho_c = K T e^{-rT} N(d_2)
$$

Put:
$$
\rho_p = -K T e^{-rT} N(-d_2)
$$

### Interpretation

* Important for long-dated options
* Measures discount-rate sensitivity

---

# Second-Order Greeks

---

## Vomma (Volga)

### Definition

Sensitivity of Vega to volatility.

$$
\text{Vomma} = \frac{\partial^2 V}{\partial \sigma^2}
$$

$$
\text{Vomma} = \nu \frac{d_1 d_2}{\sigma}
$$

### Interpretation

* Measures convexity in volatility exposure

---

## Vanna

### Definition

Sensitivity of Delta to volatility (or Vega to spot).

$$
\text{Vanna} = \frac{\partial^2 V}{\partial S \partial \sigma}
$$

$$
\text{Vanna} = -\phi(d_1)\frac{d_2}{\sigma}
$$

### Interpretation

* Important for FX and volatility hedging
* Captures joint spot-vol effects

---

## Charm

### Definition

Rate of change of Delta over time.

$$
\text{Charm} = \frac{\partial^2 V}{\partial S \partial T}
$$

Call:
$$
\text{Charm}_c =
-\phi(d_1)\frac{2rT - d_2 \sigma \sqrt{T}}{2T\sigma\sqrt{T}}
$$

### Interpretation

* Measures Delta decay as time passes

---

## Veta

### Definition

Sensitivity of Vega to time.

$$
\text{Veta} = \frac{\partial^2 V}{\partial \sigma \partial T}
$$

$$
\text{Veta} =

* S_0 \phi(d_1)\sqrt{T}
  \left(
  r\frac{d_1}{\sigma\sqrt{T}}
  -\frac{1 + d_1 d_2}{2T}
  \right)
  $$

### Interpretation

* Measures how volatility exposure decays over time

---

## Vera

### Definition

Sensitivity of Rho to volatility.

$$
\text{Vera} = \frac{\partial^2 V}{\partial r \partial \sigma}
$$

$$
\text{Vera} = K T e^{-rT}\phi(d_2)\frac{\sqrt{T}}{\sigma}
$$

### Interpretation

* Rarely used, but relevant in interest-rate sensitive options

---

# Third-Order Greeks

---

## Speed

### Definition

Rate of change of Gamma with respect to spot.

$$
\text{Speed} = \frac{\partial^3 V}{\partial S^3}
$$

$$
\text{Speed} =
-\frac{\Gamma}{S_0}
\left(
\frac{d_1}{\sigma\sqrt{T}} + 1
\right)
$$

### Interpretation

* Measures curvature acceleration

---

## Zomma

### Definition

Sensitivity of Gamma to volatility.

$$
\text{Zomma} = \frac{\partial \Gamma}{\partial \sigma}
$$

$$
\text{Zomma} = \Gamma \frac{d_1 d_2 - 1}{\sigma}
$$

### Interpretation

* Important for volatility-of-volatility effects

---

## Color

### Definition

Rate of change of Gamma over time.

$$
\text{Color} = \frac{\partial \Gamma}{\partial T}
$$

### Interpretation

* Captures how convexity evolves as time passes

---

## Ultima

### Definition

Sensitivity of Vomma to volatility.

$$
\text{Ultima} = \frac{\partial \text{Vomma}}{\partial \sigma}
$$

$$
\text{Ultima} =
-\frac{\nu}{\sigma^2}
\left[
d_1 d_2(1 - d_1 d_2) + d_1^2 + d_2^2
\right]
$$

### Interpretation

* Extremely high-order sensitivity (rare in practice)

---

# General Definition of a Greek

A Greek is any partial derivative of option value:

$$
V = V(S, \sigma, r, T)
$$

$$
\text{Greek} =
\frac{\partial^{n+m+k+\ell} V}
{\partial S^n \partial \sigma^m \partial r^k \partial T^\ell}
$$