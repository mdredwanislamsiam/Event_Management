# Good Day — Event Management Platform

> **Good Day** is a professional, role-based event management platform built with Django. Designed for businesses, universities, and communities — it empowers organizers to plan and run events while giving participants a seamless RSVP experience, all under a secure, permission-driven system.

---

##  Table of Contents

- [Overview](#overview)
- [Who Is Good Day For?](#who-is-good-day-for)
- [Highlighted Features](#highlighted-features)
- [Full Feature List](#full-feature-list)
- [Role-Based Access Control](#role-based-access-control)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Core Modules](#core-modules)
- [Contact API Reference](#contact-api-reference)
- [Notable Design Decisions](#notable-design-decisions)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**Good Day** is a full-featured event management web application built on Django's MVT (Model-View-Template) architecture.

Managing events should not be complicated. Good Day removes the chaos from event planning by giving every user type — administrators, organizers, and participants — a tailored experience built around exactly what they need. Role permissions are enforced at every level, so the right people always have the right access.

From a corporate product launch to a university orientation week or a community fundraiser, Good Day scales to fit the occasion.

---

## Who Is Good Day For?

| Audience | Use Case |
|---|---|
| 🏢 **Businesses & Corporates** | Manage conferences, product launches, team events, and client seminars with full participant tracking |
| 🎓 **Universities & Schools** | Coordinate orientations, workshops, seminars, and student-facing events with role-separated staff and student access |
| 🌍 **General Public** | Community events, meetups, fundraisers — anyone can sign up, browse events, and RSVP in seconds |

---

## Highlighted Features

### 🎭 Role-Based Access Control (Admin / Organizer / Participant)

Good Day uses Django's Groups & Permissions system to enforce a strict three-tier access model. Every user belongs to one of three roles, and each role gets a completely different dashboard, navbar, and set of capabilities.

- **Admins** have full platform control: they manage users, assign roles, create groups, delete participants, and see all event statistics
- **Organizers** can create, edit, and delete events and manage categories — but cannot touch user management
- **Participants** get a personal dashboard showing only the events they have RSVP'd to, with their own stats

Role assignment is done by the Admin through a dedicated interface, and unauthorized access to any protected view redirects the user to a custom No Permission page rather than a generic error.

---

### 📨 RSVP & Participant Management

Participants can RSVP to any event with a single click. The system:

- Checks for duplicate registrations and shows a friendly warning instead of creating duplicate records
- Displays the full participant list on each event's detail page (visible to Admins and Organizers)
- Scopes each participant's dashboard to show only *their* events — upcoming, past, and today's — with personalized counts
- Lets Admins remove participants from the platform entirely when needed

---

### 📧 Email Notifications & Password Reset

Good Day uses Django's email backend to power critical communication flows:

**Account Activation**
When a new user signs up, their account is created in an inactive state. A tokenized confirmation email is sent immediately. The account only activates when the user clicks the unique link — protecting against bots and fake registrations.

**Password Reset**
Users who forget their password can request a reset link via email. Django's secure token generator ensures the link is single-use and time-limited. A custom HTML email template is used for a polished, branded experience.

**Password Change**
Logged-in users can change their password directly from their profile, with a dedicated confirmation page on success.

**Contact & Inquiry Emails**
The built-in contact form sends a formatted inquiry directly to the platform admin's inbox, including the sender's name, email, phone, event type, date, guest count, and message.

---

### 🔍 Event Filtering & Search

The events listing page includes a powerful, stackable filtering system — all filters work simultaneously via URL query parameters:

| Filter | Parameter | Description |
|---|---|---|
| Start date | `start_date` | Show events on or after this date |
| End date | `end_date` | Show events on or before this date |
| Date range | `start_date` + `end_date` | Show events within a range |
| Category | `category` | Filter by event category |
| Keyword | `search` | Search event name and location (case-insensitive) |

For example, a request like `?start_date=2025-01-01&end_date=2025-03-31&category=2&search=workshop` returns all workshop-tagged events in category 2 within Q1 2025 — no extra configuration needed.

---

## Full Feature List

- ✅ Custom user model with profile image, bio, phone, address
- ✅ Secure sign-up with email activation (token-based)
- ✅ Login / logout with session management
- ✅ Password change and password reset via email
- ✅ Profile view and edit
- ✅ Admin: user list, role assignment, group management, user deletion
- ✅ Event CRUD (Create, Read, Update, Delete)
- ✅ Image upload on events
- ✅ Inline category creation during event setup
- ✅ Advanced event filtering (date range, category, keyword)
- ✅ RSVP system with duplicate protection
- ✅ Role-specific dashboards with live stats (total, upcoming, past, today)
- ✅ Dynamic navbar based on user role
- ✅ Contact form with email delivery
- ✅ Custom no-permission error page
- ✅ Both FBV and CBV implementations throughout

---

## Role-Based Access Control

| Feature | Admin | Organizer | Participant |
|---|---|---|---|
| View all events | ✅ | ✅ | ✅ |
| Search & filter events | ✅ | ✅ | ✅ |
| RSVP to events | ❌ | ❌ | ✅ |
| Personal event dashboard | ❌ | ❌ | ✅ |
| Create events | ✅ | ✅ | ❌ |
| Update events | ✅ | ✅ | ❌ |
| Delete events | ✅ | ✅ | ❌ |
| View admin dashboard | ✅ | ❌ | ❌ |
| Assign user roles | ✅ | ❌ | ❌ |
| Manage groups | ✅ | ❌ | ❌ |
| View & delete users | ✅ | ❌ | ❌ |

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.x, Django 4.x |
| **Database** | PostgreSQL (SQLite for development) |
| **Authentication** | Django Auth + Custom User Model |
| **Email** | Django SMTP Email Backend |
| **Frontend** | Django Templates, HTML5, CSS3 |
| **Media Handling** | Django `ImageField` + `MEDIA_ROOT` |
| **Permissions** | Django Groups & Permission System |
| **Security** | CSRF protection, token-based activation & reset |

---

## Project Structure

```
goodday/
│
├── events/                        # Events app
│   ├── models.py                  # Event, Category models
│   ├── views.py                   # FBVs + CBVs for full event CRUD
│   ├── forms.py                   # EventModelForm, CategoryModelForm
│   ├── urls.py
│   └── templates/
│       ├── events.html            # Event listing with filters
│       ├── event_detail.html      # Single event + participant list
│       ├── create_event.html      # Create form with inline category
│       └── update_event.html
│
├── users/                         # Users app
│   ├── models.py                  # Custom User model
│   ├── views.py                   # Auth, dashboards, RSVP, profile
│   ├── forms.py                   # SignUp, SignIn, Password, Profile forms
│   ├── urls.py
│   └── templates/
│       ├── registration/          # Sign up, sign in
│       ├── accounts/              # Profile, password change/reset
│       ├── admin/                 # Admin dashboard, user list, role assign
│       ├── organizer/             # Organizer dashboard
│       └── participant/           # Participant dashboard
│
├── core/                          # Project root app
│   ├── views.py                   # home(), no_permission(), contact_submit()
│   ├── urls.py
│   └── settings.py
│
├── media/                         # Uploaded event images & profile photos
├── static/                        # CSS, JS, icons
├── manage.py
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- pip
- Virtualenv (recommended)
- PostgreSQL *(optional — SQLite works out of the box for development)*

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/goodday.git
cd goodday

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your environment variables
cp .env.example .env
# Edit .env with your values (see Environment Variables section)

# 5. Apply migrations
python manage.py migrate

# 6. Create a superuser (Admin account)
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser. Log in with your superuser and assign yourself the **Admin** group via Django Admin or the platform's role assignment view.

---

## Environment Variables

Create a `.env` file in the project root:

```env
# Django Core
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database (remove to use SQLite)
DATABASE_URL=postgres://user:password@localhost:5432/goodday_db

# Email — SMTP (Gmail example)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Media
MEDIA_URL=/media/
MEDIA_ROOT=media/
```

> **Tip for Gmail:** Use an [App Password](https://support.google.com/accounts/answer/185833) rather than your main account password — required when 2-Factor Authentication is enabled.

---

## Core Modules

### `events/views.py` — Event Views

| View | Type | Permission Required |
|---|---|---|
| `EventsView` | ListView (CBV) | Login |
| `EventDetailView` | DetailView (CBV) | Login |
| `CreateEventView` | CreateView (CBV) | `events.add_event` |
| `UpdateEventView` | UpdateView (CBV) | `events.change_event` |
| `DeleteEventView` | DeleteView (CBV) | `events.delete_event` |

FBV equivalents (`events`, `event_detail`, `create_event`, `update_event`, `delete_event`) are also present for reference and flexibility.

### `users/views.py` — User & Auth Views

| View | Description |
|---|---|
| `sign_up` | Registration with email confirmation |
| `sign_in` / `sign_out` | Session-based login and logout |
| `activate_user` | Token-based email activation |
| `admin_dashboard` | Admin stats with event type filter tabs |
| `organizer_dashboard` | Organizer stats view |
| `participant_dashboard` | Personal event dashboard (RSVP'd events only) |
| `rsvp` | One-click RSVP with duplicate guard |
| `assign_role` | Admin assigns roles to users |
| `user_list` | Admin views all registered users |
| `delete_participant` | Admin deletes a user |
| `create_group` / `group_list` / `delete_group` | Group management |
| `ProfileView` | View own profile details |
| `EditProfileView` | Edit profile info and image |
| `PasswordChange` | Change password (logged-in users) |
| `PasswordReset` | Trigger password reset email |
| `PasswordResetConfirm` | Confirm new password via email link |

### Helper: `navbar_test(user)`

A shared utility in `users/views.py` used by all views across the project. Takes the current user, checks their group, and returns the correct navbar template path — eliminating duplicated logic across every view.

```python
navbar = navbar_test(request.user)
# Returns one of:
# "admin/admin_navbar.html"
# "organizer/organizer_navbar.html"
# "participant/participant_navbar.html"
# "navbar.html"  (unauthenticated / no group)
```

---

**Success Response `200`:**
```json
{ "ok": true }
```

**Error Response `400`:**
```json
{ "ok": false, "error": "Name and email are required." }
```

**Error Response `500`:**
```json
{ "ok": false, "error": "SMTP connection failed." }
```

> Only `name` and `email` are required. All other fields are optional and will appear as `—` in the admin email if omitted.

---

## Notable Design Decisions

### Inline Category Creation
When creating or updating an event, users can either pick from an existing category dropdown or fill in the inline new-category form on the same page. If both are provided, the new category takes priority. This eliminates the need for a separate admin-only category management page during the event creation workflow.

### Dual FBV + CBV Implementations
Every major view is implemented twice — once as a Function-Based View and once as a Class-Based View. This makes the codebase an excellent learning reference and gives developers the flexibility to extend using whichever pattern fits the situation.

### Participant Scoping on Dashboard
The participant dashboard does not just filter the UI — it applies the user filter directly on the queryset (`filter(participant=request.user)`), so all stat aggregations (total, upcoming, past, today) are scoped specifically to that user's events. No data leaks between participants.

### Optimized Querysets Throughout
Every event queryset uses `select_related('category')` and `prefetch_related('participant')` to minimize database hits, even when filtering is applied. This keeps the platform responsive as event and participant counts grow.

---

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add: your feature description'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request with a clear description of what changed and why

Please follow **PEP 8** code style and write tests for any new functionality.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <strong>Good Day</strong> — Making every event a great one. 🌅<br/>
  Built with Django · Python · PostgreSQL
</div>