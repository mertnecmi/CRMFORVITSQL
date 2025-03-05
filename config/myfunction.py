import datetime
import pandas as pd


class MyAttr:
    def __init__(self):
        self.today = None
        
    def to_day(self):
        self.today = datetime.date.today()
        self.today = self.today.strftime("%d-%m-%Y")
        return self.today




    def tarih_format_degistir(self, tarih_string):
        try:
            # Eğer tarih zaten bir datetime nesnesiyse, onu stringe çeviriyoruz
            if isinstance(tarih_string, datetime.datetime):
                return tarih_string.strftime("%d-%m-%Y")

            # String'in başındaki ve sonundaki boşlukları temizle
            tarih_string = tarih_string.strip()

            # Farklı tarih formatlarını dene
            possible_formats = ["%Y-%m-%d %H:%M:%S", "%d-%m-%Y"]  

            for fmt in possible_formats:
                try:
                    date_object = datetime.datetime.strptime(tarih_string, fmt)
                    return date_object.strftime("%d-%m-%Y")  # Gün-Ay-Yıl formatında döndür
                except ValueError:
                    continue  # Bu format uymadıysa diğerini dene

            # Hiçbir format uymadıysa hata ver
            raise ValueError(f"Geçersiz tarih formatı: {tarih_string}")

        except ValueError as e:
            print(f"Tarih Hatası: {e}")  # Hata mesajını yazdır
            return ""  # Hata durumunda boş döndür

    
    def read_xlsx(self, file_path):
        try:
            # Dosyayı pandas ile oku
            df = pd.read_excel(file_path)
            #print(f"Dosya: {file_path} içeriği:")
            #print(df.head())  # İlk birkaç satırı yazdır

            # Veriyi listeye dönüştürme (her satır bir liste elemanı olacak)
            data_list = df.values.tolist()  # Tüm veriyi listeye alır

            return data_list
        
        except Exception as e:
            print(f"Dosya okunurken hata oluştu: {e}")
            return None
    def read_xlsx_header(self, file_path, header_row=0):
        try:
            # Dosyayı pandas ile oku, sadece ilk satırı almak için nrows parametresi ekleniyor
            df = pd.read_excel(file_path, header=header_row, nrows=1)
            
            # Veriyi listeye dönüştürme (sadece ilk satır alınacak)
            data_list = df.values.tolist()  # İlk satırı listeye alır

            return data_list
            
        except Exception as e:
            print(f"Dosya okunurken hata oluştu: {e}")
            return None