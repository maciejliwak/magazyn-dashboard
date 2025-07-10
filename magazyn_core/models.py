from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Magazyn(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Magazyn"
        verbose_name_plural = "Magazyny"
        ordering = ["nazwa"]

    def __str__(self):
        return self.nazwa


class Producent(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Producent"
        verbose_name_plural = "Producenci"
        ordering = ["nazwa"]

    def __str__(self):
        return self.nazwa


class ModelUrzadzenia(models.Model):
    nazwa = models.CharField(max_length=100)
    producent = models.ForeignKey(Producent, on_delete=models.CASCADE, related_name="modele")

    class Meta:
        verbose_name = "Model urządzenia"
        verbose_name_plural = "Modele urządzeń"
        ordering = ["producent__nazwa", "nazwa"]
        unique_together = ("nazwa", "producent")

    def clean(self):
        if ModelUrzadzenia.objects.filter(nazwa=self.nazwa, producent=self.producent).exclude(pk=self.pk).exists():
            raise ValidationError("Taki model już istnieje dla danego producenta.")

    def __str__(self):
        return self.nazwa


class NazwaUrzadzenia(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Nazwa urządzenia"
        verbose_name_plural = "Nazwy urządzeń"
        ordering = ["nazwa"]

    def __str__(self):
        return self.nazwa


class Urzadzenie(models.Model):
    nazwa = models.ForeignKey(NazwaUrzadzenia, on_delete=models.PROTECT, null=True, blank=True)
    producent = models.ForeignKey(Producent, on_delete=models.PROTECT, related_name="urzadzenia")
    model = models.ForeignKey(ModelUrzadzenia, on_delete=models.PROTECT, related_name="urzadzenia")
    numer_seryjny = models.CharField(max_length=100, unique=True)
    indeks_dodatkowy = models.CharField(max_length=100, blank=True, null=True)
    uwagi = models.TextField(blank=True, null=True)
    ilosc = models.PositiveIntegerField(default=1)
    magazyn = models.ForeignKey(Magazyn, on_delete=models.PROTECT, related_name="urzadzenia", blank=True, null=True)
    na_stale = models.BooleanField(default=False)
    klient_nazwa = models.CharField(max_length=100, blank=True, null=True)
    numer_zgloszenia = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Urządzenie"
        verbose_name_plural = "Urządzenia"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.nazwa} ({self.numer_seryjny})"


class Czesc(models.Model):
    nazwa = models.ForeignKey(NazwaUrzadzenia, on_delete=models.PROTECT, null=True, blank=True)
    producent = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    numer_seryjny = models.CharField(max_length=100, blank=True, null=True)
    ilosc = models.PositiveIntegerField(default=1)
    magazyn = models.ForeignKey(Magazyn, on_delete=models.PROTECT, related_name="czesci", blank=True, null=True)
    klient_nazwa = models.CharField(max_length=100, blank=True, null=True)
    numer_zgloszenia = models.CharField(max_length=100, blank=True, null=True)
    uwagi = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Część"
        verbose_name_plural = "Części"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.nazwa} ({self.numer_seryjny})"


class Wypozyczenie(models.Model):
    urzadzenie = models.ForeignKey(Urzadzenie, on_delete=models.CASCADE, related_name="wypozyczenia")
    klient_nazwa = models.CharField(max_length=100)
    numer_zgloszenia = models.CharField(max_length=100)
    data_wypozyczenia = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Wypożyczenie"
        verbose_name_plural = "Wypożyczenia"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.urzadzenie} wypożyczony dla {self.klient_nazwa}"


class OperacjaLog(models.Model):
    typ_operacji = models.CharField(max_length=100)
    opis = models.TextField()
    data_operacji = models.DateTimeField(auto_now_add=True)
    uzytkownik = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Log operacji"
        verbose_name_plural = "Logi operacji"
        ordering = ["-data_operacji"]

    def __str__(self):
        return f"[{self.data_operacji:%Y-%m-%d %H:%M}] {self.typ_operacji}"


class PrzesuniecieMagazynowe(models.Model):
    urzadzenie = models.ForeignKey(Urzadzenie, on_delete=models.CASCADE, related_name="przesuniecia")
    magazyn_zrodlowy = models.ForeignKey(Magazyn, on_delete=models.PROTECT, related_name="przesuniecia_zrodlowe")
    magazyn_docelowy = models.ForeignKey(Magazyn, on_delete=models.PROTECT, related_name="przesuniecia_docelowe")
    data_przesuniecia = models.DateTimeField(auto_now_add=True)
    uzytkownik = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Przesunięcie magazynowe"
        verbose_name_plural = "Przesunięcia magazynowe"
        ordering = ["-data_przesuniecia"]

    def __str__(self):
        return f"{self.urzadzenie} ➝ {self.magazyn_docelowy.nazwa} ({self.data_przesuniecia:%Y-%m-%d %H:%M})"


class ArchiwumUrzadzen(models.Model):
    nazwa = models.ForeignKey(NazwaUrzadzenia, on_delete=models.SET_NULL, null=True)
    producent = models.ForeignKey(Producent, on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey(ModelUrzadzenia, on_delete=models.SET_NULL, null=True)
    numer_seryjny = models.CharField(max_length=100)
    ilosc = models.PositiveIntegerField(default=1)
    magazyn = models.ForeignKey(Magazyn, on_delete=models.SET_NULL, null=True)
    klient_nazwa = models.CharField(max_length=100, blank=True, null=True)
    numer_zgloszenia = models.CharField(max_length=100, blank=True, null=True)
    uwagi = models.TextField(blank=True, null=True)
    data_przekazania = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Przekazane urządzenie (archiwum)"
        verbose_name_plural = "Archiwum urządzeń przekazanych"
        ordering = ["-data_przekazania"]

    def __str__(self):
        return f"{self.nazwa} ({self.numer_seryjny}) przekazany dla {self.klient_nazwa}"
