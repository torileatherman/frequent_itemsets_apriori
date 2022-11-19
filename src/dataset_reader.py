from typing import List
from os import path

def read_transactions(file_name: str) -> List[List[int]]:

    """Read transactions from file
    Args:
        file_name: File name (E.g. T10I4D100K.dat.html)
    Returns:
        List of transactions, where each transaction is a list of integers
    """
    # Define the relative path to the zipped data
    file_dir = path.dirname(__file__)   
    rel_path = f"../data/{file_name}"
    dataset_path = path.join(file_dir, rel_path)
    with open(dataset_path) as f:
        lines = f.readlines()
        transactions = [set(map(int, line.strip().split(sep=' '))) for line in lines]
        print('Data set is read.')
    return transactions

if __name__ == '__main__':
    dataset_file = 'T10I4D100K.dat'
    transactions = read_transactions(dataset_file)

