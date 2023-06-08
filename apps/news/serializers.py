from rest_framework import serializers

from apps.news.models import News, Category, Comment, Attachment


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    def comment_count(self, obj):
        return obj.comment_set.count()

    class Meta:
        model = Comment
        fields = "__all__, comment_count"


class NewsRetrieveSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = News
        fields = "__all__"


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = "__all__"
