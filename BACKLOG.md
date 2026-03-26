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

### 1. Projekti bootstrap
- [ ] Luua Django projekt
- [ ] Luua `repairs` app
- [ ] Lisada vajadusel DRF või muu selge JSON endpointi lahendus
- [ ] Seadistada `settings.py` arendusrežiimi jaoks
- [ ] Lisada `requirements.txt`
- [ ] Seadistada templates/static konfiguratsioon
- [ ] Seadistada auth redirectid

### 2. Base layout ja frontend skeleton
- [ ] Luua `templates/base.html`
- [ ] Lisada naviriba
- [ ] Lisada teadete ala
- [ ] Lisada globaalne laadimisindikatsioon
- [ ] Lisada ühised skriptide include’id
- [ ] Lisada rollipõhine navigatsioonistruktuur

### 3. Shared JS layer
- [ ] Luua `static/js/api.js`
- [ ] Rakendada `GET/POST/PATCH/DELETE` wrapperid
- [ ] Lisada automaatne CSRF header kirjutavatele päringutele
- [ ] Lisada JSON request/response käitlus
- [ ] Lisada globaalne loading state hook
- [ ] Lisada keskne veatöötluse muster

### 4. Rakenduse sisemine arhitektuur
- [ ] Luua failid `models.py`, `forms.py`, `serializers.py`, `views.py`, `urls.py`, `admin.py`
- [ ] Luua failid `permissions.py`, `selectors.py`, `services.py`
- [ ] Luua testide baasstruktuur `repairs/tests/`

---

## P0 — Tuumikandmemudel

### 5. Department ja kasutajaga seotud mudelid
- [ ] Luua `Department` mudel
- [ ] Luua `UserProfile` mudel
- [ ] Siduda `UserProfile` kasutaja ja osakonnaga
- [ ] Otsustada profiili automaatloomine

### 6. Repair domeenimudel
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
- [ ] Lisada vajalikud indeksid

### 7. Kommentaar ja audit
- [ ] Luua `RepairComment` mudel
- [ ] Luua `RepairStatusLog` mudel
- [ ] Valmistada ette auditlogi struktuur staatuse, prioriteedi ja määramise muutuste jaoks

### 8. Migratsioonid ja admin
- [ ] Luua migratsioonid
- [ ] Registreerida kõik mudelid adminis
- [ ] Lisada admin search/filter/list display konfiguratsioonid
- [ ] Veenduda, et admin on päriselt kasulik

---

## P1 — Rollid, õigused ja äriloogika

### 9. Rollimudel
- [ ] Luua Django Groupid:
  - [ ] `department_manager`
  - [ ] `repair_master`
  - [ ] `repairer`
  - [ ] `administrator`
- [ ] Luua helperid rolli kontrollimiseks
- [ ] Dokumenteerida rollide õiguste maatriks kooditasemel

### 10. Permission layer
- [ ] Rakendada `permissions.py`
- [ ] Jõustada rollipõhine nähtavus HTML vaadetes
- [ ] Jõustada rollipõhine nähtavus JSON endpointidel
- [ ] Jõustada osakonna juhi nähtavus ainult oma osakonnale
- [ ] Jõustada parandaja nähtavus ainult talle määratud töödele

### 11. Selectors layer
- [ ] Luua selectorid paranduste listimiseks rolli järgi
- [ ] Luua selector “my work” vaate ja endpointi jaoks
- [ ] Luua selector dashboard kokkuvõtte jaoks
- [ ] Hoida päringuloogika vaadetest eraldi

### 12. Services layer
- [ ] Luua service paranduse loomiseks
- [ ] Luua service paranduse uuendamiseks
- [ ] Luua service parandaja määramiseks
- [ ] Luua service staatuse muutmiseks
- [ ] Luua service prioriteedi muutmiseks
- [ ] Lisada auditlogi kirjutamine service tasemel
- [ ] Lisada workflow valideerimine service tasemel

### 13. Forms + serializers
- [ ] Luua server-renderdatud vormid HTML vaadete jaoks
- [ ] Luua serializerid JSON endpointide jaoks
- [ ] Veenduda, et forms/serializers ei kanna põhiäriloogikat

---

## P1 — MVP vaated ja endpointid

### 14. Autentimine
- [ ] Luua login vaade
- [ ] Seadistada logout
- [ ] Kontrollida anonüümse kasutaja ligipääsu piiramine

