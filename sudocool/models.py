from django.db import models

class SudocoolBoardManager(models.Manager):
    def create_sudocoolboard(self, sudocoolData):
        sudocoolBoard = self.create(sudocoolData = sudocoolData)
        sudocoolBoard.save()
        return sudocoolBoard


class SudocoolBoard(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    sudocoolData = models.CharField(max_length=161)

    def __unicode__(self):
        return self.sudocoolData

    objects = SudocoolBoardManager()
