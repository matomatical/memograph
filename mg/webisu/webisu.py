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

Future functions:

* p_recall_t_lncdf(p, t, θ):
    logarithm of cumulative density at time t for recall probability p.
    NOT YET IMPLEMENTED.
* p_recall_t_cdf(p, t, θ)
    exponentiated version of the above.
    NOT YET IMPLEMENTED.


On parameters θ:

The above-listed functions take a parameter θ which refers to the
(α, β, λ) triple of parameters of a memory model. The meaning of
the components of this parameter triple is as follows:

    α and β are the parameters of a Bayesian Beta belief distribution
    about a fact's recall probability after time λ (also known as the
    'half-life', because the Beta prior is often symmetric about 0.5).

TODO:

* Consider putting a cap/floor on δ during updates, since this might help
  solve numerical issues and ensure stability in the learning app itself,
  at the small cost of a reasonable limit on how drastically the model
  can update in a particular step.
"""


from math import exp, pow as mpow

from mg.webisu.pmath import ln_gammafn, ln_betafn
from mg.webisu.pmath import ln, ln1p, lnsubexp
from mg.webisu.pmath import beta_match_moments

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
    Compute the approximate Beta posterior model parameters after a
    Bayesian update based on a single review.

    The hypothetical process is as follows:

        1. prior P_recall@λ_old ~ Beta(α_old, β_old)
         |
         | move through time (the quiz is at elapsed time t)
         V
        2. prior P_recall@t     ~ GeneralisedBeta1(...)
         |
         | quiz result r (True for pass, False for fail)
         V
        3. postr P_recall@t     ~ (some other analytical expression)
         |
         | approximate λ_new by solving the equation:
         |     E[postr P_recall@λ_old] approx. = 2^-λ_old/λ_new
         | and time transform the posterior to this time
         V
        4. postr P_recall@λ_new ~ (some other analytical expression)
         |
         | moment-match a Beta distribution to approximate
         V
        5. postr P_recall@λ_new approx. ~ Beta(α_new, β_new)

    This function takes parameters assuming you have completed steps 1
    and 2, and reasons through steps 3, 4, and 5, returning the approx.
    posterior's parameters θ_new = (α_new, β_new, λ_new).
    """
    _, _, λ_old = θ

    # calculate the posterior after update at time t, shifted
    # back to time λ_old
    postr_λ_old = _analytic_posterior_bernoulli(r, t, λ_old, θ)
    
    # use this posterior mean to approximate the new half-life
    ln_μ_λ_old = postr_λ_old.ln_moment(1)
    λ_new = - λ_old * ln(2) / ln_μ_λ_old
    
    # compute again the posterior, this time shifted to λ_new
    postr_λ_new = _analytic_posterior_bernoulli(r, t, λ_new, θ)
    
    # match the posterior's moments with a beta distribution
    # to fit a new model
    ln_m1 = postr_λ_new.ln_moment(1)
    ln_m2 = postr_λ_new.ln_moment(2)
    mean  = exp(ln_m1)
    var   = exp(ln_m2) - exp(2*ln_m1)
    
    α_new, β_new = beta_match_moments(mean, var)
    return (α_new, β_new, λ_new)


class _analytic_posterior_bernoulli:
    def __init__(self, result, t_update, t_new, prior):
        self.r  = result
        α, β, λ = prior
        self.α  = α
        self.β  = β
        self.δ  = t_update / λ
        # ε * δ = (t_new / t_update) * (t_update / λ)
        self.δε = t_new / λ
        # precompute the denominator:
        self._ln_moment_denom = self._ln_moment_numer(0)
    def moment(self, n):
        return exp(self.ln_moment(n))
    def ln_moment(self, n):
        return self._ln_moment_numer(n) - self._ln_moment_denom
    def _ln_moment_numer(self, n):
        if self.r:
            return ln_betafn(self.α + n*self.δε + self.δ, self.β)
        else:
            return lnsubexp(
                ln_betafn(self.α + n*self.δε,          self.β),
                ln_betafn(self.α + n*self.δε + self.δ, self.β)
            )


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

