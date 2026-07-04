from django.urls import reverse
from django.db import models
from django.utils import timezone
from django_currentuser.db.models import CurrentUserField
from django_extensions.db import fields as extension_fields


class Product(models.Model):

    # Basic Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    # Product Details
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)

    # Nutrition Information
    calories = models.IntegerField(default=0)
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fat = models.FloatField(default=0)

    # Health Recommendation Category
    food_type = models.CharField(
        max_length=20,
        choices=[
            ('Weight Loss', 'Weight Loss'),
            ('Weight Gain', 'Weight Gain'),
            ('Maintain', 'Maintain')
        ],
        default='Maintain'
    )

    image = models.ImageField(
        upload_to="media/Product-images/",
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('category', '-created',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Product_product_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('Product_product_update', args=(self.slug,))


class Order(models.Model):

    # ==========================
    # Order Status Choices
    # ==========================
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Out For Delivery', 'Out For Delivery'),
        ('Delivered', 'Delivered'),
    ]

    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=10, null=True, blank=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    address = models.TextField(blank=True, null=True)
    count = models.IntegerField(default=1)
    cost = models.IntegerField(default=0)

    # NEW FIELD
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    delivered = models.BooleanField(default=False)
    delivered_on = models.DateTimeField(blank=True, null=True)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True
    )

    order_by = CurrentUserField(
        blank=True,
        null=True,
        related_name="orders_user",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('delivered', '-created',)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('Product_order_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('Product_order_update', args=(self.slug,))

    def save(self, *args, **kwargs):

        if self.status == "Delivered":
            self.delivered = True

            if not self.delivered_on:
                self.delivered_on = timezone.now()

        else:
            self.delivered = False
            self.delivered_on = None

        super(Order, self).save(*args, **kwargs)