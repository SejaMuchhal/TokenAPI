from django.urls import include, path
from . import views


urlpatterns = [
    path('unblock_token', views.UnblockToken, name = "unblock_token"),
    path('keep_token_alive', views.IsAlive, name = "keep_token_alive"),
    path('assign_token', views.AssignToken, name = "assign_token"),
    path('create_token', views.CreateToken,name="create_token"),
]
