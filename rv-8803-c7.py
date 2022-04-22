# import the needed packages
import smbus
import datetime
import sys
import os

ARG_COUNT = 2
ARG_EXE = 0
ARG_SWITCH = 1
ARG_MESSAGE = 2

# create a varible to handle the bus
bus = smbus.SMBus(1)
# the address for RTC
address = 0x32

def bcd_2_int(value):
	return (value & 0x0f) + (value >> 4) * 10

def int_2_bcd(value):
	return ((value // 10) << 4) + (value % 10)

if len(sys.argv) < ARG_COUNT:
	print(sys.argv[ARG_EXE] + "[-I][-G]")
	print("-I - Initialize rv-8803 from utc system clock")
	print("-G - Read the RTC")
else:
	# process command line arguments.
	if sys.argv[ARG_SWITCH][1] ==  "I":
		# datetime variables
		now = datetime.datetime.utcnow()
		year = int_2_bcd(now.year - 2000)
		month = int_2_bcd(now.month)
		day = int_2_bcd(now.day)
		hour = int_2_bcd(now.hour)
		minute = int_2_bcd(now.minute)
		second = int_2_bcd(now.second)

		# write datetime to RTC registers
		data = bus.write_byte_data(address,0,second)
		data = bus.write_byte_data(address,1,minute)
		data = bus.write_byte_data(address,2,hour)
		data = bus.write_byte_data(address,4,day)
		data = bus.write_byte_data(address,5,month)
		data = bus.write_byte_data(address,6,year)
		print("Date written to RTC")

	elif sys.argv[ARG_SWITCH][1] == 'G':
		second = bus.read_byte_data(address,0)
		minute = bus.read_byte_data(address,1)
		hour = bus.read_byte_data(address,2)
		day = bus.read_byte_data(address,4)
		month = bus.read_byte_data(address,5)
		year = bus.read_byte_data(address,6)
		print("{:02d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(2000 + bcd_2_int(year), bcd_2_int(month), bcd_2_int(day), bcd_2_int(hour), bcd_2_int(minute), bcd_2_int(second)))
	else:
		print("Not a valid arguement. -I or -G")
