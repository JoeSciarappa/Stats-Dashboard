from flask import Flask, render_template,request,flash,redirect,url_for, Markup, jsonify
from collections import defaultdict
from datetime import datetime as dt
import mysql.connector as mariadb
import datetime
import random
import json
app = Flask(__name__)



@app.route("/", methods=['GET'])
def stats():

        curDate = datetime.date.today()

        mariadb_connection = mariadb.connect(user='stats', password='OGE1MTZkYzNhYWI', database='stats')
        cursor = mariadb_connection.cursor(dictionary=True)

	cursor.execute('''select count(*) as ifrows from smb_linux where date = "%s"'''%(curDate))
	ifrow = cursor.fetchone()['ifrows']
	
	mariadb_connection.close()


	if request.method == 'GET':
		return render_template('master.html',ifrow=ifrow)
	else:
		return render_template('outline.html')

	

@app.route("/PublicTicketsPerTeam")
def publicticketsperteam():


	curDate = datetime.date.today() 

        mariadb_connection = mariadb.connect(user='stats', password='OGE1MTZkYzNhYWI', database='stats')
        cursor = mariadb_connection.cursor(buffered=True, dictionary=True)

	#MySQL
	cursor.execute('''SELECT SUM(cloud) + SUM(dedicated) AS total FROM smb_linux WHERE date = "%s"''' % (curDate))
	totalPublicTickets = cursor.fetchone()['total']

	if totalPublicTickets is not None:
	
		cursor.execute('''SELECT SUM(cloud) + SUM(dedicated) AS total FROM smb_linux WHERE manager="Joe Kirby" AND date = "%s"''' % (curDate))
		watchdogsTotalPublicTickets = cursor.fetchone()['total']

		cursor.execute('''SELECT SUM(cloud) + SUM(dedicated) AS total FROM smb_linux WHERE (manager="Joshua Prichard" OR manager="Bill Pepmiller") AND date = "%s"''' % (curDate))
		spattlecocksTotalPublicTickets = cursor.fetchone()['total']
	
		cursor.execute('''SELECT SUM(cloud) + SUM(dedicated) AS total FROM smb_linux WHERE manager="Stacey Ford" AND date = "%s"''' % (curDate))
		porkchopexpressTotalPublicTickets = cursor.fetchone()['total']


		#Calculations
		watchdogs = round( (( watchdogsTotalPublicTickets / totalPublicTickets ) * 100),2)
		spattlecock = round( (( spattlecocksTotalPublicTickets / totalPublicTickets ) * 100), 2)
		porkchopexpress = round( ( porkchopexpressTotalPublicTickets / totalPublicTickets ) * 100,2)



		mariadb_connection.close()
		return jsonify(watchdogs=watchdogs, spattlecock=spattlecock, porkchopexpress=porkchopexpress)
	else: 
                mariadb_connection.close()
                return jsonify(watchdogs='null', spattlecock='null', porkchopexpress='null')

@app.route("/CallsPerTeam")
def callsperteam():


        curDate = datetime.date.today()


        mariadb_connection = mariadb.connect(user='stats', password='OGE1MTZkYzNhYWI', database='stats')
        cursor = mariadb_connection.cursor(buffered=True, dictionary=True)

	#MySQL
       	cursor.execute('''SELECT SUM(calls) AS total FROM smb_linux WHERE calls != -1 AND date = "%s"''' % (curDate))
	totalCalls = cursor.fetchone()['total']

	if totalCalls is not None:

		cursor.execute('''SELECT SUM(calls) AS total FROM smb_linux WHERE calls != -1 AND manager="Joe Kirby" AND date = "%s"''' % (curDate))
		watchdogsTotalCalls = cursor.fetchone()['total']

		cursor.execute('''SELECT SUM(calls) AS total FROM smb_linux WHERE calls != -1 AND manager="Stacey Ford" AND date = "%s"''' % (curDate))
		porkchopexpressTotalCalls = cursor.fetchone()['total']

		cursor.execute('''SELECT SUM(calls) AS total FROM smb_linux WHERE calls != -1 AND ( manager="Joshua Prichard" OR manager="Bill Pepmiller" ) AND date = "%s"''' % (curDate))
		spattlecocksTotalCalls = cursor.fetchone()['total']


	        #Calculations
        	watchdogs = round ( (( watchdogsTotalCalls / totalCalls ) * 100 ),2)
	        spattlecock = round( (( spattlecocksTotalCalls / totalCalls ) * 100),2)
        	porkchopexpress = round( (( porkchopexpressTotalCalls / totalCalls ) * 100),2)


		
		mariadb_connection.close()
	
        	return jsonify( watchdogs=watchdogs, spattlecock=spattlecock, porkchopexpress=porkchopexpress )
	else:
		mariadb_connection.close()
		return jsonify( watchdogs='null', spattlecock='null', porkchopexpress='null' )


