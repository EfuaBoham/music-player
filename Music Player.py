#Project by Maame Yaa Osei, Maame Efua Boham & Nana Ama Parker
#Music Player

#Importing libraries 
import pygame
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
import os
from tkinter.filedialog import *
from tkinter import *
from HashTable import *

#Creating window in Tkinter, setting its size and title
root = Tk()
root.minsize(500,500)
root.title("A8 MUSIC PLAYER")

#Setting popup labels
label = StringVar()
songLabel = Label(root,textvariable=label, width = 70)


'''
    Artiste class takes a name and has instance variables :
        - name
        - album
        - song

    There are the accessor methods:
        - getName: which retrieves the name of the artiste
        - getAlbums: which returns the albums of the artiste
        - getSongs: which returns the songs of the artiste

    There are the mutator methods:
        - addSong: which adds a song to the artiste's list of songs
        - addAlbum: which adds an album to the artiste's list of albums

    An __str__() method provides a string representation of the Artiste

    
    
'''
class Artiste:
    def __init__(self, name):
        self.name = name
        self.album = []
        self.song = []

    def addSong(self,song):
        (self.song).append(song)

    def addAlbum(self,album):
        (self.album).append(album)
    
    def getName(self):
        return self.name

    def getAlbums(self):
        for i in self.album:
            return(i)

    def getSongs(self):
        for i in self.song:
            return(i)

    def __str__(self):
        return (self.name)


'''
    Song class takes a title and has instance variables :
        - title
        - artiste
        - length
        - album

    There are the accessor methods:
        - getTitle: which retrieves the name of the song
        - getArtiste: which returns the artiste of the song
        - getAlbum: which returns the album containing the song
        - getLength: which returns the length of the song

    There are the mutator methods:
        - setLength: which passes a length to the self.length instance variable
        - setArtiste: which sets the artiste of the song
        - setAlbum: which sets the album of the song

    An __str__() method provides a string representation of the Song
    
'''           
class Song:
    def __init__(self,title):
        self.title = title
        self.artiste = None
        self.length = ""
        self.album = None

    def getTitle(self):
        return self.title

    def getArtiste(self):
        return self.artiste

    def getAlbum(self):
        return self.album
    
    def getLength(self):
        return str(round(self.length,2))+" seconds"

    def setLength(self,length):
        self.length = length

    def setArtiste(self,artiste):
        self.artiste = artiste

    def setAlbum(self,album):
        self.album = album

    def __str__(self):
        return (self.title)
 
'''
    Album class takes a title and has instance variables :
        - title
        - artiste
        - songs

    There are the accessor methods:
        - getTitle: which retrieves the name of the album
        - getArtiste: which returns the artiste of the album
        - getSongs: which returns the songs in the album

    There are the mutator methods:
        - setTitle: which sets the title of the album
        - addArtiste: which sets the artist of the album
        - addSong: which adds songs to the album

    An __str__() method provides a string representation of the Album
    
'''  
        
class Album:
    def __init__(self, title):
        self.title = title
        self.songs = []
        self.artiste = None


    def getTitle(self):
        return self.title

    def getSongs(self):
        for i in self.songs:
            return (i)

    def getArtiste(self):
        return self.artiste

    def setTitle(self, newTitle):
        self.Title = newTitle

    def addArtiste(self, newArtiste):
        self.artiste = newArtiste

    def addSong(self, song):
        self.songs.append(song)

    def __str__(self):
        return (self.title)

# Bradley N. Miller, David L. Ranum
# Introduction to Data Structures and Algorithms in Python
# Copyright 2005
#queue.py
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

# Bradley N. Miller, David L. Ranum
# Introduction to Data Structures and Algorithms in Python
# Copyright 2005
#stack.py
class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)



playQueue = Queue()             #creating an instance of the queue class
prevStack = Stack()             #creating an instance of the stack class
pygame.mixer.init()             #initializing pygame
songNames = []
songArtistes=[]                 #create lists to contain the artiste,length.
songLength=[]                   #and album metadata which is stripped from the songs
songAlbum = []
index = 0                       #creating index to loop through list of song names and label.


"""

    A function that accesses a selected directory,
    retrieves all songs with '.mp3' format, extracts the metadata using mutagen,
    and enqueues the .mp3 files
    
"""
def getMusicData():
    myDirectory = askdirectory()
    os.chdir(myDirectory)

    for files in os.listdir(myDirectory):
        if files.endswith(".mp3"):
            newDirectory = os.path.realpath(files)
            audio = ID3(newDirectory)
            audio_ = MP3(newDirectory)
            songNames.append(audio['TIT2'].text[0])
            songArtistes.append(audio['TPE1'].text[0])
            songAlbum.append(audio["TALB"].text[0])
            songLength.append(audio_.info.length)
            playQueue.enqueue(files)

getMusicData()


# A function that uses a global index to
# update the label of the song which is playing

def updateLabel():
    global index
    label.set("Now Playing: "+songNames[index])


# A function that takes an event as a parameter, dequeues a song, plays it,
# and calls the updateLabel() function.

def playSong(event):
    song = playQueue.dequeue()
    prevStack.push(song)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    updateLabel()

#A function that plays the next song in the queue as long as the queue is
#not empty and updates the label.
def nextSong(event):
    try:
        global index
        index += 1
        nextSong=(playQueue.dequeue())
        prevStack.push(nextSong)
        pygame.mixer.music.load(nextSong)
        pygame.mixer.music.play()
        updateLabel()
    except IndexError:
        pygame.mixer.music.stop()
        label.set("Queue is empty")

