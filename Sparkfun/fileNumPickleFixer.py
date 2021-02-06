#python3 "C:\Users\tomca\OneDrive\Documents\GitHub\RapidPCB-Github-Scraper\Sparkfun\fileNumPickleFixer.py"

from github import Github
import os
import pickle

ACCESS_TOKEN = '1fdedfe0c7da6b1eceacdec4a339ef580936b139'
viableSavingLoc = 'C:\\Users\\tomca\\OneDrive\\Documents\\GitHub\\RapidPCB-Github-Scraper\\Sparkfun'

userName="sparkfun"

updateReposFlag = False
contentFileCap=1000

class githubScraperUserRepos:
	repoNums=0
	repoNames=[]
	repoScraped=[]
	repoLoaded=False
	
	def __init__(self,user):
		self.repoUser=user
		
	def addRepo(self,userRepo):
		self.repoNames.append(userRepos.name)
		self.repoNums=self.repoNums+1
		self.repoScraped.append(False)
		
	def existsRepo(self,userRepo):
		return (userRepo.name in self.repoNames)
		
	def indexRepoByName(self,repoName):
		return self.repoNames.index(repoName)
		
	def getScrapedRepoByName(self,repoName):
		return self.repoScraped[self.indexRepoByName(repoName)]
		
	def setScrapedRepoByName(self,repoName,val):
		self.repoScraped[self.indexRepoByName(repoName)]=val
	
	def dumpPickle(self,pickleFile):
		with open(pickleFile, 'wb') as f:
			pickle.dump(self.repoUser, f, pickle.HIGHEST_PROTOCOL)
			pickle.dump(self.repoNums, f, pickle.HIGHEST_PROTOCOL)
			pickle.dump(self.repoNames, f, pickle.HIGHEST_PROTOCOL)
			pickle.dump(self.repoScraped, f, pickle.HIGHEST_PROTOCOL)
			pickle.dump(self.repoLoaded, f, pickle.HIGHEST_PROTOCOL)
	
	def loadPickle(self,pickleFile):
		with open(pickleFile, 'rb') as f:
			self.repoUser = pickle.load(f)
			self.repoNums = pickle.load(f)
			self.repoNames = pickle.load(f)
			self.repoScraped = pickle.load(f)
			self.repoLoaded = pickle.load(f)
			
			
class githubScraperContentFiles:
	fileNums=0
	fileNames=[]
	filePaths=[]
	fileSHAs=[]
	fileDownloadURLs=[]
	fileSizes=[]
	
	fileScraped=[]
	
	def __init__(self,_repoName):
		self.repoName=_repoName
		
	def addContentFiles(self,contentFile):
		self.fileNames.append(contentFile.name)
		self.filePaths.append(contentFile.path)
		self.fileSHAs.append(contentFile.sha)
		self.fileDownloadURLs.append(contentFile.download_url)
		self.fileSizes.append(contentFile.size)
		self.fileScraped.append(False)
		self.fileNums=self.fileNums+1
	
	def dumpPickle(self,pickleFile):
		with open(pickleFile, 'wb') as f:
			pickle.dump(self.repoName, f, pickle.HIGHEST_PROTOCOL)
			pickle.dump(self.fileNames, f, pickle.HIGHEST_PROTOCOL)
			pickle.dump(self.filePaths, f, pickle.HIGHEST_PROTOCOL)
			pickle.dump(self.fileSHAs, f, pickle.HIGHEST_PROTOCOL)
			pickle.dump(self.fileDownloadURLs, f, pickle.HIGHEST_PROTOCOL)
			pickle.dump(self.fileSizes, f, pickle.HIGHEST_PROTOCOL)
			pickle.dump(self.fileScraped, f, pickle.HIGHEST_PROTOCOL)
			pickle.dump(self.fileNums, f, pickle.HIGHEST_PROTOCOL)
	
	def loadPickle(self,pickleFile):
		with open(pickleFile, 'rb') as f:
			self.repoName = pickle.load(f)
			self.fileNames = pickle.load(f)
			self.filePaths = pickle.load(f)
			self.fileSHAs = pickle.load(f)
			self.fileDownloadURLs = pickle.load(f)
			self.fileSizes = pickle.load(f)
			self.fileScraped = pickle.load(f)
			#self.fileNums = pickle.load(f)


sparkfunRepos=githubScraperUserRepos(userName)

if os.path.exists(viableSavingLoc+"\\SparkfunRepos.pickle"):
	print("Loading Repos Vars")
	sparkfunRepos.loadPickle(viableSavingLoc+"\\SparkfunRepos.pickle")
	print("Loading Repos in "+ viableSavingLoc+"\\SparkfunRepos.pickle")
	
	
for repoName in sparkfunRepos.repoNames:

	sparkfunContentFiles=githubScraperContentFiles(repoName)
	
	sparkfunContentFiles.loadPickle(viableSavingLoc+"\\SparkfunRepos_"+repoName+".pickle")
	
	print("Number of Files in Loaded Pickle = %3d"%(sparkfunContentFiles.fileNums))
	
	sparkfunContentFiles.fileNums=len(sparkfunContentFiles.fileNames)
	
	print("Number of Files = %3d"%(sparkfunContentFiles.fileNums))
	
	sparkfunContentFiles.dumpPickle(viableSavingLoc+"\\SparkfunRepos_"+repoName+".pickle")
	
	del sparkfunContentFiles
	
