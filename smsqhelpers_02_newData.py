# --- HOWTO

# smsqhelpers_02_newData is a helpers script to load raw tracking data to a PostGIS database to then join pixelvalues with georeferences world coordinates, and then create linestrings from raw data

# usage:
# smsqhelpers_02_newData.py [tracking-rawdata] [camname] [timestamp] [videopart]

# e. g.:
# smsqhelpers_02_newData.py "tracks_01.txt" 'designOffices' '20180314_0800_1000' '1'

# --- GOOD TO KNOW

# double check useage of quotes for args definition

# --- used modules

import sys

import psycopg2
from psycopg2.extras import RealDictCursor, wait_select

from datetime import datetime  # stat
# --- help

if(len(sys.argv) <= 1):
	print('# --- HOWTO')
	print('\n# smsqhelpers_02_newData is a helpers script to load raw tracking data to a PostGIS database to then join pixelvalues with georeferences world coordinates, and then create linestrings from raw data')
	print('\n# usage:')
	print('# smsqhelpers_02_newData.py [tracking-rawdata] [camname] [timestamp] [videopart]')
	print('\n# e. g.:')
	print("""# smsqhelpers_02_newData.py "tracks_01.txt" 'designOffices' '20180314_0800_1000' '1'""")
	print('\n# --- GOOD TO KNOW')
	print('\n# double check useage of quotes for args definition')

# --- init

else:
	# connection to database
	connection = 'host=localhost port=5432 dbname=smsq user=postgres password=postgres'
	# pathname
	path = "C:/CSL/geoDetections/"

	# args via console
	tracks = str(sys.argv[1])  # tracks_[].txt

	cam = sys.argv[2]  # camname
	ts = sys.argv[3]  # timestamp
	vp = sys.argv[4]  # videopart

	# --- startmessage

	print('\n\n\n%%%%%%%%%%%')
	print('\nSmartSquare-Helpers-Script')
	print('\n%%%%%%%%%%%')
	print("\n\n\nYou're going to add data to a existing database now.\nMake sure you're aware of what you're doing.\nAnd don't mess it up.\n\n")

	# --- check

	print('\ntracks-file: ' + tracks)
	print('camname: ' + cam)
	print('timestamp: ' + ts)
	print('videopart: ' + vp)

	input("\n\n\nCheck for typos, etc.\nIf it's alright press Enter to continue.\n\n\n")

	# --- main

	# connect to database
	with psycopg2.connect(
		connection,
		cursor_factory=RealDictCursor
	) as dbconn:
		dbconn.autocommit = True  # so we do not need to conn.commit() every time... ;)
		
		# the wait_select callback can handle a Ctrl-C correctly (TODO: Deprecated...)
		# wait_select(dbconn)

		with dbconn.cursor() as cursor:

	# --- main - check for errors, etc.

			print('Debugging: Right time to add data?\nPlease wait while machine is asking...\n')
			start1 = datetime.now()  # stat

			with open(path + "debug_02.sql", 'r') as debug2:
				debug2_ = debug2.read()

			cursor.execute(debug2_)
			debug2res = cursor.fetchall()
			
			cursor.close()

		if debug2res[0]['count'] == 0:
			print('No problems identified. Will proceed now.')
			end1 = datetime.now()  # stat
			print(str(datetime.now()) + ' : This took you ' + str((end1-start1).seconds + 1) + ' second(s).\n\n')  # stat

	# --- main #6
	# --- load new tracking data to table

			with dbconn.cursor() as cursor:
				print('working on step 1/5...')
				start2 = datetime.now()  # stat

				with open(path + "sql_6.sql", 'r') as sql6:
					sql6_ = sql6.read().replace("STDIN", """'""" + path + tracks + """'""")

				cursor.execute(sql6_)
				end2 = datetime.now()  # stat
				print(str(datetime.now()) + ' : This took you ' + str((end2-start2).seconds + 1) + ' second(s).\n')  # stat
				
				cursor.close()

	# --- main #7 to #10

	#  7: add camname, timestamp, videopart to raw-data
	#  8: cross-reference tables to add x,y, then geometry
	#  9: create lines from point data
	# 10: drop invalid lines

			for i in range(7, 12):  # sql_7.sql to sql_11.sql  # TODO: get range from data
				with dbconn.cursor() as cursor:
					print('working on step ' + str(i-5) + '/6...')
					starti = datetime.now()  # stat

					with open(path + "sql_" + str(i) + ".sql", 'r') as sql:
						sql_ = sql.read().replace("STDIN1", cam).replace("STDIN2", ts).replace("STDIN3", eval(vp))  # TODO: ugly, especially eval()

					cursor.execute(sql_)
					endi = datetime.now()  # stat
					print(str(datetime.now()) + ' : This took you ' + str((endi-starti).seconds + 1) + ' second(s).\n')  # stat
					
					cursor.close()

	# # --- main - handle identified errors
		else:
			print("""There's still data to be processed, please check first.\n""")

	print('\n\nDone.\n\n')