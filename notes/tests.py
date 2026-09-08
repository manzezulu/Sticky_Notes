# notes/tests.py
from django.test import TestCase
from django.urls import reverse

from .models import Note
from .forms import NoteForm


class NoteModelTest(TestCase):
    """Tests for the Note model."""

    def setUp(self):
        # Create a Note object for testing
        Note.objects.create(
            title="Test Note",
            content="This is a test note.",
            colour="#FFF4A3",
        )

    def test_note_has_title(self):
        # Test that a Note object has the expected title
        note = Note.objects.get(id=1)
        self.assertEqual(note.title, "Test Note")

    def test_note_has_content(self):
        # Test that a Note object has the expected content
        note = Note.objects.get(id=1)
        self.assertEqual(note.content, "This is a test note.")

    def test_note_has_default_colour(self):
        # Test that a Note created without an explicit colour still
        # defaults to yellow, as set on the model field.
        note = Note.objects.create(title="No Colour Note", content="...")
        self.assertEqual(note.colour, "#FFF4A3")

    def test_note_string_representation(self):
        # Test that __str__ returns the note's title
        note = Note.objects.get(id=1)
        self.assertEqual(str(note), "Test Note")

    def test_note_ordering_is_most_recently_updated_first(self):
        # Test that notes are ordered by -updated_at, i.e. the most
        # recently created/updated note appears first.
        newer_note = Note.objects.create(title="Newer Note", content="...")
        notes = list(Note.objects.all())
        self.assertEqual(notes[0], newer_note)


class NoteFormTest(TestCase):
    """Tests for the NoteForm."""

    def test_form_valid_with_required_fields(self):
        # A form with a title and content, and a valid colour choice,
        # should be valid.
        form = NoteForm(
            data={
                "title": "Groceries",
                "content": "Milk, eggs, bread.",
                "colour": "#C6E2FF",
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_title(self):
        # title is a required field, so omitting it should invalidate
        # the form.
        form = NoteForm(
            data={"title": "", "content": "Missing a title.", "colour": "#FFF4A3"}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_form_invalid_with_bad_colour_choice(self):
        # colour only accepts values from Note.COLOUR_CHOICES, so an
        # arbitrary hex value outside that list should be rejected.
        form = NoteForm(
            data={
                "title": "Bad Colour",
                "content": "This colour isn't an option.",
                "colour": "#000000",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("colour", form.errors)


class NoteViewTest(TestCase):
    """Tests for the notes app's views (CRUD)."""

    def setUp(self):
        self.note = Note.objects.create(
            title="Test Note",
            content="This is a test note.",
            colour="#FFF4A3",
        )

    def test_note_list_view(self):
        # The list view should return 200 and show the note's title.
        response = self.client.get(reverse("note_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")

    def test_note_detail_view(self):
        # The detail view should return 200 and show the title and content.
        response = self.client.get(
            reverse("note_detail", args=[str(self.note.id)])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")
        self.assertContains(response, "This is a test note.")

    def test_note_detail_view_404_for_missing_note(self):
        # Requesting a note that doesn't exist should 404, not error out.
        response = self.client.get(reverse("note_detail", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_note_create_view_get(self):
        # GET should render an empty form, not create anything.
        response = self.client.get(reverse("note_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "form")

    def test_note_create_view_post(self):
        # POSTing valid data should create a new note and redirect to
        # the note list (Post/Redirect/Get).
        response = self.client.post(
            reverse("note_create"),
            data={
                "title": "New Note",
                "content": "Created via test.",
                "colour": "#C9F2C9",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("note_list"))
        self.assertTrue(Note.objects.filter(title="New Note").exists())

    def test_note_create_view_post_invalid_data_does_not_create_note(self):
        # POSTing invalid data (no title) should re-render the form and
        # must not create a note.
        notes_before = Note.objects.count()
        response = self.client.post(
            reverse("note_create"),
            data={"title": "", "content": "Missing title.", "colour": "#FFF4A3"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), notes_before)

    def test_note_update_view_post(self):
        # POSTing valid data to the update URL should change the
        # existing note rather than creating a new one.
        response = self.client.post(
            reverse("note_update", args=[str(self.note.id)]),
            data={
                "title": "Updated Title",
                "content": "Updated content.",
                "colour": "#E5D4FF",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Updated Title")
        self.assertEqual(self.note.content, "Updated content.")

    def test_note_delete_view_get_shows_confirmation_without_deleting(self):
        # GET on the delete URL should show a confirmation page and
        # must NOT delete the note.
        response = self.client.get(
            reverse("note_delete", args=[str(self.note.id)])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Note.objects.filter(id=self.note.id).exists())

    def test_note_delete_view_post_deletes_note(self):
        # POST on the delete URL should actually remove the note and
        # redirect back to the note list.
        response = self.client.post(
            reverse("note_delete", args=[str(self.note.id)])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("note_list"))
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())