@app.route("/PublicTicketsPerLevel")
def publicticketsperlevel():

        curDate = datetime.date.today()

        mariadb_connection = mariadb.connect(user='stats', password='OGE1MTZkYzNhYWI', database='stats')
        cursor = mariadb_connection.cursor(buffered=True, dictionary=True)

        cursor.execute('''SELECT SUM(cloud) + SUM(dedicated) AS total FROM smb_linux WHERE date = "%s"''' % (curDate))
	totalPublicTickets = cursor.fetchone()['total']

	if totalPublicTickets is not None:

		cursor.execute('''SELECT SUM(cloud) + SUM(dedicated) AS total FROM smb_linux WHERE level=2 AND date = "%s"''' % (curDate))
		l2PublicTickets = cursor.fetchone()['total']

		cursor.execute('''SELECT SUM(cloud) + SUM(dedicated) AS total FROM smb_linux WHERE level=1 AND date = "%s"''' % (curDate))
		l1PublicTickets = cursor.fetchone()['total']

	        #Calculations
        	l1 = round( (( l1PublicTickets / totalPublicTickets ) * 100),2)
	        l2 = round( (( l2PublicTickets / totalPublicTickets ) * 100 ),2)

		mariadb_connection.close()

	        return jsonify( l1=l1, l2=l2)
	else:
		mariadb_connection.close() 
		return jsonify( l1='null', l2='null')

@app.route("/CallsPerLevel")
def callsperlevel():

        curDate = datetime.date.today()

        mariadb_connection = mariadb.connect(user='stats', password='OGE1MTZkYzNhYWI', database='stats')
        cursor = mariadb_connection.cursor(buffered=True, dictionary=True)

        cursor.execute('''SELECT SUM(calls) AS total FROM smb_linux WHERE calls != -1 AND date = "%s"''' % (curDate))
	totalCalls = cursor.fetchone()['total']

	if totalCalls is not None:

		cursor.execute('''SELECT SUM(calls) AS total FROM smb_linux WHERE calls != -1 AND level=2 AND date = "%s"''' % (curDate))
		l2Calls = cursor.fetchone()['total']

		cursor.execute('''SELECT SUM(calls) AS total FROM smb_linux WHERE calls != -1 AND level=1 AND date = "%s"''' % (curDate))
		l1Calls = cursor.fetchone()['total']

	        #Calculations
        	l1 = round( (( l1Calls / totalCalls ) * 100),2)
	        l2 = round( (( l2Calls / totalCalls ) * 100),2)

		mariadb_connection.close()

	        return jsonify(l1=l1, l2=l2)
	else:
		mariadb_connection.close()
		return jsonify(l1='null', l2='null')

@app.route("/CallLeaderboard")
def callleaderboard():

        curDate = datetime.date.today()


        mariadb_connection = mariadb.connect(user='stats', password='OGE1MTZkYzNhYWI', database='stats')
        cursor = mariadb_connection.cursor(buffered=True, dictionary=True)

	cursor.execute('''SELECT name, calls, manager FROM smb_linux WHERE date = "%s" ORDER BY calls DESC LIMIT 3''' % (curDate))


	if cursor.rowcount != 0:
		loop=1
		for rackerDictionary in cursor:
			if loop == 1:
				leader1Name = rackerDictionary['name']
				leader1Calls = rackerDictionary['calls']
				leader1Team = rackerDictionary['manager']
				if leader1Team == "Joe Kirby":
					leader1Team = "Watchdogs"
				elif leader1Team == "Stacey Ford":
					leader1Team = "Porkchop Express"
				elif leader1Team == "Joshua Prichard" or leader1Team == "Bill Pepmiller":
					leader1Team = "Spattlecock"
                	if loop == 2:
                        	leader2Name = rackerDictionary['name']
	                        leader2Calls = rackerDictionary['calls']
				leader2Team = rackerDictionary['manager']
                	        if leader2Team == "Joe Kirby":
                        	        leader2Team = "Watchdogs"
	                        elif leader2Team == "Stacey Ford":
        	                        leader2Team = "Porkchop Express"
                	        elif leader2Team == "Joshua Prichard" or leader2Team == "Bill Pepmiller":
                        	        leader2Team = "Spattlecock"

	                if loop == 3:
        	                leader3Name = rackerDictionary['name']
                	        leader3Calls = rackerDictionary['calls']
				leader3Team = rackerDictionary['manager']
	                        if leader3Team == "Joe Kirby":
        	                        leader3Team = "Watchdogs"
                	        elif leader3Team == "Stacey Ford":
                        	        leader3Team = "Porkchop Express"
	                        elif leader3Team == "Joshua Prichard" or leader3Team == "Bill Pepmiller":
        	                        leader3Team = "Spattlecock"

			loop+=1

		mariadb_connection.close()		
		return jsonify( leader1Name=leader1Name, leader1Calls=leader1Calls, leader1Team=leader1Team, leader2Name=leader2Name, leader2Calls=leader2Calls, leader2Team=leader2Team, leader3Name=leader3Name, leader3Calls=leader3Calls, leader3Team=leader3Team)

	else:
		mariadb_connection.close()
		return jsonify( leader1Name='null', leader1Calls='null', leader1Team='null', leader2Name='null', leader2Calls='null', leader2Team='null', leader3Name='null', leader3Calls='null', leader3Team='null')


