# jizdoteka-web

[![Gitter](https://badges.gitter.im/jizdoteka/general.svg)](https://gitter.im/jizdoteka/general?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

## Instalace

Pro účely vývoje/testování doporučuji použít `virtualenv` (pip3 install virtualenv)
```
pip3 install -r requirements.txt
```

Spuštění serveru: `./manage.py runserver`

Web je dostupný na: `http://localhost:8000`
Administrace (admin/admin): `http://localhost:8000/admin`

Pokud jste provedli nějaké změny v modelech: `./manage.py makemigrations` a následně `./manage.py migrate`

## Stav projektu
Rozpracováno (částečně funguje):
 * model DB, dost tam toho ještě chybí, ale to nejdůležitější (jízdy jako takové) jsou z velké části udělané. Počítám s tím, že se lidé mohou přihlásit jen na část trasy, cena za úsek je nepovinná
 * výpis jízd
 * detail vybrané jízdy - vč. přihlášených lidí na úsecích

Chybí, je třeba opravit (hmm.. od čeho začít :)
 * plnění webu day prozatím pouze skrze administraci (viz. link výše)
 * (skrze administraci) lze přihlásit pasažéra i na trasu mimo jeho jízdu - toto budeme stejně ošetřovat už při vkládání do DB, takže to nakonec tak moc vadit nebude
 * všechno ostatní ...
