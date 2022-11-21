from itertools import combinations
from collections import defaultdict, Counter
from typing import Dict, List, Set, Any, KeysView, FrozenSet
import numpy as np
from dataset_reader import read_transactions

class Apriori():
    """This class computes the frequent item sets of a list of transactions.

    The code sketches the idea of R. Agrawal and R. Srikant in "Fast Algorithms for Mining Association Rules" and follows a cand
    It is based on a candidate generation-and-test approach. Given a list of (frequent) items, generate candidates as their combinations and then filter out the most frequent items.

    Attributes:
        transactions: A list of transactions, where each transaction is a set of integers where each corresponds to an item.
        s_threshold: The support threshold that determines which item sets are considered to be frequent.
    """

    def __init__(self, transactions: Set[FrozenSet[int]], s_threshold: float = 0.5):

        self.transactions= transactions
        self.s_threshold = s_threshold

    def find_frequent_singletones(self) -> Dict[FrozenSet[int], int]:
        """
        Returns all the singletones that have a support greater than s_threshold across all the baskets.
   
        :return: Dict of singletones and their corresponding support (i.e. number of occurences in the transactions)
        """
        # Initialize counter
        item_to_support = defaultdict(int)

        # Increment the counter if the singletone is found in a basket
        for basket in self.transactions:
            for item in basket:
                item_to_support[frozenset([item])] += 1

        # Compute the absolute support threshold based on the quantile
        s_threshold_absolute = np.quantile(list(item_to_support.values()),self.s_threshold)
        print(f'The support threshold is {s_threshold_absolute}')

        # Keep values that are above the support threshold 
        frequent_dict = dict(filter(lambda element: element[1] > s_threshold_absolute, item_to_support.items()))
        return frequent_dict

    def generate_candidate_item_sets(self, item_sets: KeysView[FrozenSet[int]], k_itemsets: int) -> Set[FrozenSet[int]]:
        """
        Returns candidates based on combinations of the frequent itemsets with a size of k_itemsets
       
        :param item_sets: the frequent itemsets found at time k-1 of the algorithm
        :param k_itemsets: the length of the next set of candidates
        :return: a set of candidate itemsets of length k
        """
        # Combines subsets such that the resulting set has length k_itemsets
        return {
        item_set_left | item_set_right
        for item_set_left in item_sets
        for item_set_right in item_sets
        if len(item_set_left | item_set_right) == k_itemsets
    }

    def filter_frequent_item_sets(self, k_candidates: Set[FrozenSet[int]]) -> Dict[FrozenSet[int], int]:
        """
        Return all the itemsets having a support greater than s_threshold across all the baskets.

        :param k_candidates: the set of candidate itemsets that are potentially frequent

        :return: the set of all frequent itemsets
        """
        # Initialize counter
        item_to_support = Counter()

        # Increment the counter if the candidate is found in a basket
        for candidate in k_candidates:
            for basket in self.transactions:
                if candidate.issubset(frozenset(basket)):
                    item_to_support[frozenset(candidate)] += 1

        print(f'The average support is {np.mean(list(item_to_support.values())):.2f}')

        # Compute the absolute support threshold based on the quantile
        s_threshold_absolute = np.quantile(list(item_to_support.values()),self.s_threshold) # self.s_threshold*np.sum(list(item_to_support.values()))
        print(f'The support threshold is {s_threshold_absolute}')

        # Keep values that are above the support threshold 
        frequent_dict = dict(filter(lambda element: element[1] > s_threshold_absolute, item_to_support.items()))
        return frequent_dict
    

    def apriori(self) ->  Dict[FrozenSet[int], int]:
        """
        This function creates the apriori pipeline. After finding the frequent singletones, it iteratively generates new candidates for 
        with a length increased by 1. Then it finds the most frequent (compared to the support threshold) items and generates new candidates again.
        The algorithm stops when the set of frequent items is 1. 

  
        :return: the set of all frequent itemsets, represented as frozensets, mapped to their support
        """

        # Find frequent singletones
        frequent_items = self.find_frequent_singletones()

        # Update the current frequent item set (only keys)
        current_frequent_items = frequent_items.keys()
        print(f"1st Pass: Frequent items = {len(frequent_items)}")

        k = 2
        while len(current_frequent_items)>1:
            # Generate new candidates
            candidates = self.generate_candidate_item_sets(item_sets = current_frequent_items, k_itemsets = k)
            print(f"{k}th Pass: Candidates = {len(candidates)}")

            if len(candidates) > 0:
                # Get the frequent items 
                new_frequent_items = self.filter_frequent_item_sets(candidates)
                print(f"Frequent items = {len(new_frequent_items)}\n -------------------------------------")
                
                # Update the current frequent item set (only keys)
                current_frequent_items = new_frequent_items.keys()
                # Save all frequent k_itemsets
                frequent_items.update(new_frequent_items)

                k += 1
        return frequent_items
