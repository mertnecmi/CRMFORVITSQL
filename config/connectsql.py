import psycopg2

# PostgreSQL bağlantısı oluştur
conn = psycopg2.connect(
    dbname="crmtovit",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

def query(query, params= None):
    cur.execute(query, params,)
    dveri = cur.fetchall()
    return dveri


def insert(query, params):
        try:
            cur.execute(query, params)
            conn.commit()
            print("Veri başarıyla eklendi.")
        except psycopg2.Error as e:
            print(f"Veri eklenirken hata oluştu: {e}")
        finally:
            conn.commit()  # Değişiklikleri kaydet

def update(q,p):
    cur.execute( q, p,)
    conn.commit()
