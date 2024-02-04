$startDate = Get-Date "09-04-2023"
$endDate = Get-Date "07-15-2024"
$subfolders = "Diplomaplan keuzedelen", "Diplomaplan kwalificaties", "Exameninstrumenten", "Resultaten"

while ($startDate -le $endDate) {
    $folderName = $startDate.ToString("yyyy-MM-dd")
    foreach($subfolder in $subfolders){
        New-Item -ItemType Directory -Force -Path "$folderName/$subfolder"
    }
    $startDate = $startDate.AddDays(7)
}
