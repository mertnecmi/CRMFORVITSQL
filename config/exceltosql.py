import connectsql as c
import pandas as pd
import myfunction as mf


def temizle_deger(value):
    if isinstance(value, str):  # Eğer değer string ise
        return value.strip().replace("\n", "").replace("\r", "")
    return value  # Eğer string değilse aynen bırak

query= "select * from kursiyerler"
veri = c.query(query)
print(veri)
for v in veri:
    isim =  temizle_deger(v[1])
    id = v[0]
    print(isim,id)
    q =  "update kursiyerler set adsoyad = %s where kursiyer_id = %s"
    p = (isim, id)
  
    c.update(q,p)


# mf = mf.MyAttr()
# veri = mf.read_xlsx("data/Mulakatlar.xlsx")

# # veri = mf.read_xlsx("data/Basvurular .xlsx")
# cur = c.cur
# for v in veri:
# # for v in veri:
#     cur.execute("SELECT * FROM kursiyerler WHERE adsoyad = %s", (v[0],))
#     dveri = cur.fetchall()
#     id = (dveri[0][0])
#     gtarih = mf.tarih_format_degistir(v[1])
#     itarih = mf.tarih_format_degistir(v[2])
#     # print(id,v[0])
#     query = """insert into projetakip (
#         kursiyerid, pgondermet, pgelist
#     ) values (%s, %s, %s) """
# #     insert_query = """INSERT INTO basvurular (
# #             kursiyerid, zamandamgasi, suankidurum, itphegitimkatilmak, ekonomikdurum, 
# #             dilkursunadevam, ingilizceseviye, hollandacaseviye, baskigoruyor , bootcampbitirdi, 
# #             onlineitkursu, ittecrube, projedahil, calismakistegi, nedenkatilmakistiyor, 
# #             basvurudonemi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
# #     params = (id, tarih, v[6], v[7], v[8], v[9], v[10], v[11], v[12], v[13], v[14], v[15], v[16], v[17], v[18],v[21])
#     params = (id, gtarih, itarih, )
#     c.insert(query, params) 

# cur.close()
# c.conn.close()
