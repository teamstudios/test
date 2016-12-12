from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from main.models import BaseModel
from goods.models import Good

# Create your models here.


class Order(BaseModel):
    """
    Order model
    """
    seller = models.ForeignKey(User, related_name='my_sold_orders')
    buyer = models.ForeignKey(User, related_name='my_bought_orders')
    address = models.CharField(max_length=250, verbose_name=_("Delivery address"))
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return "{}'s order n.{} from {}".format(self.seller.username, self.id, self.buyer.username)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    class Meta:
        ordering =('-created',)


class OrderItem(models.Model):
    """
    Order items (products) model
    """
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(Good, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity