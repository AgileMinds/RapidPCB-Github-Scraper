#python3 "C:\Users\tomca\OneDrive\Documents\GitHub\RapidPCB-Github-Scraper\Sparkfun\SparkfunScraper.py"

from github import Github
import os
import pickle
import requests

ACCESS_TOKEN = '1fdedfe0c7da6b1eceacdec4a339ef580936b139'
viableSavingLoc = 'C:\\Users\\tomca\\OneDrive\\Documents\\GitHub\\RapidPCB-Github-Scraper\\Sparkfun'
downloadloc = 'C:\\Users\\tomca\\Dropbox\\RapidPCB\\Part Data\\Sparkfun\\PCBs'
userName="sparkfun"

updateUserRepos = False
updateFileContents = False
updateDownloadList = False
contentFileCap=1000

fileSeachExtentions=["sch","brd"]

print("Starting Sparkfun Scraper")



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
			self.fileNums = pickle.load(f)
			
	
class githubScraperDownloadList:
	fileNums=0
	fileDownloadURLs=[]
	fileSavePath=[]
	fileDownloaded=[]

	
	def addDownloadFile(self,downLoadURL,savePath):
		self.fileDownloadURLs.append(downLoadURL)
		self.fileSavePath.append(savePath)
		self.fileDownloaded.append(False)
		self.fileNums=self.fileNums+1
		
	def dumpPickle(self,pickleFile):
		with open(pickleFile, 'wb') as f:
			pickle.dump(self.fileDownloadURLs, f, pickle.HIGHEST_PROTOCOL)
			pickle.dump(self.fileSavePath, f, pickle.HIGHEST_PROTOCOL)
			pickle.dump(self.fileDownloaded, f, pickle.HIGHEST_PROTOCOL)
			pickle.dump(self.fileNums, f, pickle.HIGHEST_PROTOCOL)
	
	def loadPickle(self,pickleFile):
		with open(pickleFile, 'rb') as f:
			self.fileDownloadURLs = pickle.load(f)
			self.fileSavePath = pickle.load(f)
			self.fileDownloaded = pickle.load(f)
			self.fileNums = pickle.load(f)
		
	

g = Github(ACCESS_TOKEN)

sparkfunRepos=githubScraperUserRepos(userName)

print("///////////////")
print("Scanning all Repo by "+ sparkfunRepos.repoUser)


if os.path.exists(viableSavingLoc+"\\SparkfunRepos.pickle"):
	print("Loading Repos Vars")
	sparkfunRepos.loadPickle(viableSavingLoc+"\\SparkfunRepos.pickle")
	print("Loading Repos in "+ viableSavingLoc+"\\SparkfunRepos.pickle")
	

addedRepoFlag=False

if updateUserRepos:
	print("Checking Github list of Repos")
	for userRepos in g.get_user(sparkfunRepos.repoUser).get_repos():
		#print(userRepos.name)
		if not userRepos.name in sparkfunRepos.repoNames:
			sparkfunRepos.addRepo(userRepos)
			print("Adding "+userRepos.name)
			addedRepoFlag=True
else:
	print("Using Perviously saved Repos")


print("Number of Repos = %3d"%(sparkfunRepos.repoNums))

if addedRepoFlag:
	sparkfunRepos.dumpPickle(viableSavingLoc+"\\SparkfunRepos.pickle")
else:
	print("No new Repos added")

testVar=0

for repoName in sparkfunRepos.repoNames:

	#Check if REPO is SCRAPED and correct pickle exists
	if sparkfunRepos.getScrapedRepoByName(repoName) and os.path.exists(viableSavingLoc+"\\SparkfunRepos_"+repoName+".pickle") and not updateFileContents:
		print("/// "+sparkfunRepos.repoUser+"/"+repoName+"  already scraped")
	else:
	
	
		print("///////////////")
		print("Scraping Contents of "+sparkfunRepos.repoUser+"/"+repoName)
		
		sparkfunContentFiles=githubScraperContentFiles(repoName)
		
		try:
			repo=g.get_repo(sparkfunRepos.repoUser+"/"+repoName)
			try:
				contents = repo.get_contents("")
			except:
				#repo is empty
				contents=[]
			
			while contents:
				file_content = contents.pop(0)
				if file_content.type == "dir":
					try:
						contents.extend(repo.get_contents(file_content.path))
					except:
						print("Error Extending "+file_content.path)
				else:
					print("adding "+file_content.path)
					sparkfunContentFiles.addContentFiles(file_content)

				if sparkfunContentFiles.fileNums>contentFileCap:
					print("Capped at %5d Files"%(contentFileCap))
					break
					
				del file_content
			
			print("Number of Files = %3d"%(sparkfunContentFiles.fileNums))
			
			print("Saving ContentFiles in "+ viableSavingLoc+"\\SparkfunRepos_"+repoName+".pickle")
			sparkfunContentFiles.dumpPickle(viableSavingLoc+"\\SparkfunRepos_"+repoName+".pickle")
			
			sparkfunRepos.setScrapedRepoByName(repoName,True)
			sparkfunRepos.dumpPickle(viableSavingLoc+"\\SparkfunRepos.pickle")
			print("Saving scrapted Repos in "+ viableSavingLoc+"\\SparkfunRepos.pickle")
			
		except:
			print("Error with "+sparkfunRepos.repoUser+"/"+repoName)
		
		del sparkfunContentFiles
		
		try:
			del repo
		except:
			print("Error Deleteing repo")
			
		try:
			del contents
		except:
			print("Error Deleteing contents")
		
		

