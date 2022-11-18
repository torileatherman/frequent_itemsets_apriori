
from typing import Dict, List, Set
import itertools


def find_subsets(s: Set, n: int) -> List:
    """Find all subsets of length n in a set s

    Args:
        s: The set
        n: The lenght of the desired subsets

    Returns:
        subsets: List of subsets of s of length n
    """
    subsets = list(itertools.combinations(s, n))

    # Make sure that the subsets are sorted from small to large
    subsets = [tuple(sorted(s)) for s in subsets]

    return subsets


def association_rules(f_item_sets: Dict, c:float=0.5) -> Dict:
    """Finds association rules I -> j of confidence at least c

    Args:
        f_item_sets: Frequent itemsets
        c: Confidence threshold

    Returns:
        a_rules: All association rules of confidence at least c
    """
    a_rules = {}
    for i_set, s in f_item_sets.items():
        # Association rules can only be found in item sets of at least length
        # two
        if len(i_set) > 1:
            # Find the support of the frequent itemset
            s_i_set = f_item_sets[i_set]

            # Turn the frequent itemset tuple into a set
            i_set = set(i_set)

            # Find all subsets of length n-1 of the frequent itemset
            i_subsets = find_subsets(i_set, len(i_set)-1)

            for i_subset in i_subsets:
                # Retrieve the support of the subset
                s_i_subset = f_item_sets[i_subset]

                # Calculate the confidence of the rule
                c_rule = s_i_set/s_i_subset

                # Turn the frequent subset tuple into a set
                i_subset = set(i_subset)

                if c_rule >= c:
                    # We store the association rule in a dictionary. The key is
                    # a tuple of length n  in which the first n-1 items
                    # represent an itemset and the n-th element the associated
                    # item. The value is the confidence of the association rule.
                    a_rules[(tuple(i_subset) + tuple(i_set ^ i_subset))] = c_rule

    return a_rules
