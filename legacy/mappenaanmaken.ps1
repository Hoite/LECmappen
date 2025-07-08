$startDate = Get-Date "09-04-2023"
$endDate = Get-Date "07-15-2024"

while ($startDate -le $endDate) {
    $folderName = $startDate.ToString("yyyy-MM-dd")
    New-Item -ItemType Directory -Force -Path $folderName
    $startDate = $startDate.AddDays(7)
}
