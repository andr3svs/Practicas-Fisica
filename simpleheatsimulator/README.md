# Configuración de Fortran en VS Code

## Pasos para configurar:

### 1. Instalar extensiones en VS Code:
- **Modern Fortran** (fortran-lang.linter-gfortran)
- **Fortran IntelliSense** (hansec.fortran-ls)
- **C/C++** (ms-vscode.cpptools)

### 2. Instalar compilador gfortran:

#### Opción A: MinGW-w64 (Windows nativo)
1. Descarga desde https://www.mingw-w64.org/downloads/
2. Instala la versión x86_64-posix-seh
3. Agrega `C:\mingw64\bin` al PATH del sistema
4. Reinicia VS Code

#### Opción B: WSL (Recomendado)
1. Ejecuta como administrador: `wsl --install`
2. Instala Ubuntu desde Microsoft Store
3. En WSL: `sudo apt update && sudo apt install gfortran`

### 3. Uso:
- **Ctrl+Shift+B**: Compilar archivo actual
- **Ctrl+Shift+P** → "Tasks: Run Task" → "Ejecutar Fortran"
- Los archivos .f90 tendrán resaltado de sintaxis automáticamente

### 4. Extensiones de archivo soportadas:
- `.f90` - Fortran moderno (free form)
- `.f` - Fortran clásico (fixed form)
- `.F90` - Fortran moderno con preprocesador
- `.F` - Fortran clásico con preprocesador
