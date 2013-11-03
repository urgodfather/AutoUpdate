import urllib,re,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import main

#Mash Up - by Mash2k3 2012.

addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
MainUrl='http://www.movie25.so'

def LISTMOVIES(murl):
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match = re.findall('<div class="movie_pic"><a href="(.+?)"  target=".+?">    <img src="(.+?)".+?target="_self">(.+?)</a>.+?">Genre:  <a href=".+?>(.+?)</a>.+?<br/>Views: <span>(.+?)</span>.+?(.+?)votes.+?score:(.+?)</div>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url,thumb,name,genre,views,votes,rating in match:
                votes=votes.replace('(','')
                name=name.replace('-','').replace('&','').replace('acute;','').strip()
                main.addInfo(name+'[COLOR blue] Views: '+views+'[/COLOR] [COLOR red]Votes: '+votes+'[/COLOR] [COLOR green]Rating: '+rating+'/5.00[/COLOR]',MainUrl+url,3,thumb,genre,'')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        
        main.GA("None","Movie25-list")
        
        
        paginate=re.compile('</a><a href=\'([^<]+)\'>Next</a>').findall(link)
        if paginate:
                main.addDir('[COLOR red]Home[/COLOR]','',2000,art+'/home.png')
                
                main.addDir('[COLOR red]Enter Page #[/COLOR]',murl,207,art+'/gotopage.png')
                xurl=MainUrl+paginate[0]
                r = re.findall('>Next</a><a href=\'/movies/.+?/([^<]+)\'>Last</a>',link)
                pg= re.findall('/movies/.+?/([^<]+)',paginate[0])
                pg=int(pg[0])-1
                if r:
                        main.addDir('[COLOR blue]Page '+ str(pg)+' of '+r[0]+'[/COLOR]',xurl,1,art+'/next2.png')
                else:
                        main.addDir('[COLOR blue]Page '+ str(pg)+'[/COLOR]',xurl,1,art+'/next2.png')
        
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        main.VIEWS()


def UFCMOVIE25():
                surl='http://www.movie25.so/search.php?key=ufc&submit='
                link=main.OPENURL(surl)
                link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
                match=re.compile('<div class="movie_pic"><a href="(.+?)" target=".+?">                            <img src="(.+?)" width=".+?" height=".+?" />                            </a></div>            <div class=".+?">              <div class=".+?">                <h1><a href=".+?" target=".+?">                  (.+?)                  </a></h1>                <div class=".+?">Genre:                  <a href=".+?" target=\'.+?\'>(.+?)</a>.+?Release:.+?Views: <span>                (.+?)                </span>.+?<span id=RateCount.+?>                (.+?)                </span> votes.+?<div id=".+?">score:<span id=Rate_.+?>(.+?)</span>').findall(link)
                dialogWait = xbmcgui.DialogProgress()
                ret = dialogWait.create('Please wait until Movie list is cached.')
                totalLinks = len(match)
                loadedLinks = 0
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
                for url,thumb,name,genre,views,votes,rating in match:
                        name=name.replace('-','').replace('&','').replace('acute;','').strip()
                        furl= 'http://movie25.com/'+url
                        main.addInfo(name+'('+year+')[COLOR blue] Views: '+views+'[/COLOR] [COLOR red]Votes: '+votes+'[/COLOR] [COLOR green]Rating: '+rating+'/5.00[/COLOR]',furl,3,thumb,genre,'')
                        loadedLinks = loadedLinks + 1
                        percent = (loadedLinks * 100)/totalLinks
                        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                        if (dialogWait.iscanceled()):
                                return False 
                dialogWait.close()
                del dialogWait
                main.addDir('[COLOR blue]Page 2[/COLOR]','http://www.movie25.so/search.php?page=2&key=ufc',9,art+'/next2.png')
                main.GA("UFC","UFC_Movie25-List")

def Searchhistory():
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistory25')
        if not os.path.exists(SeaFile):
            url='m25'
            SEARCH(url)
        else:
            main.addDir('Search','m25',4,art+'/search.png')
            main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
            thumb=art+'/link.png'
            searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
            for seahis in reversed(searchis):
                    url=seahis
                    seahis=seahis.replace('%20',' ')
                    main.addDir(seahis,url,4,thumb)

def SEARCH(murl):
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistory25')
        try:
            os.makedirs(seapath)
        except:
            pass
        if murl == 'm25':
                keyb = xbmc.Keyboard('', 'Search Movies')
                keyb.doModal()
                if (keyb.isConfirmed()):
                    search = keyb.getText()
                    encode=urllib.quote(search)
                    surl='http://www.movie25.so/search.php?key='+encode+'&submit='
                    if not os.path.exists(SeaFile) and encode != '':
                        open(SeaFile,'w').write('search="%s",'%encode)
                    else:
                        if encode != '':
                            open(SeaFile,'a').write('search="%s",'%encode)
                    searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
                    for seahis in reversed(searchis):
                        continue
                    if len(searchis)>=10:
                        searchis.remove(searchis[0])
                        os.remove(SeaFile)
                        for seahis in searchis:
                            try:
                                open(SeaFile,'a').write('search="%s",'%seahis)
                            except:
                                pass
                else:
                        return
        else:
                encode = murl
                surl='http://www.movie25.so/search.php?key='+encode+'&submit='
        link=main.OPENURL(surl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class="movie_pic"><a href="(.+?)" target=".+?">    <img src="(.+?)" width=".+?" height=".+?" />.+?<a href=".+?" target=".+?">(.+?)</a></h1><div class=".+?">Genre:  <a href=".+?" target=\'.+?\'>(.+?)</a>.+?Release:.+?<br/>Views: <span>(.+?)</span>.+?id=RateCount_.+?>(.+?)</span> votes.+?>score:(.+?)</div>').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url,thumb,name,genre,views,votes,rating in match:
                name=name.replace('-','').replace('&','').replace('acute;','')
                furl= MainUrl+url
                main.addInfo(name+'[COLOR blue] Views: '+views+'[/COLOR] [COLOR red]Votes: '+votes+'[/COLOR] [COLOR green]Rating: '+rating+'/5.00[/COLOR]',furl,3,thumb,genre,'')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False 
        dialogWait.close()
        del dialogWait
        exist = re.findall("<a href='search.php.?page=.+?'>Next</a>",link)
        if exist:
                r = re.findall(""">Next</a><a href='search.php.?page=([^<]+)&key=.+?'>Last</a>""",link)
                if r:
                        main.addDir('[COLOR blue]Page 1 of '+r[0]+'[/COLOR]','http://www.movie25.so/search.php?page=2&key='+encode,9,art+'/next2.png')
                else:
                        main.addDir('[COLOR blue]Page 1[/COLOR]','http://www.movie25.so/search.php?page=2&key='+encode,9,art+'/next2.png')
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        main.GA("None","Movie25-Search")


def ENTYEAR():
        dialog = xbmcgui.Dialog()
        d = dialog.numeric(0, 'Enter Year')
        if d:
                encode=urllib.quote(d)
                if encode < '2014' and encode > '1900':
                     surl='http://www.movie25.so/search.php?year='+encode+'/'
                     YEARB(surl)
                else:
                    dialog = xbmcgui.Dialog()
                    ret = dialog.ok('Wrong Entry', 'Must enter year in four digit format like 1999','Enrty must be between 1900 and 2014')
        
def GotoPage(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        r = re.findall('>Next</a><a href=\'/movies/.+?/([^<]+)\'>Last</a>',link)
        x = re.findall('>Next</a><a href=\'([^<]+)/.+?\'>Last</a>',link)
        dialog = xbmcgui.Dialog()
        d = dialog.numeric(0, 'Section Last Page = '+r[0])
        if d:
                pagelimit=int(r[0])
                if int(d) <= pagelimit:
                     encode=urllib.quote(d)
                     surl=MainUrl+x[0]+'/'+encode
                     LISTMOVIES(surl)
                else:
                    dialog = xbmcgui.Dialog()
                    ret = dialog.ok('Wrong Entry', 'The page number you entered does not exist.',' This sections page limit is '+str(pagelimit) )

def GotoPageB(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        r = re.findall('>Next</a><a href=\'search.php.?page=(.+?)&year=.+?\'>Last</a>',link)
        dialog = xbmcgui.Dialog()
        d = dialog.numeric(0, 'Section Last Page = '+r[0])
        if d:
                pagelimit=int(r[0])
                if int(d) <= pagelimit:
                     encode=urllib.quote(d)
                     year  = url.split('year=')
                     url  = url.split('year=')
                     url  = url[0].split('page=')
                     
                     
                     surl=url[0]+'page='+encode+'&year='+year[1]
                     NEXTPAGE(surl)
                else:
                    dialog = xbmcgui.Dialog()
                    ret = dialog.ok('Wrong Entry', 'The page number you entered does not exist.',' This sections page limit is '+str(pagelimit) )

def YEARB(murl):
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class="movie_pic"><a href="(.+?)" target=".+?">    <img src="(.+?)" width=".+?" height=".+?" />.+?<a href=".+?" target=".+?">(.+?)</a></h1><div class=".+?">Genre:  <a href=".+?" target=\'.+?\'>(.+?)</a>.+?Release:.+?<br/>Views: <span>(.+?)</span>.+?id=RateCount_.+?>(.+?)</span> votes.+?>score:(.+?)</div>').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url,thumb,name,genre,views,votes,rating in match:
                name=name.replace('-','').replace('&','').replace('acute;','')
                furl= 'http://movie25.com/'+url
                main.addInfo(name+'[COLOR blue] Views: '+views+'[/COLOR] [COLOR red]Votes: '+votes+'[/COLOR] [COLOR green]Rating: '+rating+'/5.00[/COLOR]',furl,3,thumb,genre,'')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False 
        dialogWait.close()
        del dialogWait
        ye = murl[38:45]
        r = re.findall("Next</a><a href='search.php.?page=([^<]+)&year=.+?'>Last</a>",link)
        if r:
                main.addDir('[COLOR red]Enter Page #[/COLOR]',murl,208,art+'/gotopage.png')
                main.addDir('[COLOR blue]Page 1 of '+r[0]+'[/COLOR]','http://www.movie25.so/search.php?page=2&year='+str(ye),9,art+'/next2.png')    
        else:
                main.addDir('[COLOR blue]Page 1[/COLOR]','http://www.movie25.so/search.php?page=2&year='+str(ye),9,art+'/next2.png')
       
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        main.VIEWS()
        
def NEXTPAGE(murl):
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class="movie_pic"><a href="(.+?)" target=".+?">    <img src="(.+?)" width=".+?" height=".+?" />.+?<a href=".+?" target=".+?">(.+?)</a></h1><div class=".+?">Genre:  <a href=".+?" target=\'.+?\'>(.+?)</a>.+?Release:.+?<br/>Views: <span>(.+?)</span>.+?id=RateCount_.+?>(.+?)</span> votes.+?>score:(.+?)</div>').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url,thumb,name,genre,views,votes,rating in match:
                name=name.replace('-','').replace('&','').replace('acute;','')
                furl= MainUrl+url
                main.addInfo(name+'[COLOR blue] Views: '+views+'[/COLOR] [COLOR red]Votes: '+votes+'[/COLOR] [COLOR green]Rating: '+rating+'/5.00[/COLOR]',furl,3,thumb,genre,'')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False
        dialogWait.close()
        del dialogWait
        
        matchx=re.compile('http://www.movie25.so/search.php.+?page=(.+?)&year=(.+?)').findall(murl)
        if len(matchx)>0:
                durl = murl + '/'
                paginate=re.compile('http://www.movie25.so/search.php.+?page=(.+?)&year=(.+?)/').findall(durl)
                for page, yearb in paginate:
                        pgs = int(page)+1
                        jurl='http://www.movie25.so/search.php?page='+str(pgs)+'&year='+str(yearb)
                main.addDir('[COLOR red]Home[/COLOR]','',0,art+'/home.png')
                r = re.findall("Next</a><a href='search.php.?page=([^<]+)&year=.+?'>Last</a>",link)
                if r:
                        main.addDir('[COLOR red]Enter Page #[/COLOR]',murl,208,art+'/gotopage.png')
                        main.addDir('[COLOR blue]Page '+str(page)+' of '+r[0]+'[/COLOR]',jurl,9,art+'/next2.png')
                else:
                        main.addDir('[COLOR blue]Page '+str(page)+'[/COLOR]',jurl,9,art+'/next2.png')
                xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
                main.VIEWS()                
        else:
                durl = murl + '/'
                paginate=re.compile('http://www.movie25.so/search.php.+?page=(.+?)&key=(.+?)/').findall(durl)
                for page, search in paginate:
                        pgs = int(page)+1
                        jurl='http://www.movie25.so/search.php?page='+str(pgs)+'&key='+str(search)
                main.addDir('[COLOR red]Home[/COLOR]','',0,art+'/home.png')
                r = re.findall(""">Next</a><a href='search.php.?page=([^<]+)&key=.+?'>Last</a>""",link)
                if r:
                        main.addDir('[COLOR blue]Page '+str(page)+' of '+r[0]+'[/COLOR]',jurl,9,art+'/next2.png')
                else:
                        main.addDir('[COLOR blue]Page '+str(page)+'[/COLOR]',jurl,9,art+'/next2.png')
        




def VIDEOLINKS(name,url):
    link=main.OPENURL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    qual = re.compile('<h1 >Links - Quality              (.+?)            </h1>').findall(link)
    quality=str(qual)
    quality=quality.replace("'","")
    name  = name.split('[COLOR blue]')[0]
    putlocker=re.compile('<li class="link_name">putlocker</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)                      
    if putlocker:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Putlocker[/COLOR]",str(putlocker),11,art+'/hosts/putlocker.png',art+'/hosts/putlocker.png')
    else:
        putlocker=re.compile("javascript:window.open.+?'http://movie25.com/redirect.php.?url=(http://www.putlocker.com/file/.+?)','.+?',.+?>(.+?)</a></span>").findall(link)
        if putlocker:
            main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Putlocker[/COLOR]",str(putlocker),11,art+'/hosts/putlocker.png',art+'/hosts/putlocker.png')
    sockshare=re.compile('<li class=link_name.+?sockshare</li>.+?<li class=".+?"><span><a href=(.+?) target=".+?">').findall(link)
    if sockshare:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Sockshare[/COLOR]",str(sockshare),22,art+'/hosts/sockshare.png',art+'/hosts/sockshare.png')
    else:
        sockshare=re.compile("javascript:window.open.+?'http://movie25.com/redirect.php.?url=(http://www.sockshare.com/file/.+?)','.+?',.+?>(.+?)</a></span>").findall(link)
        if sockshare:
            main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Sockshare[/COLOR]",str(sockshare),22,art+'/hosts/sockshare.png',art+'/hosts/sockshare.png')
    movreel=re.compile('<li class="link_name">movreel</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)
    if movreel:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Movreel[/COLOR]",str(movreel),154,art+'/hosts/movreel.png',art+'/hosts/movreel.png')
    billionuploads=re.compile('<li class="link_name">billionuploads</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)
    if billionuploads:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : BillionUploads[/COLOR]",str(billionuploads),155,art+'/hosts/billionuploads.png',art+'/hosts/billionuploads.png')
    nowvideo=re.compile('<li class="link_name">nowvideo</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)
    if nowvideo:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Nowvideo[/COLOR]",str(nowvideo),24,art+'/hosts/nowvideo.png',art+'/hosts/nowvideo.png')
    oeupload=re.compile('<li class="link_name">oeupload</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)
    if oeupload:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : 180upload[/COLOR]",str(oeupload),12,art+'/hosts/180upload.png',art+'/hosts/180upload.png')
    filenuke=re.compile('<li class="link_name">filenuke</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)
    if filenuke:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Filenuke[/COLOR]",str(filenuke),13,art+'/hosts/filenuke.png',art+'/hosts/filenuke.png')
    flashx=re.compile('<li class="link_name">flashx</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)
    if flashx:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Flashx[/COLOR]",str(flashx),15,art+'/hosts/flashx.png',art+'/hosts/flashx.png')
    novamov=re.compile('<li class="link_name">novamov</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)
    if novamov:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Novamov[/COLOR]",str(novamov),16,art+'/hosts/novamov.png',art+'/hosts/novamov.png')
    gorillavid=re.compile('<li class="link_name">gorillavid</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)
    if gorillavid:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Gorillavid[/COLOR]",str(gorillavid),148,art+'/hosts/gorillavid.png',art+'/hosts/gorillavid.png')
    divxstage=re.compile('<li class="link_name">divxstage</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)
    if divxstage:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Divxstage[/COLOR]",str(divxstage),146,art+'/hosts/divxstage.png',art+'/hosts/divxstage.png')
    movshare=re.compile('<li class="link_name">movshare</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)
    if movshare:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Movshare[/COLOR]",str(movshare),145,art+'/hosts/movshare.png',art+'/hosts/movshare.png')
    sharesix=re.compile('<li class="link_name">sharesix</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)
    if sharesix:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Sharesix[/COLOR]",str(sharesix),147,art+'/hosts/sharesix.png',art+'/hosts/sharesix.png')
    movpod=re.compile('<li class="link_name">movpod</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)
    if movpod:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Movpod[/COLOR]",str(movpod),150,art+'/hosts/movpod.png',art+'/hosts/movpod.png')
    daclips=re.compile('<li class="link_name">daclips</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)
    if daclips:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Daclips[/COLOR]",str(daclips),151,art+'/hosts/daclips.png',art+'/hosts/daclips.png')
    videoweed=re.compile('<li class="link_name">videoweed</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)
    if videoweed:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Videoweed[/COLOR]",str(videoweed),152,art+'/hosts/videoweed.png',art+'/hosts/videoweed.png')
    played=re.compile('<li class="link_name">played</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)
    if played:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Played[/COLOR]",str(played),157,art+'/hosts/played.png',art+'/hosts/played.png')
    movdivx=re.compile('<li class="link_name">movdivx</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)
    if movdivx:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : MovDivx[/COLOR]",str(movdivx),153,art+'/hosts/movdivx.png',art+'/hosts/movdivx.png')
    uploadc=re.compile('<li class="link_name">uploadc</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)
    if uploadc:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Uploadc[/COLOR]",str(uploadc),17,art+'/hosts/uploadc.png',art+'/hosts/uploadc.png')
    xvidstage=re.compile('<li class="link_name">xvidstage</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)
    if xvidstage:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Xvidstage[/COLOR]",str(xvidstage),18,art+'/hosts/xvidstage.png',art+'/hosts/xvidstage.png')        
    zooupload=re.compile('<li class="link_name">zooupload</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)
    if zooupload:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Zooupload[/COLOR]",str(zooupload),19,art+'/hosts/zooupload.png',art+'/hosts/zooupload.png')
    zalaa=re.compile('<li class="link_name">zalaa</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)
    if zalaa:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Zalaa[/COLOR]",str(zalaa),20,art+'/hosts/zalaa.png',art+'/hosts/zalaa.png')
    vidxden=re.compile('<li class="link_name">vidxden</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)
    if vidxden:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Vidxden[/COLOR]",str(vidxden),21,art+'/hosts/vidxden.png',art+'/hosts/vidxden.png')
    vidbux=re.compile('<li class="link_name">vidbux</li>.+?<li class=".+?"><span><a href="(.+?)" target=".+?">').findall(link)
    if vidbux:
        main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Vidbux[/COLOR]",str(vidbux),14,art+'/hosts/vidbux.png',art+'/hosts/vidbux.png')


def PUTLINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    putlocker = eval(url)
    try:
        for url in putlocker:
            main.addDown(name,MainUrl+url,5,art+'/hosts/putlocker.png',art+'/hosts/putlocker.png')
    except:
        for url,part in putlocker:
            main.addDown(name+"  [COLOR red]Part:"+part+"[/COLOR]",url,171,art+'/hosts/putlocker.png',art+'/hosts/putlocker.png')
def SOCKLINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    sockshare = eval(url)
    try:
        for url in sockshare:
                main.addDown(name,MainUrl+url,5,art+'/hosts/sockshare.png',art+'/hosts/sockshare.png')
    except:
        for url,part in sockshare:
            main.addDown(name+"  [COLOR red]Part:"+part+"[/COLOR]",url,171,art+'/hosts/sockshare.png',art+'/hosts/sockshare.png')
def NOWLINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    nowvideo = eval(url)
    for url in nowvideo:
        main.addDown(name,MainUrl+url,5,art+'/hosts/nowvideo.png',art+'/hosts/nowvideo.png')
def OELINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    oeupload = eval(url)
    for url in oeupload:
        main.addDown(name,MainUrl+url,5,art+'/hosts/180upload.png',art+'/hosts/180upload.png')
def FNLINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    filenuke = eval(url)
    for url in filenuke:
        main.addDown(name,MainUrl+url,5,art+'/hosts/filenuke.png',art+'/hosts/filenuke.png')
def FLALINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    flashx = eval(url)
    for url in flashx:
        main.addDown(name,MainUrl+url,5,art+'/hosts/flashx.png',art+'/hosts/flashx.png')
def VIDLINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    vidbux = eval(url)
    for url in vidbux:
        main.addDown(name,MainUrl+url,5,art+'/hosts/vidbux.png',art+'/hosts/vidbux.png')
def NOVLINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    novamov = eval(url)
    for url in novamov:
        main.addDown(name,MainUrl+url,5,art+'/hosts/novamov.png',art+'/hosts/novamov.png')
def UPLINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    uploadc = eval(url)
    for url in uploadc:
        main.addDown(name,MainUrl+url,5,art+'/hosts/uploadc.png',art+'/hosts/uploadc.png')
def XVLINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    xvidstage = eval(url)
    for url in xvidstage:
        main.addDown(name,MainUrl+url,5,art+'/hosts/xvidstage.png',art+'/hosts/xvidstage.png')
def ZOOLINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    zooupload = eval(url)
    for url in zooupload:
        main.addDown(name,MainUrl+url,5,art+'/hosts/zooupload.png',art+'/hosts/zooupload.png')
def ZALINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    zalaa = eval(url)
    for url in zalaa:
        main.addDown(name,MainUrl+url,5,art+'/hosts/zalaa.png',art+'/hosts/zalaa.png')
def VIDXLINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    vidxden = eval(url)
    for url in vidxden:
        main.addDown(name,MainUrl+url,5,art+'/hosts/vidxden.png',art+'/hosts/vidxden.png')
def PLAYEDLINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    played = eval(url)
    for url in played:
        main.addDown(name,MainUrl+url,5,art+'/hosts/played.png',art+'/hosts/played.png')
def MOVSHLINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    moveshare = eval(url)
    for url in moveshare:
        main.addDown(name,MainUrl+url,5,art+'/hosts/moveshare.png',art+'/hosts/moveshare.png')
def DIVXSLINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    divxstage = eval(url)
    for url in divxstage:
        main.addDown(name,MainUrl+url,5,art+'/hosts/divxstage.png',art+'/hosts/divxstage.png')
def SSIXLINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    sharesix = eval(url)
    for url in sharesix:
        main.addDown(name,MainUrl+url,5,art+'/hosts/sharesix.png',art+'/hosts/sharesix.png')
def GORLINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    gorillavid = eval(url)
    for url in gorillavid:
        main.addDown(name,MainUrl+url,5,art+'/hosts/gorillavid.png',art+'/hosts/gorillavid.png')
def MOVPLINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    movpod = eval(url)
    for url in movpod:
        main.addDown(name,MainUrl+url,5,art+'/hosts/movpod.png',art+'/hosts/movpod.png')
def DACLINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    daclips = eval(url)
    for url in daclips:
        main.addDown(name,MainUrl+url,5,art+'/hosts/daclips.png',art+'/hosts/daclips.png')
def VWEEDLINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    videoweed = eval(url)
    for url in videoweed:
        main.addDown(name,MainUrl+url,5,art+'/hosts/Videoweed.png',art+'/hosts/Videoweed.png')
def MOVDLINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    movdivx = eval(url)
    for url in movdivx:
        main.addDown(name,MainUrl+url,5,art+'/hosts/movdivx.png',art+'/hosts/movdivx.png')
def MOVRLINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    movreel = eval(url)
    for url in movreel:
        main.addDown(name,MainUrl+url,5,art+'/hosts/movreel.png',art+'/hosts/movreel.png')
def BUPLOADSLINKS(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    billionuploads = eval(url)
    for url in billionuploads:
        main.addDown(name,MainUrl+url,5,art+'/hosts/billionuploads.png',art+'/hosts/billionuploads.png')

def PLAY(name,murl):
        main.GA("Movie25-Movie","Watched")
        ok=True
        hname=name
        name  = name.split('[COLOR blue]')[0]
        name  = name.split('[COLOR red]')[0]
        infoLabels = main.GETMETAT(name,'','','')
        link=main.OPENURL(murl)
        match = re.search("location\.href='(.+?)'",link)
        if match:
            murl = match.group(1)
        video_type='movie'
        season=''
        episode=''
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }

        try:
            xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
            stream_url = main.resolve_url(murl)

            infoL={'Title': infoLabels['metaName'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
            # play with bookmark
            from universal import playbackengine
            player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
            #WatchHistory
            if selfAddon.getSetting("whistory") == "true":
                from universal import watchhistory
                wh = watchhistory.WatchHistory('plugin.video.movie25')
                wh.add_item(hname+' '+'[COLOR green]Movie25[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
            player.KeepAlive()
            return ok
        except Exception, e:
            if stream_url != False:
                    main.ErrorReport(e)
            return ok

def PLAYB(name,murl):
        main.GA("Movie25-Movie","Watched")
        ok=True
        hname=name
        name  = name.split('[COLOR blue]')[0]
        name  = name.split('[COLOR red]')[0]
        infoLabels = main.GETMETAT(name,'','','')
        video_type='movie'
        season=''
        episode=''
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }

        try:
            xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
            stream_url = main.resolve_url(murl)

            infoL={'Title': infoLabels['metaName'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
            # play with bookmark
            from universal import playbackengine
            player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
            #WatchHistory
            if selfAddon.getSetting("whistory") == "true":
                from universal import watchhistory
                wh = watchhistory.WatchHistory('plugin.video.movie25')
                wh.add_item(hname+' '+'[COLOR green]Movie25[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
            player.KeepAlive()
            return ok
        except Exception, e:
            if stream_url != False:
                    main.ErrorReport(e)
            return ok
