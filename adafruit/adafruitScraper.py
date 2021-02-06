#python3 "C:\Users\tomca\OneDrive\Documents\GitHub\RapidPCB-Github-Scraper\adafruit\adafruitScraper.py"

from github import Github
import os
import pickle
import requests

ACCESS_TOKEN = '1fdedfe0c7da6b1eceacdec4a339ef580936b139'
viableSavingLoc = 'C:\\Users\\tomca\\OneDrive\\Documents\\GitHub\\RapidPCB-Github-Scraper\\adafruit'
downloadloc = 'C:\\Users\\tomca\\Dropbox\\RapidPCB\\Part Data\\adafruit\\PCBs'
userName="adafruit"

updateUserRepos = True
updateFileContents = True
updateDownloadList = True
contentFileCap=1000

fileSeachExtentions=["sch","brd","lbr"]

print("Starting adafruit Scraper")



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

adafruitRepos=githubScraperUserRepos(userName)

print("///////////////")
print("Scanning all Repo by "+ adafruitRepos.repoUser)


if os.path.exists(viableSavingLoc+"\\adafruitRepos.pickle"):
	print("Loading Repos Vars")
	adafruitRepos.loadPickle(viableSavingLoc+"\\adafruitRepos.pickle")
	print("Loading Repos in "+ viableSavingLoc+"\\adafruitRepos.pickle")
	

addedRepoFlag=False

if updateUserRepos:
	print("Checking Github list of Repos")
	for userRepos in g.get_user(adafruitRepos.repoUser).get_repos():
		#print(userRepos.name)
		if not userRepos.name in adafruitRepos.repoNames:
			adafruitRepos.addRepo(userRepos)
			print("Adding "+userRepos.name)
			addedRepoFlag=True
else:
	print("Using Perviously saved Repos")


print("Number of Repos = %3d"%(adafruitRepos.repoNums))

if addedRepoFlag:
	adafruitRepos.dumpPickle(viableSavingLoc+"\\adafruitRepos.pickle")
else:
	print("No new Repos added")

testVar=0

for repoName in adafruitRepos.repoNames:

	#Check if REPO is SCRAPED and correct pickle exists
	if adafruitRepos.getScrapedRepoByName(repoName) and os.path.exists(viableSavingLoc+"\\adafruitRepos_"+repoName+".pickle") and not updateFileContents:
		print("/// "+adafruitRepos.repoUser+"/"+repoName+"  already scraped")
	else:
	
	
		print("///////////////")
		print("Scraping Contents of "+adafruitRepos.repoUser+"/"+repoName)
		
		adafruitContentFiles=githubScraperContentFiles(repoName)
		
		try:
			repo=g.get_repo(adafruitRepos.repoUser+"/"+repoName)
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
					adafruitContentFiles.addContentFiles(file_content)

				if adafruitContentFiles.fileNums>contentFileCap:
					print("Capped at %5d Files"%(contentFileCap))
					break
					
				del file_content
			
			print("Number of Files = %3d"%(adafruitContentFiles.fileNums))
			
			print("Saving ContentFiles in "+ viableSavingLoc+"\\adafruitRepos_"+repoName+".pickle")
			adafruitContentFiles.dumpPickle(viableSavingLoc+"\\adafruitRepos_"+repoName+".pickle")
			
			adafruitRepos.setScrapedRepoByName(repoName,True)
			adafruitRepos.dumpPickle(viableSavingLoc+"\\adafruitRepos.pickle")
			print("Saving scrapted Repos in "+ viableSavingLoc+"\\adafruitRepos.pickle")
			
		except:
			print("Error with "+adafruitRepos.repoUser+"/"+repoName)
		
		del adafruitContentFiles
		
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

adafruitContentFiles=githubScraperDownloadList()
if os.path.exists(viableSavingLoc+"\\adafruitDownloadList.pickle") and not updateDownloadList:
	print("Loading download list from "+viableSavingLoc+"\\adafruitDownloadList.pickle")
	adafruitContentFiles.loadPickle(viableSavingLoc+"\\adafruitDownloadList.pickle")
else:
	print("Fresh download list at "+viableSavingLoc+"\\adafruitDownloadList.pickle")

for j in range(numExtCheck):
	print("Scanning for \""+fileSeachExtentions[j]+"\" extentions")

for repoName in adafruitRepos.repoNames:

	print("/// Filtering Files from  "+adafruitRepos.repoUser+"/"+repoName)
		
	if os.path.exists(viableSavingLoc+"\\adafruitRepos_"+repoName+".pickle"):
		adafruitContentFiles=githubScraperContentFiles(repoName)
		adafruitContentFiles.loadPickle(viableSavingLoc+"\\adafruitRepos_"+repoName+".pickle")
		#print("Number of Files in Loaded Pickle = %3d"%(adafruitContentFiles.fileNums))
		
		if all(adafruitContentFiles.fileScraped) and not updateDownloadList:
			print("Already Searched")
		else:
			for i in range(adafruitContentFiles.fileNums):
				#print("/////")
				#print(adafruitContentFiles.fileNames[i])
				#print(adafruitContentFiles.filePaths[i])
				#print(adafruitContentFiles.fileDownloadURLs[i])
				extentionFlag=False
				
				if not adafruitContentFiles.fileScraped[i] or updateDownloadList:
					for j in range(numExtCheck):
						if adafruitContentFiles.fileNames[i].endswith(fileSeachExtentions[j]):
							extentionFlag=True
					
					if extentionFlag:
						adafruitContentFiles.addDownloadFile(adafruitContentFiles.fileDownloadURLs[i],downloadloc+"\\"+repoName+"\\"+adafruitContentFiles.filePaths[i])
						print("Adding \""+adafruitContentFiles.filePaths[i]+"\" to downloadlist")
				
				adafruitContentFiles.fileScraped[i]=True
			
			adafruitContentFiles.dumpPickle(viableSavingLoc+"\\adafruitRepos_"+repoName+".pickle")
			adafruitContentFiles.dumpPickle(viableSavingLoc+"\\adafruitDownloadList.pickle")
			print("Search Finished")
	
	else:
		print("/// Files does not exist "+viableSavingLoc+"\\adafruitRepos_"+repoName+".pickle")
	
	
print("Downloadlist is Compiled #Files = %5d"%adafruitContentFiles.fileNums)

for i in range(adafruitContentFiles.fileNums):
	print("Checking "+adafruitContentFiles.fileSavePath[i])

	if os.path.exists(adafruitContentFiles.fileSavePath[i]):
		print("//"+adafruitContentFiles.fileSavePath[i]+" Already Exists")
	else:
		try:
			#print(os.path.dirname(adafruitContentFiles.fileSavePath[i]))
			if not os.path.exists(os.path.dirname(adafruitContentFiles.fileSavePath[i])):
				#print("Make Dir")
				os.makedirs(os.path.dirname(adafruitContentFiles.fileSavePath[i]))
			
			print("Downloading "+adafruitContentFiles.fileDownloadURLs[i])
			req = requests.get(adafruitContentFiles.fileDownloadURLs[i], allow_redirects=True)
			
			open(adafruitContentFiles.fileSavePath[i], 'wb').write(req.content)
			adafruitContentFiles.fileDownloaded[i]=True
			adafruitContentFiles.dumpPickle(viableSavingLoc+"\\adafruitDownloadList.pickle")
			
			print("Download Complete")
			
		except:
			print("Error downloading "+adafruitContentFiles.fileDownloadURLs[i]+" to "+adafruitContentFiles.fileSavePath[i])
		

			
	
	
