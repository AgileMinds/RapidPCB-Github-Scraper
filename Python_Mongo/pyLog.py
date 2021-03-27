import pymongo
import os
from datetime import datetime


class pyLogger:

    def __init__(self, _terminalPrint, _localLogDir, _serverString, _databaseName, _logName, _logLvl):
        collectionName = 'PyLogs'
        databaseName = "PyLogDB"
        localLogDir = os.getenv('APPDATA') + "\\pyLogging\\"
        self.locLogFlag = False
        self.mongoLogFlag = False
        self.terminalPrint = True
        self.logLvl = -1

        if _terminalPrint:
            self.terminalPrint = _terminalPrint

        if _logLvl:
            self.logLvl = _logLvl

        if self.terminalPrint:
            print("Local Terminal Printing")

        if _logName:
            logName = _logName
        else:
            logName = datetime.now().strftime("%Y%m%d_%H%M%S_PyLog")

        if not _localLogDir:
            if terminalPrint:
                print("No Local Logging")
        else:
            localLogDir = _localLogDir

            try:
                locLogFilepath = os.path.join(localLogDir, logName+".plog")
                self.locLogFile = open(locLogFilepath, 'w')
                self.locLogFlag = True
                if self.terminalPrint:
                    print("Local Log File: "+locLogFilepath)
                    self.locLogFile.write("Logging to Terminal ENABLED")
                    self.locLogFile.write("\n")
            except Exception as e:
                if self.terminalPrint:
                    print("Error Opening Local log File: " + str(e))
                self.locLogFlag = False

        if not _serverString:
            if self.terminalPrint:
                print("No Remote Logging")
            if self.locLogFlag:
                self.locLogFile.write("No Remote Logging")
                self.locLogFile.write("\n")
        else:
            try:
                if _databaseName:
                    databaseName = _databaseName
                logDatabase = pymongo.MongoClient(_serverString)[databaseName]
                self.logCollection = logDatabase[collectionName]
                self.logMongoID = self.logCollection.insert_one(
                    {'logName': logName}).inserted_id
                self.mongoLogFlag = True
                if self.terminalPrint:
                    print("Logger Connected to Database: "+databaseName +
                          ", Collection Name: "+collectionName+", Log Name: "+logName)
                    self.logCollection.update_one({'_id': self.logMongoID}, {
                                                  '$push': {'logs': "Logging to Terminal ENABLED"}})
                if self.locLogFlag:
                    self.locLogFile.write("Logger Connected to Database: "+databaseName +
                                          ", Collection Name: "+collectionName+", Log Name: "+logName)
                    self.locLogFile.write("\n")
                    self.logCollection.update_one({'_id': self.logMongoID}, {
                                                  '$push': {'logs': "Local Logging to \""+locLogFilepath+"\""}})
            except Exception as e:
                self.mongoLogFlag = False

                if self.terminalPrint:
                    print("Error Connecting to Database")
                    print("Error: " + str(e))
                if self.locLogFlag:
                    self.locLogFile.write("Error Connecting to Database")
                    self.locLogFile.write("Error: " + str(e))
                    self.locLogFile.write("\n")

    def log(self, _logText, _logLvl=-1):
        _logLvlFlag = True
        if _logLvl > 0:
            if _logLvl > self.logLvl and not self.logLvl == 0:
                _logLvlFlag = False

        if _logLvlFlag:
            if self.terminalPrint:
                print(_logText)

            if self.locLogFlag:
                try:
                    self.locLogFile.write(_logText)
                    self.locLogFile.write("\n")
                except:
                    self.locLogFile.write("[Corrupt Entry]\n")
            if self.mongoLogFlag:
                self.logCollection.update_one({'_id': self.logMongoID}, {
                    '$push': {'logs': _logText}})

    def setLogLvl(self, _logLvl):
        if _logLvl < 0:
            _logLvl = -1
        self.logLvl = _logLvl
        self.log("Log Level="+str(_logLvl))

    def getLogLvl(self):
        return self.logLvl
