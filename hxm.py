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
	len, = struct.unpack("<B", dlc)
	if len != 55:
		print >>sys.stderr, "Bad DLC"
	payload = ser.read(len)
	crc, = struct.unpack("<B", ser.read())
	end, = struct.unpack("<B", ser.read())
	sum = 0
	print "L: " + str(len)
	for i in xrange(len):
		b, = struct.unpack("<B", payload[i])
		#print "Data: 0x%02x" % b
		sum = (sum ^ b) & 0xff
		for j in xrange(8):
			if sum & 0x01:
				sum = (sum >> 1) ^ 0x8c
			else:
				sum = (sum >> 1)
	#print "CRC:  0x%02x" % crc
	if crc != sum:
		print >>sys.stderr, "Bad CRC: " + str(sum) + " is not " + str(crc)
	else:
		print "CRC validated!"
	if end != 0x03:
		print >>sys.stderr, "Bad ETX"
	fid, fiv, hid, hiv, batt, hr, hbn, hbts1, hbts2, hbts3, hbts4, hbts5, hbts6, hbts7, hbts8, hbts9, hbts10, hbts11, hbts12, hbts13, hbts14, hbts15, distance, speed, strides = struct.unpack("<H2sH2sBBB15H6xHHB3x", payload)
	print "Firmware: 9500.%04d.V%2s" % (fid, fiv)
	print "Hardware: 9800.%04d.V%2s" % (hid, hiv)
	print "Battery: %3d%%" % batt
	print "Heart Rate: %3d bpm" % hr
	print "Heart Beat Number: %d" % hbn
	print "Heart Beat Timestamp #1 (Newest): %d ms" % hbts1
	#for i in xrange(14):
	#	print "Heart Beat Timestamp #%d: %d ms" % (i+2, byte)
	print "Distance: %.3f m" % (float(distance)/16)
	print "Instantaneous Speed: %.3f m/s" % (float(speed)/256)
	print "Strides: %d" % strides
	continue
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
