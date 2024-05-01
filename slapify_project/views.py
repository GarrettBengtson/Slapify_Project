from django.shortcuts import render, redirect
from .forms import CreateAccountForm

def create_account(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/slapify')
    else:
        form = CreateAccountForm()

    args = {'form': form}
    return render(request, './registration/create_account.html', args)