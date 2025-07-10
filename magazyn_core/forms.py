from django import forms
from .models import (
    Urzadzenie,
    Czesc,
    Wypozyczenie,
    Magazyn,
    Producent,
    ModelUrzadzenia,
    NazwaUrzadzenia
)

class UrzadzenieForm(forms.ModelForm):
    class Meta:
        model = Urzadzenie
        fields = [
            "nazwa", "producent", "model", "numer_seryjny",
            "indeks_dodatkowy", "uwagi", "ilosc", "magazyn",
            "na_stale", "klient_nazwa", "numer_zgloszenia"
        ]
        widgets = {
            "nazwa": forms.Select(attrs={"class": "form-select"}),
            "producent": forms.Select(attrs={"class": "form-select"}),
            "model": forms.Select(attrs={"class": "form-select"}),
            "numer_seryjny": forms.TextInput(attrs={"class": "form-control"}),
            "indeks_dodatkowy": forms.TextInput(attrs={"class": "form-control"}),
            "uwagi": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "ilosc": forms.NumberInput(attrs={"class": "form-control"}),
            "magazyn": forms.Select(attrs={"class": "form-select"}),
            "na_stale": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "klient_nazwa": forms.TextInput(attrs={"class": "form-control"}),
            "numer_zgloszenia": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrowanie modeli zależnie od producenta
        if "producent" in self.data:
            try:
                producent_id = int(self.data.get("producent"))
                self.fields["model"].queryset = ModelUrzadzenia.objects.filter(producent_id=producent_id)
            except (ValueError, TypeError):
                self.fields["model"].queryset = ModelUrzadzenia.objects.none()
        elif self.instance.pk and self.instance.producent:
            self.fields["model"].queryset = ModelUrzadzenia.objects.filter(producent=self.instance.producent)
        else:
            self.fields["model"].queryset = ModelUrzadzenia.objects.all()


class CzescForm(forms.ModelForm):
    numer_seryjny = forms.CharField(required=False)
    magazyn = forms.ModelChoiceField(
        queryset=Magazyn.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = Czesc
        fields = [
            "nazwa", "producent", "model", "numer_seryjny",
            "ilosc", "magazyn", "klient_nazwa", "numer_zgloszenia", "uwagi"
        ]
        widgets = {
            "nazwa": forms.Select(attrs={"class": "form-select"}),
            "producent": forms.TextInput(attrs={"class": "form-control"}),
            "model": forms.TextInput(attrs={"class": "form-control"}),
            "numer_seryjny": forms.TextInput(attrs={"class": "form-control"}),
            "ilosc": forms.NumberInput(attrs={"class": "form-control"}),
            "klient_nazwa": forms.TextInput(attrs={"class": "form-control"}),
            "numer_zgloszenia": forms.TextInput(attrs={"class": "form-control"}),
            "uwagi": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


class WypozyczenieForm(forms.ModelForm):
    class Meta:
        model = Wypozyczenie
        fields = ["klient_nazwa", "numer_zgloszenia"]
        widgets = {
            "klient_nazwa": forms.TextInput(attrs={"class": "form-control"}),
            "numer_zgloszenia": forms.TextInput(attrs={"class": "form-control"}),
        }


class PrzesuniecieForm(forms.Form):
    nowy_magazyn = forms.ModelChoiceField(
        queryset=Magazyn.objects.all(),
        label="Magazyn docelowy",
        widget=forms.Select(attrs={"class": "form-select"})
    )


class PrzekazanieForm(forms.Form):
    klient_nazwa = forms.CharField(label="Nazwa klienta", max_length=100, required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}))
    numer_zgloszenia = forms.CharField(label="Numer zgłoszenia", max_length=100, required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}))
    ilosc_do_przekazania = forms.IntegerField(label="Ilość do przekazania", min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control"}))
    uwagi = forms.CharField(label="Uwagi", required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}))
    
class UzupełnienieForm(forms.Form):
    ilosc_do_dodania = forms.IntegerField(min_value=1, label="Ilość do dodania")
    uwagi = forms.CharField(required=False, widget=forms.Textarea, label="Uwagi (opcjonalnie)")

