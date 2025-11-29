from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.
def get_default_menu() -> tuple:
    return (
        {'url': '/', 'text': 'Главная'},
        {'url': '/bot', 'text': 'Про бота'},
        {'url': '/commands', 'text': 'Команды бота'}, 
        {'url': '/payment', 'text': 'Пожертвовать деньги'},
    )

def index_page(request: HttpRequest) -> HttpResponse:
    context = {'menu': get_default_menu(), 'page_name': 'Робот мультик математика'}
    return render(request, 'pages/index.html', context)

def commands_page(request: HttpRequest) -> HttpResponse:
    context = {'menu': get_default_menu(), 'page_name': 'Команды бота'}
    return render(request, 'pages/bot_commands.html', context)
    
def payment_page(request: HttpRequest) -> HttpResponse:
    context = {'menu': get_default_menu(), 'page_name': 'Пожертвование'}
    return render(request, 'pages/payment.html', context)
    
def about_page(request: HttpRequest) -> HttpResponse:
    context = {'menu': get_default_menu(), 'page_name': 'О нас'}
    return render(request, 'pages/about.html', context)
    
def bot_page(request: HttpRequest) -> HttpResponse:
    context = {'menu': get_default_menu(), 'page_name': 'О боте'}
    return render(request, 'pages/bot.html', context)
