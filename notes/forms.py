# notes/forms.py
from django import forms

from .models import Note


class NoteForm(forms.ModelForm):
    """Form for creating and updating Note objects.

    Fields:
    - title: CharField for the note title.
    - content: TextField for the note content.
    - colour: ChoiceField for the note's background colour.

    Meta class:
    - Defines the model to use (Note) and the fields to include in the
      form.

    :param forms.ModelForm: Django's ModelForm class.
    """

    class Meta:
        model = Note
        fields = ["title", "content", "colour"]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Note title", "class": "form-control"}
            ),
            "content": forms.Textarea(
                attrs={
                    "placeholder": "Write your note here...",
                    "class": "form-control",
                    "rows": 6,
                }
            ),
            "colour": forms.Select(attrs={"class": "form-control"}),
        }
