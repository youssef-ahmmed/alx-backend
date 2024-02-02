#!/usr/bin/env python3
"""Implement Hypermedia pagination"""

import csv
import math
from typing import Tuple, List, Dict


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
        """ Init of class server
        """
        self.__dataset = None

    def dataset(self) -> List[List]:
        """ Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """ Get the pages of the dataset
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        start_idx, end_idx = index_range(page, page_size)

        if start_idx >= len(self.dataset()):
            return []

        return self.__dataset[start_idx:end_idx]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """ Get the hypermedia of the dataset
        """
        data = self.get_page(page, page_size)
        start_idx, end_idx = index_range(page, page_size)

        return {
            'page_size': page_size if len(data) != 0 else 0,
            'page': page,
            'data': data,
            'next_page': page + 1 if end_idx < len(self.dataset()) else None,
            'prev_page': page - 1 if start_idx > 0 else None,
            'total_pages': math.ceil(len(self.dataset()) / page_size)
        }
