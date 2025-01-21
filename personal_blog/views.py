from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from personal_blog.forms import PostForm
from personal_blog.models import Post


class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(published_at__isnull=False).order_by("-published_at")
    # queryset = Post.objects.filter(published_at__lte=timezone.now()).order_by(
    #     "-published_at"
    # )


class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        queryset = (
            get_object_or_404(Post, id=self.kwargs["pk"])
            .filter(pk=self.kwargs["pk"], published_at__isnull=False)
            .order_by("-published_at")
        )
        return queryset


class DraftListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(published_at__isnull=True).order_by("-published_at")


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = "post_create.html"
    success_url = reverse_lazy("drafts")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post was created successfully.")
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    # success_url = reverse_lazy("post-list")

    def form_valid(self, form):
        messages.success(self.request, "Post was deleted successfully.")
        return super().form_valid(form)
    
    def get_success_url(self):
        post = self.get_object()
        if post.published_at:
            return reverse_lazy("post-list")
        else:
            return reverse_lazy("draft-list")


# class PostDeleteView(View):
#     def get(self, request, pk, *args, **kwargs):
#         post = get_object_or_404(Post, pk=pk)
#         post.delete()
#         return redirect("post-list")


class PostPublishView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        post.published_at = timezone.now()
        post.save()
        return redirect("post-list")


# class PostUpdateView(LoginRequiredMixin, UpdateView):
#     model = Post
#     form_class = PostForm
#     template_name = "post_create.html"
#     success_url = reverse_lazy("post-list")


class PostUpdateView(LoginRequiredMixin, View):
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
            messages.success(self.request, "Post was updated successfully.")
            return redirect("post-detail", pk=post.pk)
        else:
            messages.error(self.request, "Post was not updated successfully.")
            return render(
                request,
                "post_create.html",
                {"form": form},
            )
