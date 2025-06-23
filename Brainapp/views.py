import re
from django.shortcuts import render ,redirect
from django.http  import HttpResponseForbidden
from .models import User,Patient ,ContactUs,MRI_Image,Result
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login ,logout
from django.contrib import messages
from django.db import transaction
from django.views.decorators.csrf import requires_csrf_token


# Create your views here.
@requires_csrf_token
def custom_csrf_failure(request, reason=""):
    from django.contrib import messages
    messages.error(request, "You are not authenticated or your session expired.", extra_tags='csrf')
    return redirect('login')

@login_required(login_url='/')
def signup(request):
    if request.user.role != 'admin':
        return redirect('login')
    
    if request.method == 'POST':
        national_id = request.POST.get('National_id') 
        name = request.POST.get('Name')
        age = request.POST.get('Age')
        gender = request.POST.get('Gender')
        email = request.POST.get('Email')
        Ph_No = request.POST.get('Phone')
        
        print("POST data:", request.POST)

        if not re.fullmatch(r'^\d{14}$', national_id):
            messages.error(request, 'National ID must be exactly 14 digits.', extra_tags='signup')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.', extra_tags='signup')
            return redirect('signup')
        if User.objects.filter(Ph_No=Ph_No).exists():
            messages.error(request, 'Phone Number already exists.', extra_tags='signup')
            return redirect('signup')
        if User.objects.filter(national_id=national_id).exists():
            messages.error(request, 'National ID already exists.', extra_tags='signup')
            return redirect('signup')
        
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    national_id=national_id,
                    name=name,
                    role='patient',
                    Ph_No=Ph_No,
                    email=email
                )
                print("User created:", user)

                patient = Patient.objects.create(
                    user=user,
                    gender=gender.capitalize(),
                    Age=int(age)
                )
                print("Patient created:", patient)

                messages.success(request, 'Patient registered successfully.', extra_tags='signup')
                return redirect('signup')

        except Exception as e:
            print("Error during signup:", str(e))
            messages.error(request, f'An error occurred: {str(e)}', extra_tags='signup')
            return redirect('signup')

    return render(request, 'Brainapp/signup-patient.html')


###################################################################

def loginpage(request):
    if request.method == 'POST':
        national_id = request.POST.get('national_id')
        name = request.POST.get('name')
        print(f"POST data: {request.POST}")

        # Detect role from ID format
        if re.fullmatch(r'^D\d{3}$', national_id):
            expected_role = 'doctor'
        elif re.fullmatch(r'^R\d{3}$', national_id):
            expected_role = 'admin'
        elif re.fullmatch(r'^\d{14}$', national_id):
            messages.error(request, 'Invalid ID or Name.', extra_tags='login')
            return redirect('login')
        else:
            messages.error(request, 'Invalid ID format. Use D### for doctors or R### for receptionist.', extra_tags='login')
            return redirect('login')

        try:
            # Match user with both national_id and name and expected role
            user = User.objects.get(national_id=national_id, name=name, role=expected_role)
            login(request, user)
            print(f"User authenticated: {user.name}, Role: {user.role}")

            if expected_role == 'admin':
                return redirect('Admin_dashboard')
            else:
                return redirect('Doctor_dashboard')

        except User.DoesNotExist:
            messages.error(request, 'Invalid credentials. Please check your ID and name.', extra_tags='login')
            return redirect('login')

    return render(request, 'Brainapp/index.html')

########################################################################################

def logoutpage(request):
    logout(request)
    return redirect('login')

##########################################################################################
@login_required(login_url='/')
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('login')
    return render(request , 'Brainapp/receptionist-home.html',{'staff_name': request.user.name})
####################################################################################################
@login_required(login_url='/')
def doctor_dashboard(request):
    if request.user.role != 'doctor':
        return redirect('login')
    return render(request , 'Brainapp/doctor-home.html',{'staff_name': request.user.name})
#####################################################################################################
@login_required(login_url='/')
def mri_analysis(request):
    
    if request.user.role != 'doctor':
        return redirect('login')
    
    if request.method == 'POST':
        doctor = request.user.doctor  
        national_id = request.POST.get('national_id')
        image = request.FILES.get('mriImage')

        if not national_id or not image:
            messages.error(request, "All fields are required.",extra_tags='mri')
            return redirect('mri_analysis')

        try:
            user = User.objects.get(national_id=national_id)
            patient = Patient.objects.get(user=user)
            
            mri = MRI_Image.objects.create(
                doctor=doctor,
                patient=patient,
                image=image
            )
            mri.save()
            messages.success(request, "MRI uploaded successfully.",extra_tags='mri')
            return redirect('mri_analysis')
            
        except User.DoesNotExist:
            messages.error(request, "No User found with this National ID.",extra_tags='mri')
            return redirect('mri_analysis')
        except Patient.DoesNotExist:
            messages.error(request, "This user is not registered as a patient.",extra_tags='mri')
            return redirect('mri_analysis')
    patients = Patient.objects.all()
    context={'patients':patients}
    return render (request ,'Brainapp/mri-analysis.html',context )
####################################################################################################


@login_required(login_url='/')
def patient_data(request):
    if request.user.role not in ['admin', 'doctor']:
        return redirect('login') 
    patients = Patient.objects.all()
    selected_patient = None

    if request.method == 'POST':
        national_id = request.POST.get('national_id')
        if national_id:
            try:
                user = User.objects.get(national_id=national_id)
                selected_patient = Patient.objects.get(user=user)
                results = Result.objects.filter(patient=selected_patient).order_by('-date')
            except User.DoesNotExist:
                messages.error(request, "No user with this National ID.",extra_tags='patient')
            except Patient.DoesNotExist:
                messages.error(request, "This user is not registered as a patient.",extra_tags='patient')
        

    context = {
        'patients': patients,
        'selected_patient': selected_patient,
        'results': results if selected_patient else []
    }
    
    return render(request, 'Brainapp/patient-data.html',context)
########################################################################


@login_required(login_url='/')
def contact_dev(request):
    if request.user.role not in ['admin', 'doctor']:
        return redirect('login') 
    
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

######################################################################################
def issue_submitted_success(request):
    return render(request, 'Brainapp/issue_success.html')