@app.route("/TicketLeaderboard")
def ticketleaderboard():

        curDate = datetime.date.today()

        mariadb_connection = mariadb.connect(user='stats', password='OGE1MTZkYzNhYWI', database='stats')
        cursor = mariadb_connection.cursor(buffered=True, dictionary=True)

        cursor.execute('''SELECT name, dedicated+cloud as tickets, manager FROM smb_linux WHERE date = "%s" ORDER BY tickets DESC LIMIT 3''' % (curDate))
       
	if cursor.rowcount != 0: 
	        loop=1
        	for rackerDictionary in cursor:
                	if loop == 1:
                        	leader1Name = rackerDictionary['name']
	                        leader1Tickets = rackerDictionary['tickets']
        	                leader1Team = rackerDictionary['manager']
                	        if leader1Team == "Joe Kirby":
                        	        leader1Team = "Watchdogs"
	                        elif leader1Team == "Stacey Ford":
        	                        leader1Team = "Porkchop Express"
                	        elif leader1Team == "Joshua Prichard" or leader1Team == "Bill Pepmiller":
                        	        leader1Team = "Spattlecock"
	                if loop == 2:
        	                leader2Name = rackerDictionary['name']
                	        leader2Tickets = rackerDictionary['tickets']
                        	leader2Team = rackerDictionary['manager']
	                        if leader2Team == "Joe Kirby":
        	                        leader2Team = "Watchdogs"
                	        elif leader2Team == "Stacey Ford":
                        	        leader2Team = "Porkchop Express"
	                        elif leader2Team == "Joshua Prichard" or leader2Team == "Bill Pepmiller":
        	                        leader2Team = "Spattlecock"

	                if loop == 3:
        	                leader3Name = rackerDictionary['name']
                	        leader3Tickets = rackerDictionary['tickets']
                        	leader3Team = rackerDictionary['manager']
	                        if leader3Team == "Joe Kirby":
        	                        leader3Team = "Watchdogs"
                	        elif leader3Team == "Stacey Ford":
                        	        leader3Team = "Porkchop Express"
	                        elif leader3Team == "Joshua Prichard" or leader3Team == "Bill Pepmiller":
        	                        leader3Team = "Spattlecock"

                	loop+=1

		mariadb_connection.close()

        	return jsonify(leader1Name=leader1Name, leader1Tickets=leader1Tickets, leader1Team=leader1Team, leader2Name=leader2Name, leader2Tickets=leader2Tickets, leader2Team=leader2Team, leader3Name=leader3Name, leader3Tickets=leader3Tickets, leader3Team=leader3Team)

	else:
		mariadb_connection.close()
		return jsonify(leader1Name='null', leader1Tickets='null', leader1Team='null', leader2Name='null', leader2Tickets='null', leader2Team='null', leader3Name='null', leader3Tickets='null', leader3Team='null')

@app.route("/TicketBarGraph")
def ticketbargraph(): 
 
        curDate = datetime.date.today()


        mariadb_connection = mariadb.connect(user='stats', password='OGE1MTZkYzNhYWI', database='stats')
        cursor = mariadb_connection.cursor(buffered=True, dictionary=True)

	masterList=[]
	cursor.execute('''SELECT name, dedicated+cloud as tickets, manager FROM smb_linux WHERE date = "%s" ORDER BY tickets DESC''' % (curDate))

	if cursor.rowcount != 0:
		for rackerDictionary in cursor:
			name = rackerDictionary['name']
			tickets = rackerDictionary['tickets']
			manager = rackerDictionary['manager']

        	        if manager == 'Joe Kirby':
                	        color='#5D6D7E'
	                elif manager == 'Stacey Ford':
        	                color='#B7DCD8'
                	elif manager == 'Joshua Prichard' or manager == 'Bill Pepmiller':
                        	color='#785A66'
	                else:
        	                color='#010000'

	                rackerList={}
        	        rackerList['name'] = name
                	rackerList['color'] = color
	                rackerList['y'] = tickets

			masterList.append(rackerList)

		mariadb_connection.close()

		return jsonify(TicketBarGraph=masterList)

	else:
		mariadb_connection.close()
		return jsonify(TicketBarGraph='null')

