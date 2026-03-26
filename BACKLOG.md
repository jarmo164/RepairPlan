# RepairPlan Backlog

See backlog on koostatud failide `PROMPT.md`, `ARCHITECTURE.md` ja `IMPLEMENTATION_PLAN.md` põhjal.

Eesmärk on viia projekt REST API põhise ehituseni nii, et backend oleks rolliteadlik, auditeeritav ja valmis eraldi frontend kliendi jaoks.

## Prioriteedid
- **P0** — kriitiline vundament
- **P1** — MVP jaoks vajalik funktsionaalsus
- **P2** — oluline tootmisküpsemus
- **P3** — hilisem laiendus

## Arhitektuuri ülevaatuse kokkuvõte

Pärast dokumentatsiooni uuendamist on valitud suund järgmine:
- Django + DRF backend
- eraldi frontend klient
- Django Groups põhine rollimudel
- backendis jõustatud permissionid
- `Department`, `UserProfile`, `Repair`, `RepairComment`, `RepairStatusLog` kui tuumikmudelid
- `serializers.py`, `selectors.py`, `services.py`, `permissions.py` kui kohustuslikud kihid

---

## P0 — Backendi vundament

### 1. Projekti bootstrap
- [ ] Luua Django projekt
- [ ] Luua `repairs` app
- [ ] Lisada Django REST Framework
- [ ] Seadistada `settings.py` arendusrežiimi jaoks
- [ ] Lisada `requirements.txt`
- [ ] Seadistada API routing
- [ ] Otsustada auth strateegia v1 jaoks (session vs token vs JWT)

### 2. Rakenduse sisemine arhitektuur
- [ ] Luua failid `models.py`, `serializers.py`, `views.py`, `urls.py`, `admin.py`
- [ ] Luua failid `permissions.py`, `selectors.py`, `services.py`
- [ ] Luua testide baasstruktuur `repairs/tests/`
- [ ] Luua minimaalne auth/template tugi ainult siis, kui backend login või admin seda vajab

### 3. Tuumikandmemudel
- [ ] Luua `Department` mudel
- [ ] Luua `UserProfile` mudel
- [ ] Luua `Repair` mudel
- [ ] Luua `RepairComment` mudel
- [ ] Luua `RepairStatusLog` mudel
- [ ] Defineerida `Status` ja `Priority` choices
- [ ] Lisada vajalikud indeksid
- [ ] Luua migratsioonid

### 4. Admin ja algseadistus
- [ ] Registreerida kõik mudelid adminis
- [ ] Seadistada admin list/filter/search vaated
- [ ] Luua grupid: `department_manager`, `repair_master`, `repairer`, `administrator`
- [ ] Valmistada ette superuser / initial seed loogika

---

## P1 — Permissionid ja äriloogika

### 5. Permission layer
- [ ] Rakendada `permissions.py`
- [ ] Jõustada rollipõhine nähtavus kõikidel endpointidel
- [ ] Jõustada osakonna juhi nähtavus ainult oma osakonnale
- [ ] Jõustada parandaja nähtavus ainult talle määratud töödele
- [ ] Jõustada meistri ja administraatori laiem nähtavus

### 6. Selectors layer
- [ ] Luua selectorid paranduste listimiseks rolli järgi
- [ ] Luua selector “my work” endpointi jaoks
- [ ] Luua selector dashboard summary jaoks
- [ ] Hoida päringuloogika API vaadetest eraldi

### 7. Services layer
- [ ] Luua service paranduse loomiseks
- [ ] Luua service paranduse uuendamiseks
- [ ] Luua service parandaja määramiseks
- [ ] Luua service staatuse muutmiseks
- [ ] Luua service prioriteedi muutmiseks
- [ ] Lisada auditlogi kirjutamine service tasemel
- [ ] Lisada workflow valideerimine service tasemel

### 8. Serializerid
- [ ] Luua repair list serializer
- [ ] Luua repair detail serializer
- [ ] Luua repair create/update serializerid
- [ ] Luua comment serializerid
- [ ] Luua dashboard summary serializer või response schema
- [ ] Veenduda, et serializerid ei kanna äriloogika põhiraskust

---

## P1 — MVP API endpointid

### 9. Auth API
- [ ] Luua login lahendus v1 valitud auth strateegia järgi
- [ ] Luua logout lahendus
- [ ] Luua `me` endpoint

