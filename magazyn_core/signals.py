from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import (
    Urzadzenie, Czesc,
    PrzesuniecieMagazynowe, Wypozyczenie,
    OperacjaLog
)

# 🟢 WYPOŻYCZENIA
@receiver(post_save, sender=Wypozyczenie)
def loguj_wypozyczenie(sender, instance, created, **kwargs):
    if created:
        opis = f"Wypożyczono urządzenie: {instance.urzadzenie} dla klienta {instance.klient_nazwa} (zgłoszenie: {instance.numer_zgloszenia})"
        OperacjaLog.objects.create(
            typ_operacji="WYPOZYCZENIE",
            opis=opis,
            uzytkownik=None
        )

# 🟢 URZĄDZENIA
@receiver(post_save, sender=Urzadzenie)
def loguj_urzadzenie(sender, instance, created, **kwargs):
    typ = "DODANIE" if created else "EDYCJA"
    opis = f"{typ}: Urządzenie {instance.nazwa} ({instance.numer_seryjny}) - magazyn: {instance.magazyn}"
    OperacjaLog.objects.create(
        typ_operacji=typ,
        opis=opis,
        uzytkownik=None
    )

@receiver(post_delete, sender=Urzadzenie)
def loguj_usuniecie_urzadzenia(sender, instance, **kwargs):
    opis = f"USUNIĘCIE: Urządzenie {instance.nazwa} ({instance.numer_seryjny}) - magazyn: {instance.magazyn}"
    OperacjaLog.objects.create(
        typ_operacji="USUNIECIE",
        opis=opis,
        uzytkownik=None
    )

# 🟣 CZĘŚCI
@receiver(post_save, sender=Czesc)
def loguj_czesc(sender, instance, created, **kwargs):
    typ = "DODANIE" if created else "EDYCJA"
    opis = f"{typ}: Część {instance.nazwa} ({instance.ilosc} szt.) - magazyn: {instance.magazyn}"
    OperacjaLog.objects.create(
        typ_operacji=typ,
        opis=opis,
        uzytkownik=None
    )

@receiver(post_delete, sender=Czesc)
def loguj_usuniecie_czesci(sender, instance, **kwargs):
    opis = f"USUNIĘCIE: Część {instance.nazwa} ({instance.ilosc} szt.) - magazyn: {instance.magazyn}"
    OperacjaLog.objects.create(
        typ_operacji="USUNIECIE",
        opis=opis,
        uzytkownik=None
    )

# 🔁 PRZESUNIĘCIA MAGAZYNOWE
@receiver(post_save, sender=PrzesuniecieMagazynowe)
def loguj_przesuniecie(sender, instance, created, **kwargs):
    if created:
        opis = f"PRZESUNIĘCIE: Urządzenie {instance.urzadzenie} z magazynu {instance.magazyn_zrodlowy} do {instance.magazyn_docelowy}"
        OperacjaLog.objects.create(
            typ_operacji="PRZESUNIECIE",
            opis=opis,
            uzytkownik=instance.uzytkownik
        )
