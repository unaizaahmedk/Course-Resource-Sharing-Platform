from django.contrib import admin
from .models import Course, ResourceCategory, Resource, Borrowing, Lender, User, Feedback, ResourceImage

from django.contrib.auth import get_user_model
User = get_user_model()

admin.site.register(Course)
admin.site.register(ResourceCategory)
admin.site.register(Resource)
admin.site.register(Borrowing)
admin.site.register(Lender)
admin.site.register(User)
admin.site.register(Feedback)
admin.site.register(ResourceImage)

