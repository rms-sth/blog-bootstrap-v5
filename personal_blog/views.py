from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView

from personal_blog.forms import PostForm
from personal_blog.models import Post


class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(published_at__lte=timezone.now()).order_by(
        "-published_at"
    )


class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"


class DraftListView(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(published_at__isnull=True).order_by("-published_at")


class PostCreateView(CreateView):
    form_class = PostForm
    template_name = "post_create.html"
    success_url = reverse_lazy("drafts")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect("post-list")


# class PostUpdateView(UpdateView):
#     model = Post
#     form_class = PostForm
#     template_name = "post_create.html"
#     success_url = reverse_lazy("post-list")


class PostPublishView(View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        post.published_at = timezone.now()
        post.save()
        return redirect("post-list")


class PostUpdateView(View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(instance=post)
        return render(
            request,
            "post_create.html",
            {"form": form},
        )

    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post-detail", pk=post.pk)
