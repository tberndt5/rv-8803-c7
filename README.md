# Python Library for RV-8803-C7 RTC

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.6+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Platform-Linux-yellow.svg" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

A simple and robust Python library for interfacing with the Micro Crystal **RV-8803-C7** real-time clock (RTC) module over I2C on Linux-based systems like the Raspberry Pi.

This library allows you to easily get and set the time, making it perfect for data logging, scheduling, and any project that requires accurate, persistent timekeeping.

---

## ✨ Features

-   **Object-Oriented**: Clean, class-based interface.
-   **Get Time**: Read the current date and time from the RTC as a standard Python `datetime` object.
-   **Set Time**: Set the RTC time using either a `datetime` object or the system's current UTC time.
-   **Command-Line Utility**: Can be run as a standalone script for quick initialization and time checks.
-   **Robust Error Handling**: Provides clear error messages for common issues like I2C connection failures.

---

## 🚀 Getting Started

### Prerequisites

-   A Linux-based single-board computer (e.g., Raspberry Pi) with I2C enabled.
-   Python 3.6 or newer.
-   The RV-8803-C7 module wired correctly to your board's I2C pins.

### Dependencies

This library requires the `smbus2` package. You can install it using pip:

```sh
pip install smbus2
```

### Installation

Clone this repository or download the `rv-8803-c7_RTC.py` file into your project directory.

```sh
git clone https://github.com/tberndt5/rv-8803-c7.git
cd rv8803-c7
```

---

## ⚙️ Usage

### As a Library

Import the `RV8803` class into your Python script to interact with the RTC module.

```python
import time
from rv8803 import RV8803

try:
    # Initialize the RTC object
    rtc = RV8803()

    # Set the time on the RTC from the system's UTC clock
    print("Setting RTC time from system clock...")
    rtc.set_time_from_system()
    print("RTC time set.")

    time.sleep(2) # Wait a couple of seconds

    # Get the current time from the RTC
    current_time = rtc.get_time()
    print(f"The current time on the RTC is: {current_time}")
    print(f"The year is: {current_time.year}")
    print(f"The hour is: {current_time.hour}")

except (RuntimeError, IOError) as e:
    print(f"An error occurred: {e}")

```

### As a Standalone Script

You can also run the file directly from the command line to quickly set or get the time without writing a separate script.

#### Set the RTC Time

To initialize the RTC with your system's current UTC time:

```sh
python rv8803.py -I
```

#### Get the RTC Time

To read the current time from the RTC and print it to the console:

```sh
python rv8803.py -G
```

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
