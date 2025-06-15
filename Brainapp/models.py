from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator,MinValueValidator,RegexValidator

class User(AbstractUser):
    Role=[
    ('admin', 'Admin'),
    ('doctor', 'Doctor'),
    ('patient', 'Patient'),
]
    phone_validator = RegexValidator(
    regex=r'^\d{11,15}$',
    message="Phone number must be 10 to 15 digits."
)
    national_id_validator = RegexValidator(
    regex=r'^\d{14}$',
    message="National ID must be exactly 14 digits."
)
    
    national_id =models.CharField(max_length=14 ,unique=True,validators=[national_id_validator],verbose_name="National ID")
    name=models.CharField(max_length=255)
    role=models.CharField(max_length=50,choices=Role)
    Ph_No=models.CharField(max_length=15,validators=[phone_validator])
    email=models.EmailField(unique=True,null=True ,blank=True)
    def __str__( self):
        return self.name
    
class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    specialty=models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.name
    
class Patient(models.Model):
    gender=[
        ('Male','Male'),
        ('Female','Female')
    ]
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    doctor=models.ForeignKey(Doctor,on_delete=models.SET_NULL,null=True ,blank=True)
    gender=models.CharField(max_length=10,choices=gender)
    Age=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(120)])
    
    def __str__(self):
        return self.user.name

class MRI_Image(models.Model):
    doctor=models.ForeignKey(Doctor,on_delete=models.SET_NULL,null=True ,blank=True)
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    image=models.ImageField( upload_to='image/'  ,null=True,blank=True)
    date=models.DateTimeField(auto_now_add=True)
    
class Result(models.Model):
    mri_image=models.OneToOneField(MRI_Image,on_delete=models.CASCADE)
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    doctor=models.ForeignKey(Doctor,on_delete=models.SET_NULL,null=True ,blank=True)
    report=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    
class ContactUs(models.Model):
    issue_type=[
        ('Bug Report','Bug Report'),
        ('Feature Request','Feature Request'),
        ('System Improvment','System Imporvment'),
        ('Other','Other')
        ]
    priority_level=[
        ('Low','Low'),
        ('Medium','Medium'),
        ('High','High'),
        ('Urgent','Urgent')
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    issue_type=models.CharField(max_length=50 ,choices=issue_type)
    issue_title = models.CharField(max_length=255)
    priority_level=models.CharField(max_length=10 ,choices=priority_level)
    message=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    
    