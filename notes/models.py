# notes/models.py
from django.db import models


class Note(models.Model):
    """Model representing a single sticky note.

    Fields:
    - title: CharField for the note's title, max length 100 characters.
    - content: TextField for the body/content of the note.
    - colour: CharField storing a hex colour used to theme the note card.
    - created_at: DateTimeField set automatically when the note is created.
    - updated_at: DateTimeField set automatically whenever the note is saved.

    Methods:
    - __str__: Returns a string representation of the note, showing the
      title.

    :param models.Model: Django's base model class.
    """

    COLOUR_CHOICES = [
        ("#FFF4A3", "Yellow"),
        ("#FFC6C6", "Pink"),
        ("#C9F2C9", "Green"),
        ("#C6E2FF", "Blue"),
        ("#E5D4FF", "Purple"),
    ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    colour = models.CharField(
        max_length=7, choices=COLOUR_CHOICES, default="#FFF4A3"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title