@app.route("/CallBarGraph")
def callbargraph():

        curDate = datetime.date.today()


        mariadb_connection = mariadb.connect(user='stats', password='OGE1MTZkYzNhYWI', database='stats')
        cursor = mariadb_connection.cursor(buffered=True, dictionary=True)


        masterList=[]
        cursor.execute('''SELECT name, calls, manager FROM smb_linux WHERE date = "%s" ORDER BY calls DESC''' % (curDate))

	if cursor.rowcount != 0:
	        for rackerDictionary in cursor:
        	        name = rackerDictionary['name']
                	calls = rackerDictionary['calls']
	                manager = rackerDictionary['manager']

			if manager == 'Joe Kirby':
				color='#5D6D7E'
			elif manager == 'Stacey Ford':
				color='#B7DCD8'
			elif manager == 'Joshua Prichard' or manager == "Bill Pepmiller":
				color='#785A66'
			else:
				color='#010000'

			rackerList={}
			rackerList['name'] = name
			rackerList['color'] = color
			rackerList['y'] = calls
	
			masterList.append(rackerList)

	        mariadb_connection.close()

        	return jsonify(CallBarGraph=masterList)
	else: 
		mariadb_connection.close()
		return jsonify(CallBarGraph='null')


@app.route("/AverageCallsPerRackerPerTeam")
def averagecallsperrackerperteam():

        curDate = datetime.date.today()

        mariadb_connection = mariadb.connect(user='stats', password='OGE1MTZkYzNhYWI', database='stats')
        cursor = mariadb_connection.cursor(buffered=True, dictionary=True)

	masterList=[]
	cursor.execute('''SELECT manager, SUM(calls) / count(name) as acprpt from smb_linux where calls!=-1 and date="%s" GROUP BY manager ORDER BY acprpt DESC;''' % (curDate))

	if cursor.rowcount != 0:
		for rackerDictionary in cursor:
			acprpt = round(rackerDictionary['acprpt'],2)
			manager = rackerDictionary['manager']

                        if manager == 'Joe Kirby':
                                color='#5D6D7E'
				team='Watchdogs'
                        elif manager == 'Stacey Ford':
                                color='#B7DCD8'
				team='Porkchop Express'
                        elif manager == 'Joshua Prichard': 
                                color='#785A66'
				team='Spattlecock - Joshua'
			elif manager == 'Bill Pepmiller':
                                color='#785A66'
                                team='Spattlecock - Bill'

                        else:
                                color='#010000'

                        teamList={}
                        teamList['color'] = color
                        teamList['y'] = acprpt
			teamList['name'] = team
                        masterList.append(teamList)

		mariadb_connection.close()
		return jsonify(acprpt=masterList)
	else:
		mariadb_connection.close()
		return jsonify(acprpt='null')

@app.route("/AverageTicketsPerRackerPerTeam")
def averageticketsperrackerperteam():

        curDate = datetime.date.today()

        mariadb_connection = mariadb.connect(user='stats', password='OGE1MTZkYzNhYWI', database='stats')
        cursor = mariadb_connection.cursor(buffered=True, dictionary=True)

        masterList=[]
        cursor.execute('''SELECT manager, SUM(dedicated + cloud) / count(name) as atprpt from smb_linux where date="%s" GROUP BY manager ORDER BY atprpt DESC;''' % (curDate))

        if cursor.rowcount != 0:
                for rackerDictionary in cursor:
                        atprpt = round(rackerDictionary['atprpt'],2)
                        manager = rackerDictionary['manager']

                        if manager == 'Joe Kirby':
                                color='#5D6D7E'
                                team='Watchdogs'
                        elif manager == 'Stacey Ford':
                                color='#B7DCD8'
                                team='Porkchop Express'
                        elif manager == 'Joshua Prichard': 
                                color='#785A66'
                                team='Spattlecock - Joshua'
                        elif manager == 'Bill Pepmiller':
                                color='#785A66'
                                team='Spattlecock - Bill'
                        else:
                                color='#010000'

                        teamList={}
                        teamList['color'] = color
                        teamList['y'] = atprpt
			teamList['name'] = team
                        masterList.append(teamList)

                mariadb_connection.close()
                return jsonify(atprpt=masterList)
        else:
                mariadb_connection.close()
                return jsonify(atprpt='null')



