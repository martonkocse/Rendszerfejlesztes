# Rendszerfejlesztes
BerAuto
## Projekt leírás

A BerAuto egy teljes stackes autókölcsönző rendszer, amely Django REST Framework backendből és React frontendből áll.

A rendszer célja az autóbérlés folyamatának digitalizálása és egyszerű kezelése különböző felhasználói szerepkörök számára.

A projekt támogatja:

- felhasználókezelést
- autók kezelését
- kölcsönzések kezelését
- JWT alapú hitelesítést
- adminisztrációs felületet
- REST API kommunikációt
- Swagger API dokumentációt

---

# Fő funkciók

## Felhasználók

- Regisztráció
- Bejelentkezés
- JWT token kezelés
- Szerepkör alapú jogosultságok

## Autók

- Autók listázása
- Új autó létrehozása
- Autó szerkesztése
- Autó törlése
- Elérhetőség kezelése

## Kölcsönzések

- Új foglalás létrehozása
- Kölcsönzés jóváhagyása
- Kölcsönzés elutasítása
- Autó átadása
- Autó visszavétele

## Admin funkciók

- Django admin felület
- Felhasználók kezelése
- Teljes rendszer hozzáférés

---

# Használt technológiák

## Backend

- Python 3
- Django
- Django REST Framework
- JWT Authentication
- drf-spectacular
- SQLite

## Frontend

- React
- JavaScript
- React Router
- CSS

---

# Projekt struktúra

```text
Rendszerfejlesztes/
│
├── config/                 # Django projekt konfiguráció
├── rental/                 # Fő alkalmazás
│   ├── api/                # REST API végpontok
│   ├── migrations/         # Adatbázis migrációk
│   ├── templates/          # HTML template-ek
│   ├── models.py           # Modellek
│   ├── helpers.py          # Segédfüggvények
│   └── decorators.py       # Dekorátorok
│
├── frontend/               # React frontend
│   ├── src/
│   ├── public/
│   └── package.json
│
├── requirements.txt
├── manage.py
└── db.sqlite3
```

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
# Frontend telepítés és futtatás

## Frontend mappa megnyitása

```bash
cd frontend
```

## Függőségek telepítése

```bash
npm install
```

## Frontend indítása

```bash
npm start
```

## A frontend alapértelmezett címe:

```text
http://localhost:3000
```

# Backend elérések

## A backend szerver alapértelmezett címe:

```text
http://127.0.0.1:8000
```

## Admin felület:

```text
http://127.0.0.1:8000/admin
```

# API dokumentáció

## Swagger UI:

```text
http://localhost:8000/api/docs/
```
## JWT token kérés

```text
http://localhost:8000/api/token/
```
## Regisztráció

```text
http://localhost:8000/api/auth/register/
```
# Admin felhasználó létrehozása

```bash
python manage.py createsuperuser
```
# API végpontok

## Auth

| Metódus | Endpoint | Leírás |
|---|---|---|
| POST | /api/auth/register/ | Regisztráció |
| POST | /api/token/ | JWT token kérés |
| POST | /api/token/refresh/ | Token frissítés |

## Autók

| Metódus | Endpoint | Leírás |
|---|---|---|
| GET | /api/cars/ | Autók listázása |
| POST | /api/cars/ | Új autó létrehozása |
| PUT | /api/cars/{id}/ | Autó módosítása |
| DELETE | /api/cars/{id}/ | Autó törlése |


## Kölcsönzések

| Metódus | Endpoint | Leírás |
|---|---|---|
| GET | /api/rentals/ | Kölcsönzések lekérése |
| POST | /api/rentals/ | Új kölcsönzés |
| POST | /api/rentals/{id}/approve/ | Jóváhagyás |
| POST | /api/rentals/{id}/reject/ | Elutasítás |
| POST | /api/rentals/{id}/handover/ | Átadás |
| POST | /api/rentals/{id}/return_car/ | Visszavétel |


# Jogosultságkezelés

## Customer

- Saját kölcsönzések megtekintése
- Új foglalás létrehozása

## Agent

- Kölcsönzések kezelése
- Jóváhagyás
- Átadás
- Visszavétel

## Admin

- Teljes rendszer hozzáférés
- Autók kezelése
- Felhasználók kezelése


# Adatbázis modellek

## User

Egyedi felhasználói modell szerepkör kezeléssel.

## Szerepkörök

- customer
- agent
- admin

## Car

Autók adatainak tárolása.

## Fő mezők

- márka
- modell
- évjárat
- rendszám
- napi díj
- kilométeróra állás
- elérhetőség

## Rental

Kölcsönzési adatok kezelése.

## Állapotok

- PENDING
- APPROVED
- REJECTED
- HANDED_OVER
- RETURNED


# Tesztelés

## Backend tesztek

```bash
python manage.py test
```

## Frontend tesztek

```bash
npm test
```

# Biztonság

A rendszer az alábbi biztonsági megoldásokat használja:

- JWT autentikáció
- Szerepkör alapú jogosultságkezelés
- Backend oldali validáció
- DRF permission osztályok
- Állapot átmenet ellenőrzés


# Fejlesztési lehetőségek

- PostgreSQL támogatás
- Docker integráció
- CI/CD pipeline
- PDF számlázás
- Email értesítések

- Fizetési rendszer
- Admin dashboard
- Képfeltöltés autókhoz


# BerAuto – Indítás röviden

## Projekt letöltése

```bash
git clone https://github.com/martonkocse/Rendszerfejlesztes.git
cd Rendszerfejlesztes
```

# Backend indítása

## Virtuális környezet létrehozása

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Csomagok telepítése

```bash
pip install -r requirements.txt
```

---

## Adatbázis migráció

```bash
python manage.py migrate
```

---

## Admin létrehozása

```bash
python manage.py createsuperuser
```

---

## Backend indítása

```bash
python manage.py runserver
```

Backend:

```text
http://127.0.0.1:8000
```

Admin:

```text
http://127.0.0.1:8000/admin
```

Swagger:

```text
http://localhost:8000/api/docs/
```

# Frontend indítása

Új terminál:

```bash
cd frontend
npm install
npm start
```

Frontend:

```text
http://localhost:3000
```

# Leállítás

```text
CTRL + C
```

