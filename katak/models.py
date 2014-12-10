from django.db import models

class CorpusFile(models.Model):
    """
    Used to save and track the corpus files.

    NOTE: May soon be deprecated in favor of pickled data as well. (Faster.)
    """
    corpusFile = models.FileField(upload_to='corpus/')
    fileName = models.CharField(max_length=256)
    trained = models.BooleanField(default=False)
    owner = models.CharField(max_length=256)