from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("register/index/", views.process, name='index'),
    path("account/", views.test, name='account'),
    path("register/", views.register, name='register' ),
    path("account/points_board", views.points, name='points_board'),
    path("account/attribue_points", views.create_transaction, name='gv_points'),
    path("account/my_points", views.my_points, name='my_points'),
    path("account/requisicoes", views.requisicoes, name='requetss')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
