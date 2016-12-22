import sys
import os
from datetime import datetime

subfile = open(sys.argv[1], "r").readlines()
videofile = sys.argv[2]
outputdir = sys.argv[3]

time_start = ''
frames = 0
sub = ''
framerate = 30
frame_str = ''

has_time = False
has_frame = False

try:
	for line in subfile:
		#print line
		if '-->' in line:
			word = line.split()
			time_start = word[0].replace(',','.')
			time_stop = word[2].replace(',','.')
			FMT = '%H:%M:%S.%f'
			#print time_start + " " + time_stop
			tdelta = datetime.strptime(time_stop, FMT) - datetime.strptime(time_start, FMT)
			ns =  tdelta.microseconds
			if ns < 1000000:
				ns = 1000000
			frames = ns / (1000000/framerate)
			has_time = True
			#print frames
			#line[:-2] remove endofline chars
			#print "time"
			print line
		else:
			#newline = line[:-2]
			newline = line.strip()
			if newline.isdigit():			
				if has_time and has_frame: 
					cmd_string = "ffmpeg -hide_banner -loglevel panic -i "+videofile+" -vframes "+str(frames)+" -ss "+time_start+" ./temp\\%03d.png"
					#print cmd_string
					os.system(cmd_string)
					for x in range(1, frames+1):
						# add subtitle
						cmd_string = "convert ./temp"+ "%03d" % (x) +".png -pointsize 40 -gravity south -stroke '#000C' -strokewidth 2 -draw \"text 0,0 '"+sub+"'\" -stroke none -fill white -draw \"text 0,0 '"+sub+"'\" ./temp"+ "%03d" % (x) +".png"
						#print cmd_string
						os.system(cmd_string)
					# generate gif
					cmd_string = "convert -delay "+str(120/framerate)+" -loop 0 temp*.png "+frame_str+".gif"
					#print cmd_string
					os.system(cmd_string)
					# remove temp files
					cmd_string = "rm ./temp*.png"
					#print cmd_string
					os.system(cmd_string)
					sub = ''
					has_time = False
					has_frame = False			
				frame_str = "%04d"%int(line)
				has_frame = True
				#print "frame"
			else:
				if newline != '':
					newline = newline.replace("<i>","")
					newline = newline.replace("</i>","")
					newline = newline.replace("'","\\'")
					sub = sub + newline + '\n'
					#print "sub"
except KeyboardInterrupt:
	print "User interrupted"

if has_time and has_frame: 
	cmd_string = "ffmpeg -hide_banner -loglevel panic -i "+videofile+" -vframes "+str(frames)+" -ss "+time_start+" ./temp\\%03d.png"
	#print cmd_string
	os.system(cmd_string)
	for x in range(1, frames+1):
		# add subtitle
		cmd_string = "convert ./temp"+ "%03d" % (x) +".png -pointsize 40 -gravity south -stroke '#000C' -strokewidth 2 -draw \"text 0,0 '"+sub+"'\" -stroke none -fill white -draw \"text 0,0 '"+sub+"'\" ./temp"+ "%03d" % (x) +".png"
		#print cmd_string
		os.system(cmd_string)
	# generate gif
	cmd_string = "convert -delay 35 -loop 0 temp*.png "+frame_str+".gif"
	#print cmd_string
	os.system(cmd_string)
	# remove temp files
	cmd_string = "rm ./temp*.png"
	#print cmd_string
	os.system(cmd_string)
	sub = ''
	has_time = False
	has_frame = False
