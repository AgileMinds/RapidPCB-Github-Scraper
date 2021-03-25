# gitScraper.py from gitScraper import gitScraper

import pymongo
import os
from pyLog import pyLogger
from github import Github


class gitScraper:

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

        self.scraperDatabase["pcbUsers"].update_one(
            {'userID': _userName}, {'$set': {'current': True}})

    def updateRepos(self, _userName, _refreshFlag=False):
        self.logger.log("gitScraper.updateRepos(" +
                        _userName+","+str(_refreshFlag)+")")
        # loop though repos on user
        userRepoLen = self.scraperDatabase["pcbUsers"].find({'userID': _userName})[
            'userRepos'].length
        print(userRepoLen)
        # check if current or refresh flag

        # loop though files and add to repo
