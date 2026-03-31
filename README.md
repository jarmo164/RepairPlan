# RepairPlan

RepairPlan on Django-põhine parandustööde haldamise süsteem, mille eesmärk on viia Exceli- ja käsitsi juhitud protsess ühtsesse rollipõhisesse töövoogu.

Projekt on suunatud remondi- ja teenindustiimidele, kus on vaja:
- võtta vastu uusi parandusi
- määrata töid parandajatele
- hallata staatuseid ja prioriteete
- eristada üld- ja elektroonikaparandusi
- jälgida kommentaare, muudatuslugu ja töökoormust

## Mis on hetkel olemas

### Põhivaated
- sisselogimine / väljalogimine
- rollipõhine avalehe suunamine
- paranduste nimekiri filtrite ja CSV ekspordiga
- paranduse loomine ja muutmine
- paranduse detailvaade koos kommentaaride ja ajalooga
- “Minu tööd” vaade parandajale
- “Tööde riiul” määramata tööde jaoks
- dashboard meistrile / administraatorile
- meistri haldusvaade töötajate ja osakondade haldamiseks

### Äriloogika
- rollid: `department_manager`, `repair_master`, `repairer`, `administrator`
- paranduse rada: `Üldine` / `Elektrooniline`
- parandaja specialty: `Üldparandaja` / `Elektrooniline parandaja`
- eraldi staatus `Elektrooniline parandus`
- staatuse muutmine on õigusega kasutajale paindlik
- `Tagastatud` tööd on vaikimisi tava-vaadetest peidetud
- kommentaaride ja muudatuste logimine
- määramise ja staatuse muutuse notification-hookid

### API ja UI tehniline lähenemine
- server-renderdatud Django template skeleton
- JSON endpointid dünaamiliste tabelite ja plokkide jaoks
- Bootstrap + vanilla JavaScript
- DRF-põhised API view’d
- CSRF kaitse kirjutavatele päringutele

## Stack

- **Backend:** Django 6
- **API:** Django REST Framework
- **Frontend:** Django Templates + Bootstrap 5 + vanilla JS
- **Andmebaas:** SQLite arenduses, PostgreSQL tootmises
- **Autentimine:** Django auth
- **Õigused:** Django Groups + eraldi permission/service kiht

## Kiire käivitamine

### 1. Loo virtuaalkeskkond
```bash
python -m venv .venv
source .venv/bin/activate
```

Windows:
```bat
.venv\Scripts\activate
```

### 2. Paigalda sõltuvused
```bash
pip install -r requirements.txt
```

### 3. Rakenda migratsioonid
```bash
python manage.py migrate
```

### 4. Loo vaikimisi rollid
```bash
python manage.py seed_roles
```

### 5. Loo administraator
```bash
python manage.py createsuperuser
```

### 6. Soovi korral lisa demoandmed
```bash
python manage.py seed_demo_data
```

### 7. Käivita arendusserver
```bash
python manage.py runserver
```

Ava:
- rakendus: <http://127.0.0.1:8000/>
- admin: <http://127.0.0.1:8000/admin/>

## Keskkonnamuutujad

Olulisemad seadistused `config/settings.py` põhjal:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DATABASE_ENGINE=sqlite|postgres`
- `DATABASE_NAME`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `REPAIRPLAN_NOTIFICATIONS_ENABLED=1`
- `DEFAULT_FROM_EMAIL`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_USE_TLS=1`

Näidis on failis `.env.example`.

## Rollid ja õigused

### `department_manager`
- näeb oma osakonna parandusi
- saab luua parandusi
- saab oma osakonna piires töid jälgida

### `repair_master`
- näeb kõiki parandusi
- saab määrata parandajaid
- saab muuta prioriteete ja staatuseid
- näeb dashboardi
- saab kasutada meistri haldusvaadet

### `repairer`
- näeb endale määratud töid
- saab muuta oma töö staatust
- saab võtta töid riiulist vastavalt specialty’le

### `administrator`
- sisuliselt täielik ligipääs
- saab lisaks kasutada Django adminit

## Peamised töövood

### Uue paranduse lisamine
1. osakonna juht / meister loob paranduse
2. määratakse osakond, rada, prioriteet ja algkommentaar
3. töö jõuab nimekirja ja vajadusel riiulisse

