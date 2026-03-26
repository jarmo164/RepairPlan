# RepairPlan

See repo sisaldab RepairPlan rakenduse lähteülesannet ja implementatsiooniplaani.

## Dokumendid

- `README.md` – algne ülesanne / prompt
- `IMPLEMENTATION_PLAN.md` – soovitatud arhitektuur ja etapiviisiline teostusplaan

## Algne prompt

Loo veebipõhine paranduste haldamise rakendus Django raamistikus.

Rakenduse eesmärk on hallata parandust vajavaid tooteid ühes keskse süsteemina. Lahendus peab asendama praeguse Exceli põhise käsitsi hallatava tabeli ning muutma paranduste lisamise, jälgimise, tööde jaotamise ja staatuste haldamise lihtsaks ning läbipaistvaks.

Rakendust hakkavad kasutama osakondade juhid, paranduse meister ja parandajad.

Töövoog:
1. Osakonna juht lisab süsteemi parandust vajava toote.
2. Paranduse meister vaatab kirjed üle.
3. Paranduse meister määrab prioriteedi, staatuse ja vajadusel parandaja.
4. Parandajad näevad neile määratud töid ja uuendavad töö staatust.
5. Süsteemist peab olema võimalik saada kiire ülevaade kõikidest aktiivsetest, ootel ja lõpetatud töödest.

Rakenduse põhiandmed iga paranduse kirje kohta:
- ID
- toote kood
- kogus
- klient või tootegrupp
- osakond, kust toode parandusse tuli
- parandusse kandmise kuupäev
- prioriteet
- staatus
- parandaja
- kommentaar

Rakenduse nõuded:

1. Tehnoloogia
- backend peab olema tehtud Django raamistikus
- andmebaasiks sobib PostgreSQL või SQLite arenduse jaoks
- frontend võib olla tehtud Django template’ide abil
- kujundus peab olema lihtne, töökindel ja sobima igapäevaseks kasutamiseks tootmiskeskkonnas

2. Kasutajarollid
Loo vähemalt järgmised rollid:
- Osakonna juht
- Paranduse meister
- Parandaja
- Administraator

3. Rollide õigused
- Osakonna juht saab lisada uusi paranduse kirjeid ja vaadata enda osakonna kirjeid
- Paranduse meister saab vaadata kõiki kirjeid, muuta staatust, määrata prioriteeti, lisada parandaja ja hallata kommentaare
- Parandaja saab näha ainult talle määratud töid ning muuta nende staatust ja lisada kommentaare
- Administraator saab hallata kasutajaid, rolle ja kogu süsteemi

4. Paranduse kirje väljad
Loo mudel paranduste jaoks järgmiste väljadega:
- id
- product_code
- quantity
- client_or_group
- department
- created_at
- priority
- status
- assigned_to
- comment

5. Staatuse valikud
Staatus peab olema valitav etteantud väärtuste seast:
- Alustamata
- Üle vaadatud
- Töös
- Ootel
- Lõpetatud
- Tagastatud

6. Prioriteedi valikud
Prioriteet peab olema valitav etteantud väärtuste seast:
- Kõrge
- Keskmine
- Madal

7. Peamised vaated
Rakenduses peavad olema vähemalt järgmised vaated:
- sisselogimise vaade
- paranduste üldnimekiri
- uue paranduse lisamise vorm
- paranduse detailvaade
- paranduse muutmise vaade
- minu tööde vaade parandajale
- kokkuvõtte või dashboardi vaade paranduse meistrile

8. Üldnimekirja funktsioonid
Paranduste üldnimekirjas peab saama:
- otsida toote koodi järgi
- filtreerida osakonna järgi
- filtreerida kliendi või tootegrupi järgi
- filtreerida staatuse järgi
- filtreerida prioriteedi järgi
- filtreerida parandaja järgi
- sorteerida parandusse kandmise kuupäeva järgi

9. Dashboard
Loo kokkuvõttevaade, kus on näha:
- mitu tööd on alustamata
- mitu tööd on töös
- mitu tööd on lõpetatud
- mitu tööd on kõrge prioriteediga
- kõige vanemad avatud tööd
- tööde arv parandajate kaupa

10. Kasutusmugavus
- vormid peavad olema lihtsad ja loogilised
- prioriteet ja staatus peavad olema valitavad dropdown-väljad
- nimekirjavaates võiks kasutada värvilist märgistust staatuse ja prioriteedi jaoks
- rakendus peab olema skaleeruv ja sobima suurema hulga kirjete haldamiseks

11. Täiendavad soovitused
- lisa muutmiste ajalugu või logi, et oleks näha, kes ja millal staatust muutis
- võimalda kommentaaride lisamist töö käigus
- lisa valmisolek hiljem e-posti teavituste lisamiseks
- võimalda eksportida andmeid CSV või Excel formaati

12. Soovitud väljund
Palun genereeri:
- Django projekti struktuur
- models.py
- views.py
- forms.py
- urls.py
- vajalikud template failid
- admin.py seadistus
- näide kasutajaõiguste lahendusest
- lihtne ja selge Bootstrap-põhine kasutajaliides
- lühike juhend, kuidas projekt käivitada
