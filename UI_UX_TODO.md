# RepairPlan UI/UX To-Do

See dokument kirjeldab järgmist UX/UI paranduste paketti eesmärgiga muuta RepairPlan visuaalselt juhtivamaks, loogilisemaks ja rolliteadlikumaks.

Fookus ei ole “ilusam admin”, vaid:
- tähtsa info parem esiletõstmine
- järgmise tegevuse selgem nähtavus
- rollipõhine töövoog ilma liigse mõtlemiseta
- parem leitavus ja visuaalne hierarhia

---

# 1. Üldised UI põhimõtted ✅

## Eesmärgid
- kasutaja peab kiiresti aru saama, kus ta on
- kasutaja peab kohe nägema, mis vajab tähelepanu
- kasutaja peab nägema, milline on tema järgmine tegevus
- tähtis info peab eristuma ilma, et kogu ekraan karjuks

## Üldised muudatused
- [x] Lisada aktiivse nav-itemi visuaalne eristus
- [x] Ühtlustada kõigi vaadete headeri struktuur:
  - [x] pealkiri
  - [x] lühikirjeldus
  - [x] primaarne tegevus
  - [x] sekundaarsed tegevused
- [x] Ühtlustada badge’ide süsteem staatuste ja prioriteetide jaoks
- [x] Lisada tugevam edukate tegevuste visuaalne tagasiside
- [x] Parandada empty state sõnumeid ja paigutust
- [x] Ühtlustada spacing cardide, tabelite ja action plokkide vahel

---

# 2. Repair List – paranduste nimekiri ✅

## Eesmärk
Paranduste nimekiri peab olema “operatiivne juhtpaneel”, mitte lihtsalt tabel.

## Muudatused
- [x] Tugevdada list view headeri hierarhiat
  - [x] selge primaarne nupp `Lisa uus parandus`
  - [x] sekundaarsed tegevused `Ekspordi CSV`, `Lähtesta filtrid`
- [x] Lisada nähtav `Lähtesta filtrid` nupp
- [x] Tõsta filtriala visuaalselt eraldi tööriistaribaks
- [x] Parandada tabeli loetavust:
  - [x] tootekood visuaalselt peamiseks väljaks
  - [x] klient/tootegrupp sekundaarseks
  - [x] osakond ja parandaja kompaktsemaks
- [x] Lisada prioriteedi tugevam visuaalne esiletõst:
  - [x] kõrge prioriteet peab kohe silma jääma
- [x] Lisada staatuse visuaalne järjekindlus
- [x] Lisada rea/kaardi tasemel tähelepanusignaal töödele, mis on:
  - [x] kõrge prioriteediga
  - [x] kaua avatud
  - [x] määramata parandajaga
- [x] Kontrollida, et tabeli interaktsioonid oleksid loogilised ka mobiilsemal laiuse tasemel

## Võimalik lisaparandus
- [x] Lisada nimekirja ülaserva mini-summary:
  - [x] kokku töid
  - [x] kõrge prioriteediga
  - [x] määramata
  - [x] töös

---

# 3. Repair Detail – detailvaade ✅

## Eesmärk
Detailvaade peab olema ühe kirje “juhtimiskeskus”.

## Muudatused
- [x] Jagada detailvaade selgemalt kolmeks tsooniks:
  - [x] ülevaade
  - [x] tegevused
  - [x] ajalugu/kommentaarid
- [x] Tugevdada ülaosa kokkuvõtet:
  - [x] staatus
  - [x] prioriteet
  - [x] osakond
  - [x] parandaja
  - [x] viimati uuendatud
- [x] Teha tegevuste plokk visuaalselt selgemaks:
  - [x] primaarne tegevus eespool
  - [x] meistri tegevused eraldi loogilise grupina
  - [x] parandaja tegevused eraldi loogilise grupina
- [x] Lisada tegevuste juurde lühike kontekstitugi, kui vaja
- [x] Muuta kommentaaride ala rohkem timeline-tüüpi vaateks
- [x] Muuta auditlogi paremini loetavaks ja vähem “tooresteks kaartideks”
- [x] Lisada detailvaates selgem tagasiside pärast:
  - [x] staatuse muutmist
  - [x] prioriteedi muutmist
  - [x] parandaja määramist
  - [x] kommentaari lisamist
- [x] Kontrollida, et detailvaate actionid oleksid rolliti hästi arusaadavad, mitte lihtsalt “nähtavad”

## Võimalik lisaparandus
- [ ] Lisada “vajab tähelepanu” märge, kui töö on:
  - [x] kõrge prioriteediga
  - [ ] kaua muutmata
  - [x] parandajata

---

# 4. My Work – parandaja töölaud ✅

## Eesmärk
See vaade peab tunduma nagu parandaja tööjärjekord, mitte lihtsalt veel üks tabel.

## Muudatused
- [x] Lisada vaate ülaossa mini-summary:
  - [x] mitu tööd kokku
  - [x] mitu kõrge prioriteediga
  - [x] mitu aktiivset
  - [x] mitu ootel