@app.route("/archive", methods=['GET','POST'])
def archive():
        if request.method == 'GET':
		return render_template('archiveLanding.html')
	if request.method == 'POST':

		errorMessage=''

		try:
			sDate = datetime.datetime.strptime(str(request.form['sdate']), '%m/%d/%Y').strftime('%Y-%m-%d')
                        eDate = datetime.datetime.strptime(str(request.form['edate']), '%m/%d/%Y').strftime('%Y-%m-%d')

		except ValueError:
			errorMessage='Input did not pass validation'	
			return render_template('archiveLanding.html',errorMessage=errorMessage)

	        mariadb_connection = mariadb.connect(user='stats', password='OGE1MTZkYzNhYWI', database='stats')
        	cursor = mariadb_connection.cursor(buffered=True, dictionary=True)

################PublicTicketsPerTeam
	        #MySQL
       		cursor.execute('''SELECT SUM(cloud) + SUM(dedicated) AS total FROM smb_linux WHERE date BETWEEN "%s" AND "%s"''' % (sDate,eDate))
        	totalPublicTickets = cursor.fetchone()['total']

        	cursor.execute('''SELECT SUM(cloud) + SUM(dedicated) AS total FROM smb_linux WHERE manager="Joe Kirby" AND date BETWEEN "%s" AND "%s"''' % (sDate,eDate))
        	watchdogsTotalPublicTickets = cursor.fetchone()['total']

        	cursor.execute('''SELECT SUM(cloud) + SUM(dedicated) AS total FROM smb_linux WHERE (manager="Joshua Prichard" OR manager="Bill Pepmiller") AND date BETWEEN "%s" AND "%s"''' % (sDate,eDate))
        	spattlecocksTotalPublicTickets = cursor.fetchone()['total']

        	cursor.execute('''SELECT SUM(cloud) + SUM(dedicated) AS total FROM smb_linux WHERE manager="Stacey Ford" AND date BETWEEN "%s" AND "%s"''' % (sDate,eDate))
        	porkchopexpressTotalPublicTickets = cursor.fetchone()['total']

        	#Calculations
		try:
	        	ptptWatchdogs = round( (( watchdogsTotalPublicTickets / totalPublicTickets ) * 100),2)
		except TypeError:
			ptptWatchdogs = 0
		try:
        		ptptSpattlecock = round( (( spattlecocksTotalPublicTickets / totalPublicTickets ) * 100), 2)
		except TypeError:
			ptptSpattlecock = 0
		try:
        		ptptPorkchopexpress = round( ( porkchopexpressTotalPublicTickets / totalPublicTickets ) * 100,2)
		except TypeError:
			ptptPorkchopexpress = 0

################CallsPerTeam
	        #MySQL
        	cursor.execute('''SELECT SUM(calls) AS total FROM smb_linux WHERE calls != -1 AND date BETWEEN "%s" AND "%s"''' % (sDate,eDate))
        	totalCalls = cursor.fetchone()['total']

        	cursor.execute('''SELECT SUM(calls) AS total FROM smb_linux WHERE calls != -1 AND manager="Joe Kirby" AND date BETWEEN "%s" AND "%s"''' % (sDate,eDate))
        	watchdogsTotalCalls = cursor.fetchone()['total']

        	cursor.execute('''SELECT SUM(calls) AS total FROM smb_linux WHERE calls != -1 AND manager="Stacey Ford" AND date BETWEEN "%s" AND "%s"''' % (sDate,eDate))
        	porkchopexpressTotalCalls = cursor.fetchone()['total']

        	cursor.execute('''SELECT SUM(calls) AS total FROM smb_linux WHERE calls != -1 AND (manager="Joshua Prichard" OR manager="Bill Pepmiller") AND date BETWEEN "%s" AND "%s"''' % (sDate,eDate))
        	spattlecocksTotalCalls = cursor.fetchone()['total']


        	#Calculations
		try:
	        	cptWatchdogs = round ( (( watchdogsTotalCalls / totalCalls ) * 100 ),2)
		except:
			cptWatchdogs = 0
		try:
        		cptSpattlecock = round( (( spattlecocksTotalCalls / totalCalls ) * 100),2)
		except:
			cptSpattlecock = 0
		try:
	        	cptPorkchopexpress = round( (( porkchopexpressTotalCalls / totalCalls ) * 100),2)
		except:
			cptPorkchopexpress = 0

