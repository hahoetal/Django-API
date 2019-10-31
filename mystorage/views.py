from rest_framework import viewsets
from .models import Essay, Album, Files
from .serializers import EssaySerializer, AlbumSerializer, FilesSerializer
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .pagination import MyPagination
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication # 사용하고 싶은 authentication 클래스 가져오기
# from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser # 사용하고 싶은 permission 방식 클래스 가져오기.

class PostViewSet(viewsets.ModelViewSet):
    
    # authentication_classes = [BasicAuthentication, SessionAuthentication]
    # 적용하고 싶은 authentication 방식 리스트 형식으로 써주기. 쓰기만 해도 구현 완료!
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # 적용하고 싶은 permission 방식 리스트 형식으로 써주기

    queryset = Essay.objects.all().order_by('id') # 페이지네이션은 레코드를 정렬한 상태에서 해야 함...
    serializer_class = EssaySerializer
    pagination_class = MyPagination
    # view 마다 다르게 페이지네이션하고 싶을 때 pagiantion class를 만들어줌.


    filter_backends = [SearchFilter]
    search_fields = ('title', 'body')

    def perform_create(self, serializer):
        serializer.save(author = self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated:
            qs = qs.filter(author = self.request.user)
        else:
            qs = qs.none()

        return qs


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

# pdf 같은 파일을 업로드하려고 했을 때 오류가 발생... 이를 잡으려면 두가지가 필요.
# parser_class
# create() 오버라이딩, create() -> post()

class FileViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser) # 다양한 미디어 타입으로 request 수락할 수 있게 해줌
    
    queryset = Files.objects.all()
    serializer_class = FilesSerializer

    def post(self, request, *args, **kwargs): # post() 오버라이딩
        serializer = FilesSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = HTTP_201_CREATED)
        else:
            return Response(serializer.error, status = HTTP_400_BAD_REQUEST)