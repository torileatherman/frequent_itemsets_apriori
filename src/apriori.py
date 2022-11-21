from itertools import combinations
from collections import defaultdict, Counter
from typing import Dict, List, Set, Any, KeysView, FrozenSet
import numpy as np
from dataset_reader import read_transactions

class Apriori():
# initializing datastructures for transactions, itemsets and rules
    def __init__(self, transactions: Set[FrozenSet[int]], s_threshold: float = 0.5):
        self.transactions= transactions
        self.s_threshold = s_threshold

    def find_frequent_singletones(self) -> Dict[FrozenSet[int], int]:
        """
        TODO
        This function finds all the items having a support greater than s across all the baskets.
        :param baskets: the list of all baskets represented as sets
        :param s: the threshold support to consider an item as frequent
        :return: the set of all frequent singletons
        """

        item_to_support = defaultdict(int)

        for basket in self.transactions:
            for item in basket:
                item_to_support[frozenset([item])] += 1

        s_threshold_absolute = np.quantile(list(item_to_support.values()),self.s_threshold)
        frequent_dict = dict(filter(lambda element: element[1] > s_threshold_absolute, item_to_support.items()))
        return frequent_dict

    def generate_candidate_item_sets(self, item_sets: KeysView[FrozenSet[int]], k_itemsets: int) -> Set[FrozenSet[int]]:
        """
        This function returns the set of candidate new frequent itemsets for step k+1 of the a priori algorithm
        by combining the itemsets found at step k.
        :param precedent_item_sets: the frequent itemsets found at time k of the algorithm
        :param item_set_length: the length of the next candidates to be returned
        :return: a set of candidate frequent itemsets of length k+1
        """
        # k_candidates = frozenset(combinations(sorted(item_sets), k_itemsets))

        # return k_candidates
        return {
        item_set_left | item_set_right
        for item_set_left in item_sets
        for item_set_right in item_sets
        if len(item_set_left | item_set_right) == k_itemsets
    }

    def filter_frequent_item_sets(self, k_candidates: Set[FrozenSet[int]], k_itemsets: int) -> Dict[FrozenSet[int], int]:
        """
        This function finds all the itemsets having a support greater than s across all the baskets.
        :param baskets: the list of all baskets represented as sets
        :param candidate_item_sets: the set of itemsets candidate to be frequent
        :param item_set_length: the length of the itemsets
        :param s: the threshold support to consider an itemset as frequent
        :return: the set of all frequent itemsets
        """
        item_to_support = Counter()
        for candidate in k_candidates:
            for basket in self.transactions:
                if candidate.issubset(frozenset(basket)):
                    item_to_support[frozenset(candidate)] += 1

        print(f'The average support is {np.mean(list(item_to_support.values())):.2f}')
        s_threshold_absolute = np.quantile(list(item_to_support.values()),self.s_threshold) # self.s_threshold*np.sum(list(item_to_support.values()))
        frequent_dict = dict(filter(lambda element: element[1] > s_threshold_absolute, item_to_support.items()))
        return frequent_dict
    

    def apriori(self) ->  Dict[FrozenSet[int], int]:
        """
        This function reads from a file .dat assuming that on every row of the file there is a basket of items.
        The function then generates the set of frequent itemsets having support greater or equal than s and maximum size
        equal to maximum_item_set_size with the apriori algorithm.
        :param verbose:  if set to true, prints information on the process
        :param file: the path to the input file
        :param s: the minimum support required to consider an itemset frequent
        :return: the set of all frequent itemsets, represented as frozensets, mapped to their support
        """
     
        frequent_items = self.find_frequent_singletones()

        current_frequent_items = frequent_items.keys()
        print(f"1st Pass: Frequent items = {len(frequent_items)}")

        k = 2
        while len(current_frequent_items)>1:
            candidates = self.generate_candidate_item_sets(item_sets = current_frequent_items, k_itemsets = k)
            print(f"{k}th Pass: Candidates = {len(candidates)}")
            if len(candidates) > 0:
                new_frequent_items = self.filter_frequent_item_sets(candidates, k_itemsets = k)
                print(f"Frequent items = {len(new_frequent_items)}\n -------------------------------------")
                
                current_frequent_items = new_frequent_items.keys()
                frequent_items.update(new_frequent_items)
                k += 1
        return frequent_items
#if __name__ == '__main__':
    # dataset_file = 'T10I4D100K.dat'
    # transactions = read_transactions(dataset_file)
    # finder = Apriori(transactions, s_threshold=0.95)
    # k_frequent_item_sets = finder.apriori()