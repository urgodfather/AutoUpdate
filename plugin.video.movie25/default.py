#-*- coding: utf-8 -*-
import xbmc,xbmcgui, xbmcaddon, xbmcplugin
import urllib,re,string,os,time,threading

#################### Set Environment ######################
ENV = "Prod"  # "Prod" or "Dev"
###########################################################

addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
from resources.libs import main
################################################################################ Directories ##########################################################################################################
UpdatePath=os.path.join(main.datapath,'Update')
try: os.makedirs(UpdatePath)
except: pass
CachePath=os.path.join(main.datapath,'Cache')
try: os.makedirs(CachePath)
except: pass
CookiesPath=os.path.join(main.datapath,'Cookies')
try: os.makedirs(CookiesPath)
except: pass
TempPath=os.path.join(main.datapath,'Temp')
try: os.makedirs(TempPath)
except: pass



def MAIN():
    import os 
    folder = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            pass
    folder2 = main.datapath
    for the_file in os.listdir(folder2):
        import shutil
        file_path = os.path.join(folder2, the_file)
        try:os.unlink(file_path)
        except:pass
        try:shutil.rmtree(file_path)
        except:pass
        try:os.removedirs(file_path)
        except:pass
        
    addDir('Goodbye','',420,'')
              
def Announcements():
    #Announcement Notifier from xml file
    try:
        import time
        link=main.OPENURL('https://raw.github.com/mash2k3/MashUpNotifications/master/Notifier.xml?'+ str(time.time()),verbose=False)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    except: link='nill'
    text = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.movie25', 'goodbye.txt'))
    TextBoxes('Announcement',text)
    match=re.compile('<AutoSource>([^<]+)</AutoSource><UpdateOption>([^<]+)</UpdateOption>').findall(link)
    if match:
        for AutoSource,UpdateOption in match:
            print AutoSource,UpdateOption
            if AutoSource == 'github':
                selfAddon.setSetting('autosource', 'false')
                if UpdateOption == 'original':
                    selfAddon.setSetting('updateoption', 'original')
                if UpdateOption == 'gitupdate1':
                    selfAddon.setSetting('updateoption', 'gitupdate1')
                if UpdateOption == 'gitupdate2':
                    selfAddon.setSetting('updateoption', 'gitupdate2')
            else:
                selfAddon.setSetting('autosource', 'true')
        else: print 'No Messages'
    else: print 'Github Link Down'

def TextBoxes(heading,anounce):
        class TextBox():
            """Thanks to BSTRDMKR for this code:)"""
                # constants
            WINDOW = 10147
            CONTROL_LABEL = 1
            CONTROL_TEXTBOX = 5

            def __init__( self, *args, **kwargs):
                # activate the text viewer window
                xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
                # get window
                self.win = xbmcgui.Window( self.WINDOW )
                # give window time to initialize
                xbmc.sleep( 500 )
                self.setControls()


            def setControls( self ):
                # set heading
                self.win.getControl( self.CONTROL_LABEL ).setLabel(heading)
                try:
                        f = open(anounce)
                        text = f.read()
                except:
                        text=anounce
                self.win.getControl( self.CONTROL_TEXTBOX ).setText(text)
                return
        TextBox()
