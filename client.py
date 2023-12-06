#
# Bluesky Notifier
#

# Import Python Modules
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import *
import datetime
from atproto import Client, models
from dotenv import load_dotenv
import os

from PIL import Image
import urllib.request

# Import Own Modules
import globals
import writeLogfile

#
# Function: About Message Box
#
def about():
    writeLogfile.log("In about Fuction", "I")

    aboutMessage = "Bluesky App \n" + "Version " + globals.versionNumber + "\nCopyright 2023"
    messagebox.showinfo("About", aboutMessage)

#
# Function: Display Log File
#
def showLog():
    writeLogfile.log("In showLog Fuction", "I")

    # Create new window
    window = Tk()
    window.title('Bluesky App')
    window.geometry('1024x768')
    window.resizable(False, False)

    # Setup Menus
    menubar = Menu(window)

    # create File menu, and add it to the menu bar
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Exit", command=window.destroy)
    menubar.add_cascade(label="File", menu=filemenu)

    # Vertical (y) Scroll Bar
    scroll = Scrollbar(window)
    scroll.pack(side=RIGHT, fill=Y)

    # Text field to display log
    logfileText = Text(window,
                       state="normal",
                       height=48,
                       width=160,
                       wrap=WORD,
                       yscrollcommand=scroll.set)
    logfileText.pack()

    # Read logfile and populate text field
    with open(globals.logfileName, 'r') as f:
        logMessage = f.read()
        logfileText.insert(INSERT, logMessage)

    scroll.config(command=logfileText.yview)

