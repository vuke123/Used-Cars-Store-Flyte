import psycopg2

host = "flaskpostgres-abc123.postgres.database.azure.com"
#user = 
port = "5432"
database = "postgres"
#password = 

conn = psycopg2.connect(
        host=host,
        user=user,
        port=port,
        database=database,
        password=password
    )
    
cursor = conn.cursor()
cursor.execute("SELECT engine, power FROM uc_training_data")
data = cursor.fetchall()
print(data)
