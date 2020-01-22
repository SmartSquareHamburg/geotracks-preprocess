# --- HOWTO

# smsqhelpers_01_newReference is a helpers script to load the georeference's result into a PostGIS database to then join this with raw tracking data

# usage:
# smsqhelpers_01_newReference.py [georeference-result] [camname] [timestamp]

# e. g.:
# smsqhelpers_01_newReference.py tps_result.csv 'designOffices' '20180314_0800_1000'

# --- GOOD TO KNOW

# use single quotes for args definition

# --- used modules

import sys

import psycopg2
from psycopg2.extras import RealDictCursor

from datetime import datetime  # stat

# --- help

if(len(sys.argv) <= 1):
	print('# --- HOWTO')
	print("\n# smsqhelpers_01_newReference is a helpers script to load the georeference's result into a PostGIS database to then join this with raw tracking data")
	print('\n# usage:')
	print('# smsqhelpers_01_newReference.py [georeference-result] [camname] [timestamp]')
	print('\n# e. g.:')
	print("# smsqhelpers_01_newReference.py tps_result.csv 'designOffices' '20180314_0800_1000'")
	print('\n# --- GOOD TO KNOW')
	print('\n# use single quotes for args definition')

# --- init

else:
	# connection to database
	connection = 'host=localhost port=5432 dbname=smsq user=postgres password=postgres'
	# pathname
	path = "C:/CSL/geoDetections/"

	# args via console
	targets = str(sys.argv[1])

	cam = sys.argv[2]  #  camname
	ts = sys.argv[3]  # timestamp

	# --- startmessage

	print('\n\n\n%%%%%%%%%%%')
	print('\nSmartSquare-Helpers-Script')
	print('\n%%%%%%%%%%%')
	print("\n\n\nYou're going to add data to a existing database now.\nMake sure you're aware of what you're doing.\nAnd don't mess it up.\n\n")

	# --- check

	print('\ntarget-file: ' + targets)
	print('camname: ' + cam)
	print('timestamp: ' + ts)

	input("\n\n\nCheck for typos, etc.\nIf it's alright press Enter to continue.\n\n\n")

	# --- main

	# connect to database
	with psycopg2.connect(
		connection,
		cursor_factory=RealDictCursor
	) as dbconn:
		dbconn.autocommit = True  # so we do not need to conn.commit() every time... ;)
		with dbconn.cursor() as cursor:

	# --- main - check for errors, etc.

			print('Debugging: Right time to add new reference?\nPlease wait while machine is asking...\n')
			start1 = datetime.now()  # stat

			with open(path + "debug_01.sql", 'r') as debug1:
				debug1_ = debug1.read()

			cursor.execute(debug1_)
			
			debug1res = cursor.fetchall()

			if debug1res[0]['count'] == 0:
				print('No problems identified. Will proceed now.')
				end1 = datetime.now()  # stat
				print(str(datetime.now()) + ' : This took you ' + str((end1-start1).seconds + 1) + ' second(s).\n\n')  # stat

	# --- main #1
	# --- load new target data to table

				print('working on step 1/2...')
				start2 = datetime.now()  # stat

				with open(path + "sql_1.sql", 'r') as sql1:
					sql1_ = sql1.read().replace("STDIN", """'""" + path + targets + """'""")

				cursor.execute(sql1_)
				end2 = datetime.now()  # stat
				print(str(datetime.now()) + ' : This took you ' + str((end2-start2).seconds + 1) + ' second(s).\n')

	# --- main #2
	# --- add camname, timestamp, videopart to raw-data

				print('working on step 2/2...')
				start3 = datetime.now()  # stat

				with open(path + "sql_2.sql", 'r') as sql2:
					sql2_ = sql2.read().replace("STDIN1", cam).replace("STDIN2", ts)  # TODO: ugly

				cursor.execute(sql2_)
				end3 = datetime.now()  # stat
				print(str(datetime.now()) + ' : This took you ' + str((end3-start3).seconds + 1) + ' second(s).')  # stat

	# --- main - handle identified errors
			else:
				print("""There's reference data available. Please check if it fits your purposes.""")
				end1 = datetime.now()  # stat
				print(str(datetime.now()) + ' : This took you ' + str((end1-start1).seconds + 1) + ' seconds')

	print('\n\n\nDone.\n\n')
