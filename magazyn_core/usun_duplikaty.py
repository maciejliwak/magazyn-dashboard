from magazyn_core.models import Czesc, NazwaUrzadzenia

for cz in Czesc.objects.all():
    if isinstance(cz.nazwa, str) and cz.nazwa.strip():
        nazwa_tekstowa = cz.nazwa.strip()
        nazwa_obj, _ = NazwaUrzadzenia.objects.get_or_create(nazwa=nazwa_tekstowa)
        cz.nazwa = nazwa_obj
        cz.save(update_fields=["nazwa"])

print("✅ Wszystkie tekstowe nazwy zostały zamienione na relacje ForeignKey.")


