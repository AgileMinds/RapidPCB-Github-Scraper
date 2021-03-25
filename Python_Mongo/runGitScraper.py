from gitScraper import gitScraper

ACCESS_TOKEN = '1fdedfe0c7da6b1eceacdec4a339ef580936b139'
userName = "adafruit"

mongoDBPassword = 'U6HE8AaikAaCsROw'
mongoDBUser = "tom_p50_dev"

severString = "mongodb+srv://"+mongoDBUser+":"+mongoDBPassword + \
    "@rapidpcb.m3xrw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

userScraper = gitScraper(ACCESS_TOKEN, severString, "PartStudy2")

userScraper.updateUser(userName)

userScraper.updateRepos(userName)
