from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=50)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    author = models.CharField(null=True, max_length=100)
    is_bestselling = models.BooleanField(default=False)
    # convert url "3" to "harry-ptter-1", add db_index for search performace (you may set this it pk also)
    # options blank=True, editable=False,
    slug = models.SlugField(default="", null=False, db_index=True)
    # id = models.AutoField() will be automatically added

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
