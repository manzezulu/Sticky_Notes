# Sticky Notes — Django Application

A Django app that lets a user create, view, update, and delete sticky notes.

## Project structure

```
sticky_notes/
├── manage.py
├── db.sqlite3                 (empty — created fresh by migrate)
├── research_answers.md        
├── diagrams/
│   ├── use_case_diagram.svg
│   ├── sequence_diagram.svg
│   └── class_diagram.svg
├── notes/                     (the "notes" app)
│   ├── models.py              (Note model)
│   ├── forms.py                (NoteForm — ModelForm)
│   ├── views.py                (CRUD views)
│   ├── urls.py                 (app URL patterns)
│   ├── admin.py                (Note registered with the admin site)
│   ├── migrations/
│   ├── templates/
│   │   ├── base.html
│   │   └── notes/
│   │       ├── note_list.html
│   │       ├── note_detail.html
│   │       ├── note_form.html
│   │       └── note_confirm_delete.html
│   └── static/notes/styles.css
└── sticky_notes/               (project/core app)
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # venv\Scripts\activate on Windows

# 2. Install Django
pip install django

# 3. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 4. Collect static files
python manage.py collectstatic

# 5. (Optional) create an admin user
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Then visit **http://127.0.0.1:8000/** to use the app, or
**http://127.0.0.1:8000/admin/** to manage notes through the Django admin.

## Features implemented

- **Model** — `Note` with `title`, `content`, `colour`, `created_at`, and
  `updated_at` fields.
- **Views** — full CRUD: `note_list`, `note_detail`, `note_create`,
  `note_update`, `note_delete` (with a delete confirmation page).
- **Forms** — `NoteForm`, a `ModelForm` used for both creating and editing
  notes.
- **URLs** — named URL patterns in `notes/urls.py`, included from the
  project's root `urls.py`.
- **Templates** — a `base.html` template extended by all note templates,
  using Django template tags for dynamic content.
- **Static files** — a custom stylesheet (`notes/static/notes/styles.css`)
  giving each note a sticky-note card look, collected via `collectstatic`.
- **Admin** — the `Note` model is registered so notes can also be managed
  from `/admin/`.

## Testing

Run the automated test suite (17 tests covering the model, form, and every
CRUD view):

```bash
python manage.py test notes -v 2
```

## Diagrams


See the `diagrams/` folder for the use case, sequence, and class diagrams
covering this application's design.
