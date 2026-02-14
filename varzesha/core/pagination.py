"""
Pagination classes following FAANG standards.
Cursor pagination for time-series data, page number for search.
"""
from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.response import Response


class CursorPagination(CursorPagination):
    """
    Cursor-based pagination for high-performance lists.
    Prevents skip/offset degradation on large datasets.
    """
    page_size = 20
    ordering = "-created_at"
    cursor_query_param = "cursor"

    def get_paginated_response(self, data: list) -> Response:
        return Response({
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        })


class SearchPagination(PageNumberPagination):
    """
    Page-number pagination for search results with relevance scoring.
    """
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data: list) -> Response:
        return Response({
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
            "total_pages": self.page.paginator.num_pages,
            "current_page": self.page.number,
        })