from django.db import models
from django.template.defaultfilters import slugify

from users.models import Profile


class Type(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Type, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(editable=False)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Exercise, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)


class Area(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(default='slug', editable=False)
    exercise = models.ManyToManyField(Exercise, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Area, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)


WEIGHT_CHOICES = (
    ('lb', 'lb'),
    ('kg', 'kg')
)


DISTANCE_CHOICES = (
    ('ft', 'ft'),
    ('m', 'm'),
    ('mi', 'mi'),
    ('km', 'km')
)


class Workout(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    weight = models.DecimalField(default=0.0, max_digits=5, decimal_places=1)
    pref_weight = models.CharField(max_length=2, choices=WEIGHT_CHOICES, default='kg')
    reps = models.PositiveIntegerField(default=0)
    distance = models.PositiveIntegerField(default=0)
    pref_dist = models.CharField(max_length=2, choices=DISTANCE_CHOICES, default='m')
    time = models.DurationField(default=0)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.exercise.name

    class Meta:
        ordering = ('created',)
