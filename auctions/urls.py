from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create',views.create,name="create"),
    path("listing/<int:id>",views.listing,name="listing"),
    path("addwatchlist/<int:id>",views.addwatchlist,name="addwatchlist"),
    path("removewathclist/<int:id>",views.removewatchlist,name="removewatchlist"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("placebid/<int:id>",views.placebid,name="placebid"),
    path("closebid<int:id>",views.closebid,name="closebid"),
    path("closeview",views.closeview,name="closeview"),
    path("addcomment<int:id>",views.addcomment,name="addcomment")

]
