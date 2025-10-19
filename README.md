# 🎵 Lyrics Music Player

Un reproductor de música con visualizador de audio y letras sincronizadas en tiempo real para la terminal.

![Demo](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Características

- 🎶 **Reproductor de audio** con soporte para MP3 y otros formatos
- 🎨 **Visualizador de audio** en tiempo real con efectos coloridos
- 📝 **Letras sincronizadas** que aparecen automáticamente
- 🌐 **Búsqueda automática** de letras desde múltiples fuentes online
- ⚡ **Efectos visuales** dinámicos (pulsación, sparkles, colores cambiantes)
- 📊 **Barra de progreso** con tiempo transcurrido
- 🎯 **Centrado automático** de texto en la terminal

## 🚀 Instalación

### Requisitos previos
- Python 3.8 o superior
- Sistema operativo: Windows, macOS, Linux

### Instalar dependencias

```bash
pip install numpy sounddevice soundfile pyfiglet requests
```

### Descargar el proyecto

```bash
git clone https://github.com/xtaxx12/Lyrics-music.git
cd Lyrics-music
```

## 🎯 Uso rápido

1. **Coloca tu archivo de música** en la carpeta del proyecto
2. **Edita el archivo `lyrics.py`** y cambia estas líneas:

```python
AUDIO_FILE   = "tu-cancion.mp3"    # Nombre de tu archivo
START_TIME   = 0                   # Segundo donde empezar (opcional)
LYRIC_OFFSET = 0                   # Ajuste de sincronización (opcional)
```

3. **Ejecuta el reproductor:**

```bash
python lyrics.py
```

## 📁 Formato recomendado de archivos

Para mejores resultados en la búsqueda de letras, nombra tus archivos así:

```
Artista - Canción.mp3
```

**Ejemplos:**
- `Arctic Monkeys - Do I Wanna Know.mp3`
- `The Weeknd - Blinding Lights.mp3`
- `Billie Eilish - Bad Guy.mp3`

## ⚙️ Configuración avanzada

### Variables principales

```python
AUDIO_FILE   = "cancion.mp3"    # Tu archivo de música
START_TIME   = 30               # Empezar en el segundo 30
LYRIC_OFFSET = -1.5             # Ajustar sincronización de letras
LRC_FOLDER   = "~/lyrics"       # Carpeta para archivos .lrc locales
```

### Ajustar sincronización de letras

Si las letras no están sincronizadas:
- **Positivo** (`LYRIC_OFFSET = 2.0`): Letras aparecen 2 segundos después
- **Negativo** (`LYRIC_OFFSET = -1.5`): Letras aparecen 1.5 segundos antes

## 🌐 Fuentes de letras

El sistema busca letras automáticamente en:

1. **LRCLIB** - Base de datos principal
2. **NetEase Music** - Fuente alternativa
3. **Archivos locales** - Carpeta `~/lyrics`

### Usar archivos .lrc locales

1. Crea la carpeta: `~/lyrics` (en tu directorio home)
2. Descarga archivos `.lrc` de sitios como:
   - [lrclib.net](https://lrclib.net)
   - [megalobiz.com/lrc](https://megalobiz.com/lrc)
3. Guárdalos con el mismo nombre que tu MP3

## 🎨 Efectos visuales

- **Colores dinámicos** que cambian con el tiempo
- **Pulsación** sincronizada con la música
- **Sparkles** (✦) durante picos de audio altos
- **Texto centrado** con efectos de resaltado
- **Vista previa** de próximas líneas de letra

## 🛠️ Solución de problemas

### No encuentra letras
```bash
# Verifica el formato del nombre del archivo
"Artista - Canción.mp3"

# O descarga manualmente el archivo .lrc a ~/lyrics/
```

### Audio no reproduce
```bash
# Instala dependencias de audio
pip install sounddevice soundfile

# En Linux, puede necesitar:
sudo apt-get install portaudio19-dev
```

### Letras desincronizadas
```python
# Ajusta el offset en lyrics.py
LYRIC_OFFSET = -2.0  # Prueba diferentes valores
```

## 📝 Controles

- **Ctrl+C**: Detener reproducción
- El reproductor se detiene automáticamente al final de la canción

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Créditos

- **APIs de letras**: LRCLIB, NetEase Music
- **Librerías**: NumPy, SoundDevice, SoundFile, PyFiglet, Requests

---

**¿Problemas o sugerencias?** Abre un [issue](https://github.com/xtaxx12/Lyrics-music/issues) en GitHub.

**¡Disfruta tu música con estilo! 🎵✨**