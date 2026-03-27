# RepairPlan User Stories

See dokument kirjeldab RepairPlan rakenduse peamised kasutajalood rollide kaupa.

Eesmärk:
- teha süsteemi kasutusjuhtumid selgeks
- aidata hinnata, kas rakendus katab päris töö vajadused
- anda alus järgmistele parandustele ja laiendustele

---

# 1. Osakonna juht

## US-1 — Uue paranduse lisamine
**Kasutajana** tahan lisada süsteemi parandust vajava toote,  
**et** töö jõuaks nähtavale ja paranduse meister saaks sellega edasi tegeleda.

### Vastuvõtukriteeriumid
- osakonna juht saab avada uue paranduse vormi
- vormis saab sisestada vähemalt:
  - tootekoodi
  - koguse
  - kliendi / grupi
  - prioriteedi
  - kommentaari
- töö seotakse juhi enda osakonnaga
- pärast salvestamist on kirje süsteemis olemas ja nähtav

---

## US-2 — Oma osakonna tööde nägemine
**Kasutajana** tahan näha ainult oma osakonna parandusi,  
**et** ma saaksin jälgida oma vastutusala ilma liigse mürata.

### Vastuvõtukriteeriumid
- osakonna juht ei näe teiste osakondade kirjeid
- nimekirjas saab otsida ja filtreerida
- detailvaates näeb ta ainult oma osakonna töid

---

## US-3 — Prioriteedi määramine või muutmine
**Kasutajana** tahan vajadusel määrata või muuta paranduse prioriteeti,  
**et** kiireloomulised tööd oleksid süsteemis õigesti tähistatud.

### Vastuvõtukriteeriumid
- osakonna juht saab create/update voos valida prioriteedi
- prioriteedi muutus salvestub süsteemi
- muutus on detailvaates nähtav

---

# 2. Paranduse meister

## US-4 — Kõigi tööde ülevaade
**Kasutajana** tahan näha kõiki parandusi ühes süsteemis,  
**et** ma saaksin juhtida tööde jaotust, koormust ja prioriteete.

### Vastuvõtukriteeriumid
- meister näeb kõiki kirjeid
- nimekirjas saab filtreerida ja otsida
- dashboard annab juhtimisülevaate

---

## US-5 — Töö määramine parandajale
**Kasutajana** tahan määrata töö konkreetsele parandajale,  
**et** vastutus oleks selge ja töö liiguks edasi.

### Vastuvõtukriteeriumid
- meister saab detailvaates valida parandaja
- määramine salvestub
- auditlogis on muudatus näha
- parandaja näeb tööd oma töölauda ilmumas

---

## US-6 — Staatuse ja prioriteedi haldamine
**Kasutajana** tahan muuta töö staatust ja prioriteeti,  
**et** süsteem peegeldaks päris tööseisu.

### Vastuvõtukriteeriumid
- meister saab muuta staatust
- meister saab muuta prioriteeti
- kõik muudatused logitakse

---

## US-7 — Ülevaade ise võetud töödest
**Kasutajana** tahan näha, millised tööd parandajad ise riiulist võtsid,  
**et** mul oleks koormusest ja isetekkinud jaotusest ülevaade.

### Vastuvõtukriteeriumid
- dashboardis on plokk ise võetud tööde jaoks
- nädalavahetusel ise võetud tööd on eraldi nähtavad
- detaili saab sealt edasi avada

---

# 3. Parandaja

## US-8 — Oma tööde töölaud
**Kasutajana** tahan näha ainult mulle määratud töid,  
**et** ma teaksin, mille kallal pean töötama.

### Vastuvõtukriteeriumid
- parandaja maandub oma töölauda
- ta näeb ainult talle määratud töid
- tööde juures on tähtsad väljad kohe nähtavad

---

## US-9 — Töö staatuse uuendamine
**Kasutajana** tahan muuta oma töö staatust,  
**et** süsteem näitaks, kas töö on töös, ootel või lõpetatud.

### Vastuvõtukriteeriumid
- parandaja saab staatust muuta ainult lubatud sammudes
- muudatus salvestub
- auditlogi täieneb

---

## US-10 — Kommentaari lisamine
**Kasutajana** tahan lisada tööle kommentaari,  
**et** oluline tööinfo ei jääks suuliseks või kaduma.

### Vastuvõtukriteeriumid
- parandaja saab lisada kommentaari detailvaates
- parandaja saab lisada kommentaari my-work vaatest
- kommentaar on detailvaates nähtav koos autori ja ajaga

---

## US-11 — Töö võtmine riiulist
**Kasutajana** tahan võtta endale määramata töö riiulist,  
**et** ma saaksin tööaega ise sisustada ja vaba tööd üles korjata.

### Vastuvõtukriteeriumid
- parandaja näeb tööde riiulit
- ta saab võtta töö endale
- pärast võtmist kaob töö riiulist ja ilmub tema töölauda
- süsteem logib, et töö võeti self-claim kaudu

---

# 4. Administraator

## US-12 — Süsteemi haldus
**Kasutajana** tahan pääseda admin-paneeli ja hallata süsteemi andmeid,  
**et** ma saaksin kasutajaid, osakondi ja süsteemi seadeid korras hoida.

### Vastuvõtukriteeriumid
- administraator näeb navis teed admin-paneeli
- admin-paneelist saab hallata:
  - kasutajaid
  - gruppe
  - osakondi
  - parandusi
  - profiile

---

# 5. Süsteem kui tervik

## US-13 — Auditlogi olemasolu
**Kasutajana** tahan, et olulised muudatused jääksid süsteemi logisse,  
**et** hiljem oleks võimalik aru saada, kes mida muutis.

### Vastuvõtukriteeriumid
- logitakse vähemalt:
  - töö loomine
  - parandaja määramine
  - prioriteedi muutmine
  - staatuse muutmine
  - self-claim allikas

---

## US-14 — Elektroonilise töö eristus
**Kasutajana** tahan näha, millised tööd on elektroonika rajal ja millised parandajad on elektroonilised parandajad,  
**et** tööde jaotus oleks selgem.

### Vastuvõtukriteeriumid
- elektroonilise rajaga töödel on eristus
- elektrooniliste parandajate juures on visuaalne märge
- list/detail/dashboard/my-work vaated peegeldavad seda infot

---

## US-15 — Andmete eksport
**Kasutajana** tahan eksportida tööde nimekirja CSV-sse,  
**et** vajadusel andmeid jagada või töödelda väljaspool rakendust.

### Vastuvõtukriteeriumid
- eksport austab samu nähtavusreegleid nagu nimekiri
- eksport arvestab aktiivseid filtreid

---

# 6. Edasised võimalikud kasutajalood

Need ei pea olema praegu valmis, aga sobivad järgmisteks iteratsioonideks:

- automaatne esmaspäevane meistri kokkuvõte nädalavahetusel ise võetud töödest
- tööde riiuli filtreerimine specialty / repair_track järgi detailsemalt
- lisaraportid osakondade või parandajate lõikes
- `client_or_group` normaliseerimine eraldi andmeobjektiks
