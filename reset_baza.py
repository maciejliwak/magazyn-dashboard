import os
import shutil
import subprocess

APP_NAME = "magazyn_core"
DB_NAME = "db.sqlite3"
MIGRATIONS_DIR = f"{APP_NAME}/migrations"

def czysc_baze():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"✅ Usunięto bazę danych: {DB_NAME}")
    else:
        print(f"⚠️ Baza danych nie istnieje: {DB_NAME}")

    for file in os.listdir(MIGRATIONS_DIR):
        if file.startswith("0") and file.endswith(".py"):
            os.remove(os.path.join(MIGRATIONS_DIR, file))
            print(f"🧹 Usunięto migrację: {file}")
    print("✅ Migracje wyczyszczone.")

    subprocess.call(["python", "manage.py", "makemigrations", APP_NAME])
    subprocess.call(["python", "manage.py", "migrate"])
    print("📦 Nowa migracja i baza gotowa!")

if __name__ == "__main__":
    czysc_baze()
