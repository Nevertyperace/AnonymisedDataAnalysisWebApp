from django.urls import path
from . import views

#set up urls, refer to views.py (controller)
urlpatterns = [
    path('', views.index_view, name='index_view'),
    path('index', views.index_view, name='index_view'),
    path('data/raw', views.raw_view, name='raw_view'),
    path('data/<slug:slug>', views.DepthView.as_view(), name='depth_view'),
    path('charts/all', views.ChartsAllView.as_view(), name="charts_all"),
    path('charts/<slug:slug>', views.ChartsView.as_view(), name="charts_view"),
]