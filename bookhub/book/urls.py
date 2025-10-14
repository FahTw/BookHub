from django.urls import path

from book.views import *

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('home/', HomeView.as_view(), name='home'), # Home page
    path('profile/', ProfileView.as_view(), name='profile'),
    path('book/', BookListView.as_view(), name='book'),
    path('book/<int:book_id>/', BookDetailView.as_view(), name='book_detail'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='category'),
    path("cart/<int:user>/", CartView.as_view(), name="cart"),
    path('add_to_cart/<int:book_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('add_to_payment/<int:user>/', AddToPaymentView.as_view(), name='add_to_payment'),
    path("payment/<int:user>/", PaymentView.as_view(), name="payment"),
    path("orderhistory/<int:user>/", OrderHistoryView.as_view(), name="order_history_user"),
    path("orderhistory/<int:user>/<int:order>/", OrderHistoryDetailView.as_view(), name="order_history_detail"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path('managebooks/', ManageBookListView.as_view(), name='managelist_book'),
    path('managebooks/<int:book_id>/', ManageBookView.as_view(), name='manage_book'),
    path('managebooks/delete/<int:book_id>/', ManageBookDeleteView.as_view(), name='manage_book_delete'),
    path("orderhistoryowner/", OrderHistoryOwnerView.as_view(), name="order_history_owner"),
    path("orderhistoryowner/<int:order>/", OrderHistoryOwnerDetailView.as_view(), name="order_history_owner_detail"),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:user_id>/', UserDetailView.as_view(), name='user_detail'),
    path('users/delete/<int:user_id>/', UserView.as_view(), name='user_delete'),
    path('stat/', StatView.as_view(), name='stat'),
]
