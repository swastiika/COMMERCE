from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/",views.createListing,name="create"),
    path("create_category/",views.createCategory,name="category"),
    path("display/",views.displaycat,name="displaycategory"),
    path("listing/<int:id>",views.listing,name="listing"),
    path("removewatchlist<int:id>",views.removewatchlist,name="removewatchlist"),
    path("addwatchlist/<int:id>",views.addwatchlist,name="addwatchlist"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("addcomment/<int:id>",views.addcomment,name="addcomment")
]
