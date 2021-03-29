# gitScraper.py from gitScraper import gitScraper

import pymongo
import os
from pyLog import pyLogger
from github import Github


class gitScraper:

    CONTENT_FILE_CAP = 500

    def __init__(self, _gitAcessToken, _databaseString, _databaseDest):
        self.logger = pyLogger(
            True, os.getcwd(), _databaseString, _databaseDest, [], 1)
        self.logger.log("gitScraper.__init__()")
        self.logger.log("_databaseDest="+_databaseDest)

        self.logger.log("Connecing to Github")
        self.git = Github(_gitAcessToken)
        self.logger.log("Conneced to Github")

        self.logger.log("Connecing to MongDB")
        self.scraperDatabase = pymongo.MongoClient(_databaseString)[
            _databaseDest]
        self.logger.log("Conneced to MongDB")

##############################
    def updateUser(self, _userName, _refreshFlag=False):
        self.logger.log(
            "gitScraper.updateUser("+_userName+","+str(_refreshFlag)+")")

        # Check if user exists in DB
        if not self.scraperDatabase["pcbUsers"].find_one({'userID': _userName}):
            self.logger.log("Adding User " + _userName + " to database")
            self.scraperDatabase["pcbUsers"].insert_one({'userID': _userName})
        else:
            self.logger.log("User \"" + _userName + "\" exists in database")

        # check is user is current
        if self.scraperDatabase["pcbUsers"].find_one({'userID': _userName, 'current': True}) and not _refreshFlag:
            self.logger.log(_userName+" is current")
            return

        # Get Repos
        self.logger.log("git.get_user(\""+_userName+"\").get_repos()")

        # repoCount = 0  # debugging
        for userRepo in self.git.get_user(_userName).get_repos():
            # check if repo exists in DB
            if not self.scraperDatabase["pcbRepos"].find_one({'userID': _userName, 'repoName': userRepo.name}):
                self.logger.log("Adding Repo \"" +
                                userRepo.name + "\" to database")
                repo_id = self.scraperDatabase["pcbRepos"].insert_one(
                    {'userID': _userName, 'repoName': userRepo.name, "files": []}).inserted_id
            else:
                self.logger.log("Repo Exists in database:" +
                                _userName+"\\" + userRepo.name)
                repo_id = self.scraperDatabase["pcbRepos"].find_one(
                    {'userID': _userName, 'repoName': userRepo.name}).get('_id')

             # add repo to user
            if not self.scraperDatabase["pcbUsers"].find_one({'userID': _userName, 'userRepos.name': userRepo.name}):
                self.logger.log("Adding Repo \""+userRepo.name +
                                "\" to user \"" + _userName+"\"")
                self.scraperDatabase["pcbUsers"].update_one({'userID': _userName}, {
                    '$push': {'userRepos': {'name': userRepo.name, 'dbID': repo_id, 'current': False}}})
            else:
                self.logger.log("Repo \"" + userRepo.name +
                                "\" exists for \"" + _userName+"\"")

            # debugging
            #repoCount = repoCount+1
            # if repoCount > 10:
                # break

        self.scraperDatabase["pcbUsers"].update_one(
            {'userID': _userName}, {'$set': {'current': True}})

###########################
    def updateRepos(self, _userName, _refreshFlag=False):
        self.logger.log("gitScraper.updateRepos(" +
                        _userName+","+str(_refreshFlag)+")")
        # loop though repos on user

        userDBRepoList = self.scraperDatabase["pcbUsers"].find(
            {'userID': _userName}).next()['userRepos']

        for userDBRepo in userDBRepoList:

            # check if current or refresh flag
            if userDBRepo['current'] and not _refreshFlag:
                self.logger.log("DB Repo " + userDBRepo['name']+" current")
            else:
                self.logger.log(
                    "get_repo("+_userName+"/"+userDBRepo['name']+")")
                remoteRepo = self.git.get_repo(
                    _userName+"/"+userDBRepo['name'])
                contents = []
                try:
                    contents = remoteRepo.get_contents("")
                except:
                    self.logger.log("Contents Empty)")
                    contents = []

                fileNums = 0
                # loop though files
                while contents:
                    file_content = contents.pop(0)
                    if file_content.type == "dir":
                        try:
                            contents.extend(
                                remoteRepo.get_contents(file_content.path))
                            self.logger.log(
                                "Extending "+file_content.path)
                        except:
                            self.logger.log(
                                "Error Extending "+file_content.path)
                    else:
                        self.logger.log("Check "+str(file_content.path))
                        # add file to repo entry
                        if not self.scraperDatabase["pcbRepos"].find_one({'_id': userDBRepo['dbID'], 'files.sha': file_content.sha}):
                            self.logger.log(
                                "Adding to Repo DB Doc "+file_content.path)
                            self.scraperDatabase["pcbRepos"].update_one({'_id': userDBRepo['dbID']}, {'$push': {'files': {
                                                                        'name': file_content.name, 'path': file_content.path, 'sha': file_content.sha, 'download_url': file_content.download_url, 'size': file_content.size}}})
                        else:
                            self.logger.log(
                                "File already in Repo DB Doc "+str(file_content.path))

                    fileNums = fileNums+1
                    if fileNums > self.CONTENT_FILE_CAP:
                        self.logger.log("Capped at %5d Files" %
                                        (self.CONTENT_FILE_CAP))
                        break
                try:
                    del file_content
                except:
                    self.logger.log("Error del file_content")
                # set flag current
                self.scraperDatabase["pcbUsers"].update_one(
                    {'userID': _userName, 'userRepos.name': userDBRepo['name']}, {'$set': {'userRepos.$.current': True}})

            # Stop after one repo for debug
            # break
