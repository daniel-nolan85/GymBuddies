from django.urls import path

from .views import *


app_name = 'posts'

urlpatterns = [
    path('', post_create_and_list_view, name='index'),
    path('update/<int:pk>/', UpdatePostView.as_view(), name='update'),
    path('detail/<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('comment/', comment_view, name='comment'),
    path('high-fived/', high_five_take_back_post, name='high_fived'),
    path('category-list/', CategoryList.as_view(), name='category_list'),
    path('category/<int:pk>/<slug:slug>', CategoryDetail.as_view(), name='category_detail'),
    path('delete-post/<str:id>', DeletePost.as_view(), name='delete_post'),
    path('delete-comment/<str:id>', DeleteComment.as_view(), name='delete_comment'),
    path('search/', SearchView.as_view(), name='search'),
    path('acknowledgements/', Acknowledgements.as_view(), name='acknowledgements'),
]