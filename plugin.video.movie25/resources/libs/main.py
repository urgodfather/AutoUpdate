import urllib,re,string,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import time,threading
#Mash Up - by Mash2k3 2012.

addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
mashpath = selfAddon.getAddonInfo('path')
grab = None
fav = False
hostlist = None
Dir = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.movie25', ''))
repopath = xbmc.translatePath(os.path.join('special://home/addons/repository.mash2k3', ''))
datapath = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
supportsite = 'mashupxbmc.com'
hosts = 'putlocker,sockshare,billionuploads,hugefiles,mightyupload,movreel,lemuploads,180upload,megarelease,filenuke,flashx,gorillavid,bayfiles,veehd,vidto,mailru,videomega,epicshare,bayfiles,2gbhosting,alldebrid,allmyvideos,vidspot,castamp,cheesestream,clicktoview,crunchyroll,cyberlocker,daclips,dailymotion,divxstage,donevideo,ecostream,entroupload,facebook,filebox,hostingbulk,hostingcup,jumbofiles,limevideo,movdivx,movpod,movshare,movzap,muchshare,nolimitvideo,nosvideo,novamov,nowvideo,ovfile,play44_net,played,playwire,premiumize_me,primeshare,promptfile,purevid,rapidvideo,realdebrid,rpnet,seeon,sharefiles,sharerepo,sharesix,skyload,stagevu,stream2k,streamcloud,thefile,tubeplus,tunepk,ufliq,upbulk,uploadc,uploadcrazynet,veoh,vidbull,vidcrazynet,video44,videobb,videofun,videotanker,videoweed,videozed,videozer,vidhog,vidpe,vidplay,vidstream,vidup,vidx,vidxden,vidzur,vimeo,vureel,watchfreeinhd,xvidstage,yourupload,youtube,youwatch,zalaa,zooupload,zshare'
if selfAddon.getSetting('visitor_ga')=='':
    from random import randint
    selfAddon.setSetting('visitor_ga',str(randint(0, 0x7fffffff)))

VERSION = str(selfAddon.getAddonInfo('version'))
#PATH = "MashUp-DEV"  
PATH = "MashUp-"            
UATRACK="UA-38312513-1" 

try:
    log_path = xbmc.translatePath('special://logpath')
    log = os.path.join(log_path, 'xbmc.log')
    logfile = open(log, 'r').read()
    match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built').search(logfile)
    if not match:
        match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?bit)').search(logfile)
        if match:
            build = match.group(1)
            PLATFORM = match.group(2)
            print 'XBMC '+build+' Platform '+PLATFORM
        else:
            PLATFORM=''
except:
    PLATFORM=''

sys.path.append( os.path.join( selfAddon.getAddonInfo('path'), 'resources', 'libs' ))
################################################################################ Common Calls ##########################################################################################################
if selfAddon.getSetting("skin") == "0":
    art = 'https://raw.github.com/mash2k3/MashupArtwork/master/skins/vector'
    fanartimage=Dir+'fanart2.jpg'
else:
    art = 'https://raw.github.com/mash2k3/MashupArtwork/master/skins/greenmonster'
    fanartimage=Dir+'fanart.jpg'
elogo = xbmc.translatePath('special://home/addons/plugin.video.movie25/resources/art/bigx.png')
slogo = xbmc.translatePath('special://home/addons/plugin.video.movie25/resources/art/smallicon.png')

def OPENURL(url, mobile = False, q = False, verbose = True, timeout = 10, cookie = None, data = None, cookiejar = False, log = True, headers = [], type = '',ua = False):
    import urllib2 
    UserAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    if ua: UserAgent = ua
    try:
        if log:
            print "MU-Openurl = " + url
        if cookie and not cookiejar:
            import cookielib
            cookie_file = os.path.join(os.path.join(datapath,'Cookies'), cookie+'.cookies')
            cj = cookielib.LWPCookieJar()
            if os.path.exists(cookie_file):
                try: cj.load(cookie_file,True)
                except: cj.save(cookie_file,True)
            else: cj.save(cookie_file,True)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        elif cookiejar:
            import cookielib
            cj = cookielib.LWPCookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        else:
            opener = urllib2.build_opener()
        if mobile:
            opener.addheaders = [('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')]
        else:
            opener.addheaders = [('User-Agent', UserAgent)]
        for header in headers:
            opener.addheaders.append(header)
        if data:
            if type == 'json': 
                import json
                data = json.dumps(data)
                opener.addheaders.append(('Content-Type', 'application/json'))
            else: data = urllib.urlencode(data)
            response = opener.open(url, data, timeout)
        else:
            response = opener.open(url, timeout=timeout)
        if cookie and not cookiejar:
            cj.save(cookie_file,True)
        link=response.read()
        response.close()
        opener.close()
        #link = net(UserAgent).http_GET(url).content
        link=link.replace('&#39;',"'").replace('&quot;','"').replace('&amp;',"&").replace("&#39;","'").replace('&lt;i&gt;','').replace("#8211;","-").replace('&lt;/i&gt;','').replace("&#8217;","'").replace('&amp;quot;','"').replace('&#215;','x').replace('&#038;','&').replace('&#8216;','').replace('&#8211;','').replace('&#8220;','').replace('&#8221;','').replace('&#8212;','')
        link=link.replace('%3A',':').replace('%2F','/')
        if q: q.put(link)
        return link
    except Exception as e:
        if verbose:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Source Website is Down,3000,"+elogo+")")
        xbmc.log('***********Website Error: '+str(e)+'**************', xbmc.LOGERROR)
        import traceback
        traceback.print_exc()
        link ='website down'
        if q: q.put(link)
        return link
