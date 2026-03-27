# RepairPlan Next Updates Plan

See plaan kirjeldab järgmise suurema muudatuste bloki, mis keskendub:
- elektrooniliste parandajate eristamisele
- tööde riiuli / self-claim töövoole
- my-work vaate lihtsustamisele
- detailvaate action flow koondamisele üheks salvestuseks

Eesmärk on enne implementatsiooni lukustada ära õige domeenimudel ja UX loogika, et mitte ehitada valesid asju valesse kohta.

---

# 1. Probleemid, mida see plokk lahendab

## 1.1 Elektroonilised parandajad ei eristu süsteemis
Praegu on parandajad kõik ühesugused kasutajad. Süsteem ei tea:
- kas tegu on üldise parandajaga
- või elektroonilise parandajaga

Selle tõttu ei saa:
- neid visuaalselt eristada
- tööde jaotust õigesti juhtida
- tööde riiulit tulevikus eriala järgi suunata

---

## 1.2 Meister ei pruugi nädalavahetusel töötavatele parandajatele piisavalt töid ette määrata
Kui osa parandajaid töötab ainult teatud päevadel, siis ainult meistri käsitsi määramise loogika jätab süsteemi liiga jäigaks.

Vaja on mehhanismi, kus parandaja saab:
- võtta töö riiulist ise
- ilma et süsteem kontrolli kaotaks

Ja meister peab saama hiljem näha:
- millised tööd võeti ise
- kes võttis
- millal võttis

---

## 1.3 My Work vaates on üks osa UX-ist üleliigne
Praegune “järgmine tegevus” veerg on pigem abitekst kui päris töövahend.

Soovitud suund:
- eemaldada see veerg
- teha kommentaari lisamine otsemaks
- hoida töölaud lihtsam ja kiirem

---

## 1.4 Detailvaates on liiga palju eraldi salvestusnuppe
Praegu on detailis eraldi action nupud erinevatele väljadele.

Soovitud suund:
- üks koondatud “Salvesta”
- kui midagi muudetakse, siis salvestatakse kõik korraga
- kommentaar lisatakse kaasa ainult siis, kui see on täidetud

---

# 2. Soovitatud domeenimudeli muudatused

## 2.1 Parandaja eriala / specialty

### Soovitus
Lisa `UserProfile` mudelile uus väli:
- `specialty`

Näidisväärtused:
- `GENERAL`
- `ELECTRONICS`

### Miks nii
See on parem kui lihtsalt `is_electronics_repairer: bool`, sest jätab ruumi tulevikuks.

Hiljem saab lisada näiteks:
- `MECHANICAL`
- `TESTING`
- `QUALITY`

---

## 2.2 Töö tüüp / suund

### Tähtis otsus
Praegu tundub, et “Elektrooniline” on pigem:
- töö tüüp
- või routing kategooria

mitte puhas workflow staatus.

### Soovitus
Lisa `Repair` mudelile uus väli:
- `repair_track`

Näidisväärtused:
- `GENERAL`
- `ELECTRONICS`

### Miks mitte staatus
Kui panna “Elektrooniline” staatuseks, siis tekib segadus:
- kas see on workflow samm?
- kas see on töö tüüp?
- kas sellest liigutakse edasi “Töösse”?

Puhas lahendus on hoida:
- **staatus** = workflow
- **repair_track** = töö tüüp / rada

---

## 2.3 Self-claim allikas
Kui parandaja võtab töö ise riiulist, siis peab see olema jälgitav.

### Soovitus
Lisa auditlogi / muudatuste semantiline eristus:
- `assignment_source`
  - `MASTER_ASSIGNED`
  - `SELF_CLAIMED`

Seda saab teha kas:
1. eraldi väljana Repair mudelis
2. logikirjena `RepairStatusLog` alla

### Minu soovitus
Alguses piisab logikirjest, et mitte paisutada mudelit liiga vara.

---

# 3. UI / UX muudatused

## 3.1 Elektrooniliste parandajate visuaalne eristus

### Soovitud tulemus
Kui parandaja on `ELECTRONICS`, siis:
- tema nime juures kuvatakse tehniline ikoon
- tema tööde read eristuvad kergelt teisest toonist

### Rakenduskoht
- paranduste nimekiri
- my work
- dashboard workload
- detailvaade

### Märkus
Kui valmis oscilloscope ikoon puudub, siis kasutada:
- inline SVG
- või tehnilist waveform/circuit stiili ikooni

---

## 3.2 My Work lihtsustus

### Muudatused
- eemaldada veerg `Järgmine tegevus`
- jätta alles:
  - töö
  - kogus
  - staatus
  - staatuse muutmine
  - kommentaar
  - detail
