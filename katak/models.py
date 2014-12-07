from django.db import models

class BigramNode(models.Model):
    name = models.CharField(max_length=256)
    count = models.IntegerField(default=0)

class Bigram(models.Model):
    name = models.CharField(max_length=256)
    isBeginning = models.BooleanField(default=False)
    nodes = models.ManyToManyField(BigramNode)

    @classmethod
    def insertToken(cls, word_a, word_b, isBeginning=False):
        if cls.objects.filter(name=word_a).count() == 0:
            aBigram = cls(name=word_a, isBeginning=isBeginning)
            aBigram.save()
        else:
            aBigram = cls.objects.get(name=word_a)

        if aBigram.nodes.filter(name=word_b).count() == 0:
            bigramNode = BigramNode(name=word_b, count=1)
        else:
            bigramNode = aBigram.nodes.get(name=word_b)
            bigramNode.count += 1

        bigramNode.save()
        aBigram.nodes.add(bigramNode)
        aBigram.save()

    @classmethod
    def getNexts(cls, word):
        if cls.objects.filter(name=word).count() == 0:
            raise Exception("Word not in bigram.")

        total = 0
        wordNexts = dict()

        bigram = cls.objects.get(name=word)
        for bigramNode in bigram.nodes.all():
            wordNexts[bigramNode.name] = bigramNode.count
            total += bigramNode.count

        probabilities = []
        for key, value in wordNexts.items():
            probabilities.append((key, float(float(value)/float(total))))

        return probabilities

    @classmethod
    def getRandomBeginning(cls):
        import random

        beginningList = []
        for bigram in cls.objects.all():
            if bigram.isBeginning: beginningList.append(bigram.name)

        return random.choice(beginningList)
