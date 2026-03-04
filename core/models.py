from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Model for Course
class Course(models.Model):
    courseid = models.AutoField(primary_key=True)
    coursename = models.CharField(max_length=255)
    coursecode = models.CharField(max_length=50)

    def __str__(self):
        return self.coursename


# UserManager for creating users and superusers
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)  # Hash the password before saving
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

# User Model
class User(AbstractBaseUser):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  
    is_admin = models.BooleanField(default=False)  
    is_superuser = models.BooleanField(default=False)   

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
        
    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return True

# Model for Resource Category
class ResourceCategory(models.Model):
    categoryid = models.AutoField(primary_key=True)
    categoryname = models.CharField(max_length=255, unique=True)
    is_public = models.BooleanField(default=False)  # True for public, False for borrowed

    def __str__(self):
        return self.categoryname


# Model for Resource
class Resource(models.Model):
    resourceid = models.AutoField(primary_key=True)
    resourcename = models.CharField(max_length=255)
    description = models.TextField()
    availability = models.BooleanField(default=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE)
    lender = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        related_name='resources_lent',
        on_delete=models.CASCADE
    )
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    uploaded_on = models.DateTimeField(auto_now_add=True)

    average_rating = models.FloatField(default=0)  
    total_ratings = models.IntegerField(default=0)  

    def __str__(self):
        return self.resourcename
    
# Model for Resource Images
class ResourceImage(models.Model):
    resource = models.ForeignKey(Resource, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='resource_images/')  # Default upload path for borrowed resources

    def __str__(self):
        return f"{self.resource.resourcename} - Image"


class Borrowing(models.Model):
    BORROWED = 'borrowed'
    RETURNED = 'returned'
    STATUS_CHOICES = [
        (BORROWED, 'Borrowed'),
        (RETURNED, 'Returned'),
    ]

    borrowingid = models.AutoField(primary_key=True)
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        related_name='borrowed_resources',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    borrowdate = models.DateField()
    returndate = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=BORROWED)

    def __str__(self):
        return f"Borrowing {self.borrowingid} - {self.resource.resourcename}"


class Lender(models.Model):
    lenderid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="lended_resources", on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE)
    lendingdate = models.DateField()

    def __str__(self):
        return f"Lender {self.user.username}"

# Model for Feedback
class Feedback(models.Model):
    feedbackid = models.AutoField(primary_key=True)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(null=True, blank=True) 
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Feedback {self.feedbackid} - {self.resource.resourcename}"