- [x] Muuta read tegevuskesksemaks
- [x] Teha staatuse muutmine visuaalselt lihtsamini haaratavaks
- [x] Muuta kommentaari lisamine vähem robustseks:
  - [x] inline ala paremaks
  - [x] või modaal / expand lahendus
- [x] Lisada selgem töö tähtsuse eristus
- [x] Lisada nähtavam tee detailvaatesse peale ID lingi
- [x] Mõelda läbi, kas “Minu tööd” vajab kaardi- või split-layouti väiksematel ekraanidel

## Võimalik lisaparandus
- [x] Lisada “järgmine soovituslik samm” UX:
  - [x] kui töö on reviewed → rõhk `Alusta`
  - [x] kui töös → rõhk `Lõpeta` või `Pane ootele`

---

# 5. Dashboard – juhtimisvaade ✅

## Eesmärk
Dashboard peab aitama juhil/meistril kohe näha:
- mis seis on
- mis põleb
- kellel on koormus

## Muudatused
- [x] Tugevdada dashboardi kolmeks sisuliseks tsooniks:
  - [x] hetkeseis
  - [x] vajab tähelepanu
  - [x] koormus
- [x] Kujundada KPI plokid tugevama hierarhiaga
- [x] Tõsta “vanimad avatud tööd” visuaalselt tähtsamaks
- [x] Lisada eraldi plokk töödele, mis vajavad kiiret sekkumist:
  - [x] kõrge prioriteediga avatud tööd
  - [x] parandajata tööd
  - [x] kaua avatud tööd
- [x] Parandada “tööde arv parandajate kaupa” visuaalset esitlust
  - [x] lihtne tabel või bar chart
- [x] Kontrollida, et chartid ei oleks dekoratsioon, vaid aitaksid otsustada

## Võimalik lisaparandus
- [x] Lisada dashboardilt otseteed tegutsemiseks:
  - [x] `Vaata kõiki töid`
  - [ ] `Vaata parandajata töid`
  - [x] `Loo uus parandus`

---

# 6. Rollipõhine visuaalne juhtimine ✅

## Osakonna juht
- [x] rõhutada uue paranduse lisamist
- [x] rõhutada oma osakonna tööde nähtavust
- [x] hoida vaade vähem operatiivmüra täis

## Parandaja
- [x] rõhutada “Minu tööd” kui põhitöölauda
- [x] teha järgmine tegevus võimalikult lihtsaks
- [x] vähendada kõrvalisi juhtimisfunktsioone

## Meister
- [x] rõhutada dashboardi, määramist ja prioriseerimist
- [x] näidata ummikud ja koormus võimalikult kiirelt

## Admin
- [x] teha selgeks, et admini töövoog on süsteemihaldus, mitte ainult sama kasutajavaade rohkemate õigustega
- [x] lisada vajadusel nähtavam tee admin-paneeli

---

# 7. Mikro-UX parandused ✅

- [x] Lisada aktiivse lehe visuaalne indikaator navigatsioonis
- [x] Lisada selgemad success/error sõnumid async tegevustele
- [x] Lisada “Tühista” ja “Tagasi” nupud järjekindla loogikaga
- [x] Lisada vormides selgem veasõnumite kujundus
- [x] Kontrollida nuppude järjestust: primaarne enne, sekundaarsed pärast
- [x] Lisada detailvaates ja listis parem visuaalne kontrast oluliste badge’ide jaoks

---

# 8. Soovitatud teostusjärjekord

## Etapp 1 – Struktuur ja leitavus ✅
- [x] aktiivne nav
- [x] ühtne header hierarchy
- [x] primaarne/sekundaarne action loogika
- [x] quick actions ülevaatus

## Etapp 2 – List ja detail ✅
- [x] list view visuaalne prioriseerimine
- [x] detailvaate tsoonide ümberkujundus
- [x] kommentaaride / ajaloo parem esitlus

## Etapp 3 – My Work ja Dashboard ✅
- [x] my-work töölaudlikumaks
- [x] dashboardi tähelepanu-tsoonid
- [x] workload visualiseerimine

## Etapp 4 – Polishing ✅
- [x] mikro-UX
- [x] spacing
- [x] badge consistency
- [x] empty states
- [x] feedback states

---

# 9. Definition of Done

See UX/UI pakett on valmis siis, kui:
- kasutaja näeb igal ekraanil kiiresti, kus ta on
- kasutaja näeb kiiresti, mis on järgmine loogiline tegevus
- tähtsad tööd eristuvad visuaalselt
- rollipõhised töövood tunduvad sihipärased, mitte juhuslikud
- UI ei ole ainult funktsionaalne, vaid juhib kasutajat teadlikult


# 10. Audit update

Pärast uut täis-UI auditit on punktid 1–6 hinnatud sisuliselt tehtuks.
Punkt 7 on nüüd märgitud tehtuks: mikro-UX viimased järjekindluse ja tagasiside detailid viidi samuti lõpuni.
