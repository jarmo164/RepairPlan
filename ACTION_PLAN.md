# RepairPlan Action Plan

See plaan on koostatud failide `PROMPT.md`, `README.md`, `ARCHITECTURE.md`, `IMPLEMENTATION_PLAN.md`, `BACKLOG.md`, `docs/DEPLOYMENT.md` ja `docs/INTEGRATIONS.md` ning tegeliku koodibaasi hetkeseisu põhjal.

Eesmärk: viia projekt olukorda, kus backlogi avatud või poolikud punktid saavad päriselt valmis ning dokumentatsioon ja kood on kooskõlas.

---

## 1. Hetkeseisu aus kokkuvõte

### Tehtud tugev vundament
- P0 on tehtud
- P1 tuumik on suuresti tehtud
- P2-st on suur osa tehtud
- P3-st on osa tehtud dokumentatsiooni ja ettevalmistuste tasemel

### Peamised päriselt lahtised kohad
1. Detailvaates puudub päris rollipõhine tegevuspaneel
2. "Minu tööd" vaates puudub kommentaari lisamine
3. Dashboardis puudub tööde arv parandajate kaupa
4. Detailvaates puudub kommentaari lisamise UI sidumine
5. Eraldi serializer testid puuduvad
6. HTML view testid puuduvad
7. Tabeli jõudluse parandamine suure andmemahu jaoks on sisuliselt tegemata
8. Notification flow on ainult hookide tasemel, mitte päriselt tootevalmis funktsioonina
9. Raportid ja `client_or_group` normaliseerimine on alles tulevikuteemad, mitte kohe tegemist vajavad asjad

---

## 2. Tööjärjekord

## FAAS A — Sulgeme kõik avatud P1/P2 kriitilised augud

### A1. Detailvaate rollipõhine tegevuspaneel ✅
Eesmärk:
- kuvada detailvaates tegevused sõltuvalt kasutajarollist ja kirje seisust

Teha:
- lisada template’i tegevusplokk
- osakonna juhile piiratud tegevused
- meistrile assign / priority / status tegevused
- parandajale ainult lubatud staatusemuudatused ja kommentaarid
- kasutada olemasolevaid endpoint’e, mitte ehitada uut suvalist rada

Valmis kui:
- detailvaates on visuaalselt nähtavad ainult lubatud tegevused
- backend jääb ikka tõe allikaks

### A2. Kommentaari lisamine detailvaates ✅
Eesmärk:
- viia olemasolev comment POST endpoint päriselt kasutusse detailvaates

Teha:
- lisada kommentaarivorm `repair_detail.html` sisse
- submit läbi `fetch` wrapperi
- pärast lisamist uuendada kommentaaride listi DOM-is
- kuvada vead kasutajale arusaadavalt

Valmis kui:
- detailvaates saab kommentaari lisada ilma lehte refreshimata
- uus kommentaar ilmub kohe nähtavale

### A3. Kommentaari lisamine "Minu tööd" vaates ✅
Eesmärk:
- täita backlogi avatud punkt ausalt päris funktsionaalsusega

Teha:
- lisada my-work vaates igale reale lihtne kommentaari lisamise tegevus
- kas inline väli või modaal
- kasutada olemasolevat comments endpointi

Valmis kui:
- parandaja saab "Minu tööd" vaatest kommentaari lisada

### A4. Dashboard: tööde arv parandajate kaupa ✅
Eesmärk:
- sulgeda avatud dashboardi puudujääk prompti vastu

Teha:
- lisada selector, mis koondab tööde arvu parandaja kaupa
- lisada see summary endpointi või eraldi endpointi
- kuvada dashboardis tabeli või lihtsa chartina

Valmis kui:
- dashboard näitab tööde arvu parandajate kaupa

---

## FAAS B — Sulgeme P2 kvaliteedivõlad

### B1. Serializer testid ✅
Eesmärk:
- mitte tugineda ainult API testidele

Teha:
- lisada eraldi testid vähemalt:
  - `RepairCreateSerializer`
  - `RepairUpdateSerializer`
  - `RepairCommentSerializer`
  - `RepairStatusLogSerializer`

