from itertools import combinations
from typing import Dict, List

def apriori(transactions: List, s_threshold: int, k_itemsets:int) -> Dict:
    """Finds frequent itemsets with a support threshold s
    Args:
      transactions: Input data
      s_threshold: Support threshold
      k_itemsets: Parameter for the size of the item set
    Returns:
        frequent_item_sets: All frequent item sets and their corresponding support
    """
    # Placeholder to store all frequent itemsets and their support
    frequent_item_sets = {}

    # A-Priori pass for each of 1 up to K-itemsets
    for k in range(0, k_itemsets+1):
        # Create a dictionary for counting k-itemsets
        counts = {}
        for idx, t in enumerate(transactions):
            if k == 0:
                Ck = list(combinations(t, 1))
            else:
                # Turn the list of integers into a list of tuples, where we make
                # sure that the tuples are sorted from small to large
                t = list(combinations(sorted(t), k))

                # Find all frequent itemsets from the previous round
                k_min_f_items = []
                for k_item in t:
                    # Note Lk here is Lk-1
                    if Lk[k_item] != 0:
                        k_min_f_items.append(k_item)

                # Turn f_items into a set of frequent singletons
                f_singletons = set([x for l in k_min_f_items for x in l])

                # Obtain all candidate frequent k-itemsets
                Ck = list(combinations(sorted(f_singletons), k+1))

            # Loop over the candidate items and count them
            for item in Ck:
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