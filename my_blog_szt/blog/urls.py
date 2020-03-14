from . import views
from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view(), name='list'),
    path('blog/<slug:slug>/', views.post_detail, name='post_detail'),
    path('blog/user_posts', views.UserPostList.as_view(), name='user_posts'),
    #url(r'^(?P<slug>[\w-]+)/$', views.post_detail, name="post_detail"),
    path('blog/contact_us', views.contact,  name='contact_us'),
    path('blog/success', views.successView, name='success'),
    #path('blog/about_us', views.about, name='about'),
    path('blog/create', views.post_create, name="create_post"),
    path('blog/comment', views.post_create, name="comment"),
    path('blog/<slug:slug>/update', views.PostUpdate.as_view(), name='post_update'),

    path('restapi/', include(router.urls)),
    path('blog/restapi/api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] 
