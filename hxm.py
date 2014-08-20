#!/usr/bin/env python

import sys
import serial
import struct

ser = serial.Serial('/dev/tty.HXM011522-BluetoothSeri', 115200, timeout=1)

async = False
stx = struct.pack("<B", 0x02)
etx = struct.pack("<B", 0x02)
rate = struct.pack("<B", 0x26)
dlc_byte = struct.pack("<B", 55)
while True:
	d = ser.read()
	if d != stx:
		if not async:
			print >>sys.stderr, "Not synched"
			async = True
		continue
	async = False
	# 60 bytes total in message
	print "Found message"
	type = ser.read()	# Msg ID
	if type != rate:
		print >>sys.stderr, "Unknown message type"
	dlc = ser.read()	# DLC
	if dlc != dlc_byte:
		print >>sys.stderr, "Bad DLC"
	data = ser.read(2)	# Firmware ID
	fid, = struct.unpack("<H", data)
	#print "Firmware ID: 0x%02x" % fid
	data = ser.read(2)	# Firmware Version
	fiv, = struct.unpack("<2s", data)
	#print "Firmware Version: 0x%02x" % fiv
	data = ser.read(2)	# Hardware ID
	hid, = struct.unpack("<H", data)
	#print "Hardware ID: 0x%02x" % hid
	data = ser.read(2)	# Hardware Version
	hiv, = struct.unpack("<2s", data)
	#print "Hardware Version: 0x%02x" % hiv
	print "Firmware: 9500.%04d.V%2s" % (fid, fiv)
	print "Hardware: 9800.%04d.V%2s" % (hid, hiv)
	data = ser.read()	# Battery Charge Indicator
	byte, = struct.unpack("<B", data)
	print "Battery: %3d%%" % byte
	data = ser.read()	# Heart Rate
	byte, = struct.unpack("<B", data)
	print "Heart Rate: %3d bpm" % byte
	data = ser.read()	# Heart Beat Number
	byte, = struct.unpack("<B", data)
	print "Heart Beat Number: %d" % byte
	data = ser.read(2)	# Heart Beat Timestamp #1 (Newest)
	byte, = struct.unpack("<H", data)
	print "Heart Beat Timestamp #1 (Newest): %d ms" % byte
	for i in xrange(14):
		data = ser.read(2)	# Heart Beat Timestamp #x
		byte, = struct.unpack("<H", data)
		print "Heart Beat Timestamp #%d: %d ms" % (i+2, byte)
	data = ser.read(2)	# Reserved
	byte, = struct.unpack("<H", data)
	print "Reserved: %d" % byte
	data = ser.read(2)	# Reserved
	byte, = struct.unpack("<H", data)
	print "Reserved: %d" % byte
	data = ser.read(2)	# Reserved
	byte, = struct.unpack("<H", data)
	print "Reserved: %d" % byte
	data = ser.read(2)	# Distance
	byte, = struct.unpack("<H", data)
	print "Distance: %.3f m" % (float(byte)/16)
	data = ser.read(2)	# Instantaneous Speed
	byte, = struct.unpack("<H", data)
	print "Instantaneous Speed: %.3f m/s" % (float(byte)/256)
	data = ser.read()	# Strides
	byte, = struct.unpack("<B", data)
	print "Strides: %d" % byte
	data = ser.read()	# Reserved
	byte, = struct.unpack("<B", data)
	print "Reserved: %d" % byte
	data = ser.read(2)	# Reserved
	byte, = struct.unpack("<H", data)
	print "Reserved: %d" % byte
	data = ser.read()	# CRC
	byte, = struct.unpack("<B", data)
	print "CRC: %d" % byte
	end = ser.read()
	while end != etx:
		print "Extra"
		end = ser.read()
	#print struct.unpack("<B", d)
