# LoPy Window Detection

This project uses LoPy4 and ultrasonic sensors to detect the opening and closing of windows. The state of the window is then published to ThingSpeak using MQTT. Note that for Tilt and Turn windows, all states work but 2 sensors are required.

## Table of Contents

- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
- [License](#license)

## Requirements

You need a LoPy4 with MQTT capabilites.

## Installation

1. Clone this repository to your local machine.
2. Install the necessary dependencies:
    - Pycom firmware for LoPy4
    - MQTT library for Python
3. Set up your ThingSpeak account and get your MQTT credentials.
4. Update the `main.py` file with your WiFi and ThingSpeak credentials.

## Usage

Connect the ultrasonic sensors to your LoPy4 device. The number of sensors and their pin numbers should be specified in the `main.py` file.
Upload all the project files to you LoPy


## License

This project is licensed under the MIT License.