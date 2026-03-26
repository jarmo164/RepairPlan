# RepairPlan – Implementation Plan

## 1. Eesmärk

RepairPlan on veebipõhine parandustööde haldussüsteem, mis asendab Exceli-põhise käsitsi töövoo. Süsteemi eesmärk on muuta paranduste sisestamine, tööde jaotamine, staatuste haldamine ja juhtimisülevaade üheselt mõistetavaks, jälgitavaks ja skaleeruvaks.

Peamised kasutajad:
- osakonna juhid
- paranduse meister
- parandajad
- administraatorid

## 2. Valitud tehniline lahendus

### Stack
- **Backend:** Django + Django REST Framework
- **Database:** SQLite arenduses, PostgreSQL tootmises
- **Frontend:** eraldi frontend klient, mis tarbib REST API-t
- **Auth:** Django authentication baas, rakendatud API-kõlblikult
- **Permissions:** Django Groups + backend permission layer + queryset filtering
- **Audit log:** oma lihtne mudel
- **Export:** CSV esimeses versioonis, Excel tugi hiljem

### Miks see valik
- jätab parema tee mobiilile ja integratsioonidele
- võimaldab hoida backend loogika ühes kohas ning UI eraldi kihis
- teeb süsteemi API-first, mitte ainult ühe server-rendered veebivaate külge lukustatuks
- on alguses keerulisem kui templates-only lahendus, aga paindlikum pikemas plaanis

## 3. Arhitektuuri põhimõtted

### Disainiprintsiibid
- **Monoliitne backend, selged piirid sees.** Ei ehita mikroteenuste tsirkust.
- **API-first.** Backend modelleerib domeeni ja reegleid; frontend on tarbija.
- **Domain-first mudel.** Parandus, kommentaar, auditlogi ja kasutajarollid on süsteemi tuum.
- **Permission-aware endpoints.** Iga endpoint peab tagastama ainult selle, mida kasutaja tohib näha või muuta.
- **Simple now, extensible later.** Esimene versioon peab töötama hästi, aga jätma ruumi teavitustele, raportitele ja integratsioonidele.

### Soovitatud projektistruktuur
```text
repairplan/
├── manage.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py / asgi.py
├── repairs/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── services.py
│   ├── selectors.py
│   ├── permissions.py
│   └── tests/
├── templates/
│   └── registration/
├── requirements.txt
└── README.md
```

### Miks `services.py`, `selectors.py`, `permissions.py`, `serializers.py`
See ei ole overengineering, vaid odav korrastus.
- `serializers.py` – API sisendi/väljundi skeemid
- `selectors.py` – päringuloogika ja rollipõhised querysetid
- `services.py` – state transitionid, audit log, määramised
- `permissions.py` – keskne koht rollireeglite jaoks

Nii ei paisu API vaated kiiresti poriseks mudaauguks.

## 4. Domeenimudel

## 4.1 Põhiobjektid

### Repair
Põhiüksus, mis kirjeldab parandust vajavat toodet.

Väljad:
- `id`
- `product_code`
- `quantity`
- `client_or_group`
- `department`
- `created_at`
- `created_by`
- `priority`
- `status`
- `assigned_to`
- `comment`
- `updated_at`

### RepairComment
Eraldi kommentaaride tabel, et töö käigus lisanduvad märkused ei jääks ühe tekstivälja otsa rippuma.

Väljad:
- `repair`
- `author`
- `comment`
- `created_at`

### RepairStatusLog
Auditlogi staatuse, prioriteedi ja määramise muutuste jaoks.

Väljad:
- `repair`
- `changed_by`
- `field_name`
- `old_value`
- `new_value`
- `created_at`

### UserProfile või laiendus kasutajale
Kui osakonna juhid peavad nägema ainult oma osakonna kirjeid, peab kasutajal olema seotud osakond.

Valikud:
1. **UserProfile mudel** – praktiline ja lihtne
2. Custom User – paindlikum, aga alguses rohkem setupi

