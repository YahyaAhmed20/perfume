class CartItem(models.Model):
    perfume_size = models.ForeignKey(PerfumeSize, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.perfume_size.perfume.name_ar} - {self.quantity}×{self.perfume_size.size_ml}مل"
    
    


    
def create_order(request, perfume_id):
    if request.method == 'POST':
        size_id = request.POST.get('size_id')
        quantity = int(request.POST.get('quantity', 1))
        size = get_object_or_404(PerfumeSize, id=size_id)
        total_price = size.price * quantity

        # حفظ المنتج في السلة
        CartItem.objects.create(
            perfume_size=size,
            quantity=quantity,
            total_price=total_price
        )

        # عرض صفحة نجاح الإضافة
        return render(request, 'home/cart_success.html', {
            'perfume': size.perfume,
            'size': size,
            'quantity': quantity,
            'total_price': total_price
        })
    return redirect('home:home')
  
        




        'OPTIONS': {
    'context_processors': [
        ...
        'home.context_processors.cart_count',
    ],
},



@media (max-width: 576px) {
    .brand-logo {
        height: 180px;
        top: -81%;
        left: 75% !important;
        transform: translate(-35%, -40%);
    }
}