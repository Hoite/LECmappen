# Legacy Scripts

Deze folder bevat de originele Bash en PowerShell scripts uit versie 1.0.0.

## Bestanden

- `mappenaanmaken.sh` / `mappenaanmaken.ps1` - Basis mapstructuur
- `mappen_aanvragenstudenten.sh` / `mappen_aanvragenstudenten.ps1` - Aanvragenstudenten
- `mappen_diplomabesluiten.sh` / `mappen_diplomabesluiten.ps1` - Diplomabesluiten
- `mappen_vaststellingen.sh` / `mappen_vaststellingen.ps1` - Vaststellingen

## Waarom legacy?

Deze scripts zijn vervangen door het nieuwe Python script `lec_mappen.py` omdat:

- Ze moesten elk jaar handmatig aangepast worden
- Ze werkten alleen op specifieke platforms (Bash vs PowerShell)
- Ze hadden geen foutafhandeling
- Ze waren moeilijk te onderhouden door code duplicatie

## Gebruik van legacy scripts

**Alleen als het nieuwe Python script niet werkt:**

1. Pas start/einddatum aan in elk script
2. Maak executable: `chmod +x *.sh`
3. Voer uit: `./mappenaanmaken.sh`

**Aanbeveling:** Gebruik het nieuwe Python script in de hoofdfolder.
