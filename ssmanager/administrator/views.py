from django.shortcuts import  render, redirect
from administrator.forms import NewUserForm, LoginUserForm, ServiceSecretsForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from api.models import Service


@require_http_methods("GET")
def index(request):
    return render(request=request, template_name="administrator/index.html")

@require_http_methods(["POST","GET"])
def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="administrator/register.html", context={"register_form":form})

@require_http_methods(["POST","GET"])
def login_request(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    form = LoginUserForm()
    return render(request=request, template_name="administrator/login.html", context={"login_form": form})

@login_required
@require_http_methods("GET")
def logout_request(request):
    logout(request)
    return redirect('/login')

@login_required
@require_http_methods(["POST","GET"])
def create_service_request(request):
	if request.method == "POST":
		form = ServiceSecretsForm(request.user, request.POST)
		if form.is_valid():
			service_id = form.save()
			messages.success(request, "Created service with id " + str(service_id))
		else:
			messages.error(request, "Unsuccessful registration. Invalid information.")
	form = ServiceSecretsForm(request.user)
	return render (request=request, template_name="administrator/create_service.html", context={"service_form":form})

@login_required
@require_http_methods("GET")
def list_services_request(request):
	user_id = request.user.id
	services = Service.objects.filter(admin_aid=user_id)
	return render (request=request, template_name="administrator/list_services.html", context={"services":services})
