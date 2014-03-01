import json
import urllib.request
import re


class youtube:
    def __init__(self, core, client):
        try:
            self.apikey = core.mconf['moduleconf']['googleapikey']
            if self.apikey == "":
                return None
        except:
            return None
        core.addHandler("pubmsg", self, "ytlinks")
    
    def ytlinks(self, cli, ev):
        yr = re.compile("youtube\.com\/watch\?.*v=([A-Za-z0-9._%-]*)[&\w;=\+_\-]*")
        res = yr.search(" ".join(ev.splitd))
        if res is not None:
            r = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/videos?id=" + m1.group(1) +"&part=id,contentDetails,statistics,snippet&key=" + self.apikey)
            jao = json.loads(r.decode('utf-8'))
            vtitle = jao['items'][0]['snippet']['title']
            views = jao['items'][0]['statistics']['viewCount']
            likes = jao['items'][0]['statistics']['likeCount']
            dislikes = jao['items'][0]['statistics']['dislikeCount']
            comments = jao['items'][0]['statistics']['commentCount']
            duration = jao['items'][0]['contentDetails']['duration']
            tr = re.compile("PT(\d{1,})*(H)*(\d{1,})(M)*(\d{1,})(S)*")
            tm = tr.search(duration)
            m = 0
            h = 0
            try:
                s = tm.group(3)
                m = tm.group(2)
                h = tm.group(1)
            except:
                pass
            if s < 10:
                s = "0" + str(s)
            if m < 10:
                s = "0" + str(m)
            if h < 10:
                s = "0" + str(h)
            rank = round((likes / (likes + dislikes)) * 100)
            resp = "\2%s\2 \00310Duración:\003 %s:%s:%s \00310Visto\003 \2%s\2" \
                " veces, con \00303%s \2Me gusta\2\003, \00305%s \2No me gusta\2\003" \
                " (%s\%) y %s \2comentarios\2" % (vtitle, str(h), str(m), str(s),
                views, likes, dislikes, rank, comments)
            cli.privmsg(ev.target, resp)
