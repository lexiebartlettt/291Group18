class User():
    
    def __init__(self, email, isAgent):
        self.email = email
        self.isAgent = isAgent
        
    def getEmail(self):
        return self.email
    
    def isAgent(self):
        return self.isAgent