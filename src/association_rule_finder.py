from collections import defaultdict
from itertools import combinations
from typing import Dict, Set, FrozenSet

class AssociationRuleFinder():
    '''
    The class takes the frequent itemsets as input, and finds all association rules that meet the minimum confidence threshold.
        
    '''

    def __init__(self, c_threshold: float = 0.5):
        self.c_threshold = c_threshold

    def find_rules(self, frequent_itemsets: Dict[FrozenSet[int], int]) -> Dict[FrozenSet[int], Set[FrozenSet[int]]]:

        '''
          Returns all association rules X -> Y with a confidence greater than c_threshold.
        '''

        rules  = {}

        for item_set in filter(lambda x: len(x) > 1, frequent_itemsets.keys()):
            for left_side_length in range(1, len(item_set)):
                for left_side in [frozenset(combination) for combination in combinations(item_set, left_side_length)]:

                    if left_side in frequent_itemsets.keys():
                        confidence = frequent_itemsets.get(item_set) / frequent_itemsets.get(left_side)
                        if confidence >= self.c_threshold:
                            right_side = item_set - left_side
                            
                            rules[(left_side,right_side)] = confidence

        return rules



    