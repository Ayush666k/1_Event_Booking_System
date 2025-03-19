from django.contrib.auth.hashers import check_password
from django.shortcuts import render,get_object_or_404, redirect
from .models import Event, User
from django.contrib import messages
from .forms import BookingForm
from django.http import HttpResponse

# Create your views here.

def home(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        return render(request, 'home.html', {'user': user})
    else:
        return render(request, 'home.html')


def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})

def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    bookings = event.booking_set.all()
    form = BookingForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            booking = form.save(commit=False)
            booking.event = event
            booking.save()
            messages.success(request, 'Your booking was successful!')
            return redirect('event_detail', id=id)

    return render(request, 'event_detail.html', {'event': event, 'form': form, 'bookings': bookings})


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        user = User(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')

    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse("User does not exist!")

        if check_password(password, user.password):
            request.session['user_id'] = user.id
            return redirect('home')
        else:
            return HttpResponse("Invalid password!")

    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    messages.success(request, "logged out successfully")
    return redirect('home')



def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        message.success(request, f"Thank you {name}, your message has been sent")

    return render(request, 'contact.html')
