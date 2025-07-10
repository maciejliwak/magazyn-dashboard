from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



from .views import (
    dashboard,
    eksport_excel,
    eksport_widoku_excel,
    eksport_logi,
    AddUrzadzenieView,
    AddCzescView,
    AddWypozyczenieView,
    ReturnWypozyczenieView,
    PrzesunUrzadzenieView,
    MarkNaStaleView,
    MarkCzescNaStaleView,
    HistoriaUrzadzeniaView,
    EksportHistoriaUrzadzeniaView,
    PrzywrocUrzadzenieView,
    DodajNaStanCzescView,
    custom_logout,
    zmien_haslo_startowe,
    sprawdzenie_hasla,  # ✅ nowy widok kontrolny po logowaniu
)

urlpatterns = [
    path("", dashboard, name="dashboard"),

    path("dodaj-urzadzenie/", AddUrzadzenieView.as_view(), name="add_urzadzenie"),
    path("dodaj-czesc/", AddCzescView.as_view(), name="add_czesc"),

    path("wypozycz/<int:pk>/", AddWypozyczenieView.as_view(), name="wypozycz_urzadzenie"),
    path("zwrot/<int:pk>/", ReturnWypozyczenieView.as_view(), name="zwrot_urzadzenia"),

    path("przesun/<int:pk>/", PrzesunUrzadzenieView.as_view(), name="przesun_urzadzenie"),

    path("na-stale/<int:pk>/", MarkNaStaleView.as_view(), name="oznacz_na_stale"),
    path("czesc-na-stale/<int:pk>/", MarkCzescNaStaleView.as_view(), name="oznacz_czesc_na_stale"),

    path("eksport-magazyn/", eksport_excel, name="eksport_excel"),
    path("eksport-widok/", eksport_widoku_excel, name="eksport_widoku_excel"),
    path("eksport-logi/", eksport_logi, name="eksport_logi"),
    path("urzadzenie/<int:pk>/eksport-historia/", EksportHistoriaUrzadzeniaView.as_view(), name="eksport_historia_urzadzenia"),

    path("urzadzenie/<int:pk>/historia/", HistoriaUrzadzeniaView.as_view(), name="historia_urzadzenia"),
    path("przywroc/<int:pk>/", PrzywrocUrzadzenieView.as_view(), name="przywroc_urzadzenie"),

    path("czesc/<int:pk>/dodaj_na_stan/", DodajNaStanCzescView.as_view(), name="dodaj_na_stan_czesc"),

    path("dodaj-obserwatora", views.rejestruj_obserwatora, name="rejestruj_obserwatora"),

    # Jedno wystąpienie ścieżki do zmiany hasła
    path("zmien-haslo/", zmien_haslo_startowe, name="zmien_haslo_startowe"),

    # Jedno wystąpienie ścieżki do sprawdzenia hasła
    path("sprawdzenie-hasla/", sprawdzenie_hasla, name="sprawdzenie_hasla"),

    # Logowanie i wylogowanie
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", custom_logout, name="logout"),
    
    path('sprawdz-haslo/', sprawdzenie_hasla, name='sprawdzenie_hasla'),
    path('zmien-haslo/', zmien_haslo_startowe, name='zmien_haslo_startowe'),
    path("zmien-haslo/", auth_views.PasswordChangeView.as_view(template_name="zmien_haslo.html", success_url="/"), name="password_change"),
]
