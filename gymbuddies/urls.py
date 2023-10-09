from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from users.views import CustomPasswordChangeView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/password/change/', CustomPasswordChangeView.as_view(), name="account_change_password"),
    path('accounts/', include('allauth.urls')),
    path('', include('posts.urls', namespace='posts')),
    path('users/', include('users.urls', namespace='users')),
    path('tracker/', include('tracker.urls', namespace='tracker')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)