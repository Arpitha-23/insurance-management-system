from django.contrib import admin

from .models import (
    InsuranceCompany,
    InsuranceProduct,
    CustomerProfile,
    Agent,
    Policy,
    Claim,
    ClaimDocument,
    PremiumPayment,
    Commission,
    PolicyRenewal,
)


@admin.register(InsuranceCompany)
class InsuranceCompanyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'code',
        'phone',
        'email',
        'is_active',
    )
    search_fields = ('name', 'code', 'email')
    list_filter = ('is_active',)


@admin.register(InsuranceProduct)
class InsuranceProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'company',
        'type',
        'premium_rate',
        'is_active',
    )
    search_fields = ('name',)
    list_filter = ('type', 'is_active')


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'user',
        'phone',
        'email',
    )
    search_fields = (
        'first_name',
        'last_name',
        'phone',
        'email',
    )


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = (
        'agent_code',
        'user',
        'company',
        'license_number',
        'commission_rate',
        'is_active',
    )
    search_fields = (
        'agent_code',
        'license_number',
        'user__username',
    )
    list_filter = ('company', 'is_active')


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = (
        'policy_number',
        'policy_type',
        'customer',
        'company',
        'agent',
        'premium_amount',
        'status',
        'next_due_date',
    )
    search_fields = (
        'policy_number',
        'customer__username',
    )
    list_filter = (
        'policy_type',
        'status',
        'company',
    )


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = (
        'claim_number',
        'policy',
        'customer',
        'claim_amount',
        'approved_amount',
        'status',
        'claim_date',
    )
    search_fields = (
        'claim_number',
        'policy__policy_number',
    )
    list_filter = ('status',)


@admin.register(ClaimDocument)
class ClaimDocumentAdmin(admin.ModelAdmin):
    list_display = (
        'claim',
        'document_type',
        'uploaded_at',
    )
    search_fields = (
        'claim__claim_number',
        'document_type',
    )


@admin.register(PremiumPayment)
class PremiumPaymentAdmin(admin.ModelAdmin):
    list_display = (
        'policy',
        'payment_date',
        'amount',
        'payment_method',
        'status',
        'transaction_id',
    )
    search_fields = (
        'policy__policy_number',
        'transaction_id',
        'receipt_number',
    )
    list_filter = ('status', 'payment_method')


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = (
        'agent',
        'policy',
        'amount',
        'rate',
        'is_paid',
        'paid_date',
    )
    search_fields = (
        'agent__agent_code',
        'policy__policy_number',
    )
    list_filter = ('is_paid',)


@admin.register(PolicyRenewal)
class PolicyRenewalAdmin(admin.ModelAdmin):
    list_display = (
        'policy',
        'renewal_date',
        'old_premium',
        'new_premium',
        'is_renewed',
    )
    search_fields = ('policy__policy_number',)
    list_filter = ('is_renewed',)