from bs4 import BeautifulSoup
import requests

# Anggi Wijaya

def main():
    print("======= List Commands =======\n [1]Anime Terbaru\n [2]Cari Anime")
    tipe = int(input())
    if tipe == 1:
        max = int(input("Max Data?"))
        if max not in range(1, 15):
            print("Max 14 hehe")
            max = int(input("Max Data? : "))
        else:
            #ScrapeData(tipe, max)
            print("Pakai Command 2 Dulu")
    elif tipe == 2:
        keyword = input("Keyword? :")
        max = int(input("Max Data? : "))
        if max not in range(1, 8):
            print("Max 7 hehe")
            max = int(input("Max Data? : "))
        else:
            ScrapeData(tipe, max, keyword)
    else:
        print("hmmm,","\n Command Not found.")
        exit()


# Save into file
def Save(no, judul, link):
    # Filename to append
    filename = "linkdownload.txt"
    # The 'a' flag tells Python to keep the file contents
    # and append (add line) at the end of the file.
    myfile = open(filename, 'a')
    # Add the line
    myfile.write(no + '. Judul : ' + judul + '\nLink : https:' + link + '\n\n')
    # Close the file
    myfile.close()


# Function Scrape Data
def ScrapeData(tipe, max, search=''):
    link = ''
    no = 0
    if tipe == 1:
        link = "http://www.samehadaku.tv"
        init = requests.get(link)
        if init.status_code == 200:
            Parser = BeautifulSoup(init.content, 'html.parser')
            getlink1 = Parser.find_all("h3",class_="post-title")
            getlink1 = getlink1[0:int(max)]
            print("prosess getting data, wait for a sec..")
            for a in getlink1:
                linkopen = a.find("a").get('href')
                RequestLink1 = requests.get(linkopen)
                if RequestLink1.status_code == 200:
                    Respon1 = BeautifulSoup(RequestLink1.content, 'html.parser')
                    # Ambil Judul
                    judul = Respon1.find(class_="post-title entry-title").text
                    # Select Class, Ambil Resolusi 720P Server ZippyShare
                    extract1 = Respon1.find("div", class_="download-eps").select("li:nth-of-type(3) > a:nth-of-type(4)")
                    for a in extract1:
                        no += 1
                        RequestLink2 = requests.get(a['href'])
                        Respon2 = BeautifulSoup(RequestLink2.content, 'html.parser')
                        extract2 = Respon2.find("div", class_="download-link").find("a")

                        RequestLink3 = requests.get(extract2["href"])
                        Respon3 = BeautifulSoup(RequestLink3.content, 'html.parser')
                        extract3 = Respon3.find("div", class_="download-link").find("a")

                        RequestLink4 = requests.get(extract3["href"])
                        Respon4 = BeautifulSoup(RequestLink4.content, 'html.parser')

                        if (Respon4.find('div', class_="video-share") is None):
                            LinkFinal = 'none'
                            Status = "Failed, Can't Fetch Url Data."
                        else:
                            LinkFinal = Respon4.find('div', class_="video-share").find('input').get(
                                    'value')
                            Status = no, "Success."
                        Save(str(no), judul, LinkFinal)
                        print(linkopen)

    elif tipe == 2:
        link = "http://www.samehadaku.tv/?s=%s" % search
        init = requests.get(link)
        if init.status_code == 200:
            Parser = BeautifulSoup(init.content, 'html.parser')
            getlink1 = Parser.find_all(class_="more-link button", limit=max)

            print("prosess getting data, wait for a sec..")
            for i in getlink1:
                RequestLink1 = requests.get(i['href'])
                if RequestLink1.status_code == 200:
                    Respon1 = BeautifulSoup(RequestLink1.content, 'html.parser')
                    # Ambil Judul
                    judul = Respon1.find(class_="post-title entry-title").text
                    # Select Class, Ambil Resolusi 720P Server ZippyShare
                    extract1 = Respon1.find("div", class_="download-eps").select("li:nth-of-type(3) > a:nth-of-type(4)")
                    for a in extract1:
                        no += 1
                        RequestLink2 = requests.get(a['href'])
                        Respon2 = BeautifulSoup(RequestLink2.content, 'html.parser')
                        extract2 = Respon2.find("div", class_="download-link").find("a")

                        RequestLink3 = requests.get(extract2["href"])
                        Respon3 = BeautifulSoup(RequestLink3.content, 'html.parser')
                        extract3 = Respon3.find("div", class_="download-link").find("a")

                        RequestLink4 = requests.get(extract3["href"])
                        Respon4 = BeautifulSoup(RequestLink4.content, 'html.parser')

                        if (Respon4.find('div', class_="video-share") is None):
                            LinkFinal = 'none'
                            Status = "Failed, Can't Fetch Url Data."
                        else:
                            LinkFinal = Respon4.find('div', class_="video-share").find('input').get(
                                'value')
                            Status = no, "Success."
                        Save(str(no), judul, LinkFinal)
                        print(Status)
    else:
        print('Hmmmmmmmmmmmm ?????? ')
        exit()

if __name__ == '__main__':
    main()
