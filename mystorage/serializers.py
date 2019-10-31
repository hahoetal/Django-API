from .models import Essay, Album, Files
from rest_framework import serializers

class EssaySerializer(serializers.ModelSerializer):

    author_name = serializers.ReadOnlyField(source = 'author.username')

    class Meta:
        model = Essay
        fields = ('pk', 'title','body', 'author_name')

class AlbumSerializer(serializers.ModelSerializer):

    author_name = serializers.ReadOnlyField(source = 'author.username')
    image = serializers.ImageField(use_url = True) # url을 이용해서 파일이 제대로 올라갔는지 확인.

    class Meta:
        model = Album
        fields = ('pk', 'author_name', 'image', 'desc')

class FilesSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source = 'author.username')
    myfile = serializers.FileField(use_url = True)

    class Meta:
        model = Files
        fields = ('pk', 'author', 'myfile', 'desc')
