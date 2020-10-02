from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser):
    ROLES = [
        ("user", "user"),
        ("moderator", "moderator"),
        ("admin", "admin"),
    ]

    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=50, unique=True)
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLES, default="user")
    confirmation_code = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.username


class Categories(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


def current_year():
    return datetime.now().strftime("%Y")


def max_value_current_year(value):
    if value > 2100:
        raise ValidationError(
            _("%(value)s is not a correct year!"),
            params={"value": value},
        )


class Titles(models.Model):
    name = models.CharField(max_length=300)
    year = models.PositiveIntegerField(
        default=current_year(),
        validators=[MinValueValidator(1450), max_value_current_year],
    )
    rating = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name="categories",
        blank=True,
        null=True,
    )
    description = models.TextField(null=True, blank=True)
    genre = models.ManyToManyField(
        Genres,
        related_name="genres",
    )

    def __str__(self):
        return f"{self.name} ({self.year}г.)"


class Review(models.Model):
    text = models.TextField(blank=False)
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    title = models.ForeignKey(Titles, on_delete=models.CASCADE, related_name="title")

    class Meta:
        unique_together = ["author", "title"]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True, db_index=True)
