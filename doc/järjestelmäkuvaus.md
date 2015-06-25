# Pistedatatallennin

## Johdanto

Järjestelmään on tarkoitus tallettaa metadataa käyttäjän vierailemista paikoista. Talletettava tieto voi olla mitä vain, minkä käyttäjä arvioi itselleen tai muille hyödylliseksi. 

Pistedatatallennin on selaimen avulla käytettävä sovellus, johon käyttäjä syöttää tietoa siitä mitä mielenkiintoista kyseisessä paikassa on. Sijainnin haun hoitaa selain ja se talletetaan tietokantaan sellaisenaan. Pisteillä voisi olla jonkinlainen säde, jotta jotkin paikat tallentuisivat "samoina" paikkoina. (tämän toteutumisesta en ole vielä oikein varma)

Pistedatatallentimella käyttäjä voi tagata paikkoja haluamillaan tageilla, ja sitten esim. listata niitä. Esimerkiksi käyttäjä voi tallettaa tiedon siitä missä on hyviä ravintoloita tai missä on vaarallisia risteyksiä.

Sovellus toteutetaan python-ohjelmointikielellä ja Bottle-mikroframeworkilla, jota ajetaan Osuuskunta Sangen Oiva-palvelimella. Tietokantatalletukset tehdään Oivan PostgreSQL-tietokantaan.

Jos ehdin ja osaan, toteutan sovellukseen karttanäkymän, josta käyttäjä näkee intuitiivisesti tekemänsä tietokantatalletukset. Tämä todennäköisesti vaatii jotain javascript-säätöä.

## Käyttötapaukset

![käyttötapauskaavio](käyttötapauskaavio.png)

### Käyttäjäryhmät

Käyttäjä
- kuka tahansa sovellukseen rekisteröityvä henkilö. Tavallisen käyttäjän rooli

Ylläpitäjä
- käytännössä käyttäjä, mutta jolta löytyy ylläpitäjän rooli ja oikeus poistaa paikkatietoja

### Käyttötapauskuvaukset

#### Käyttäjän käyttötapaukset

Uuden käyttäjän luominen
- kuka tahansa voi luoda uuden käyttäjän

Omien tietojen muokkaus
- nimi

Tiedon syöttäminen
- rekisteröityneet ja kirjautuneet käyttäjät voivat luoda uuden paikkatiedon. Selain hakee lomakkeeseen sijainnin ja käyttäjä täyttää varsinaisen tiedon ja lisää tagit.

Tiedon listaaminen
- käyttäjä voi suodattaa tietoa tagien perusteella. Tageja voi valita useita kerrallaan tai ei yhtään (jolloin käyttäjälle listataan kaikki paikkatiedot)

Tiedon poistaminen
- käyttäjä voi poistaa sellaisen paikkatiedon, jonka omistaja hän on

Tiedon yhdistäminen
- käyttäjä voi yhdistää kaksi paikkatietoa, jolloin luodaan kolmas paikkatieto, joka laskee näiden kahden pisteen puolivälin koordinaattien perustella ja se asetetaan uuden paikkatiedon sijainnksi. Kumpaakaan näistä paikkatiedoista ei poisteta, mutta niitä ei myöskään näytetä listauksissa.

#### Ylläpitäjän käyttötapaukset

Käyttäjän poistaminen
- käyttäjiä kannattaa poistaa vain jos ne ovat häiriköiviä, esim spämmereitä.

## Järjestelmän tietosisältö
![tietosisältökaavio] (tietosisältökaavio.png)

### paikka

                               Table "public.paikka"
            Column    |  Type   |                      Modifiers
         --------------+---------+-----------------------------------------------------
         id           | integer | not null default nextval('paikka_id_seq'::regclass)
         koordinaatti | point   | not null
         omistaja     | integer | 
         luotu        | date    | default now()
         yhdpaikkaan  | integer | 

postgreSQL tarjoaa pistedatatyypin, jota käytetään koordinaattien tallettamisessa. Omistaja on integer, joka viittaa käyttäjän id:hen. Yhdpaikkaan on mergeämistä varten. Jos yhdpaikkaan ei ole null, kyseistä paikkaa ei näytetä listauksissa.

### kuvaus

                                  Table "public.kuvaus"
          Column |           Type           |                      Modifiers                      
         --------+--------------------------+-----------------------------------------------------
         id     | integer                  | not null default nextval('kuvaus_id_seq'::regclass)
         paikka | integer                  | not null
         kuvaus | text                     | not null
         luotu  | timestamp with time zone | default now()

Paikka viittaa paikan id:hen. Kuvaus on mitä tahansa paikkaan liittyvää kuvailevaa tekstiä.

