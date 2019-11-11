from django.urls import path

from phone_book import views

app_name = 'phone_book'

urlpatterns = [
    path('', views.PersonListView.as_view(), name='contacts'),
    path('add/contact/', views.PersonCreateView.as_view(), name='add-contact'),
    path('edit/contact/<int:pk>/', views.PersonUpdateView.as_view(), name='edit-contact'),
    path('delete/contact/<int:pk>/', views.delete_person, name='delete-contact'),
    path('add-phone/contact/<int:pk>/', views.create_phone, name='add-phone'),
    path('add-email/contact/<int:pk>/', views.create_email, name='add-email'),
    path('search/', views.PersonSearch.as_view(), name='search'),
]
