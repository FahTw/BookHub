import re
from django.shortcuts import render,redirect
from django.views import View
from .models import Book, BookCategory
from .form import ManageBookForm, ProfileForm
from .form import ReviewForm



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
class ProfileView(View):
    def get(self, request):
        form = ProfileForm()
        return render(request, 'profile.html')
    def post(self, request):
        # Handle profile update logic here
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/book/')
        return redirect('profile')
class BookListView(View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'book_list.html', {'books': books})
class ReviewView(View):
    def get(self, request, book_id):
        form = ReviewForm()
        book = Book.objects.get(pk=book_id)
        return render(request, 'review.html', {'form': form, 'book': book})
    def post(self, request, book_id):
        form = ReviewForm(request.POST)
        book = Book.objects.get(pk=book_id)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('book_detail', book_id=book_id)
        

        return render(request, 'review.html', {'form': form, 'book': book})
class ManageBookView(View):
    def get(self, request):
        form = ManageBookForm()
        books = Book.objects.all()
        return render(request, 'book_manage.html', {'form': form, 'books': books})
    def post(self, request):
        form = ManageBookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_book')
        books = Book.objects.all()
        return render(request, 'book_manage.html', {'form': form, 'books': books})