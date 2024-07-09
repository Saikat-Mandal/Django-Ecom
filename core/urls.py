
from django.contrib import admin
from django.urls import path

admin.site.site_header = 'Storefront admin dashboard'
admin.site.index_title = 'Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
]
