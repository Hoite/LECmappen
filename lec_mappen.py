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
CONFIG_FILE = "config.json"

# Standaard configuratie
DEFAULT_CONFIG = {
    "school_year_start_month": 9,  # September
    "school_year_start_day": 1,
    "school_year_end_month": 7,    # Juli
    "school_year_end_day": 31,
    "meeting_day": 0,              # Maandag (0=Maandag, 6=Zondag)
    "folder_types": {
        "basic": [],
        "aanvragenstudenten": ["Aangepaste examinering", "Extra herkansing", "Hoger niveau", "Vrijstelling"],
        "diplomabesluiten": ["Certificaten", "Diploma's", "Mbo-verklaringen"],
        "vaststellingen": ["Diplomaplan keuzedelen", "Diplomaplan kwalificaties", "Exameninstrumenten", "Resultaten"]
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
    parser = argparse.ArgumentParser(description="LEC Mappen Generator")
    parser.add_argument("--year", type=int, help="Startjaar van het schooljaar (bijv. 2024 voor schooljaar 2024/2025)")
    parser.add_argument("--type", choices=["basic", "aanvragenstudenten", "diplomabesluiten", "vaststellingen"], 
                       help="Type mapstructuur")
    parser.add_argument("--config", action="store_true", help="Configuratie bestand aanmaken/bewerken")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactieve modus (aanbevolen)")
    
    args = parser.parse_args()
    
    if args.config:
        config = load_config()
        save_config(config)
        print(f"Configuratie opgeslagen in {CONFIG_FILE}")
        return
    
    if args.interactive or (not args.year and not args.type):
        interactive_mode()
        return
    
    # Command line modus
    config = load_config()
    year = args.year or datetime.now().year
    folder_type = args.type or "basic"
    
    start_date, end_date = get_school_year(year)
    mondays = get_mondays_in_range(start_date, end_date)
    subfolders = config["folder_types"][folder_type]
    
    print(f"Mappen aanmaken voor schooljaar {year}/{year+1} ({folder_type})")
    success_count = 0
    
    for monday in mondays:
        if create_folder_structure(".", monday, subfolders):
            success_count += 1
    
    print(f"✓ {success_count}/{len(mondays)} mappen aangemaakt.")

if __name__ == "__main__":
    main()
