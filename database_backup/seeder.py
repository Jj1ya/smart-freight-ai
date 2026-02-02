import random
from faker import Faker
from database.connector import get_connection

# Faker 객체 생성 (랜덤 데이터 생성기)
fake = Faker()

def seed_data():
    print("🌱 Starting Data Seeding...")
    conn = get_connection()
    cur = conn.cursor()

    try:
        # 1. 운송사(Carriers) 기초 데이터 삽입
        # 이미 존재하면 넣지 않도록 간단히 처리
        carriers = [
            ('DHL', 'USD', 'contact@dhl.com'),
            ('FedEx', 'USD', 'support@fedex.com'),
            ('UPS', 'USD', 'help@ups.com')
        ]
        
        print("🚚 Seeding Carriers...")
        for name, currency, email in carriers:
            # 중복 방지를 위해 삽입 전 확인 (간단한 버전)
            cur.execute("SELECT id FROM carriers WHERE name = %s", (name,))
            if not cur.fetchone():
                cur.execute(
                    "INSERT INTO carriers (name, base_currency, contact_email) VALUES (%s, %s, %s)",
                    (name, currency, email)
                )

        # 2. 사용자(Users) 더미 데이터 50명 생성
        print("busts👤 Seeding Users (50 profiles)...")
        user_ids = []
        for _ in range(50):
            profile = fake.profile()
            username = profile['username']
            email = profile['mail']
            
            # 이메일 중복 에러 방지 (ON CONFLICT DO NOTHING은 Postgres 전용 문법)
            cur.execute("""
                INSERT INTO users (username, email) 
                VALUES (%s, %s) 
                ON CONFLICT (email) DO NOTHING
                RETURNING id;
            """, (username, email))
            
            result = cur.fetchone()
            if result:
                user_ids.append(result[0])

        # 3. 배송(Shipments) 더미 데이터 100건 생성
        print("📦 Seeding Shipments (100 orders)...")
        if user_ids: # 유저가 한 명이라도 있어야 배송을 만듦
            statuses = ['PENDING', 'IN_TRANSIT', 'DELIVERED', 'CANCELLED']
            
            for _ in range(100):
                random_user_id = random.choice(user_ids) # 랜덤 유저 선택
                origin = fake.country_code()
                dest = fake.country_code()
                weight = round(random.uniform(1.0, 50.0), 2) # 1kg ~ 50kg 랜덤
                status = random.choice(statuses)

                cur.execute("""
                    INSERT INTO shipments (user_id, origin_country, dest_country, weight_kg, status)
                    VALUES (%s, %s, %s, %s, %s)
                """, (random_user_id, origin, dest, weight, status))

        conn.commit()
        print("✅ Data Seeding Completed Successfully!")

    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        conn.rollback()
    
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    seed_data()