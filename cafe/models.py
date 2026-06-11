from django.db import models
from django.contrib.auth.models import User

class Tour(models.Model):
    SERVICE_CHOICES = [
        ('stay', 'Проживание'),
        ('tour', 'Экскурсия/Тур'),
    ]

    CATEGORY_CHOICES = [
        # Категории для проживания
        ('hotels', 'Отели'),
        ('apartments', 'Квартиры'),
        ('houses', 'Дома/Коттеджи'),
        # Категории для туров
        ('excursion', 'Экскурсия'),
        ('active', 'Активный отдых'),
        ('multi_day', 'Многодневный тур'),
    ]

    # Основные поля
    title = models.CharField(max_length=200, verbose_name="Название")
    service_type = models.CharField(max_length=10, choices=SERVICE_CHOICES, verbose_name="Тип услуги")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Категория")
    location = models.CharField(max_length=100, verbose_name="Город")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='tours/', null=True, blank=True, verbose_name="Фото")
    
    # Дополнительные поля (которые искал Django)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    start_date = models.DateField(verbose_name="Дата начала", blank=True, null=True)
    end_date = models.DateField(verbose_name="Дата окончания", blank=True, null=True)
    available_slots = models.PositiveIntegerField(default=10, verbose_name="Свободные места")

    def save(self, *args, **kwargs):
        # АВТО-ЛОГИКА: определяем service_type по категории
        stay_categories = ['hotels', 'apartments', 'houses']
        if self.category in stay_categories:
            self.service_type = 'stay'
        else:
            self.service_type = 'tour'
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_category_display()}: {self.title}"

    class Meta:
        verbose_name = "Объект"
        verbose_name_plural = "Объекты (Туры и Жилье)"
        
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    date_of_birth = models.DateField(verbose_name="Дата рождения")

    def __str__(self):
        return self.full_name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачено'),
        ('canceled', 'Отменено'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='my_bookings')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='bookings')
    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    client_phone = models.CharField(max_length=20, verbose_name="Телефон")
    people_count = models.PositiveIntegerField(default=1, verbose_name="Кол-во человек")
    
    # НОВОЕ ПОЛЕ
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    
    # Поле для итоговой цены (со скидкой)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Итоговая цена")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка {self.id} - {self.get_status_display()}"

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Промокод")
    discount = models.PositiveIntegerField(verbose_name="Скидка в %")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return f"{self.code} (-{self.discount}%)"

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"