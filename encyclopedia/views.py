from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import randint

import markdown2

from . import util



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entrypage(request , entrypage):
   page = util.get_entry(entrypage)
   if page != None:
       html = markdown2.markdown(page)
       return render(request,"encyclopedia/entry.html", {
         "html" : html , "entrypage" : entrypage
           })
   else :
        return render(request,"encyclopedia/404.html",{
            "entrypage" : entrypage
        })
        

def pos(ch1,ch2):
    i=0
    possibility = True
    while possibility:
        while (i < len(ch2)) and (ch1[0] != ch2[i] ):
            i += 1
        if i < len(ch2):
            if (len(ch2) - i - 1) >= (len(ch1) - 1 ):
                j=1
                while (j < len(ch1)) and (ch1[j] == ch2[i+j] ):
                    j += 1
                if (j >= len(ch1)):
                    return True
                else:
                    i += 1
                    possibility = ( len(ch2) - i - 1) >= len(ch1)
            else:
                return False
        
        else : 
            possibility = False
    return(False)        
            
    

def longuest(ch1,ch2):
    if len(ch1) >= len(ch2):
        return ch1
    else : 
        return ch2
def Shortest(ch1,ch2):
    if len(ch1) < len(ch2):
        return ch1
    else : 
        return ch2


def search(request):
    if request.method == "POST":
        query = request.POST
        page = util.get_entry(query["q"])
        if page:
            return entrypage(request , query["q"])
        else:
            results = []
            for entry in util.list_entries():
                ch1 = query["q"].upper()
                ch2 = entry.upper()
                if pos(Shortest(ch1,ch2) , longuest(ch1,ch2) ):
                    results.append(entry)
            return render(request,"encyclopedia/search.html", {
                "results" : results , "q":query["q"]
            })

    else:
        return render(request,"encyclopedia/search.html")


def NewPage(request):

    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        if util.get_entry(title):
            return render(request,"encyclopedia/newpage.html", {
                "error" : "Error : Unfortunately, there is an entry with same title, try another one!"
            } )
        else:
            util.save_entry(title,content)
            return entrypage(request,title)
    else:
        return render(request,"encyclopedia/newpage.html")    

def edit(request):
    if request.method == "GET":
        entry = request.GET["entry"]
        page = util.get_entry(entry)
    
        return render(request,"encyclopedia/edit.html", {
        "content" : page , "entry" : entry
        })
    if request.method == "POST":
        content = request.POST["editedcontent"] 
        entry = request.POST["entry"]
        util.save_entry(entry,content)
        return entrypage(request,entry)   

def randompage(request):
    number_of_entries=0
    for entry in util.list_entries():
        number_of_entries += 1
    r = randint(0,number_of_entries - 1 )

    i=0
    for entry in util.list_entries():
        if i == r:
            return entrypage(request,entry)
        i += 1
