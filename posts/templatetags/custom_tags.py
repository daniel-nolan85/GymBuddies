from django import template

from posts.forms import CommentModelForm, PostModelForm, PostUpdateForm
from posts.models import Category
from users.forms import ProfileUpdateForm
from users.models import Profile

register = template.Library()


@register.simple_tag(name='categories')
def all_categories():
    return Category.objects.all()


@register.inclusion_tag('posts/comment_form.html')
def comment_tag():
    c_form = CommentModelForm()

    return {'c_form': c_form}


# @register.inclusion_tag('posts/update.html')
# def update_tag():
#     u_form = PostUpdateForm()
#
#     return {'u_form': u_form}


@register.inclusion_tag('users/update.html', takes_context=True)
def update_profile_tag(context):
    request = context['request']
    profile = Profile.objects.get(user=request.user)
    up_form = ProfileUpdateForm(request.POST or None, instance=profile)

    return {'up_form': up_form}