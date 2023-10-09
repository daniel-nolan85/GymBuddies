from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, ListView, TemplateView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from allauth.account.views import PasswordChangeView

from .models import Profile, Relationship, Message
from .forms import ProfileUpdateForm, ProfilePicForm, MessageForm


@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)

    p_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile)
    if p_form.is_valid():
        p_form.save()
        return JsonResponse({'message': 'works'})

    context = {
        'profile': profile,
        'p_form': p_form,
    }

    return render(request, 'users/my_profile.html', context)


@login_required
def update_my_profile_view(request):
    profile = Profile.objects.get(user=request.user)

    up_form = ProfileUpdateForm(request.POST or None, instance=profile)
    if up_form.is_valid():
        up_form.save()
        return JsonResponse({'message': 'works'})


@login_required
def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False

    if len(results) == 0:
        is_empty = True

    context = {
        'qs': results,
        'is_empty': is_empty,
        'profile': profile,
    }

    return render(request, 'users/my_invites.html', context)


@login_required
def accept_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)

        if rel.status == 'sent':
            rel.status = 'accepted'
            rel.save()

    return redirect('users:my_invites')


@login_required
def reject_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()

    return redirect('users:my_invites')


@login_required
def invite_profiles_list_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_sent(profile)
    results = list(map(lambda x: x.receiver, qs))
    is_empty = False

    if len(results) == 0:
        is_empty = True

    context = {
        'qs': results,
        'is_empty': is_empty,
        'profile': profile,
    }

    return render(request, 'users/to_invite_list.html', context)


@login_required
def cancel_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(user=request.user)
        receiver = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()

    return redirect('users:invite_profiles')


class ProfileDetailView(LoginRequiredMixin, CreateView):
    model = Profile
    template_name = 'users/detail.html'
    form_class = MessageForm

    def get_object(self, slug=None):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []

        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)

        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False
        context['account'] = Profile.objects.get(slug=self.kwargs['slug'])
        context['profile'] = Profile.objects.get(user=self.request.user)

        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = Profile.objects.get(slug=self.kwargs['slug'])
        instance.sender = Profile.objects.get(id=self.kwargs['sender_id'])
        instance.save()
        return JsonResponse({'message': model_to_dict(instance)}, status=200)

    def get_success_url(self):
        return reverse('posts:index')


class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'users/profile_list.html'
    context_object_name = 'qs'
    paginate_by = 12

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []

        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)

        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False
        context['profile'] = Profile.objects.get(user=self.request.user)

        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context


class MyBuddiesView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'users/my_buddies.html'
    context_object_name = 'qs'
    paginate_by = 12

    def get_queryset(self):
        qs = Profile.objects.get_all_buddies(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []

        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)

        context['profile'] = profile
        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False

        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context


@login_required
def send_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='sent')

        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('users:my_profile')


@login_required
def remove_from_buddies(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()

        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('users:my_profile')


class SearchBuddiesView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'users/buddy_search.html'
    context_object_name = 'qs'
    # paginate_by = 4

    def get_queryset(self):
        q1 = self.request.GET.get('buddy_name')
        q2 = self.request.GET.get('buddy_location')

        if q1 or q2:
            return Profile.objects.filter(Q(first_name__icontains=q1) |
                                          Q(last_name__icontains=q1) |
                                          Q(user__username__icontains=q1),
                                          location__icontains=q2)

        return Profile.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []

        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)

        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False
        context['profile'] = Profile.objects.get(user=self.request.user)

        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context


class MessagesView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'users/messages.html'
    context_object_name = 'messages'
    # paginate_by = 5

    def get_queryset(self):
        return Message.objects.filter(user__user=self.request.user).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(MessagesView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context


@login_required
def message_read(request):
    if request.method == 'POST':
        selected_messages = request.POST.getlist('message')
        Message.objects.filter(id__in=selected_messages).update(unread=False)
        return redirect('users:messages')
    return redirect('users:my_profile')


@login_required
def message_unread(request):
    if request.method == 'POST':
        selected_messages = request.POST.getlist('message')
        Message.objects.filter(id__in=selected_messages).update(unread=True)
        return redirect('users:messages')
    return redirect('users:my_profile')


@login_required
def message_delete(request):
    if request.method == 'POST':
        selected_messages = request.POST.getlist('message')
        Message.objects.filter(id__in=selected_messages).delete()
        return redirect('users:messages')
    return redirect('users:my_profile')


class TermsAndConditionsView(TemplateView):
    template_name = 'users/terms_conditions.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'users/privacy.html'


class CookiesPolicyView(TemplateView):
    template_name = 'users/cookies.html'


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = '/'


@login_required
def deactivate_user(request, username):
    context = {}
    try:
        user = User.objects.get(username=username)
        user.is_active = False
        user.save()
        context['msg'] = 'Profile successfully disabled.'
    except User.DoesNotExist:
        context['msg'] = 'User does not exist.'
    except Exception as e:
        context['msg'] = e.message

    return render(request, 'account/account_inactive.html', context=context)

