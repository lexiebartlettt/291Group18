import sys
import clearScreen
import user

def giveOptions(user1):
	
	print("Welcome. Please choose one of the following options.")
	print("Type 'Search' to search for a flight. ")
	print("Type 'Book' to make a booking.")
	print("Type 'List' to list existing bookings.")
	print("Type 'Logout' to logout.")

	#print(user1.isAgent())	
	if user1.isAgent():
		print( "\n Agent Options")
		print("Type 'Dep' to record a flight departure")
		print("Type 'Arr' to record a flight arrival")
	return()

def displayMenu(user1):
	
	clearScreen.clearScreen()	
	#userInput = input()
	while True:
		giveOptions(user1)
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
		elif userInput.strip().lower() == 'dep':
			if user1.isAgent():
				print("Record Dep")
				#recordDep()
			else:
				clearScreen.clearScreen()
				print("Action Unauthorized")
		elif userInput.strip().lower() == 'arr':
			if user1.isAgent():
				print("Record Arr")
				#recordArr()
			else:
				clearScreen.clearScreen()
				print("Action Unauthorized")
		else:
			clearScreen.clearScreen()
			print("Command not recognised.\n")
			#break
			
		
	return()

if __name__ == '__main__':
	displayMenu(False)
