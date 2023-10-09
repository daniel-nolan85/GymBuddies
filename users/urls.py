from django.urls import path

from .views import *


app_name = 'users'

urlpatterns = [
    path('', ProfileListView.as_view(), name='all_profiles'),
    path('my-buddies/', MyBuddiesView.as_view(), name='my_buddies'),
    path('search/', SearchBuddiesView.as_view(), name='search'),
    path('my-profile/', my_profile_view, name='my_profile'),
    path('update/', update_my_profile_view, name='update'),
    path('my-invites/', invites_received_view, name='my_invites'),
    path('to-invite/', invite_profiles_list_view, name='invite_profiles'),
    path('send-invite/', send_invitation, name='send_invite'),
    path('send-invite/cancel/', cancel_invitation, name='cancel_invite'),
    path('remove_buddy/', remove_from_buddies, name='remove_buddy'),
    path('profile/<slug>/<int:sender_id>', ProfileDetailView.as_view(), name='profile_detail'),
    path('my-invites/accept/', accept_invitation, name='accept_invite'),
    path('my-invites/reject/', reject_invitation, name='reject_invite'),

    path('messages/', MessagesView.as_view(), name='messages'),
    path('read-message/', message_read, name='read_message'),
    path('unread-message/', message_unread, name='unread_message'),
    path('delete-message/', message_delete, name='delete_message'),

    path('terms-and-conditions', TermsAndConditionsView.as_view(), name='terms_conditions'),
    path('privacy-policy', PrivacyPolicyView.as_view(), name='privacy'),
    path('cookies-policy', CookiesPolicyView.as_view(), name='cookies'),

    path('deactivate-user/<str:username>', deactivate_user, name='deactivate_user'),
]
