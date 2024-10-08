from django.urls import path

from notes import views as note_views

app_name = 'notes'
urlpatterns = [
    path('', note_views.HomeView.as_view(), name="home"),
    path('add/', note_views.AddView.as_view(), name="add"),
    path('edit/<int:note_id>/',
         note_views.EditView.as_view(),
         name="edit"),
    path('tags/', note_views.TagsView.as_view(), name="tags"),
    path('tag/<tag_slug>', note_views.TagView.as_view(), name="tag_view"),
    path('search/', note_views.SearchView.as_view(), name="search"),
    path('fav/', note_views.FavouritesView.as_view(), name="favs"),
]
