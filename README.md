# 🌱 Smart Plant Watering System

> **Version:** 1.0  
> **Author:** **S4bt**  
> **Website:** [SharkByte](https://s4bt.de)
> **Status:** 🚧 In Development

---

## 📑 Table of Contents

- [Project Overview](#-project-overview)
- [Objectives](#-objectives)
- [Learning Goals](#-learning-goals)
- [System Architecture](#-system-architecture)
- [Hardware Components](#-hardware-components)
- [Actuators](#-actuators)
- [Wiring Guide](#-wiring-guide)
- [Software Workflow](#-software-workflow)
- [Sensor Calibration](#-sensor-calibration)
- [User Interface](#-user-interface)
- [Watering Logic](#-watering-logic)
- [Safety Features](#-safety-features)
- [Future Roadmap](#-future-roadmap)
- [Bill of Materials](#-bill-of-materials)
- [Project Milestones](#-project-milestones)
- [Success Criteria](#-success-criteria)
- [Future Expansion](#-future-expansion)

---

# 🌿 Project Overview

## 🎯 Goal

Design and build an autonomous **ESP32-powered Smart Plant Watering System** capable of monitoring soil moisture and watering plants only when necessary.

The system is designed to minimize water usage while keeping plants healthy through intelligent automation.

### Key Features

- 🌱 Continuous soil moisture monitoring
- 💧 Automatic watering when soil becomes dry
- 🚫 Overwatering prevention
- 📺 OLED status display
- 🔌 Modular design for future expansion
- 📶 Wi-Fi ready (future version)

---

# 🎯 Objectives

## Functional Requirements

| Feature                | Status |
| ---------------------- | :----: |
| Measure soil moisture  |   ✅   |
| Automatic watering     |   🔜   |
| Display moisture level |   🔜   |
| Empty tank detection   |   🔜   |
| Watering history       |   🔜   |
| Remote monitoring      |   🔜   |

---

# 📚 Learning Goals

This project introduces several core embedded systems concepts:

- Embedded Programming (ESP32)
- Analog-to-Digital Conversion (ADC)
- Digital Outputs
- Sensor Integration
- Electronics Fundamentals
- Power Management
- Automation Logic
- Basic Robotics Concepts
- Modular System Design

---

# 🏗️ System Architecture

```text
                    Water Reservoir
                          │
                          ▼
                  Mini Water Pump
                          │
                    Silicone Tube
                          │
                          ▼
                     Plant Pot
                          ▲
                          │
          Capacitive Soil Moisture Sensor
                          │
                          ▼
                      ESP32 Controller
                 ┌─────────────────────┐
                 │ Decision Algorithm  │
                 └─────────────────────┘
                    │            │
                    ▼            ▼
              OLED Display   MOSFET Driver
```

---

# 🔧 Hardware Components

## 🧠 Microcontroller

### ESP32 Development Board

| Feature       | Benefit             |
| ------------- | ------------------- |
| Wi-Fi         | Remote monitoring   |
| Bluetooth     | Mobile connectivity |
| Dual Core CPU | Fast processing     |
| ADC Inputs    | Sensor support      |
| Low Cost      | Budget friendly     |

---

## 🌱 Sensors

### Capacitive Soil Moisture Sensor

Measures soil moisture using electrical capacitance instead of exposed probes.

### Advantages

- ✔ Does not corrode
- ✔ Accurate readings
- ✔ Long lifespan
- ✔ Low maintenance

---

### 🌡️ BME280 _(Optional)_

Measures:

- Temperature
- Humidity
- Atmospheric Pressure

Useful for monitoring environmental conditions.

---

### 💧 Water Level Sensor

Monitors the remaining water inside the reservoir.

Benefits:

- Prevents dry pump operation
- Enables low-water warnings
- Protects hardware

---

# ⚙️ Actuators

## Mini Water Pump

**Type:** 5V Submersible Pump

Purpose:

Transfers water from the tank to the plant.

---

## MOSFET Driver Module

Safely switches the pump using the ESP32.

> ⚠ **Important:** Never connect the pump directly to an ESP32 GPIO pin.

---

# 🔌 Wiring Guide

## Soil Moisture Sensor

| Pin | ESP32  |
| --- | ------ |
| VCC | 3.3V   |
| GND | GND    |
| AO  | GPIO34 |

---

## OLED Display (I²C)

| OLED Pin | ESP32  |
| -------- | ------ |
| VCC      | 3.3V   |
| GND      | GND    |
| SDA      | GPIO21 |
| SCL      | GPIO22 |

---

## Pump Circuit

```text
ESP32 GPIO
     │
     ▼
 MOSFET Gate
     │
MOSFET Module
     │
     ▼
5V Pump
     │
External Power Supply
```

---

# 💻 Software Workflow

```text
Start
 │
 ▼
Initialize Hardware
 │
 ▼
Read Moisture Sensor
 │
 ▼
Is Moisture < Threshold?
 ├───────────────┐
 │               │
 │ No            │ Yes
 ▼               ▼
Wait         Activate Pump
 │               │
 ▼               ▼
Read Again   Pump OFF
                 │
                 ▼
          Wait 30 Minutes
                 │
                 ▼
              Repeat
```

---

# 🌱 Sensor Calibration

Each moisture sensor has slightly different readings.

Example values:

| Soil Condition | ADC Reading |
| -------------- | ----------: |
| Dry Soil       |        3200 |
| Wet Soil       |        1500 |

Convert readings into a percentage:

```text
0%   = Completely Dry

100% = Fully Wet
```

---

# 📺 User Interface

Example OLED display:

```text
╔════════════════════╗
║ 🌱 Plant Monitor   ║
║                    ║
║ Moisture: 67%      ║
║ Pump: OFF          ║
║ Temp: 22°C         ║
║ Humidity: 48%      ║
╚════════════════════╝
```

---

# 💧 Automatic Watering Logic

### Decision Rule

```text
IF Moisture < 30%

THEN

Pump ON
```

Pump runtime:

```text
3 seconds
```

Cooldown period:

```text
30 minutes
```

Then measure moisture again.

---

# 🛡️ Safety Features

The system includes multiple safeguards:

- ⏱ Maximum pump runtime
- 💧 Empty tank detection
- 📉 Sensor failure detection
- ❄ Pump cooldown period
- 🔘 Manual override button
- ⚡ External power isolation
- 🔌 Safe MOSFET switching

---

# 🚀 Future Roadmap

## Version 1

### Information

- Soil moisture sensor
- Display for moisture information
- Manual watering remains required

---

## Version 2

### Automation Improvements

- Smarter watering algorithm
- Adjustable moisture thresholds
- Better calibration

---

## Version 3

### IoT Features

- Wi-Fi dashboard
- Phone notifications
- Live monitoring
- OTA firmware updates
- Cloud data logging

---

## Version 4

### Multi-Plant Support

- Multiple sensors
- Multiple pumps
- Independent watering schedules
- Zone management

---

## Version 5

### Machine Vision

Using an ESP32-CAM or Raspberry Pi camera:

- 🍃 Leaf color analysis
- 📈 Growth tracking
- 🦠 Disease detection
- 🌿 Wilting detection
- 🤖 AI-based watering decisions

---

# 💰 Bill of Materials

| Component                  |    Qty | Price |
| -------------------------- | -----: | ----: |
| ESP32 Development Board    |      1 |    $6 |
| Capacitive Moisture Sensor |      1 |    $5 |
| Breadboard                 |      1 |    $6 |
| Jumper Wires               | 1 Pack |    $4 |
| OLED Display               |      1 |    $5 |
| MOSFET Module              |      1 |    $3 |
| Mini Water Pump            |      1 |    $8 |
| Silicone Tubing            |      1 |    $2 |
| 5V Power Supply            |      1 |    $8 |

---

## Estimated Total

|      Cost |
| --------: |
| **≈ $47** |

---

# 📅 Project Milestones

## Phase 1 — Sensor Integration

- [ ] Read soil moisture
- [ ] Display sensor values
- [ ] Calibrate readings

---

## Phase 2 — Pump Control

- [ ] Connect MOSFET
- [ ] Drive pump safely
- [ ] Test watering cycle

---

## Phase 3 — User Interface

- [ ] OLED integration
- [ ] Display live status
- [ ] Add safety logic

---

## Phase 4 — Smart Features

- [ ] Wi-Fi dashboard
- [ ] Notifications
- [ ] Data logging
- [ ] OTA updates

---

# ✅ Success Criteria

The project is considered complete when:

- [x] Soil moisture is measured accurately.
- [x] Watering occurs automatically when needed.
- [x] Overwatering is prevented.
- [x] OLED displays live system information.
- [x] The system can operate unattended for several days.
- [x] The design is modular and expandable.

---

# 📈 Future Expansion

Potential upgrades include:

- 📦 Custom 3D-printed enclosure
- 🔋 Solar-powered operation
- 📊 Grafana dashboard
- ☁ MQTT integration
- 📱 Mobile application
- 📈 Historical moisture graphs
- 🤖 AI watering recommendations
- 🌍 Home Assistant integration
- 🔄 OTA firmware updates
- 🧪 Automated diagnostics

---

# 📜 License

This project is released under the **MIT License**.

Feel free to use, modify, and distribute it with attribution.

---

<div align="center">

# 🌱 Smart Plant Watering System

**Built with ESP32 • Designed for Automation • Ready for IoT**

⭐ _If you found this project useful, consider starring the repository on GitHub._

</div>