#
# Function: notifications
#
def notifications():
    writeLogfile.log("In Notifications Fuction", "I")

    # Remove all existing widgets
    for widget in notificationsFrame.winfo_children():
        widget.destroy()

    client = Client()
    profile = client.login(globals.logonID, globals.password)

    profileText = "Bluesky Profile: " + profile.display_name + " (" + profile.handle + ")"
    Label(notificationsFrame, text=profileText, style='H.TLabel').grid(row=0,column=0,columnspan=12)

    likeIMG = PhotoImage(file="images/like.png")
    repostIMG = PhotoImage(file="images/repost.png")
    mentionIMG = PhotoImage(file="images/mention.png")
    quoteIMG = PhotoImage(file="images/quote.png")
    followIMG = PhotoImage(file="images/follow.png")
    replyIMG = PhotoImage(file="images/reply.png")

    # Intialise Notification type counts
    likeCount = 0
    repostCount = 0
    mentionCount = 0
    quoteCount = 0
    followCount = 0
    replyCount = 0

    # Create Notifcations Canvas
    c = Canvas(notificationsFrame, background="white", borderwidth=1, relief="solid", highlightthickness=0)
    c.grid(row=2,column=0,columnspan=12)

    # save the time when we fetch notifications
    now = datetime.datetime.now()
    lastUpdatedText = "Last Updated: " + now.strftime("%Y-%m-%d %H:%M:%S")
    Label(notificationsFrame, text=lastUpdatedText, style='H.TLabel').grid(row=3,column=0,columnspan=12)

    # Create Text widget
    notificationsText = Text(c, height=45, width=93, state="normal", wrap=NONE, highlightthickness = 0, borderwidth=0)
    notificationsText.tag_configure('new', background='white', foreground='red', font=("Courier", 10))
    notificationsText.tag_configure('old', background='white', foreground='black', font=("Courier", 10))
    notificationsText.pack(padx=6, pady=6)

    # fetch new notifications
    response = client.app.bsky.notification.list_notifications({'limit':100})

    newNotificationsCount = 0
    
    # For each notification get details
    for notification in response.notifications:

        notificationType = notification.reason
        name = notification.author.handle
        nameStop = name.find(".")
        nameLength = len(notification.author.handle)
        notificationFrom = name[:-(nameLength-nameStop)]

        notificationIndexedAt = notification.indexed_at.replace("T"," ")
        notificationIndexedAt = notificationIndexedAt[0:19]
        notificationIndexedAt = notificationIndexedAt + " "

        if notification.is_read:
            notificationsText.insert(END, notificationIndexedAt, 'old')
        else:
            notificationsText.insert(END, notificationIndexedAt, 'new')
        
        if notificationType == "like":
            notificationsText.image_create(END, image=likeIMG)
            notificationsText.imageL = likeIMG
            likeCount = likeCount + 1
        elif notificationType == "mention":
            notificationsText.image_create(END, image=mentionIMG)
            notificationsText.imageM = mentionIMG
            mentionCount = mentionCount + 1
        elif notificationType == "repost":
            notificationsText.image_create(END, image=repostIMG)
            notificationsText.imageRp = repostIMG
            repostCount = repostCount + 1
        elif notificationType == "quote":
            notificationsText.image_create(END, image=quoteIMG)
            notificationsText.imageQ = quoteIMG
            quoteCount = quoteCount + 1
        elif notificationType == "follow":
            notificationsText.image_create(END, image=followIMG)
            notificationsText.imageF = followIMG
            followCount = followCount + 1
        elif notificationType == "reply":
            notificationsText.image_create(END, image=replyIMG)
            notificationsText.imageRe = replyIMG
            replyCount = replyCount + 1

        notificationDetails = " From: " + notificationFrom + "\n"

        if notification.is_read:
            notificationsText.insert(END, notificationDetails, 'old')
        else:
            notificationsText.insert(END, notificationDetails, 'new')
            newNotificationsCount = newNotificationsCount + 1

    notificationsText.configure(state='disabled')
    
    if newNotificationsCount >0:
        tabControl.tab(notificationsFrame, text = 'Notifications('+str(newNotificationsCount)+')')
    else:
        tabControl.tab(notificationsFrame, text = 'Notifications')

    # Create Notification Counts Labels
    Label(notificationsFrame, image=likeIMG).grid(row=1,column=0,sticky="E")
    Label(notificationsFrame, text=likeCount, style='S.TLabel').grid(row=1,column=1,sticky="W")
    Label(notificationsFrame, image=repostIMG).grid(row=1,column=2,sticky="E")
    Label(notificationsFrame, text=repostCount, style='S.TLabel').grid(row=1,column=3,sticky="W")
    Label(notificationsFrame, image=mentionIMG).grid(row=1,column=4,sticky="E")
    Label(notificationsFrame, text=mentionCount, style='S.TLabel').grid(row=1,column=5,sticky="W")
    Label(notificationsFrame, image=quoteIMG).grid(row=1,column=6,sticky="E")
    Label(notificationsFrame, text=quoteCount, style='S.TLabel').grid(row=1,column=7,sticky="W")
    Label(notificationsFrame, image=followIMG).grid(row=1,column=8,sticky="E")
    Label(notificationsFrame, text=followCount, style='S.TLabel').grid(row=1,column=9,sticky="W")
    Label(notificationsFrame, image=replyIMG).grid(row=1,column=10,sticky="E")
    Label(notificationsFrame, text=replyCount, style='S.TLabel').grid(row=1,column=11,sticky="W")

    # Refresh frame
    root.after(globals.notificationsRefreshInterval,notifications)

