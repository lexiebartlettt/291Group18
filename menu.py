import sys
import clearScreen

def giveOptions():
	
	print("Welcome. Please choose one of the following options.")
	print("Type 'Search' to search for a flight. ")
	print("Type 'Book' to make a booking.")
	print("Type 'List' to list existing bookings.")
	print("Type 'Logout' to logout.")
	
	return()

def displayMenu(isAgent):
	
	clearScreen.clearScreen()	
	#userInput = input()
	while True:
		giveOptions()
		userInput = input()
		if userInput.strip().lower()  == 'search':
			input("Do search.")
			#search()
			#break
			clearScreen.clearScreen()	

		elif userInput.strip().lower() == 'book':
			input("Do booking.")
			#book()
			#break
			clearScreen.clearScreen()	
		elif userInput.strip().lower() == 'list':
			input("List bookings.")
			#list()
			#break
			clearScreen.clearScreen()	
		elif userInput.strip().lower() == 'logout':
			print("Logging out.")
			#logout()
			#break
			sys.exit()
		else:
			clearScreen.clearScreen()
			print("Command not recognised.\n")
			#break
			
		
	return()

displayMenu(False)
