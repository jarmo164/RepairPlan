# RepairPlan – Implementation Plan

## 1. Eesmärk

RepairPlan on veebipõhine parandustööde haldussüsteem, mis asendab Exceli-põhise käsitsi töövoo. Süsteemi eesmärk on muuta paranduste sisestamine, tööde jaotamine, staatuste haldamine ja juhtimisülevaade üheselt mõistetavaks, jälgitavaks ja skaleeruvaks.

Peamised kasutajad:
- osakonna juhid
- paranduse meister
- parandajad
- administraatorid

## 2. Soovitatud tehniline lahendus

### Stack
- **Backend:** Django
- **Database:** SQLite arenduses, PostgreSQL tootmises
- **Frontend:** Django templates + Bootstrap 5
- **Auth:** Django built-in authentication
- **Permissions:** Django groups + object/queryset level filtering rakenduse loogikas
- **Audit log:** oma lihtne mudel (esimese versiooni jaoks piisav)
- **Export:** CSV esimeses versioonis, Excel tugi hiljem

### Miks see valik
- Django annab kiiresti tugeva admini, authi, ORM-i ja vormid.
- Template-põhine UI on selle kasutusjuhtumi jaoks kiirem ja töökindlam kui SPA.
- SQLite võimaldab arendust ilma lisainfrata, PostgreSQL jätab tootmiskindla kasvutee.
- Groups + permission mapping on selle rollimudeli jaoks piisav ega vaja kohe keerulist RBAC-i süsteemi.

## 3. Arhitektuuri põhimõtted

