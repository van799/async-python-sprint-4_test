from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Urls(models.Model):
    urls = models.CharField(max_length=250)
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'URL'
        verbose_name_plural = 'URLs'

    def __str__(self):
        return self.urls[:15]
