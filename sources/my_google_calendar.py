import os
import datetime
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google Calendar API'ye erişim sağlamak için gerekli yetkilendirme
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_google_calendar_events():
    creds = None
    # Token dosyasını kontrol et (yetkilendirme)
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # Eğer geçerli token yoksa veya geçersizse, OAuth2 işlemi yap
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'config/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Token'ı kaydet
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Calendar API servisini oluştur
    service = build('calendar', 'v3', credentials=creds)

    # Etkinlikleri almak için API'yi kullan
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' UTC saatini belirtir
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    
    events = events_result.get('items', [])

    if not events:
        print('Etkinlik bulunamadı.')
    else:
        event_list = []
        for event in events:
            # Etkinlikten alınabilecek tüm bilgileri çıkarıyoruz
            start = event['start'].get('dateTime', event['start'].get('date'))
            attendees = event.get('attendees', [])
            event_data = {
                'summary': event.get('summary', 'Başlık yok'),
                'start': start,
                'location': event.get('location', 'Yer bilgisi yok'),
                'description': event.get('description', 'Açıklama yok'),
                'attendees': [{'email': attendee.get('email'), 'responseStatus': attendee.get('responseStatus')} for attendee in attendees],
            }
            event_list.append(event_data)
        return event_list

# Etkinlikleri al
event = get_google_calendar_events()
#print(event)
