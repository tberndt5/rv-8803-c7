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

# int to bcd.
def int_2_bcd(value):
	bcd = {
		0:0x00,
		1:0x01,
		2:0x02,
		3:0x03,
		4:0x04,
		5:0x05,
		6:0x06,
		7:0x07,
		8:0x08,
		9:0x09,
		10:0x10,
		11:0x11,
		12:0x12,
		13:0x13,
		14:0x14,
		15:0x15,
		16:0x16,
		17:0x17,
		18:0x18,
		19:0x19,
		20:0x20,
		21:0x21,
		22:0x22,
		23:0x23,
		24:0x24,
		25:0x25,
		26:0x26,
		27:0x27,
		28:0x28,
		29:0x29,
		30:0x30,
		31:0x31,
		32:0x32,
		33:0x33,
		34:0x34,
		35:0x35,
		36:0x36,
		37:0x37,
		38:0x38,
		39:0x39,
		40:0x40,
		41:0x41,
		42:0x42,
		43:0x43,
		44:0x44,
		45:0x45,
		46:0x46,
		47:0x47,
		48:0x48,
		49:0x49,
		50:0x50,
		51:0x51,
		52:0x52,
		53:0x53,
 		54:0x54,
		55:0x55,
		56:0x56,
		57:0x57,
		58:0x58,
		59:0x59,
		60:0x60,
		61:0x61,
		62:0x62,
		63:0x63,
		64:0x64,
		65:0x65,
		66:0x66,
		67:0x67,
		68:0x68,
		69:0x69,
		70:0x70,
		71:0x71,
		72:0x72,
		73:0x73,
		74:0x74,
		75:0x75,
		76:0x76,
		77:0x77,
		78:0x78,
		79:0x79,
		80:0x80,
		81:0x81,
		82:0x82,
		83:0x83,
		84:0x84,
		85:0x85,
		86:0x86,
		87:0x87,
		88:0x88,
		89:0x89,
		90:0x90,
		91:0x91,
		92:0x92,
		93:0x93,
		94:0x94,
		95:0x95,
		96:0x96,
		97:0x97,
		98:0x98,
		99:0x99
	}
	#return the bcd value
	return bcd.get(value,"Invalid")

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
		print("{}-{}-{} {}:{}:{}".format(hex(year),hex(month),hex(day),hex(hour),hex(minute),hex(second)))
	else:
		print("Not a valid arguement. -I or -G")
