# Course Resource Sharing Platform

A Django-based web application that enables students to share, browse, and borrow academic resources (documents, notes, and materials) across different courses. The platform facilitates collaborative learning by allowing users to upload resources and have them rated by the community.

## 📋 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## 🎯 About the Project

**Course Resource Sharing Platform** is designed to bridge the gap between students in academic settings. Instead of students individually searching for course materials, this platform provides a centralized hub where:

- Students can upload and share resources (notes, PDFs, images, etc.)
- Peers can browse and borrow resources from other students
- Resource quality is maintained through a community rating system
- Resources are organized by course and category for easy discovery

### Why This Project?

Traditional course material sharing relies on email chains, message groups, or scattered cloud links. This platform provides a structured, organized, and rating-based system to ensure quality resource sharing while building a supportive learning community.

## ✨ Features Implemented

### 1. **User Authentication & Authorization**
- Custom user model with email and username
- Secure signup and login functionality
- Role-based access (students/admins)
- Password hashing and validation
- Session-based authentication

### 2. **Resource Management**
- **Upload Resources** - Users can add resources with descriptions and select associated courses
- **Two Resource Categories:**
  - **Public Resources** - Can include files (PDFs, documents, etc.)
  - **Borrowed Resources** - Can include multiple images for visual reference
- **Browse Resources** - Search and filter by course, category, or keyword
- **View Details** - Detailed resource pages with full descriptions and metadata

### 3. **Course Management**
- 14 pre-populated computer science courses (CS101-CS310)
- Course browsing for both authenticated and anonymous users
- Easy course selection when adding resources

### 4. **Borrowing System**
- Users can borrow available resources by specifying a return date
- Automatic availability tracking (resources marked as unavailable when borrowed)
- Borrowed resources dashboard showing all current borrowings
- Return functionality to mark resources as available again
- Return date validation to ensure realistic borrowing periods

### 5. **Rating & Feedback System**
- Users can rate resources on a 1-5 star scale
- Optional comments/feedback on resources
- Real-time average rating calculation
- Display of community feedback on resource detail pages
- Visual star rating display (filled and empty stars)

### 6. **Dashboard**
- Personalized user dashboard with quick links
- Access to "My Resources" (uploaded resources)
- Access to "Borrowed Resources" (active borrowings)
- Easy resource addition from dashboard

### 7. **Search & Filter**
- Full-text search across resource names and descriptions
- Filter by course and category
- Pagination for better performance with large datasets

### 8. **Responsive Design**
- Mobile-friendly interface
- Clean, modern CSS styling
- Intuitive navigation bar
- Category-specific styling for different pages

## 🛠 Tech Stack

- **Backend:** Django 5.1.1 (Python web framework)
- **Database:** SQLite (development); can be upgraded to PostgreSQL for production
- **Frontend:** HTML5, CSS3, JavaScript
- **Authentication:** Django's built-in auth system with custom User model
- **Media Handling:** Django ImageField and FileField for uploads
- **Version Control:** Git & GitHub

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/unaizaahmedk/Course-Resource-Sharing-Platform.git
   cd Course-Resource-Sharing-Platform
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # or
   source venv/bin/activate      # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - Main app: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## 📖 Usage

### For Students (Regular Users)

1. **Sign Up** - Create an account with username, email, and password
2. **Browse Courses** - Explore available courses and their resources
3. **Add a Resource**:
   - Navigate to Dashboard → Add Resources
   - Select a course and category
   - Upload file (for public) or images (for borrowed)
4. **Borrow Resources** - Find resources and specify a return date
5. **Rate Resources** - Leave ratings and feedback on borrowed resources
6. **Return Resources** - Mark borrowed items as returned when done

### For Administrators

1. Access `/admin/` to manage:
   - Users
   - Courses
   - Resources
   - Categories
   - Borrowing records
   - Feedback and ratings

## 📁 Project Structure

```
resource_sharing/
├── core/                          # Main Django app
│   ├── models.py                 # Database models (User, Course, Resource, etc.)
│   ├── views.py                  # View functions for all pages
│   ├── urls.py                   # URL routing
│   ├── forms.py                  # Django forms
│   ├── admin.py                  # Admin configuration
│   ├── templates/core/           # HTML templates
│   ├── migrations/               # Database migration files
│   └── templatetags/             # Custom template filters
├── resource_sharing/              # Project settings
│   ├── settings.py               # Django configuration
│   ├── urls.py                   # Main URL router
│   └── wsgi.py                   # WSGI application
├── static/
│   ├── css/                      # Stylesheets
│   └── images/                   # Static images
├── resources/                     # Media upload directory
│   ├── resources/                # Uploaded files
│   └── resource_images/          # Uploaded images
├── manage.py                      # Django management script
└── db.sqlite3                     # SQLite database
```

## 🗄 Database Models

### User
- Custom user model with email-based authentication
- Fields: userid, username, email, password, is_active, is_staff, is_admin, is_superuser

### Course
- Fields: courseid, coursename, coursecode

### ResourceCategory
- Fields: categoryid, categoryname, is_public (distinguishes public/borrowed)

### Resource
- Fields: resourceid, resourcename, description, availability, course, category, lender, file, uploaded_on, average_rating, total_ratings

### ResourceImage
- Fields: resource (FK), image (for borrowed resources)

### Borrowing
- Fields: borrowingid, borrower, resource, borrowdate, returndate, status

### Feedback
- Fields: feedbackid, resource, borrower, rating, comment

### Lender
- Fields: lenderid, user, course, category, lendingdate

## 🔮 Future Enhancements

- [ ] Email notifications for borrowing reminders
- [ ] Advanced search with tags and filters
- [ ] User profiles with sharing statistics
- [ ] Resource recommendations based on ratings
- [ ] File preview functionality (PDF, DOC)
- [ ] Real-time chat between borrowers and lenders
- [ ] Resource expiry and automatic archival
- [ ] API endpoints for mobile app support
- [ ] Two-factor authentication
- [ ] Analytics dashboard for admins

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ by Unaiza Ahmed K**