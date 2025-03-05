import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    from_email = "necmimertnl@gmail.com"  # Gönderen e-posta adresiniz
    password = "amvz ksjk hjxx ykjz"  # 2FA kullanıyorsanız uygulama şifresi kullanın

    # E-posta mesajını oluşturma
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # SMTP sunucusuna bağlanma
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # TLS bağlantısını başlat
        server.login(from_email, password)  # Gmail hesabınıza giriş yap

        # E-posta gönderimi
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)

        # Bağlantıyı kapatma
        server.quit()
        return f"E-posta başarıyla gönderildi: {to_email}"

    except smtplib.SMTPException as e:
        return f"E-posta gönderilirken hata oluştu: {e}"