#A function that plays the previous song in the queue by popping it off a
#stack and updating the label.
def prevSong(event):
    try:
        global index
        index -= 1
        prevSong= prevStack.pop()
        pygame.mixer.music.load(prevSong)
        pygame.mixer.music.play()
        updateLabel()
        
    except IndexError:
        pygame.mixer.music.stop()
        label.set("No previous song")

#Funtcion to pause music
def pauseSong(event):
    pygame.mixer.music.pause()
    label.set("")

#Function to continue paused music
def continueSong(event):
    pygame.mixer.music.unpause()
    global index
    label.set("Now Playing:" + songNames[index])

#Function to stop music.
def stopSong(event):
    pygame.mixer.music.stop()
    label.set("")                        


#Creates a listbox to display queue of songs in Tkinter window. 
listBox = Listbox(root, width= 50)
listBox.pack()

#Reverses list of song names, inserts them in the listbox, and reverses it back to original order. 
songNames.reverse()
for names in songNames:
    listBox.insert(0,names)
songNames.reverse() 


#Creating buttons to handle events, labelling them and packing them into Tkinter window.
playButton = Button(root, text= 'Start Playing!')
playButton.pack()

nextButton = Button(root,text = 'Next Song')
nextButton.pack()

previousButton = Button(root,text = 'Previous Song')
previousButton.pack()

pauseButton = Button(root, text= 'Pause')
pauseButton.pack()

continueButton = Button(root, text= 'Continue')
continueButton.pack()

stopButton = Button(root,text='Stop Music')
stopButton.pack()

#Binding buttons created to their respective functions to enable event to execute on click.
playButton.bind("<Button-1>",playSong)
nextButton.bind("<Button-1>",nextSong)
previousButton.bind("<Button-1>",prevSong)
pauseButton.bind("<Button-1>",pauseSong)
continueButton.bind("<Button-1>",continueSong)
stopButton.bind("<Button-1>",stopSong)

#Packing label to display what song is currently playing in Tkinter window. 
songLabel.pack()

songs = []                  #initializing list of song objects
artistes = []               #initializing list of artiste objects
albums = []                 #initializing list of album objects
songMap = HashTable()       #creating hashtable of song objects
albumMap = HashTable()      #creating hashtable of album objects
artisteMap = HashTable()    #creating hashtable of artiste objects

'''
Loops through list of song names and creates instances of an artiste, 
an album and a song for each song. Appends each object to its respective
list of objects. Adds songs for a particular artiste to that artiste's
list of songs. Adds songs that belong to a particular album to that album's
list of songs.
'''
            
def sortSongs():
    for i in range (len(songNames)):
        artiste = Artiste(songArtistes[i])
        artistes.append(artiste)
        album = Album(songAlbum[i])
        albums.append(album)
        song = Song(songNames[i])
        song.setArtiste(artistes[i])
        song.setAlbum(albums[i])
        song.setLength(songLength[i])
        songs.append(song)
        songMap.put(songNames[i],songs[i])
        if songs[i].getArtiste().getName() == artistes[i].getName():
            artistes[i].addSong(songs[i].getTitle())
            artistes[i].addAlbum(songs[i].getAlbum())
        artisteMap.put(songArtistes[i],artistes[i])
        if songs[i].getAlbum().getTitle() == albums[i].getTitle():
            albums[i].addSong(songs[i].getTitle())
            albums[i].addArtiste(songs[i].getArtiste())
        albumMap.put(songAlbum[i],albums[i])
                     
sortSongs()

#Creating entry box to allow searching.
searchBox = Entry(root, width = 50)
searchBox.pack()
searchBox.focus_force()

#Creating search button.
searchButton = Button(root,text='Search')
searchButton.pack()

#Creating labels to display details of particular song, album or artiste in Tkinter window.
label2 = StringVar()
label3 = StringVar()
label4 = StringVar()
songLabel2 = Label(root,textvariable=label2, width = 70)
songLabel2.pack()
songLabel3 = Label(root,textvariable=label3, width = 70)
songLabel3.pack()
songLabel4 = Label(root,textvariable=label4, width = 70)
songLabel4.pack()

#A function to search in hashtable using the search term as a key.
#It displays information on a given song, artiste or album typed in.


def search(event):
    #Getting information entered into searchbox.
    searchTerm = searchBox.get()
    #Checking to see if it exists in either the song, artiste or album
    #hashmap and displaying the appropriate information. If not, returns a prompt.
    if songMap.get(searchTerm)!= None and songMap.get(searchTerm) in songMap.data:
       label2.set("Artiste: " + str(songMap.get(searchTerm).getArtiste()))
       label3.set("Length: " + str(songMap.get(searchTerm).getLength()))
       label4.set("Album: " + str(songMap.get(searchTerm).getAlbum()))      

    elif albumMap.get(searchTerm) != None and albumMap.get(searchTerm) in albumMap.data:
        label2.set("Title: " + str(albumMap.get(searchTerm).getTitle()))
        label3.set("Artiste: " + str(albumMap.get(searchTerm).getArtiste()))
        label4.set("Songs: " + str(albumMap.get(searchTerm).getSongs()))

    elif artisteMap.get(searchTerm) != None and artisteMap.get(searchTerm) in artisteMap.data:
        label2.set("Name: " + str(artisteMap.get(searchTerm).getName()))
        label3.set("Songs: " + str(artisteMap.get(searchTerm).getSongs()))
        label4.set("Albums: " + str(artisteMap.get(searchTerm).getAlbums()))
        
    else:
        label2.set(searchTerm + " does not exist in directory")
        label3.set("")
        label4.set("")
           
#Binding search button with search function.
searchButton.bind("<Button-1>",search)      

root.mainloop()
