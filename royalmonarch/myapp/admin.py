from django.contrib import admin
from django.utils.html import format_html
from .models import *

# Register your models here.

class Contact_admin(admin.ModelAdmin):
    list_display = ['contact_id','First_Name','Last_Name','Email','Mobile','Comments','Date_Time']

admin.site.register(Contact, Contact_admin)

class Testimonials_admin(admin.ModelAdmin):
    list_display = ['id','First_Name','Last_Name','Feedback','image']

admin.site.register(Testimonials, Testimonials_admin)

class Role_admin(admin.ModelAdmin):
    list_display = ['role_id','name', 'can_view_applications', 'can_post_jobs']

admin.site.register(Role, Role_admin)

class Employee_admin(admin.ModelAdmin):
    list_display = ['emp_id', 'Name', 'Email', 'Phone', 'Password', 'role', 'Active', 'OTP']

admin.site.register(Employee, Employee_admin)

class Applications_admin(admin.ModelAdmin):
    list_display = ['user_id', 'First_Name', 'Last_Name', 'Email', 'Mobile', 'download_resume','job_id']

    def download_resume(self, obj):
        if obj.Resume:
            return format_html('<a href="{}">Download</a>', obj.Resume.url)
        else:
            return "No resume uploaded"

    download_resume.short_description = 'Resume'

admin.site.register(Applications, Applications_admin)

class Jobs_admin(admin.ModelAdmin):
    list_display = ['job_id','Title', 'Description', 'Requirments', 'Salary_Range', 'Location', 'Date_Time']

admin.site.register(Jobs, Jobs_admin)