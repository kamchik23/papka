from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.views import LoginView  # Импортируем для кастомного входа
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Tour, Booking, UserProfile
from .forms import BookingForm, ExtendedRegistrationForm, TourForm

# КЛАСС ДЛЯ ВХОДА (чтобы выводилось сообщение "С возвращением")
class MyLoginView(LoginView):
    template_name = 'cafe/client/login.html'
    
    def form_valid(self, form):
        # Это срабатывает при правильном пароле
        messages.success(self.request, f"С возвращением, {self.request.POST.get('username')}!")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Это срабатывает при ошибке
        messages.error(self.request, "Неверное имя пользователя или пароль.")
        return super().form_invalid(form)

def is_manager(user):
    return user.is_authenticated and user.is_staff

def tour_list(request):
    query = request.GET.get('q', '')
    service_type = request.GET.get('service_type')
    category = request.GET.get('category')
    location = request.GET.get('location')
    max_price = request.GET.get('max_price')

    tours = Tour.objects.all()

    if service_type:
        tours = tours.filter(service_type=service_type)
    if query:
        tours = tours.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        tours = tours.filter(category=category)
    if location:
        tours = tours.filter(location=location)
    if max_price and max_price.isdigit():
        tours = tours.filter(price__lte=int(max_price))

    all_locations = Tour.objects.values_list('location', flat=True).distinct().order_by('location')

    context = {
        'tours': tours,
        'current_type': service_type,
        'all_locations': all_locations,
        'selected_location': location,
        'selected_max_price': max_price,
        'query': query,
    }
    
    if request.path == '/':
        return render(request, 'cafe/client/main.html', {'tours': tours[:4]})
    
    return render(request, 'cafe/client/tour_list.html', context)

def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tour = tour
            booking.total_price = tour.price * booking.people_count

            if request.user.is_authenticated:
                booking.user = request.user
            
            booking.save()
            messages.success(request, f'Тур "{tour.title}" успешно забронирован! Ожидаем оплаты.')
            return render(request, 'cafe/client/payment.html', {'booking': booking})
        else:
            messages.error(request, 'Ошибка при заполнении формы.')
    else:
        form = BookingForm(initial={'people_count': 1})
    return render(request, 'cafe/client/tour_detail.html', {'tour': tour, 'form': form})

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'full_name': request.user.username, 'phone': 'Не указан', 'date_of_birth': '2000-01-01'}
    )
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'cafe/client/profile.html', {'profile': profile, 'bookings': bookings})

def register(request):
    if request.method == 'POST':
        form = ExtendedRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}! Ваш аккаунт успешно создан.')
            return redirect('main')
        else:
            messages.error(request, 'Ошибка регистрации. Проверьте введенные данные.')
    else:
        form = ExtendedRegistrationForm()
    return render(request, 'cafe/client/register.html', {'form': form})

@user_passes_test(is_manager)
def manager_dashboard(request):
    tours = Tour.objects.all().order_by('-id')
    bookings = Booking.objects.all().order_by('-created_at')
    
    users = None
    if request.user.is_superuser:
        users = User.objects.all().exclude(id=request.user.id)

    context = {
        'tours': tours,
        'bookings': bookings,
        'users': users,
        'total_tours': tours.count(),
        'total_bookings': bookings.count(),
    }
    return render(request, 'cafe/manager/dashboard.html', context)

@user_passes_test(is_manager)
def tour_create(request):
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Новый тур успешно добавлен!')
            return redirect('manager_dashboard')
    else:
        form = TourForm()
    return render(request, 'cafe/manager/tour_form.html', {'form': form, 'title': 'Создать тур'})

@user_passes_test(is_manager)
def tour_edit(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES, instance=tour)
        if form.is_valid():
            form.save()
            messages.success(request, f'Тур "{tour.title}" обновлен.')
            return redirect('manager_dashboard')
    else:
        form = TourForm(instance=tour)
    return render(request, 'cafe/manager/tour_form.html', {'form': form, 'title': 'Редактировать'})

@user_passes_test(lambda u: u.is_superuser)
def tour_delete(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    title = tour.title
    tour.delete()
    messages.warning(request, f'Тур "{title}" был удален.')
    return redirect('manager_dashboard')

@user_passes_test(lambda u: u.is_superuser)
def make_manager(request, user_id):
    u = get_object_or_404(User, id=user_id)
    u.is_staff = not u.is_staff
    u.save()
    status = "теперь менеджер" if u.is_staff else "больше не менеджер"
    messages.info(request, f'Пользователь {u.username} {status}.')
    return redirect('manager_dashboard')

def game_view(request):
    return render(request, 'cafe/client/game.html')