################PublicTicketsPerLevel
		#MySQL
        	cursor.execute('''SELECT SUM(cloud) + SUM(dedicated) AS total FROM smb_linux WHERE date BETWEEN "%s" AND "%s"''' % (sDate,eDate))
        	totalPublicTickets = cursor.fetchone()['total']

        	cursor.execute('''SELECT SUM(cloud) + SUM(dedicated) AS total FROM smb_linux WHERE level=2 AND date BETWEEN "%s" AND "%s"''' % (sDate,eDate))
        	l2PublicTickets = cursor.fetchone()['total']

        	cursor.execute('''SELECT SUM(cloud) + SUM(dedicated) AS total FROM smb_linux WHERE level=1 AND date BETWEEN "%s" AND "%s"''' % (sDate,eDate))
        	l1PublicTickets = cursor.fetchone()['total']

        	#Calculations
		try:
	        	ptplL1 = round( (( l1PublicTickets / totalPublicTickets ) * 100),2)
		except TypeError:
			ptplL1 = 0
		try:
	        	ptplL2 = round( (( l2PublicTickets / totalPublicTickets ) * 100 ),2)
		except TypeError:
			ptplL2 = 0
################CallsPerLevel
	        cursor.execute('''SELECT SUM(cloud) + SUM(dedicated) AS total FROM smb_linux WHERE date BETWEEN "%s" AND "%s"''' % (sDate,eDate))
       		totalPublicTickets = cursor.fetchone()['total']

        	cursor.execute('''SELECT SUM(cloud) + SUM(dedicated) AS total FROM smb_linux WHERE level=2 AND date BETWEEN "%s" AND "%s"''' % (sDate,eDate))
        	l2PublicTickets = cursor.fetchone()['total']

        	cursor.execute('''SELECT SUM(cloud) + SUM(dedicated) AS total FROM smb_linux WHERE level=1 AND date BETWEEN "%s" AND "%s"''' % (sDate,eDate))
        	l1PublicTickets = cursor.fetchone()['total']

        	#Calculations
		try:
	        	cplL1 = round( (( l1PublicTickets / totalPublicTickets ) * 100),2)
		except TypeError:
			cplL1 = 0
		try:
	        	cplL2 = round( (( l2PublicTickets / totalPublicTickets ) * 100 ),2)
		except TypeError:
			cplL2 = 0
################CallLeaderboard

	        cursor.execute('''SELECT name, SUM(calls) as calls, manager FROM smb_linux WHERE calls != -1 AND date BETWEEN "%s" AND "%s" GROUP BY name ORDER BY calls DESC LIMIT 3''' % (sDate,eDate))

		if cursor.rowcount != 0:
	        	loop=1
        		for rackerDictionary in cursor:
	                	if loop == 1:
        	                	cleader1Name = rackerDictionary['name']
                	        	cleader1Calls = rackerDictionary['calls']
                        		cleader1Team = rackerDictionary['manager']
                        		if cleader1Team == "Joe Kirby":
	                                	cleader1Team = "Watchdogs"
        	                	elif cleader1Team == "Stacey Ford":
                	                	cleader1Team = "Porkchop Express"
                        		elif cleader1Team == "Joshua Prichard" or cleader1Team == "Bill Pepmiller":
                                		cleader1Team = "Spattlecock"
	                	if loop == 2:
        	                	cleader2Name = rackerDictionary['name']
                	        	cleader2Calls = rackerDictionary['calls']
                        		cleader2Team = rackerDictionary['manager']
                        		if cleader2Team == "Joe Kirby":
	                                	cleader2Team = "Watchdogs"
        	                	elif cleader2Team == "Stacey Ford":
                	                	cleader2Team = "Porkchop Express"
                        		elif cleader2Team == "Joshua Prichard" or cleader2Team == "Bill Pepmiller":
                                		cleader2Team = "Spattlecock"

	                	if loop == 3:
        	                	cleader3Name = rackerDictionary['name']
                	        	cleader3Calls = rackerDictionary['calls']
                        		cleader3Team = rackerDictionary['manager']
                        		if cleader3Team == "Joe Kirby":
	                                	cleader3Team = "Watchdogs"
        	                	elif cleader3Team == "Stacey Ford":
                	                	cleader3Team = "Porkchop Express"
                        		elif cleader3Team == "Joshua Prichard" or cleader3Team == "Bill Pepmiller":
                                		cleader3Team = "Spattlecock"

	                	loop+=1
		try:
			cleader1Name
		except NameError:
			cleader1Name=''
		try:
			cleader1Calls
		except NameError:
			cleader1Calls=''
		try:
			cleader1Team
		except NameError:
			cleader1Team=''
		try:
			cleader2Name
		except NameError:
			cleader2Name=''
		try:
			cleader2Calls
		except NameError:
			cleader2Calls=''
		try:
			cleader2Team
		except NameError:
			cleader2Team=''
		try:
			cleader3Name
		except NameError:
			cleader3Name=''
		try:
			cleader3Calls
		except NameError:
			cleader3Calls=''
		try:
			cleader3Team
		except NameError:
			cleader3Team=''

