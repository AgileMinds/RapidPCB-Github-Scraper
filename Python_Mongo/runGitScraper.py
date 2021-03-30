from gitScraper import gitScraper
from secret import secureInputs

userName = "adafruit"

severString = "mongodb+srv://"+secureInputs.MONGODB_USER+":"+secureInputs.MONGODB_PASSWORD + \
    "@rapidpcb.m3xrw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

locStorageDir = "Z:\\Tom Documents\\Git Scraper Data"

userScraper = gitScraper(secureInputs.GIT_ACCESS_TOKEN,
                         severString, "PartStudy2", locStorageDir)

# userScraper.updateUser(userName)
# userScraper.updateRepos(userName)
# userScraper.pcbBoardFilter(userName)

userName = "sparkfun"

# userScraper.updateUser(userName)
# userScraper.updateRepos(userName)
# userScraper.pcbBoardFilter(userName)
