
from django.urls import path
import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.basket, name="view"),
    path('add/<int:pk>/', basketapp.basket_add, name="add"),
    # path('delete/<int:pk>/', basketapp.basket_delete(), name="basket_delete"),
    path('remove/<int:pk>/', basketapp.basket_remove, name="remove"),
    path('remove/ajax/<int:pk>/', basketapp.basket_remove_ajax, name="remove_ajax"),
    path('edit/<int:pk>/<int:quantity>/', basketapp.basket_edit, name='edit')
]

