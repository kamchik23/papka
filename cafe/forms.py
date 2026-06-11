from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Booking, UserProfile, Tour

# 1. Форма для создания и редактирования тура (для Менеджера)
class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        # Добавляем новые поля: service_type, category, location
        fields = [
            'service_type', 
            'category', 
            'title', 
            'location', 
            'description', 
            'price', 
            'image', 
            'available_slots', 
            'start_date', 
            'end_date'
        ]
        # Можно добавить виджеты для красоты, например для даты:
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class BookingForm(forms.ModelForm):
    # Общие стили для всех инпутов
    input_style = 'w-full p-4 rounded-2xl bg-slate-50 dark:bg-white/5 outline-none border-2 border-transparent focus:border-blue-600 dark:text-white font-bold text-sm transition-all'

    client_name = forms.CharField(
        label="Ваше имя",
        widget=forms.TextInput(attrs={'placeholder': 'Иван Иванов', 'class': input_style})
    )
    client_phone = forms.CharField(
        label="Телефон",
        widget=forms.TextInput(attrs={'placeholder': '+7 (999) 000-00-00', 'class': input_style})
    )
    people_count = forms.IntegerField(
        label="Количество человек",
        widget=forms.NumberInput(attrs={'min': 1, 'class': input_style})
    )
    promo_code = forms.CharField(
        label="Промокод",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Если есть код на скидку', 'class': input_style})
    )

    class Meta:
        model = Booking
        fields = ['client_name', 'client_phone', 'people_count', 'promo_code']

# 3. Расширенная форма регистрации (ФИО, Телефон, Дата рождения)
class ExtendedRegistrationForm(UserCreationForm):
    full_name = forms.CharField(label="ФИО", required=True)
    phone = forms.CharField(label="Телефон", required=True)
    date_of_birth = forms.DateField(label="Дата рождения", widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    email = forms.EmailField(label="Email", required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Автоматически создаем профиль при регистрации
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'full_name': self.cleaned_data['full_name'],
                    'phone': self.cleaned_data['phone'],
                    'date_of_birth': self.cleaned_data['date_of_birth']
                }
            )
        return user