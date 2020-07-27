from django.db import models


class Manager(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.EmailField(max_length=255)
    first_name = models.TextField(max_length=255)
    last_name = models.TextField(max_length=255)
    address = models.TextField()
    dob = models.DateField()
    company = models.TextField(max_length=100)
    card_id = models.TextField(blank=True)
    stripe_user_id = models.TextField(blank=True)
    card_number = models.TextField(blank=True)
    sub_id = models.TextField(blank=True)
    product_id = models.TextField(blank=True)
    # sub_date = models.TextField(blank=True)


class Subscription(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    subscription_name = models.TextField()
    subscription_id = models.TextField()
    subscription_purchase_on = models.TextField()
    subscription_status = models.TextField()
    subscription_ended_on = models.TextField()
