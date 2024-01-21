

# myapp/urls.py

from django.urls import path
from .views import view_home, insert_data,view_data
print("hell")

urlpatterns = [
    path('', view_home, name='viewhome'),
    path('insert', insert_data, name='insertdata'),
    path('view', view_data, name='viewdata'),
]
