from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title','author', 'content','created_on')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('author','content','created_on','post')