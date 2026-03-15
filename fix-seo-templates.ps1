# Script para corregir todos los archivos SEOLandingTemplate que faltan title y description

$files = @(
    "frontend\app\reclamar-fianza-piso\page.tsx",
    "frontend\app\reclamar-vuelo-retrasado\page.tsx", 
    "frontend\app\reclamar-vuelo-cancelado\page.tsx",
    "frontend\app\recurso-reposicion-hacienda\page.tsx",
    "frontend\app\reclamacion-seguridad-social\page.tsx",
    "frontend\app\recurrir-multa-trafico\page.tsx"
)

foreach ($file in $files) {
    $fullPath = Join-Path $PSScriptRoot $file
    if (Test-Path $fullPath) {
        Write-Host "Procesando: $file"
        
        # Leer el contenido del archivo
        $content = Get-Content $fullPath -Raw
        
        # Extraer title y description del metadata
        if ($content -match 'title:\s*"([^"]*)"') {
            $title = $matches[1]
        }
        if ($content -match 'description:\s*\n\s*"([^"]*)"') {
            $description = $matches[1]
        }
        
        # Buscar y reemplazar el patrón <SEOLandingTemplate h1=
        $pattern = '(<SEOLandingTemplate\s+)(h1=)'
        $replacement = "`$1title=`"$title`"`n      description=`"$description`"`n      `$2"
        
        $newContent = $content -replace $pattern, $replacement
        
        # Escribir el archivo corregido
        Set-Content -Path $fullPath -Value $newContent -Encoding UTF8
        
        Write-Host "Corregido: $file"
    } else {
        Write-Host "No encontrado: $file"
    }
}

Write-Host "Corrección completada."