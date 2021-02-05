from django import forms

from durationwidget.widgets import TimeDurationWidget

from .models import Area, Exercise, Workout


# Add an Area
class AreaForm(forms.ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Area', 'class': 'form-control'}))

    class Meta:
        model = Area
        fields = ['name']


# Add an Exercise
class ExerciseForm(forms.ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Exercise', 'class': 'form-control'}))

    class Meta:
        model = Exercise
        fields = ['name', 'type']
        widgets = {'type': forms.Select(attrs={'class': 'form-control'})}


# Weight & Reps
class WeightRepsModelForm(forms.ModelForm):
    time = forms.DurationField(widget=TimeDurationWidget(show_days=False, show_hours=False, show_minutes=False, show_seconds=False), required=False)
    weight = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Weight', 'class': 'form-control', 'step': 2.5}))
    reps = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Reps', 'class': 'form-control'}))

    class Meta:
        model = Workout
        fields = ['weight', 'pref_weight', 'reps', 'time']
        widgets = {'pref_weight': forms.Select(attrs={'class': 'form-control'})}


# Weight & Distance
class WeightDistanceModelForm(forms.ModelForm):
    time = forms.DurationField(widget=TimeDurationWidget(show_days=False, show_hours=False, show_minutes=False, show_seconds=False), required=False)
    weight = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Weight', 'class': 'form-control', 'step': 2.5}))
    distance = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Distance', 'class': 'form-control'}))

    class Meta:
        model = Workout
        fields = ['weight', 'pref_weight', 'distance', 'pref_dist', 'time']
        widgets = {
            'pref_weight': forms.Select(attrs={'class': 'form-control'}),
            'pref_dist': forms.Select(attrs={'class': 'form-control'}),
        }


# Weight & Time
class WeightTimeModelForm(forms.ModelForm):
    time = forms.DurationField(widget=TimeDurationWidget(attrs={'class': 'form-control', 'style': 'display: inline-block'}, show_days=False, show_hours=True, show_minutes=True, show_seconds=True), required=False)
    weight = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Weight', 'class': 'form-control', 'step': 2.5}))

    class Meta:
        model = Workout
        fields = ['weight', 'pref_weight', 'time']
        widgets = {'pref_weight': forms.Select(attrs={'class': 'form-control'})}


# Reps & Distance
class RepsDistanceModelForm(forms.ModelForm):
    time = forms.DurationField(widget=TimeDurationWidget(show_days=False, show_hours=False, show_minutes=False, show_seconds=False), required=False)
    reps = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Reps', 'class': 'form-control'}))
    distance = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Distance', 'class': 'form-control'}))

    class Meta:
        model = Workout
        fields = ['reps', 'distance', 'pref_dist', 'time']
        widgets = {'pref_dist': forms.Select(attrs={'class': 'form-control'})}


# Reps & Time
class RepsTimeModelForm(forms.ModelForm):
    time = forms.DurationField(widget=TimeDurationWidget(attrs={'class': 'form-control', 'style': 'display: inline-block'}, show_days=False, show_hours=True, show_minutes=True, show_seconds=True), required=False)
    reps = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Reps', 'class': 'form-control'}))

    class Meta:
        model = Workout
        fields = ['reps', 'time']


# Distance & Time
class DistanceTimeModelForm(forms.ModelForm):
    time = forms.DurationField(widget=TimeDurationWidget(attrs={'class': 'form-control', 'style': 'display: inline-block'}, show_days=False, show_hours=True, show_minutes=True, show_seconds=True), required=False)
    distance = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Distance', 'class': 'form-control'}))

    class Meta:
        model = Workout
        fields = ['distance', 'pref_dist', 'time']
        widgets = {'pref_dist': forms.Select(attrs={'class': 'form-control'})}


# Weight
class WeightModelForm(forms.ModelForm):
    time = forms.DurationField(widget=TimeDurationWidget(show_days=False, show_hours=False, show_minutes=False, show_seconds=False), required=False)
    weight = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Weight', 'class': 'form-control', 'step': 2.5}))

    class Meta:
        model = Workout
        fields = ['weight', 'pref_weight', 'time']
        widgets = {'pref_weight': forms.Select(attrs={'class': 'form-control'})}


# Reps
class RepsModelForm(forms.ModelForm):
    time = forms.DurationField(widget=TimeDurationWidget(show_days=False, show_hours=False, show_minutes=False, show_seconds=False), required=False)
    reps = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Reps', 'class': 'form-control'}))

    class Meta:
        model = Workout
        fields = ['reps', 'time']


# Distance
class DistanceModelForm(forms.ModelForm):
    time = forms.DurationField(widget=TimeDurationWidget(show_days=False, show_hours=False, show_minutes=False, show_seconds=False), required=False)
    distance = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Distance', 'class': 'form-control'}))

    class Meta:
        model = Workout
        fields = ['distance', 'pref_dist', 'time']
        widgets = {'pref_dist': forms.Select(attrs={'class': 'form-control'})}


# Time
class TimeModelForm(forms.ModelForm):
    time = forms.DurationField(widget=TimeDurationWidget(attrs={'class': 'form-control', 'style': 'display: inline-block'}, show_days=False, show_hours=True, show_minutes=True, show_seconds=True), required=False)

    class Meta:
        model = Workout
        fields = ['time']


# Weight, Distance & Time
class WeightDistanceTimeModelForm(forms.ModelForm):
    time = forms.DurationField(widget=TimeDurationWidget(attrs={'class': 'form-control', 'style': 'display: inline-block'}, show_days=False, show_hours=True, show_minutes=True, show_seconds=True), required=False)
    weight = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Weight', 'class': 'form-control', 'step': 2.5}))
    distance = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Distance', 'class': 'form-control'}))

    class Meta:
        model = Workout
        fields = ['weight', 'pref_weight', 'distance', 'pref_dist', 'time']
        widgets = {
            'pref_weight': forms.Select(attrs={'class': 'form-control'}),
            'pref_dist': forms.Select(attrs={'class': 'form-control'}),
        }