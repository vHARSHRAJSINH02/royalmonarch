from django.urls import path
from myapp import views

urlpatterns = [
   path('',views.index, name='index'),
   path('about/',views.about, name='about'),
   path('contact/',views.contact, name='contact'),
   path('services/',views.services, name='services'),
   path('testimonials/',views.testimonials, name='testimonials'),
   path('contact_form',views.contact_form, name='contact_form'),
   path('testimonialform',views.testimonial_form, name='testimonialform'),
   path('mailform',views.mailform, name='mailform'),
   path('careers/',views.careers, name='careers'),
   path('Emp_Login',views.Emp_Login, name='Emp_Login'),
   path('verify_Otp',views.verify_Otp, name='verify_Otp'),
   path('logout_emp',views.logout_emp, name='logout_emp'),
   path('post_jobs',views.post_jobs, name='post_jobs'),
   path('update_job_post',views.update_job_post, name='update_job_post'),
   path('delete_job_post',views.delete_job_post, name='delete_job_post'),
   path('apply_job',views.apply_job, name='apply_job'),
   path('login/',views.login, name='login'),
   path('otp/',views.otp, name='otp'),
   path('applications/',views.applications, name='applications'),
   path('addjobs/',views.addjobs, name='addjobs'),
   path('addnewjobs',views.addnewjobs, name='addnewjobs'),
   path('editjobs',views.editjobs, name='editjobs'),
   path('deletejob',views.deletejob, name='deletejob'),
]
