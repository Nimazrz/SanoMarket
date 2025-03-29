from market.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        product_price = product.offer_price if product.offer_price else product.price

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'price': product_price}
        else:
            if self.cart[product_id]['quantity'] < product.inventory:
                self.cart[product_id]['quantity'] += 1

        self.cart[product_id]['price'] = product_price  # Always update price
        self.save()

    def decrease(self, product):
        product_id = str(product.id)
        if self.cart[product_id]['quantity'] > 1:
            self.cart[product_id]['quantity'] -= 1
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def clear(self):
        del self.session['cart']
        self.save()

    def get_total_price(self):
        price = sum(item['price'] * item['quantity'] for item in self.cart.values())
        return price

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_dict = self.cart.copy()

        for product in products:
            cart_dict[str(product.id)]['product'] = {
                "id": product.id,
                "name": product.name,
                "price": product.offer_price if product.offer_price else product.price,
                "image_url": product.image.url if product.images.all() else None
            }  # ✅ Convert product to a dictionary

        for item in cart_dict.values():
            item['total'] = (item['price'] or 0) * item['quantity']
            yield item

    def save(self):
        self.session.modified = True