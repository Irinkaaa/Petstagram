from django.urls import path

from Petstagram.pets.views import pets_list, pets_details_or_comment, pets_like, pets_edit, pets_delete, pets_create

urlpatterns = [
    path('', pets_list, name='pet list'),
    path('details/<int:pk>/', pets_details_or_comment, name='pet details or comment'),
    path('like/<int:pk>/', pets_like, name='like pet'),
    path('edit/<int:pk>/', pets_edit, name='edit pet'),
    path('delete/<int:pk>/', pets_delete, name='delete pet'),
    path('create/', pets_create, name='create pet'),
]
