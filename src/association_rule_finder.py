from collections import defaultdict
from itertools import combinations
from typing import Dict, Set, FrozenSet

class AssociationRuleFinder():
    '''
    Given a set of frequent item sets, this method generates association rules and finds rules 
    that are said to have a practical effect in the context of the market-basket model.
    Attributes:
    
        c_threshold: The confidence threshold that determines which rules have a practical effect.
    '''

    def __init__(self, c_threshold: float = 0.5):
        self.c_threshold = c_threshold

    def find_rules(self, frequent_itemsets: Dict[FrozenSet[int], int]) -> Dict[FrozenSet[int], Set[FrozenSet[int]]]:

        '''
          Returns all association rules X -> Y  [i.e. left_side -> right_side] with a confidence greater than c_threshold.
        '''
        # Initialise the dict of rules
        rules  = {}

        # In order to create a rule we need at least 2 items in the item set.
        for item_set in filter(lambda x: len(x) > 1, frequent_itemsets.keys()):
            # Compute all possible subsets of item_sets
            for left_side_length in range(1, len(item_set)):
                for left_side in [frozenset(combination) for combination in combinations(item_set, left_side_length)]:

                    # Compute the confidence by getting the support of the item sets 
                    if left_side in frequent_itemsets.keys():
                        # Make use of the oberservation in lecture
                        confidence = frequent_itemsets.get(item_set) / frequent_itemsets.get(left_side)

                        # Keep assoc. rules that are confident enough
                        if confidence >= self.c_threshold:
                            # Get the complement set of items
                            right_side = item_set - left_side
                            rules[(left_side,right_side)] = confidence

        return rules



    