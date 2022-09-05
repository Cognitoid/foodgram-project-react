from rest_framework.pagination import PageNumberPagination

PAGE_SIZE = 6


class LimitPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'
