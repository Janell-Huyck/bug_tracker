from django.shortcuts import render, get_object_or_404
from bugs.models import Ticket, CustomUser
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from bug_tracker import settings
from bugs.forms import TicketForm, LoginForm, CustomUserForm
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
        return HttpResponseRedirect(reverse("ticketDetail", kwargs={"id": ticket.id}))
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
def returnTicket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    ticket.assigned_to = None
    ticket.completed_by = None
    ticket.status = "NEW"
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


@login_required
def markInvalid(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    ticket.status = "INVALID"
    ticket.assigned_to = None
    ticket.completed_by = None
    ticket.save()

    return HttpResponseRedirect(request.GET.get("next", reverse("home")))


@login_required
def markCompleted(request, id):
    user = CustomUser.objects.get(username=request.user.username)
    ticket = get_object_or_404(Ticket, id=id)
    if ticket.status == "INVALID":
        ticket.assigned_to = user
    if ticket.assigned_to is None:
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


@login_required
def newUser(request):
    context = {}
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = CustomUser.objects.create(
                username=data["username"],
                password=data["password"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                tag_line=data["tag_line"],
            )
            new_user.set_password(raw_password=data["password"])
            new_user.save()
            user = authenticate(
                request, username=data["username"], password=data["password"]
            )
            if user:
                login(request, user)
            return HttpResponseRedirect(reverse("home"))

    else:
        form = CustomUserForm()
        context["form"] = form
    return render(request, "general_form.html", context)


def userDetail(request, id):
    user = CustomUser.objects.get(id=id)
    context = {"user": user}
    context["created_tickets"] = Ticket.objects.filter(created_by=user)
    context["assigned_tickets"] = Ticket.objects.filter(assigned_to=user)
    context["completed_tickets"] = Ticket.objects.filter(completed_by=user)

    return render(request, "userDetail.html", context)
