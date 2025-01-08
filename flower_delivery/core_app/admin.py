from django.contrib import admin
from core_app.models import User, Product, Order, OrderItem, Review

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'address', 'telegram_id')  # Добавили telegram_id
    search_fields = ('id', 'username', 'email', 'phone', 'telegram_id')  # Добавили telegram_id в поиск
    list_editable = ('telegram_id',)  # Позволяет редактировать telegram_id прямо в списке
    fields = ('username', 'email', 'phone', 'address', 'telegram_id')  # Определяем поля для редактирования



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    search_fields = ( 'id',  'name',)
    list_filter = ('price',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'order_date')
    list_filter = ('status', 'order_date')
    inlines = [OrderItemInline]

    # Разрешение для изменения статуса
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj:  # Если это не новый заказ
            fields = list(fields) + ['status']  # Добавляем статус
        return fields

    # Разрешаем изменение всех заказов
    def has_change_permission(self, request, obj=None):
        if obj is None:
            return super().has_change_permission(request, obj)
        return True  # Разрешаем изменения для всех объектов

    # Разрешаем удаление заказов
    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return super().has_delete_permission(request, obj)
        return True  # Разрешаем удаление





@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'rating')
    list_filter = ('rating',)
    search_fields = ('user__username', 'product__name')





