# Ground Station GUI for CanSat & OBCs 🚀

Real-time telemetry monitoring interface for CanSats and On-Board Computers (OBCs). Displays altitude, 3-axis acceleration, 3-axis gyroscope, pressure, temperature, speed, battery, and free-fall status in real-time.

Modernized to support **Linux**, **macOS**, and **Windows 11** using modern Python tooling ([`uv`](https://github.com/astral-sh/uv)), Python 3.10+, and **PyQt6** / **PyQt5**.

![Ground Station Interface](https://i.imgur.com/zDY3DnY.gif)

---

## ⚡ Quick Start with `uv`

The recommended way to run this application across Linux, macOS, and Windows 11 is using **`uv`**.

### Prerequisites
Install `uv` (if not already installed):
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Installation & Execution

1. Clone the repository and navigate into the project directory:
   ```bash
   git clone https://github.com/darods/CanSat-Ground-station.git
   cd CanSat-Ground-station
   ```

2. Run in **Simulated / Dummy Mode** (no sensors or serial connection required):
   ```bash
   uv run main.py --dummy
   ```

3. Run with a **Real Serial Hardware Port**:
   ```bash
   # Linux (e.g. /dev/ttyUSB0 or /dev/ttyACM0)
   uv run main.py --port /dev/ttyUSB0 --baud 9600

   # macOS (e.g. /dev/tty.usbmodem14101)
   uv run main.py --port /dev/tty.usbmodem14101

   # Windows 11 (e.g. COM3)
   uv run main.py --port COM3
   ```

---

## 🛠 Command-Line Options

```text
options:
  -h, --help           Show help message and exit
  --port PORT          Serial port device name (e.g. /dev/ttyUSB0, COM3, /dev/tty.usbmodem14101)
  --baud BAUD          Serial baud rate (default: 9600)
  --dummy              Force simulated telemetry data mode
  --interval INTERVAL  Telemetry polling rate in ms (default: 50)
```

---

## 📊 Telemetry Data Frame Format

The station reads comma-separated CSV frames from serial hardware (or generates them in dummy mode):

| Index | Field | Description |
|---|---|---|
| `0` | Timestamp | Elapsed flight time (ms) |
| `1` | Altitude | Relative altitude (meters) |
| `2` | Free Fall | Free fall indicator (`0` = No, `1` = Yes) |
| `3` | Temperature | Temperature (°C) |
| `4` | Pressure | Barometric pressure (hPa) |
| `5` | Gyro Pitch | Angular pitch rate (°/s) |
| `6` | Gyro Roll | Angular roll rate (°/s) |
| `7` | Gyro Yaw | Angular yaw rate (°/s) |
| `8` | Accel X | X-axis acceleration (m/s²) |
| `9` | Accel Y | Y-axis acceleration (m/s²) |
| `10` | Accel Z | Z-axis acceleration (m/s²) |
| `11` | Battery | Battery charge % (dummy mode only, optional on hardware) |

> **Dummy mode** runs a realistic sub-orbital flight simulator: motor burn,
> ballistic coast to apogee (weightlessness / free fall), terminal-velocity
> descent, parachute recovery and a slowly draining battery. The elapsed-time
> clock advances 1:1 with real wall-clock time. While you hold a plot panel
> with the mouse to pan/zoom, the trace is paused and snaps back to the live
> position when you release the button.

Data can be saved to `flight_data.csv` in real-time by clicking **Start storage** on the GUI.

---

## 🧪 Testing

This is a development tool that keeps evolving, so the telemetry pipeline is
covered by unit tests. Run the full suite (headless, no display needed):

```bash
uv run pytest
```

Run a single area:

```bash
uv run pytest tests/test_communication.py
uv run pytest -k "battery or free_fall"
```

Every run prints a coverage report for `communication`, `dataBase`,
`graphs` and `main`. See [`docs/TESTING.md`](docs/TESTING.md) for the test
layout, conventions, and a guide on adding new tests.

---

## 📦 Stack & Compatibility

- **Package Manager**: [`uv`](https://astral-sh.github.io/uv/)
- **Python**: `>=3.10`
- **UI Framework**: PyQt6 / PyQt5 (`pyqtgraph`)
- **Hardware Interface**: `pyserial`
- **Math & Data**: `numpy`

---

## 📜 License

[MIT License](LICENSE).

Developed by **Daniel Alejandro Rodríguez Suárez**, Leader of the ATL Research Seedbed, linked to the **LIDER Research Group** at Universidad Distrital Francisco José de Caldas.
