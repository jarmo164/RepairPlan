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
- **Backend:** Django
- **Data/API layer:** Django REST Framework või sihitud JSON endpointid
- **Database:** SQLite arenduses, PostgreSQL tootmises
- **Frontend:** Django templates + Bootstrap + vanilla JavaScript
- **Auth:** Django authentication
- **Permissions:** Django Groups + backend permission layer + queryset filtering
- **Audit log:** oma lihtne mudel
- **Export:** CSV esimeses versioonis, Excel tugi hiljem
- **Charts:** vajadusel Chart.js

### Miks see valik
- jätab alles lihtsa ja stabiilse Django auth / template mudeli
- võimaldab dünaamilist andmelaadimist ilma SPA keerukuseta
- sobib väga hästi sisekasutuse infosüsteemile
- hoiab õigused ja äriloogika backendis
- väldib tarbetut frontend build chain’i

## 3. Arhitektuuri põhimõtted

### Disainiprintsiibid
- **Server-rendered first, enrich second.** Esmalt tuleb HTML skeleton serverist, siis JS rikastab.
- **Monoliitne backend, selged piirid sees.** Ei ehita mikroteenuste karnevali.
- **Domain-first mudel.** Parandus, kommentaar, auditlogi ja kasutajarollid on süsteemi tuum.
- **Permission-aware views ja endpointid.** Iga HTML vaade ja JSON endpoint peab tagastama ainult selle, mida kasutaja tohib näha või muuta.
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
│   ├── forms.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── services.py
│   ├── selectors.py
│   ├── permissions.py
│   └── tests/
├── templates/
│   ├── base.html
│   ├── registration/
│   └── repairs/
├── static/
│   ├── css/
│   └── js/
├── requirements.txt
└── README.md
```

### Miks `services.py`, `selectors.py`, `permissions.py`, `serializers.py`
See ei ole overengineering, vaid odav korrastus.
- `forms.py` – server-renderdatud vormide valideerimine
- `serializers.py` – JSON sisendi/väljundi skeemid
- `selectors.py` – päringuloogika ja rollipõhised querysetid
- `services.py` – state transitionid, audit log, määramised
- `permissions.py` – keskne koht rollireeglite jaoks

Nii ei paisu HTML vaated, API endpointid ega JS poriseks mudaauguks.

## 4. Frontendi põhimuster

Lahendus töötab mustriga:

**server-renderdatud skeleton + kliendipoolne rikastus**

See tähendab:
1. server renderdab page shelli, navigatsiooni, filtrid, placeholderid ja põhilise struktuuri
2. ühine JS kiht laeb detailandmed või tabeliandmed API kaudu
3. DOM-i uuendatakse lokaalselt seal, kus see on kasulik

### Ühine base template peab sisaldama
- naviriba
- teadete ala
- globaalset laadimisindikatsiooni
- korduvkasutatavaid UI komponente
- ühist skriptikihti
- rollipõhist navigatsiooni

### Ühine JS API-wrapper peab
- toetama `GET/POST/PATCH/DELETE`
- lisama automaatselt CSRF kaitse kirjutavatele päringutele
- tegelema JSON payloadidega
- kuvama kasutajale globaalse laadimisoleku
- koondama veatöötluse ühte kohta

## 5. Domeenimudel

## 5.1 Põhiobjektid

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

## 5.2 Enumid

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

JSON vastused võivad tagastada nii stabiilsed väärtused kui ka inimloetavad labelid.

## 6. Rollid ja õigused

## 6.1 Rollid
Django Groupid:
- `department_manager`
- `repair_master`
- `repairer`
- `administrator`

## 6.2 Õiguste maatriks

### Osakonna juht
Saab:
- lisada uusi parandusi
- näha ainult enda osakonna parandusi
- avada detailvaadet enda osakonna kirjetel

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
- näha dashboardi ja kokkuvõtteid

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

## 6.3 Tähtis otsus
UI ei tohi olla turvalisuse allikas. Kõik õigused peavad olema backendis jõustatud.

## 7. Töövoog ja staatuse üleminekud

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

## 8. Vaated ja endpointid

### 8.1 HTML vaated
Rakenduses peavad olema vähemalt järgmised server-renderdatud vaated:
- sisselogimise vaade
- paranduste üldnimekirja vaade
- uue paranduse lisamise vorm
- paranduse detailvaade
- paranduse muutmise vaade
- minu tööde vaade parandajale
- kokkuvõtte või dashboardi vaade paranduse meistrile

### 8.2 JSON / API endpointid
Dünaamilise andmelaadimise jaoks:
- repairs list endpoint
- repairs detail endpoint
- repairs partial update endpoint
- assign action endpoint
- status change endpoint
- priority change endpoint
- comments list/create endpointid
- dashboard summary endpoint
- my work endpoint
- export endpoint

## 9. UI / UX suunised

### Bootstrap-põhine kasutajaliides
- ühine baasmall
- naviriba
- tabelid
- vormid
- modaalid
- badge’id staatuse ja prioriteedi jaoks
- teadete ala
- globaalne loading state

### Lehtede tööpõhimõte
- skeleton renderdatakse serverist
- tabeliread, kokkuvõtteplokid ja muud dünaamilised osad laetakse vajadusel API kaudu
- Chart.js kasutatakse ainult seal, kus visuaal päriselt annab väärtust

## 10. Turvalisus ja andmekontroll

- kõik kirjutavad tegevused ainult autentitud kasutajatele
- CSRF kaitse kirjutavatel päringutel
- serveripoolne valideerimine kõikidel sisenditel
- query filtering rolli ja osakonna alusel
- audit log kriitiliste muudatuste jaoks
- admin vaade eraldatud ainult admin/grupi kasutajatele

## 11. Skaaleeruvus

Kasvusuunad:
- PostgreSQL tootmises
- indekseerimine väljadele: `status`, `priority`, `created_at`, `assigned_to`, `department`
- pagination list vaadetes ja endpointidel
- background jobs teavituste jaoks hiljem (Celery/RQ)
- võimalik hilisem väliste integratsioonide API kiht

## 12. Arendusetapid

## Etapp 1 – Projektiskelet
Eesmärk: backend ja HTML raamistik käima.

Tulemus:
- Django projekt loodud
- `repairs` app loodud
- settings korrastatud
- auth baas seadistatud
- base template loodud
- JS wrapperi raamistik loodud

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
- HTML vaadete ja endpointide permissionid

## Etapp 4 – HTML vaated + API rikastus
Eesmärk: põhitöövoog töötab.

Tulemus:
- repairs list/create/detail/update vaated
- my work vaade
- dashboard vaade
- vajalikud data endpointid
- ühine API wrapper

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
- form testid
- serializer testid
- view testid
- service testid
- README käivitusjuhend

## 13. MVP ulatus

MVP sisaldab:
- autentimist
- rollid
- server-renderdatud põhivaated
- JSON endpointid dünaamiliste osade jaoks
- my work
- dashboard
- kommentaarid
- auditlogi lihtversioon

MVP-st võib välja jätta:
- email teavitused
- Excel export
- keeruline workflow engine
- realtime uuendused
- raske frontend framework

## 14. Riskid ja tähelepanekud

### Risk 1 – JS kiht muutub mini-SPA sodiks

**Leevendus:** hoida JS fokusseeritud rikastuskihina, mitte rakenduse teise ajustikuna.

### Risk 2 – permission-loogika valgub vaadetesse ja endpointidesse laiali

**Leevendus:** keskne `permissions.py` + `selectors.py` + `services.py`.

### Risk 3 – lehed muutuvad tühjaks skeletoniks ilma kasutatava baasrenderduseta

**Leevendus:** server-renderdatud HTML peab jääma sisuliseks, mitte ainult loading screeniks.

### Risk 4 – API wrapper dubleerib suvalist loogikat iga lehe peal

**Leevendus:** hoida ühine fetch wrapper ja standardsed DOM update mustrid.

## 15. Minu konkreetne soovitus

Parim tee on:
1. **Django server-renderdatud rakendus**
2. **Bootstrap + vanilla JS**
3. **ühine fetch-põhine API wrapper**
4. **Department + UserProfile + Repair + Comment + StatusLog**
5. **Django Groups põhine rollimudel**
6. **SQLite dev / PostgreSQL prod**
7. **CSV export ja auditlog esimesse pärisversiooni**

## 16. Järgmised sammud

Pärast selle plaani kinnitamist teeksin kohe järgmises järjekorras:
1. Django projekti skeleton
2. base template + JS wrapper skeleton
3. andmemudelid + migratsioonid
4. grupid + permission helperid
5. HTML vaated + JSON endpointid
6. dashboard + my work
7. auditlog + kommentaarid + export
