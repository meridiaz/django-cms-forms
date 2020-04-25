from django.urls import path

from . import views

urlpatterns = [
    path('new/', views.cms_new, name='cms_new'), #ponemos name= para poder llamarla desde el template
    path('new/<str:llave>', views.comentario_new, name='comentario_new'),
    path('', views.index),
    path('imagen', views.imagen),
    path('loggedIn', views.loggedIn),
    path('logout', views.logout_view),
    path('<str:llave>', views.get_content, name="get_content"),
    path('modify/<str:llave>', views.cms_modify, name="cms_modify"),
    path('modify/<str:llave>/<str:titulo_comen>', views.comentario_modify, name="comentario_modify"),
]
