from django.db import models

# Create your models here.

class Stock(models.Model):  #to store which stock a user has
    user_name = models.TextField()
    stock_name = models.TextField()
    buy_price = models.FloatField()
    share_quantity = models.IntegerField()

class Link(models.Model):
    user_name = models.TextField()
    link = models.TextField()

class Stock_Data(models.Model):  #to store stock info from nse
    symbol = models.TextField()
    date = models.TextField()
    open_price = models.FloatField()
    close_price = models.FloatField()
    avg_price = models.FloatField()
    turn_over_in_cr = models.FloatField()
    delivery_percentage = models.FloatField()
    delivery_in_cr = models.FloatField()
    buy_price = models.FloatField()
    percentage_difference = models.FloatField()
    username = models.TextField()
