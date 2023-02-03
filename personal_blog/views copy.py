from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from personal_blog.forms import PostForm
from personal_blog.models import Post


def post_list(request):
    posts = Post.objects.filter(published_at__isnull=False).order_by("-published_at")
    # posts = Post.objects.filter(published_at__lte=timezone.now()).order_by(
    #     "-published_at"
    # )
    return render(
        request,
        "post_list.html",
        {"posts": posts},
    )


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(
        request,
        "post_detail.html",
        {"post": post},
    )


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_at__isnull=True).order_by("-published_at")
    return render(
        request,
        "post_list.html",
        {"posts": posts},
    )


@login_required
def post_create(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("drafts")
    return render(
        request,
        "post_create.html",
        {"form": form},
    )


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect("post-list")


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(instance=post)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post-detail", pk=post.pk)

    return render(
        request,
        "post_create.html",
        {"form": form},
    )


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.published_at = timezone.now()
    post.save()
    return redirect("post-list")
