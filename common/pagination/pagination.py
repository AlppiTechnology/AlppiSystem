from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response



class CustomPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 30

    def get_paginated_response(self, data):
        return Response(
            {   
                'navigation':{
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link()
                },
                'next': self.page.next_page_number() if self.page.has_next() else None,
                'previous': self.page.previous_page_number() if self.page.has_previous() else None,
                'count':self.page.paginator.count,
                'results': data
            }
        )