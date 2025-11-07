from django.contrib import admin
from .models import Perfume, PerfumeSize,Booking


class PerfumeSizeInline(admin.TabularInline):
    model = PerfumeSize
    extra = 1  # عدد الصفوف الفارغة الجاهزة للإضافة
    fields = ('size_ml', 'price')

@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = ('name_ar', 'name_en')
    inlines = [PerfumeSizeInline]  # ربط العطر بالأحجام من نفس الصفحة
    search_fields = ('name_ar', 'name_en')  # شريط البحث في لوحة الإدارة

# Inline model علشان تضيف الأحجام مباشرة من صفحة العطر
# class PerfumeSizeInline(admin.TabularInline):
#     model = PerfumeSize
#     extra = 1  # عدد الصفوف الفارغة الجاهزة للإضافة
#     fields = ('size_ml', 'price')

# @admin.register(Perfume)
# class PerfumeAdmin(admin.ModelAdmin):
#     list_display = ('name_ar', 'name_en')
#     inlines = [PerfumeSizeInline]  # ربط العطر بالأحجام من نفس الصفحة

@admin.register(PerfumeSize)
class PerfumeSizeAdmin(admin.ModelAdmin):
    list_display = ('perfume', 'size_ml', 'price')
    list_filter = ('perfume',)
    search_fields = ('perfume__name_ar', 'perfume__name_en')




@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address', 'total_price', 'date')
    search_fields = ('name', 'phone', 'address')
    list_filter = ('date',)
    readonly_fields = ('date', 'total_price')

    fieldsets = (
        ('بيانات العميل', {
            'fields': ('name', 'phone', 'address')
        }),
        ('تفاصيل الطلب', {
            'fields': ('total_price', 'date')
        }),
    )

    ordering = ('-date',)