### käyttäjä

                                   Table "public.kayttaja"
         Column  |           Type           |                       Modifiers                       
          -------+--------------------------+-------------------------------------------------------
        id       | integer                  | not null default nextval('kayttaja_id_seq'::regclass)
        nimi     | text                     | 
        tunnus   | text                     | not null
        salasana | text                     | 
        luotu    | timestamp with time zone | default now()
        muokattu | timestamp with time zone | default now()
        rooli    | rooli                    | 

Nimi on käyttäjän nimi. Tunnus on käyttäjän käyttäjätunnus. Rooli on enum, joka voi olla joko "tavis" tai "admin".

### tagi

                         Table "public.tagi"
          Column |  Type   |                     Modifiers                     
         --------+---------+---------------------------------------------------
          id     | integer | not null default nextval('tagi_id_seq'::regclass)
          tagi   | text    | not null
          lang   | text    | 

tagi on yleensä lyhyt, yhden sanan mittainen kuvaileva sana, esimerkiksi "ravintola" tai "uimapaikka"

### paikkatagi

        Table "public.paikkatagi"
          Column |  Type   | Modifiers 
         --------+---------+-----------
          paikka | integer | 
          tagi   | integer | 

paikka ja tagi viittaavat paikka ja tagi -taulujen id-kohtiin.


## Relaatiotietokantakaavio

![tietokantakaavio] (tietokantakaavio.png)

## Järjestelmän yleisrakenne

Sovellus noudattaa MVC-mallia. pistesovellus.py -tiedostosta löytyy Model-luokka, josta löytyy kaikki tietokantaa käsittelevät funktiot. Tiedoston lopussa on peräkkäin kaikki kontrollerifunktiot. Näkymät löytyvät taas src/sivut -hakemiston alta.

Järjestelmän riippuvuuksista pitää huolta Makefile, jolloin sovellusta on syytä ajaa komennolla $make run

## Käyttöliittymä ja järjestelmän komponentit

![käyttöliittymäkaavio] (käyttöliittymä.png)

## Asennustiedot

Sovellus voidaan pystyttää kloonaamalla pistedatatallennin-repo githubista ja sen jälkeen hyödyntämällä Makefilea. Riippuudet ja käynnistys tehdään Makefilen avulla. Makefilessa on melkein kaikki tarvittavat riippuvuudet sovelluksen toiminnan kannalta. Sovellusta pyörittävässä koneessa on lisäksi oltava asennettuna Python ja Pythonin sessiohallintalisäosa python-beaker. 

Eri palvelimissa postgresql-portti on eri paikassa, joten ennen sovelluksen käynnistämistä pitäisi suoritettavassa hakemistossa olla config-tiedosto "pisteconfig.py", jonka sisältö on: 

					port=5432

5432 on oletusportti

Sovellus käynnistetään komentoriviltä komennolla:

					$ make run

joka lataa bottle-kirjaston suoritettavaan hakemistoon ja luo tietokannan taulut, jos niitä ei ole luotu jo. Jos halutaan tietokantaan testidataa, annetaan komentoriviltä komento:

					$ make import-data

ja jos halutaan tyhjentää koko tietokanta datasta ja tauluista, se tehdään helpoiten komennolla:

					$ make clean-database

## Käyttöohje

Sovellusta voi tällä hetkellä testata kirjautumalla sisään näillä tiedoilla: 

				käyttäjätunnus: test 
				salasana: test123

Ilman kirjautumista sovelluksessa voi käyttää hakutoimintoa, joka listaa paikkoja.
Kirjautumisen jälkeen sovellus uudelleenohjaa käyttäjän etusivulle, josta käyttäjä voi hakea paikkoja, tai valita lisäävänsä uuden paikan. Jos kirjautumaton käyttäjä yrittää lisätä uuden paikan, sovellus ohjaa käyttäjän kirjautumaan sisään.

## Omat kokemukset

Halusin tehdä sovelluksen Pythonilla, koska halusin enemmän käytännöllistä koodauskokemusta Pythonista. Valitsin ensin kehitysympäristökseni Bottlen, joka antoi yksinkertaiset puitteet. Bottle on hyvin minimalistinen ja sen päälle oli suhteellisen helppoa rakentaa sovellusta. Webdevaus oli minulle silti aivan uutta ja jouduin opettelemaan paljon uusia asioita. Luin mielettömät määrät dokumentaatiota, joista ainakin osan tallensin [tälle sivulle] (linkkejä.md)

Javascript on minulle aivan tuntematon, mutta onneksi w3.orgista löytyi selkeä määrittely geopositioningia varten.

Pääsin myös tutustumaan Google developers Console -työkaluihin.

## TODO

- kuvausten lisääminen tietokantaan ja niiden näyttäminen hakusivulla
- paikkojen mergeäminen

- käyttäjän merkitseminen paikkojensa omistajaksi
- omien paikkojen tarkastelusivu "mypage.tpl"

- koordinaattien sijoittaminen googlemapsiin
- syötteiden validointi



