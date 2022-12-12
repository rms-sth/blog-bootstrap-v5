from django.urls import path
from personal_blog import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post-list"),
    path("drafts/", views.DraftListView.as_view(), name="drafts"),
    path("post-detail/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post-create/", views.PostCreateView.as_view(), name="post-create"),
    path("post-delete/<int:pk>/", views.PostDeleteView.as_view(), name="post-delete"),
    path("post-update/<int:pk>/", views.PostUpdateView.as_view(), name="post-update"),
    path("post-publish/<int:pk>/", views.PostPublishView.as_view(), name="post-publish"),
]
