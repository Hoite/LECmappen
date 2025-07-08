# LEC mappen
Universeel Python script voor het aanmaken van mappen en submappen per week voor de examencommissie van Alfa-college.

## Functies

- ✅ **Cross-platform**: Werkt op Windows, macOS en Linux
- ✅ **Automatische schooljaar detectie**: Geen handmatige datums aanpassen
- ✅ **Interactieve modus**: Gebruiksvriendelijke interface
- ✅ **Configureerbaar**: Eenvoudig aanpassen via config.json
- ✅ **Meerdere maptypes**: Verschillende structuren voor verschillende doeleinden

## Vereisten

- Python 3.6 of hoger

## Gebruik

### Eenvoudige methode (Aanbevolen)

1. **Downloaden repository**
   ```bash
   git clone https://github.com/Hoite/LECmappen
   cd LECmappen
   ```

2. **Uitvoeren**
   
   **Windows:**
   ```cmd
   run_windows.bat
   ```
   
   **Linux/macOS:**
   ```bash
   chmod +x run_unix.sh
   ./run_unix.sh
   ```

### Geavanceerde methode

**Interactieve modus:**
```bash
python3 lec_mappen.py --interactive
```

**Command line modus:**
```bash
# Mappen voor volgend schooljaar (2025/2026)
python3 lec_mappen.py --year 2025 --type basic

# Mappen voor huidig schooljaar (2024/2025)
python3 lec_mappen.py --year 2024 --type aanvragenstudenten

# Alle opties bekijken
python3 lec_mappen.py --help
```

## Schooljaar notatie

Het programma gebruikt de standaard schooljaar notatie:
- **Schooljaar 2024/2025**: Start september 2024, eindigt juli 2025
- **Jaar parameter**: Gebruik het **startjaar** (bijv. `--year 2024` voor schooljaar 2024/2025)
- **Automatische detectie**: In interactieve modus krijg je duidelijke keuzes tussen huidig en volgend schooljaar

### Praktisch gebruik:
- **Einde schooljaar (juni/juli)**: Maak alvast mappen voor volgend schooljaar
- **Begin schooljaar (september)**: Maak mappen voor huidig schooljaar
- **Tussentijds**: Kies zelf welk schooljaar je nodig hebt

## Configuratie

Het bestand `config.json` bevat alle instellingen en je kunt dit eenvoudig aanpassen:

### Handmatig bewerken:
```json
{
  "school_year_start_month": 9,     // September
  "school_year_start_day": 1,       // 1e dag van de maand
  "school_year_end_month": 7,       // Juli
  "school_year_end_day": 31,        // Laatste dag van de maand
  "meeting_day": 0,                 // 0=Maandag, 1=Dinsdag, etc.
  "folder_types": {
    "basic": [],                    // Alleen hoofdmappen
    "aanvragenstudenten": [         // Met submappen
      "Aangepaste examinering",
      "Extra herkansing",
      "Hoger niveau", 
      "Vrijstelling"
    ],
    "diplomabesluiten": [...],      // Met submappen
    "vaststellingen": [...]         // Met submappen
  }
}
```

### Interactieve configuratie editor:
```bash
# Start de configuratie editor
python3 lec_mappen.py --edit-config
```

**Met de configuratie editor kun je:**
- ✅ Schooljaar datums aanpassen
- ✅ Submappen per categorie toevoegen/wijzigen/verwijderen
- ✅ Nieuwe mapstructuren maken
- ✅ Bestaande mapstructuren verwijderen
- ✅ Alles opslaan zonder handmatig JSON te bewerken

### Submappen aanpassen:

**Nieuwe submap toevoegen:**
- Voeg toe aan de lijst in `config.json`
- Of gebruik `--edit-config` voor gebruiksvriendelijke interface

**Nieuwe mapstructuur maken:**
```json
"folder_types": {
  "examens": [
    "Theoretische examens",
    "Praktische examens",
    "Herexamens"
  ]
}
```

**Bestaande submappen wijzigen:**
- Pas de namen aan in `config.json`  
- Of gebruik de interactieve editor
```

## Beschikbare maptypes

- **basic**: Alleen wekelijkse hoofdmappen (YYYY-MM-DD)
- **aanvragenstudenten**: Met submappen voor aanvragen
- **diplomabesluiten**: Met submappen voor diploma's en certificaten
- **vaststellingen**: Met submappen voor vaststellingen

## Troubleshooting

### Python niet gevonden
- **Windows**: Download Python van [python.org](https://python.org) en zorg dat "Add Python to PATH" is aangevinkt
- **macOS**: Installeer Python via Homebrew: `brew install python3`
- **Linux**: Installeer via package manager: `sudo apt install python3` (Ubuntu/Debian) of `sudo yum install python3` (RHEL/CentOS)

### Permissie problemen
- **Linux/macOS**: Zorg dat scripts executable zijn: `chmod +x lec_mappen.py run_unix.sh`

### Configuratie aanpassen
- Bewerk `config.json` om schooljaar datums of mapnamen aan te passen
- Gebruik `python3 lec_mappen.py --config` om configuratie te valideren

## Migratie van oude scripts

Als je de oude Bash/PowerShell scripts gebruikt, kun je eenvoudig migreren:

1. Backup je huidige mappen
2. Installeer de nieuwe versie
3. Gebruik `--interactive` modus voor eerste keer
4. Oude scripts kunnen worden verwijderd

## Voordelen van de nieuwe versie

### Vs. Oude Bash/PowerShell scripts:
- ✅ Geen jaarlijkse aanpassing van datums nodig
- ✅ Werkt op alle platforms (Windows, macOS, Linux)
- ✅ Gebruiksvriendelijke interface
- ✅ Configureerbaar zonder code te wijzigen
- ✅ Automatische schooljaar detectie
- ✅ Betere foutafhandeling
- ✅ Flexibele mapstructuren

## Bijdragen

Heb je suggesties of verbeteringen? Maak een issue of pull request aan op GitHub.

## Changelog

### v2.0.0 (2025-07-08)
- Volledig herschreven in Python voor cross-platform ondersteuning
- Automatische schooljaar detectie
- Configureerbaar via JSON bestand
- Interactieve modus toegevoegd
- Betere foutafhandeling
- Meerdere mapstructuren ondersteund

### v1.0.0 (2024)
- Originele Bash en PowerShell scripts

---

```
Auteur: Hoite Prins
Versie: 2.0.0
Licentie: MIT
```