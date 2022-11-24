from django.urls import path

from .views import PostListView, PostDetailView

urlpatterns = [
    path('', PostListView.as_view(), name='postlist_view'),
    path('<slug:slug>', PostDetailView.as_view(), name='postdetail_view'),
]