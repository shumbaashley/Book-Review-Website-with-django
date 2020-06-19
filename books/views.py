from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, View
from django.views.generic.edit import CreateView
from .forms import BookForm, ReviewForm, CommentForm
from .models import Author, Book, Comment, Editor

# Create your views here.
def login_view(request): 
    return render(request, 'login.html', {})

def sign_in_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("review-books"))
    else:
        return render(request, "login.html", {})

def sign_out_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("books"))


def list_books(request):
    """
    List the books that have reviews
    """
    books = Book.objects.exclude(date_reviewed__isnull=True).prefetch_related('authors')

    context = {
        'books': books,
    }
    return render(request, "lists.html", context) 

class EditorList(View):
    def get(self, request):
        editors = Editor.objects.all

        context = {
            'editors': editors,
        }

        return render(request, "editors.html", context)

def book_detail_view(request, pk):
    book = Book.objects.get(pk=pk)
    context = {
        "book" : book
    }
 
    return render(request, "book.html", context)

class EditorDetail(DetailView):
    model = Editor
    template_name = "editor.html"

class ReviewList(View):
    """
	List all of the books that we want to review.
	"""
    def get(self, request):
        books = Book.objects.filter(date_reviewed__isnull=True).prefetch_related('authors')
        
        context = {
            'books': books,
            'form': BookForm,
        }
        return render(request, "list-to-review.html", context)
	
    def post(self, request):
        form = BookForm(request.POST)
        books = Book.objects.filter(date_reviewed__isnull=True).prefetch_related('authors')
       
        if form.is_valid():
           form.save()
           return redirect('review-books')

        context = {
            'form': form,
            'books': books,
        }
        return render(request, "list-to-review.html", context)

@login_required	
def review_book(request, pk):
    """
	Review an individual book
	"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        # Process our form
        form = ReviewForm(request.POST)

        if form.is_valid():
            book.is_favourite = form.cleaned_data['is_favourite']
            book.review = form.cleaned_data['review']
            book.reviewed_by = request.user
            book.save()
            
            return redirect('review-books')

    else:
        form = ReviewForm

    context = {
		'book': book,
        'form': form,
	}
    return render(request, "review-book.html", context)
	
class CreateAuthor(CreateView):
    model = Author
    fields = ['name',]
    template_name = "create-author.html"

    def get_success_url(self):
        return reverse('review-books')


def create_comment_view(request, pk):

    name = request.POST['name']
    email = request.POST['email']
    message = request.POST['message']

    comment = Comment.objects.create(name=name, email=email, message=message)
    comment.save()

    book = Book.objects.get(pk = pk)
    
    
    book.comments.add(comment)
    book.save()
    
    return HttpResponseRedirect(reverse("book-detail", args=(pk,)))




def contact_view(request):
    return render(request, "contact.html", {})

def about_view(request):
    return render(request, "about.html", {})

def reviewer_profile_view(request, pk):
    book = Book.objects.get(pk=pk)
    context = {
        "editor": book.reviewed_by
    }
    return render(request, "editor.html", context)