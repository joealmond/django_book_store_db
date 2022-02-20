from tabnanny import verbose
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=80)
    code = models.CharField(max_length=2)

    def __str__(self):
        return self.name

    class Meta:
        # for rename the table on the admin panel:
        verbose_name_plural = "Countries"


class Address(models.Model):
    street = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=5)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.street}, {self.postal_code}, {self.city}"

    class Meta:
        # for rename the table on the admin panel:
        verbose_name_plural = "Address Entries"


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.OneToOneField(
        Address, on_delete=models.CASCADE, null=True)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    # Just a utility for the function belove it
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    # For showing the first and last name insted of the object name:

    def __str__(self):
        return self.full_name()


class Book(models.Model):
    title = models.CharField(max_length=50)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    # author = models.CharField(null=True, max_length=100)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, null=True, related_name="books")
    is_bestselling = models.BooleanField(default=False)
    # convert url "3" to "harry-ptter-1", add db_index for search performace (you may set this it pk also)
    # options blank=True, editable=False,
    slug = models.SlugField(default="", null=False, db_index=True)
    # id = models.AutoField() will be automatically added

    published_countries = models.ManyToManyField(
        Country, null=False, related_name="books")

    # For save a slug based on the title (not needed if you chse pre populated value in admin)
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)

    # For simler url call in template(by Jocc):
    def get_absolute_url(self):
        return reverse("book-detail-string", args=[self.slug])
    # def get_absolute_url(self):
    #     return reverse("book-detail", args=[self.id])

    # For outputing readable queris in the shell(by Jocc):
    def __str__(self):
        return f"{self.title} ({self.rating})"


"""
Circular Relations & Lazy Relations
Sometimes, you might have two models that depend on each other - i.e. you end up with a circular relationship.

Or you have a model that has a relation with itself.

Or you have a model that should have a relation with some built-in model (i.e. built into Django) or a model defined in another application.

Below, you find examples for all three cases that include Django's solution for these kinds of "problems": Lazy relationships. You can also check out the official docs in addition.

1) Two models that have a circular relationship

class Product(models.Model):
  # ... other fields ...
  last_buyer = models.ForeignKey('User')
  
class User(models.Model):
  # ... other fields ...
  created_products = models.ManyToManyField('Product')
In this example, we have multiple relationships between the same two models. Hence we might need to define them in both models. By using the model name as a string instead of a direct reference, Django is able to resolve such dependencies.

2) Relation with the same model

class User(models.Model):
  # ... other fields ...
  friends = models.ManyToManyField('self') 
The special self keyword (used as a string value) tells Django that it should form a relationship with (other) instances of the same model.

3) Relationships with other apps and their models (built-in or custom apps)

class Review(models.Model):
  # ... other fields ...
  product = models.ForeignKey('store.Product') # '<appname>.<modelname>'
You can reference models defined in other Django apps (no matter if created by you, via python manage.py startapp <appname> or if it's a built-in or third-party app) by using the app name and then the name of the model inside the app.
"""
