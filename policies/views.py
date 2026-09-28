from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from openpyxl import Workbook

from .models import (
    CustomerProfile,
    Policy,
    Claim,
    PremiumPayment,
    PolicyRenewal,
    Agent,
)


# ============================================================
# CUSTOMER REGISTRATION FORM
# ============================================================

class CustomerRegistrationForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Create a password'
            }
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm your password'
            }
        )
    )

    def clean_username(self):

        username = self.cleaned_data['username']

        if User.objects.filter(
            username=username
        ).exists():

            raise forms.ValidationError(
                'This username is already taken.'
            )

        return username

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get(
            'confirm_password'
        )

        if password and confirm_password:

            if password != confirm_password:

                raise forms.ValidationError(
                    'Passwords do not match.'
                )

        return cleaned_data


# ============================================================
# CUSTOMER PROFILE FORM
# ============================================================

class CustomerProfileForm(forms.ModelForm):

    class Meta:

        model = CustomerProfile

        fields = [
            'first_name',
            'last_name',
            'date_of_birth',
            'gender',
            'phone',
            'email',
            'address',
            'occupation',
            'annual_income',
        ]

        widgets = {

            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'date_of_birth': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'gender': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'address': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),

            'occupation': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'annual_income': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


# ============================================================
# LOGIN
# ============================================================

def login_view(request):

    if request.user.is_authenticated:

        return redirect('dashboard')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                'Login successful!'
            )

            return redirect('dashboard')

        else:

            messages.error(
                request,
                'Invalid username or password.'
            )

    return render(
        request,
        'policies/login.html'
    )


# ============================================================
# REGISTER
# ============================================================

def register_view(request):

    if request.user.is_authenticated:

        return redirect('dashboard')

    if request.method == 'POST':

        form = CustomerRegistrationForm(
            request.POST
        )

        if form.is_valid():

            username = form.cleaned_data[
                'username'
            ]

            email = form.cleaned_data[
                'email'
            ]

            password = form.cleaned_data[
                'password'
            ]

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            CustomerProfile.objects.create(
                user=user,
                first_name=username,
                last_name='',
                date_of_birth='2000-01-01',
                gender='O',
                phone='',
                email=email,
                address=''
            )

            messages.success(
                request,
                'Account created successfully. Please login.'
            )

            return redirect('login')

    else:

        form = CustomerRegistrationForm()

    return render(
        request,
        'policies/register.html',
        {
            'form': form
        }
    )


# ============================================================
# LOGOUT
# ============================================================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        'You have been logged out successfully.'
    )

    return redirect('login')


# ============================================================
# DASHBOARD
# ============================================================

@login_required(login_url='login')
def dashboard(request):

    user = request.user

    policy_count = Policy.objects.filter(
        customer=user
    ).count()

    claim_count = Claim.objects.filter(
        customer=user
    ).count()

    payment_count = PremiumPayment.objects.filter(
        policy__customer=user
    ).count()

    renewal_count = PolicyRenewal.objects.filter(
        policy__customer=user
    ).count()

    context = {

        'policy_count': policy_count,

        'claim_count': claim_count,

        'payment_count': payment_count,

        'renewal_count': renewal_count,

    }

    return render(
        request,
        'policies/dashboard.html',
        context
    )


# ============================================================
# CUSTOMER PROFILE
# ============================================================

@login_required(login_url='login')
def profile_view(request):

    try:
        profile = CustomerProfile.objects.get(
            user=request.user
        )

    except CustomerProfile.DoesNotExist:

        profile = None

    return render(
        request,
        'policies/profile.html',
        {
            'profile': profile
        }
    )
# ============================================================
# POLICY LIST
# ============================================================

@login_required(login_url='login')
def policy_list(request):

    policies = Policy.objects.filter(
        customer=request.user
    ).select_related(
        'company'
    )

    return render(
        request,
        'policies/policy_list.html',
        {
            'policies': policies
        }
    )


# ============================================================
# POLICY DETAILS
# ============================================================

@login_required(login_url='login')
def policy_detail(
    request,
    policy_id
):

    policy = Policy.objects.filter(
        id=policy_id,
        customer=request.user
    ).select_related(
        'company'
    ).first()

    if policy is None:

        messages.error(
            request,
            'Policy not found.'
        )

        return redirect(
            'policy_list'
        )

    claims = policy.claims.all()

    payments = policy.payments.all()

    renewals = policy.renewals.all()

    context = {

        'policy': policy,

        'claims': claims,

        'payments': payments,

        'renewals': renewals,

    }

    return render(
        request,
        'policies/policy_detail.html',
        context
    )
@login_required(login_url='login')
def payment_list(request):

    payments = PremiumPayment.objects.filter(
        policy__customer=request.user
    ).select_related(
        'policy'
    )

    return render(
        request,
        'policies/payment_list.html',
        {
            'payments': payments
        }
    )
@login_required(login_url='login')
def agent_list(request):

    agents = Agent.objects.filter(
        is_active=True
    ).select_related(
        'user',
        'company'
    )

    return render(
        request,
        'policies/agent_list.html',
        {
            'agents': agents
        }
    )
