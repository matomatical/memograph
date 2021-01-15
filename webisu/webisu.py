"""
Pure python implementation of a variant of the ebisu memory model.
See https://fasiha.github.io/ebisu/ for the original (implemented
in Python/NumPy, as well as other languages).

Matthew Farrugia-Roberts (m@far.in.net), 2021

Functions:

* p_recall_t_lnpdf(p, t, θ):
    logarithm of probability density at time t for recall probability p.
* p_recall_t_pdf(p, t, θ)
    exponentiated version of the above.
* p_recall_t_lncdf(p, t, θ):
    logarithm of cumulative density at time t for recall probability p.
    NOT YET IMPLEMENTED.
* p_recall_t_cdf(p, t, θ)
    exponentiated version of the above.
    NOT YET IMPLEMENTED.
* p_recall_t_lnmean(t, θ):
    logarithm of mean/expected recall probability at time t.
* p_recall_t_mean(t, θ):
    exponentiated version of the above.
* update_model_bernoulli(r, t, θ):
    return an updated model based on the result of a bernoulli trial
    with result r at time t.
* init_model(λ, α=2, β=α):
    return an initial model with some optional default values, you
    just need to provide a half-life in your preferred unit of time.


On parameters θ:

The above-listed functions take a parameter θ which refers to the
(α, β, λ) triple of parameters of a memory model. The meaning of
the components of this parameter triple is as follows:

    α and β are the parameters of a Bayesian Beta belief distribution
    about a fact's recall probability after time λ (also known as the
    'half-life', because the Beta prior is often symmetric about 0.5).

TODO:

* Is it appropriate to call the third parameter a 'half-life'---do things
  indeed stay balanced? Reconsider this to make sure it makes sense.
* Consider putting a cap/floor on δ during updates, since this might help
  solve numerical issues and ensure stability in the learning app itself,
  at the small cost of a reasonable limit on how drastically the model
  can update in a particular step.
* Currently the update method does not change λ, should consider some
  appropriate mechanisms including ebisu proper's method of setting to
  t and rebalancing as necessary (but I probably would prefer a simpler
  scheme such as just adapting it in either direction depending on r).
"""


from math import exp, pow as mpow

from webisu.pmath import ln_gammafn, ln_betafn
from webisu.pmath import ln, ln1p, lnsubexp
from webisu.pmath import beta_match_moments

# TODO: Also move GB1 pdf and expectation to a stats module? Then this
# module could just be about piping the parameters into the distribns...!


def p_recall_t_lnpdf(p, t, θ):
    """
    Compute log probability density of recall prob p after t units
    of elapsed time since last review.

    θ is an (α, β, λ) triple--see module documentation.

    TODO: Special case for p in {0, 1} (currently gives error)
    """
    α, β, λ = θ
    δ = t / λ

    # P_δ(p) = GB1(p; 1/δ, 1, α, β)
    #        = p^((α-δ)/δ)(1-p^(1/δ))^(β-1) / (d Β(α, β))
    lnpdf = (
            + (α - δ) / δ * ln(p)
            + (β - 1) * ln1p(-mpow(p, 1/δ))
            - ln(δ)
            - ln_betafn(α, β)
        )
    return lnpdf


def p_recall_t_pdf(p, t, θ):
    """
    Compute probability density of recall prob p after t units
    of elapsed time since last review.

    θ is an (α, β, λ) triple--see module documentation.
    """
    return exp(p_recall_t_lnpdf(p, t, θ))


def p_recall_t_lncdf(p, t, θ):
    """
    Compute log cumulative density of recall prob p after t units
    of elapsed time since last review.

    θ is an (α, β, λ) triple--see module documentation.

    TODO: Implement (!) incomplete beta function to help with the
    computation
    """
    α, β, λ = θ
    δ = t / λ

    # F_GB1(p; 1/δ, 1, α, β) = F_B(x/d; α, β)
    # according to:
    # "Butler and McDonald (1989) and Kleiber and Kotz (2003)",
    # as summarised in
    # Sarabia, Guillen, Chulia, and Prieto, "Tail risk measures using flex-
    # ible parametric distributions", SORT 2019; DOI 10.2436/20.8080.02.86
    return NotImplementedError("TODO: Needs the incomplete beta function")


def p_recall_t_cdf(p, t, θ):
    """
    Compute cumulative density of recall prob p after t units
    of elapsed time since last review.

    θ is an (α, β, λ) triple--see module documentation.
    """
    return exp(p_recall_t_lncdf(p, t, θ))


def p_recall_t_lnmean(t, θ):
    """
    Compute log expected recall probability after t units of time
    since last review.

    θ is an (α, β, λ) triple---see module documentation.
    """
    α, β, λ = θ
    δ = t / λ

    # E_GB1[P] = (Γ(α+β) * Γ(α+δ)) / (Γ(α) * Γ(α+β+δ))
    lnmean = (
            + ln_gammafn(α+β)
            + ln_gammafn(α+δ)
            - ln_gammafn(α)
            - ln_gammafn(α+β+δ)
        )
    return lnmean


def p_recall_t_mean(t, θ):
    """
    Compute expected recall probability after t units of time
    since last review.

    θ is an (α, β, λ) triple---see module documentation.
    """
    return exp(p_recall_t_lnmean(t, θ))


def update_model_bernoulli(r, t, θ):
    """
    Compute the posterior model parameters after a Bayesian update to
    the beta distribution at the half-life for a single review after
    elapsed time t with recall result r (recalled=True, failed=False).

    TODO: How to decide new λ? for now set t'=λ (so δε=1)
    """
    α, β, λ = θ
    δ = t / λ

    # for now, just set the new half-life to the same as the old;
    # TODO: come up with an elegant way to select a new half-life
    λ_new = λ
    δε = 1

    # compute the moments of the posterior distribution at the new half-life
    if r:
        _ln_m = lambda N: ln_betafn(α + δ + N*δε, β)
    else:
        _ln_m = lambda N: lnsubexp(ln_betafn(α+N*δε,β), ln_betafn(α+δ+N*δε,β))
    ln_mNdenom = _ln_m(0)
    ln_m1numer = _ln_m(1)
    ln_m2numer = _ln_m(2)
    m1   = exp(ln_m1numer - ln_mNdenom)
    m2   = exp(ln_m2numer - ln_mNdenom)
    m1sq = exp(2*(ln_m1numer - ln_mNdenom))
    mean = m1
    var  = m2 - m1sq

    # match a beta distribution to this posterior to give the new model
    α_new, β_new = beta_match_moments(mean, var)
    return (α_new, β_new, λ_new)


def init_model(λ, α=2, β=None):
    """
    Construct a default/initial model with parameters α, β, and λ, 
    see module documentation.

    Parameters
    ----------
    * λ--half-life. Required. It's the initial half-life of the
        memory model in arbitrary time units (the same should be
        used for the t parameter for other functions from this
        module).
    * α--first beta distribution parameter. Optional (default: 2).
    * β--second beta distribution parameter. Optional (default:
        same value as α, for a symmetric beta distribution).
    """
    if β is None:
        β = α
    return (α, β, λ)

