from django.shortcuts import render,redirect, get_object_or_404
from .models import Perfume, PerfumeSize,CartItem,Booking
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string


def home(request):
    perfumes = Perfume.objects.all()
    cart_count = CartItem.objects.count()

    return render(request, 'home/home.html', {'perfumes': perfumes})


def search_perfumes(request):
    q = request.GET.get('q', '').strip()
    perfumes = Perfume.objects.filter(name_ar__icontains=q) | Perfume.objects.filter(name_en__icontains=q)
    html = render_to_string('home/perfume_cards.html', {'perfumes': perfumes})
    return JsonResponse({'html': html}, safe=False)



    
def create_order(request, perfume_id):
    if request.method == 'POST':
        size_id = request.POST.get('size_id')
        quantity = int(request.POST.get('quantity', 1))
        size = get_object_or_404(PerfumeSize, id=size_id)
        total_price = size.price * quantity

        # إنشاء session للمستخدم لو مش موجودة
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        # تحقق لو المنتج ده موجود بالفعل في نفس الـ session
        existing_item = CartItem.objects.filter(perfume_size=size, session_key=session_key).first()
        if existing_item:
            existing_item.quantity += quantity
            existing_item.total_price = existing_item.perfume_size.price * existing_item.quantity
            existing_item.save()
        else:
            CartItem.objects.create(
                perfume_size=size,
                quantity=quantity,
                total_price=total_price,
                session_key=session_key
            )

        # عرض صفحة نجاح الإضافة
        return render(request, 'home/cart_success.html', {
            'perfume': size.perfume,
            'size': size,
            'quantity': quantity,
            'total_price': total_price
        })
    return redirect('home:home')


def cart_view(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_items = CartItem.objects.filter(session_key=session_key)
    total_price = sum(item.total_price for item in cart_items)
    cart_count = cart_items.count()

    return render(request, 'home/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': cart_count
    })

    
    
@csrf_exempt
def update_cart_quantity(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')

        item = CartItem.objects.get(id=item_id)
        if action == "increase":
            item.quantity += 1
        elif action == "decrease" and item.quantity > 0:
            item.quantity -= 1
        item.save()

        # احسب السعر الإجمالي لكل منتج
        item_total = item.quantity * item.perfume_size.price

        # اجمالي السلة
        total_price = sum(i.quantity * i.perfume_size.price for i in CartItem.objects.all())

        return JsonResponse({
            'new_quantity': item.quantity,
            'item_total': item_total,
            'total_price': total_price,
        })




@csrf_exempt
def remove_cart_item(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        item = CartItem.objects.get(id=item_id)
        item.delete()

        total_price = sum(i.quantity * i.perfume_size.price for i in CartItem.objects.all())

        return JsonResponse({'total_price': total_price})





import requests
# بيانات التليجرام
TELEGRAM_TOKEN = "8567567969:AAHjkMD9KvelDSp4DJdk4KquX5pvDjHO9F4"
TELEGRAM_CHAT_ID = "8062956270"

def send_telegram_message(message):
    """إرسال رسالة إلى بوت التليجرام"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print("⚠️ Telegram error:", response.text)


def booking(request):
    """صفحة تأكيد الطلب وإرساله لتليجرام"""
    cart_items = CartItem.objects.all()
    total_price = sum(i.quantity * i.perfume_size.price for i in cart_items)

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        booking = Booking.objects.create(
            name=name,
            phone=phone,
            address=address,
            total_price=total_price
        )

        # تحضير رسالة الطلب
        message = (
            "📦 <b>طلب جديد من الموقع 🕌</b>\n\n"
            f"👤 <b>الاسم:</b> {name}\n"
            f"📞 <b>الهاتف:</b> {phone}\n"
            f"🏠 <b>العنوان:</b> {address}\n\n"
            "🧴 <b>الطلبات:</b>\n"
        )

        for item in cart_items:
            message += (
                f"- {item.perfume_size.perfume.name_ar} "
                f"({item.perfume_size.size_ml} مل) × {item.quantity} "
                f"= {item.total_price} جنيه\n"
            )

        message += f"\n💰 <b>الإجمالي:</b> {total_price} جنيه"

        # إرسال الطلب إلى تليجرام
        send_telegram_message(message)

        # تفريغ السلة بعد الإرسال
        CartItem.objects.all().delete()

        return render(request, "home/booking_success.html", {"booking": booking})

    return render(request, "home/booking.html", {
        "cart_items": cart_items,
        "total_price": total_price
    })
