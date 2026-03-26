# RepairPlan Backlog

See backlog on koostatud failide `PROMPT.md`, `ARCHITECTURE.md` ja `IMPLEMENTATION_PLAN.md` põhjal.

Eesmärk ei ole lihtsalt teha “to-do list”, vaid panna paika ehitusjärjekord, mis viib kõige kiiremini töötava, puhta ja edasiarendatava Django rakenduseni.

## Prioriteedid
- **P0** — kriitiline vundament
- **P1** — MVP jaoks vajalik funktsionaalsus
- **P2** — oluline tootmisküpsemus
- **P3** — hilisem laiendus

## Arhitektuuri ülevaatuse kokkuvõte

Pärast `PROMPT.md`, `ARCHITECTURE.md` ja `IMPLEMENTATION_PLAN.md` ülevaatust on põhisuund loogiline ja kooskõlaline.

### Kinnitatud tehnilised otsused
- Django monoliit on õige valik
- Django Templates + Bootstrap 5 on selle kasutusjuhtumi jaoks parem kui SPA
- SQLite arenduseks, PostgreSQL tootmisse
- Rollid lahendada Django Groups kaudu
- Permissionid peavad olema serveripoolel päriselt jõustatud
- `Department`, `UserProfile`, `Repair`, `RepairComment`, `RepairStatusLog` on õige tuumikmudelite komplekt
- `selectors.py`, `services.py`, `permissions.py` tasub kohe sisse planeerida, et vaated ei läheks käest ära

### Täpsustused, mis backlogis nüüd arvesse võetud
- `Department` tuleb teha eraldi mudelina, mitte plain text väljana
- `Repair.comment` jääb alles algkommentaariks, aga töö käigus lisanduvad märkused lähevad `RepairComment` alla
- workflow üleminekud tuleb panna service layerisse, mitte vormi või view sisse laiali
- dashboard tuleb ehitada pärast seda, kui tuumikmudel + õigused on paigas
- README lõpus peab olema ka käivitusjuhend, mitte ainult kontseptsioonidokid
- testid ei ole “kui aega jääb”, vaid vähemalt permissionite, vormide ja põhivaadete baas peab olema MVP osa

---

## P0 — Vundament ja projektistruktuur

### 1. Projekti bootstrap
- [ ] Luua Django projekt
- [ ] Luua `repairs` app
- [ ] Luua `config/` projektistruktuur
- [ ] Seadistada `settings.py` arendusrežiimi jaoks
- [ ] Lisada `requirements.txt`
- [ ] Seadistada templates/static konfiguratsioon
- [ ] Seadistada auth redirectid (`LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL`)

### 2. Rakenduse sisemine arhitektuur
- [ ] Luua failid `models.py`, `views.py`, `forms.py`, `urls.py`, `admin.py`
- [ ] Luua failid `permissions.py`, `selectors.py`, `services.py`
- [ ] Luua testide baasstruktuur `repairs/tests/`
- [ ] Luua `templates/base.html`
- [ ] Luua `templates/registration/login.html`
- [ ] Luua `static/css/` baasstiilide jaoks

### 3. UI vundament
- [ ] Lisada Bootstrap 5 base layout
- [ ] Luua navigeerimise põhistruktuur
- [ ] Luua ühised badge/helper klassid staatuse ja prioriteedi kuvamiseks
- [ ] Hoida UI desktop-first, aga responsiivne

---

## P0 — Tuumikandmemudel

### 4. Department ja kasutajaga seotud mudelid
- [ ] Luua `Department` mudel
- [ ] Luua `UserProfile` mudel
- [ ] Siduda `UserProfile` kasutaja ja osakonnaga
- [ ] Otsustada ja rakendada profiili automaatloomine signaliga või seed/management commandi kaudu

### 5. Repair domeenimudel
- [ ] Luua `Repair` mudel väljadega:
  - [ ] `product_code`
  - [ ] `quantity`
  - [ ] `client_or_group`
  - [ ] `department`
  - [ ] `created_at`
  - [ ] `created_by`
  - [ ] `priority`
  - [ ] `status`
  - [ ] `assigned_to`
  - [ ] `comment`
  - [ ] `updated_at`
