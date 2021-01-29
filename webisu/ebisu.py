"""
This module provides a rough translation between the webisu API
and the original ebisu API, where functionality is equivalent.
Note that there may still be some differences, as noted in each
function, and in the README for this module.
"""

from webisu.webisu import p_recall_t_lnpdf       as _p_recall_t_lnpdf
from webisu.webisu import p_recall_t_pdf         as _p_recall_t_pdf
from webisu.webisu import p_recall_t_lnmean      as _p_recall_t_lnmean
from webisu.webisu import p_recall_t_mean        as _p_recall_t_mean
from webisu.webisu import update_model_bernoulli as _update_model_bernoulli
from webisu.webisu import init_model             as _init_model


def _convert_prior_to_params(prior):
    """
    Luckily, we both use (alpha, beta, half-life) tuples as parameters.
    If that ever changes, I will update this code.
    """
    return prior


def predictRecall(prior, tnow, exact=False):
    """
    See ebisu's predictRecall function documentation.

    Note: No _cachedBetaln (yet)
    """
    if exact:
        return _p_recall_t_mean(tnow, _convert_prior_to_params(prior))
    else:
        return _p_recall_t_lnmean(tnow, _convert_prior_to_params(prior))


def updateRecall(prior, successes, total, tnow, rebalance=True, tback=None):
    """
    See ebisu's updateRecall function documentation.

    Notes:
    * half-life chosen differently (as yet), which means the tback
      argument is ignored.
    * No _rebalace (yet), which means the rebalance argument is
      ignored.
    * No Binomial trials with total > 1, If a total argument
      greater than 1 is provided, this method will raise a
      NotImplementedError.
    """
    if total > 1:
        raise NotImplementedError("Sorry, total > 1 not implemented.")
    r = bool(successes) # true iff successes > 0 (assume non-negative)
    return _update_model_bernoulli(r, tnow, _convert_prior_to_params(prior))


def modelToPercentileDecay(model, percentile=0.5, coarse=False):
    """
    See ebisu's modelToPercentileDecay function documentation.

    Note: Not implemented. All arguments are ignores, and an
    exception is raised.
    """
    raise NotImplementedError("Sorry, modelToPercentilDecay not implemented.")


def defaultModel(t, alpha=3.0, beta=None):
    """
    See ebisu's defaultModel function documentation.

    Note: This app's init_model function provides default alpha=2
    instead of alpha=3.0, but it's a small difference, and this
    function goes with default alpha=3.0.
    """
    if beta is None:
        beta = alpha
    return (alpha, beta, t)

