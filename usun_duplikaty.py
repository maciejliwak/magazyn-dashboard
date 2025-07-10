from magazyn_core.models import Czesc
from django.db.models import Count

duplikaty = Czesc.objects.values("numer_seryjny").annotate(ile=Count("id")).filter(ile__gt=1)
for dup in duplikaty:
    parts = Czesc.objects.filter(numer_seryjny=dup["numer_seryjny"]).order_by("id")
    pozostawiony = parts.first()
    duplikaty_do_usuniecia = parts.exclude(id=pozostawiony.id)
    duplikaty_do_usuniecia.delete()

# ← teraz naciśnij ENTER, aby zamknąć pętlę, dopiero potem:
print("✅ Duplikaty usunięte.")
