from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search",views.search, name="search"),
    path("newpage",views.NewPage,name="NewPage"),
    path("edit",views.edit,name="edit"),
    path("randompage",views.randompage,name="randompage"),
    path("<str:entrypage>", views.entrypage , name="entry page")
    
]