################TicketLeaderboard
        	cursor.execute('''SELECT name, SUM(dedicated + cloud) as tickets, manager FROM smb_linux WHERE date BETWEEN "%s" AND "%s" GROUP BY name ORDER BY tickets DESC LIMIT 3''' % (sDate,eDate))

		if cursor.rowcount != 0:
	        	loop=1
        		for rackerDictionary in cursor:
                		if loop == 1:
	                        	tleader1Name = rackerDictionary['name']
        	               		tleader1Tickets = rackerDictionary['tickets']
                	        	tleader1Team = rackerDictionary['manager']
	                        	if tleader1Team == "Joe Kirby":
        	                        	tleader1Team = "Watchdogs"
                	        	elif tleader1Team == "Stacey Ford":
                        	        	tleader1Team = "Porkchop Express"
	                        	elif tleader1Team == "Joshua Prichard" or tleader1Team == "Bill Pepmiller":
        	                        	tleader1Team = "Spattlecock"
                		if loop == 2:
                        		tleader2Name = rackerDictionary['name']
                        		tleader2Tickets = rackerDictionary['tickets']
	                        	tleader2Team = rackerDictionary['manager']
        	                	if tleader2Team == "Joe Kirby":
                	                	tleader2Team = "Watchdogs"
                        		elif tleader2Team == "Stacey Ford":
                                		tleader2Team = "Porkchop Express"
	                        	elif tleader2Team == "Joshua Prichard" or tleader2Team == "Bill Pepmiller":
        	                        	tleader2Team = "Spattlecock"

                		if loop == 3:
                        		tleader3Name = rackerDictionary['name']
                        		tleader3Tickets = rackerDictionary['tickets']
	                        	tleader3Team = rackerDictionary['manager']
        	                	if tleader3Team == "Joe Kirby":
                	                	tleader3Team = "Watchdogs"
                        		elif tleader3Team == "Stacey Ford":
	                                	tleader3Team = "Porkchop Express"
        	                	elif tleader3Team == "Joshua Prichard" or tleader3Team == "Bill Pepmiller":
                	                	tleader3Team = "Spattlecock"

                		loop+=1

                try:
                        tleader1Name
                except NameError:
                        tleader1Name=''
                try:
                        tleader1Tickets
                except NameError:
                        tleader1Tickets=''
                try:
                        tleader1Team
                except NameError:
                        tleader1Team=''
                try:
                        tleader2Name
                except NameError:
                        tleader2Name=''
                try:
                        tleader2Tickets
                except NameError:
                        tleader2Tickets=''
                try:
                        tleader2Team
                except NameError:
                        tleader2Team=''
                try:
                        tleader3Name
                except NameError:
                        tleader3Name=''
                try:
                        tleader3Tickets
                except NameError:
                        tleader3Tickets=''
                try:
                        tleader3Team
                except NameError:
                        tleader3Team=''

################TicketBarGraph
        	tmasterList=[]
        	cursor.execute('''SELECT name, SUM(dedicated + cloud) as tickets, manager FROM smb_linux WHERE date BETWEEN "%s" AND "%s" GROUP BY name ORDER BY tickets DESC LIMIT 30''' % (sDate,eDate))
        	for rackerDictionary in cursor:
                	name = rackerDictionary['name']
                	tickets = rackerDictionary['tickets']
                	manager = rackerDictionary['manager']

                	if manager == 'Joe Kirby':
                        	color='#5D6D7E'
                	elif manager == 'Stacey Ford':
                        	color='#B7DCD8'
                	elif manager == 'Joshua Prichard' or manager == 'Bill Pepmiller':
                        	color='#785A66'
                	else:
                        	color='#010000'

                	rackerList={}
                	rackerList['name'] = str(name)
                	rackerList['color'] = str(color)
                	rackerList['y'] = int(tickets)

                	tmasterList.append(rackerList)



