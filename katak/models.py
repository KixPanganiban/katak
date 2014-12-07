from django.db import models

class CorpusFile(models.Model):
    corpusFile = models.FileField(upload_to='corpus/')
    fileName = models.CharField(max_length=256)
    trained = models.BooleanField(default=False)
    owner = models.CharField(max_length=256)