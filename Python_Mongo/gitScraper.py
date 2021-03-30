# gitScraper.py from gitScraper import gitScraper

import pymongo
import os
from pyLog import pyLogger
from github import Github
from pathlib import Path
import requests
import hashlib


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
            # repoCount = repoCount+1
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

###########################
    def pcbBoardFilter(self, _userName, _cadType='Eagle'):
        self.logger.log("gitScraper.pcbBoardFilter(" +
                        _userName+","+_cadType+")")

        # define file extentions to search

        if _cadType == 'Eagle':
            _searchExt = ['.brd', '.sch']
            self.logger.log("_searchExt=['.brd','.sch']")

        else:
            _searchExt = ['.brd', '.sch']
            self.logger.log("_searchExt=['.brd','.sch']")

        # loop though repos on user
        userDBRepoList = self.scraperDatabase["pcbUsers"].find(
            {'userID': _userName}).next()['userRepos']

        for userDBRepo in userDBRepoList:
            self.logger.log("Checking " + userDBRepo['name']+" for CAD Files")
            # get file list

            fileNames = []
            filePaths = []
            fileSHAs = []
            fileDownloadURLs = []
            fileSizes = []
            fileExts = []
            fileExtIndex = []
            fileFolders = []
            numFiles = 0

            fileList = self.scraperDatabase["pcbRepos"].find(
                {'_id': userDBRepo['dbID']}).next()['files']

            for f in fileList:
                fileNames.append(f['name'])
                filePaths.append(f['path'])
                fileSHAs.append(f['sha'])
                fileDownloadURLs.append(f['download_url'])
                fileSizes.append(f['size'])
                fileExt = Path(f['name']).suffix
                fileExts.append(fileExt)
                if fileExt in _searchExt:
                    fileExtIndex.append(_searchExt.index(fileExt))
                else:
                    fileExtIndex.append(-1)
                fileFolders.append(str(Path(f['path']).parent))
                numFiles = numFiles+1

            # search for matching extention
            for i in range(numFiles):
                # find board files
                if fileExtIndex[i] == 0:
                    self.logger.log("Board File "+filePaths[i])
                    # find matching sch files
                    for j in range(numFiles):
                        if fileExtIndex[j] == 1 and fileFolders[i] == fileFolders[j] and Path(filePaths[i]).stem == Path(filePaths[i]).stem:
                            self.logger.log("Schematic File"+filePaths[j])
                            # define project name
                            projectName = Path(filePaths[i]).stem

                            try:

                                if not self.scraperDatabase["pcbBoards"].find_one({'userID': _userName, 'name': projectName}):
                                    self.logger.log(
                                        "Adding "+projectName+" to Database pcbBoards")
                                    doc_id = self.scraperDatabase["pcbBoards"].insert_one(
                                        {'userID': _userName, 'name': projectName, 'cadType': _cadType, 'quotes': [], 'partsList': [], 'files': []}).inserted_id

                                    # Download files
                                    self.logger.log(
                                        "Downloading Board File: \""+fileDownloadURLs[i]+"\"")
                                    req = requests.get(
                                        fileDownloadURLs[i], allow_redirects=True)
                                    boardFile = req.content
                                    fileHash = hashlib.sha224(
                                        boardFile).digest()
                                    boardFile = boardFile.decode(
                                        'utf-8', 'ignore')

                                    if not self.scraperDatabase["pcbFiles"].find_one({'fileHash': fileHash}):
                                        file_id = self.scraperDatabase["pcbFiles"].insert_one(
                                            {'fileName': fileNames[i], 'fileHash': fileHash, 'fileContents': boardFile}).inserted_id
                                        self.logger.log(
                                            "Uploading File: \""+fileNames[i]+"\"")
                                    else:
                                        file_id = self.scraperDatabase["pcbFiles"].find_one(
                                            {'fileHash': fileHash}).get('_id')
                                        self.logger.log(
                                            "File Exists: \""+fileNames[i]+"\", HASH=\""+str(fileHash)+"\"")

                                    self.logger.log(
                                        "Linking File: \""+fileNames[i]+"\" to \""+projectName+"\"")
                                    self.scraperDatabase["pcbBoards"].update_one({'_id': doc_id}, {'$push': {
                                        'files': {'fileName': fileNames[i], 'filetype': fileExts[i], 'fileHash': fileHash}}})

                                    self.logger.log(
                                        "Downloading Schematic File: \""+fileDownloadURLs[j]+"\"")
                                    req = requests.get(
                                        fileDownloadURLs[j], allow_redirects=True)
                                    schematicFile = req.content
                                    fileHash = hashlib.sha224(
                                        schematicFile).digest()
                                    schematicFile = schematicFile.decode(
                                        'utf-8', 'ignore')

                                    if not self.scraperDatabase["pcbFiles"].find_one({'fileHash': fileHash}):
                                        file_id = self.scraperDatabase["pcbFiles"].insert_one(
                                            {'fileName': fileNames[j], 'fileHash': fileHash, 'fileContents': schematicFile}).inserted_id
                                        self.logger.log(
                                            "Uploading File: \""+fileNames[j]+"\"")
                                    else:
                                        file_id = self.scraperDatabase["pcbFiles"].find_one(
                                            {'fileHash': fileHash}).get('_id')
                                        self.logger.log(
                                            "File Exists: \""+fileNames[j]+"\", HASH=\""+str(fileHash)+"\"")

                                    self.logger.log(
                                        "Linking File: \""+fileNames[j]+"\" to \""+projectName+"\"")
                                    self.scraperDatabase["pcbBoards"].update_one({'_id': doc_id}, {'$push': {
                                        'files': {'fileName': fileNames[j], 'filetype': fileExts[j], 'fileHash': fileHash}}})

                                else:
                                    self.logger.log(
                                        "Board "+projectName+" Exists in Database pcbBoards")
                            except:
                                self.logger.log(
                                    "Error with \""+projectName+"\"")
                                if self.scraperDatabase["pcbBoards"].find_one({'userID': _userName, 'name': projectName}):
                                    self.scraperDatabase["pcbBoards"].delete_one(
                                        {'userID': _userName, 'name': projectName})
                                    self.logger.log(
                                        "Removing \""+projectName+"\"")

            # Stop after one repo for debug
            # break
