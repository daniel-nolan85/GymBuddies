from django.urls import path
from django.views.decorators.http import require_POST

from .views import *


app_name = 'tracker'

urlpatterns = [

    path('', AreaList.as_view(), name='areas'),
    path('area-delete/<str:id>', AreaDelete.as_view(), name='area_delete'),
    path('area/<int:pk>/detail/', ExerciseList.as_view(), name='exercises'),
    path('exercise-add-new/<int:area_id>/', ExerciseFormView.as_view(), name='exercise_add_new'),
    path('exercise-delete/<str:id>', ExerciseDelete.as_view(), name='exercise_delete'),
    path('exercise/<int:pk>/workout/', WorkoutView.as_view(), name='workout'),
    path('exercise/<int:pk>/weight-rep/', WeightRepFormView.as_view(), name='weight_rep'),
    path('exercise/<int:pk>/weight-dist/', WeightDistFormView.as_view(), name='weight_dist'),
    path('exercise/<int:pk>/weight-time/', WeightTimeFormView.as_view(), name='weight_time'),
    path('exercise/<int:pk>/rep-dist/', RepDistFormView.as_view(), name='rep_dist'),
    path('exercise/<int:pk>/rep-time/', RepTimeFormView.as_view(), name='rep_time'),
    path('exercise/<int:pk>/distance-time/', DistanceTimeFormView.as_view(), name='distance_time'),
    path('exercise/<int:pk>/weight/', WeightFormView.as_view(), name='weight'),
    path('exercise/<int:pk>/rep/', RepFormView.as_view(), name='rep'),
    path('exercise/<int:pk>/dist/', DistFormView.as_view(), name='dist'),
    path('exercise/<int:pk>/time/', TimeFormView.as_view(), name='time'),
    path('exercise/<int:pk>/weight-dist-time/', WeightDistanceTimeFormView.as_view(), name='weight-dist-time'),
    path('workout-delete/<str:id>', WorkoutDeleteView.as_view(), name='workout_delete'),
]

