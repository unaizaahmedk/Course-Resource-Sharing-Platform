from math import floor
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import (
    User, Resource, ResourceImage, ResourceCategory,
    Course, Lender, Borrowing, Feedback
)

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('signup')

        try:
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return redirect('signup')

    return render(request, 'core/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', '/dashboard/')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please fill in both fields.")

    return render(request, 'core/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/home.html')


@login_required
def dashboard(request):
    user = request.user
    resources = Resource.objects.filter(lender_id=user.userid)
    all_courses = Course.objects.all()

    context = {
        'user': user,
        'resources': resources,
        'all_courses': all_courses,
    }

    return render(request, 'core/dashboard.html', context)

def browse_courses(request):
    courses = Course.objects.all()
    paginator = Paginator(courses, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/browse_course.html', {'courses': page_obj})

@login_required
def logged_browse_courses(request):
    courses = Course.objects.all()
    paginator = Paginator(courses, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/logged_browse_course.html', {'courses': page_obj})

@login_required
def add_resource(request):
    if request.method == "POST":
        try:
            resourcename = request.POST.get('resourcename')
            description = request.POST.get('description')
            course_id = request.POST.get('course')
            category_id = request.POST.get('category')

            category = ResourceCategory.objects.get(pk=category_id)
            is_public = category.is_public

            course = Course.objects.get(pk=course_id)

            lender = Lender.objects.filter(user=request.user, course=course).first()
            if not lender:
                lender = Lender.objects.create(
                    user=request.user,
                    course=course,
                    category=category,
                    lendingdate=timezone.now()
                )

            resource = Resource.objects.create(
                resourcename=resourcename,
                description=description,
                course=course,
                category=category,
                lender=lender.user,
                availability=True
            )

            if is_public:
                file = request.FILES.get('file')
                if file:
                    resource.file = file
                    resource.save()
                else:
                    messages.error(request, "Please upload a file for public resources.")
                    return redirect('add_resources')

            if not is_public:
                images = request.FILES.getlist('images')
                if images:
                    for image in images:
                        try:
                            ResourceImage.objects.create(resource=resource, image=image)
                            print(f"Image {image.name} saved successfully.")
                        except Exception as e:
                            print(f"Failed to save image {image.name}: {str(e)}")
                            messages.error(request, f"An error occurred while saving image {image.name}: {str(e)}")
                            return redirect('add_resources')
                else:
                    messages.error(request, "Please upload at least one image for borrowed resources.")
                    return redirect('add_resources')

            messages.success(
                request,
                "Resource added successfully! You can check your resources on the My Resources page."
            )
            return redirect('dashboard')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('add_resources')

    courses = Course.objects.all()
    categories = ResourceCategory.objects.all()
    return render(
        request,
        'core/add_resource.html',
        {'courses': courses, 'categories': categories}
    )


@login_required
def browse_resource(request):
    resources = Resource.objects.all()

    search_query = request.GET.get('search', '').strip()
    course_filter = request.GET.get('course')
    category_filter = request.GET.get('category')

    if search_query:
        resources = resources.filter(
            resourcename__icontains=search_query
        ) | resources.filter(
            description__icontains=search_query
        )

    if course_filter and course_filter != "all":
        try:
            course = Course.objects.get(coursename=course_filter)
            resources = resources.filter(course_id=course.courseid)
        except Course.DoesNotExist:
            resources = resources.none()

    if category_filter:
        try:
            category = ResourceCategory.objects.get(categoryname=category_filter)
            resources = resources.filter(category=category)
        except ResourceCategory.DoesNotExist:
            resources = resources.none()

    paginator = Paginator(resources, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    courses = Course.objects.all()
    categories = ResourceCategory.objects.all()

    context = {
        'resources': page_obj,
        'courses': courses,
        'categories': categories,
        'search_query': search_query,
        'selected_course': course_filter or "all",
        'selected_category': category_filter or "all",
    }

    return render(request, 'core/browse_resource.html', context)


@login_required
def my_resources(request):
    user_resources = Resource.objects.filter(lender=request.user).exclude(resourceid__isnull=True)
    return render(request, 'my_resource.html', {'resources': user_resources})


@login_required
def resource_details(request, resource_id):
    resource = get_object_or_404(Resource, resourceid=resource_id)

    if request.method == 'POST':
        print("POST Data:", request.POST)

        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        print("Rating:", rating, "Comment:", comment)

        if rating:
            try:
                rating = int(rating)
                if not (1 <= rating <= 5):
                    raise ValueError("Rating must be between 1 and 5.")
            except ValueError as e:
                print(f"Error: {e}")
                rating = None

        comment = comment.strip() if comment else None

        print("Processed Rating:", rating, "Processed Comment:", comment)

        try:
            feedback = Feedback(
                resource=resource,
                borrower=request.user,
                rating=rating,
                comment=comment
            )
            feedback.save()
            print("Feedback saved!")
        except Exception as e:
            print("Error saving feedback:", e)

        if rating is not None:
            total_ratings = resource.feedback_set.count()
            average_rating = resource.feedback_set.aggregate(Avg('rating'))['rating__avg']
            resource.average_rating = average_rating
            resource.total_ratings = total_ratings
            resource.save()

            print("Updated Resource Ratings - Average:", average_rating, "Total:", total_ratings)

        return redirect('resource_details', resourceid=resource_id)

    avg_rating = resource.average_rating or 0
    filled_stars = range(floor(avg_rating))
    empty_stars = range(5 - floor(avg_rating))

    feedback_list = Feedback.objects.filter(resource=resource).order_by('-feedbackid')

    context = {
        'resource': resource,
        'filled_stars': filled_stars,
        'empty_stars': empty_stars,
        'rating_range': range(1, 6),
        'feedback_list': feedback_list,
    }
    return render(request, 'core/resource_details.html', context)


@login_required
def add_feedback(request, resource_id):
    resource = get_object_or_404(Resource, resourceid=resource_id)

    if request.method == 'POST':
        print("POST data received:", request.POST)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if rating or comment:
            feedback = Feedback(
                resource=resource,
                borrower=request.user,
                rating=rating if rating else None,
                comment=comment if comment else None
            )
        feedback.save()

        if rating:
            total_ratings = resource.feedback_set.count()
            average_rating = resource.feedback_set.aggregate(Avg('rating'))['rating__avg']
            resource.average_rating = average_rating
            resource.total_ratings = total_ratings
            resource.save()

        return redirect('resource_details', resource_id=resource.resourceid)

    context = {'resource': resource}
    return render(request, 'core/resource_details.html', context)


@login_required
def borrow_resource(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)

    if request.method == "POST":

        if resource.lender == request.user:
            messages.error(request, "You cannot borrow your own resource.")
            return redirect('browse_resource')

        if Borrowing.objects.filter(resource=resource, status='borrowed').exists():
            messages.error(request, "This resource has already been borrowed by someone else.")
            return redirect('browse_resource')

        borrow_date = timezone.now().date()
        return_date_str = request.POST.get('return_date')
        if not return_date_str:
            messages.error(request, "Please select a return date.")
            return redirect('browse_resource')

        try:
            return_date = datetime.strptime(return_date_str, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid return date format.")
            return redirect('browse_resource')

        if return_date <= borrow_date:
            messages.error(request, "Return date must be after the borrow date.")
            return redirect('browse_resource')

        Borrowing.objects.create(
            borrower=request.user,
            resource=resource,
            borrowdate=borrow_date,
            returndate=return_date
        )

        resource.availability = False
        resource.save()

        messages.success(request, f"You have successfully borrowed '{resource.resourcename}'. Return it by {return_date}.")
        return redirect('borrowed_resources')

    else:
        return render(request, 'core/borrow.html', {'resource': resource})


@login_required
def borrowed_resources(request):
    borrowed_resources = Borrowing.objects.filter(
        borrower=request.user, status=Borrowing.BORROWED
    ).exclude(resource_id__isnull=True)

    return render(request, 'core/borrowed_resource.html', {'resources': borrowed_resources})


@login_required
def return_resource(request, resource_id):
    borrowing = get_object_or_404(Borrowing, resource__resourceid=resource_id, borrower=request.user, status=Borrowing.BORROWED)

    borrowing.status = Borrowing.RETURNED
    borrowing.resource.availability = True
    borrowing.resource.save()
    borrowing.save()

    messages.success(request, f'You have successfully returned "{borrowing.resource.resourcename}".')
    return redirect('borrowed_resources')