# RepairPlan Workflows

See dokument kirjeldab RepairPlan rakenduse peamised töövood praktilise protsessina.

Fookus on sellel:
- kuidas töö süsteemis liigub
- kes mida teeb
- millised otsused ja harud protsessis tekivad

---

# 1. Uue paranduse loomise workflow

## Eesmärk
Viia uus parandust vajav toode süsteemi nii, et see oleks kohe nähtav ja juhitav.

## Sammud
1. Osakonna juht avab `Uus parandus` vormi
2. Sisestab:
   - tootekoodi
   - koguse
   - kliendi / grupi
   - prioriteedi
   - kommentaari
3. Süsteem seob kirje automaatselt tema osakonnaga
4. Kirje salvestub
5. Kirje avaneb detailvaates
6. Auditlogisse tekib loomise sündmus

## Tulemus
- töö on süsteemis olemas
- meister saab selle üle vaadata ja edasi suunata

---

# 2. Meistri tööjaotuse workflow

## Eesmärk
Jagada töö õigetele parandajatele ja seada tööle õige prioriteet ja seis.

## Sammud
1. Meister avab paranduste nimekirja või dashboardi
2. Valib töö detailvaatesse
3. Muudab vajadusel:
   - parandajat
   - prioriteeti
   - staatust
   - lisab kommentaari
4. Vajutab `Salvesta muudatused`
5. Süsteem:
   - salvestab muudatused
   - logib auditisse
   - saadab vajadusel teavituse

## Tulemus
- töö on määratud
- seis on uuendatud
- parandaja näeb tööd oma töölauda ilmumas

---

# 3. Parandaja töövoog – määratud töö

## Eesmärk
Võimaldada parandajal hallata talle määratud töid kiiresti ja selgelt.

## Sammud
1. Parandaja logib sisse
2. Maandub `Minu tööd` vaatesse
3. Näeb ainult talle määratud töid
4. Saab iga töö juures:
   - muuta staatust
   - lisada kommentaari
   - avada detailvaate
5. Vajadusel avab detailvaate ja lisab rohkem infot

## Tulemus
- tööde tegelik seis kajastub süsteemis
- oluline info jõuab kommentaaridesse ja logisse

---

# 4. Tööde riiuli workflow (self-claim)

## Eesmärk
Lubada parandajal võtta endale määramata töö, kui meistri käsitsi määramine pole seda ette teinud.

## Sammud
1. Parandaja avab `Tööde riiul` vaate
2. Näeb määramata ja saadaval töid
3. Vajutab töö juures `Võta töö`
4. Süsteem:
   - määrab töö parandajale
   - eemaldab töö riiulist
   - lisab auditlogi kirje:
     - `assigned_to`
     - `assignment_source = SELF_CLAIMED`
5. Töö ilmub parandaja `Minu tööd` vaatesse

## Tulemus
- parandaja saab ise töö üles võtta
- süsteem säilitab kontrollitavuse
- meister näeb hiljem, et töö võeti ise

---

# 5. Meistri ülevaate workflow self-claimed töödest

## Eesmärk
Anda meistrile nähtavus töödest, mis parandajad ise riiulist võtsid.

## Sammud
1. Meister avab dashboardi
2. Näeb eraldi plokke:
   - `Ise võetud tööd`
   - `Nädalavahetusel ise võetud tööd`
3. Saab nende kaudu liikuda detailvaatesse
4. Vajadusel korrigeerib:
   - prioriteeti
   - parandajat
   - staatust

## Tulemus
- meistril on pilt ees isetekkinud tööjaotusest
- eriti kasulik esmaspäevase ülevaate jaoks

---

# 6. Detailvaate muudatuste workflow

## Eesmärk
Hoida töö juhtimine koondatuna ühte vaatesse ja ühe salvestuse alla.

## Sammud
1. Kasutaja avab detailvaate
2. Muudab vajadusel:
   - parandajat
   - prioriteeti
   - staatust
   - kommentaari
3. Vajutab `Salvesta muudatused`
4. Süsteem:
   - valideerib õigused
   - valideerib staatuse üleminekud
   - salvestab kõik muudatused
   - lisab kommentaari, kui see pole tühi
   - logib auditisse

## Tulemus
- detailvaade toimib ühe kirje juhtimiskeskusena
- kasutaja ei pea tegema mitut eraldi save actionit

---

# 7. Elektroonilise töö workflow

## Eesmärk
Eristada elektroonika rajaga tööd ja elektroonilisi parandajaid, et tööde jaotus oleks loogilisem.

## Loogika
- parandajal on `specialty`
- tööl on `repair_track`

## Mõju süsteemis
- elektroonilise rajaga töödel on visuaalne märge
- elektrooniliste parandajate juures on visuaalne ikoon
- tööde riiulit saab tulevikus selle järgi täpsemalt suunata
- dashboard ja nimekirjad näitavad seda infot otsuste tegemiseks

## Tulemus
- süsteem ei käsitle kõiki parandusi enam ühe homogeenilise massina

---

# 8. CSV ekspordi workflow

## Eesmärk
Võimaldada kasutajal viia nähtavad tööd süsteemist välja ilma õigusi rikkumata.

## Sammud
1. Kasutaja avab paranduste nimekirja
2. Seab vajadusel filtrid
3. Vajutab `Ekspordi CSV`
4. Süsteem ekspordib ainult need kirjed, mida kasutaja tohib näha
5. Ekspordi tulemus järgib aktiivseid filtreid

## Tulemus
- nähtavuse loogika jääb ka ekspordi puhul korrektseks

---

# 9. Admin workflow

## Eesmärk
Anda administraatorile süsteemi haldusvõimekus ilma, et ta peaks kasutajavaadet kuritarvitama.

## Sammud
1. Admin logib sisse
2. Saab liikuda admin-paneeli
3. Haldab seal:
   - kasutajaid
   - gruppe
   - osakondi
   - profiile
   - parandusi
4. Vajadusel kasutab ka dashboardi ja tava-UI-d seireks

## Tulemus
- süsteemihaldus ja tööoperatsioonid on mõlemad kaetud

---

# 10. Töövoogude kokkuvõte

RepairPlanis liigub töö üldiselt nii:

1. **Osakonna juht** loob töö
2. **Meister** vaatab üle ja määrab edasi
3. **Parandaja** teeb tööd ja uuendab seisu
4. Vajadusel **parandaja võtab töö ise riiulist**
5. **Meister** saab hiljem self-claim tegevustest ülevaate
6. **Admin** hoiab süsteemi korras

See tähendab, et süsteem toetab korraga kahte jaotuse loogikat:
- klassikaline meistri määramine
- kontrollitud self-claim riiulist

Mõlemad on auditeeritud ja nähtavad.