#
# Function: feed
#
def feed():
    writeLogfile.log("In Feed Fuction", "I")

    # Remove all existing widgets
    for widget in feedFrame.winfo_children():
        widget.destroy()

    newpostIMG = PhotoImage(file="images/newpost.png")
    repostIMG = PhotoImage(file="images/repost.png")

    client = Client()
    profile = client.login(globals.logonID, globals.password)

    profileText = "Bluesky Profile: " + profile.display_name + " (" + profile.handle + ")"
    Label(feedFrame, text=profileText, style='H.TLabel').pack(pady=6)

    # Create Notifcations Canvas
    c = Canvas(feedFrame, background="white", borderwidth=1, relief="solid", highlightthickness=0)
    c.pack()

    # Create Text widget
    feedText = Text(c, height=45, width=93, state="normal", wrap=NONE, highlightthickness = 0, borderwidth=0)
    feedText.tag_configure('new', background='white', foreground='red', font=("Courier", 10))
    feedText.tag_configure('old', background='white', foreground='black', font=("Courier", 10))
    feedText.pack(padx=6, pady=6)

    # save the time when we fetch timeline
    now = datetime.datetime.now()
    lastUpdatedTime = now.strftime("%Y-%m-%d %H:%M:%S")
    lastUpdatedLabel = Label(feedFrame, text="Last Updated:" + lastUpdatedTime, style='H.TLabel').pack(pady=6)

    if globals.firstTimeFeed == False:
        globals.lastUpdated = lastUpdatedTime
    else:
        globals.lastUpdated = "1970-02-01 00:00:00"
        globals.firstTimeFeed = False

    # Get 'Home' Page
    timeline = client.app.bsky.feed.get_timeline()

    newPostCount = 0
    
    for feed_view in timeline.feed:
        author = feed_view.post.author

        action = 'New Post' # default
        action_by = author.handle[:-12]

        # Check for non-new post action
        if feed_view.reason:
            action = type(feed_view.reason).__name__.replace('Reason', '')
            writeLogfile.log("Reason Code: "+action, "I")

        post = feed_view.post.record

        postCreatedAt = post.created_at.replace("T"," ")
        postCreatedAt = postCreatedAt[0:19]
        feedText.insert(END, postCreatedAt, 'old')

        if action == "New Post":
            feedText.image_create(END, image=newpostIMG)
            feedText.imageL = newpostIMG
        elif action == "Repost":
            feedText.image_create(END, image=repostIMG)
            feedText.imageM = repostIMG

        postText = post.text.replace("\n", " ")
        displayText = " " + action_by + " >> " + postText + "\n"

        if postCreatedAt >= globals.lastUpdated:
            feedText.insert(END, displayText, 'new')
            newPostCount = newPostCount + 1
        else:
            feedText.insert(END, displayText, 'old')

    feedText.configure(state='disabled')

    # Refresh frame
    root.after(globals.feedRefreshInterval,feed)

#
# Function: postComment
#
def postComment(commentText):
    writeLogfile.log("In Post Comment Fuction", "I")

    client = Client()
    profile = client.login(globals.logonID, globals.password)

    client.send_post(text=commentText)
    messagebox.showinfo("OK", "Message Posted to Bluesky")

#
# Function: createPost
#
def createPost():

    writeLogfile.log("In Post Fuction", "I")

    # Remove all existing widgets
    for widget in postFrame.winfo_children():
        widget.destroy()

    client = Client()
    profile = client.login(globals.logonID, globals.password)

    profileText = profile.display_name + " (" + profile.handle + ")"
    Label(postFrame, text="Posting as: " + profileText, style='H.TLabel').grid(row=0,column=0,columnspan=2)
    Label(postFrame, text="Enter Text to Post", style='S.TLabel').grid(row=1,column=0)
    postText = Text(postFrame,width=75,height=4)
    postText.grid(row=1,column=1)    
    postButton = Button(postFrame,text="Post",command=lambda: postComment(postText.get("1.0","end-1c")))
    postButton.grid(row=2,column=0,sticky="E")
    clearButton = Button(postFrame,text="Cancel",command=lambda: createPost())
    clearButton.grid(row=2,column=1,sticky="W")

