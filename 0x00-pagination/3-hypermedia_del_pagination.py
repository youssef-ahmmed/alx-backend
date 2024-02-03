#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Returns the start and end indices of a page"""
    start_idx: int = (page - 1) * page_size
    end_idx: int = page * page_size

    return start_idx, end_idx


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Handle deletion of item when querying
        """
        remaining_indices: List[int] = []
        indexed_data: Dict[int, List] = self.indexed_dataset()
        index: int = 0 if index is None else index
        indexed_data_keys: List[int] = sorted(indexed_data.keys())

        assert 0 <= index <= indexed_data_keys[-1]

        [remaining_indices.append(idx) for idx in indexed_data_keys
         if idx >= index and len(remaining_indices) <= page_size]
        data = [indexed_data.get(key) for key in remaining_indices]
        next_index = remaining_indices[-1] if len(remaining_indices) - page_size == 1 else None

        return {
            'index': index,
            'data': data,
            'page_size': page_size,
            'next_index': next_index
        }
