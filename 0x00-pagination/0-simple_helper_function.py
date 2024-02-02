#!/usr/bin/env python3
"""Simple helper function"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Returns the start and end indices of a page"""
    start_idx = (page - 1) * page_size
    end_idx = page * page_size

    return start_idx, end_idx
