from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField

# Create your models here.

class Perfume(models.Model):
    # GENDER_CHOICES = [
    #     ('M', 'رجالي'),
    #     ('F', 'حريمي'),
    #     ('U', 'يونيسكس (للجنسين)'),
    # ]

    name_ar = models.CharField(max_length=100, verbose_name="الاسم بالعربية")
    name_en = models.CharField(max_length=100, verbose_name="الاسم بالإنجليزية")
    image = CloudinaryField(verbose_name="صورة العطر")
    is_original = models.BooleanField(default=False, verbose_name="إزازة أوريجينال؟")  # 👈 ضيف السطر ده

    # gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U', verbose_name="النوع")

    def __str__(self):
        return self.name_ar



class PerfumeSize(models.Model):
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE, related_name='sizes')
    size_ml = models.PositiveIntegerField(verbose_name="السعة (مل)")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="السعر")
    is_original = models.BooleanField(default=False, verbose_name="إزازة أوريجينال؟")  # ✅ هنا مكانها الصحيح


    def __str__(self):
        return f"{self.size_ml} مل - {'أوريجينال' if self.is_original else 'عادية'}"
    
    
class CartItem(models.Model):
    perfume_size = models.ForeignKey(PerfumeSize, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    session_key = models.CharField(max_length=100, null=True, blank=True)



    def __str__(self):
        return f"{self.perfume_size.perfume.name_ar} - {self.quantity}×{self.perfume_size.size_ml}مل"
    
    
    
class Booking(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    

    def __str__(self):
        return f"{self.name} - {self.phone}"