"""readit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls.static import static 
from django.conf import settings 
from django.contrib.auth.decorators import login_required
from  books.views import ( EditorDetail, EditorList, ReviewList, CreateAuthor, list_books, review_book )
from books.views import sign_in_view, sign_out_view, login_view, contact_view, about_view, book_detail_view, comment_view, home_view
urlpatterns = [
    # Auth
    path('logout/', sign_out_view, name='logout'),
    path('sign-in/', sign_in_view, name="sign-in"),
    path('login/', login_view, name='login'),
 
    # Admin
    path('admin/', admin.site.urls),
    
    # Custom
    #path('', home_view, name='home'),
    path('', list_books, name='books'),
    path('editors/', EditorList.as_view(), name='editors'),
    path('posts/<slug:slug>/', book_detail_view, name='book-detail'),
    path('authors/add/', login_required(CreateAuthor.as_view()), name='add-author'),
    path('editors/<slug:slug>/', EditorDetail.as_view(), name='editor-detail'),
    path('review/', login_required(ReviewList.as_view()), name='review-books'),
    path('review/<slug:slug>/', review_book, name='review-book'),
    path('comment/<slug:slug>/', comment_view, name="comment"),

    path('contact/', contact_view, name="contact"),
    path('about/', about_view, name="about"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
