from dotenv import load_dotenv
import os 
import psycopg

load_dotenv()

Connection_String = os.getenv("DATABASE_URL")  


def ConnectDB():
    try:
            
        with psycopg.connect(conn_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT NOW()")
                time = cur.fetchone()
                
    except Exception as e:
        print("error:",ValueError(e))

