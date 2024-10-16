from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from falco.htmx import for_htmx
from falco.pagination import paginate_queryset
from falco.types import HttpRequest

from .forms import BookForm
from .models import Book


# @for_htmx(use_partial="table")
def index(request: HttpRequest):
    books = Book.objects.order_by("-created_at")
    return TemplateResponse(
        request,
        "books/index.html",
        context={
            "books_page": paginate_queryset(request, books),
            "fields": (
                "created_at",
                "name",
                "description",
                "published_at",
                "on_going",
                "cover_art",
                "author",
            ),
        },
    )


def detail(request: HttpRequest, slug):
    book = get_object_or_404(Book.objects, slug=slug)
    return TemplateResponse(
        request,
        "books/detail.html",
        context={"book": book},
    )


def process_form(request: HttpRequest, slug=None):
    instance = get_object_or_404(Book.objects, slug=slug) if slug else None
    form = BookForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(
            reverse("books:detail", args=(slug,)) if slug else reverse("books:index")
        )
    return TemplateResponse(
        request,
        "books/form.html",
        context={"instance": instance, "form": form},
    )


@require_http_methods(["DELETE", "POST"])
def delete(request: HttpRequest, slug):
    Book.objects.filter(slug=slug).delete()
    return HttpResponse() if request.htmx else redirect("books:index")