def CheckForAutoUpdate(force = False):
	if selfAddon.getSetting("autosource") == "false":
                if selfAddon.getSetting("updateoption") == "gitupdate1":
                    GitHubRepo    = 'gitupdate1'
                    UpdateVerFile = 'gitupdate1'
                    GitHubUser    = 'mashupdater'
                elif selfAddon.getSetting("updateoption") == "gitupdate2":
                    GitHubRepo    = 'gitupdate2'
                    UpdateVerFile = 'gitupdate2'
                    GitHubUser    = 'mashupdater'
                else:
                    GitHubRepo    = 'AutoUpdate'
                    UpdateVerFile = 'update'
                    GitHubUser    = 'mash2k3'
		GitHubBranch  = 'master'
		RunningFile   = 'running'
		verCheck=True #main.CheckVersion()#Checks If Plugin Version is up to date
		if verCheck == True:
			from resources.libs import autoupdate
			try:
				print "Mashup auto update - started"
				html=main.OPENURL('https://github.com/'+GitHubUser+'/'+GitHubRepo+'?files=1', mobile=True, verbose=False)
			except: html=''
			m = re.search("View (\d+) commit",html,re.I)
			if m: gitver = int(m.group(1))
			else: gitver = 0
			UpdateVerPath = os.path.join(UpdatePath,UpdateVerFile)
			try: locver = int(autoupdate.getUpdateFile(UpdateVerPath))
			except: locver = 0
			RunningFilePath = os.path.join(UpdatePath, RunningFile)
			if locver < gitver and (not os.path.exists(RunningFilePath) or os.stat(RunningFilePath).st_mtime + 120 < time.time()) or force:
				UpdateUrl = 'https://github.com/'+GitHubUser+'/'+GitHubRepo+'/archive/'+GitHubBranch+'.zip'
				UpdateLocalName = GitHubRepo+'.zip'
				UpdateDirName   = GitHubRepo+'-'+GitHubBranch
				UpdateLocalFile = xbmc.translatePath(os.path.join(UpdatePath, UpdateLocalName))
				main.setFile(RunningFilePath,'')
				print "auto update - new update available ("+str(gitver)+")"
				xbmc.executebuiltin("XBMC.Notification(MashUp Update,New Update detected,3000,"+main.slogo+")")
				xbmc.executebuiltin("XBMC.Notification(MashUp Update,Updating...,3000,"+main.slogo+")")
				try:os.remove(UpdateLocalFile)
				except:pass
				try: urllib.urlretrieve(UpdateUrl,UpdateLocalFile)
				except:pass
				if os.path.isfile(UpdateLocalFile):
					extractFolder = xbmc.translatePath('special://home/addons')
					pluginsrc =  xbmc.translatePath(os.path.join(extractFolder,UpdateDirName))
					if autoupdate.unzipAndMove(UpdateLocalFile,extractFolder,pluginsrc):
						autoupdate.saveUpdateFile(UpdateVerPath,str(gitver))
						main.GA("Autoupdate",str(gitver)+" Successful")
						print "Mashup auto update - update install successful ("+str(gitver)+")"
						xbmc.executebuiltin("XBMC.Notification(MashUp Update,Successful,5000,"+main.slogo+")")
						xbmc.executebuiltin("XBMC.Container.Refresh")
						if selfAddon.getSetting('autochan')=='true':
							xbmc.executebuiltin('XBMC.RunScript('+xbmc.translatePath(main.mashpath + '/resources/libs/changelog.py')+',Env)')
					else:
						print "Mashup auto update - update install failed ("+str(gitver)+")"
						xbmc.executebuiltin("XBMC.Notification(MashUp Update,Failed,3000,"+main.elogo+")")
						main.GA("Autoupdate",str(gitver)+" Failed")
				else:
					print "Mashup auto update - cannot find downloaded update ("+str(gitver)+")"
					xbmc.executebuiltin("XBMC.Notification(MashUp Update,Failed,3000,"+main.elogo+")")
					main.GA("Autoupdate",str(gitver)+" Repo problem")
				try:os.remove(RunningFilePath)
				except:pass
			else:
				if force: xbmc.executebuiltin("XBMC.Notification(MashUp Update,MashUp is up-to-date,3000,"+main.slogo+")")
				print "Mashup auto update - Mashup is up-to-date ("+str(locver)+")"
			return
	else:
		GitHubRepo    = 'bitautoupdate1'
		GitHubUser    = 'mash2k3'
		GitHubBranch  = 'master'
		UpdateVerFile = 'bitupdate1'
		RunningFile   = 'running'
		verCheck=True #main.CheckVersion()#Checks If Plugin Version is up to date
		if verCheck == True:
			from resources.libs import autoupdate
			try:
                                import time
				print "Mashup auto update - started"
				html=main.OPENURL('https://bitbucket.org/api/1.0/repositories/'+GitHubUser+'/'+GitHubRepo+'/branches-tags?'+ str(time.time()), mobile=True, verbose=False)
			except: html=''
			m = re.search('"changeset": "([^"]+?)"',html,re.I)
			if m: 
				gitver = m.group(1)[0:7]
				CommitNumber=m.group(1)[0:12]
			else: gitver = 0
			UpdateVerPath = os.path.join(UpdatePath,UpdateVerFile)
			try: locver = autoupdate.getUpdateFile(UpdateVerPath)
			except: locver = 0
			RunningFilePath = os.path.join(UpdatePath, RunningFile)
			if locver != gitver and (not os.path.exists(RunningFilePath) or os.stat(RunningFilePath).st_mtime + 120 < time.time()) or force:
				UpdateUrl = 'https://bitbucket.org/'+GitHubUser+'/'+GitHubRepo+'/get/'+GitHubBranch+'.zip'
				UpdateLocalName = GitHubRepo+'.zip'
				UpdateDirName   = GitHubUser+'-'+GitHubRepo+'-'+CommitNumber
				print UpdateDirName
				UpdateLocalFile = xbmc.translatePath(os.path.join(UpdatePath, UpdateLocalName))
				main.setFile(RunningFilePath,'')
				print "auto update - new update available ("+str(gitver)+")"
				xbmc.executebuiltin("XBMC.Notification(MashUp Update,New Update detected,3000,"+main.slogo+")")
				xbmc.executebuiltin("XBMC.Notification(MashUp Update,Updating...,3000,"+main.slogo+")")
				try:os.remove(UpdateLocalFile)
				except:pass
				try: urllib.urlretrieve(UpdateUrl,UpdateLocalFile)
				except:pass
				if os.path.isfile(UpdateLocalFile):
                                        extractFolder = xbmc.translatePath('special://home/addons')
                                        pluginsrc =  xbmc.translatePath(os.path.join(extractFolder,UpdateDirName))
                                        if autoupdate.unzipAndMove(UpdateLocalFile,extractFolder,pluginsrc):
						autoupdate.saveUpdateFile(UpdateVerPath,str(gitver))
						main.GA("Autoupdate",str(gitver)+" Successful")
						print "Mashup auto update - update install successful ("+str(gitver)+")"
						xbmc.executebuiltin("XBMC.Notification(MashUp Update,Successful,5000,"+main.slogo+")")
						xbmc.executebuiltin("XBMC.Container.Refresh")
						if selfAddon.getSetting('autochan')=='true':
							xbmc.executebuiltin('XBMC.RunScript('+xbmc.translatePath(main.mashpath + '/resources/libs/changelog.py')+',Env)')
					else:
						print "Mashup auto update - update install failed ("+str(gitver)+")"
						xbmc.executebuiltin("XBMC.Notification(MashUp Update,Failed,3000,"+main.elogo+")")
						main.GA("Autoupdate",str(gitver)+" Failed")
				else:
					print "Mashup auto update - cannot find downloaded update ("+str(gitver)+")"
					xbmc.executebuiltin("XBMC.Notification(MashUp Update,Failed,3000,"+main.elogo+")")
					main.GA("Autoupdate",str(gitver)+" Repo problem")
				try:os.remove(RunningFilePath)
				except:pass
			else:
				if force: xbmc.executebuiltin("XBMC.Notification(MashUp Update,MashUp is up-to-date,3000,"+main.slogo+")")
				print "Mashup auto update - Mashup is up-to-date ("+str(locver)+")"
			return




