# RepairPlan Backlog

See backlog on koostatud failide `PROMPT.md`, `ARCHITECTURE.md` ja `IMPLEMENTATION_PLAN.md` põhjal.

Eesmärk on viia projekt hübriidse SSR arhitektuurini, kus:
- HTML vaated tulevad Django templatemootorist
- vanilla JS lisab dünaamilise andmelaadimise
- backend jõustab rollid, õigused ja workflow reeglid

## Prioriteedid
- **P0** — kriitiline vundament
- **P1** — MVP jaoks vajalik funktsionaalsus
- **P2** — oluline tootmisküpsemus
- **P3** — hilisem laiendus

## Arhitektuuri ülevaatuse kokkuvõte

Valitud suund:
- Django server-renderdatud rakendus
- Bootstrap + ikooniteek
- vanilla JS + ühine `fetch` wrapper
- sisemised JSON / REST-stiilis endpointid dünaamiliste osade jaoks
- Django Groups põhine rollimudel
- backendis jõustatud permissionid
- `Department`, `UserProfile`, `Repair`, `RepairComment`, `RepairStatusLog` kui tuumikmudelid
- `forms.py`, `serializers.py`, `selectors.py`, `services.py`, `permissions.py` kui kohustuslikud kihid

---

## P0 — Vundament

### 1. Projekti bootstrap ✅
- [x] Luua Django projekt
- [x] Luua `repairs` app
- [x] Lisada vajadusel DRF või muu selge JSON endpointi lahendus
- [x] Seadistada `settings.py` arendusrežiimi jaoks
- [x] Lisada `requirements.txt`
- [x] Seadistada templates/static konfiguratsioon
- [x] Seadistada auth redirectid

### 2. Base layout ja frontend skeleton ✅
- [x] Luua `templates/base.html`
- [x] Lisada naviriba
- [x] Lisada teadete ala
- [x] Lisada globaalne laadimisindikatsioon
- [x] Lisada ühised skriptide include’id
- [x] Lisada rollipõhine navigatsioonistruktuur

### 3. Shared JS layer ✅
- [x] Luua `static/js/api.js`
- [x] Rakendada `GET/POST/PATCH/DELETE` wrapperid
- [x] Lisada automaatne CSRF header kirjutavatele päringutele
- [x] Lisada JSON request/response käitlus
- [x] Lisada globaalne loading state hook
- [x] Lisada keskne veatöötluse muster

### 4. Rakenduse sisemine arhitektuur ✅
- [x] Luua failid `models.py`, `forms.py`, `serializers.py`, `views.py`, `urls.py`, `admin.py`
- [x] Luua failid `permissions.py`, `selectors.py`, `services.py`
- [x] Luua testide baasstruktuur `repairs/tests/`

---

## P0 — Tuumikandmemudel

### 5. Department ja kasutajaga seotud mudelid ✅
- [x] Luua `Department` mudel
- [x] Luua `UserProfile` mudel
- [x] Siduda `UserProfile` kasutaja ja osakonnaga
- [x] Otsustada profiili automaatloomine

### 6. Repair domeenimudel ✅
- [x] Luua `Repair` mudel väljadega:
  - [x] `product_code`
  - [x] `quantity`
  - [x] `client_or_group`
  - [x] `department`
  - [x] `created_at`
  - [x] `created_by`
  - [x] `priority`
  - [x] `status`
  - [x] `assigned_to`
  - [x] `comment`
  - [x] `updated_at`
- [x] Defineerida `Status` choices sisemiste stabiilsete väärtustega
- [x] Defineerida `Priority` choices sisemiste stabiilsete väärtustega
- [x] Lisada vajalikud indeksid

### 7. Kommentaar ja audit ✅
- [x] Luua `RepairComment` mudel
- [x] Luua `RepairStatusLog` mudel
- [x] Valmistada ette auditlogi struktuur staatuse, prioriteedi ja määramise muutuste jaoks

