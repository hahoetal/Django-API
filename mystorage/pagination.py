from rest_framework.pagination import PageNumberPagination
# viewset마다 다르게 페이지네이션하기 위해 가져옴.

class MyPagination(PageNumberPagination):
    page_size = 5