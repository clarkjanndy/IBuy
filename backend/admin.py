from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from . models import (
    User, 
    FAQ, 
    SystemInformation, 
    Category, 
    Uniform, 
    UniformImage, 
    Inventory,
    Cart,
    PaymentOption,
    Order,
    OrderItem,
    OrderHistory
)

# Register your admin manager here
class UserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'last_login', 'is_superuser', 'date_joined')

    fieldsets = (
        (_("Credentials"), {"fields": ("username", "password")}),
        (_("Information"), {"fields": ("student_id", "email", "first_name", 
                                       "middle_name", "last_name", "suffix", "birthday",
                                       "mobile_number", "address", "bio", "photo")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer',)
    search_fields = ('question', 'answer',)

class SystemInformationAdmin(admin.ModelAdmin):
    list_display = ('title', 'content',)
    search_fields = ('title', 'content',)
    
class PaymentOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at', 'modified_at',)
    search_fields = ('name', 'code')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'modified_at',)
    search_fields = ('name',)

class UniformAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at', 'modified_at',)
    search_fields = ('name', 'category__name')

    def category(self, object):
        return object.category.name
    
class UniformImageAdmin(admin.ModelAdmin):
    list_display = ('uniform', 'image', 'created_at', 'modified_at',)
    search_fields = ('uniform__name', )

    def uniform(self, object):
        return object.uniform.name

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('uniform', 'price', 'quantity', 'created_at', 'modified_at',)
    search_fields = ('uniform__name', )

    def uniform(self, object):
        return object.uniform.name
    
    def price(self, object):
        return object.uniform.price

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('uniform', 'price', 'quantity', 'created_at', 'modified_at',)
    search_fields = ('uniform__name', )

    def uniform(self, object):
        return object.uniform.name
    
    def price(self, object):
        return object.uniform.price
    
class CartAdmin(admin.ModelAdmin):
    list_display = ('uniform', 'user', 'quantity', 'created_at', 'modified_at',)
    search_fields = ('uniform__name', '')
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ('ref_no', 'user', 'payment_option', 'total', 'status', 'created_at',)
    search_fields = ('ref_no', '')
    
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order_ref_no', 'uniform', 'variant', 'unit_price', 'quantity', 'subtotal', 'created_at',)
    search_fields = ('order__ref_no', '')
    
    def order_ref_no(self, object):
        return object.order.ref_no

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(SystemInformation, SystemInformationAdmin)
admin.site.register(PaymentOption, PaymentOptionAdmin)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Uniform, UniformAdmin)
admin.site.register(UniformImage, UniformImageAdmin)
admin.site.register(Inventory, InventoryAdmin)

admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)






