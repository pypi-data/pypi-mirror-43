trap { Write-Error $_; Exit 1 }

$downloadDir = "C:/Downloads"
New-Item -ItemType Directory -Force -Path $downloadDir

if (![System.IO.File]::Exists("$downloadDir\install-utils.ps1")) {
  Write-Host "Download install-utils.ps1"
  $url = "https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-utils.ps1"
  (new-object net.webclient).DownloadFile($url, "$downloadDir\install-utils.ps1")
}
Import-Module "$downloadDir\install-utils.ps1" -Force

$version = "1.9.5"
$archiveName = "Slik-Subversion-$version-x64"
$targetDir = "C:\\SlikSvn"

if ([System.IO.Directory]::Exists($targetDir)) {
  Write-Host "Installing $archiveName.msi into $targetDir"
  Write-Host "-> skipping: existing target directory"
  return
}

Download-URL "https://sliksvn.com/pub/$archiveName.zip" $downloadDir

Always-Extract-Zip (Join-Path $downloadDir "$archiveName.zip") "$downloadDir"

Install-MSI "$archiveName.msi" $downloadDir "$targetDir-tmp"

$from = Join-Path "$targetDir-tmp" "SlikSvn"
Write-Host "Moving $from to $targetDir"
Move-Item "$from" "$targetDir"

Write-Host "Removing $targetDir-tmp"
Remove-Item "$targetDir-tmp" -Recurse

Write-Host "Pre-pending '$targetDir\bin\' to PATH"
[Environment]::SetEnvironmentVariable("Path", "$targetDir\bin\;$env:Path", "Machine")
