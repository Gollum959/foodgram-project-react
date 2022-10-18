from rest_framework.pagination import PageNumberPagination


class PageNumberLimitPagination(PageNumberPagination):
    """Custom paginator, rename page_size_query_param to limit"""
    page_size_query_param = 'limit'
