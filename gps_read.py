import serial
from datetime import datetime

PORT = "COM8"   # Change this to your COM port
BAUD = 9600     # Common baud rates: 9600, 38400


def nmea_to_decimal(value, direction):
    """
    Convert NMEA coordinate format to decimal degrees.
    Latitude:  ddmm.mmmm
    Longitude: dddmm.mmmm
    """
    if not value or not direction:
        return None

    try:
        raw = float(value)

        if direction in ("N", "S"):
            degrees = int(raw / 100)
            minutes = raw - (degrees * 100)
        elif direction in ("E", "W"):
            degrees = int(raw / 100)
            minutes = raw - (degrees * 100)
        else:
            return None

        decimal = degrees + (minutes / 60)

        if direction in ("S", "W"):
            decimal = -decimal

        return decimal
    except ValueError:
        return None


def parse_gga(parts):
    """
    Parse GGA sentence:
    $GPGGA,time,lat,N/S,lon,E/W,fix,sats,hdop,alt,M,...
    """
    if len(parts) < 10:
        return None

    lat = nmea_to_decimal(parts[2], parts[3])
    lon = nmea_to_decimal(parts[4], parts[5])

    return {
        "type": "GGA",
        "time_utc": parts[1],
        "latitude": lat,
        "longitude": lon,
        "fix_quality": parts[6],
        "satellites": parts[7],
        "hdop": parts[8],
        "altitude_m": parts[9],
    }


def parse_rmc(parts):
    """
    Parse RMC sentence:
    $GPRMC,time,status,lat,N/S,lon,E/W,speed,course,date,...
    """
    if len(parts) < 10:
        return None

    lat = nmea_to_decimal(parts[3], parts[4])
    lon = nmea_to_decimal(parts[5], parts[6])

    return {
        "type": "RMC",
        "time_utc": parts[1],
        "status": parts[2],   # A = valid, V = invalid
        "latitude": lat,
        "longitude": lon,
        "speed_knots": parts[7],
        "course": parts[8],
        "date": parts[9],
    }


def pretty_print(data):
    if not data:
        return

    print("\nParsed Data")
    print("-" * 40)

    if data["type"] == "GGA":
        print(f"Sentence Type : {data['type']}")
        print(f"UTC Time      : {data['time_utc']}")
        print(f"Latitude      : {data['latitude']}")
        print(f"Longitude     : {data['longitude']}")
        print(f"Fix Quality   : {data['fix_quality']}")
        print(f"Satellites    : {data['satellites']}")
        print(f"HDOP          : {data['hdop']}")
        print(f"Altitude (m)  : {data['altitude_m']}")

    elif data["type"] == "RMC":
        print(f"Sentence Type : {data['type']}")
        print(f"UTC Time      : {data['time_utc']}")
        print(f"Status        : {data['status']}")
        print(f"Latitude      : {data['latitude']}")
        print(f"Longitude     : {data['longitude']}")
        print(f"Speed (knots) : {data['speed_knots']}")
        print(f"Course        : {data['course']}")
        print(f"Date          : {data['date']}")

    print("-" * 40)


def main():
    print(f"Opening {PORT} at {BAUD} baud...")
    print("Waiting for GPS data... Press Ctrl+C to stop.\n")

    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
    except Exception as e:
        print(f"Could not open port {PORT}: {e}")
        return

    try:
        while True:
            raw_line = ser.readline()

            if not raw_line:
                continue

            line = raw_line.decode("ascii", errors="ignore").strip()

            if not line.startswith("$"):
                continue

            print(f"RAW: {line}")

            parts = line.split(",")

            parsed = None
            if parts[0] in ("$GPGGA", "$GNGGA"):
                parsed = parse_gga(parts)
            elif parts[0] in ("$GPRMC", "$GNRMC"):
                parsed = parse_rmc(parts)

            if parsed:
                pretty_print(parsed)

    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        ser.close()
        print("Serial port closed.")


if __name__ == "__main__":
    main()