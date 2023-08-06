from django.db import models
import sys
import os
from yapayzekainterface.yapayzekacore import Yapayzeka
from django.db import models
PATH = ""
sys.path += [os.path.abspath(__file__)]



class Tahmin(models.Model):
    # tahmin = models.ForeignKey(Egitim, on_delete=models.CASCADE
    metin = models.TextField(help_text="Metin giriniz.",blank=True,)
    tahmin = models.TextField(help_text="Algoritmanın tahmin ettiği etiket.",blank=True,)
    beklenen = models.TextField(help_text="Beklenen etiket.",blank=True,)

    def save(self, *args, **kwargs):
        orn = Yapayzeka()
        self.tahmin = list(orn.predict_from_model(self.metin))
        super(Tahmin, self).save(self, *args, **kwargs)

    def deneme(self):
        return tuple((self.metin, self.tahmin))


class Egitim(models.Model):
    etiket = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return self.etiket
