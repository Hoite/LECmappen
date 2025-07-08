# Voorbeeld: Submappen configureren in config.json

## Huidige submappen per categorie:

### 1. aanvragenstudenten:
- Aangepaste examinering
- Extra herkansing  
- Hoger niveau
- Vrijstelling

### 2. diplomabesluiten:
- Certificaten
- Diploma's
- Mbo-verklaringen

### 3. vaststellingen:
- Diplomaplan keuzedelen
- Diplomaplan kwalificaties
- Exameninstrumenten
- Resultaten

## Voorbeelden van aanpassingen:

### Nieuwe submap toevoegen (handmatig in config.json):
```json
"aanvragenstudenten": [
  "Aangepaste examinering",
  "Extra herkansing",
  "Hoger niveau", 
  "Vrijstelling",
  "Individueel traject"  ← NIEUW
]
```

### Nieuwe mapstructuur toevoegen:
```json
"examens": [
  "Theoretische examens",
  "Praktische examens",
  "Herexamens",
  "Portfolio beoordelingen"
]
```

### Submappen wijzigen:
```json
"diplomabesluiten": [
  "Certificaten niveau 2",  ← GEWIJZIGD
  "Certificaten niveau 3",  ← GEWIJZIGD
  "Certificaten niveau 4",  ← GEWIJZIGD
  "Diploma's",
  "Mbo-verklaringen"
]
```

## Interactieve editor gebruiken:

```bash
# Start de configuratie editor
python3 lec_mappen.py --edit-config
```

De editor biedt een gebruiksvriendelijke interface om:
- Submappen toe te voegen/wijzigen/verwijderen
- Nieuwe mapstructuren te maken
- Schooljaar datums aan te passen
- Alles op te slaan zonder JSON handmatig te bewerken
