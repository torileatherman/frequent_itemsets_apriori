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
    print(dataset_path)
    with open(dataset_path, 'r') as f:
        print(f)
        return [[int(x) for x in line.split()] for line in f]


if __name__ == '__main__':
    dataset_file = 'T10I4D100K.dat.html' 

    transactions = read_transactions(dataset_file)
    print(transactions)