### 8. Migratsioonid ja admin ✅
- [x] Luua migratsioonid
- [x] Registreerida kõik mudelid adminis
- [x] Lisada admin search/filter/list display konfiguratsioonid
- [x] Veenduda, et admin on päriselt kasulik

---

## P1 — Rollid, õigused ja äriloogika

### 9. Rollimudel ✅
- [x] Luua Django Groupid:
  - [x] `department_manager`
  - [x] `repair_master`
  - [x] `repairer`
  - [x] `administrator`
- [x] Luua helperid rolli kontrollimiseks
- [x] Dokumenteerida rollide õiguste maatriks kooditasemel

### 10. Permission layer ✅
- [x] Rakendada `permissions.py`
- [x] Jõustada rollipõhine nähtavus HTML vaadetes
- [x] Jõustada rollipõhine nähtavus JSON endpointidel
- [x] Jõustada osakonna juhi nähtavus ainult oma osakonnale
- [x] Jõustada parandaja nähtavus ainult talle määratud töödele

### 11. Selectors layer ✅
- [x] Luua selectorid paranduste listimiseks rolli järgi
- [x] Luua selector “my work” vaate ja endpointi jaoks
- [x] Luua selector dashboard kokkuvõtte jaoks
- [x] Hoida päringuloogika vaadetest eraldi

### 12. Services layer ✅
- [x] Luua service paranduse loomiseks
- [x] Luua service paranduse uuendamiseks
- [x] Luua service parandaja määramiseks
- [x] Luua service staatuse muutmiseks
- [x] Luua service prioriteedi muutmiseks
- [x] Lisada auditlogi kirjutamine service tasemel
- [x] Lisada workflow valideerimine service tasemel

### 13. Forms + serializers ✅
- [x] Luua server-renderdatud vormid HTML vaadete jaoks
- [x] Luua serializerid JSON endpointide jaoks
- [x] Veenduda, et forms/serializers ei kanna põhiäriloogikat

---

## P1 — MVP vaated ja endpointid

### 14. Autentimine ✅
- [x] Luua login vaade
- [x] Seadistada logout
- [x] Kontrollida anonüümse kasutaja ligipääsu piiramine

### 15. Paranduste üldnimekiri ✅
- [x] Luua server-renderdatud list page
- [x] Luua filtrite UI
- [x] Luua tabeli skeleton
- [x] Luua list data endpoint
- [x] Lisada otsing `product_code` järgi
- [x] Lisada filtrid: department, client_or_group, status, priority, assigned_to
- [x] Lisada sort `created_at` järgi
- [x] Lisada pagination
- [x] Lisada staatuse/prioriteedi badge’id

### 16. Uue paranduse lisamine ✅
- [x] Luua create form
- [x] Luua create view
- [x] Luua create template
- [x] Seada `created_by` automaatselt sessiooni kasutajast
- [x] Seada `created_at` automaatselt
- [x] Piirata osakonna juhi sisestusõigused vastavalt ärireeglitele

### 17. Paranduse detailvaade ✅
- [x] Luua detail page
- [x] Luua detail template skeleton
- [x] Kuvada põhiandmete baasserverrenderdus
- [x] Luua detail data endpointid kommentaaride ja ajaloo jaoks
- [x] Kuvada rollipõhised tegevused

### 18. Paranduse muutmise vaade ✅
- [x] Luua update form(id)
- [x] Luua update view
- [x] Luua update template
- [x] Luua vajalikud partial update / action endpointid
- [x] Rakendada erinevad muutmisõigused rolli järgi

### 19. Parandaja “Minu tööd” ✅
- [x] Luua “my work” page
- [x] Luua vastav template
- [x] Luua “my work” data endpoint
- [x] Lubada kiireid staatusemuudatusi lubatud workflow piires
- [x] Lubada kommentaari lisamine

### 20. Dashboard ✅
- [x] Luua dashboard page
- [x] Luua dashboard template skeleton
- [x] Luua dashboard summary endpoint
- [ ] Näidata:
  - [x] alustamata tööde arv
  - [x] töös tööde arv
  - [x] lõpetatud tööde arv
  - [x] kõrge prioriteediga tööde arv
  - [x] vanimad avatud tööd
  - [x] tööde arv parandajate kaupa
