from django.contrib import admin
from .models import Tour, Booking, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# 1. Объединяем просмотр Юзера и его Профиля (ФИО, телефон) в одном месте
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Дополнительная информация'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff') 

# Перерегистрируем стандартную модель User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    # Добавляем service_type в список, чтобы сразу видеть ошибки
    list_display = ('title', 'service_type', 'category', 'location', 'price')
    # Фильтр справа поможет быстро найти косячные записи
    list_filter = ('service_type', 'category', 'location')
    search_fields = ('title', 'location')
    
    # Чтобы админ случайно не поменял тип, который ставится автоматом
    readonly_fields = ('service_type',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'tour', 'client_name', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    list_editable = ('status',) # Позволяет менять статус прямо в списке!

# 4. Управление Профилями (если нужно редактировать отдельно от User)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')

# КРАСИВЫЙ БРЕНДИНГ АДМИНКИ
admin.site.site_header = "УПРАВЛЕНИЕ ТУРАГЕНТСТВОМ"
admin.site.site_title = "TravelAgency Admin"
admin.site.index_title = "Панель администратора / Менеджера"