from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError
from rest_framework.response import Response
from rest_framework import authentication, views, generics
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, ListItemSerializer, ProfileSerializer, NotificationSerializer, InviteSerializer
from .models import List, ListItem, Profile, Notification, Invite

class UserRetrieve(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            username = self.request.query_params['username']
        except KeyError:
            username = None
        if username:
            try:
                user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                return None
            else:
                if (username != self.request.user.username):
                    return user
                else:
                    return None
        return self.request.user

class ListItemView(generics.ListCreateAPIView):
    serializer_class = ListItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        list = current_user.profile.list
        return ListItem.objects.filter(parent=list)

    def create(self, request, *args, **kwargs):
        obj = ListItem.objects.create(
            parent=request.user.profile.list,
            author=request.user,
            body=request.data['body']
        )
        serialized = ListItemSerializer(obj)
        return Response(serialized.data)

class ListItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ListItem.objects.all()
    serializer_class = ListItemSerializer

class DidPartnerDisconnect(views.APIView):
    """Check if partner disconnected from the shared list"""

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """Compare the users' profile list IDs"""
        current_user = request.user

        list = current_user.profile.list

        if (list.userone == current_user):
            partner_list = list.usertwo.profile.list
        else:
            partner_list = list.userone.profile.list

        if (partner_list is None):
            result = True
        else:
            result = list.id != partner_list.id

        response = {'partnerDisconnected': result}
        return Response(response)

class UserConnectedToList(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        if (profile.list is None):
            result = False
        else:
            result = True
        return Response({"hasList": result})

class Disconnect(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        profile = request.user.profile
        list = profile.list

        if (list.userone == request.user):
            partner = list.usertwo
        else:
            partner = list.userone

        try:
            if (partner.profile.list is None):
                # partner disconnected
                list = profile.list
                list.delete()

                profile.list = None
                profile.save()
            else:
                profile.list = None
                profile.save()
        except:
            result = False
        else:
            result = True

        return Response({ "listDisconnected": result })

class ListNotificationView(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        current_user = self.request.user
        return Notification.objects.filter(receiver=current_user)

class SendInvite(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        receiver = get_object_or_404(User, username=request.data['username'])
        if receiver:
            try:
                with transaction.atomic():
                    i = Invite.objects.create(sender=request.user, receiver=receiver)
                    n = Notification.objects.create(sender=request.user, receiver=receiver, action='invite')
            except IntegrityError:
                return Response({ "error": "Something went wrong with saving data."})
            else:
                return Response({"result": "OK"})

class CheckInvite(generics.GenericAPIView):
    serializer_class = InviteSerializer

    def get(self, request, format=None):
        result = {
            "sent": None,
            "received": None
        }

        try:
            sent = get_object_or_404(Invite, sender=self.request.user, accepted=False)
        except:
            sent = None

        received = Invite.objects.filter(receiver=self.request.user, accepted=False)


        if sent:
            result["sent"] = InviteSerializer(sent).data
        if len(received) > 0:
            result["received"] =  InviteSerializer(received, many=True).data

        return Response(result)

class WithdrawInvite(generics.DestroyAPIView):
    seializer_class = InviteSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        current_user = self.request.user
        return get_object_or_404(Invite, sender=current_user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.perform_destroy(instance)
        return Response({ "success": True })

class DeclineInvite(generics.DestroyAPIView):
    seializer_class = InviteSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Invite, id=kwargs.get('pk', None))
        data = self.perform_destroy(instance)
        return Response({ "success": True })

class InviteListCreateView(generics.ListCreateAPIView):
    serializer_class = InviteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        obj = Invite.objects.create(
            sender=request.user,
            receiver=User.objects.get(id=request.data['receiver_id'])
        )
        serialized = InviteSerializer(obj)
        return Response(serialized.data)

class AcceptInvite(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        pk = kwargs.get('pk', None)

        try:
            with transaction.atomic():
                invite = get_object_or_404(Invite, id=pk)

                if (invite.sender_id > invite.receiver_id):
                    list, created = List.objects.get_or_create(userone=invite.receiver, usertwo=invite.sender)
                else:
                    list, created = List.objects.get_or_create(userone=invite.sender, usertwo=invite.receiver)

                if not created:
                    invite.sender.profile.list = list
                    invite.sender.profile.save()

                invite.delete()
        except:
            return Response({ "error": "Something went wrong!"})
        else:
            return Response({ "result": "success" })

# class CheckRequest(generics.RetrieveAPIView):
#     serializer_class = InviteSerializer
#
#     def get_object(self):
#         obj = get_object_or_404(Invite, receiver=self.request.user, accepted=False)
#         return obj
#
#
# class CheckRequestSent(generics.RetrieveAPIView):
#     serializer_class = InviteSerializer
#
#     def get_object(self):
#         obj = get_object_or_404(Invite, sender=self.request.user, accepted=False)
#         return obj
