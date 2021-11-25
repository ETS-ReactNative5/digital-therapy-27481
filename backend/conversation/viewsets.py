from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from conversation.models import Conversation, Item
from conversation.serializers import (
    ConversationSerializer, ItemSerializer,
)
from contact.models import Contact
from core.utils import send_invitation_code
from users.models import User

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Item.objects.filter(listener=self.request.user)

    @action(["get"], detail=False)
    def sent(self, request):
        items = Item.objects.filter(speaker=request.user)
        page = self.paginate_queryset(items)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(self.serializer_class(items, many=True).data)

    @action(["post"], detail=True)
    def resolve(self, request, pk):
        obj = self.get_object()
        obj.resolved = True
        obj.save()
        return Response(self.serializer_class(obj, context={'request': request}).data)


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(person_from=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user

        instance = serializer.save(person_from=user)
        user_qs = User.objects.filter(email=instance.invited_email)
        if user_qs.exists():
            # add user as friend and send a notification
            Contact.objects.add_friend(user, user_qs.first())
            instance.person_to = user_qs.first()
            instance.save()
        else:
            # send an email invitation
            if hasattr(user, 'contacts'):
                invite_code = user.contacts.invite_code
            else:
                instance = Contact.objects.create(user=user)
                invite_code = instance.invite_code
            send_invitation_code(user, invite_code, instance.invited_email)