#
# Function: profile
#
def showProfile():

    writeLogfile.log("In showProfile Fuction", "I")

    # Remove all existing widgets
    for widget in showProfileFrame.winfo_children():
        widget.destroy()

    client = Client()
    profile = client.login(globals.logonID, globals.password)

    # Get & Display Avatar
    avatarURL = profile.avatar
    urllib.request.urlretrieve(avatarURL,"images/avatar.jpg")
    avatarImageJPG = Image.open(r"images/avatar.jpg")
    scale = 0.3
    avatarImageJPGsmall = avatarImageJPG.resize((int(avatarImageJPG.width*scale),int(avatarImageJPG.height*scale)))
    avatarImageJPGsmall.save(r"images/avatar.png")
    avatarPhoto = PhotoImage(file="images/avatar.png")
    avatarImage = Label(showProfileFrame, image=avatarPhoto)
    avatarImage.image = avatarPhoto
    avatarImage.grid(row=0,column=0,columnspan=2)    

    Label(showProfileFrame, text="Display Name:",style='H.TLabel').grid(row=1,column=0,sticky="E")
    Label(showProfileFrame, text=profile.display_name,style='D.TLabel').grid(row=1,column=1,sticky="W")
    Label(showProfileFrame, text="Handle:",style='H.TLabel').grid(row=2,column=0,sticky="E")
    Label(showProfileFrame, text=profile.handle,style='D.TLabel').grid(row=2,column=1,sticky="W")
    Label(showProfileFrame, text="Description:",style='H.TLabel').grid(row=3,column=0,sticky="E")
    descriptionText = Text(showProfileFrame,width=50,height=10)
    descriptionText.grid(row=3,column=1)
    descriptionText.insert(END, profile.description)
    descriptionText.configure(state='disabled')

##################### 
# Main Process Loop #
#####################
writeLogfile.log("In Main Fuction", "I")

# Load environment variables
load_dotenv()
globals.logonID = os.getenv("BLUESKYUSERNAME")
globals.password = os.getenv("BLUESKYPASSWORD")

print("Starting Bluesky App .....")

# Create a TK application
root = Tk()
root.configure(background="white")
root.title('Bluesky')
root.resizable(False, False)
root.geometry('780x1000')

# Gobal Styles
headerStyle = Style()
headerStyle.configure("H.TLabel",
                      background='white',
                      foreground='blue',
                      font=("Cordia, Bold", 12),
                      anchor="center") # Title text
dataStyle = Style()
dataStyle.configure("D.TLabel",
                    background='white',
                    foreground='black',
                    font=("Cordia", 12)) # Data text
statusMessageStyle = Style()
statusMessageStyle.configure("S.TLabel",
                    background='white',
                    foreground='red',
                    font=("Cordia, Bold", 12)) # Status Message text
    
# Setup Menus
menubar = Menu(root)

# create File menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="File", menu=filemenu)

# create Help menu, and add it to the menu bar
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Show Log", command=showLog)
helpmenu.add_separator()
helpmenu.add_command(label="About", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)

# Display the menu
root.config(menu=menubar)

blueskyPhoto = PhotoImage(file="images/bluesky.png")
blueskyImage = Label(image=blueskyPhoto, borderwidth=0, background="white")
blueskyImage.image = blueskyPhoto
blueskyImage.pack()

# Add Tabbed Frame
tabControl = Notebook(root)
noteStyler = Style()
noteStyler.configure("TNotebook", background='white')

#Add Profile Tab
showProfileFrame = Frame(tabControl, style='TNotebook')
tabControl.add(showProfileFrame, text='Profile')

# Add Feed Tab
feedFrame = Frame(tabControl, style='TNotebook')
tabControl.add(feedFrame, text='Feed')

# Add Notifications Tab
notificationsFrame = Frame(tabControl, style='TNotebook')
tabControl.add(notificationsFrame, text='Notifications')

# Add Post Tab
postFrame = Frame(tabControl, style='TNotebook')
tabControl.add(postFrame, text='Post')

# Display Tabs
tabControl.pack()

# Populate Tabs
showProfile()
feed()
notifications()
createPost()

# Main Window Loop
root.mainloop()