################CallBarGraph
        	cmasterList=[]
        	cursor.execute('''SELECT name, SUM(calls) as calls, manager FROM smb_linux WHERE calls != -1 AND date BETWEEN "%s" AND "%s" GROUP BY name ORDER BY calls DESC LIMIT 30''' % (sDate,eDate))
        	for rackerDictionary in cursor:
                	name = rackerDictionary['name']
                	calls = rackerDictionary['calls']
                	manager = rackerDictionary['manager']

                	if manager == 'Joe Kirby':
                        	color='#5D6D7E'
                	elif manager == 'Stacey Ford':
                        	color='#B7DCD8'
                	elif manager == 'Joshua Prichard' or manager == 'Bill Pepmiller':
                        	color='#785A66'
                	else:
                        	color='#010000'

                	rackerList={}
                	rackerList['name'] = str(name)
                	rackerList['color'] = str(color)
                	rackerList['y'] = int(calls)

                	cmasterList.append(rackerList)


################atprpt
		atprptmasterList=[]
		cursor.execute('''SELECT manager, SUM(dedicated + cloud) / count(name) as atprpt from smb_linux where date BETWEEN "%s" AND "%s" GROUP BY manager ORDER BY atprpt DESC;''' % (sDate,eDate))

		for rackerDictionary in cursor:
	                atprpt = round( rackerDictionary['atprpt'] ,2)
			manager = rackerDictionary['manager']
			if manager == 'Joe Kirby':
				color='#5D6D7E'
                                team='Watchdogs'
			elif manager == 'Stacey Ford':
				color='#B7DCD8'
                                team='Porkchop Express'
			elif manager == 'Joshua Prichard': 
				color='#785A66'
                                team='Spattlecock - Joshua'
                        elif manager == 'Bill Pepmiller':
                                color='#785A66'
                                team='Spattlecock - Bill'

			else:
				color='#010000'
			teamList={}
			teamList['color'] = color
			teamList['y'] = atprpt
			teamList['name'] = team

			atprptmasterList.append(teamList)


##############acprpt
                acprptmasterList=[]
                cursor.execute('''SELECT manager, SUM(calls) / count(name) as acprpt from smb_linux where date BETWEEN "%s" AND "%s" GROUP BY manager ORDER BY acprpt DESC;''' % (sDate,eDate))
        
                for rackerDictionary in cursor:
                        acprpt = round( rackerDictionary['acprpt'] , 2)
                        manager = rackerDictionary['manager']
                        if manager == 'Joe Kirby':
                                color='#5D6D7E'
				team='Watchdogs'
                        elif manager == 'Stacey Ford':
                                color='#B7DCD8'
				team='Porkchop Express'
                        elif manager == 'Joshua Prichard':
                                color='#785A66'
				team='Spattlecock - Joshua'
                        elif manager == 'Bill Pepmiller':
                                color='#785A66'
                                team='Spattlecock - Bill'

                        else:   
                                color='#010000'
                        teamList={}
                        teamList['color'] = color
                        teamList['y'] = acprpt
			teamList['name'] = team

                        acprptmasterList.append(teamList)


################################


		#Close Connection
        	mariadb_connection.close()

                return render_template('archiveMaster.html', sdate=sDate,edate=eDate,ptptWatchdogs=ptptWatchdogs,ptptSpattlecock=ptptSpattlecock,ptptPorkchopexpress=ptptPorkchopexpress,cptWatchdogs=cptWatchdogs,cptSpattlecock=cptSpattlecock,cptPorkchopexpress=cptPorkchopexpress,ptplL1=ptplL1,ptplL2=ptplL2,cplL1=cplL1,cplL2=cplL2,cleader1Name=cleader1Name,cleader1Calls=cleader1Calls,cleader1Team=cleader1Team,cleader2Name=cleader2Name,cleader2Calls=cleader2Calls,cleader2Team=cleader2Team,cleader3Name=cleader3Name,cleader3Calls=cleader3Calls,cleader3Team=cleader3Team,tleader1Name=tleader1Name,tleader1Tickets=tleader1Tickets,tleader1Team=tleader1Team,tleader2Name=tleader2Name,tleader2Tickets=tleader2Tickets,tleader2Team=tleader2Team,tleader3Name=tleader3Name,tleader3Tickets=tleader3Tickets,tleader3Team=tleader3Team,tmasterList=tmasterList,cmasterList=cmasterList,atprptmasterList=atprptmasterList,acprptmasterList=acprptmasterList)






@app.route("/about", methods=['GET'])
def about():
	return render_template('about.html')


if __name__ == "__main__":
	app.run(debug=False,port=5001)
	app.run()
