from rest_framework import generics, permissions

from api.permissions import IsLinkOwner
from api.serializers import LinkSerializer
from shortener.models import URL


class ChangeLinkTitle(generics.UpdateAPIView):
    pass


class LinksList(generics.ListAPIView):
    serializer_class = LinkSerializer

    def get_queryset(self):
        return URL.objects.filter(owner=self.request.user)


class LinkDetail(generics.RetrieveAPIView):
    serializer_class = LinkSerializer
    permission_classes = (IsLinkOwner,)
    queryset = URL.objects.all()
