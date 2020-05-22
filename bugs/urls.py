from django.urls import path
from bugs import views


urlpatterns = [
    path("", views.index, name="home"),
    path("login_page/", views.loginView, name="login"),
    path("logout_page/", views.logoutView, name="logout"),
    path("tickets/new/", views.newTicketView, name="newTicketPage"),
    path("tickets/detail/<int:id>/", views.ticketDetailView, name="ticketDetail"),
    path("tickets/edit/<int:id>/assign_self", views.assignSelf, name="assignSelf"),
    path("tickets/edit/<int:id>/", views.editTicket, name="editTicket"),
    path("tickets/edit/<int:id>/markInvalid/", views.markInvalid, name="markInvalid"),
    path(
        "tickets/edit/<int:id>/mark_completed/",
        views.markCompleted,
        name="markCompleted",
    ),
    path("users/new/", views.newUser, name="newUser"),
    path("users/detail/<int:id>/", views.userDetail, name="userDetail"),
    path("tickets/edit/<int:id>/returnTicket", views.returnTicket, name="returnTicket"),
]
