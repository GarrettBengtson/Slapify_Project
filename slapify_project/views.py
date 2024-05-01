from django.shortcuts import render, redirect
from .forms import CreateAccountForm

def create_account(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_account_success')
    else:
        form = CreateAccountForm()

    args = {'form': form}
    return render(request, './registration/create_account.html', args)

def create_account_success(request):
    return render(request, './registration/create_account_success.html')