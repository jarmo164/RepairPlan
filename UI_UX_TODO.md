# RepairPlan UI/UX To-Do

See dokument kirjeldab järgmist UX/UI paranduste paketti eesmärgiga muuta RepairPlan visuaalselt juhtivamaks, loogilisemaks ja rolliteadlikumaks.

Fookus ei ole “ilusam admin”, vaid:
- tähtsa info parem esiletõstmine
- järgmise tegevuse selgem nähtavus
- rollipõhine töövoog ilma liigse mõtlemiseta
- parem leitavus ja visuaalne hierarhia

---

# 1. Üldised UI põhimõtted

## Eesmärgid
- kasutaja peab kiiresti aru saama, kus ta on
- kasutaja peab kohe nägema, mis vajab tähelepanu
- kasutaja peab nägema, milline on tema järgmine tegevus
- tähtis info peab eristuma ilma, et kogu ekraan karjuks

## Üldised muudatused
- [ ] Lisada aktiivse nav-itemi visuaalne eristus
- [ ] Ühtlustada kõigi vaadete headeri struktuur:
  - [ ] pealkiri
  - [ ] lühikirjeldus
  - [ ] primaarne tegevus
  - [ ] sekundaarsed tegevused
- [ ] Ühtlustada badge’ide süsteem staatuste ja prioriteetide jaoks
- [ ] Lisada tugevam edukate tegevuste visuaalne tagasiside
- [ ] Parandada empty state sõnumeid ja paigutust
- [ ] Ühtlustada spacing cardide, tabelite ja action plokkide vahel

---

# 2. Repair List – paranduste nimekiri

## Eesmärk
Paranduste nimekiri peab olema “operatiivne juhtpaneel”, mitte lihtsalt tabel.

## Muudatused
- [ ] Tugevdada list view headeri hierarhiat
  - [ ] selge primaarne nupp `Lisa uus parandus`
  - [ ] sekundaarsed tegevused `Ekspordi CSV`, `Lähtesta filtrid`
- [ ] Lisada nähtav `Lähtesta filtrid` nupp
- [ ] Tõsta filtriala visuaalselt eraldi tööriistaribaks
- [ ] Parandada tabeli loetavust:
  - [ ] tootekood visuaalselt peamiseks väljaks
  - [ ] klient/tootegrupp sekundaarseks
  - [ ] osakond ja parandaja kompaktsemaks
- [ ] Lisada prioriteedi tugevam visuaalne esiletõst:
  - [ ] kõrge prioriteet peab kohe silma jääma
- [ ] Lisada staatuse visuaalne järjekindlus
- [ ] Lisada rea/kaardi tasemel tähelepanusignaal töödele, mis on:
  - [ ] kõrge prioriteediga
  - [ ] kaua avatud
  - [ ] määramata parandajaga
- [ ] Kontrollida, et tabeli interaktsioonid oleksid loogilised ka mobiilsemal laiuse tasemel

## Võimalik lisaparandus
- [ ] Lisada nimekirja ülaserva mini-summary:
  - [ ] kokku töid
  - [ ] kõrge prioriteediga
  - [ ] määramata
  - [ ] töös

---

# 3. Repair Detail – detailvaade

## Eesmärk
Detailvaade peab olema ühe kirje “juhtimiskeskus”.

## Muudatused
- [ ] Jagada detailvaade selgemalt kolmeks tsooniks:
  - [ ] ülevaade
  - [ ] tegevused
  - [ ] ajalugu/kommentaarid
- [ ] Tugevdada ülaosa kokkuvõtet:
  - [ ] staatus
  - [ ] prioriteet
  - [ ] osakond
  - [ ] parandaja
  - [ ] viimati uuendatud
- [ ] Teha tegevuste plokk visuaalselt selgemaks:
  - [ ] primaarne tegevus eespool
  - [ ] meistri tegevused eraldi loogilise grupina
  - [ ] parandaja tegevused eraldi loogilise grupina
- [ ] Lisada tegevuste juurde lühike kontekstitugi, kui vaja
- [ ] Muuta kommentaaride ala rohkem timeline-tüüpi vaateks
- [ ] Muuta auditlogi paremini loetavaks ja vähem “tooresteks kaartideks”
- [ ] Lisada detailvaates selgem tagasiside pärast:
  - [ ] staatuse muutmist
  - [ ] prioriteedi muutmist
  - [ ] parandaja määramist
  - [ ] kommentaari lisamist
- [ ] Kontrollida, et detailvaate actionid oleksid rolliti hästi arusaadavad, mitte lihtsalt “nähtavad”

## Võimalik lisaparandus
- [ ] Lisada “vajab tähelepanu” märge, kui töö on:
  - [ ] kõrge prioriteediga
  - [ ] kaua muutmata
  - [ ] parandajata

---

# 4. My Work – parandaja töölaud

## Eesmärk
See vaade peab tunduma nagu parandaja tööjärjekord, mitte lihtsalt veel üks tabel.

