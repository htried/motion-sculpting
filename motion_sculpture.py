import math
import csv
import rhinoscriptsyntax as rs

# Reading CSV
file = raw_input("Enter csv file to model")
b = raw_input("Enter bone to model movement of [#/all]")
pipe_bool = raw_input("Wire sculpture, solid-body, or point cloud? [w/s/p]")
if pipe_bool == 's':
	pipe_size = raw_input("Size of pipe? [1 - 10]")
else:
	pipe_size = 0

if b == "all":
	b = -1
else:
	b = int(b)

pipe_size = int(pipe_size)/100

input_csv = open(file, 'r')
csv_reader = csv.reader(input_csv)

row_count = sum(1 for row in input_csv)
row_count += 1
input_csv.seek(0)

final_arr = [[[0, 0, 0] for i in range(row_count)] for j in range(59)]

count = 0
start_bool = 1
for row in csv_reader:
	if count < 6 and start_bool == 1:
		count += 1
		continue

	start_bool = 0

	for i in range(0, 944, 16):
		bone = int(i / 16)
		
		final_arr[bone][count][0] = float(row[i])
		final_arr[bone][count][1] = float(row[i + 1])
		final_arr[bone][count][2] = float(row[i + 2])
		
		count += 1
		if count >= row_count:
			count = 0

# Actually processing data
threshold = .5; # min distance between two points in a curve
curveids = [0 for i in range(59)]  # the ids of the curves of each bone

if (b == -1):

	for bone in range(21): # for each bone
		linePoints = []
		lastFrame = 0
		for frame in range(0, row_count): # for each frame of this bone
			if final_arr[bone][frame][0] != 0.0 and final_arr[bone][frame][1] != 0.0 and final_arr[bone][frame][2] != 0.0: # do not consider values at origin
				if final_arr[bone][frame][2] != 0.0: # do not consider values with z = 0
					if lastFrame == 0 or rs.Distance(final_arr[bone][frame], final_arr[bone][lastFrame]) > threshold:
						if pipe_bool == 'p':
							rs.AddPoint(final_arr[bone][frame])
						else:
							linePoints.append(final_arr[bone][frame])
							lastFrame = frame
		if pipe_bool != 'p':
			curveids[bone] = rs.AddCurve(linePoints)
			if pipe_bool == 's':
				rs.AddPipe(curveids[bone], 0, pipe_size)

else:
	linePoints = []
	lastFrame = 0
	for frame in range(0, row_count): # for each frame of this bone
		if final_arr[b][frame][0] != 0.0 and final_arr[b][frame][1] != 0.0 and final_arr[b][frame][2] != 0.0: # do not consider values at origin
			if final_arr[b][frame][2] != 0.0: # do not consider values with z = 0
				if lastFrame == 0 or rs.Distance(final_arr[b][frame], final_arr[b][lastFrame]) > threshold:
					if pipe_bool == 'p':
						rs.AddPoint(final_arr[b][frame])
					else:
						linePoints.append(final_arr[b][frame])
						lastFrame = frame
	if pipe_bool != 'p':
		curveids[b] = rs.AddCurve(linePoints)
		if pipe_bool == 's':
			rs.AddPipe(curveids[b], 0, pipe_size)