- kommentaar olgu kohe nähtav tekstiväli + salvesta nupp
- kommentaar ei ole kohustuslik

### Eesmärk
See peab tunduma nagu kiire töölaud, mitte õpetlik tabel.

---

## 3.3 Detailvaate ühe salvestuse mudel

### Muudatused
Praeguse mitme eraldi actioni asemel:
- `assigned_to`
- `priority`
- `status`
- `optional comment`

koondada ühe action-ploki alla.

### Soovitud UX
Kasutaja muudab välju ja vajutab:
- `Salvesta muudatused`

Kui kommentaariväli on tühi:
- kommentaari ei lisata

Kui kommentaar on täidetud:
- kommentaar luuakse sama salvestuse käigus

### Tehniline märkus
See vajab:
- koondatud update endpointi või olemasoleva PATCH flow laiendamist
- serveris järjekindlat loogikat, mis oskab salvestada muutused + kommentaari ühes käsus

---

## 3.4 Tööde riiul / self-claim vaade

### Uus vaade
Lisada eraldi vaade:
- `Tööde riiul`

### Nähtavad tööd
Riiulis kuvatakse tööd, mis on:
- määramata (`assigned_to is null`)
- aktiivsed / lõpetamata
- vajadusel filtreeritud `repair_track` järgi

### Tegevus
Parandaja saab vajutada:
- `Võta töö`

See teeb:
- määrab töö endale
- logib sündmuse auditisse
- märgib, et see tuli self-claim kaudu

---

## 3.5 Meistri ülevaade self-claimed töödest

### Soovitus
Dashboardi või eraldi plokki lisada:
- hiljuti ise võetud tööd
- nädalavahetusel ise võetud tööd

See annab meistrile esmaspäeval ülevaate, mis toimus ilma käsitsi määramiseta.

### Minu soovitus
Alustada dashboardi plokist, mitte kohe scheduleri või e-maili summaryga.

---

# 4. Teostusjärjekord

## Etapp 1 — domeenimudel
- [ ] lisa `UserProfile.specialty`
- [ ] lisa `Repair.repair_track`
- [ ] lisa migratsioonid
- [ ] lisa admin konfiguratsioon neile väljadele

## Etapp 2 — parandajate ja tööde visuaalne eristus
- [ ] ikoonid parandajate juurde
- [ ] toonieristus elektroonika rajaga töödele
- [ ] detailvaate ja dashboardi badge’id / tähised

## Etapp 3 — my-work lihtsustus
- [ ] eemalda `Järgmine tegevus`
- [ ] lisa kommentaari inline input + salvesta
- [ ] hoia kommentaar valikulisena

## Etapp 4 — detailvaate ühe salvestuse loogika
- [ ] koonda actionid ühte salvestusse
- [ ] salvesta staatuse/prioriteedi/määramise muudatused korraga
- [ ] lisa kommentaar samas flow’s, kui väli pole tühi

## Etapp 5 — tööde riiul
- [ ] lisa shelf view
- [ ] lisa self-claim action
- [ ] logi self-claim auditisse

## Etapp 6 — meistri ülevaade
- [ ] lisa self-claimed tööde plokk dashboardi
- [ ] võimalusel näita ka nädalavahetuse tegevust

---

# 5. Riskid ja tähelepanekud

## 5.1 “Elektrooniline” kui staatus võib osutuda valeks abstraheerimiseks
Kui see tegelikult tähendab töö tüüpi, siis staatuseks panemine teeb mudeli poriseks.

### Soovitus
Lukustada enne implementatsiooni ära:
- kas “elektrooniline” tähendab töö tüüpi
- või päris workflow staadiumi

Minu soovitus: **töö tüüp, mitte staatus**.

---

## 5.2 Self-claim ei tohi rikkuda kontrollitavust
Kui parandajad saavad ise töid võtta, siis peab meister ikka nägema:
- kes võttis
- mida võttis
- millal võttis

See peab jääma auditeeritavaks.

---

## 5.3 Ühe salvestuse detailvaade vajab backendi ümbermõtlemist
See ei ole ainult template muutus. See muudab:
- JS loogikat
- endpointide semantikat
- backend save flow’d

See on mõistlik muudatus, aga mitte ainult kosmeetika.

---

# 6. Minu soovituslik järgmine samm

Kõige õigem järgmine plokk on:
1. lukustada ära otsus, et **elektrooniline = repair_track, mitte staatus**
2. teha domeenimudeli muudatused
3. teha my-work lihtsustus
4. teha detailvaate ühe salvestuse mudel
5. alles siis self-claim shelf

See hoiab muudatused loogilises järjekorras ja väldib seda, et UI jookseks mudelist ette.
