#import libraries
import requests
import urllib.request
import time
import datetime
from bs4 import BeautifulSoup
import tkinter as tk


class App():  # Class for an instance of the application

    def __init__(self, master):  # main method

        master.title('MetaGrabber')  # sets title of the application
        # sets the default canvas size
        canvas = tk.Canvas(master, height=700, width=1000)
        canvas.pack()

        # creates frame for the entry box and run button
        frame = tk.Frame(master, bg='#80c1ff', bd=4)
        frame.place(relx=0.5, rely=0, relwidth=1, relheight=0.1, anchor='n')

        self.button = tk.Button(frame, text="Meta Tags", font='helvetica', bg='gray', command=lambda: self.websiteCall(
            entry.get()))  # calls the websiteCall method that grabs the meta tags
        self.button.place(relx=0.654, rely=.5, relheight=.4, relwidth=0.1)

        self.urlLabel = tk.Label(frame, text="Enter URL here:", font='helvetica',
                                 bg="white", justify='left')  # description box
        self.urlLabel.place(rely=0, relwidth=0.2, relheight=.5)

        # creates entry field for website to be inputed
        entry = tk.Entry(frame, font=40)
        entry.place(rely=.5, relwidth=0.65, relheight=.5)

        # frame hold the output field
        lowerFrame = tk.Frame(master, bg='#80c1ff', bd=5)
        lowerFrame.place(relx=0.5, rely=0.1, relwidth=1,
                         relheight=0.82, anchor='n')

        # allows for scrolling if list is too long to be viewed in window
        scrollbar = tk.Scrollbar(lowerFrame)
        scrollbar.pack(side='right', fill='y')

        # allows for scrolling if list is too long to be viewed in window
        scrollbar2 = tk.Scrollbar(lowerFrame, orient="horizontal")
        scrollbar2.pack(side='bottom', fill='x')

        self.txtBox = tk.Text(lowerFrame, width=500, font='helvetica', height=400, yscrollcommand=scrollbar.set,
                              xscrollcommand=scrollbar2.set, wrap="none")  # text box to hold outputed meta tags
        self.txtBox.pack(expand=0, fill='both')

        scrollbar.config(command=self.txtBox.yview)
        scrollbar2.config(command=self.txtBox.xview)

        # frame to hold web code and quit button
        bottomFrame = tk.Frame(master, bg='#80c1ff', bd=5)
        bottomFrame.place(relx=0.5, rely=0.92, relwidth=1,
                          relheight=0.08, anchor='n')

        self.quitButton = tk.Button(bottomFrame, text="Quit", font='helvetica',
                                    bg='gray', command=frame.quit)  # button to quit application
        self.quitButton.place(relx=0.9, rely=0.1, relheight=0.64, relwidth=0.1)

        self.codeLabel = tk.Label(bottomFrame, text="Status Code:", width=10,
                                  height=1, font='helvetica', bg="#80c1ff")  # description box
        self.codeLabel.place(relx=.65)

        # displays the site codde status
        self.codeBox = tk.Text(bottomFrame, width=5,
                               height=1, font='helvetica')
        self.codeBox.place(relx=0.7)

        fileEntry = tk.Entry(bottomFrame, font=30)
        fileEntry.place(relx=0.19, relwidth=0.09, relheight=0.5)

        self.docButton = tk.Button(
            bottomFrame, text="Create File", font='hekvetica', bg='gray', command=lambda: self.createFile(entry.get(), fileEntry.get()))
        self.docButton.place(relx=.3)

        self.fileLabel = tk.Label(bottomFrame, text="Enter name of file here: ",
                                  font='helvetica', bg="#80c1ff", justify='left')  # description box
        self.fileLabel.place(rely=0, relwidth=0.18, relheight=.5)

    def websiteCall(self, entry):  # function call the website and scan it for meta tags

        self.txtBox.delete('1.0', 'end')  # clears the text box

        try:
            url = entry  # passes the user inout itnto the url variable
            response = requests.get(url)  # passes the url into a request
            # beautifulsoup sets the url info to text to scan through
            soup = BeautifulSoup(response.text, 'lxml')
            # puts all meta tags to a variable
            metatags = soup.find_all('meta')

            for x in metatags:  # prints the tags to the screen
                self.txtBox.insert('end', str(x) + '\n')

        except:
            # outputs if an improper url or no url is inputed
            self.txtBox.insert(
                'end', "Improper website URL. Please input a correct URL.\nA complete url needs to be inlcuded. \nExample: https://examplesite.com/")

    def codeGrab(self, url, name):  # function to grab the http status code of the website

        self.codeBox.delete('1.0', 'end')  # clears the textbox
        # sets the status code to a variable
        code = urllib.request.urlopen(url).getcode()
        # outputs the status code to the text box
        self.codeBox.insert('end', code)

        currentDT = datetime.datetime.now()

        file = open(name, "a+")
        file.write(
            "\n\nStatus code at time of running: ["+str(code) + "] at " + str(currentDT))
        file.close()

    def createFile(self, entry, name):
        url = entry
        fileName = name
        file = open(fileName, "w")
        file.write("These are the metatags for: " +
                   str(url) + "\n\n" + self.txtBox.get('1.0', 'end') + '\n\n')

        file.close()
        self.codeGrab(url, fileName)


root = tk.Tk()  # initializes tkinter
b = App(root)  # creates an object for the application
top = None
root.mainloop()  # runs the application

#https://www.humblebundle.com/
