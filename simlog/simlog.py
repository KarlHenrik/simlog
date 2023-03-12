"""Main module."""
import numpy as np
from scipy.stats import ttest_ind
import numpy as np

from scripts.config import logger
from simlog.logger import InnerContext


def get_arrays():
    arrays = []
    for i in range(100):
        array = np.random.uniform(0, 1, 1000)
        arrays.append(array)
    return arrays


def get_pvalues_per_index(list1, list2):
    pvalues = np.zeros(1000)
    for j in range(1000):
        group1 = [list1[i][j] for i in range(100)]
        group2 = [list2[i][j] for i in range(100)]
        _, pvalue = ttest_ind(group1, group2)
        pvalues[j] = pvalue
    return pvalues


def get_fdr(pvalues, alpha=0.05):
    n = len(pvalues)
    indices = np.argsort(pvalues)
    sorted_pvalues = pvalues[indices]
    fdr = np.zeros(n)
    for i in range(n):
        fdr[i] = sorted_pvalues[i] * n / (i + 1)
    min_fdr = np.minimum.accumulate(fdr[::-1])[::-1]
    fdr = np.minimum(min_fdr, 1)
    return fdr


def get_lowest_fdr(pvalues):
    fdr = get_fdr(pvalues)
    logger.log_histogram(fdr, ["fdrs"])
    lowest_fdr = np.min(fdr)
    logger.log_append(lowest_fdr, ["..","lowestFdrs"], level=logger.HIGH) #Could avoid the ugly ".." by logging the full list of lowest_fdrs, so just to point to a potential weakness of the logger architecture here..
    return lowest_fdr


