from django.urls import path
from . import views


urlpatterns = [

    # Login
    path(
        '',
        views.login_view,
        name='login'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    # Registration
    path(
        'register/',
        views.register_view,
        name='register'
    ),

    # Logout
    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # Dashboard
    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    # Customer Profile
    path(
        'profile/',
        views.profile_view,
        name='profile'
    ),

    # Policy List
    path(
        'policies/',
        views.policy_list,
        name='policy_list'
    ),

    # Policy Details
    path(
        'policies/<int:policy_id>/',
        views.policy_detail,
        name='policy_detail'
    ),
    path(
    'payments/',
    views.payment_list,
    name='payment_list'
),
path(
    'agents/',
    views.agent_list,
    name='agent_list'
),
path(
    'renewals/',
    views.renewal_list,
    name='renewal_list'
),
path(
    'reports/',
    views.reports,
    name='reports'
),
path(
    'reports/pdf/',
    views.reports_pdf,
    name='reports_pdf'
),

path(
    'reports/excel/',
    views.reports_excel,
    name='reports_excel'
),
]