import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated  # <-- protect
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book, Author, BookInstance, Genre
from .forms import RenewBookForm
from .service import BookInstanceFilter
from .serializers import (
    AuthorsSerializer,
    AuthorSerializer,
    AuthorBoooksSerializer,
    BooksSerializer,
    BooksInstanceSerializer
)


def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Available copies of books
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # The 'all()' is implied by default.

    # TEST Generate counts of Genre
    num_genre=Genre.objects.all().count()

    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors,
            'num_visits':num_visits, 'num_genre':num_genre},
    )# TEST add counts of Genre


class BookListView(generic.ListView):
    """
    Generic class-based view for a list of books.
    """
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    """
    Generic class-based detail view for a book.
    """
    model = Book

class AuthorListView(generic.ListView):
    """
    Generic class-based list view for a list of authors.
    """
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    """
    Generic class-based detail view for an author.
    """
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksAllListView(PermissionRequiredMixin,generic.ListView):
    """
    Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission.
    """
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name ='catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'05/04/2018',}
    permission_required = 'catalog.can_mark_returned'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
    permission_required = 'catalog.can_mark_returned'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'


#Classes created for the forms challenge
class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_mark_returned'


#for api
class AuthorsView(APIView):
    permission_classes = (IsAuthenticated,)             # <-- protect
    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorsSerializer(authors, many=True)
        return Response({"authors": serializer.data})


class AuthorView(APIView):
    permission_classes = (IsAuthenticated,)             # <-- protect
    def get(self, request, pk):
        autor = Author.objects.filter(id=pk)
        serializer = AuthorSerializer(autor, many=True)
        return Response({
            "autor": serializer.data,
            })


class AuthorBooksView(APIView):
    permission_classes = (IsAuthenticated,)             # <-- protect
    def get(self, request, pk):
        autor = Author.objects.filter(id=pk)
        serializer = AuthorBoooksSerializer(autor, many=True)
        books = Book.objects.filter(author=autor[0])
        serializer_books = BooksSerializer(books, many=True)
        result_copy = []
        for book in books:
            book_copy = BookInstance.objects.filter(book=book)
            result_copy += book_copy
        serializer_copy = BooksInstanceSerializer(result_copy, many=True)
        return Response({
            "autor": serializer.data,
            "books": serializer_books.data,
            "books copy": serializer_copy.data,
            })


class BooksView(APIView):
    permission_classes = (IsAuthenticated,)             # <-- protect
    def get(self, request):
        books = Book.objects.all()
        serializer_books = BooksSerializer(books, many=True)
        result_copy = []
        for book in books:
            book_copy = BookInstance.objects.filter(book=book)
            result_copy += book_copy
        serializer_copy = BooksInstanceSerializer(result_copy, many=True)
        return Response({
            "books": serializer_books.data,
            "books copy": serializer_copy.data,
            })


class BookView(APIView):
    permission_classes = (IsAuthenticated,)             # <-- protect
    def get(self, request, pk):
        book = Book.objects.filter(id=pk)
        serializer_book = BooksSerializer(book, many=True)
        book_copy = BookInstance.objects.filter(book=book[0])
        serializer_copy = BooksInstanceSerializer(book_copy, many=True)
        return Response({
            "book": serializer_book.data,
            "books copy": serializer_copy.data,
            })


class BooksList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)             # <-- protect
    queryset = BookInstance.objects.all()
    serializer_class = BooksInstanceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookInstanceFilter
