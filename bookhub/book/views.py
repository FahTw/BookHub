from django.shortcuts import render,redirect
from django.views import View
from .models import Book, BookCategory
from .form import ProfileForm

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
