class User():
    
    def __init__(self, email, isAirAgent):
        self.email = email
        self.isAirAgent = isAirAgent
        
    def getEmail(self):
        return self.email
    
    def isAgent(self):
        return self.isAgent
