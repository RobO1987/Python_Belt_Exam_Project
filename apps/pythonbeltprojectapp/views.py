from django.shortcuts import render,HttpResponse, redirect
import bcrypt
from django.contrib import messages
from .models import Userinfo, Quotecontribute, Quotefavorites
import re
from django.core.urlresolvers import reverse

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
ALPHA_REGEX = re.compile(r'^[A-Za-z]+$')

def index(request):
    if 'name' in request.session:
        return redirect('pythonbelt:quotes')
    else:
        return render (request,'pythonbeltprojectapp/index.html')

def register(request):
    nologinerrors = True

    if len(request.POST['Name']) < 2:
        messages.add_message(request, messages.ERROR, "Your name is too short")
        nologinerrors = False

    if not EMAIL_REGEX.match(request.POST['Email']):
        messages.add_message(request, messages.ERROR, "Your email is not in a valid format")
        notloginerrors = False

    if request.POST['Password'] < 8:
        messages.add_message(request, messages.ERROR, "your password is too short")
        nologinerrors = False

    if request.POST['Password'] != request.POST['ConfirmPW']:
        messages.add_message(request, messages.ERROR, "your passwords don't match")
        nologinerrors = False

    email = request.POST['Email']
    if Userinfo.objects.filter(email = email).exists():
        messages.add_message(request, messages.ERROR, "your email already exists in the database")
        nologinerrors = False

    if nologinerrors == False:
        return redirect ('pythonbelt:index')

    else :
        hashpw = bcrypt.hashpw(request.POST['Password'].encode(), bcrypt.gensalt())

        Userinfo.objects.create(name = request.POST['Name'],alias =  request.POST['Alias'], email = request.POST['Email'], password = hashpw,)

        request.session['name'] = request.POST['Name']

        return redirect ('pythonbelt:quotes')

def login(request):
    email = request.POST['Email']
    password = request.POST['Password']

    try:
        user = Userinfo.objects.get(email = email)
        hashpw = bcrypt.hashpw(password.encode(), user.password.encode())
        ###Check w/Fiaz on why the password validation doesn't work...doesn't actually hit the "except" statement...###
        if hashpw == user.password:
            user = Userinfo.objects.get(email = email)
            request.session['name'] = user.name
            request.session['id'] = user.id
            return redirect ('pythonbelt:quotes')
        else:
            pass
    except:
        messages.add_message(request, messages.ERROR, "Invalid login or password")
        return redirect('pythonbelt:index')

def quotecontribute (request):
    nologinerrors = True
    user = Userinfo.objects.get (name = request.session['name'])

    if len(request.POST['quotemessage']) < 1:
        messages.add_message(request, messages.ERROR, "You have no quote dummy")
        nologinerrors = False

    if len(request.POST['quoteauthor']) < 1:
        messages.add_message(request, messages.ERROR, "You didn't put a quote author in idiot")
        nologinerrors = False

    if nologinerrors == False:
        return redirect ('pythonbelt:quotes')

    else:
        Quotecontribute.objects.create(quoteauthor = request.POST['quoteauthor'],quotemessage = request.POST['quotemessage'], user = user)
        return redirect ('pythonbelt:quotes')

def quotes(request):
    context = {
    "quotes" : Quotecontribute.objects.all(),
    "favquotes" : Quotefavorites.objects.filter(userfav_id = request.session['id'])
    }
    return render (request,'pythonbeltprojectapp/quotes.html', context)

def favquote(request, quote_id):
    quotes = Quotecontribute.objects.get(id = quote_id)

    Quotefavorites.objects.create(quoteauthorfav = quotes.quoteauthor, quotemessagefav = quotes.quotemessage, quote_id = quotes.id ,userfav_id = request.session['id'] )
    ###running issue into the above earlier...will need to understand why I was having trouble with the "quote_id" and "userfav_id" issue...had something to do with ".get" vs. ".filter"
    return redirect ('pythonbelt:quotes')

def quoteuser(request, quote_user_id):
    usersubmissions = Userinfo.objects.filter(id = quote_user_id)
    quotecount = Quotecontribute.objects.filter (user = quote_user_id).count()

    context = {
    'quoteuser' : usersubmissions,
    'quotecount' : quotecount
    }

    return render (request,'pythonbeltprojectapp/userpage.html', context)

def remove (request, fav_id):
    Quotefavorites.objects.filter(id = fav_id).delete()
    return redirect ('pythonbelt:quotes')

def clearsession(request):
    request.session.clear()
    return redirect ('pythonbelt:index')
