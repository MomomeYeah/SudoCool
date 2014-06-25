from django.db import models
from django.utils import timezone

class SudocoolBoardManager(models.Manager):
    def create_sudocoolboard(self, sudocoolData):
        sudocoolBoard = self.create(created_date = timezone.now(), sudocoolData = sudocoolData)
        sudocoolBoard.save()
        return sudocoolBoard


class SudocoolBoard(models.Model):
    created_date = models.DateTimeField()
    sudocoolData = models.CharField(max_length=161)

    def __unicode__(self):
        return self.sudocoolData

    objects = SudocoolBoardManager()