## Muudatused
- [ ] Lisada vaate ülaossa mini-summary:
  - [ ] mitu tööd kokku
  - [ ] mitu kõrge prioriteediga
  - [ ] mitu aktiivset
  - [ ] mitu ootel
- [ ] Muuta read tegevuskesksemaks
- [ ] Teha staatuse muutmine visuaalselt lihtsamini haaratavaks
- [ ] Muuta kommentaari lisamine vähem robustseks:
  - [ ] inline ala paremaks
  - [ ] või modaal / expand lahendus
- [ ] Lisada selgem töö tähtsuse eristus
- [ ] Lisada nähtavam tee detailvaatesse peale ID lingi
- [ ] Mõelda läbi, kas “Minu tööd” vajab kaardi- või split-layouti väiksematel ekraanidel

## Võimalik lisaparandus
- [ ] Lisada “järgmine soovituslik samm” UX:
  - [ ] kui töö on reviewed → rõhk `Alusta`
  - [ ] kui töös → rõhk `Lõpeta` või `Pane ootele`

---

# 5. Dashboard – juhtimisvaade

## Eesmärk
Dashboard peab aitama juhil/meistril kohe näha:
- mis seis on
- mis põleb
- kellel on koormus

## Muudatused
- [ ] Tugevdada dashboardi kolmeks sisuliseks tsooniks:
  - [ ] hetkeseis
  - [ ] vajab tähelepanu
  - [ ] koormus
- [ ] Kujundada KPI plokid tugevama hierarhiaga
- [ ] Tõsta “vanimad avatud tööd” visuaalselt tähtsamaks
- [ ] Lisada eraldi plokk töödele, mis vajavad kiiret sekkumist:
  - [ ] kõrge prioriteediga avatud tööd
  - [ ] parandajata tööd
  - [ ] kaua avatud tööd
- [ ] Parandada “tööde arv parandajate kaupa” visuaalset esitlust
  - [ ] lihtne tabel või bar chart
- [ ] Kontrollida, et chartid ei oleks dekoratsioon, vaid aitaksid otsustada

## Võimalik lisaparandus
- [ ] Lisada dashboardilt otseteed tegutsemiseks:
  - [ ] `Vaata kõiki töid`
  - [ ] `Vaata parandajata töid`
  - [ ] `Loo uus parandus`

---

# 6. Rollipõhine visuaalne juhtimine

## Osakonna juht
- [ ] rõhutada uue paranduse lisamist
- [ ] rõhutada oma osakonna tööde nähtavust
- [ ] hoida vaade vähem operatiivmüra täis

## Parandaja
- [ ] rõhutada “Minu tööd” kui põhitöölauda
- [ ] teha järgmine tegevus võimalikult lihtsaks
- [ ] vähendada kõrvalisi juhtimisfunktsioone

## Meister
- [ ] rõhutada dashboardi, määramist ja prioriseerimist
- [ ] näidata ummikud ja koormus võimalikult kiirelt

## Admin
- [ ] teha selgeks, et admini töövoog on süsteemihaldus, mitte ainult sama kasutajavaade rohkemate õigustega
- [ ] lisada vajadusel nähtavam tee admin-paneeli

---

# 7. Mikro-UX parandused

- [ ] Lisada aktiivse lehe visuaalne indikaator navigatsioonis
- [ ] Lisada selgemad success/error sõnumid async tegevustele
- [ ] Lisada “Tühista” ja “Tagasi” nupud järjekindla loogikaga
- [ ] Lisada vormides selgem veasõnumite kujundus
- [ ] Kontrollida nuppude järjestust: primaarne enne, sekundaarsed pärast
- [ ] Lisada detailvaates ja listis parem visuaalne kontrast oluliste badge’ide jaoks

---

# 8. Soovitatud teostusjärjekord

## Etapp 1 – Struktuur ja leitavus
- [ ] aktiivne nav
- [ ] ühtne header hierarchy
- [ ] primaarne/sekundaarne action loogika
- [ ] quick actions ülevaatus

## Etapp 2 – List ja detail
- [ ] list view visuaalne prioriseerimine
- [ ] detailvaate tsoonide ümberkujundus
- [ ] kommentaaride / ajaloo parem esitlus

## Etapp 3 – My Work ja Dashboard
- [ ] my-work töölaudlikumaks
- [ ] dashboardi tähelepanu-tsoonid
- [ ] workload visualiseerimine

## Etapp 4 – Polishing
- [ ] mikro-UX
- [ ] spacing
- [ ] badge consistency
- [ ] empty states
- [ ] feedback states

---

# 9. Definition of Done

See UX/UI pakett on valmis siis, kui:
- kasutaja näeb igal ekraanil kiiresti, kus ta on
- kasutaja näeb kiiresti, mis on järgmine loogiline tegevus
- tähtsad tööd eristuvad visuaalselt
- rollipõhised töövood tunduvad sihipärased, mitte juhuslikud
- UI ei ole ainult funktsionaalne, vaid juhib kasutajat teadlikult
