# Black–Scholes Model

## Call Option Price

$$
C = s N(d_1) - K e^{-rt} N(d_2)
$$

## Put Option Price

$$
P = K e^{-rt} N(d_2) - s N(d_1)
$$

---

# Core Quantities

$$
d_1 = \frac{\ln(s/K) + \left(r + \frac{1}{2}\sigma^2\right)t}{\sigma\sqrt{t}}
$$

$$
d_2 = d_1 - \sigma\sqrt{t}
$$

---

## Definitions (Inputs)

* $s$ current underlying asset price
* $K$ strike price
* $t$ time to maturity (in years)
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
\Delta = \frac{\partial V}{\partial s}
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

* Measures directional exposure ("shares equivalent")
* Positive for calls, negative for puts

---

## Gamma ($\Gamma$)

### Definition

Rate of change of Delta with respect to underlying price.

$$
\Gamma = \frac{\partial^2 V}{\partial s^2}
$$

$$
\Gamma = \frac{\phi(d_1)}{s \sigma \sqrt{t}}
$$

### Interpretation

* Measures convexity of option price
* Same for calls and puts

---

## Vega ($\nu$)

### Definition

Sensitivity of option price to volatility.

$$
\nu = \frac{\partial V}{\partial \sigma}
$$

$$
\nu = s \phi(d_1)\sqrt{t}
$$

### Interpretation

* Higher when option is ATM
* Measures exposure to implied volatility changes

---

## Theta ($\Theta$)

### Definition

Sensitivity of option price to time decay.

$$
\Theta = \frac{\partial V}{\partial t}
$$

Call:

$$
\Theta_c =
-\frac{s \phi(d_1)\sigma}{2\sqrt{t}}
- rK e^{-rt} N(d_2)
$$

Put:

$$
\Theta_p =
-\frac{s \phi(d_1)\sigma}{2\sqrt{t}}
+ rK e^{-rt} N(-d_2)
$$

### Interpretation

* Measures daily time decay ("theta burn")
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
\rho_c = K t e^{-rt} N(d_2)
$$

Put:

$$
\rho_p = -K t e^{-rt} N(-d_2)
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
\text{Vanna} = \frac{\partial^2 V}{\partial s \partial \sigma}
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
\text{Charm} = \frac{\partial^2 V}{\partial s \partial t}
$$

Call:

$$
\text{Charm}_c =
-\phi(d_1)\frac{2rt - d_2 \sigma \sqrt{t}}{2t\sigma\sqrt{t}}
$$

### Interpretation

* Measures Delta decay as time passes

---

## Veta

### Definition

Sensitivity of Vega to time.

$$
\text{Veta} = \frac{\partial^2 V}{\partial \sigma \partial t}
$$

$$
\text{Veta} =
- s \phi(d_1)\sqrt{t}
  \left(
  r\frac{d_1}{\sigma\sqrt{t}}
  -\frac{1 + d_1 d_2}{2t}
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
\text{Vera} = K t e^{-rt}\phi(d_2)\frac{\sqrt{t}}{\sigma}
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
\text{Speed} = \frac{\partial^3 V}{\partial s^3}
$$

$$
\text{Speed} =
-\frac{\Gamma}{s}
\left(
\frac{d_1}{\sigma\sqrt{t}} + 1
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
\text{Color} = \frac{\partial \Gamma}{\partial t}
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
V = V(s, \sigma, r, t)
$$

$$
\text{Greek} =
\frac{\partial^{n+m+k+\ell} V}
{\partial s^n \partial \sigma^m \partial r^k \partial t^\ell}
$$