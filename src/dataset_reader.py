from os import path
from typing import List, Set

def read_transactions(file_name: str) -> List[Set[int]]:

    """Read transactions from file
    Args:
        file_name: File name (Here, T10I4D100K.dat.html)
    Returns:
        List of transactions, where each transaction is a set of integers
    """

    # Define the relative path to the zipped data
    file_dir = path.dirname(__file__)   
    rel_path = "../data/" + file_name
    dataset_path = path.join(file_dir, rel_path)

    # Read the data set and save them in a list 
    with open(dataset_path) as f:
        lines = f.readlines()
        transactions = [set(map(int, line.strip().split(sep=' '))) for line in lines]
        print('Data set is load.')
    return transactions

