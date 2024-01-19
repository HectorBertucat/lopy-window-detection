# LoPy Window Detection

This project uses LoPy4 and ultrasonic sensors to detect the opening and closing of windows. The state of the window is then published to ThingSpeak using MQTT. Note that for Tilt and Turn windows, all states work but 2 sensors are required.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Hardware Setup](#hard-setup)
- [Usage](#usage)
- [License](#license)

## Requirements

You need a Pycom. You also need a LoPy4 to be able to use the Wi-Fi for MQTT related features. You also need an ultrasound sensor (the one used for the prototype is a HC-SR04 model).

## Installation

1. Clone this repository to your local machine.
2. Install the necessary dependencies:
    - Pycom firmware for LoPy4
    - MQTT library for Python
3. Set up your ThingSpeak account and get your MQTT credentials.
4. Update the `main.py` file with your WiFi and ThingSpeak credentials.

## Hardware Setup<a name="hard-setup"/>

Here you can find 2 pictures showing the module used as a prototype to test out the features. It is made of a pycom as well as a LoPy4 module. Connected to the pycom is an HC-SR04 ultrasound sensor.

The first images shows how the sensor and the pycom are connected.
The second one shows an example of how to place a sensor to detect the opening of a sliding window.

<img src="https://github.com/HectorBertucat/lopy-window-detection/assets/47351005/04ddf002-cadc-49cb-a236-c1f2f4a5ea82" alt="pycom-ultrasound" width="300"/> <img src="https://github.com/HectorBertucat/lopy-window-detection/assets/47351005/e28fd631-acee-412a-9650-731243e4435f" alt="sensor-placing" width="300"/>

## Usage

Connect the ultrasonic sensors to your LoPy4 device. The number of sensors and their pin numbers should be specified in the `main.py` file.
Upload all the project files to you LoPy

## License

This project is licensed under the MIT License.
