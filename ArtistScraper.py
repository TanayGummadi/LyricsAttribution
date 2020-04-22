import lyricsgenius
import json
import threading
import concurrent.futures
import sys

class ArtistScraper:

    def __init__(self, filename):
        self.lock = threading.Lock()
        self.threadList = []
        self.curThread = 0;

        self.filename = filename+".json"
        open(self.filename, "w").close()

        self.access_token = ""
        with open("access_token.txt", "r") as tokenFile:
            self.access_token = tokenFile.read()
        self.genius = lyricsgenius.Genius(self.access_token)
        self.genius.excluded_terms = ["(Remix)", "(Live)", "(Extended Version)"]
        self.genius.remove_section_headers = True
        self.genius.skip_non_songs = True

    def scrapeSongs(self, artist, amount):
        artist = self.genius.search_artist(artist, max_songs=amount)
        with self.lock:
            self.curThread += 1
            songDict = {}
            songDict[artist.name] = {song.title : song.lyrics for song in artist.songs}
            outstr = json.dumps(songDict)
            if(self.curThread != 1):
                outstr = outstr.replace("{", ", ", 1)   #Add commas to separate artists
            if(self.curThread != len(self.threadList)):
                outstr = outstr[:-1]    #Kick closing brace of each dict except for last artist
            with open(self.filename, "a") as writeFile:
                writeFile.write(outstr)
            songDict.clear()

    def insertArtist(self, artist, amount):
        curThread = threading.Thread(target=self.scrapeSongs, args=(artist, amount))
        self.threadList.append(curThread)

    def runScraper(self):
        for thread in self.threadList:
            thread.start()
        for thread in self.threadList:
            thread.join()

if __name__== "__main__":
    if(len(sys.argv) != 2):
        print("Invalid args")
        sys.exit(1)
    totalArtists = input("Enter total amount of artists to pull songs for: ")
    while(not totalArtists.isdigit()):
        totalArtists = input("Given value is not valid, please enter total amount of artists to pull songs for: ")
    totalArtists = int(totalArtists)
    ArtistScraper = ArtistScraper(sys.argv[1]);
    for i in range(int(totalArtists)):
        artistName = input("Enter artist {} name: ".format(i+1))
        artistAmount = input("Enter amount of songs for {}: ".format(artistName))
        while(not artistAmount.isdigit()):
            artistAmount = input("Given value is not valid, please enter amount of songs for {}: ".format(artistName))
        ArtistScraper.insertArtist(artistName, int(artistAmount))
    print("Starting scraper...")
    ArtistScraper.runScraper()
    print("Finished scraping to {}.json".format(sys.argv[1]))
