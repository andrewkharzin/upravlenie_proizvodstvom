from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required



def login_view(request):
    page_title = "Вход в систему"
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Replace 'home' with your desired homepage URL name
    else:
        form = AuthenticationForm()
    
    context = {
        'page_title': page_title,
        'form': form
    }

    return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def session_lock_view(request):
    if request.method == 'POST':
        if 'unlock' in request.POST:
            return redirect('home')  # Replace 'home' with your desired homepage URL name
        elif 'logout' in request.POST:
            logout(request)
            return redirect('login')
    return render(request, 'accounts/session_lock.html')


# def telegram_login(request):
#     # Получаем сообщение от Telegram бота
#     message = request.POST.get('message', '')
    
#     if message == '/login':
#         # Выполняем вход в Django
#         user = authenticate(username='telegram_user', password='telegram_password')
#         if user is not None:
#             login(request, user)
#             return HttpResponse('Вход выполнен')
#         else:
#             return HttpResponse('Ошибка входа')