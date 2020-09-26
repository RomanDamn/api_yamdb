from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class Review(models.Model):
    text = models.TextField(blank=False)
    pub_date = models.DateTimeField("Дата публикации",
                                    auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="posts")
    score = models.IntegerField(validators=[MinValueValidator(1),
                                            MaxValueValidator(10)])


class Comment(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="comments")
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name="comments")
    text = models.TextField()
    pub_date = models.DateTimeField("Дата добавления",
                                    auto_now_add=True,
                                    db_index=True)
