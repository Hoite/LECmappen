$startDate = Get-Date "09-04-2023"
$endDate = Get-Date "07-15-2024"
$subfolders = "Aangepaste examinering", "Extra herkansing", "Hoger niveau", "Vrijstelling"

while ($startDate -le $endDate) {
    $folderName = $startDate.ToString("yyyy-MM-dd")
    foreach($subfolder in $subfolders){
        New-Item -ItemType Directory -Force -Path "$folderName/$subfolder"
    }
    $startDate = $startDate.AddDays(7)
}
