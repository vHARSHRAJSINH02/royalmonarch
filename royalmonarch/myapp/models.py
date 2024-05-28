from django.db import models

# Create your models here.
class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    First_Name = models.CharField(max_length=100,null=True)
    Last_Name = models.CharField(max_length=100,null=True)
    Email = models.EmailField(max_length=200,null=True)
    Mobile = models.CharField(max_length=10, null=True)
    Comments = models.TextField(max_length=2000, null=True)
    Date_Time = models.DateTimeField(auto_now=True,editable=False)

    def __str__(self):
        return str(self.contact_id)
    
class Testimonials(models.Model):
    id = models.AutoField(primary_key=True)
    First_Name = models.CharField(max_length=100,null=True)
    Last_Name = models.CharField(max_length=100,null=True)
    Sub_Feedback = models.CharField(max_length=100,null=True)
    Feedback = models.TextField(max_length=1000,null=True)
    image = models.ImageField(upload_to='uploads/',null=True)

    def __str__(self):
        return str(self.id)
    
class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    can_view_applications = models.BooleanField(default=False)
    can_post_jobs = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100,null=True)
    Email = models.EmailField(max_length=254, null=True)
    Phone = models.CharField(max_length=15, null=True)
    Password = models.CharField(max_length=16, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    OTP = models.CharField(max_length=6, null=True)
    Active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.emp_id)
    
class Jobs(models.Model):
    job_id = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=100, null=True)
    Description = models.TextField(max_length=2000,null=True)
    Requirments = models.CharField(max_length=1000,null=True)
    Salary_Range = models.CharField(max_length=100, null=True)
    Location = models.CharField(max_length=500, null=True)
    Date_Time = models.DateTimeField(auto_now=True, editable=False)
    
    def __str__(self):
        return str(self.job_id)
    
class Applications(models.Model):
    user_id = models.AutoField(primary_key=True)
    First_Name = models.CharField(max_length=100,null=True)
    Last_Name = models.CharField(max_length=100,null=True)
    Email = models.EmailField(max_length=254, null=True)
    Mobile = models.CharField(max_length=15,null=True)
    Resume = models.FileField(upload_to='resumes/', null=True)
    job_id = models.ForeignKey(Jobs, on_delete=models.CASCADE, null=True)
    STATUS_CHOICES = [
        ('P','Pending'),
        ('V', 'Viewed'),
        ('F', 'Follow Up'),
        ('FF', 'Followed Up'),
    ]
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='P')
    def __str__(self):
        return str(self.user_id)