### 15. Paranduste üldnimekiri
- [ ] Luua server-renderdatud list page
- [ ] Luua filtrite UI
- [ ] Luua tabeli skeleton
- [ ] Luua list data endpoint
- [ ] Lisada otsing `product_code` järgi
- [ ] Lisada filtrid: department, client_or_group, status, priority, assigned_to
- [ ] Lisada sort `created_at` järgi
- [ ] Lisada pagination
- [ ] Lisada staatuse/prioriteedi badge’id

### 16. Uue paranduse lisamine
- [ ] Luua create form
- [ ] Luua create view
- [ ] Luua create template
- [ ] Seada `created_by` automaatselt sessiooni kasutajast
- [ ] Seada `created_at` automaatselt
- [ ] Piirata osakonna juhi sisestusõigused vastavalt ärireeglitele

### 17. Paranduse detailvaade
- [ ] Luua detail page
- [ ] Luua detail template skeleton
- [ ] Kuvada põhiandmete baasserverrenderdus
- [ ] Luua detail data endpointid kommentaaride ja ajaloo jaoks
- [ ] Kuvada rollipõhised tegevused

### 18. Paranduse muutmise vaade
- [ ] Luua update form(id)
- [ ] Luua update view
- [ ] Luua update template
- [ ] Luua vajalikud partial update / action endpointid
- [ ] Rakendada erinevad muutmisõigused rolli järgi

### 19. Parandaja “Minu tööd”
- [ ] Luua “my work” page
- [ ] Luua vastav template
- [ ] Luua “my work” data endpoint
- [ ] Lubada kiireid staatusemuudatusi lubatud workflow piires
- [ ] Lubada kommentaari lisamine

### 20. Dashboard
- [ ] Luua dashboard page
- [ ] Luua dashboard template skeleton
- [ ] Luua dashboard summary endpoint
- [ ] Näidata:
  - [ ] alustamata tööde arv
  - [ ] töös tööde arv
  - [ ] lõpetatud tööde arv
  - [ ] kõrge prioriteediga tööde arv
  - [ ] vanimad avatud tööd
  - [ ] tööde arv parandajate kaupa
- [ ] Lisada Chart.js ainult siis, kui see päriselt parandab loetavust

---

## P2 — Tootmisküpsemus ja kvaliteet

### 21. Workflow hardening
- [ ] Kodeerida lubatud staatuse üleminekud ühes kohas
- [ ] Tagada, et parandaja ei saa teha suvalisi üleminekuid
- [ ] Tagada, et meister saab teha äriliselt lubatud üleminekuid
- [ ] Lisada kasutajasõbralikud veateated keelatud muudatuste korral

### 22. Kommentaarid ja auditlogi viimistleminen
- [ ] Siduda kommentaaride lisamine detailvaatega
- [ ] Näidata kommentaaridel autorit ja aega
- [ ] Näidata auditlogis väljanime, vana väärtust, uut väärtust ja muutjat
- [ ] Otsustada, kas kirje loomine logitakse samuti auditisse

### 23. Export
- [ ] Lisada CSV export
- [ ] Tagada, et export austab samu permissioneid nagu list vaade/endpoint
- [ ] Jätta Excel export hilisemaks

### 24. Dokumentatsioon ja käivitusjuhend
- [ ] Uuendada `README.md`, et selles oleks käivitusjuhend
- [ ] Lisada lokaalse arenduse sammud
- [ ] Lisada migratsioonide käivitamise juhis
- [ ] Lisada superuseri loomise juhis
- [ ] Lisada JS wrapperi ja endpointide lühikokkuvõte

### 25. Testid
- [ ] Lisada permission testid
- [ ] Lisada form testid
- [ ] Lisada serializer testid
- [ ] Lisada HTML view testid
- [ ] Lisada JSON endpointide testid
- [ ] Lisada workflow service testid
- [ ] Lisada vähemalt üks export test

---

## P3 — Hilisemad laiendused

### 26. UX laiendused
- [ ] Lisada rohkem korduvkasutatavaid UI komponente
- [ ] Parandada tabeli jõudlust suurema andmemahu korral
- [ ] Lisada rikkam visualiseerimine ainult seal, kus see päriselt aitab

### 27. Teavitused
- [ ] Valmistada ette hook’id e-posti teavituste lisamiseks
- [ ] Lisada võimalik assignment/status notification flow hiljem

### 28. Infra ja skaleeruvus
- [ ] Lisada PostgreSQL tootmiskonfiguratsioon
- [ ] Valmistada ette keskkonnamuutujate põhine seadistus
- [ ] Hinnata background job lahendust (Celery või RQ)

### 29. Laiendused ja integratsioonid
- [ ] Hinnata väliste integratsioonide API vajadust hiljem
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