#Create download list
numExtCheck=len(fileSeachExtentions)

sparkfunDownloadList=githubScraperDownloadList()
if os.path.exists(viableSavingLoc+"\\SparkfunDownloadList.pickle") and not updateDownloadList:
	print("Loading download list from "+viableSavingLoc+"\\SparkfunDownloadList.pickle")
	sparkfunDownloadList.loadPickle(viableSavingLoc+"\\SparkfunDownloadList.pickle")
else:
	print("Fresh download list at "+viableSavingLoc+"\\SparkfunDownloadList.pickle")

for j in range(numExtCheck):
	print("Scanning for \""+fileSeachExtentions[j]+"\" extentions")

for repoName in sparkfunRepos.repoNames:

	print("/// Filtering Files from  "+sparkfunRepos.repoUser+"/"+repoName)
		
	if os.path.exists(viableSavingLoc+"\\SparkfunRepos_"+repoName+".pickle"):
		sparkfunContentFiles=githubScraperContentFiles(repoName)
		sparkfunContentFiles.loadPickle(viableSavingLoc+"\\SparkfunRepos_"+repoName+".pickle")
		#print("Number of Files in Loaded Pickle = %3d"%(sparkfunContentFiles.fileNums))
		
		if all(sparkfunContentFiles.fileScraped) and not updateDownloadList:
			print("Already Searched")
		else:
			for i in range(sparkfunContentFiles.fileNums):
				#print("/////")
				#print(sparkfunContentFiles.fileNames[i])
				#print(sparkfunContentFiles.filePaths[i])
				#print(sparkfunContentFiles.fileDownloadURLs[i])
				extentionFlag=False
				
				if not sparkfunContentFiles.fileScraped[i] or updateDownloadList:
					for j in range(numExtCheck):
						if sparkfunContentFiles.fileNames[i].endswith(fileSeachExtentions[j]):
							extentionFlag=True
					
					if extentionFlag:
						sparkfunDownloadList.addDownloadFile(sparkfunContentFiles.fileDownloadURLs[i],downloadloc+"\\"+repoName+"\\"+sparkfunContentFiles.filePaths[i])
						print("Adding \""+sparkfunContentFiles.filePaths[i]+"\" to downloadlist")
				
				sparkfunContentFiles.fileScraped[i]=True
			
			sparkfunContentFiles.dumpPickle(viableSavingLoc+"\\SparkfunRepos_"+repoName+".pickle")
			sparkfunDownloadList.dumpPickle(viableSavingLoc+"\\SparkfunDownloadList.pickle")
			print("Search Finished")
	
	else:
		print("/// Files does not exist "+viableSavingLoc+"\\SparkfunRepos_"+repoName+".pickle")
	
	
print("Downloadlist is Compiled #Files = %5d"%sparkfunDownloadList.fileNums)

for i in range(sparkfunDownloadList.fileNums):
	print("Checking "+sparkfunDownloadList.fileSavePath[i])

	if os.path.exists(sparkfunDownloadList.fileSavePath[i]):
		print("//"+sparkfunDownloadList.fileSavePath[i]+" Already Exists")
	else:
		try:
			#print(os.path.dirname(sparkfunDownloadList.fileSavePath[i]))
			if not os.path.exists(os.path.dirname(sparkfunDownloadList.fileSavePath[i])):
				#print("Make Dir")
				os.makedirs(os.path.dirname(sparkfunDownloadList.fileSavePath[i]))
			
			print("Downloading "+sparkfunDownloadList.fileDownloadURLs[i])
			req = requests.get(sparkfunDownloadList.fileDownloadURLs[i], allow_redirects=True)
			
			open(sparkfunDownloadList.fileSavePath[i], 'wb').write(req.content)
			sparkfunDownloadList.fileDownloaded[i]=True
			sparkfunDownloadList.dumpPickle(viableSavingLoc+"\\SparkfunDownloadList.pickle")
			
			print("Download Complete")
			
		except:
			print("Error downloading "+sparkfunDownloadList.fileDownloadURLs[i]+" to "+sparkfunDownloadList.fileSavePath[i])
		

			
	
	