- [ ] Defineerida `Status` choices sisemiste stabiilsete väärtustega
- [ ] Defineerida `Priority` choices sisemiste stabiilsete väärtustega
- [ ] Lisada mudeli `Meta` tasemel indeksid väljadele `status`, `priority`, `created_at`, `assigned_to`, `department`

### 6. Kommentaar ja audit
- [ ] Luua `RepairComment` mudel
- [ ] Luua `RepairStatusLog` mudel
- [ ] Valmistada ette auditlogi struktuur vähemalt staatuse, prioriteedi ja määramise muutuste jaoks

### 7. Migratsioonid ja admin
- [ ] Luua migratsioonid
- [ ] Registreerida kõik mudelid Django adminis
- [ ] Lisada admin search/filter/list display konfiguratsioonid
- [ ] Veenduda, et admin on päriselt kasulik, mitte lihtsalt “registreeritud ära”

---

## P1 — Rollid, õigused ja äriloogika

### 8. Rollimudel
- [ ] Luua Django Groupid:
  - [ ] `department_manager`
  - [ ] `repair_master`
  - [ ] `repairer`
  - [ ] `administrator`
- [ ] Luua helperid rolli kontrollimiseks
- [ ] Dokumenteerida rollide õiguste maatriks kooditasemel

### 9. Permission layer
- [ ] Rakendada `permissions.py`
- [ ] Rakendada rollipõhine nähtavus detail-, list- ja update-vaadetes
- [ ] Jõustada osakonna juhi nähtavus ainult oma osakonnale
- [ ] Jõustada parandaja nähtavus ainult talle määratud töödele
- [ ] Jõustada meistri ja administraatori laiem nähtavus

### 10. Selectors layer
- [ ] Luua `selectors.py` paranduste listimiseks rolli järgi
- [ ] Luua selector “my work” vaatele
- [ ] Luua selector dashboardi agregaatide jaoks
- [ ] Hoida päringuloogika vaadetest eraldi

### 11. Services layer
- [ ] Luua service paranduse loomiseks
- [ ] Luua service paranduse uuendamiseks
- [ ] Luua service parandaja määramiseks
- [ ] Luua service staatuse muutmiseks
- [ ] Lisada service tasemel workflow valideerimine
- [ ] Lisada auditlogi kirjutamine service tasemel

---

## P1 — MVP kasutajavaated

### 12. Sisselogimine
- [ ] Luua login vaade/template
- [ ] Seadistada logout
- [ ] Kontrollida anonüümse kasutaja ligipääsu piiramine

### 13. Paranduste üldnimekiri
- [ ] Luua list view
- [ ] Luua vastav template
- [ ] Lisada otsing `product_code` järgi
- [ ] Lisada filtrid:
  - [ ] department
  - [ ] client_or_group
  - [ ] status
  - [ ] priority
  - [ ] assigned_to
- [ ] Lisada sort `created_at` järgi
- [ ] Lisada pagination
- [ ] Lisada staatuse/prioriteedi värvilised badge’id

### 14. Uue paranduse lisamine
- [ ] Luua create form
- [ ] Luua create view
- [ ] Luua create template
- [ ] Seada `created_by` automaatselt sessiooni kasutajast
- [ ] Seada `created_at` automaatselt
- [ ] Piirata osakonna juhi sisestusõigused vastavalt ärireeglitele

### 15. Paranduse detailvaade
- [ ] Luua detail view
- [ ] Luua detail template
- [ ] Kuvada põhiandmed
- [ ] Kuvada määratud parandaja
- [ ] Kuvada algkommentaar
- [ ] Kuvada kommentaaride timeline
- [ ] Kuvada staatuse/prioriteedi muutuste ajalugu
- [ ] Kuvada rollipõhised tegevused detailvaates

### 16. Paranduse muutmise vaade
- [ ] Luua update form(id)
- [ ] Luua update view
- [ ] Luua update template
- [ ] Rakendada erinevad muutmisõigused rolli järgi:
  - [ ] osakonna juht
  - [ ] paranduse meister
  - [ ] parandaja

### 17. Parandaja “Minu tööd”
- [ ] Luua “my work” view
- [ ] Luua vastav template
- [ ] Näidata ainult kasutajale määratud töid
- [ ] Lubada kiireid staatusemuudatusi lubatud workflow piires
- [ ] Lubada kommentaari lisamine

