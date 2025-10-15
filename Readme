# API Generador de Códigos QR

API REST desarrollada con Flask para generar códigos QR personalizables.

## Características

- Generación de códigos QR desde texto, URLs, datos TOTP, etc.
- Tamaño personalizable (formato `300x300` o `300_300`)
- Control de borde ajustable
- Respuesta como archivo PNG o base64
- Endpoints GET y POST disponibles

## Requisitos

- Python 3.7+
- Flask
- qrcode[pil]

## Instalación

1. Clonar o descargar el proyecto

2. Crear un entorno virtual:
```bash
python -m venv .venv
```

3. Activar el entorno virtual:
   - Windows:
   ```bash
   .venv\Scripts\activate
   ```
   - Linux/Mac:
   ```bash
   source .venv/bin/activate
   ```

4. Instalar dependencias:
```bash
pip install flask qrcode[pil]
```

## Uso

### Iniciar el servidor

```bash
python Main.py
```

El servidor se iniciará en `http://127.0.0.1:5000`

## Endpoints

### 1. POST `/generar-qr`

Genera un código QR con opciones completas.

**Parámetros (JSON):**
- `data` (requerido): Contenido del código QR
- `size` (opcional): Tamaño en formato `300x300` o número para tamaño de cajas (default: 10)
- `border` (opcional): Grosor del borde en cajas (default: 1)
- `formato` (opcional): `archivo` o `base64` (default: archivo)

**Ejemplo con curl:**
```bash
curl -X POST http://127.0.0.1:5000/generar-qr \
  -H "Content-Type: application/json" \
  -d '{"data": "https://ejemplo.com", "size": "300x300", "border": 1}' \
  --output qr.png
```

**Ejemplo con Python:**
```python
import requests

response = requests.post('http://127.0.0.1:5000/generar-qr', 
    json={
        'data': 'https://ejemplo.com',
        'size': '300x300',
        'border': 1
    }
)

with open('qr.png', 'wb') as f:
    f.write(response.content)
```

**Obtener base64:**
```bash
curl -X POST http://127.0.0.1:5000/generar-qr \
  -H "Content-Type: application/json" \
  -d '{"data": "Hola Mundo", "size": "400x400", "formato": "base64"}'
```

### 2. GET `/generar-qr-get`

Genera un código QR usando parámetros URL.

**Parámetros (Query):**
- `data` (requerido): Contenido del código QR
- `size` (opcional): Tamaño en formato `300x300` o `300_300`
- `border` (opcional): Grosor del borde (default: 1)

**Ejemplo:**
```bash
curl "http://127.0.0.1:5000/generar-qr-get?data=https://ejemplo.com&size=300x300&border=1" --output qr.png
```

**Desde navegador:**
```
http://127.0.0.1:5000/generar-qr-get?data=https://ejemplo.com&size=300_300
```

### 3. GET `/health`

Verifica el estado de la API.

**Ejemplo:**
```bash
curl http://127.0.0.1:5000/health
```

**Respuesta:**
```json
{
  "status": "ok",
  "message": "API funcionando correctamente"
}
```

## Ejemplos de Uso

### QR para URL
```bash
curl "http://127.0.0.1:5000/generar-qr-get?data=https://github.com&size=500x500" -o github_qr.png
```

### QR para WiFi
```bash
curl -X POST http://127.0.0.1:5000/generar-qr \
  -H "Content-Type: application/json" \
  -d '{"data": "WIFI:T:WPA;S:MiRed;P:MiPassword;;", "size": "400x400"}' \
  -o wifi_qr.png
```

### QR para TOTP (Autenticación de dos factores)
```bash
curl "http://127.0.0.1:5000/generar-qr-get?size=300_300&data=otpauth://totp/App:usuario@example.com?secret=SECRETKEY&issuer=App" -o totp_qr.png
```

### QR sin borde
```bash
curl "http://127.0.0.1:5000/generar-qr-get?data=Sin+borde&size=300x300&border=0" -o sin_borde.png
```

## Formato de Tamaño

El parámetro `size` acepta dos formatos:

1. **Dimensiones exactas**: `300x300` o `300_300` (ancho x alto en píxeles)
2. **Tamaño de cajas**: Número entero (ej: `10`) que define el tamaño de cada cuadrito del QR

## Notas

- El formato `300_300` es recomendado para URLs GET ya que no requiere encoding especial
- Para usar `300x300` en URLs GET, debe codificarse como `300%78300`
- El borde predeterminado es 1 caja para un margen mínimo
- La API soporta cualquier dato que pueda ser codificado en un código QR

## Solución de Problemas

**Error: `ModuleNotFoundError: No module named 'flask'`**
- Solución: Instalar dependencias con `pip install flask qrcode[pil]`

**Error: `invalid literal for int() with base 10: '300x300'`**
- Solución: Usar formato `300_300` o codificar la 'x' como `%78` en URLs GET

## Licencia

Libre para uso personal y comercial.