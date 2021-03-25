from gitScraper import gitScraper
from secret import secureInputs

userName = "adafruit"

severString = "mongodb+srv://"+secureInputs.MONGODB_USER+":"+secureInputs.MONGODB_PASSWORD + \
    "@rapidpcb.m3xrw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

userScraper = gitScraper(secureInputs.GIT_ACCESS_TOKEN,
                         severString, "PartStudy2")

userScraper.updateUser(userName)

userScraper.updateRepos(userName)