@login_required(login_url='login')
def renewal_list(request):

    renewals = PolicyRenewal.objects.filter(
        policy__customer=request.user
    ).select_related(
        'policy'
    )

    return render(
        request,
        'policies/renewal_list.html',
        {
            'renewals': renewals
        }
    )
@login_required(login_url='login')
def reports(request):

    user = request.user

    policies = Policy.objects.filter(
        customer=user
    )

    claims = Claim.objects.filter(
        customer=user
    )

    payments = PremiumPayment.objects.filter(
        policy__customer=user
    )

    renewals = PolicyRenewal.objects.filter(
        policy__customer=user
    )

    total_policies = policies.count()

    active_policies = policies.filter(
        status='active'
    ).count()

    total_claims = claims.count()

    approved_claims = claims.filter(
        status='approved'
    ).count()

    paid_claims = claims.filter(
        status='paid'
    ).count()

    total_premium = sum(
        payment.amount
        for payment in payments
        if payment.status == 'paid'
    )

    total_claim_amount = sum(
        claim.claim_amount
        for claim in claims
    )

    total_approved_amount = sum(
        claim.approved_amount
        for claim in claims
    )

    context = {

        'total_policies': total_policies,

        'active_policies': active_policies,

        'total_claims': total_claims,

        'approved_claims': approved_claims,

        'paid_claims': paid_claims,

        'total_premium': total_premium,

        'total_claim_amount': total_claim_amount,

        'total_approved_amount': total_approved_amount,

        'renewal_count': renewals.count(),

    }

    return render(
        request,
        'policies/reports.html',
        context
    )
@login_required(login_url='login')
def reports_pdf(request):

    user = request.user

    policies = Policy.objects.filter(
        customer=user
    )

    claims = Claim.objects.filter(
        customer=user
    )

    payments = PremiumPayment.objects.filter(
        policy__customer=user,
        status='paid'
    )

    total_policies = policies.count()

    active_policies = policies.filter(
        status='active'
    ).count()

    total_claims = claims.count()

    total_premium = sum(
        payment.amount
        for payment in payments
    )

    total_claim_amount = sum(
        claim.claim_amount
        for claim in claims
    )

    total_approved_amount = sum(
        claim.approved_amount
        for claim in claims
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="insurance_report.pdf"'

    pdf = canvas.Canvas(response)

    pdf.setTitle("Insurance Report")

    pdf.drawString(
        50,
        800,
        "INSURANCE MANAGEMENT REPORT"
    )

    pdf.drawString(
        50,
        770,
        f"Customer: {user.username}"
    )

    pdf.drawString(
        50,
        730,
        f"Total Policies: {total_policies}"
    )

    pdf.drawString(
        50,
        700,
        f"Active Policies: {active_policies}"
    )

    pdf.drawString(
        50,
        670,
        f"Total Claims: {total_claims}"
    )

    pdf.drawString(
        50,
        640,
        f"Paid Premium: Rs. {total_premium}"
    )

    pdf.drawString(
        50,
        610,
        f"Total Claim Amount: Rs. {total_claim_amount}"
    )

    pdf.drawString(
        50,
        580,
        f"Approved Claim Amount: Rs. {total_approved_amount}"
    )

    pdf.drawString(
        50,
        530,
        "Generated by Insurance Management System"
    )

    pdf.save()

    return response
@login_required(login_url='login')
def reports_excel(request):

    user = request.user

    policies = Policy.objects.filter(
        customer=user
    )

    claims = Claim.objects.filter(
        customer=user
    )

    payments = PremiumPayment.objects.filter(
        policy__customer=user
    )

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Insurance Report"

    sheet.append([
        "Insurance Management Report"
    ])

    sheet.append([])

    sheet.append([
        "Policy Number",
        "Policy Type",
        "Start Date",
        "End Date",
        "Premium",
        "Status"
    ])

    for policy in policies:

        sheet.append([
            policy.policy_number,
            policy.get_policy_type_display(),
            policy.start_date,
            policy.end_date,
            float(policy.premium_amount),
            policy.get_status_display()
        ])

    sheet.append([])

    sheet.append([
        "Claims"
    ])

    sheet.append([
        "Claim Number",
        "Policy",
        "Claim Amount",
        "Approved Amount",
        "Status"
    ])

    for claim in claims:

        sheet.append([
            claim.claim_number,
            claim.policy.policy_number,
            float(claim.claim_amount),
            float(claim.approved_amount),
            claim.get_status_display()
        ])

    sheet.append([])

    sheet.append([
        "Premium Payments"
    ])

    sheet.append([
        "Policy",
        "Payment Date",
        "Amount",
        "Payment Method",
        "Status"
    ])

    for payment in payments:

        sheet.append([
            payment.policy.policy_number,
            payment.payment_date,
            float(payment.amount),
            payment.payment_method,
            payment.get_status_display()
        ])

    response = HttpResponse(
        content_type=(
            'application/vnd.openxmlformats-officedocument'
            '.spreadsheetml.sheet'
        )
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="insurance_report.xlsx"'

    workbook.save(response)

    return response