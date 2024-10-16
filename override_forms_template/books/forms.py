from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            "name",
            "description",
            "published_at",
            "on_going",
            "cover_art",
            "author",
        )
        widgets = {
            "published_at": forms.DateInput(attrs={"type": "date"}),
        }