### Disainiprintsiibid
- **Monoliit alguses, selged piirid sees.** Pole mõtet ehitada mikroteenuseid parandustööde tabeli ümber.
- **Domain-first mudel.** Parandus, kommentaar, auditlogi ja kasutajarollid on süsteemi tuum.
- **Permission-aware views.** Iga vaade peab vaikimisi tagastama ainult selle, mida kasutaja tohib näha.
- **Simple now, extensible later.** Esimene versioon peab töötama hästi tootmises, aga jätma ruumi teavitustele, raportitele ja integratsioonidele.

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
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── services.py
│   ├── selectors.py
│   ├── permissions.py
│   └── tests/
├── templates/
│   ├── base.html
│   ├── registration/login.html
│   └── repairs/
├── static/
│   └── css/
├── requirements.txt
└── README.md
```

### Miks `services.py`, `selectors.py`, `permissions.py`
See ei ole overengineering, vaid odav korrastus.
- `selectors.py` – päringuloogika ja rollipõhised querysetid
- `services.py` – state transitionid, audit log, määramised
- `permissions.py` – keskne koht rollireeglite jaoks

Nii ei paisu `views.py` kiiresti poriseks mudaauguks.

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

**Soovitus:** võtta **UserProfile**, mitte custom user. Custom userit tasub teha ainult siis, kui tead ette, et auth-mudel läheb kohe keeruliseks.

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

Kasutajaliideses kuvatakse eestikeelsed nimetused, aga koodis hoitakse stabiilsed ingliskeelsed väärtused.

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

## 5.3 Tähtis otsus: kas kasutada ainult “hidden UI” või päris permissione?
**Õige vastus:** päris permissionid. UI peitmine ilma serveripoole kontrollita on mänguasi, mitte süsteem.

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

## 7. Vaated

## 7.1 Autentimine
- login
- logout
- vajadusel password change hilisemas etapis

## 7.2 Rakenduse põhivaated

### 1. Paranduste üldnimekiri
- tabelivaade
- otsing `product_code` järgi
- filtrid:
  - department
  - client_or_group
  - status
  - priority
  - assigned_to
- sort `created_at` järgi
- rollipõhine nähtavus

### 2. Uue paranduse lisamine
- lihtne vorm osakonna juhile
- `created_by` tuleb automaatselt sessiooni kasutajast
- `created_at` automaatselt

### 3. Paranduse detailvaade
- põhiandmed
- kommentaarid
- staatuse ajalugu
- kiire tegevuspaneel (õiguste põhine)

### 4. Paranduse muutmise vaade
- sõltub rollist
- osakonna juhile piiratud muutmine
- meistrile täislahendus
- parandajale ainult tööga seotud väljad

### 5. Minu tööd
- parandajale filtreeritud nimekiri ainult talle määratud töödest
- kiire status update

### 6. Dashboard
- aktiivsete tööde koguarvud staatuse kaupa
- kõrge prioriteediga tööde arv
- vanimad avatud tööd
- tööde arv parandajate lõikes

## 8. UI / UX lähenemine

### Põhimõtted
- lihtne, robustne, kiire
- töökeskkonda sobiv, mitte “startup demo dashboard”
- tabelid ja vormid on esikohal
- värvikoodid ainult seal, kus need päriselt aitavad

### Bootstrap 5 kasutus
- navbar + sisupaneel
- kaart dashboardi KPI-de jaoks
- badge’id staatuse ja prioriteedi jaoks
- responsiivne tabel koos filtrireaga

### Soovitatud visuaalne loogika
- Staatused badge’idega:
  - Alustamata – hall
  - Üle vaadatud – sinine
  - Töös – kollane / oranž
  - Ootel – tumehall
  - Lõpetatud – roheline
  - Tagastatud – punane
- Prioriteedid:
  - Kõrge – punane
  - Keskmine – kollane
  - Madal – sinine või hall

## 9. Andmemudeliga seotud praktilised otsused

### Department
Valikud:
1. hoida tekstiväljana
2. teha eraldi `Department` mudel

**Soovitus:** tee kohe eraldi `Department` mudel.
Põhjus: õigused, filtrid ja raportid muutuvad oluliselt puhtamaks.

### Client or product group
Esimeses versioonis võib olla tekstiväli. Kui hiljem on vaja normaliseerida, saab sellest teha eraldi mudeli.

### Comment põhimudelis
README nõuab `comment` välja, aga ainult sellest jääb kiiresti väheks.

**Soovitus:**
- jäta `Repair.comment` kui lühike algkommentaar / sissekande märkus
- lisa eraldi `RepairComment`, et töö käigus lisatavad kommentaarid oleks normaalselt hallatavad

## 10. Turvalisus ja andmekontroll

- kõik kirjutavad tegevused ainult autentitud kasutajatele
- CSRF kaitse Django defaultiga
- serveripoolne valideerimine kõikidel vormidel
- query filtering rolli ja osakonna alusel
- audit log kriitiliste muudatuste jaoks
- admin vaade eraldatud ainult admin/grupi kasutajatele

## 11. Skaaleeruvus

Süsteem ei vaja alguses keerulist hajuslahendust, aga peaks jääma puhas kasvuks.

Kasvusuunad:
- PostgreSQL tootmises
- indekseerimine väljadele: `status`, `priority`, `created_at`, `assigned_to`, `department`
- pagination nimekirjavaates
- background jobs teavituste jaoks hiljem (Celery/RQ)
- API kiht hilisemaks mobiili või integratsioonide tarbeks

## 12. Arendusetapid

## Etapp 1 – Projektiskelet
Eesmärk: projekt käima.

Tulemus:
- Django projekt loodud
- `repairs` app loodud
- settings korrastatud
- auth, static, templates seadistatud
- Bootstrap baaslayout lisatud

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
- vaadete piiramine

## Etapp 4 – CRUD ja töövaated
Eesmärk: põhitöövoog töötab.

Tulemus:
- paranduste nimekiri
- lisamine
- detail
- muutmine
- minu tööd

## Etapp 5 – Dashboard ja raporti baas
Eesmärk: juhtimisülevaade.

Tulemus:
- KPI plokid
- vanimad avatud tööd
- tööde arv parandajate kaupa

## Etapp 6 – Audit, kommentaarid, CSV export
Eesmärk: süsteem oleks päriselu jaoks piisavalt küps.

Tulemus:
- kommentaaride lisamine detailvaates
- staatuse/prioriteedi muutuste logi
- CSV eksport filtritega nimekirjast

## Etapp 7 – Viimistlus ja testid
Eesmärk: vähem üllatusi tootmises.

Tulemus:
- permission testid
- vormide testid
- põhilised view testid
- UX polish
- README käivitamisjuhend

## 13. MVP ulatus

Kui eesmärk on kiiresti saada kasutatav esimene versioon, siis MVP sisaldaks:
- login
- rollid
- paranduse loomine
- paranduste nimekiri filtritega
- detailvaade
- parandaja “Minu tööd”
- meistri dashboard
- kommentaarid
- auditlogi lihtversioon

MVP-st võib välja jätta:
- email teavitused
- Excel export (CSV piisab alguses)
- keeruline workflow engine
- REST API
- realtime uuendused

## 14. Riskid ja tähelepanekud

### Risk 1 – õigused vajuvad laiali
Kui permission-loogika jääb viewdesse laiali, muutub süsteem kiiresti hapraks.

**Leevendus:** keskne `permissions.py` + `selectors.py`.

### Risk 2 – üksainus kommentaariväli jääb lahjaks
Kui kasutada ainult `Repair.comment`, kaob tegevusajalugu ära.

**Leevendus:** eraldi kommentaarimudel.

### Risk 3 – osakonna piirangud jäävad kasutajamudelis lahtiseks
Kui kasutajal puudub ametlik seos osakonnaga, ei saa õiguseid usaldusväärselt rakendada.

**Leevendus:** `UserProfile.department`.

### Risk 4 – dashboard ehitatakse enne andmemudeli küpsemist
See tekitab palju ümbertegemist.

**Leevendus:** enne dashboardi peab Repair mudel + rollid olema paigas.

## 15. Minu konkreetne soovitus

Parim tee on:
1. **Django monolith**
2. **Template + Bootstrap UI**
3. **Department + UserProfile + Repair + Comment + StatusLog**
4. **Django Groups põhine rollimudel**
5. **SQLite dev / PostgreSQL prod**
6. **CSV export ja auditlog esimesse pärisversiooni**

See on piisavalt tugev, et mitte laguneda kohe koost, ja piisavalt lihtne, et me ei ehitaks tanki mutrivõtme hoidmiseks.

## 16. Järgmised sammud

Pärast selle plaani kinnitamist teeksin kohe järgmises järjekorras:
1. Django projekti skeleton
2. andmemudelid + migratsioonid
3. grupid + permission helperid
4. list/detail/create/update vaated
5. dashboard
6. auditlog + kommentaarid + export