### Töö määramine
1. meister avab paranduse detaili või kasutab koondvaateid
2. määrab parandaja
3. süsteem logib muudatuse
4. soovi korral käivitub notification-hook

### Töö võtmine riiulist
1. parandaja avab “Tööde riiul” vaate
2. näeb määramata töid
3. elektroonikaparandaja näeb elektroonilisi töid sihitumalt
4. töö muutub määratuks ja logitakse “self claimed”

### Staatuse haldus
- võimalikud staatused:
  - `Alustamata`
  - `Üle vaadatud`
  - `Elektrooniline parandus`
  - `Töös`
  - `Ootel`
  - `Lõpetatud`
  - `Tagastatud`
- `Tagastatud` kirjed on vaikimisi põhivaadetest peidetud, kuid neid saab filtriga kuvada

## URL-id

### HTML vaated
- `/` — rollipõhine redirect
- `/dashboard/` — dashboard
- `/dashboard/manage/` — meistri haldus
- `/repairs/` — paranduste nimekiri
- `/repairs/new/` — uus parandus
- `/repairs/my-work/` — minu tööd
- `/repairs/shelf/` — tööde riiul
- `/repairs/<id>/` — detailvaade
- `/repairs/<id>/edit/` — muutmine

### API endpointid
- `/api/repairs/`
- `/api/repairs/export/`
- `/api/repairs/my-work/`
- `/api/repairs/shelf/`
- `/api/repairs/<id>/`
- `/api/repairs/<id>/assign/`
- `/api/repairs/<id>/change-status/`
- `/api/repairs/<id>/change-priority/`
- `/api/repairs/<id>/save-actions/`
- `/api/repairs/<id>/comments/`
- `/api/repairs/<id>/history/`
- `/api/dashboard/summary/`

## Projekti struktuur

```text
config/                     Django seadistus
repairs/                    põhiäri loogika
  management/commands/      seed käsud
  migrations/               migratsioonid
  tests/                    testid
static/                     CSS/JS
templates/                  HTML template’id
docs/                       lisa-dokumendid
```

Olulisemad failid:
- `repairs/models.py` — andmemudelid
- `repairs/permissions.py` — rollid ja õigused
- `repairs/selectors.py` — päringuloogika
- `repairs/services.py` — ärireeglid ja muutmisteenused
- `repairs/views.py` — HTML + API view’d
- `repairs/serializers.py` — API serialiseerimine

## Testimine

Kõik testid:
```bash
python manage.py test
```

Soovi korral kitsamalt:
```bash
python manage.py test repairs.tests.test_services
python manage.py test repairs.tests.test_api
```

## Notification behavior

Kui `REPAIRPLAN_NOTIFICATIONS_ENABLED=1`, saadetakse e-kirja hookid näiteks:
- parandaja määramisel, kui määratud kasutaja päriselt muutub
- staatuse muutmisel, kui staatus päriselt muutub

Teavitused kasutavad Django mail backendit ja `DEFAULT_FROM_EMAIL` väärtust.

## Dokumentatsioon repo sees

- `ARCHITECTURE.md` — arhitektuuri ülevaade
- `IMPLEMENTATION_PLAN.md` — teostusplaan
- `BACKLOG.md` — tööjärg
- `WORKFLOWS.md` — protsessid
- `USER_STORIES.md` — kasutuslood
- `docs/DEPLOYMENT.md` — deploy märkmed
- `docs/INTEGRATIONS.md` — integratsioonide otsused
- `NEXT_UPDATES_PLAN.md` — järgmiste sammude mõtted
- `docs/IMPROVEMENT_PROPOSALS.md` — praktilised parendusettepanekud

## Hetke hinnang

Projekt on juba täiesti kasutatav sisemise tööriistana:
- rollid ja põhiline õigussüsteem on olemas
- UI katab peamised vood
- dashboard ja shelf annavad operatiivset väärtust
- testibaas on olemas ja jookseb läbi

Suurim järgmine väärtus tuleb nüüd pigem:
1. UX silumisest
2. admin- ja meistrivoogude tugevdamisest
3. tootmiskõlblikust deploy / observability / audit kihist
