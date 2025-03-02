'''URL приложения'''
from django.urls import path
from app.views import IndexView, PostDetailView


app_name = 'posts'

urlpatterns = [
    path('', IndexView.as_view(), name='index_view'),
    path(
        '<slug:slug>',
        PostDetailView.as_view(),
        name='detail_view'
    ),
]
