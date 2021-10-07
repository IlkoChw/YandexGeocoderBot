from django.db import models
from django.utils import timezone


class BotUser(models.Model):
    user_id = models.CharField(max_length=20, unique=True, verbose_name='Telegram ID')

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'

    def __str__(self):
        return self.user_id


class SearchArea(models.Model):
    name = models.CharField(unique=True, max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'Область поиска'
        verbose_name_plural = 'Области поиска'

    def __str__(self):
        return self.name


class SearchResult(models.Model):
    user = models.ForeignKey(
        'BotUser', on_delete=models.CASCADE, related_name='search_result', verbose_name='Пользователь бота')
    request = models.CharField(max_length=200, verbose_name='Запрос')
    result = models.TextField(verbose_name='Результат')
    created = models.DateField(default=timezone.now(), verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Результат поиска'
        verbose_name_plural = 'Результаты поиска'

    def __str__(self):
        return self.request
