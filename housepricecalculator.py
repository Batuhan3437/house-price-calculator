import pandas as pd
from sklearn import linear_model
from pymongo import MongoClient

df = pd.read_csv("reading_data/multilinearregression.csv", sep=";")

reg = linear_model.LinearRegression()
reg.fit(df[['alan', 'odasayisi', 'binayasi']], df['fiyat'])

print("=============================\n")
print("Ev fiyatı tahmin edici yapay zeka")
print("\n=============================\n")

# MongoDB connection
client = MongoClient('"""MongoDB Connection"""')
db = client['Ev_fiyat']
collection = db['veri_my']

while True:
    metre_kare = int(input("\nmetre kare sayısını giriniz: "))
    oda_sayisi = int(input("\noda sayısını giriniz: "))
    bina_yasi = int(input("\nbina yaşını giriniz: "))

    if oda_sayisi >= 1 and metre_kare >= 1 and bina_yasi >= 0:
        sonuc = int(reg.predict([[metre_kare, oda_sayisi, bina_yasi]]))
        formatted_x = "{0:,}".format(sonuc).replace(",", ".")
        
        print("=============================\n")
        print("\nBinanın tahmini fiyatı:", formatted_x, "₺")
        print("\n=============================\n")
        print("\n=============================\n")
        
        # MongoDB'ye veri ekleme
        document = {'metre kare': metre_kare, 'oda sayısı': oda_sayisi, 'bina yaşı': bina_yasi, 'evin fiyatı': formatted_x}
        collection.insert_one(document)
    else:
        print("\nDeğerler sıfırdan küçük olamaz, lütfen yeniden deneyiniz.\n")
        continue

    devam = input("Yeni bir tahmin yapmak için 'devam' yazın, çıkmak için 'q' ya da 'quit' yazın: ")
    
    if devam.lower() in ["q", "quit"]:
        break

# Bağlantıyı kapatın
client.close()
