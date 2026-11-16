# foerder.dk

Statisk hjemmeside for Førder (butik og fælles reception, Brøddegade 28, Gudhjem).
Erstatter den gamle one.com Website Builder-side. Udgiv ALDRIG fra Website Builder igen – den overskriver siden.

## Ret tekst
1. Ret teksterne i `build.py` (HOME, BUTIK, RECEP).
2. Kør `python3 build.py` – den færdige side lægges i `dist/`.
3. Commit og push til `main`.
4. Læg de ændrede filer fra `dist/` op på webhotellet (one.com File Manager, mappen httpd.www for foerder.dk).

Billederne ligger på webhotellet i `/onewebmedia/` (fra den gamle side) og ligger ikke i dette repo.
Statistik: Cloudflare Web Analytics (ingen cookies, intet cookie-banner).
Den gamle sides filer er gemt på webhotellet i `/_wsb-backup/` (spærret for besøgende).
