from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),  # Home page
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('book/', views.BookListView.as_view(), name='book'),
    # path('book/<int:book_id>/', views.BookDetailView.as_view(), name='book_detail'),
    path('category/<int:category_id>/', views.CategoryView.as_view(), name='category'),
    path("cart/<int:user>/", views.CartView.as_view(), name="cart"),
    path("payment/<int:user>/", views.PaymentView.as_view(), name="payment"),
    path("orderhistory/<int:user>/", views.OrderHistoryView.as_view(), name="order_history_user"),
    path("orderhistory/<int:user>/<int:order>/", views.OrderHistoryDetailView.as_view(), name="order_history_detail"),
    #path("orderhistoryowner/", views.OrderHistoryOwnerView.as_view(), name="order_history_owner"),
    #path("orderhistoryowner/<int:order>/", views.OrderHistoryOwnerDetailView.as_view(), name="order_history_owner_detail"),
    path('managebooks/', views.ManageBookView.as_view(), name='manage_book'),
]