### 18. Dashboard
- [ ] Luua dashboard view
- [ ] Luua dashboard template
- [ ] Näidata:
  - [ ] alustamata tööde arv
  - [ ] töös tööde arv
  - [ ] lõpetatud tööde arv
  - [ ] kõrge prioriteediga tööde arv
  - [ ] vanimad avatud tööd
  - [ ] tööde arv parandajate kaupa

---

## P2 — Tootmisküpsemus ja kvaliteet

### 19. Workflow hardening
- [ ] Kodeerida lubatud staatuse üleminekud ühes kohas
- [ ] Tagada, et parandaja ei saa teha suvalisi üleminekuid
- [ ] Tagada, et meister saab teha äriliselt lubatud üleminekuid
- [ ] Lisada kasutajasõbralikud veateated keelatud muudatuste korral

### 20. Kommentaarid ja auditlogi viimistleminen
- [ ] Siduda kommentaaride lisamine detailvaatega
- [ ] Näidata kommentaaridel autorit ja aega
- [ ] Näidata auditlogis väljanime, vana väärtust, uut väärtust ja muutjat
- [ ] Otsustada, kas kirje loomine ise logitakse samuti auditisse

### 21. Export
- [ ] Lisada CSV export üldnimekirja filtrite pealt
- [ ] Tagada, et export austab samu permissioneid nagu list view
- [ ] Jätta Excel export hilisemaks

### 22. Käivitus- ja kasutusjuhend
- [ ] Uuendada `README.md`, et selles oleks ka käivitusjuhend
- [ ] Lisada lokaalse arenduse sammud
- [ ] Lisada migratsioonide käivitamise juhis
- [ ] Lisada superuseri loomise juhis
- [ ] Lisada lühike ülevaade rollidest

### 23. Testid
- [ ] Lisada permission testid
- [ ] Lisada vormide valideerimise testid
- [ ] Lisada põhivaadete testid
- [ ] Lisada workflow teenuste testid
- [ ] Lisada vähemalt üks test exportile

### 24. UX polish
- [ ] Parandada vormide loogikat ja veateateid
- [ ] Lisada tühjade vaadete sõnumid
- [ ] Hoida tabelid loetavad ka suurema andmemahu korral
- [ ] Parandada navigeerimist rolli järgi

---

## P3 — Hilisemad laiendused

### 25. Teavitused
- [ ] Valmistada ette hook’id e-posti teavituste lisamiseks
- [ ] Lisada võimalik assignment/status notification flow hiljem

### 26. Infra ja skaleeruvus
- [ ] Lisada PostgreSQL tootmiskonfiguratsioon
- [ ] Valmistada ette keskkonnamuutujate põhine seadistus
- [ ] Hinnata background job lahendust (Celery või RQ) kui teavitused päriselt tulevad

### 27. Laiendused ja integratsioonid
- [ ] Hinnata REST API vajadust alles siis, kui tuleb reaalne integratsioonivajadus
- [ ] Lisada täiendavad raportid ainult ärilise vajaduse tekkimisel
- [ ] Vajadusel normaliseerida `client_or_group` eraldi mudeliks hilisemas etapis

---

## Soovitatud ehitusjärjekord

1. Projektiskelet + settings + auth + base layout
2. Department / UserProfile / Repair / Comment / StatusLog mudelid
3. Admin + migratsioonid + grupid
4. Permission, selector ja service layer
5. List + create + detail + update
6. My Work
7. Dashboard
8. Workflow hardening + auditlogi sidumine
9. CSV export
10. Testid
11. README käivitusjuhend + UX polish

---

## Definition of Done — MVP

MVP võib lugeda valmis siis, kui:
- kasutaja saab sisse logida
- osakonna juht saab lisada paranduse
- osakonna juht näeb ainult oma osakonna kirjeid
- meister saab määrata prioriteedi, staatuse ja parandaja
- parandaja näeb ainult oma töid ja saab neid uuendada lubatud workflow piires
- üldnimekiri toetab otsingut, filtreid, sorteerimist ja paginationit
- detailvaates on näha põhiandmed, kommentaarid ja auditlogi
- dashboard annab kiire juhtimisülevaate
- permissionid on serveripoolel jõustatud
- vähemalt baas-testid katavad õigused, vormid ja põhitöövoo