Valmis kui:
- serializeri väljad, validatsioon ja output on otse testitud

### B2. HTML view testid ✅
Eesmärk:
- katta server-renderdatud vaadete põhikäitumine

Teha:
- testid vähemalt vaadetele:
  - repair list
  - repair create
  - repair detail
  - repair update
  - my work
  - dashboard
- kontrollida vähemalt:
  - auth
  - status code
  - põhi-template render
  - nähtavuse piirangud rollide kaupa

Valmis kui:
- HTML vaadete baasregressioonid on testidega kaetud

---

## FAAS C — UX polish, mis päriselt annab väärtust

### C1. List/detail/my-work UX ühtlustus ✅
Teha:
- parandada vormide field styling
- lisada selgemad empty state’id
- ühtlustada nuppude ja badge’ide kasutus
- lisada edukate tegevuste visuaalne tagasiside JS tegevustele

### C2. Suure andmemahu tabeli jõudlus ✅
Teha:
- vähendada tarbetuid DOM ümberrenderdusi
- kasutada väiksemaid render helper’eid
- piirata korraga laetavat andmehulk ja kontrollida pagination flow’d
- vajadusel lisada serveri poolel kitsamad väljad nimekirja jaoks

Valmis kui:
- “jõudluse parandamine” on midagi enamat kui debounce

---

## FAAS D — Teavitused päris funktsioonina

### D1. Notification flow lõpuni ✅
Praegu olemas:
- hookid
- settings toggle

Teha:
- otsustada, millal notif saadetakse
- vältida topeltteavitusi
- dokumenteerida notification behavior README või deployment doci
- lisada testid notification helperitele

Valmis kui:
- teavitused on ennustatavad, mitte lihtsalt koodis vedelevad hookid

---

## FAAS E — Alles siis tulevikulaiendused

### E1. Lisaraportid (deferred)
Teha ainult siis, kui on päris vajadus.
Esimene mõistlik kandidaat:
- backlog by department
- aging report
- turnaround time

### E2. `client_or_group` normaliseerimine (deferred)
Teha ainult siis, kui andmekvaliteet või raportid seda päriselt nõuavad.
Praegu mitte prioriteet.

---

## 3. Konkreetne järgmine tööde järjekord

Soovitatud täitmisjärjekord:
1. A1 — detailvaate rollipõhine tegevuspaneel
2. A2 — detailvaate kommentaari lisamine
3. A3 — my-work kommentaari lisamine
4. A4 — dashboard tööde arv parandajate kaupa
5. B1 — serializer testid
6. B2 — HTML view testid
7. C1 — UX ühtlustus
8. C2 — tabeli jõudluse parandamine
9. D1 — notification flow lõpuni
10. E1 / E2 ainult vajadusel

---

## 4. Definition of Done järgmisele tööblokile

Järgmine tööblokk võib lugeda edukaks siis, kui:
- backlogi avatud P1/P2 funktsionaalsed augud on suletud
- backlogi märgistus ja tegelik kood vastavad üksteisele
- testikate paraneb, mitte ainult feature list ei kasva
- kasutaja saab detailvaates ja my-work vaates päriselt vajalikud põhitegevused tehtud

---

## 5. Minu praktiline soovitus

Ära hüppa praegu uute “võib-olla tore” laienduste juurde.

Kõige mõistlikum on nüüd teha järgmine tööblokk just selles järjekorras:
- detailvaate tegevused
- kommentaarivood
- dashboardi parandaja-jaotus
- testivõlad

See sulgeb suure osa sellest, mis praegu on backlogis ausalt pooleli, ja teeb süsteemi palju terviklikumaks kui järgmise ilusa lisa ehitamine.


## 6. Täitmise staatus

Tehtud selles tööblokis:
- A1, A2, A3, A4
- B1, B2
- C1, C2
- D1

Teadlikult edasi lükatud:
- E1 lisaraportid ainult siis, kui tekib päris äriline vajadus
- E2 `client_or_group` normaliseerimine ainult siis, kui andmekvaliteet või integratsioonid seda nõuavad
