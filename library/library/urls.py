"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from catalog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('', RedirectView.as_view(url='/catalog/', permanent=True)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#for login, logout, password management
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

#for api
app_name = "library"
urlpatterns += [
    path('api/authors/', views.AuthorsView.as_view()), # authors list
    path('api/author/<int:pk>', views.AuthorView.as_view()), # detailed information about the author
    path('api/author_books/<int:pk>', views.AuthorBooksView.as_view()), # author book list
    path('api/books/', views.BooksView.as_view()), # book list
    path('api/book/<int:pk>', views.BookView.as_view()), # detailed information about the book
    path('api/books_copy/', views.BooksList.as_view()), # filtered list of books (by year and by title)
]
