from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


DEFAULT_PAGE = 1

class CustomPagination(PageNumberPagination):
	page = DEFAULT_PAGE
	page_size = 10
	max_page_size = 10
	page_size_query_param = 'page_size'

	def get_paginated_response(self, data):
		return Response({
			'next': self.get_next_link(),
			'previous': self.get_previous_link(),
			'count': self.page.paginator.count,
			'current_page': int(self.request.GET.get('page', DEFAULT_PAGE)),
			'page_size': int(self.request.GET.get('page_size', self.page_size)),
			'total': self.page.paginator.num_pages,
			'results': data
		})
