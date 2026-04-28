import psycopg2
import json
import os

DATABASE_URL = "postgres://99be508d44282a3a1afd94c0bd57a6546ab54d006552c343596ebe66041d5400:sk_9hF93tATSU3czfR6F3J2Y@db.prisma.io:5432/postgres?sslmode=require"

def export_table_to_json():
    conn = None
    try:
        # 1. Connect using full URL
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # 2. Query your table
        cursor.execute('''SELECT * FROM "Post" ORDER BY "createdAt" DESC;''')

        # 3. Column names
        colnames = [desc[0] for desc in cursor.description]

        # 4. Fetch data
        rows = cursor.fetchall()

        # 5. Convert to dict
        data = [dict(zip(colnames, row)) for row in rows]

        # 6. Save JSON
        with open("data/output.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, default=str)

        print("Export complete ✅")

    except Exception as e:
        print("Error:", e)

    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    export_table_to_json()