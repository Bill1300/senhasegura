from django.contrib import admin
from django.urls import path
from .views import home, save, edit, update, delete, docs, structure

urlpatterns = [
    path('', home),
    path('save/', save, name="save"),
    path('edit/<int:id>', edit, name="edit"),
    path('update/<int:id>', update, name="update"),
    path('delete/<int:id>', delete, name="delete"),
    path('docs/', docs, name="docs"),
    path('structure/', structure, name="structure"),
]

