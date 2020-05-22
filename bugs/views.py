from django.shortcuts import render, get_object_or_404
from bugs.models import Ticket, CustomUser
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from bug_tracker import settings
from bugs.forms import TicketForm, LoginForm
from bugs.models import Ticket
from django.utils import timezone


@login_required
def index(request):

    new_tickets = Ticket.objects.filter(status="NEW")
    in_progress_tickets = Ticket.objects.filter(status="IN_PROGRESS")
    completed_tickets = Ticket.objects.filter(status="COMPLETED")
    invalid_tickets = Ticket.objects.filter(status="INVALID")
    context = {
        "new_tickets": new_tickets,
        "in_progress_tickets": in_progress_tickets,
        "completed_tickets": completed_tickets,
        "invalid_tickets": invalid_tickets,
    }
    return render(request, "index.html", context)


@login_required
def newTicketView(request):
    context = {"creator": request.user}
    html = "general_form.html"
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            time = timezone.now()
            ticket = Ticket.objects.create(
                title=data["title"],
                details=data["details"],
                created_by=request.user,
                created_time=time,
                status="NEW",
            )
        return HttpResponseRedirect(
            reverse("ticketDetailPage", kwargs={"id": ticket.id})
        )
    form = TicketForm()
    context["form"] = form
    return render(request, html, context)


@login_required
def ticketDetailView(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    context = {"ticket": ticket}
    return render(request, "ticketDetail.html", context)


@login_required
def assignSelf(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    assign_to = request.user
    ticket.assigned_to = assign_to
    ticket.completed_by = None
    ticket.status = "IN_PROGRESS"
    ticket.save()
    return HttpResponseRedirect(request.GET.get("next", reverse("home")))


@login_required
def editTicket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    html = "general_form.html"
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ticket.title = data["title"]
            ticket.details = data["details"]
            ticket.save()
            return HttpResponseRedirect(request.GET.get("next", reverse("home")))
    form = TicketForm(initial={"title": ticket.title, "details": ticket.details})
    context = {"form": form}
    return render(request, html, context)


def markInvalid(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    ticket.status = "INVALID"
    ticket.assigned_to = None
    ticket.completed_by = None
    ticket.save()

    return HttpResponseRedirect(request.GET.get("next", reverse("home")))


def markCompleted(request, id):
    user = CustomUser.objects.get(username=request.user.username)
    ticket = get_object_or_404(Ticket, id=id)
    if ticket.status == "INVALID":
        ticket.assigned_to = user

    ticket.status = "COMPLETED"
    ticket.completed_by = ticket.assigned_to
    ticket.assigned_to = None
    ticket.save()
    return HttpResponseRedirect(request.GET.get("next", reverse("home")))


@login_required
def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def signupView(request):
    pass


def loginView(request):
    message_after = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data["username"], password=data["password"]
            )
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get("next", reverse("home")))
            else:
                message_after = """Credentials supplied do not match our records.
                    Please try again."""
    form = LoginForm()
    return render(
        request, "general_form.html", {"form": form, "message_after": message_after}
    )


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
    index - has new tickets| in progress tickets | completed tickets (no invalid), sorted.
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
    status - choice field New, In Progress, completed, Invalid - start as new
    created by - many-1 - autocreate - who's logged in
    assigned to - many-1 - start as none, Foreignkey
    completed by - many-1   Foreignkey


"""
