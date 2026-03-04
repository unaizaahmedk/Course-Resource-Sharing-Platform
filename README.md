# Course Resource Sharing Platform

A Django-based web application that enables students to share, browse, and borrow academic resources across courses. The application serves as a centralized hub where students can upload resources they own, discover resources shared by peers, and borrow physical materials, all in one place. The project was shortlisted as one of the top projects in the Database course.


### Features

**1. User Authentication**
Students can sign up with a username and email, with validation to prevent duplicate registrations and secure password hashing. Non-authenticated users can browse and view resources but cannot upload, download, or borrow anything. All such actions are restricted to logged-in users only. Admin access is available via Django's admin panel.

**2. Resource Listing**
Logged-in students can list a resource by providing its name, description, course, and category. Soft copy resources such as PDFs, notes, or books are uploaded as a file so other students can download them directly. Hard copy resources such as physical books or printed notes are uploaded as images so students can preview them and decide whether they want to borrow them physically.

**3. Browse and Search**
All users can browse available resources, search by name or description, and filter by course and category. Results are paginated at 12 per page. Downloading or borrowing a resource requires logging in.

**4. Resource Detail Page**
Each resource has a dedicated page showing its full details including description, course, and category, along with a downloadable file or preview images, average star rating out of 5, and all community reviews.

**5. Borrow and Return**
Students can borrow a hard copy resource by selecting a return date. Once borrowed, the resource is marked unavailable so no other student can borrow it at the same time. Students cannot borrow their own resources. Once returned, availability is restored.

**6. My Resources**
Students can view all resources they have personally listed on the platform in one place, whether soft or hard copy.

**7. Borrowed Resources**
Students can view all resources they currently have on loan along with the date by which each must be returned.

**8. Ratings and Feedback**
Students can leave a star rating out of 5 and a written comment on any resource. The average rating is automatically recalculated and updated on every new submission.



### Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django 5.1.1 |
| Database | SQLite |
| Frontend | HTML5, CSS3, JavaScript |
| Authentication | Custom AbstractBaseUser, Django Auth |
| File Handling | Django FileField, ImageField |
| Version Control | Git & GitHub |



### Installation

**Prerequisites:** Python 3.8+, pip, Git

```bash
# Clone the repository
git clone https://github.com/unaizaahmedk/Course-Resource-Sharing-Platform.git
cd Course-Resource-Sharing-Platform

# Create and activate a virtual environment
python -m venv venv
source venv/Scripts/activate   # Windows
source venv/bin/activate        # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

Access the app at `http://127.0.0.1:8000/` and the admin panel at `http://127.0.0.1:8000/admin/`



### Project Structure

```
resource_sharing/
├── core/
│   ├── models.py               # Database models
│   ├── views.py                # View functions
│   ├── urls.py                 # URL routing
│   ├── forms.py                # Django forms
│   ├── admin.py                # Admin configuration
│   ├── templates/core/         # HTML templates
│   └── migrations/             # Database migrations
├── resource_sharing/
│   ├── settings.py             # Project settings
│   ├── urls.py                 # Root URL configuration
│   └── wsgi.py                 # WSGI entry point
├── static/
│   ├── css/                    # Stylesheets
│   └── images/                 # Static images
├── resources/                  # Media uploads
├── manage.py
└── db.sqlite3
```


### Database Models

| Model | Key Fields |
|---|---|
| User | userid, username, email, password, is_admin |
| Course | courseid, coursename, coursecode |
| ResourceCategory | categoryid, categoryname, is_public |
| Resource | resourcename, description, availability, course, category, lender, file, average_rating |
| ResourceImage | resource (FK), image |
| Borrowing | borrower, resource, borrowdate, returndate, status |
| Feedback | resource, borrower, rating, comment |
| Lender | user, course, category, lendingdate |
