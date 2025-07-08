#!/usr/bin/env python3
"""
LEC Mappen Generator
Automatische aanmaak van mappenstructuur voor de examencommissie van Alfa-college
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
import argparse
import sys

# Configuratie
SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "config.json"

# Standaard configuratie
DEFAULT_CONFIG = {
    "school_year_start_month": 9,  # September
    "school_year_start_day": 1,
    "school_year_end_month": 7,    # Juli
    "school_year_end_day": 31,
    "meeting_day": 0,              # Maandag (0=Maandag, 6=Zondag)
    "folder_types": {
        "LEC Vergaderingen": [],
        "Aanvragen Studenten": ["Aangepaste examinering", "Extra herkansing", "Hoger niveau", "Vrijstelling"],
        "Diplomabesluiten": ["Certificaten", "Diploma's", "Mbo-verklaringen"],
        "Vaststellingen": ["Diplomaplan keuzedelen", "Diplomaplan kwalificaties", "Exameninstrumenten", "Resultaten"]
    }
}

def load_config():
    """Laad configuratie uit bestand of maak standaard configuratie aan"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Fout in {CONFIG_FILE}, gebruik standaard configuratie")
    return DEFAULT_CONFIG

def save_config(config):
    """Sla configuratie op in bestand"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def get_school_year(year=None):
    """Bepaal schooljaar datums"""
    if year is None:
        current_date = datetime.now()
        # Als we voor september zijn, gebruiken we het vorige schooljaar
        if current_date.month < 9:
            year = current_date.year - 1
        else:
            year = current_date.year
    
    config = load_config()
    start_date = datetime(year, config["school_year_start_month"], config["school_year_start_day"])
    end_date = datetime(year + 1, config["school_year_end_month"], config["school_year_end_day"])
    
    return start_date, end_date

def get_mondays_in_range(start_date, end_date):
    """Vind alle maandagen in het opgegeven bereik"""
    mondays = []
    current_date = start_date
    
    # Vind eerste maandag
    while current_date.weekday() != 0:  # 0 = Maandag
        current_date += timedelta(days=1)
    
    # Verzamel alle maandagen
    while current_date <= end_date:
        mondays.append(current_date)
        current_date += timedelta(weeks=1)
    
    return mondays

def create_folder_structure(base_path, date, subfolders):
    """Maak mapstructuur aan voor een specifieke datum"""
    date_folder = date.strftime("%Y-%m-%d")
    full_path = Path(base_path) / date_folder
    
    try:
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Hoofdmap aangemaakt: {date_folder}")
        
        for subfolder in subfolders:
            subfolder_path = full_path / subfolder
            subfolder_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ Submap aangemaakt: {subfolder}")
            
    except Exception as e:
        print(f"✗ Fout bij aanmaken van {date_folder}: {e}")
        return False
    
    return True

def interactive_mode():
    """Interactieve modus voor gebruikersvriendelijke configuratie"""
    print("=== LEC Mappen Generator ===")
    print()
    
    config = load_config()
    
    # Schooljaar selectie met betere uitleg
    current_date = datetime.now()
    current_year = current_date.year
    
    # Bepaal welk schooljaar we suggereren
    if current_date.month < 9:
        # Voor september: huidig schooljaar (bijv. Juli 2025 → schooljaar 2024/2025)
        current_school_year = current_year - 1
        next_school_year = current_year
    else:
        # Na september: huidig schooljaar (bijv. September 2025 → schooljaar 2025/2026)
        current_school_year = current_year
        next_school_year = current_year + 1
    
    print(f"Huidige datum: {current_date.strftime('%d %B %Y')}")
    print(f"Huidig schooljaar: {current_school_year}/{current_school_year + 1}")
    print(f"Volgend schooljaar: {next_school_year}/{next_school_year + 1}")
    print()
    
    # Toon schooljaar opties
    print("Welk schooljaar:")
    print(f"1. Huidig schooljaar ({current_school_year}/{current_school_year + 1})")
    print(f"2. Volgend schooljaar ({next_school_year}/{next_school_year + 1})")
    print("3. Ander schooljaar (handmatig invoeren)")
    print()
    
    while True:
        try:
            choice = input("Kies een optie (1/2/3): ").strip()
            if choice == "1":
                year = current_school_year
                break
            elif choice == "2":
                year = next_school_year
                break
            elif choice == "3":
                year_input = input("Voer het startjaar van het schooljaar in (bijv. 2024 voor schooljaar 2024/2025): ").strip()
                year = int(year_input)
                break
            else:
                print("Kies 1, 2 of 3.")
        except ValueError:
            print("Voer een geldig jaar in.")
    
    # Maptype selectie
    print("\nBeschikbare maptypes:")
    folder_types = config["folder_types"]
    for i, (key, folders) in enumerate(folder_types.items(), 1):
        print(f"{i}. {key}")
        if folders:
            print(f"   Submappen: {', '.join(folders)}")
        else:
            print("   Alleen hoofdmappen")
    
    while True:
        try:
            choice = input("\nKies maptype (1-{}): ".format(len(folder_types))).strip()
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(folder_types):
                selected_type = list(folder_types.keys())[choice_idx]
                selected_folders = folder_types[selected_type]
                break
            else:
                print("Ongeldige keuze.")
        except ValueError:
            print("Voer een geldig nummer in.")
    
    # Bevestiging
    start_date, end_date = get_school_year(year)
    mondays = get_mondays_in_range(start_date, end_date)
    
    print(f"\nSamenvatting:")
    print(f"Schooljaar: {year}/{year + 1}")
    print(f"Periode: {start_date.strftime('%d %B %Y')} tot {end_date.strftime('%d %B %Y')}")
    print(f"Maptype: {selected_type}")
    print(f"Aantal maandagen: {len(mondays)}")
    print(f"Eerste maandag: {mondays[0].strftime('%d %B %Y')}")
    print(f"Laatste maandag: {mondays[-1].strftime('%d %B %Y')}")
    
    if input("\nDoorgaan? (j/n): ").lower() != 'j':
        print("Geannuleerd.")
        return
    
    # Mappen aanmaken
    print("\nMappen aanmaken...")
    success_count = 0
    
    for monday in mondays:
        if create_folder_structure(".", monday, selected_folders):
            success_count += 1
    
    print(f"\n✓ Klaar! {success_count}/{len(mondays)} mappen succesvol aangemaakt.")

def main():
    """Hoofdfunctie"""
    # Laad configuratie voor dynamische choices
    config = load_config()
    available_types = list(config["folder_types"].keys())
    
    parser = argparse.ArgumentParser(description="LEC Mappen Generator")
    parser.add_argument("--year", type=int, help="Startjaar van het schooljaar (bijv. 2024 voor schooljaar 2024/2025)")
    parser.add_argument("--type", choices=available_types, 
                       help="Type mapstructuur")
    parser.add_argument("--config", action="store_true", help="Configuratie bestand aanmaken/bewerken")
    parser.add_argument("--edit-config", action="store_true", help="Interactieve configuratie editor")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactieve modus (aanbevolen)")
    
    args = parser.parse_args()
    
    if args.config:
        config = load_config()
        save_config(config)
        print(f"Configuratie opgeslagen in {CONFIG_FILE}")
        return
    
    if args.edit_config:
        edit_config_interactive()
        return
    
    if args.interactive or (not args.year and not args.type):
        interactive_mode()
        return
    
    # Command line modus
    config = load_config()
    year = args.year or datetime.now().year
    folder_type = args.type or list(config["folder_types"].keys())[0]  # Gebruik eerste beschikbare type
    
    start_date, end_date = get_school_year(year)
    mondays = get_mondays_in_range(start_date, end_date)
    subfolders = config["folder_types"][folder_type]
    
    print(f"Mappen aanmaken voor schooljaar {year}/{year+1} ({folder_type})")
    success_count = 0
    
    for monday in mondays:
        if create_folder_structure(".", monday, subfolders):
            success_count += 1
    
    print(f"✓ {success_count}/{len(mondays)} mappen aangemaakt.")

def edit_config_interactive():
    """Interactieve configuratie editor"""
    config = load_config()
    
    print("=== Configuratie Editor ===")
    print()
    
    while True:
        print("Wat wil je bewerken?")
        print("1. Schooljaar datums")
        print("2. Mapstructuren (submappen)")
        print("3. Nieuwe mapstructuur toevoegen")
        print("4. Mapstructuur verwijderen")
        print("5. Configuratie opslaan en afsluiten")
        print("6. Afsluiten zonder opslaan")
        
        choice = input("\nKies een optie (1-6): ").strip()
        
        if choice == "1":
            edit_school_year_dates(config)
        elif choice == "2":
            edit_folder_structures(config)
        elif choice == "3":
            add_new_folder_type(config)
        elif choice == "4":
            remove_folder_type(config)
        elif choice == "5":
            save_config(config)
            print("✓ Configuratie opgeslagen!")
            break
        elif choice == "6":
            print("Configuratie niet opgeslagen.")
            break
        else:
            print("Ongeldige keuze.")
        print()

def edit_school_year_dates(config):
    """Bewerk schooljaar datums"""
    print("\nHuidige schooljaar datums:")
    print(f"Start: {config['school_year_start_day']}/{config['school_year_start_month']}")
    print(f"Eind: {config['school_year_end_day']}/{config['school_year_end_month']}")
    
    if input("\nWil je deze wijzigen? (j/n): ").lower() == 'j':
        try:
            config['school_year_start_month'] = int(input("Start maand (1-12): "))
            config['school_year_start_day'] = int(input("Start dag (1-31): "))
            config['school_year_end_month'] = int(input("Eind maand (1-12): "))
            config['school_year_end_day'] = int(input("Eind dag (1-31): "))
            print("✓ Schooljaar datums bijgewerkt!")
        except ValueError:
            print("✗ Ongeldige invoer, wijzigingen niet opgeslagen.")

def edit_folder_structures(config):
    """Bewerk bestaande mapstructuren"""
    folder_types = config["folder_types"]
    
    print("\nBeschikbare mapstructuren:")
    for i, (key, folders) in enumerate(folder_types.items(), 1):
        print(f"{i}. {key}")
        if folders:
            print(f"   Submappen: {', '.join(folders)}")
        else:
            print("   Alleen hoofdmappen")
    
    try:
        choice = int(input(f"\nWelke wil je bewerken (1-{len(folder_types)})? ")) - 1
        if 0 <= choice < len(folder_types):
            selected_key = list(folder_types.keys())[choice]
            edit_single_folder_type(config, selected_key)
        else:
            print("Ongeldige keuze.")
    except ValueError:
        print("Voer een geldig nummer in.")

def edit_single_folder_type(config, folder_key):
    """Bewerk één mapstructuur"""
    folders = config["folder_types"][folder_key]
    
    print(f"\nMapstructuur: {folder_key}")
    if folders:
        print("Huidige submappen:")
        for i, folder in enumerate(folders, 1):
            print(f"  {i}. {folder}")
    else:
        print("Geen submappen (alleen hoofdmappen)")
    
    print("\nOpties:")
    print("1. Submap toevoegen")
    print("2. Submap wijzigen")
    print("3. Submap verwijderen")
    print("4. Alle submappen wissen")
    print("5. Terug")
    
    choice = input("\nKies een optie (1-5): ").strip()
    
    if choice == "1":
        new_folder = input("Naam van nieuwe submap: ").strip()
        if new_folder:
            folders.append(new_folder)
            print(f"✓ Submap '{new_folder}' toegevoegd!")
    
    elif choice == "2" and folders:
        try:
            idx = int(input(f"Welke submap wijzigen (1-{len(folders)})? ")) - 1
            if 0 <= idx < len(folders):
                old_name = folders[idx]
                new_name = input(f"Nieuwe naam voor '{old_name}': ").strip()
                if new_name:
                    folders[idx] = new_name
                    print(f"✓ Submap gewijzigd van '{old_name}' naar '{new_name}'!")
        except (ValueError, IndexError):
            print("Ongeldige keuze.")
    
    elif choice == "3" and folders:
        try:
            idx = int(input(f"Welke submap verwijderen (1-{len(folders)})? ")) - 1
            if 0 <= idx < len(folders):
                removed = folders.pop(idx)
                print(f"✓ Submap '{removed}' verwijderd!")
        except (ValueError, IndexError):
            print("Ongeldige keuze.")
    
    elif choice == "4":
        if input("Alle submappen wissen? (j/n): ").lower() == 'j':
            folders.clear()
            print("✓ Alle submappen gewist!")

def add_new_folder_type(config):
    """Voeg nieuwe mapstructuur toe"""
    folder_types = config["folder_types"]
    
    new_key = input("\nNaam voor nieuwe mapstructuur: ").strip()
    if not new_key:
        print("Geen naam ingevoerd.")
        return
    
    if new_key in folder_types:
        print(f"Mapstructuur '{new_key}' bestaat al!")
        return
    
    print(f"\nSubmappen voor '{new_key}' (druk Enter zonder tekst om te stoppen):")
    subfolders = []
    while True:
        subfolder = input(f"Submap {len(subfolders) + 1}: ").strip()
        if not subfolder:
            break
        subfolders.append(subfolder)
    
    folder_types[new_key] = subfolders
    print(f"✓ Mapstructuur '{new_key}' toegevoegd met {len(subfolders)} submappen!")

def remove_folder_type(config):
    """Verwijder mapstructuur"""
    folder_types = config["folder_types"]
    
    if len(folder_types) <= 1:
        print("Kan niet alle mapstructuren verwijderen!")
        return
    
    print("\nBeschikbare mapstructuren:")
    for i, key in enumerate(folder_types.keys(), 1):
        print(f"{i}. {key}")
    
    try:
        choice = int(input(f"\nWelke verwijderen (1-{len(folder_types)})? ")) - 1
        if 0 <= choice < len(folder_types):
            key_to_remove = list(folder_types.keys())[choice]
            if input(f"'{key_to_remove}' verwijderen? (j/n): ").lower() == 'j':
                del folder_types[key_to_remove]
                print(f"✓ Mapstructuur '{key_to_remove}' verwijderd!")
        else:
            print("Ongeldige keuze.")
    except ValueError:
        print("Voer een geldig nummer in.")

if __name__ == "__main__":
    main()
