from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DeleteView, View, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import PostModelForm, CommentModelForm, PostUpdateForm
from .models import Post, HighFive, Category, Comment
from users.models import Profile


@login_required
def post_create_and_list_view(request):
    posts = Post.objects.all()
    profile = Profile.objects.get(user=request.user)
    pic = profile.get_avatar
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 5)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    p_form = PostModelForm(request.POST or None, request.FILES or None)
    if request.is_ajax():
        if p_form.is_valid():
            p_form.save()
            return JsonResponse({'message': 'works'})

    p_form = PostModelForm()
    post_added = False

    if 'submit_p_form' in request.POST:
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()
            post_added = True

    context = {
        'posts': posts,
        'profile': profile,
        'p_form': p_form,
        'post_added': post_added,
        'pic': pic,
    }

    return render(request, 'posts/index.html', context)


@login_required
def comment_view(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            print(instance)
            return JsonResponse({'comment': model_to_dict(instance)}, status=200)

    return redirect('posts:index')


@login_required
def high_five_take_back_post(request):
    user = request.user

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.high_fived.all():
            post_obj.high_fived.remove(profile)
        else:
            post_obj.high_fived.add(profile)

        high_five, created = HighFive.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if high_five.value == 'High Five':
                high_five.value = 'Take Back'
            else:
                high_five.value = 'High Five'
        else:
            high_five.value = 'High Five'

            post_obj.save()
            high_five.save()

        data = {
            'value': high_five.value,
            'high_fives': post_obj.high_fived.all().count()
        }

        return JsonResponse(data, safe=False)

    return redirect('posts:index')


class CategoryList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'categories/category_list.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context


class CategoryDetail(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'categories/category_detail.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Post.objects.filter(category=self.category).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        context['category'] = self.category
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context


class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'posts/post_update.html'
    form_class = PostUpdateForm

    def get_success_url(self):
        return reverse('posts:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if self.request.is_ajax():
            form.save()
            return JsonResponse({'message': 'works'})

        form.instance.author.user = self.request.user
        return super(UpdatePostView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.author.user != request.user:
            return HttpResponseRedirect('/')

        return super(UpdatePostView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UpdatePostView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    template_name = 'posts/post_detail.html'
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.author.user != request.user:
            return HttpResponseRedirect('/')

        return super(PostDetailView, self).get(request, *args, **kwargs)


class DeletePost(LoginRequiredMixin, View):
    def post(self, request, id):
        post = Post.objects.get(id=id)
        post.delete()
        return JsonResponse({'result': 'ok'}, status=200)


class DeleteComment(LoginRequiredMixin, View):
    def post(self, request, id):
        comment = Comment.objects.get(id=id)
        comment.delete()
        return JsonResponse({'result': 'ok'}, status=200)


class SearchView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/search.html'
    context_object_name = 'posts'
    # paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            return Post.objects.filter(Q(content__icontains=query)|
                                       Q(category__title__icontains=query)).order_by('created', 'id').distinct()

        return Post.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context


class Acknowledgements(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/acknowledgements.html'

    def get_context_data(self, **kwargs):
        context = super(Acknowledgements, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context

