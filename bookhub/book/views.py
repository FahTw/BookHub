from django.shortcuts import render,redirect
from django.views import View
from .models import Book, BookCategory

# Create your views here.
class BookCategoryView(View):
    def get(self, request, category_id):
        category = BookCategory.objects.get(id=category_id)
        books = Book.objects.filter(category=category)
        categories = BookCategory.objects.all()
        return render(request, 'home.html', {'category': category, 'books': books})
class HomeView(View):
    def get(self, request):
        categories = BookCategory.objects.all()
        return render(request, 'home.html', {'categories': categories})
