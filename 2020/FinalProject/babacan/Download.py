import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import sys
import lxml

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138"
headers = {"user-agent": user_agent}
resp = req.get(f"https://eksisozluk.com/", headers=headers)
df = pd.DataFrame()


def _get_page_entries(page_number, topics, topic):
    global df, resp
    resp = req.get(f"https://eksisozluk.com/{topic}?p={page_number}", headers=headers)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "lxml")
        entry_list = soup.find("ul", {"id": "entry-item-list"})
        entries = entry_list.find_all("li")
        for entry in entries:
            entry_content = entry.find("div", {"class": "content"}).text
            entry_content = entry_content.replace("\r", " ").replace("\n", " ").strip()
            entry_author = entry.find("a", {"class": "entry-author"}).text
            entry_date = entry.find("a", {"class": "entry-date permalink"}).text
            if " ~ " in entry_date:
                entry_date = entry_date.split(" ~ ")[0]
            row_dict = {"date": entry_date,
                        "author": entry_author,
                        "topic": topics[topic],
                        "content": entry_content}
            df = df.append(row_dict, ignore_index=True)
            #print(f"{entry_content}\n{entry_date}\t{entry_author}\n----------------")#test purposes


def _analyze_topic(topics, topic, num_topic):
    global df, resp
    page_number = 1
    _get_page_entries(page_number, topics, topic)

    resp = req.get(f"https://eksisozluk.com/{topic}?p={page_number}", headers=headers)

    while resp.status_code == 200:# and page_number < 2:#test purposes
        page_number += 1
        _print_progress_bar(page_number, topics[topic], prefix="Downloading page")
        _get_page_entries(page_number, topics, topic)
    sys.stdout.write(f"\rDownload of topic {num_topic} ({topics[topic]}) complete with {page_number} pages\n")


def _print_progress_bar(page, topic, prefix=""):
    sys.stdout.write(f"\r{prefix} {page} of topic {topic}")
    sys.stdout.flush()


def download(path):
    global df, resp
    topics = {"ali-babacan--414679": "ali babacan",
              "25-mayis-2020-cuneyt-ozdemir-ali-babacan-yayini--6535493": "25 mayıs 2020 cüneyt özdemir ali babacan yayını",
              "ali-babacanin-yeni-parti-aciklamasi--6025196": "ali babacan'ın yeni parti açıklaması",
              "ali-babacanin-gumbur-gumbur-geliyor-olmasi--6110627": "ali babacan'ın gümbür gümbür geliyor olması",
              "ali-babacanin-kuracagi-parti--4706840": "ali babacan'ın kuracağı parti",
              "akpyi-elestirip-ali-babacani-sevmek--4505072": "akp'yi eleştirip ali babacan'ı sevmek",
              "ali-babacanin-basbakan-olmasi--1901610": "ali babacan'ın başbakan olması",
              "ali-babacanin-omurgasizligini-itiraf-etmesi--6537372": "ali babacan'ın omurgasızlığını itiraf etmesi",
              "ali-babacanin-41-oy-oranina-dayanmasi--6536837": "ali babacan'ın %41 oy oranına dayanması",
              "ali-babacana-oy-vermiyoruz-kampanyasi--6534947": "ali babacan'a oy vermiyoruz kampanyası",
              "gunlerdir-yapilan-ali-babacan-pr-calismasi--6536823": "günlerdir yapılan ali babacan pr çalışması",
              "ali-babacanin-odtuyu-4-0-ortalama-ile-bitirmesi--6284234": "ali babacan'ın odtü'yü 4.0 ortalama ile bitirmesi",
              "25-mayis-2020-halk-tv-ali-babacan-canli-yayini--6535263": "25 mayıs 2020 halk tv ali babacan canlı yayını",
              "ali-babacan-eksi-sozluke-gelsin-kampanyasi--6533246": "ali babacan ekşi sözlük'e gelsin kampanyası",
              "140journosin-ali-babacan-belgeseli--6524689": "140journos'ın ali babacan belgeseli",
              "ali-babacana-sorulacak-tek-soru--6535458": "ali babacan'a sorulacak tek soru",
              "dusun-ki-ali-babacan-bunu-okuyor--6537113": "düşün ki ali babacan bunu okuyor",
              "ali-babacanin-oy-orani-34e-dayandi-iddiasi--6524893": "ali babacan'ın oy oranı %34'e dayandı iddiası",
              "ali-babacanin-oy-oraninin-35e-dayanmasi--6443009": "ali babacan'ın oy oranının %35'e dayanması",
              "ali-babacanin-yuzde-30-oy-almasi--6535069": "ali babacan'ın yüzde 30 oy alması",
              "ali-babacan-fetocudur--6443185": "ali babacan fetöcüdür",
              "dusun-ki-ali-babacan-bunu-okuyor--6537113": "düşün ki ali babacan bunu okuyor",
              "ali-babacan-turkiyenin-justin-trudeausudur--6282471": "ali babacan türkiye'nin justin trudeau'sudur",
              "ali-babacan-tarafindan-kurulacak-merkez-sag-parti--5870345": "ali babacan tarafından kurulacak merkez sağ parti",
              "ali-babacanin-partisi-deyince-akla-gelen-ilk-sey--6529953": "ali babacan'ın partisi deyince akla gelen ilk şey",
              "8-temmuz-2019-ali-babacanin-akpden-istifa-etmesi--6100718": "8 temmuz 2019 ali babacan'ın akp'den istifa etmesi",
              "140journosun-sakin-kader-deme-videosu--6524672": "140journos'un sakın kader deme videosu"}

    #print("----------------\n")
    resp = req.get(f"https://eksisozluk.com/", headers=headers)
    df = pd.DataFrame(columns=("date", "author", "topic", "content"))
    print(f"Starting to download {len(topics)} topics.")
    num_topic = 0
    for topic in topics:
        num_topic += 1
        _analyze_topic(topics, topic, num_topic)

    print("Writing to csv.")
    df.to_csv(f"{path}babacan_eksisozluk.csv", index=False, encoding="utf-8-sig")
    print("Writing to csv completed.")
    print("Data download completed.\n\n")
