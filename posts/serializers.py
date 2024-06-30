from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    image = serializers.CharField()
    owner = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Post
        fields = [
            'id',
            'image',
            'title',
            'owner',
            'content',
            'created_at',
        ]

    def save(self, **kwargs):
        kwargs['owner'] = self.fields['owner'].get_default()
        return super().save(**kwargs)