from rest_framework import serializers

from shortener.models import URL


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = (
            'id', 'title', 'full_link', 'description',
            'created_at', 'short_link', 'short_link_with_hostname'
        )

