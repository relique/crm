import datetime as dt

from django.db import models
from django.core.urlresolvers import reverse
from apps.accounts.models import User


class Customer(models.Model):
    """Foreign keys: `amounts`."""
    # Basic Info.
    MISTER = 'mr'
    MISSIS = 'mrs'
    MISS = 'ms'
    DOCTOR = 'dr'
    SALUTATION_CHOICES = (
        (MISTER, "Mr."),
        (MISSIS, "Mrs."),
        (MISS, "Ms."),
        (DOCTOR, "Dr."),
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    salutation = models.CharField(
        max_length=50, blank=True, choices=SALUTATION_CHOICES)

    # Work Info.
    position = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    website = models.URLField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    # Social Networks.
    facebook = models.URLField(max_length=255, blank=True)
    googleplus = models.URLField(max_length=255, blank=True)
    twitter = models.URLField(max_length=255, blank=True)
    linkedin = models.URLField(max_length=255, blank=True)

    # Contact Info.
    email = models.EmailField(max_length=255, blank=True)
    skype = models.CharField(max_length=255, blank=True)
    cell_phone = models.CharField(max_length=50, blank=True)
    main_phone = models.CharField(max_length=50, blank=True)

    # Location Info.
    street = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    postcode = models.PositiveIntegerField(blank=True, null=True)

    # Owner (i.e. Sales representative).
    user = models.ForeignKey(User, related_name='customers')

    # Date Records.
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'customer'
        verbose_name_plural = 'customers'

    def __str__(self):
        return "{sal} {first} {last}".format(
            sal=self.salutation, first=self.first_name, last=self.last_name)

    def save(self, *args, **kwargs):
        self.date_modified = dt.datetime.now()
        super(Customer, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('customers:edit', kwargs={'pk': self.pk})


class Amount(models.Model):
    """Amount of money."""
    OPPORTUNITY = 'opportunity'
    WIN = 'win'
    LOST = 'lost'
    STATUS_CHOICES = (
        (OPPORTUNITY, "Opportunity"),
        (WIN, "Closed-Win"),
        (LOST, "Closed-Lost"),
    )

    status = models.CharField(
        max_length=255, default=OPPORTUNITY, choices=STATUS_CHOICES)
    value = models.DecimalField(max_digits=50, decimal_places=2)
    product = models.CharField(max_length=255, blank=True)
    customer = models.ForeignKey(Customer, related_name='amounts')

    # Date Records.
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'amount'
        verbose_name_plural = 'amounts'

    def __str__(self):
        return str(self.value)


class SuggestedCompany(models.Model):
    # Basic Info.
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)

    # Contact Info.
    phone = models.CharField(max_length=50)

    # Location Info.
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'suggested company'
        verbose_name_plural = 'suggested companies'

    def __str__(self):
        return self.name
