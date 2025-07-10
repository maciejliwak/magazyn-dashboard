from django.contrib import admin
from .models import (
    Magazyn, Producent, ModelUrzadzenia, NazwaUrzadzenia,
    Urzadzenie, Czesc, Wypozyczenie, OperacjaLog, PrzesuniecieMagazynowe
)
from .forms import UrzadzenieForm


@admin.register(ModelUrzadzenia)
class ModelUrzadzeniaAdmin(admin.ModelAdmin):
    list_display = ["nazwa", "producent"]
    search_fields = ["nazwa", "producent__nazwa"]
    list_filter = ["producent"]
    ordering = ["nazwa"]


@admin.register(Magazyn)
class MagazynAdmin(admin.ModelAdmin):
    list_display = ["nazwa"]
    search_fields = ["nazwa"]
    ordering = ["nazwa"]


@admin.register(Producent)
class ProducentAdmin(admin.ModelAdmin):
    list_display = ["nazwa"]
    search_fields = ["nazwa"]
    ordering = ["nazwa"]


@admin.register(NazwaUrzadzenia)
class NazwaUrzadzeniaAdmin(admin.ModelAdmin):
    list_display = ["nazwa"]
    search_fields = ["nazwa"]
    ordering = ["nazwa"]


@admin.register(Urzadzenie)
class UrzadzenieAdmin(admin.ModelAdmin):
    form = UrzadzenieForm
    list_display = [
        "nazwa", "numer_seryjny", "model", "producent",
        "magazyn", "na_stale", "klient_nazwa", "numer_zgloszenia"
    ]
    search_fields = [
        "numer_seryjny", "klient_nazwa", "model__nazwa",
        "producent__nazwa", "nazwa__nazwa", "numer_zgloszenia"
    ]
    list_filter = ["magazyn", "producent", "na_stale"]
    ordering = ["-id"]
    readonly_fields = ["na_stale"]  # Pole systemowe — nieedytowalne ręcznie


@admin.register(Czesc)
class CzescAdmin(admin.ModelAdmin):
    list_display = ["nazwa", "numer_seryjny", "producent", "magazyn", "klient_nazwa", "ilosc"]
    search_fields = ["numer_seryjny", "klient_nazwa", "producent", "nazwa__nazwa"]
    list_filter = ["magazyn", "producent"]
    ordering = ["-id"]
    readonly_fields = ["klient_nazwa", "numer_zgloszenia"]


@admin.register(Wypozyczenie)
class WypozyczenieAdmin(admin.ModelAdmin):
    list_display = ["urzadzenie", "klient_nazwa", "numer_zgloszenia", "data_wypozyczenia"]
    search_fields = ["klient_nazwa", "numer_zgloszenia", "urzadzenie__numer_seryjny"]
    list_filter = ["klient_nazwa", "data_wypozyczenia"]
    ordering = ["-data_wypozyczenia"]
    readonly_fields = ["urzadzenie"]


@admin.register(OperacjaLog)
class OperacjaLogAdmin(admin.ModelAdmin):
    list_display = ["typ_operacji", "data_operacji", "uzytkownik"]
    search_fields = ["typ_operacji", "opis", "uzytkownik__username"]
    list_filter = ["typ_operacji", "uzytkownik"]
    ordering = ["-data_operacji"]
    readonly_fields = ["typ_operacji", "opis", "data_operacji", "uzytkownik"]


@admin.register(PrzesuniecieMagazynowe)
class PrzesuniecieAdmin(admin.ModelAdmin):
    list_display = [
        "urzadzenie", "magazyn_zrodlowy", "magazyn_docelowy",
        "data_przesuniecia", "uzytkownik"
    ]
    search_fields = [
        "urzadzenie__numer_seryjny",
        "magazyn_zrodlowy__nazwa",
        "magazyn_docelowy__nazwa"
    ]
    list_filter = ["magazyn_zrodlowy", "magazyn_docelowy", "uzytkownik"]
    ordering = ["-data_przesuniecia"]
    readonly_fields = ["urzadzenie", "magazyn_zrodlowy", "magazyn_docelowy", "data_przesuniecia", "uzytkownik"]
