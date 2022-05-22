from django.conf import settings

# Import order item model 

class OrderItem():
    pass

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
 

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart
    
    def __setitem__(self,product,data):
        self.cart[product] = data
    
    def __getitem__(self,product):
        return self.cart[product]

    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = OrderItem.objects.get(pk=p)
        
        for item in self.cart.values():
            item['total_price'] = item['product'].price * item['quantity']

            yield item
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def add(self, product_id,data, update_quantity=False):
        product_id = str(product_id) 
        self.cart[product_id] = data                        
        self.save()
    
    def update(self,product_id,new_data):
        product_id = str(product_id) 
        if product_id in self.cart.keys():
            self.cart[product_id] = new_data 
            self.save()

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
    
    def get_total_cost(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = OrderItem.objects.get(pk=p)

        return sum(item['quantity'] * item['product'].price for item in self.cart.values())