from django.core.validators import FileExtensionValidator
from django.db import models
from django.template.defaultfilters import truncatechars, slugify

from users.models import Profile


class Category(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(editable=False)
    image = models.ImageField(upload_to='cat-img', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], default='profile_pics/default.png',)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def post_count(self):
        return self.posts.all().count()

    class Meta:
        ordering = ('title',)


class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='uploads', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    video = models.FileField(upload_to='videos', blank=True)
    high_fived = models.ManyToManyField(Profile, blank=True, related_name='high_fives')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, related_name='posts')

    @property
    def short_content(self):
        return truncatechars(self.content, 35)

    def __str__(self):
        return self.short_content

    def high_fives_num(self):
        return self.high_fived.all().count()

    def comments_num(self):
        return self.comment_set.all().count()

    class Meta:
        ordering = ('-created',)


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return str(self.post.short_content)
        return str(self.user)


HIGH_FIVE_CHOICES = (
    ('High Five', 'High Five'),
    ('Take Back', 'Take Back'),
)


class HighFive(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=HIGH_FIVE_CHOICES, max_length=9)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}-{self.post}-{self.value}'