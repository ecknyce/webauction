from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createListing, name="create"),
    path("displaycategory", views.displaycategory, name="displaycategory"),
    path("list-detail/<int:id>", views.listing_detail, name="list_detail"),
    path("removeWatchList/<int:id>", views.removeWatchlist, name="removeWatchlist"),
    path("addWatchList/<int:id>", views.addWatchlist, name="addWatchlist"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("WatchList", views.displayWatchList, name="watchlist"),
    path("new-comment/<int:id>", views.addComment, name="addComment"),
    path("close-auction/<int:id>", views.closeAuction, name="closeAuction"),
]
