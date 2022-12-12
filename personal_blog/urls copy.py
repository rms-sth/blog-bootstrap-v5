from django.urls import path
from personal_blog import views

urlpatterns = [
    path("", views.post_list, name="post-list"),
    path("drafts/", views.post_draft_list, name="drafts"),
    path("post-detail/<int:pk>/", views.post_detail, name="post-detail"),
    path("post-create/", views.post_create, name="post-create"),
    path("post-delete/<int:pk>/", views.post_delete, name="post-delete"),
    path("post-update/<int:pk>/", views.post_update, name="post-update"),
    path("post-publish/<int:pk>/", views.post_publish, name="post-publish"),
]
