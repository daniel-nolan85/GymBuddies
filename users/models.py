from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatechars, slugify
from django.db.models import Q
from django.utils import timezone


from .utils import get_random_code


class ProfileManager(models.Manager):
    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))

        accepted = set([])

        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)

        available = [profile for profile in profiles if profile not in accepted]

        return available

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles

    def get_all_buddies(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))

        accepted = set([])

        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)

        available = [profile for profile in profiles if profile in accepted]

        return available


class Profile(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True, max_length=1000)
    location = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(blank=True, null=True, default='profile_pics/default.png', upload_to='profile_pics')
    buddies = models.ManyToManyField(User, blank=True, related_name='buddies')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    def __str__(self):
        return f'{self.user.username}'

    def get_buddies(self):
        return self.buddies.all()

    def get_buddies_num(self):
        return self.buddies.all().count()

    def get_all_authors_posts(self):
        return self.posts.all()

    def get_posts_num(self):
        return self.posts.all().count()

    def get_high_fives_given_num(self):
        high_fives = self.highfive_set.all()
        total_high_fived = 0

        for item in high_fives:
            if item.value == 'High Five':
                total_high_fived += 1
        return total_high_fived

    def get_high_fives_received_num(self):
        posts = self.posts.all()
        total_high_fived = 0

        for item in posts:
            total_high_fived += item.high_fived.all().count()
        return total_high_fived

    def get_unread_messages_num(self):
        return self.messages.filter(unread=True).count()

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        return '/media/profile_pics/default.png'

    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name

    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug

        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug == '':
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + ' ' + str(self.last_name))
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + ' ' + str(get_random_code()))
                    ex = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)

        self.slug = to_slug
        super().save(*args, **kwargs)


STATUS_CHOICES = (
    ('sent', 'sent'),
    ('accepted', 'accepted')
)


class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='sent')
        return qs

    def invitations_sent(self, sender):
        qs = Relationship.objects.filter(sender=sender, status='sent')
        return qs


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return f'{self.sender}-{self.receiver}-{self.status}'


class Message(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='messages_from', default=None)
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    unread = models.BooleanField(default=True)

    @property
    def short_content(self):
        return truncatechars(self.message, 35)

    def __str__(self):
        return f'{self.sender}-{self.short_content}'