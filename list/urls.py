from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.UserRetrieve.as_view(), name='profile'),
    path('find/user/', views.UserRetrieve.as_view(), name='user-list-view'),

    path('listitems/', views.ListItemView.as_view(), name='list'),
    path('listitems/<int:pk>/', views.ListItemDetailView.as_view(), name='toggle-listitem'),

    path('did/partner/disconnect/', views.DidPartnerDisconnect.as_view(), name='did-partner-disconnect'),
    path('user/connected/to/list/', views.UserConnectedToList.as_view(), name='user-connected-to-list'),
    path('disconnect/', views.Disconnect.as_view(), name='disconnect'),
    path('notifications/', views.ListNotificationView.as_view(), name='notifications'),
    path('send/invite/', views.SendInvite.as_view(), name='send-invite'),

    path('check/invite/', views.CheckInvite.as_view(), name='check-invite'),
    path('withdraw/invite/', views.WithdrawInvite.as_view(), name='withdraw-invite'),
    path('decline/invite/<int:pk>/', views.DeclineInvite.as_view(), name='decline-invite'),
    path('accept/invite/<int:pk>/', views.AcceptInvite.as_view(), name='accept-invite'),
    path('invite/listcreate/', views.InviteListCreateView.as_view(), name='invite-list-create'),

    # path('check/request/', views.CheckRequest.as_view(), name='check-request'),
    # path('check/request/sent/', views.CheckRequestSent.as_view(), name='check-request-sent'),
]
