from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict


class CustomPageNumberPagination(pagination.PageNumberPagination):

    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):  # pragma: no cover
        return Response(OrderedDict([
            ('rows_number', self.page.paginator.count), # this is the total number of rows in the queryset
            ('rows_per_page', self.page.paginator.per_page), # this is the number of rows per page
            ('page', self.page.number), # this is the current page number
            ('results', data),
        ]))

