import dataclasses
import numpy as np

from scripts.config import logger
from simlog.logger import InnerContext
from simlog.simlog import get_arrays, get_pvalues_per_index, get_lowest_fdr


@dataclasses.dataclass
class SimulationParams:
    pass

class PostProcessor:
    def __init__(self, logger):
        #logger provides the config
        pass

    def get_result(self, keys):
        pass



def main():
    n = 2
    num_full_experiments = 2
    for experiment_iter in range(num_full_experiments):
        for i in range(n):
            with InnerContext(logger, [f"experiment{experiment_iter}", f"i{i}"]):
                list1 = get_arrays()
                logger.log_raw_numbers(list1, ["arrayValues", "healthy"], level=logger.LOW)
                list2 = get_arrays()
                logger.log_raw_numbers(list2, ["arrayValues", "diseased"], level=logger.LOW)

                pvalues = get_pvalues_per_index(list1, list2)
                logger.log_histogram(pvalues, ["pvalues"])

                lowest_fdrs = np.zeros(n)
                lowest_fdrs[i] = get_lowest_fdr(pvalues)
                
        with InnerContext(logger, [str(experiment_iter)]):
            print("Result")
            print(lowest_fdrs)
            ALPHA = 0.5
            num_significant_fdrs = np.sum(lowest_fdrs < ALPHA)
            print(num_significant_fdrs)
            logger.log_append(num_significant_fdrs, ["..", "significantFdrs"], level=logger.HIGH) #could have stored in list and logged outside loop..

if __name__ == "__main__":
    main()

