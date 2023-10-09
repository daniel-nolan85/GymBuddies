from .models import Profile, Relationship, Message


def profile_pic(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        pic = profile_obj.get_avatar
        return {'pic': pic}
    return {}


def invites_received_num(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        qs_count = Relationship.objects.invitations_received(profile_obj).count()
        return {'invites_num': qs_count}
    return {}