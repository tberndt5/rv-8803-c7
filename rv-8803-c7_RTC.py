# rv8803.py
# A Python library for interacting with the RV-8803-C7 RTC via I2C.
# Author: Tyler Berndt

import smbus2
import datetime
import sys

# RV-8803-C7 I2C Address
_RV8803_ADDRESS = 0x32

# RV-8803-C7 Register Addresses
_REG_SECONDS = 0x00
_REG_MINUTES = 0x01
_REG_HOURS = 0x02
_REG_WEEKDAY = 0x03
_REG_DAY = 0x04
_REG_MONTH = 0x05
_REG_YEAR = 0x06


class RV8803:
    # --- A class to manage the RV-8803-C7 real-time clock. ---
    def __init__(self, i2c_bus_number=1):
        # --- Initializes the RV8803 object. ---
        # :param i2c_bus_number: The I2C bus number (default is 1 for Raspberry Pi).
        try:
            self.bus = smbus2.SMBus(i2c_bus_number)
        except FileNotFoundError:
            raise RuntimeError(
                "I2C bus not found. Ensure I2C is enabled on your system."
            )

    def _bcd_to_int(self, bcd_value):
        # --- Converts a Binary-Coded Decimal (BCD) value to an integer. ---
        # :param bcd_value: The BCD value to convert.
        # :return: The integer representation.
        return (bcd_value & 0x0F) + ((bcd_value >> 4) * 10)

    def _int_to_bcd(self, int_value):
        # --- Converts an integer to a Binary-Coded Decimal (BCD) value. ---
        # :param int_value: The integer to convert.
        # :return: The BCD representation.
        return ((int_value // 10) << 4) + (int_value % 10)

    def get_time(self):
        # --- Reads the current date and time from the RTC. ---
        # :return: A datetime.datetime object representing the current RTC time.
        try:
            # --- Read time registers in a single block for atomicity ---
            time_data = self.bus.read_i2c_block_data(
                _RV8803_ADDRESS, _REG_SECONDS, 7
            )

            second = self._bcd_to_int(time_data[0] & 0x7F)
            minute = self._bcd_to_int(time_data[1] & 0x7F)
            hour = self._bcd_to_int(time_data[2] & 0x3F)  # 24-hour format
            day = self._bcd_to_int(time_data[4] & 0x3F)
            month = self._bcd_to_int(time_data[5] & 0x1F)
            # Year is offset from 2000
            year = self._bcd_to_int(time_data[6]) + 2000

            return datetime.datetime(year, month, day, hour, minute, second)
        except IOError:
            raise RuntimeError(
                "Failed to read from RV-8803. Check connection."
            )

    def set_time(self, dt_object):
        # --- Sets the RTC time from a datetime object. ---
        # :param dt_object: A datetime.datetime object to set the time to.
	    
        second = self._int_to_bcd(dt_object.second)
        minute = self._int_to_bcd(dt_object.minute)
        hour = self._int_to_bcd(dt_object.hour)
        weekday = self._int_to_bcd(dt_object.isoweekday() % 7)  # 0=Sun
        day = self._int_to_bcd(dt_object.day)
        month = self._int_to_bcd(dt_object.month)
        year = self._int_to_bcd(dt_object.year - 2000)

        try:
            self.bus.write_byte_data(_RV8803_ADDRESS, _REG_SECONDS, second)
            self.bus.write_byte_data(_RV8803_ADDRESS, _REG_MINUTES, minute)
            self.bus.write_byte_data(_RV8803_ADDRESS, _REG_HOURS, hour)
            self.bus.write_byte_data(_RV8803_ADDRESS, _REG_WEEKDAY, weekday)
            self.bus.write_byte_data(_RV8803_ADDRESS, _REG_DAY, day)
            self.bus.write_byte_data(_RV8803_ADDRESS, _REG_MONTH, month)
            self.bus.write_byte_data(_RV8803_ADDRESS, _REG_YEAR, year)
        except IOError:
            raise RuntimeError("Failed to write to RV-8803. Check connection.")

    def set_time_from_system(self):
        # --- Sets the RTC time using the system's current UTC time. ---
        now_utc = datetime.datetime.utcnow()
        self.set_time(now_utc)

def main():
    # --- Main function to run the script from the command line for quick setup. ---
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} [-I | -G]")
        print("  -I : Initialize RTC from system's UTC clock.")
        print("  -G : Get and display the current time from the RTC.")
        sys.exit(1)

    try:
        rtc = RV8803()
        arg = sys.argv[1].upper()

        if arg == "-I":
            print("Initializing RTC from system UTC time...")
            rtc.set_time_from_system()
            print("RTC time has been set successfully.")
            current_time = rtc.get_time()
            print(f"Current RTC time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

        elif arg == "-G":
            print("Reading time from RTC...")
            current_time = rtc.get_time()
            print(f"Current RTC time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

        else:
            print(f"Error: Invalid argument '{sys.argv[1]}'. Use -I or -G.")
            sys.exit(1)

    except (RuntimeError, IOError) as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

