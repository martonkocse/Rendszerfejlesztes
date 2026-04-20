# Rendszerfejlesztes
BerAuto

## Telepítés és futtatás

### Linux 

```bash
git clone https://github.com/martonkocse/Rendszerfejlesztes.git
cd Rendszerfejlesztes

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Windows (PowerShell)

```powershell
git clone https://github.com/martonkocse/Rendszerfejlesztes.git
cd Rendszerfejlesztes

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

A szerver ezután itt érhető el:

http://127.0.0.1:8000

http://127.0.0.1:8000/admin

API dokumentáció:
Swagger ui felület elérhető innen:
http://localhost:8000/api/docs/

token kérés:
http://localhost:8000/api/token/

regisztráció:
http://localhost:8000/api/auth/register/

Admin user létrehozása

```md
## Admin létrehozása

```bash
python manage.py createsuperuser


Projekt struktúra

```md
## Struktúra

config/ - Django projekt konfiguráció  
rental/ - Bérlési logika és modellek  

teszt

