from django.db import models
from django.contrib.auth.models import AbstractUser ,BaseUserManager
from django.core.validators import MaxValueValidator,MinValueValidator,RegexValidator
class UserManager(BaseUserManager):
    def create_user(self, national_id, name, password=None, **extra_fields):
        if not national_id:
            raise ValueError('The National ID must be set')
        user = self.model(national_id=national_id, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, national_id, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(national_id, name, password, **extra_fields)
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
        regex=r'^((D|R)\d{3}|\d{14})$',  # allows D###, R###, or 14-digit patient ID
        message="ID must be D### for doctors, R### for admins, or 14-digit for patients."
    )

    username = None   
    national_id =models.CharField(max_length=14 ,unique=True,validators=[national_id_validator],verbose_name="National ID")
    name=models.CharField(max_length=255)
    email=models.EmailField(unique=True,null=True ,blank=True)
    role=models.CharField(max_length=50,choices=Role)
    Ph_No=models.CharField( unique=True,max_length=15,validators=[phone_validator])
    
    USERNAME_FIELD = 'national_id'
    REQUIRED_FIELDS = ['name']
    objects = UserManager()

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
    
    