from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Reimbursement

@login_required
def home(request):
    if request.method == 'POST':
        ad_type = request.POST.get('ad_type')
        count = request.POST.get('count')
        spend = request.POST.get('spend')

        if count and count.isdigit():
            count = int(count)
        else:
            count = 0
        try:
            spend = float(spend)
        except ValueError:
            spend = 0.0

        reimbursement = Reimbursement()
        reimbursement.add_ad(ad_type, count, spend)

        all_ads_data = []
        for ad_type, ad_info in reimbursement.ads.items():
            if ad_info['count'] > 0:
                cost_share = ad_info['cost_share_rate'] * ad_info['actual_spend']
                reimbursement_value = count * ad_info['cost_share_rate'] * spend

                all_ads_data.append({
                    'ad_type': ad_type,
                    'count': ad_info['count'],
                    'date':  ad_info['date'],
                    'actual_spend': ad_info['actual_spend'],
                    'cost_share': cost_share,
                    'reimbursement': reimbursement_value
                })

        context = {
            'all_ads_data': all_ads_data
        }

        return render(request, 'reimbursement_app/home.html', context)
    else:
        return render(request, 'reimbursement_app/home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'reimbursement_app/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'reimbursement_app/signup.html', {'form': form})
