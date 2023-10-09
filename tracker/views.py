from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, View
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max

from .forms import *

from .forms import (
    AreaForm,
    ExerciseForm as e_form,

    WeightRepsModelForm as wr_form,
    WeightDistanceModelForm as wd_form,
    WeightTimeModelForm as wt_form,
    RepsDistanceModelForm as rd_form,
    RepsTimeModelForm as rt_form,
    DistanceTimeModelForm as dt_form,
    WeightModelForm as w_form,
    RepsModelForm as r_form,
    DistanceModelForm as d_form,
    TimeModelForm as t_form,
    WeightDistanceTimeModelForm as wdt_form
)

from .models import Area, Exercise, Workout
from posts.models import Profile


class AreaList(LoginRequiredMixin, View):
    def get(self, request):
        form = AreaForm()
        areas = Area.objects.all()
        profile = Profile.objects.get(user=request.user)
        return render(request, 'tracker/areas.html', context={'form': form, 'areas': areas, 'profile': profile})

    def post(self, request):
        form = AreaForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = Profile.objects.get(user=request.user)
            instance.save()
            return JsonResponse({'area': model_to_dict(instance)}, status=200)
        else:
            return redirect('tracker:areas')


class AreaDelete(LoginRequiredMixin, View):
    def post(self, request, id):
        area = Area.objects.get(id=id)
        area.delete()
        return JsonResponse({'result': 'ok'}, status=200)


class ExerciseList(LoginRequiredMixin, DetailView):
    model = Area
    template_name = 'tracker/exercises.html'

    def get_context_data(self, **kwargs):

        context = super(ExerciseList, self).get_context_data(**kwargs)
        context['e_form'] = ExerciseForm
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context


class ExerciseFormView(LoginRequiredMixin, CreateView):
    form_class = e_form
    success_url = '/'

    def form_valid(self, form):
        form.save()
        area = Area.objects.get(pk=self.kwargs["area_id"])
        new_ex = Exercise.objects.latest('id')
        new_ex.user = self.request.user
        area.exercise.add(new_ex)
        return JsonResponse({'exercise': model_to_dict(new_ex)}, status=200)


class ExerciseDelete(LoginRequiredMixin, View):
    def post(self, request, id):
        exercise = Exercise.objects.get(id=id)
        exercise.delete()
        return JsonResponse({'result': 'ok'}, status=200)


class WorkoutView(LoginRequiredMixin, DetailView):
    model = Exercise
    template_name = 'tracker/workouts.html'

    def get_context_data(self, **kwargs):
        context = super(WorkoutView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['workout'] = Workout.objects.all()
        context['m_weight'] = Exercise.objects.filter(workout__user=Profile.objects.get(user=self.request.user)).annotate(max_weight=Max('workout__weight'))
        context['wr_form'] = wr_form
        context['wd_form'] = wd_form
        context['wt_form'] = wt_form
        context['rd_form'] = rd_form
        context['rt_form'] = rt_form
        context['dt_form'] = dt_form
        context['w_form'] = w_form
        context['r_form'] = r_form
        context['d_form'] = d_form
        context['t_form'] = t_form
        context['wdt_form'] = wdt_form
        return context


# Weight & Reps
class WeightRepFormView(LoginRequiredMixin, CreateView):
    form_class = wr_form

    def form_valid(self, form):
        form.instance.exercise_id = self.kwargs['pk']
        form.instance.user = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracker:workout', kwargs={'pk': self.kwargs['pk']})


# Weight & Distance
class WeightDistFormView(LoginRequiredMixin, CreateView):
    form_class = wd_form

    def form_valid(self, form):
        form.instance.exercise_id = self.kwargs['pk']
        form.instance.user = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracker:workout', kwargs={'pk': self.kwargs['pk']})


# Weight & Time
class WeightTimeFormView(LoginRequiredMixin, CreateView):
    form_class = wt_form

    def form_valid(self, form):
        form.instance.exercise_id = self.kwargs['pk']
        form.instance.user = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracker:workout', kwargs={'pk': self.kwargs['pk']})


# Reps & Distance
class RepDistFormView(LoginRequiredMixin, CreateView):
    form_class = rd_form

    def form_valid(self, form):
        form.instance.exercise_id = self.kwargs['pk']
        form.instance.user = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracker:workout', kwargs={'pk': self.kwargs['pk']})


# Reps & Time
class RepTimeFormView(LoginRequiredMixin, CreateView):
    form_class = rt_form

    def form_valid(self, form):
        form.instance.exercise_id = self.kwargs['pk']
        form.instance.user = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracker:workout', kwargs={'pk': self.kwargs['pk']})


# Distance & Time
class DistanceTimeFormView(LoginRequiredMixin, CreateView):
    form_class = dt_form

    def form_valid(self, form):
        form.instance.exercise_id = self.kwargs['pk']
        form.instance.user = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracker:workout', kwargs={'pk': self.kwargs['pk']})


# Weight
class WeightFormView(LoginRequiredMixin, CreateView):
    form_class = w_form

    def form_valid(self, form):
        form.instance.exercise_id = self.kwargs['pk']
        form.instance.user = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracker:workout', kwargs={'pk': self.kwargs['pk']})


# Reps
class RepFormView(LoginRequiredMixin, CreateView):
    form_class = r_form

    def form_valid(self, form):
        form.instance.exercise_id = self.kwargs['pk']
        form.instance.user = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracker:workout', kwargs={'pk': self.kwargs['pk']})


# Distance
class DistFormView(LoginRequiredMixin, CreateView):
    form_class = d_form

    def form_valid(self, form):
        form.instance.exercise_id = self.kwargs['pk']
        form.instance.user = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracker:workout', kwargs={'pk': self.kwargs['pk']})


# Time
class TimeFormView(LoginRequiredMixin, CreateView):
    form_class = t_form

    def form_valid(self, form):
        form.instance.exercise_id = self.kwargs['pk']
        form.instance.user = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracker:workout', kwargs={'pk': self.kwargs['pk']})


# Weight, Distance & Time
class WeightDistanceTimeFormView(LoginRequiredMixin, CreateView):
    form_class = wdt_form

    def form_valid(self, form):
        form.instance.exercise_id = self.kwargs['pk']
        form.instance.user = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracker:workout', kwargs={'pk': self.kwargs['pk']})


class WorkoutDeleteView(LoginRequiredMixin, View):
    def post(self, request, id):
        workout = Workout.objects.get(id=id)
        workout.delete()
        return JsonResponse({'result': 'ok'}, status=200)