def addDir(name, url, mode, thumbImage):

        u  = sys.argv[0]

        u += "?url="  + urllib.quote_plus(url)
        u += "&mode=" + str(mode)
        u += "&name=" + urllib.quote_plus(name)

        liz = xbmcgui.ListItem(name, iconImage='', thumbnailImage=thumbImage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image','')

        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=True)




def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param
              
params=get_params()

url=None
name=None
mode=None
iconimage=None
fanart=None
plot=None
genre=None
title=None
season=None
episode=None
location=None
path=None
index=None

try: name=urllib.unquote_plus(params["name"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: mode=int(params["mode"])
except: pass
try:
    iconimage=urllib.unquote_plus(params["iconimage"])
    iconimage = iconimage.replace(' ','%20')
except: pass
try: plot=urllib.unquote_plus(params["plot"])
except: pass
try:
    fanart=urllib.unquote_plus(params["fanart"])
    fanart = fanart.replace(' ','%20')
except: pass
try: genre=urllib.unquote_plus(params["genre"])
except: pass
try: title=urllib.unquote_plus(params["title"])
except: pass
try: episode=int(params["episode"])
except: pass
try: season=int(params["season"])
except: pass
try: location=urllib.unquote_plus(params["location"])
except: pass
try: path=urllib.unquote_plus(params["path"])
except: pass
try: index=urllib.unquote_plus(params["index"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Thumb: "+str(iconimage)



if mode==None or url==None or len(url)<1:
    threading.Thread(target=Announcements).start()
    threading.Thread(target=CheckForAutoUpdate).start()
    MAIN()
        
   
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
