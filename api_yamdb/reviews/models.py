from django.db import models


class Title(models.Model):
    pass


class Review(models.Model):
    text = models.TextField('Текст')
    author = models.IntegerField('Автор')  # models.ForeignKey()
    score = models.PositiveSmallIntegerField('Оценка')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        ordering = ('pub_date',)


class Comment(models.Model):
    text = models.TextField('Текст')
    author = models.IntegerField('Автор')  # models.ForeignKey()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
