from itertools import combinations
from collections import defaultdict, Counter
from typing import Dict, List, Set, Any, KeysView
import numpy as np

def apriori(transactions: List, s_threshold: int, k_itemsets:int) -> Dict:
    """Finds frequent itemsets with a support threshold s
    Args:
      transactions: Input data
      s_threshold: Support threshold
      k_itemsets: Parameter for the size of the item set i.e. number of iterations
    Returns:
        frequent_item_sets: All frequent item sets and their corresponding support
    """
    # Placeholder to store all frequent itemsets and their support
    frequent_item_sets = {}

    # A-Priori pass for each of 1 up to K-itemsets
    for k in range(0, k_itemsets+1):
        # Create a dictionary for counting k-itemsets
        # TODO counts = defaultdict() 
        counts = {}
        for idx, transaction in enumerate(transactions):
            if k == 0:
                # create singletones
                Ck = list(combinations(transaction, 1))
            else:
                # Turn the list of integers into a list of tuples, where we make
                # sure that the tuples are sorted from small to large
                transaction = list(combinations(sorted(transaction), k))

                # Find all frequent itemsets from the previous round
                k_min_f_items = []
                for k_item in transaction:
                    # Note Lk here is Lk-1
                    if Lk[k_item] != 0:
                        k_min_f_items.append(k_item)

                # Turn f_items into a set of frequent singletons
                f_singletons = set([x for l in k_min_f_items for x in l])

                # Obtain all candidate frequent k-itemsets
                Ck = list(combinations(sorted(f_singletons), k+1))

            # Loop over the candidate items and count them
            for item in Ck:
                    # counts[item] += 1 TODO
                if item not in counts.keys():
                    counts[item] = 1
                else:
                    counts[item] += 1

            if not k == 0:
                # Only keep the items in the transaction that are candidate
                # f_singletons
                transactions[idx] = list(f_singletons)

        # Determine which items are frequent
        Lk = {}
        for key, v in counts.items():
            if v >= s_threshold:
                # Create a unique hash for the frequent itemset
                Lk[key] = 1

                # Store the frequent itemset and its support
                frequent_item_sets[key] = v
            else:
                Lk[key] = 0

        if Lk == {}:
            print(f"There are at most {k}-itemsets.\n")
            break

    return frequent_item_sets

def find_frequent_singletones(transactions: List[Set[int]], s_threshold: int = 1161) ->Set[int]:
    """
    TODO
    This function finds all the items having a support greater than s across all the baskets.
    :param baskets: the list of all baskets represented as sets
    :param s: the threshold support to consider an item as frequent
    :return: the set of all frequent singletons
    """

    item_to_support = defaultdict(int)

    for basket in transactions:
        for item in basket:
            item_to_support[item] += 1

    print(f'The market contains {len(item_to_support)} different items.')
    print(f'The average support is {np.mean(list(item_to_support.values())):.2f}')

    # s_threshold_absolute = s_threshold*len(item_to_support)
    frequent_dict = dict(filter(lambda element: element[1] > s_threshold, item_to_support.items()))
    return frequent_dict.keys()

def generate_candidate_item_sets(
    item_sets: Set[int],
    k_itemsets: int
    ) -> Set[Set[int]]:
    """
    This function returns the set of candidate new frequent itemsets for step k+1 of the a priori algorithm
    by combining the itemsets found at step k.
    :param precedent_item_sets: the frequent itemsets found at time k of the algorithm
    :param item_set_length: the length of the next candidates to be returned
    :return: a set of candidate frequent itemsets of length k+1
    """
    k_candidates = list(combinations(sorted(item_sets), k_itemsets))

    return k_candidates

def filter_frequent_item_sets(
        transactions: List[Set[int]],
        k_candidates: Set[Set[int]],
        k_itemsets: int,
        s_threshold: float = 0.1
) -> Dict[Set[int], int]:
    """
    This function finds all the itemsets having a support greater than s across all the baskets.
    :param baskets: the list of all baskets represented as sets
    :param candidate_item_sets: the set of itemsets candidate to be frequent
    :param item_set_length: the length of the itemsets
    :param s: the threshold support to consider an itemset as frequent
    :return: the set of all frequent itemsets
    """
    item_to_support = Counter(
        [
            set(item_set)
            for basket in transactions
            for item_set in combinations(basket, k_itemsets)
            if set(item_set) in k_candidates
        ]
    )
    item_to_support = Counter()
     
             
    # for basket in transactions:
    #     for candidate_set in k_candidates: #{{12,14}, {8,5},...}
    #         for candidate in candidate_set: # {12,14}
    #             if candidate in basket:
                    
    #             else:
    #                 break
    #             item_to_support[]
            
    #         for item_set in combinations(basket, k_itemsets)
    #         if set(item_set) in k_candidates
    #     ]
    # )

    s_threshold_absolute = s_threshold*len(item_to_support)
    return dict(
        filter(
            lambda element: element[1] > s_threshold_absolute,
            item_to_support.items()
        )
    )



if __name__ == '__main__':
    from dataset_reader import read_transactions
    dataset_file = 'T10I4D100K.dat'
    transactions = read_transactions(dataset_file)
    print(len(transactions))
    frequent_singletones = find_frequent_singletones(transactions = transactions)
    print(len(frequent_singletones))
    candidates_2 = generate_candidate_item_sets(frequent_singletones, k_itemsets=2 )
    print(len(candidates_2))
    frequent_items = filter_frequent_item_sets(transactions, candidates_2, k_itemsets=3)
    print(frequent_items, len(frequent_items))



