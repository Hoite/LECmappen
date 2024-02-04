#!/bin/bash

startDate=$(date -jf "%d-%m-%Y" "04-09-2023" "+%s")
endDate=$(date -jf "%d-%m-%Y" "15-07-2024" "+%s")

folders=("Certificaten" "Diploma's" "Mbo-verklaringen" "Vaststellingslijsten, steekproefverslag en overige groepsdocumenten")

for (( i=startDate; i<=endDate; i+=(60*60*24*7) ))  # 60 seconden * 60 minuten * 24 uren * 7 dagen
do
    directoryName=$(date -r $i "+%Y-%m-%d")
    mkdir "$directoryName"

    for folder in "${folders[@]}"
    do
      mkdir "$directoryName/$folder"
    done
done

