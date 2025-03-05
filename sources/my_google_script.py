import json
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account


# # JSON anahtar dosyasının yolu
# SERVICE_ACCOUNT_FILE = 'config/vit-project-450321-8da140d2ff54.json'

# # Google Drive API'ye bağlanma
# SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
# credentials = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# service = build('drive', 'v3', credentials=credentials)

# # Drive API ile dosya listeleme örneği
# results = service.files().list().execute()
# items = results.get('files', [])

# if not items:
#     print('No files found.')
# else:
#     for item in items:
#         print(f'{item["name"]} ({item["id"]})')

# Hizmet hesabı JSON dosyasından kimlik doğrulaması yaparak credentials oluşturma
def authenticate_service_account(json_file):
    try:
        # JSON dosyasını kullanarak kimlik doğrulaması yapmak için gerekli credentials'ı oluşturuyoruz
        creds = Credentials.from_service_account_file(
            json_file, 
            scopes=["https://www.googleapis.com/auth/drive.readonly"]
        )
        return creds
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return None

# Google Drive API'ye bağlanma
def authenticate_google_drive_with_service_account(credentials):
    try:
        # Google Drive API servisini başlat
        service = build('drive', 'v3', credentials=credentials)
        return service
    except Exception as e:
        print(f"Google Drive API bağlantısı başarısız oldu: {e}")
        return None

# Drive'dan dosya listeleme örneği
def list_drive_files(service):
    try:
        # Dosyaları listele (ismi ve ID'si ile)
        results = service.files().list(
            fields="nextPageToken, files(id, name)"
        ).execute()
        
        items = results.get('files', [])
        
        if not items:
            print("Hiç dosya bulunamadı.")
        else:
            print("Bulunan dosyalar:")
            for item in items:
                print(f"{item['name']} ({item['id']})")

    except Exception as e:
        print(f"Dosya listeleme sırasında bir hata oluştu: {e}")


import os
from googleapiclient.http import MediaIoBaseDownload
from io import BytesIO
import pandas as pd


def download_file(service, file_id, destination):
    try:
        request = service.files().get_media(fileId=file_id)
        fh = BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"İndirme {int(status.progress() * 100)}%.")
        
        # Dosyayı kaydet
        with open("data/"+destination, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())
        print(f"Dosya '{destination}' olarak kaydedildi.")
    
    except Exception as e:
        print(f"Dosya indirirken hata oluştu: {e}")

# .xlsx uzantılı dosyaları listeleyip indir
def download_xlsx_files(service):
    try:
        results = service.files().list(
            fields="nextPageToken, files(id, name)"
        ).execute()
        
        items = results.get('files', [])
        
        if not items:
            print("Hiç dosya bulunamadı.")
        else:
            print("Bulunan .xlsx dosyalar:")
            for item in items:
                if item['name'].endswith('.xlsx'):
                    print(f"İndirilen dosya: {item['name']} ({item['id']})")
                    download_file(service, item['id'], item['name'])
                    # Dosyayı okuma ve verileri listeye dönüştürme
                    
                    #data = read_xlsx(item['name'])  # Veriyi bir listeye alıyoruz
                    #print(f"Veri listesi: {data}")
    except Exception as e:
        return(f"Dosya listeleme sırasında bir hata oluştu: {e}")

def main():
    # Hizmet hesabı JSON dosyasının yolunu belirtin
    credentials = authenticate_service_account('config/vit-project-450321-8da140d2ff54.json')  # JSON dosyanızın adı
    
    if credentials:
        print("Hizmet hesabı ile kimlik doğrulama başarılı!")
        
        # Google Drive API'ye bağlan
        service = authenticate_google_drive_with_service_account(credentials)
        
        if service:
            
            # Dosya listeleme işlemi
            list_drive_files(service)
            download_xlsx_files(service)
            return("Google Drive API bağlantısı başarılı!")
        else:
            return("Google Drive API bağlantısı başarısız.")
    else:
        return("Kimlik doğrulama başarısız.")

