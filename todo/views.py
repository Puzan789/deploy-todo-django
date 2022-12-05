from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .models import task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.


class userlogin(LoginView):
    template_name = "todo/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("index")


class userregistration(FormView):
    template_name = "todo/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = False
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(userregistration, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("index")
        return super(userregistration, self).get(*args, **kwargs)


class Tasklist(LoginRequiredMixin, ListView):
    model = task
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user)
        context["count"] = context["tasks"].filter(complete=False).count()

        search_input = self.request.GET.get("search-area") or ("")
        if search_input:
            context["tasks"] = context["tasks"].filter(
                title__icontains=search_input
            )  # icontains bhaneko sabai search hunxa startswith ends with ni hunxa aaaru
        context["search_input"] = search_input
        return context


class Taskdetail(LoginRequiredMixin, DetailView):
    model = task
    context_object_name = "tasks"
    template_name = "todo/detail.html"


class taskcreate(LoginRequiredMixin, CreateView):
    model = task
    fields = ["title", "description", "complete"]
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(taskcreate, self).form_valid(form)


class taskupdate(LoginRequiredMixin, UpdateView):
    model = task
    fields = ["title", "description", "complete"]
    success_url = reverse_lazy("index")


class taskdelete(LoginRequiredMixin, DeleteView):
    model = task
    context_object_name = "tasks"
    success_url = reverse_lazy("index")
