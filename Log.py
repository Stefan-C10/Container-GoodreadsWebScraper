class Log:
    def __init__(self):
        self.message = ""

    def log(self, message):
        self.message += message

    def getLog(self):
        return self.message