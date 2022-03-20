from bs4 import BeautifulSoup as bs
import datetime
from jikanpy import AioJikan
from difflib import SequenceMatcher
import asyncio




class AnimeDetay:
    kategori = ""
    digerAdlari = ""
    japonca = ""
    animeTuru = []
    bolumSayisi = []
    baslamaTarihi = ""
    bitisTarihi = ""
    yasSiniri = ""
    yapimci = ""
    bolumSuresi = 0
    puani = 0.0
    ozet = ""
    mal_id=""
    mal_ImgUrl = ""
    mal_score=""
    mal_ytTrailerUrl=""

    def __switchDateTime(self, dateStr):
        switcher = {
            "Ocak": 1,
            "Şubat": 2,
            "Mart": 3,
            "Nisan": 4,
            "Mayıs": 5,
            "Haziran": 6,
            "Temmuz": 7,
            "Ağustos": 8,
            "Eylül": 9,
            "Ekim": 10,
            "Kasım": 11,
            "Aralık": 12
        }
        end = dateStr.find(",")
        dateStrList = dateStr[:end].strip().split(" ")
        month = switcher.get(dateStrList[1], "")
        if month:
            date_str = dateStrList[0]+"-"+str(month)+"-"+dateStrList[2]
            return datetime.datetime.strptime(date_str, '%d-%m-%Y').date()

    def __characterChanger(self, word):
        def func(s): return s[:1].lower() + s[1:] if s else ''
        if len(word) > 1:
            newWord = func(word)
            newWord = newWord.replace("ö", "o")
            newWord = newWord.replace("Ö", "O")
            newWord = newWord.replace("ü", "u")
            newWord = newWord.replace("Ü", "U")
            newWord = newWord.replace("ş", "s")
            newWord = newWord.replace("Ş", "S")
            newWord = newWord.replace("ç", "c")
            newWord = newWord.replace("Ç", "C")
            newWord = newWord.replace("ğ", "g")
            newWord = newWord.replace("Ğ", "G")
            newWord = newWord.replace("İ", "I")
            newWord = newWord.replace("ı", "i")
            newWord = newWord.replace(" ", "")
            newWord = newWord.replace(";", "")
            return newWord
        else:
            return None
        
        async def __animeSearch(self,name):
            async with AioJikan() as aio_jikan:
                return await aio_jikan.search(search_type='anime', query=name)
        
        async def __getAnime(self,id):
            episodes=[]
            async with AioJikan() as aio_jikan:
                anime= await aio_jikan.anime(id)
                _episodes=await aio_jikan.anime(id,extension='episodes',page=1)
                episodes.append(_episodes)
                EpLP=int(_episodes["episodes_last_page"]);
                if int(EpLP)>1:
                    for i in range(2,EpLP+1):
                        _episodes=await aio_jikan.anime(id,extension='episodes',page=i)

                        





    def __init__(self, source,name):
        super().__init__()
        soup = bs(source)
        img = soup.find_all("img")[0]

        if img["src"]:
            self.resimLink = img["src"]

        rank = img.next
        if rank:
            self.puani = float(rank.text)

        animeDetay = soup.find("div", id="animedetay")
        malAnimeSearch=asyncio.run(self.__animeSearch(name))
        if malAnimeSearch["results"]:
            for result in malAnimeSearch["results"]:
                similarityRatio = SequenceMatcher(None,result["title"].lower(),name.lower()).ratio()
                if similarityRatio>=0.9:
                    malAnime=asyncio.run(self.__getAnime(result["mal_id"]))
                    self.mal_id=malAnime["mal_id"]
                    self.mal_score=malAnime["score"]
                    self.mal_ImgUrl=malAnime["image_url"]
                      
        trler = animeDetay.find_all("tr")
        for tr in trler:
            textlist = tr.text.split(":")
            if len(textlist) == 2:
                baslik = self.__characterChanger(textlist[0])
                deger=textlist[1].strip()
                if baslik and len(deger)>1:
                    if baslik == "kategori":
                        self.kategori = deger
                    elif baslik == "digerAdlari":
                        self.digerAdlari = deger
                    elif baslik == "japonca":
                        self.japonca = deger
                    elif baslik == "animeTuru":
                        for d in deger.split(" "):
                            if d.strip():
                                self.animeTuru.append(d) 
                    elif baslik == "bolumSayisi":
                        self.bolumSayisi = deger
                    elif baslik == "baslamaTarihi":
                        self.baslamaTarihi = self.__switchDateTime(deger)
                    elif baslik == "bitisTarihi":
                        self.bitisTarihi = self.__switchDateTime(deger)
                    elif baslik == "yasSiniri":
                        self.yasSiniri = deger
                    elif baslik == "yapimci":
                        self.yapimci = deger
                    elif baslik == "bolumSuresi":
                        self.bolumSuresi = deger
                    elif baslik == "ozet":
                        self.ozet = int(deger.split(" ")[0])