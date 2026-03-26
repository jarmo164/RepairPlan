# RepairPlan

RepairPlan on veebipõhine parandustööde haldamise süsteem, mille eesmärk on asendada Exceli-põhine töövoog struktureeritud, rollipõhise lahendusega.

## Repo eesmärk

See repo sisaldab töötavat Django rakenduse vundamenti koos P0 + P1 ja osaliselt lõpetatud P2 teostusega.

## Dokumendid

- `PROMPT.md` — algne lähteülesanne
- `ARCHITECTURE.md` — arhitektuuri ülevaade ja tehnilised otsused
- `IMPLEMENTATION_PLAN.md` — detailsem teostusplaan
- `BACKLOG.md` — prioriseeritud tööde nimekiri
- `docs/DEPLOYMENT.md` — keskkonna- ja deploy märkmed
- `docs/INTEGRATIONS.md` — laienduste ja integratsioonide otsustusreeglid

## Stack

- **Backend:** Django
- **Data/API layer:** Django REST Framework + sihitud JSON endpointid
- **Frontend:** Django Templates + Bootstrap + vanilla JavaScript
- **Database:** SQLite arenduses, PostgreSQL tootmises
- **Auth:** Django authentication
- **Permissions:** Django Groups + backend permission layer

## Peamised olemasolevad võimed

- sisselogimine / väljalogimine
- rollide seemne loomine (`seed_roles`)
- paranduste nimekiri filtrite, otsingu ja paginationiga
- paranduse loomine
- paranduse detailvaade
- paranduse muutmine
- "Minu tööd" vaade
- dashboard summary
- kommentaaride ja ajaloo endpointid
- CSV eksport

## Kohalik käivitamine

### 1. Loo virtuaalkeskkond
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Paigalda sõltuvused
```bash
pip install -r requirements.txt
```

### 3. Rakenda migratsioonid
```bash
python manage.py migrate
```

### 4. Loo rolligrupid
```bash
python manage.py seed_roles
```

### 5. Loo administraator
```bash
python manage.py createsuperuser
```

### 6. Käivita arendusserver
```bash
python manage.py runserver
```

Ava brauseris:
- rakendus: <http://127.0.0.1:8000/>
- admin: <http://127.0.0.1:8000/admin/>

## Rollid

Vaikimisi kasutatakse järgmisi gruppe:
- `department_manager`
- `repair_master`
- `repairer`
- `administrator`

## Peamised endpointid

### HTML vaated
- `/` — rollipõhine avalehe suunaja
- `/repairs/` — paranduste nimekiri
- `/repairs/new/` — uue paranduse vorm
- `/repairs/my-work/` — minu tööd
- `/repairs/<id>/` — detailvaade
- `/repairs/<id>/edit/` — muutmise vaade

### JSON / API endpointid
- `/api/repairs/`
- `/api/repairs/export/`
- `/api/repairs/my-work/`
- `/api/repairs/<id>/`
- `/api/repairs/<id>/assign/`
- `/api/repairs/<id>/change-status/`
- `/api/repairs/<id>/change-priority/`
- `/api/repairs/<id>/comments/`
- `/api/repairs/<id>/history/`
- `/api/dashboard/summary/`

## Frontendi tööpõhimõte

Rakendus kasutab mustrit:
- server-renderdatud HTML skeleton
- `fetch`-põhine ühine API-wrapper
- dünaamiline andmelaadimine tabelitele, kokkuvõtetele ja ajaloologle
- CSRF kaitse kirjutavatel päringutel
- globaalne loading indicator

## Testid

Käivita testid:
```bash
python manage.py test
```

## Järgmised sammud

Järgmine loogiline samm on P2 lõpetamine ja seejärel P3/P4 vastavalt vajadusele.

## Notification behavior

Kui `REPAIRPLAN_NOTIFICATIONS_ENABLED=1`, saadetakse e-kirja hookid järgmistes olukordades:
- parandaja määramisel ainult siis, kui määratud kasutaja tegelikult muutub
- staatuse muutmisel ainult siis, kui staatus päriselt muutub

Teavitused kasutavad `DEFAULT_FROM_EMAIL` ja standardset Django mail backendit.
