# RepairPlan – parendusettepanekud

Allpool on praktilised ettepanekud pärast praeguse koodi ja struktuuri ülevaatust.

## 1. Kõrge väärtusega lähisammud

### 1.1 Tee staatuste haldus päriselt seadistatavaks
Praegu on staatused `TextChoices` kujul koodis.

Soovitus:
- vii staatused eraldi mudelisse, nt `RepairStatusDefinition`
- luba meistril / administraatoril neid UI-st hallata
- lisa väljad:
  - nimi
  - järjestus
  - värv / badge variant
  - kas aktiivne
  - kas loetakse lõpetatuks
  - kas peidetakse vaikimisi

Miks:
- praegu iga uue staatuse lisamine nõuab migratsiooni ja deploy’d
- ärireeglid muutuvad päriselus kiiresti

---

### 1.2 Tugevda audit trail’i
Praegu logitakse olulisemaid välju, aga audit võiks olla täielikum.

Soovitus:
- logi ka:
  - `department`
  - `repair_track`
  - `quantity`
  - `client_or_group`
- lisa muutuslogile inimesele loetavad väärtused
- detailvaates kuva “kes, mida, millal” selgemalt

Miks:
- teenindus- ja remondiprotsessides vaieldakse tihti “kes muutis?” teemal
- audit on üks selle süsteemi tegelikest väärtustest

---

### 1.3 Paranda meistri mass-tegevused
Praegu enamik tegevusi on üks-kirje-korraga.

Soovitus:
- bulk assign
- bulk status change
- bulk priority change
- bulk export valitud kirjetele

Miks:
- meistri töö läheb kiiresti tüütuks, kui kirjeid on kümneid või sadu
- just siin tuleb operatiivne ajavõit

---

## 2. UX / tooteparandused

### 2.1 Tee paranduste nimekiri tihedamaks ja töökindlamaks
Praegu on nimekiri kasutatav, aga suure mahu puhul võiks olla parem.

Soovitus:
- salvesta viimased filtrid URL-i ja localStorage’isse
- lisa kiire-filtrid:
  - minu osakond
  - määramata
  - kõrge prioriteet
  - elektrooniline
  - tagastatud
- lisa sorteerimine rohkemate väljade järgi

---

### 2.2 Lisa nähtavam visuaalne tähendus radadele ja specialty’dele
Praegu elektroonika on olemas, aga seda võiks kanda süsteemis järjekindlamalt.

Soovitus:
- ühtne ikooni- ja värvisüsteem:
  - elektrooniline töö
  - elektroonikaparandaja
  - high priority
  - returned
- kasuta samu badge’e kõigis vaadetes

---

### 2.3 Paranduse detailvaade võiks olla tegevuskeskus
Praegu detailvaade on juba tugev, aga seda saaks teha veel praktilisemaks.

Soovitus:
- sticky action panel desktopis
- kiire järgmise staatuse nupud
- “määramata → määra mulle” või “tagasi riiulisse” tegevused
- kommentaaride juures @mention valmisolek tulevikuks

---

## 3. Arhitektuursed parendused

### 3.1 Eemalda SVG duplikaadid template’itest
Praegu elektroonika ikoon on mitmes kohas inline SVG-na.

Soovitus:
- tee ikoonile üks keskne helper
- või hoia seda eraldi partial template’is / JS helperis / sprite’is

Miks:
- väiksem duplikaat
- lihtsam muuta ühes kohas

---

### 3.2 Vii osa view-loogikast rohkem selector/service kihti
`views.py` on juba arusaadav, aga kasvab kiiresti.

Soovitus:
- vii dashboard / operations manage konteksti koostamine selectoritesse
- hoia view’d õhemad
- standardiseeri nimekiri:
  - selectors = read
  - services = write
  - views = wiring

---

### 3.3 Lisa tüüpide ja enumite ühtlustus
Praegu on mudelites ja UI-s valikuid mitmes kohas.

Soovitus:
- hoia staatuste, radade ja specialty väärtuste kasutus kesksemana
- väldi magic stringe JS-is ja template’ites

---

## 4. Tootmiskõlblikkus

### 4.1 PostgreSQL-first tootmisseadistus
Praegu on PostgreSQL tugi olemas, aga vaikimisi arenduslähenemine domineerib.

Soovitus:
- lisa tootmisnäide `.env.example` faili detailsemalt
- lisa migration/deploy checklist
- dokumenteeri backup / restore protsess

---

### 4.2 Logimine ja veaotsing
Soovitus:
- lisa struktureeritud logging
- eraldi request/error logid
- productionis Sentry või analoog

Miks:
- hetkel veaotsing sõltub liiga palju käsitsi vaatamisest

---

### 4.3 Permissions audit
Soovitus:
- lisa testid kõigile rollide piirijuhtudele
- kontrolli, et department manager ei saaks tahtmatult üle oma piiri minna
- kontrolli operations manage õigusi eraldi testikomplektiga

---

## 5. Testide parandused

### 5.1 Kata uued vood testidega
Pärast viimaseid muudatusi tasub lisada testid järgmistele teemadele:
- `Tagastatud` kirjed on vaikimisi peidetud
- filtri kaudu saab `Tagastatud` siiski näha
- meistri haldusvaade töötab GET/POST jaoks
- osakonna loomine / muutmine / toggle
- specialty muutmise mõju shelf loogikale

---

### 5.2 Lisa UI smoke testid
Kui projekt kasvab, siis vähemalt mõned integraatsioonitestid oleks mõistlikud.

Soovitus:
- Django test client + HTML assertionid
- või hiljem Playwright kõige kriitilisematele voogudele

---

## 6. Minu soovitatud järjekord

Kui teha ainult 5 järgmist asja, siis ma teeks nii:

1. **Returned peitmise ja staatusevabaduse testide laiendamine**
2. **Meistri bulk actions**
3. **Staatused andmemudelisse, mitte koodi**
4. **Audit trail tugevamaks**
5. **Production logging + deploy checklist**

## Lühihinnang

RepairPlan ei näe välja nagu “algeline demo”, vaid nagu päris sisetööriista tugev vundament.

Praegune põhirisk ei ole see, et asi ei töötaks.
Põhirisk on pigem see, et:
- ärireeglid hakkavad koodi sees laiali valguma
- UI jääb suurema mahu jaoks liiga käsitööseks
- admin/meistri vood vajavad järgmise sammuna mass-tegevusi ja paremat seadistatavust

Ehk lühidalt:
- **vundament on hea**
- **järgmine väärtus tuleb skaleeritavast haldusest, auditist ja UX-ist**