- [x] Lisada Chart.js ainult siis, kui see päriselt parandab loetavust

---

## P2 — Tootmisküpsemus ja kvaliteet

### 21. Workflow hardening ✅
- [x] Kodeerida lubatud staatuse üleminekud ühes kohas
- [x] Tagada, et parandaja ei saa teha suvalisi üleminekuid
- [x] Tagada, et meister saab teha äriliselt lubatud üleminekuid
- [x] Lisada kasutajasõbralikud veateated keelatud muudatuste korral

### 22. Kommentaarid ja auditlogi viimistleminen ✅
- [x] Siduda kommentaaride lisamine detailvaatega
- [x] Näidata kommentaaridel autorit ja aega
- [x] Näidata auditlogis väljanime, vana väärtust, uut väärtust ja muutjat
- [x] Otsustada, kas kirje loomine logitakse samuti auditisse

### 23. Export ✅
- [x] Lisada CSV export
- [x] Tagada, et export austab samu permissioneid nagu list vaade/endpoint
- [x] Jätta Excel export hilisemaks

### 24. Dokumentatsioon ja käivitusjuhend ✅
- [x] Uuendada `README.md`, et selles oleks käivitusjuhend
- [x] Lisada lokaalse arenduse sammud
- [x] Lisada migratsioonide käivitamise juhis
- [x] Lisada superuseri loomise juhis
- [x] Lisada JS wrapperi ja endpointide lühikokkuvõte

### 25. Testid ✅
- [x] Lisada permission testid
- [x] Lisada form testid
- [x] Lisada serializer testid
- [x] Lisada HTML view testid
- [x] Lisada JSON endpointide testid
- [x] Lisada workflow service testid
- [x] Lisada vähemalt üks export test

---

## P3 — Hilisemad laiendused

### 26. UX laiendused ✅
- [x] Lisada rohkem korduvkasutatavaid UI komponente
- [x] Parandada tabeli jõudlust suurema andmemahu korral
- [x] Lisada rikkam visualiseerimine ainult seal, kus see päriselt aitab

### 27. Teavitused ✅
- [x] Valmistada ette hook’id e-posti teavituste lisamiseks
- [x] Lisada võimalik assignment/status notification flow hiljem

### 28. Infra ja skaleeruvus ✅
- [x] Lisada PostgreSQL tootmiskonfiguratsioon
- [x] Valmistada ette keskkonnamuutujate põhine seadistus
- [x] Hinnata background job lahendust (Celery või RQ)

### 29. Laiendused ja integratsioonid
- [x] Hinnata väliste integratsioonide API vajadust hiljem
- [ ] Lisada täiendavad raportid ärilise vajaduse tekkimisel
- [ ] Vajadusel normaliseerida `client_or_group` eraldi mudeliks

---

## Soovitatud ehitusjärjekord

1. Django skeleton + settings + auth
2. base template + shared JS wrapper
3. mudelid + admin + migratsioonid
4. grupid + permission layer
5. selectors + services + forms/serializers
6. list/create/detail/update
7. my work
8. dashboard
9. auditlog + export
10. testid
11. README käivitusjuhend + UX polish

---

## Definition of Done — MVP

MVP võib lugeda valmis siis, kui:
- kasutaja saab sisse logida
- osakonna juht saab lisada paranduse
- osakonna juht näeb ainult oma osakonna kirjeid
- meister saab määrata prioriteedi, staatuse ja parandaja
- parandaja näeb ainult oma töid ja saab neid uuendada lubatud workflow piires
- üldnimekiri töötab server-renderdatud skeleton + dünaamilise andmelaadimise mustriga
- detailvaates on näha põhiandmed, kommentaarid ja auditlogi
- dashboard annab kiire juhtimisülevaate
- permissionid on backendis jõustatud
- baas-testid katavad õigused, vormid, endpointid ja põhitöövoo
