# RepairPlan

RepairPlan on veebipõhine parandustööde haldamise süsteem, mille eesmärk on asendada Exceli-põhine töövoog struktureeritud, rollipõhise lahendusega.

## Repo eesmärk

See repo koondab projekti lähteülesande, arhitektuuriotsused ja teostusplaani enne rakenduse ehitamist.

## Dokumendid

- `PROMPT.md` — algne lähteülesanne
- `ARCHITECTURE.md` — arhitektuuri ülevaade ja tehnilised otsused
- `IMPLEMENTATION_PLAN.md` — detailsem teostusplaan
- `BACKLOG.md` — prioriseeritud tööde nimekiri

## Valitud tehniline suund

RepairPlan liigub edasi **server-renderdatud Django veebirakendusena**, kus:
- HTML vaated tulevad Django templatemootorist
- kliendipoolne **vanilla JavaScript** lisab dünaamilise andmelaadimise
- andmed tulevad sisemistest REST-stiilis API endpointidest
- lahendus **ei ole SPA** ega vaja rasket frontend build chain’i

### Backend
- **Django**
- **Django REST Framework** või kergemad Django JSON endpointid API kihi jaoks
- **SQLite** arenduses
- **PostgreSQL** tootmises
- **Django auth + Groups + backend permission layer**

### Frontend
- **Django Templates**
- **Bootstrap**
- ikooniteek
- **vanilla JS**
- `fetch`-põhine ühine API-wrapper
- vajadusel **Chart.js** visualiseerimiseks

## Core domain

- `Department`
- `UserProfile`
- `Repair`
- `RepairComment`
- `RepairStatusLog`

## MVP fookus

Esimene pärisversioon peaks sisaldama vähemalt:
- autentimist
- rollipõhiseid õigusi backendis
- server-renderdatud põhivaateid
- paranduste nimekirja filtrite ja sorteerimisega
- detailvaadet
- parandaja “Minu tööd” vaadet
- dashboardi kokkuvõtet
- kommentaare
- auditlogi lihtversiooni
- API kihte dünaamilise andmelaadimise jaoks

## Järgmine samm

Järgmine praktiline samm on scaffoldida Django projektistruktuur ning panna paika:
- base template
- auth flow
- API-wrapperi muster
- andmemudelid
- rollipõhine navigeerimine
