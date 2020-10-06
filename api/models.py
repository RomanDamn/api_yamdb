from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.utils import current_year, max_value_current_year


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES_CHOICES = [
        (USER, "user"),
        (MODERATOR, "moderator"),
        (ADMIN, "admin"),
    ]

    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30,
                            choices=ROLES_CHOICES,
                            default=USER)
    confirmation_code = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=300,
                            verbose_name='Название')
    year = models.PositiveIntegerField(default=current_year(),
                                       verbose_name='Год',
                                       validators=[MinValueValidator(1700),
                                                   max_value_current_year],
                                       db_index=True)
    category = models.ForeignKey(Category,
                                 verbose_name='Категории',
                                 on_delete=models.SET_NULL,
                                 related_name="titles",
                                 blank=True,
                                 null=True,
                                 )
    description = models.TextField(null=True,
                                   blank=True
                                   )
    genre = models.ManyToManyField(Genre,
                                   verbose_name='Жанры',
                                   related_name="titles",
                                   )

    def __str__(self):
        return f"{self.name} ({self.year}г.)"


class Review(models.Model):
    text = models.TextField(blank=False)
    pub_date = models.DateTimeField("Дата публикации",
                                    auto_now_add=True)
    author = models.ForeignKey(User,
                               blank=True,
                               on_delete=models.CASCADE,
                               related_name="reviews")
    score = models.IntegerField(validators=[MinValueValidator(1),
                                            MaxValueValidator(10)])
    title = models.ForeignKey(Title,
                              blank=True,
                              on_delete=models.CASCADE,
                              related_name="reviews")

    class Meta:
        ordering = ["pub_date"]
        unique_together = ['author', 'title']

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="comments")
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name="comments")
    text = models.TextField()
    pub_date = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True,
        db_index=True
    )
