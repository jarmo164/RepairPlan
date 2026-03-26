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

RepairPlan liigub edasi **REST API põhise arhitektuuriga**.

### Backend
- **Django**
- **Django REST Framework**
- **SQLite** arenduses
- **PostgreSQL** tootmises
- **Django auth + Groups + backend permission layer**

### Frontend
- eraldi frontend klient, mis tarbib REST API-t
- täpne frontend stack otsustatakse rakenduse ehitusfaasis, kuid arhitektuur arvestab eraldi kliendiga algusest peale

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
- paranduse loomist API kaudu
- paranduste nimekirja filtrite ja sorteerimisega
- detailvaadet / detailandmete endpointi
- parandaja “Minu tööd” endpointi
- dashboardi summary endpointi
- kommentaare
- auditlogi lihtversiooni

## Järgmine samm

Järgmine praktiline samm on scaffoldida Django + DRF projektistruktuur ja alustada andmemudelite ning API kihtidega.
