from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from nepali_date import NepaliDate



from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class is imported. ##
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# from django.contrib.auth.mixins import PermissionRequiredMixin

gender_choices = (('Male', 'Male'), ('Female', 'Female'))
Type_choices = (('Principle','Principle'),('Vice-Principle','Vice-Principle'),('Accountant','Accountant'),('Teacher','Teacher'),('Piyan','Piyan'))


# Create your models here.

class Registration(models.Model):
    name = models.CharField(max_length=200)
    dob = models.DateField(blank = True, null=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=1000)
    email = models.EmailField(max_length=1000)
    grade = models.IntegerField()
    voucher = models.ImageField(upload_to='images', blank=True, null=True)
    date = models.DateTimeField(default=NepaliDate.today().isoformat())

    def __str__(self):
        return self.name


    
class User(AbstractUser,UserManager):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)
    is_accountant= models.BooleanField(default=False)
    is_principal =models.BooleanField(default=False)
    is_viceprinciple = models.BooleanField(default=False)

    def get_absolute_url(self): # new
        return reverse('user')




class Session(models.Model):
    session_choices = (
        ('',''),
        ("2020/2021","2020/2021"),
        ("2021/2022","2021/2022"),
        ("2022/2023","2022/2023"),
        ("2023/2024","2023/2024"))
    session = models.CharField(max_length=20, choices = session_choices, unique=True)
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')

    def __str__(self):
        return self.session



class ClassRoom(models.Model):
    class_level = models.CharField(max_length=20)
    section = models.CharField(max_length=20)
    no_student = models.IntegerField(default=0)
    room_number = models.IntegerField(unique=True)

    class Meta:
        ordering = ('class_level',)


    def __str__(self):
        return (self.class_level+" sec: " + self.section)

    def total(self):
        total = Admission.object.filter(class_level=class_room)

    def get_absolute_url(self): # new
        return reverse('addclass')



class Admission(models.Model):
    name = models.CharField(max_length=20)
    dob = models.DateField(null=False)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices = gender_choices)
    current_address = models.CharField(max_length=100)
    permanent_address = models.CharField(max_length=1000)
    email = models.EmailField(max_length=1000)
    sesson = models.ForeignKey(Session, on_delete=models.SET_NULL,null=True)
    class_level = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, related_name="class_room" )
    roll_no = models.CharField(max_length=10)
    registration_no = models.CharField(max_length=20,unique=True)
    image = models.ImageField(upload_to='images/students/')
    join_date = models.DateField(auto_now=True)

    # class Meta:
    #     ordering =('name',)
  
    def __str__(self):
        return self.name

    def get_absolute_url(self): # new
        return reverse('allstudent')



class Staff(models.Model):
    name = models.CharField(max_length=20)
    Type = models.CharField(max_length=100, choices = Type_choices)
    dob = models.DateField(blank = True, null=True)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices = gender_choices, default='Male')
    district = models.CharField(max_length=100,default="")
    address = models.CharField(max_length=1000)
    email = models.EmailField(max_length=1000,null=True)
    image = models.ImageField(upload_to='images/staff/')
    date =models.DateField(default=NepaliDate.today().isoformat())
    def __str__(self):
        return str(self.name)

    def get_absolute_url(self): # new
        return reverse('allstaff')


class Subject(models.Model):
    name = models.CharField(max_length=100)
    class_level = models.ForeignKey(ClassRoom ,on_delete=models.SET_NULL,null=True) 
    book_ID = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self): # new
        return reverse('addsubject')



class Routine(models.Model):
    period_choices=(
        ("Period 1","Period 1"),
        ("Period 2","Period 2"),
        ("Period 3","Period 3"),
        ("Period 4","Period 4"),
        ("Period 5","Period 5"),
        ("Period 6","Period 6"),
        ("Period 7","Period 7"))

    day_choices=(
        ("Sunday","Sunday"),
        ("Monday","Monday"),
        ("Tuesday","Tuesday"),
        ("wednesday","Wednesday"),
        ("Thrusday","Thrusday"),
        ("Friday","Friday"),
        ("Saturday","Saturday"))

    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL,null=True,related_name="subjectinroutine")
    period = models.CharField(max_length=20, choices = period_choices)
    day = models.CharField(max_length=30,choices = day_choices)
    start_time = models.TimeField( default="10:00" )
    end_time = models.TimeField(default="10:00" )
    teacher = models.ForeignKey(Staff, on_delete=models.SET_NULL,null=True)
    class_level = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL,null=True)


    def __str__(self):
        return str(self.Class)

    def get_absolute_url(self): # new
        return reverse('routine')



class Contact(models.Model):
    name = models.CharField(max_length=1000, default="")
    query = models.TextField(default="")
    address = models.CharField(max_length = 2000,default="")
    phone_no = models.CharField(max_length = 50,default="")
    email = models.EmailField(max_length = 1000, blank = True, null = True)

    def __str__(self):
        return self.name


class Notice(models.Model):
    title = models.CharField(max_length=100)
    detail = models.CharField(max_length=1000)
    postby = models.CharField(max_length=200)
    date = models.DateField(auto_now=True)
    created_at =models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title



class Staff_Leave_Application(models.Model):
    status_Choice=(
        ('Pending','pending'),
        ('Approved','Approved'),
        ('Rejected','Rejected'),
    )
    s_type=(
        ('sick','sick'),
        ('casual','casual'),
    )
    user=models.CharField(max_length=20)
    reason=models.CharField(max_length=30)
    leave_type = models.CharField(max_length=20,choices=s_type, null=False)
    startdate=models.DateField(default=NepaliDate.today().isoformat())
    endate = models.DateField(default=NepaliDate.today().isoformat())
    received_date = models.DateTimeField(default=NepaliDate.today().isoformat())
    approve=models.CharField(max_length=8,choices = status_Choice,default="Pending")

    def __str__(self):
        return self.user+"'s leave application"

    class Meta:
        ordering = ('-received_date',)