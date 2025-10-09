from django.urls import path
from . import views

urlpatterns = [
    path('category/<int:category_id>/', views.BookCategoryView.as_view(), name='book_category'),
    path('', views.HomeView.as_view(), name='home'),
    # path('', views.BookListView.as_view(), name='book_list'),
    # path('book/<int:book_id>/', views.BookDetailView.as_view(), name='book_detail'),
]