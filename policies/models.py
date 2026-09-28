from django.db import models
from django.contrib.auth.models import User


# ============================================================
# CHOICES
# ============================================================

POLICY_TYPES = [
    ('life', 'Life Insurance'),
    ('health', 'Health Insurance'),
    ('auto', 'Auto Insurance'),
    ('property', 'Property Insurance'),
    ('travel', 'Travel Insurance'),
    ('business', 'Business Insurance'),
]

POLICY_STATUS = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('lapsed', 'Lapsed'),
    ('cancelled', 'Cancelled'),
    ('pending', 'Pending'),
]

CLAIM_STATUS = [
    ('pending', 'Pending'),
    ('under_review', 'Under Review'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('paid', 'Paid'),
]

PAYMENT_STATUS = [
    ('pending', 'Pending'),
    ('paid', 'Paid'),
    ('overdue', 'Overdue'),
    ('cancelled', 'Cancelled'),
]

PAYMENT_FREQUENCY = [
    ('monthly', 'Monthly'),
    ('quarterly', 'Quarterly'),
    ('half_yearly', 'Half Yearly'),
    ('yearly', 'Yearly'),
]


# ============================================================
# INSURANCE COMPANY
# ============================================================

class InsuranceCompany(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField(blank=True)
    logo = models.ImageField(
        upload_to='insurance_companies/',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# ============================================================
# INSURANCE PRODUCT
# ============================================================

class InsuranceProduct(models.Model):
    company = models.ForeignKey(
        InsuranceCompany,
        on_delete=models.CASCADE,
        related_name='products'
    )

    name = models.CharField(max_length=200)

    type = models.CharField(
        max_length=20,
        choices=POLICY_TYPES
    )

    description = models.TextField()

    min_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    max_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    premium_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company.name} - {self.name}"


# ============================================================
# CUSTOMER PROFILE
# ============================================================

class CustomerProfile(models.Model):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='customer_profile'
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    date_of_birth = models.DateField()

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES
    )

    phone = models.CharField(max_length=15)

    email = models.EmailField()

    address = models.TextField()

    occupation = models.CharField(
        max_length=100,
        blank=True
    )

    annual_income = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# ============================================================
# AGENT
# ============================================================

class Agent(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='agent_profile'
    )

    agent_code = models.CharField(
        max_length=20,
        unique=True
    )

    company = models.ForeignKey(
        InsuranceCompany,
        on_delete=models.CASCADE,
        related_name='agents'
    )

    phone = models.CharField(max_length=15)

    address = models.TextField()

    license_number = models.CharField(
        max_length=50
    )

    license_expiry = models.DateField()

    commission_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    is_active = models.BooleanField(default=True)

    joined_date = models.DateField(
        auto_now_add=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.agent_code}"


# ============================================================
# POLICY
# ============================================================

class Policy(models.Model):

    policy_number = models.CharField(
        max_length=50,
        unique=True
    )

    policy_type = models.CharField(
        max_length=20,
        choices=POLICY_TYPES
    )

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='policies'
    )

    company = models.ForeignKey(
        InsuranceCompany,
        on_delete=models.CASCADE,
        related_name='policies'
    )

    product = models.ForeignKey(
        InsuranceProduct,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='policies'
    )

    agent = models.ForeignKey(
        Agent,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sold_policies'
    )

    start_date = models.DateField()

    end_date = models.DateField()

    premium_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    sum_insured = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=POLICY_STATUS,
        default='pending'
    )

    payment_frequency = models.CharField(
        max_length=20,
        choices=PAYMENT_FREQUENCY
    )

    next_due_date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.policy_number} - {self.customer.username}"

    class Meta:
        ordering = ['-created_at']


# ============================================================
# CLAIM
# ============================================================

class Claim(models.Model):

    claim_number = models.CharField(
        max_length=50,
        unique=True
    )

    policy = models.ForeignKey(
        Policy,
        on_delete=models.CASCADE,
        related_name='claims'
    )

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='claims'
    )

    claim_date = models.DateField(
        auto_now_add=True
    )

    incident_date = models.DateField()

    incident_description = models.TextField()

    claim_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    approved_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=CLAIM_STATUS,
        default='pending'
    )

    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_claims'
    )

    review_notes = models.TextField(
        blank=True
    )

    payment_date = models.DateField(
        null=True,
        blank=True
    )

    payment_reference = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Claim {self.claim_number} - {self.policy.policy_number}"

    class Meta:
        ordering = ['-created_at']


# ============================================================
# CLAIM DOCUMENT
# ============================================================

class ClaimDocument(models.Model):

    claim = models.ForeignKey(
        Claim,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    document_type = models.CharField(
        max_length=100
    )

    file = models.FileField(
        upload_to='claim_documents/'
    )

    description = models.TextField(
        blank=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.claim.claim_number} - {self.document_type}"


# ============================================================
# PREMIUM PAYMENT
# ============================================================

class PremiumPayment(models.Model):

    policy = models.ForeignKey(
        Policy,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    payment_date = models.DateField()

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=50
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending'
    )

    receipt_number = models.CharField(
        max_length=50,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.policy.policy_number} - {self.payment_date}"

    class Meta:
        ordering = ['-payment_date']


# ============================================================
# COMMISSION
# ============================================================

class Commission(models.Model):

    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name='commissions'
    )

    policy = models.ForeignKey(
        Policy,
        on_delete=models.CASCADE,
        related_name='commissions'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    rate = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    paid_date = models.DateField(
        null=True,
        blank=True
    )

    payment_reference = models.CharField(
        max_length=100,
        blank=True
    )

    is_paid = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.agent.agent_code} - {self.policy.policy_number}"


# ============================================================
# POLICY RENEWAL
# ============================================================

class PolicyRenewal(models.Model):

    policy = models.ForeignKey(
        Policy,
        on_delete=models.CASCADE,
        related_name='renewals'
    )

    renewal_date = models.DateField()

    new_premium = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    old_premium = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    is_renewed = models.BooleanField(
        default=False
    )

    renewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.policy.policy_number} - {self.renewal_date}"