import simplejson
from decimal import Decimal
from django.conf import settings

from common.functions import convert_str_to_int
from goods.constants import SALE, BUY_SELL, AUCTION
from goods.models import Good

from .models import AuctionCartModel


class Cart:
    def __init__(self, request):
        """
        Initialize the cart
        :param request: HttpRequest
        """
        self.session = request.session
        self.user = request.user
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
            if request.user.is_authenticated():
                saved_auct_objects = AuctionCartModel.objects.filter(user=request.user)
                if saved_auct_objects.exists():
                    # If have saved objects in database add it to cart
                    for obj in saved_auct_objects:
                        good_id = str(obj.good.id)
                        price = obj.good.max_price
                        cart[good_id] = {'quantity': 0, 'price': simplejson.dumps(price)}
        self.cart = cart

    def add(self, good, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity
        :param good: Good objects
        :param quantity: int
        :param update_quantity: Bool
        :return: None
        """
        good_id = str(good.id)
        if good_id not in self.cart:
            if good.deal == SALE:
                price = good.new_price
            elif good.deal == BUY_SELL:
                price = good.price
            else:
                price = good.max_price
                if self.user.is_authenticated():
                    model = AuctionCartModel()
                    model.user = self.user
                    model.good = good
                    model.ready_for_sale = False
                    model.save()
            self.cart[good_id] = {'quantity': 0, 'price': simplejson.dumps(price)}
        if update_quantity:
            self.cart[good_id]['quantity'] = quantity
        else:
            self.cart[good_id]['quantity'] += quantity
        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, good):
        """
        Remove a product from the cart
        :param good: Good object
        :return:
        """
        good_id = str(good.id)
        if good.deal == AUCTION and self.user.is_authenticated():
            model = AuctionCartModel.objects.filter(user=self.user, good=good)
            model.delete()
        if good_id in self.cart:
            del self.cart[good_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        :return: Iter objects
        """
        good_ids = self.cart.keys()
        # get the product objects and add them to the cart
        goods = Good.objects.filter(id__in=good_ids)
        for good in goods:
            self.cart[str(good.id)]['good'] = good
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart
        :return:
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        remove cart from session
        :return:
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_price_after_discount(self):
        # return self.get_total_price() - self.get_discount()
        pass

    def get_list_items(self):
        """
        get self.cart keys and convert it to int. Used as method in templates
        :return: list of id's
        """
        return [convert_str_to_int(item_id) for item_id in self.cart.keys()]
