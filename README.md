# GPS Module Validation

## Objective
To verify that the GPS module is powered correctly, connected through a USB-TTL converter, and able to output valid GPS/NMEA data.

## Module Information
- Module: NEO-6M GPS Module
- Interface: UART
- Test Method: USB-TTL serial reading


## Hardware Used
- GPS module
- USB-TTL converter
- Jumper wires
- Host computer / Jetson board

## Wiring
Connections used:
- GPS VCC -> USB-TTL 3.3V or 5V
- GPS GND -> USB-TTL GND
- GPS TX -> USB-TTL RX

Note:
- GPS RX was not connected because only data reading was required.
- Common ground was used.

## Connection Diagram
![Connection Diagram](docs/connection-diagram.png)

## Software / Tools Used
- Python 3
- pyserial
- Serial terminal / minicom / screen
- OS: Ubuntu / Windows

## Test Procedure
1. Connected the GPS module to the USB-TTL converter.
2. Verified power and ground wiring.
3. Connected module TX to converter RX.
4. Opened serial port at the required baud rate.
5. Read incoming NMEA messages from the GPS module.
6. Logged sample output for validation.

## Sample Command
```bash
python3 scripts/read_gps.py
