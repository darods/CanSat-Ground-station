# GUI Estación Terrena para CanSat y OBCs 🚀

Interfaz de monitoreo de telemetría en tiempo real para CanSats y Computadoras de A Bordo (OBCs). Muestra altitud, aceleración en 3 ejes, giroscopio en 3 ejes, presión barométrica, temperatura, velocidad, estado de batería y caída libre.

Modernizado para funcionar en **Linux**, **macOS** y **Windows 11** utilizando herramientas modernas de Python ([`uv`](https://github.com/astral-sh/uv)), Python 3.10+ y **PyQt6** / **PyQt5**.

![Interfaz Estación Terrena](https://i.imgur.com/zDY3DnY.gif)

---

## ⚡ Inicio Rápido con `uv`

La forma recomendada de ejecutar la aplicación en Linux, macOS y Windows 11 es usando **`uv`**.

### Requisitos previos
Instalar `uv` (si aún no lo tienes instalado):
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Instalación y Ejecución

1. Clona el repositorio e ingresa al directorio:
   ```bash
   git clone https://github.com/darods/CanSat-Ground-station.git
   cd CanSat-Ground-station
   ```

2. Ejecutar en **Modo Simulación / Dummy** (no requiere hardware ni puerto serie):
   ```bash
   uv run main.py --dummy
   ```

3. Ejecutar con **Puerto Serie de Hardware Real**:
   ```bash
   # Linux (ejemplo: /dev/ttyUSB0 o /dev/ttyACM0)
   uv run main.py --port /dev/ttyUSB0 --baud 9600

   # macOS (ejemplo: /dev/tty.usbmodem14101)
   uv run main.py --port /dev/tty.usbmodem14101

   # Windows 11 (ejemplo: COM3)
   uv run main.py --port COM3
   ```

---

## 🛠 Opciones de Línea de Comandos

```text
Opciones:
  -h, --help           Muestra el mensaje de ayuda y sale
  --port PORT          Nombre del puerto serie (ej: /dev/ttyUSB0, COM3, /dev/tty.usbmodem14101)
  --baud BAUD          Velocidad en baudios (por defecto: 9600)
  --dummy              Fuerza el modo de datos simulados (dummy)
  --interval INTERVAL  Intervalo de actualización de telemetría en ms (por defecto: 500)
```

---

## 📊 Formato del Trama de Telemetría

La estación lee tramas de valores separados por comas desde el puerto serie (o los genera dinámicamente en modo simulado):

| Índice | Campo | Descripción |
|---|---|---|
| `0` | Tiempo | Tiempo transcurrido de vuelo (ms) |
| `1` | Altitud | Altitud relativa (metros) |
| `2` | Caída Libre | Indicador de caída libre (`0` = No, `1` = Sí) |
| `3` | Temperatura | Temperatura (°C) |
| `4` | Presión | Presión barométrica (hPa) |
| `5` | Gyro Pitch | Velocidad angular Pitch (°/s) |
| `6` | Gyro Roll | Velocidad angular Roll (°/s) |
| `7` | Gyro Yaw | Velocidad angular Yaw (°/s) |
| `8` | Accel X | Aceleración en eje X (m/s²) |
| `9` | Accel Y | Aceleración en eje Y (m/s²) |
| `10` | Accel Z | Aceleración en eje Z (m/s²) |

Los datos pueden guardarse en `flight_data.csv` en tiempo real haciendo clic en **Start storage** en la interfaz gráfica.

---

## 📦 Tecnologías y Compatibilidad

- **Gestor de paquetes**: [`uv`](https://astral-sh.github.io/uv/)
- **Python**: `>=3.10`
- **Interfaz gráfica**: PyQt6 / PyQt5 (`pyqtgraph`)
- **Conexión serie**: `pyserial`
- **Cálculos**: `numpy`

---

## 📜 Licencia

[Licencia MIT](LICENSE).

Desarrollado por **Daniel Alejandro Rodríguez Suárez**, Líder del semillero de investigación ATL, vinculado al **Grupo de Investigación LIDER** de la Universidad Distrital Francisco José de Caldas.