### 10. Repairs API
- [ ] `GET /api/repairs/`
- [ ] `POST /api/repairs/`
- [ ] `GET /api/repairs/{id}/`
- [ ] `PATCH /api/repairs/{id}/`
- [ ] Lisada otsing `product_code` järgi
- [ ] Lisada filtrid: department, client_or_group, status, priority, assigned_to
- [ ] Lisada sort `created_at` järgi
- [ ] Lisada pagination

### 11. Workflow action endpointid
- [ ] `POST /api/repairs/{id}/assign/`
- [ ] `POST /api/repairs/{id}/change-status/`
- [ ] `POST /api/repairs/{id}/change-priority/`

### 12. Comments API
- [ ] `GET /api/repairs/{id}/comments/`
- [ ] `POST /api/repairs/{id}/comments/`

### 13. Dashboard API
- [ ] `GET /api/dashboard/summary/`
- [ ] `GET /api/repairs/my-work/`

---

## P2 — Tootmisküpsemus

### 14. Audit ja workflow hardening
- [ ] Logida staatuse muutused `RepairStatusLog` tabelisse
- [ ] Logida prioriteedi muutused
- [ ] Logida määramise muudatused
- [ ] Otsustada, kas kirje loomine logitakse samuti auditisse
- [ ] Lisada selged veateated keelatud workflow üleminekute korral

### 15. Export
- [ ] Lisada `GET /api/repairs/export/` CSV jaoks
- [ ] Tagada, et export austab samu permissioneid nagu list endpoint
- [ ] Hoida Excel export hilisemaks

### 16. Dokumentatsioon ja käivitusjuhend
- [ ] Uuendada `README.md`, et seal oleks käivitusjuhend
- [ ] Lisada lokaalse arenduse sammud
- [ ] Lisada migratsioonide käivitamise juhis
- [ ] Lisada superuseri loomise juhis
- [ ] Lisada auth strateegia kirjeldus
- [ ] Lisada API endpointide lühikokkuvõte

### 17. Testid
- [ ] Lisada permission testid
- [ ] Lisada serializer testid
- [ ] Lisada API view testid
- [ ] Lisada workflow service testid
- [ ] Lisada vähemalt üks export test

---

## P3 — Hilisemad laiendused

### 18. Frontend integratsioon
- [ ] Lukustada frontend stack
- [ ] Siduda frontend auth flow backendiga
- [ ] Lisada frontendis rollipõhine UI nähtavus

### 19. Teavitused
- [ ] Valmistada ette hook’id e-posti teavituste lisamiseks
- [ ] Lisada võimalik assignment/status notification flow hiljem

### 20. Infra ja skaleeruvus
- [ ] Lisada PostgreSQL tootmiskonfiguratsioon
- [ ] Valmistada ette keskkonnamuutujate põhine seadistus
- [ ] Hinnata background job lahendust (Celery või RQ)
- [ ] Hinnata API versioneerimise vajadust hiljem

### 21. Laiendused ja integratsioonid
- [ ] Hinnata REST API täiendavaid tarbijaid (mobiil, integratsioonid)
- [ ] Lisada täiendavad raportid ärilise vajaduse tekkimisel
- [ ] Vajadusel normaliseerida `client_or_group` eraldi mudeliks

---

## Soovitatud ehitusjärjekord

1. Django + DRF skeleton
2. mudelid + admin + migratsioonid
3. grupid + permission layer
4. selectors + services + serializers
5. repairs API
6. workflow action endpointid
7. comments + my work + dashboard
8. auditlog + export
9. testid
10. README käivitusjuhend + frontend integratsiooni ettevalmistus

---

## Definition of Done — MVP

MVP võib lugeda valmis siis, kui:
- kasutaja saab autentida valitud API auth strateegiaga
- osakonna juht saab luua paranduse API kaudu
- osakonna juht näeb ainult oma osakonna kirjeid
- meister saab määrata prioriteedi, staatuse ja parandaja
- parandaja näeb ainult oma töid ja saab neid uuendada lubatud workflow piires
- repairs endpoint toetab otsingut, filtreid, sorteerimist ja paginationit
- detailandmed, kommentaarid ja auditlogi on API kaudu kättesaadavad
- dashboard summary endpoint annab kiire juhtimisülevaate
- permissionid on backendis jõustatud
- baas-testid katavad õigused, serializerid ja põhitöövoo
