from django.shortcuts import render ,redirect
from .models import User,Patient ,ContactUs,MRI_Image
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login ,logout
from django.contrib import messages
from django.db import transaction


# Create your views here.


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('UserName')
        national_id = request.POST.get('National_id') 
        name = request.POST.get('Name')
        age = request.POST.get('Age')
        gender = request.POST.get('Gender')
        email = request.POST.get('Email')
        Ph_No = request.POST.get('Phone')
        
        print("POST data:", request.POST)
        print("Parsed:", username, national_id, name, age, gender, email, Ph_No)

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('signup')
        
        if User.objects.filter(national_id=national_id).exists():
            messages.error(request, 'National ID already exists.')
            return redirect('signup')
        
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    national_id=national_id,
                    name=name,
                    role='patient',
                    Ph_No=Ph_No,
                    email=email
                )
                user.save()
                print("User created:", user)

                patient = Patient.objects.create(
                    user=user,
                    gender=gender.capitalize(),
                    Age=int(age)
                )
                print("Patient created:", patient)

                messages.success(request, 'Patient registered successfully.')
                return redirect('Admin_dashboard')

        except Exception as e:
            print("Error during signup:", str(e))
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('signup')

    return render(request, 'Brainapp/signup-patient.html')





def loginpage(request):
    if request.method=='POST':
        national_id=request.POST.get('national_id')
        name =request.POST.get('name')
        print(f"POST data: {request.POST}")
        try:
            user = User.objects.get( national_id=national_id,name=name )
            login(request, user)
            print(f"User authenticated: {user.name}, Role: {user.role}")
            
            if user.role=='admin':
                return redirect('Admin_dashboard')
            if user.role=='doctor':
                return redirect('Doctor_dashboard')
            else:
                messages.error(request, 'Invalid role. Please contact support.')
                print("Invalid role detected")  
                return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'Invalid name or national ID.')
            return redirect('login')
    return render(request, 'Brainapp/index.html')

def logoutpage(request):
    logout(request)
    return redirect('login')



def admin_dashboard(request):
    return render(request , 'Brainapp/receptionist-home.html',{'staff_name': request.user.name})


def doctor_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request , 'Brainapp/doctor-home.html',{'staff_name': request.user.name})

@login_required(login_url='login/')
def mri_analysis(request):
    if request.method == 'POST':
        doctor = request.user.doctor  
        national_id = request.POST.get('national_id')
        image = request.FILES.get('mriImage')

        if not national_id or not image:
            messages.error(request, "All fields are required.")
            return redirect('mri_analysis')

        try:
            user = User.objects.get(national_id=national_id, role='patient')
            patient = Patient.objects.get(user=user)
            
            mri = MRI_Image.objects.create(
                doctor=doctor,
                patient=patient,
                image=image
            )
            mri.save()
            messages.success(request, "MRI uploaded successfully.")
            return redirect('Doctor_dashboard')
        except User.DoesNotExist:
            messages.error(request, "No patient found with this National ID.")
            return redirect('mri_analysis')
        except Patient.DoesNotExist:
            messages.error(request, "This user is not registered as a patient.")
            return redirect('mri_analysis')

    
    patients = Patient.objects.all()
    context={'patients':patients}
    return render (request ,'Brainapp/mri-analysis.html',context )

@login_required(login_url='login/')
def patient_data(request):
    
    patients = Patient.objects.all()
    selected_patient = None

    if request.method == 'POST':
        national_id = request.POST.get('national_id')
        if national_id:
            try:
                user = User.objects.get(national_id=national_id)
                selected_patient = Patient.objects.get(user=user)
            except User.DoesNotExist:
                messages.error(request, "No user with this National ID.")
            except Patient.DoesNotExist:
                messages.error(request, "This user is not registered as a patient.")

    context = {
        'patients': patients,
        'selected_patient': selected_patient
    }
    return render(request, 'Brainapp/patient-data.html',context)

@login_required(login_url='login/')
def contact_dev(request):
    if request.method=='POST':
        id=request.POST.get('staffId')
        issue_type=request.POST.get('issueType')
        issue_title = request.POST.get('issueTitle')
        priority_level=request.POST.get('priority_level')
        message=request.POST.get('issueDescription')
        print(request.POST)
        
        try:
            user = User.objects.get(national_id=id)
        except User.DoesNotExist:
            user = None

        if user:
            ContactUs.objects.create(
                user=user,
                issue_type=issue_type,
                issue_title=issue_title,
                message=message,
                priority_level=priority_level
            )
            
            return redirect('issue_submitted')
    return render(request,'Brainapp/contact-dev.html',{'user': request.user})


def issue_submitted_success(request):
    return render(request, 'Brainapp/issue_success.html')
