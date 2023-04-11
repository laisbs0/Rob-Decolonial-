#importing libraries
import gspread
import google.auth
import tkinter as tk
from tkinter import *

#creating window
root = Tk()
root.geometry('600x650')#geometry of window
root.title('DataFlair')#title for window
Label(root,text='Lets Display the Content of This File',font='arial 10').pack()

s=tk.StringVar()#s is string type
def read_the_sheet():
    sheet_to_display=s.get()#get the value of s
# use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('json file.json', scope)
    client = gspread.authorize(creds)
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
    sheet = client.open(sheet_to_display).sheet1
# Extract and print all of the values
    display_record = sheet.get_all_records()
    for i in display_record:
        Message(root,text=i).pack()#display the details in sheet

Entry(root,textvariable=s).pack()#entry field
Button(root,text='Display',bg='red',command=read_the_sheet).pack()#button widget on the window
root.mainloop()