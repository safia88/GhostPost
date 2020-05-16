"""ghost URL Configuration

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
from ghost.models import Post
from ghost import views
admin.site.register(Post)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="homepage"),
    path('add_post/', views.add_post, name='addPost'),
    path('upvote/<int:id>/', views.up_votes, name='up_votes'),
    path('downvote/<int:id>/', views.down_votes, name='down_votes'),
    path('boasts/', views.boast, name='boast'),
    path('roasts/', views.roast, name='roast'),
    path('sorted/', views.sorted_posts),
    path('delete/<int:id>/', views.delete_post)
]
