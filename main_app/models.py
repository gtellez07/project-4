from django.db import models

class Show(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    class Rating(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
    review = models.IntegerField(choices=Rating.choices)

    def __str__(self):
        return self.title,


class Series(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    show_id = models.IntegerField()
    user_id = models.IntegerField()
    favorite = models.BooleanField()
    watched = models.BooleanField()

    class Rating(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
    review = models.IntegerField(choices=Rating.choices)
    series = models.Manager()
    def __str__(self):
        return self.title,


