from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def loginView(request):
    pass


def logoutView(request):
    pass


def signupView(request):
    pass


# from django.http import HttpResponseRedirect
# from django.urls import reverse
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import logout, login, authenticate
# from django.shortcuts import render
# from microscope import settings
# from my_user.forms import LoginForm, MyUserForm
# from my_user.models import MyUser


# @login_required
# def index(request):
#     context = {'settings': settings.AUTH_USER_MODEL}
#     return render(request, 'index.html', context)


# def logoutView(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('loginPage'))


# def loginView(request):
#     message_after = ""
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             user = authenticate(
#                 request, username=data['username'], password=data['password'])
#             if user is not None:
#                 login(request, user)
#                 return HttpResponseRedirect(
#                     request.GET.get('next', reverse('home'))
#                 )
#             else:
#                 message_after = """Credentials supplied do not match our records.
#                     Please try again."""
#     form = LoginForm()
#     return render(request, 'general_form.html',
#                   {'form': form, 'message_after': message_after})


# def signupView(request):
#     context = {}
#     if request.method == "POST":
#         form = MyUserForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             new_user = MyUser.objects.create(
#                 username=data['username'],
#                 password=data['password'],
#                 display_name=data['display_name'],
#                 home_page=data['home_page'],
#                 age=data['age']
#             )
#             new_user.set_password(raw_password=data['password'])
#             new_user.save()
#             user = authenticate(
#                 request, username=data['username'], password=data['password']
#             )
#             if user:
#                 login(request, user)
#             return HttpResponseRedirect(reverse('home'))
#         else:
#             context['form'] = form
#     else:
#         form = MyUserForm()
#         context['form'] = form
#     return render(request, 'general_form.html', context)


# @staff_member_required(login_url='/login/?next=/addauthor/')
# def add_author(request):
#     html = "recipes/add_form.html"
#     message_before = """Create a new user/author below.
#       Each user account is associates with exactly one author name."""
#     if request.method == "POST":
#         form = AddAuthorForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             User.objects.create_user(
#                 username=data['username'],
#                 password=data['password']
#             )
#             Author.objects.create(
#                 name=data['author_name'],
#                 bio=data['bio'],
#                 user=User.objects.get(username=data['username'])
#             )
#         return HttpResponseRedirect(reverse('home'))
#     form = AddAuthorForm()
#     return render(request, html, {
#         'form': form, 'message_before': message_before})


# @login_required
# def add_recipe(request):
#     html = "recipes/add_form.html"
#        if request.method == "POST":
#             form = StaffAddRecipeForm(request.POST)
#             if form.is_valid():
#                 data = form.cleaned_data
#                 Recipe.objects.create(
#                     title=data['title'],
#                     author=data['author'],
#                     description=data['description'],
#                     time_required=data['time_required'],
#                     instructions=data['instructions'],
#                 )
#             return HttpResponseRedirect(reverse('home'))
#         form = StaffAddRecipeForm()
#         return render(request, html, {
#             'form': form,
#         })


# def author_detail(request, pk):
#     author = get_object_or_404(Author, pk=pk)
#     recipes = Recipe.objects.filter(
#         author=author).order_by('title')
#     return render(request, 'recipes/author_detail.html', {
#         'author': author, 'recipes': recipes, })


# def loginview(request):
#     message_after = ""
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             user = authenticate(
#                 request, username=data['username'], password=data['password'])
#             if user:
#                 login(request, user)
#                 return HttpResponseRedirect(
#                     request.GET.get('next', reverse('home'))
#                 )
#             else:
#                 message_after = """Credentials supplied do not match our records.
#                     Please try again."""
#     form = LoginForm()
#     return render(request, 'recipes/add_form.html',
#                   {'form': form, 'message_after': message_after})


"""
Templates needed:
    menubar - home, create ticket, logout
    index - has new tickets| in progress tickets | done tickets (no invalid), sorted.
        tickets details to show: 
            title
            assigned to
            reported by
            ticket age
            ticket # (on left)
        needs a title bar for these categories - is there a built in way to show this data?
        look up boostrap
    detail view - 
        has details:
            status
            submitted on:
            reported by:
            completed by:
            assigned to:  (new section popup when assigned?)
        title
        details
        number
        button to do available actions: assign to self / complete / mark invalid / return / edit
        
        
        
        
Views needed
    login
        form: username, password, submit
        needs the next/?= feature
    logout
    signup/new user
    create ticket
    modify ticket
    view specific ticket
        assign ticket
        has edit button
    list of all tickets
        each has edit button
        sorted by ticket status
    user's detail - what they've created, completed, and filed
    mark invalid - sets status to completed, assigns completer as person marking
    




User
    username    charfield
    password    charfield

Ticket
    title   charfield
    details textarea
    created at datetime - autocomplete this
    status - choice field New, In Progress, Done, Invalid - start as new
    created by - many-1 - autocreate - who's logged in
    assigned to - many-1 - start as none, Foreignkey
    completed by - many-1   Foreignkey


"""