**Soovitus:** võtta **UserProfile**, mitte custom user, kui puudub konkreetne auth-mudeli vajadus.

## 4.2 Enumid

### Priority
- HIGH
- MEDIUM
- LOW

### Status
- NOT_STARTED
- REVIEWED
- IN_PROGRESS
- ON_HOLD
- COMPLETED
- RETURNED

API võib tagastada nii stabiilsed väärtused kui ka inimloetavad labelid.

## 5. Rollid ja õigused

## 5.1 Rollid
Django Groupid:
- `department_manager`
- `repair_master`
- `repairer`
- `administrator`

## 5.2 Õiguste maatriks

### Osakonna juht
Saab:
- lisada uusi parandusi
- näha ainult enda osakonna parandusi
- avada detailendpointi enda osakonna kirjetel

Ei saa:
- määrata parandajat
- muuta globaalset prioriteeti või workflow’d väljaspool lubatud piire
- näha teiste osakondade kirjeid

### Paranduse meister
Saab:
- näha kõiki parandusi
- muuta staatust
- muuta prioriteeti
- määrata parandajat
- lisada kommentaare
- näha dashboardi ja kokkuvõtte endpoint’e

### Parandaja
Saab:
- näha ainult talle määratud parandusi
- muuta oma töö staatust lubatud sammudes
- lisada kommentaare

Ei saa:
- näha kogu süsteemi nimekirja
- muuta teistele määratud töid

### Administraator
Saab:
- hallata kasutajaid
- hallata gruppe ja õigusi
- näha kogu süsteemi
- kasutada admin-paneeli

## 5.3 Tähtis otsus
UI ei tohi olla turvalisuse allikas. Kõik õigused peavad olema backendis jõustatud.

## 6. Töövoog ja staatuse üleminekud

Soovitatud lubatud üleminekud:
- `NOT_STARTED` → `REVIEWED`
- `REVIEWED` → `IN_PROGRESS`
- `IN_PROGRESS` → `ON_HOLD`
- `IN_PROGRESS` → `COMPLETED`
- `ON_HOLD` → `IN_PROGRESS`
- `REVIEWED` → `RETURNED`
- `IN_PROGRESS` → `RETURNED`

Täiendavad reeglid:
- parandaja ei tohiks muuta kirjet suvalisse olekusse; ainult talle lubatud sammudesse
- paranduse meister võib teha kõik äriloogikas lubatud üleminekud
- kõik staatusemuutused logitakse
- üleminekute valideerimine peab elama service layeris

## 7. API ulatus

### 7.1 Auth
- login endpoint või sessioonipõhine auth API-le sobivas vormis
- logout
- current user / me endpoint

### 7.2 Repairs API
- list
- create
- retrieve
- partial update
- assign repairer action
- change status action
- change priority action

### 7.3 Comments API
- list repair comments
- create repair comment

### 7.4 Dashboard API
- summary endpoint
- my work endpoint
- export endpoint

## 8. Frontendi suunised

Kuigi frontend stack ei ole veel lõplikult lukus, peab backend olema sellele valmis.

Põhimõtted:
- frontend ei tohi dubleerida backend security loogikat “tõe allikana”
- frontend võib peita nuppe, aga backend peab otsustama loa
- endpointid peavad olema piisavalt selged, et frontend ei peaks ärireegleid tuletama fragmenteeritud CRUD-ist

## 9. Andmemudeliga seotud praktilised otsused

### Department
Valikud:
1. hoida tekstiväljana
2. teha eraldi `Department` mudel

**Soovitus:** tee kohe eraldi `Department` mudel.

### Client or product group
Esimeses versioonis võib olla tekstiväli. Kui hiljem on vaja normaliseerida, saab sellest teha eraldi mudeli.

### Comment põhimudelis
Prompt nõuab `comment` välja, aga ainult sellest jääb kiiresti väheks.

**Soovitus:**
- jäta `Repair.comment` kui lühike algkommentaar / sissekande märkus
- lisa eraldi `RepairComment`, et töö käigus lisatavad kommentaarid oleks normaalselt hallatavad

