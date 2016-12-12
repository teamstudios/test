from django.db import models
from django.contrib.auth.models import User

from main.models import BaseModel
from goods.models import Good, AuctionBids
from goods.constants import AUCTION

# Create your models here.


class AuctionCartModel(BaseModel):
    """
    Cart model, to store users/goods in database.
    """
    user = models.ForeignKey(User, related_name='cart_items')
    good = models.ForeignKey(Good, related_name='in_carts')
    ready_for_sale = models.BooleanField(default=True, verbose_name='Ready for sale (auction)')

    def __str__(self):
        return "{}'s cart".format(self.user.username)

    def get_user_bid(self):
        """
        Get user bid price
        :return:
        """
        if self.good.deal == AUCTION:
            bid = AuctionBids.objects.filter(good=self.good, user=self.user).latest('updated')
            return bid.user_price

    class Meta:
        ordering = ('-created',)
        unique_together = (("user", "good"),)
