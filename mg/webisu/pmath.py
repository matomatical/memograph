"""
Some pure Python math functions for working with the beta and gamma
functions and the beta distribution in logarithmic space.
"""

# # #
# Working in log space
# 

from math import log as ln, log1p as ln1p, exp


def lnaddexp(x, y):
    """
    Safely compute ln(exp(x) + exp(y)), to add numbers within their
    log-space representations.
    """
    if x == y:
        return x + ln(2)
    elif x < y:
        return y + ln1p(exp(x - y))
    else:
        return x + ln1p(exp(y - x))


def lnsubexp(x, y):
    """
    Safely compute ln(exp(x) - exp(y)), to subtract numbers within
    their log-space representations.

    Assumes x > y so that exp(x) - exp(y) > 0 and ln(exp(x) - exp(y))
    is defined; otherwise MathError.
    """
    return x + ln1p(-exp(y-x))



# # #
# Gamma and Beta functions
# 

from math import lgamma as ln_gammafn


def ln_betafn(α, β):
    """
    Compute the logarithm of the beta function for parameters α and β.
    """
    return ln_gammafn(α) + ln_gammafn(β) - ln_gammafn(α+β)



# # #
# Beta distribution
# 

def beta_match_moments(μ, Σ):
    """
    Match a Beta distribution given mean μ and variance Σ.
    """
    factor = μ * (1-μ) / Σ - 1
    α = factor * μ
    β = factor * (1-μ)
    return α, β