## 10. Turvalisus ja andmekontroll

- kõik kirjutavad tegevused ainult autentitud kasutajatele
- turvaline auth/session/token strateegia
- serveripoolne valideerimine kõikidel sisenditel
- query filtering rolli ja osakonna alusel
- audit log kriitiliste muudatuste jaoks
- admin vaade eraldatud ainult admin/grupi kasutajatele

## 11. Skaaleeruvus

Kasvusuunad:
- PostgreSQL tootmises
- indekseerimine väljadele: `status`, `priority`, `created_at`, `assigned_to`, `department`
- pagination list endpointidel
- background jobs teavituste jaoks hiljem (Celery/RQ)
- võimalik hilisem API versioneerimine

## 12. Arendusetapid

## Etapp 1 – Projektiskelet
Eesmärk: backend käima.

Tulemus:
- Django projekt loodud
- `repairs` app loodud
- DRF lisatud
- settings korrastatud
- auth baas seadistatud

## Etapp 2 – Andmemudel ja admin
Eesmärk: tuumik paika.

Tulemus:
- `Department`
- `UserProfile`
- `Repair`
- `RepairComment`
- `RepairStatusLog`
- admin konfiguratsioon
- migratsioonid

## Etapp 3 – Rollid ja permissionid
Eesmärk: nähtavus ja kontroll paika.

Tulemus:
- Django grupid
- helperid rollide kontrolliks
- queryset filtering
- endpoint permissionid

## Etapp 4 – API põhifunktsioonid
Eesmärk: põhitöövoog töötab.

Tulemus:
- repairs list/create/retrieve/update
- comments create/list
- my work
- dashboard summary

## Etapp 5 – Audit, workflow, export
Eesmärk: süsteem oleks päriselu jaoks piisavalt küps.

Tulemus:
- kommentaarid seotud workflowga
- staatuse/prioriteedi muutuste logi
- CSV export
- workflow valideerimine

## Etapp 6 – Testid ja viimistlus
Eesmärk: vähem üllatusi tootmises.

Tulemus:
- permission testid
- serializer testid
- API view testid
- service testid
- README käivitusjuhend

## 13. MVP ulatus

MVP sisaldab:
- autentimist
- rollid
- repair create/list/retrieve/update API
- my work endpoint
- dashboard summary endpoint
- kommentaarid
- auditlogi lihtversioon

MVP-st võib välja jätta:
- email teavitused
- Excel export
- keeruline workflow engine
- realtime uuendused
- avalik API-partnerlus

## 14. Riskid ja tähelepanekud

### Risk 1 – auth ja frontend integratsioon muutub poriseks
Kui auth strateegia jäetakse hägusaks, tekib kiiresti jama.

**Leevendus:** otsustada varakult, kas kasutatakse session authi, token authi või JWT-d.

### Risk 2 – permission-loogika valgub serializeritesse ja viewdesse laiali

**Leevendus:** keskne `permissions.py` + `selectors.py` + `services.py`.

### Risk 3 – API muutub suvaliseks CRUD hunnikuks

**Leevendus:** teha domeenipõhised action endpointid, mitte ainult pime CRUD.

### Risk 4 – frontend hakkab äriloogikat dubleerima

**Leevendus:** hoida tõeline äriloogika backendis.

## 15. Minu konkreetne soovitus

Parim tee on:
1. **Django + DRF backend**
2. **eraldi frontend klient**
3. **Department + UserProfile + Repair + Comment + StatusLog**
4. **Django Groups põhine rollimudel**
5. **SQLite dev / PostgreSQL prod**
6. **CSV export ja auditlog esimesse pärisversiooni**

## 16. Järgmised sammud

Pärast selle plaani kinnitamist teeksin kohe järgmises järjekorras:
1. Django + DRF projekti skeleton
2. andmemudelid + migratsioonid
3. grupid + permission helperid
4. serializers + endpoints
5. dashboard + my work
6. auditlog + kommentaarid + export
