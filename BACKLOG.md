# RepairPlan Backlog

See backlog on tuletatud failidest `PROMPT.md`, `ARCHITECTURE.md` ja `IMPLEMENTATION_PLAN.md`.

## Prioriteedid
- **P0** — kriitiline vundament, ilma milleta projekt ei liigu
- **P1** — MVP jaoks vajalik
- **P2** — oluline, aga võib tulla pärast esimest töötavat versiooni
- **P3** — nice-to-have / hilisem täiendus

---

## P0 — Projekti vundament

### 1. Django projekti skeleton
- [ ] Luua Django projekt ja `repairs` app
- [ ] Seadistada `settings.py` arendusrežiimi jaoks
- [ ] Lisada templates/static konfiguratsioon
- [ ] Seadistada login/logout flow
- [ ] Lisada Bootstrap 5 baaslayout

### 2. Andmemudelid
- [ ] Luua `Department` mudel
- [ ] Luua `UserProfile` mudel kasutaja-osakonna seose jaoks
- [ ] Luua `Repair` mudel
- [ ] Luua `RepairComment` mudel
- [ ] Luua `RepairStatusLog` mudel
- [ ] Defineerida status ja priority choices
- [ ] Lisada vajalikud indeksid
- [ ] Luua migratsioonid

### 3. Admin ja süsteemi algseadistus
- [ ] Registreerida mudelid Django adminis
- [ ] Seadistada admin list/filter/search vaated
- [ ] Luua grupid: `department_manager`, `repair_master`, `repairer`, `administrator`
- [ ] Valmistada ette superuser / initial seed loogika

---

## P1 — MVP põhifunktsionaalsus

### 4. Permission layer
- [ ] Luua `permissions.py`
- [ ] Luua rollihelperid
- [ ] Piirata querysetid rolli ja osakonna järgi
- [ ] Kontrollida serveripoolel create/update/detail õigusi

### 5. Paranduste nimekiri
- [ ] Luua üldnimekirja vaade
- [ ] Lisada otsing tootekoodi järgi
- [ ] Lisada filtrid: osakond, klient/tootegrupp, staatus, prioriteet, parandaja
- [ ] Lisada sort kuupäeva järgi
- [ ] Lisada pagination
- [ ] Lisada staatuse/prioriteedi badge’id

### 6. Uue paranduse lisamine
- [ ] Luua repair create vorm
- [ ] Automaatne `created_by`
- [ ] Automaatne `created_at`
- [ ] Piirata osakonna juhi sisestusloogika vastavalt õigustele

### 7. Detail- ja muutmisvaated
- [ ] Luua repair detailvaade
- [ ] Näidata põhiandmeid, kommentaare ja ajalugu
- [ ] Luua repair update vaade
- [ ] Rakendada rollipõhine väljade muutmise loogika

### 8. Parandaja “Minu tööd” vaade
- [ ] Näidata ainult kasutajale määratud töid
- [ ] Võimaldada kiiret staatuse uuendamist lubatud sammudes
- [ ] Võimaldada kommentaari lisamist

### 9. Dashboard
- [ ] Näidata tööde arvu staatuste kaupa
- [ ] Näidata kõrge prioriteediga tööde arvu
- [ ] Näidata vanimaid avatud töid
- [ ] Näidata tööde arvu parandajate kaupa

---

## P2 — Tootmisküpsemus

### 10. Audit ja workflow kontroll
- [ ] Rakendada staatuse üleminekute valideerimine service layeris
- [ ] Logida staatuse muutused `RepairStatusLog` tabelisse
- [ ] Logida prioriteedi muutused
- [ ] Logida määramise muudatused

### 11. Kommentaarisüsteem
- [ ] Lisada eraldi kommentaaride timeline detailvaatesse
- [ ] Näidata autor ja aeg
- [ ] Võimaldada kommentaaride loomine õiguste piires

### 12. Export
- [ ] Lisada CSV export üldnimekirja filtrite pealt
- [ ] Hoida Excel export hilisemaks vajadusel

### 13. UX polish
- [ ] Parandada tabeli loetavust suure andmemahu korral
- [ ] Ühtlustada vormide paigutus ja veateated
- [ ] Lisada tühjade vaadete UX
- [ ] Parandada navigeerimine rollipõhiselt

---

## P3 — Hilisemad laiendused

### 14. Teavitused
- [ ] Valmistada ette email notification hook’id
- [ ] Võimalik hilisem assignment/status notification flow

### 15. Tehnilised laiendused
- [ ] PostgreSQL tootmiskonfiguratsioon
- [ ] Background jobs (Celery või RQ)
- [ ] Võimalik REST API integratsioonide jaoks

### 16. Täiendavad raportid
- [ ] Ajalised raportid
- [ ] Osakondade lõikes kokkuvõtted
- [ ] Parandajate jõudluse vaated, kui äriliselt vajalik

---

## Soovitatud tööjärjekord

1. Django skeleton
2. mudelid + admin + migratsioonid
3. rollid + permission layer
4. list/create/detail/update vaated
5. minu tööd
6. dashboard
7. auditlog + kommentaarid
8. CSV export
9. testid ja polish

---

## Definition of Done (MVP)

MVP võib lugeda valmis siis, kui:
- kasutaja saab sisse logida
- osakonna juht saab lisada paranduse
- meister saab määrata prioriteedi, staatuse ja parandaja
- parandaja näeb ainult oma töid ja saab neid uuendada
- nimekiri toetab otsingut ja filtreid
- dashboard annab kiire juhtimisülevaate
- kommentaarid ja auditlogi on olemas
- õigused on serveripoolel päriselt jõustatud
