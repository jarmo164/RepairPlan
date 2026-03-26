# RepairPlan

RepairPlan on veebipõhine parandustööde haldamise rakendus, mille eesmärk on asendada Exceli-põhine töövoog struktureeritud, rollipõhise süsteemiga.

## Repo eesmärk

See repo koondab projekti lähteülesande, arhitektuuriotsused ja teostusplaani enne rakenduse ehitamist.

## Dokumendid

- `PROMPT.md` — algne lähteülesanne
- `ARCHITECTURE.md` — arhitektuuri ülevaade ja tehnilised otsused
- `IMPLEMENTATION_PLAN.md` — detailsem teostusplaan
- `BACKLOG.md` — prioriseeritud tööde nimekiri järgmisteks sammudeks

## Soovitatud lahendus lühidalt

- **Backend:** Django
- **Frontend:** Django Templates + Bootstrap 5
- **Database:** SQLite arenduses, PostgreSQL tootmises
- **Auth:** Django built-in authentication
- **Authorization:** Django Groups + serveripoolne permission-kontroll
- **Core domain:** Department, UserProfile, Repair, RepairComment, RepairStatusLog

## MVP fookus

Esimene pärisversioon peaks sisaldama vähemalt:
- sisselogimist
- rollipõhiseid õigusi
- paranduse loomist
- filtritega paranduste nimekirja
- detailvaadet
- parandaja “Minu tööd” vaadet
- meistri dashboardi
- kommentaare
- auditlogi lihtversiooni

## Järgmine samm

Järgmine praktiline samm on scaffoldida Django projektistruktuur ja alustada andmemudelitega.
