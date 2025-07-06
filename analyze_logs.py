from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract, col, to_date, unix_timestamp
import os
import glob
import shutil
import pandas as pd

# -----------------------------------
# 1. Initialiser la session Spark
# -----------------------------------
spark = SparkSession.builder \
    .appName("Log Analysis") \
    .getOrCreate()

# -----------------------------------
# 2. Charger le fichier de logs
# -----------------------------------
log_file = "data/web_logs.txt"
logs_df = spark.read.text(log_file)

# -----------------------------------
# 3. Définir le pattern des logs Apache
# -----------------------------------
log_pattern = r'^(\S+) - - \[(.*?)\] "(.*?) (.*?) HTTP.*" (\d{3})$'

# -----------------------------------
# 4. Extraire les champs
# -----------------------------------
logs_df = logs_df.withColumn("IP", regexp_extract("value", log_pattern, 1)) \
                 .withColumn("Timestamp", regexp_extract("value", log_pattern, 2)) \
                 .withColumn("Method", regexp_extract("value", log_pattern, 3)) \
                 .withColumn("Page", regexp_extract("value", log_pattern, 4)) \
                 .withColumn("Code", regexp_extract("value", log_pattern, 5)) \
                 .drop("value")

# -----------------------------------
# 5. Filtrer les lignes bien parsées
# -----------------------------------
logs_df = logs_df.filter(col("IP") != "")

# -----------------------------------
# 6. Aperçu
# -----------------------------------
print("Aperçu des logs parsés :")
logs_df.show(10, truncate=False)

# -----------------------------------
# 7. Statistiques : Codes HTTP
# -----------------------------------
print("Distribution des codes HTTP :")
codes_distribution = logs_df.groupBy("Code").count().orderBy("count", ascending=False)
codes_distribution.show()

# -----------------------------------
# 8 à 11. Analyses diverses
# -----------------------------------
print("Pages les plus consultées :")
logs_df.groupBy("Page").count().orderBy("count", ascending=False).show(10, truncate=False)

print("Méthodes HTTP les plus utilisées :")
logs_df.groupBy("Method").count().orderBy("count", ascending=False).show()

print("IPs les plus actives :")
logs_df.groupBy("IP").count().orderBy("count", ascending=False).show(10)

# Ajout colonne Date
logs_df = logs_df.withColumn("Date", to_date(unix_timestamp(col("Timestamp"), "dd/MMM/yyyy:HH:mm:ss").cast("timestamp")))

print("Nombre de requêtes par jour :")
logs_df.groupBy("Date").count().orderBy("Date").show()

# -----------------------------------
# 12. Export CSV codes HTTP
# -----------------------------------
temp_codes_dir = "outputs/codes_distribution_temp"
final_codes_path = "outputs/codes_distribution.csv"

codes_distribution.coalesce(1) \
    .write \
    .option("header", "true") \
    .mode("overwrite") \
    .csv(temp_codes_dir)

# -----------------------------------
# 13. Export complet des logs parsés
# -----------------------------------
temp_logs_dir = "outputs/logs_export_temp"
final_logs_path = "outputs/logs_parsed.csv"

logs_df.coalesce(1) \
    .write \
    .option("header", "true") \
    .mode("overwrite") \
    .csv(temp_logs_dir)

# -----------------------------------
# 14. Renommer les fichiers
# -----------------------------------
# → codes_distribution.csv
os.makedirs("outputs", exist_ok=True)
part_code_file = glob.glob(os.path.join(temp_codes_dir, "part-*.csv"))[0]
shutil.copy(part_code_file, final_codes_path)
shutil.rmtree(temp_codes_dir)

# → logs_parsed.csv
part_logs_file = glob.glob(os.path.join(temp_logs_dir, "part-*.csv"))[0]
shutil.copy(part_logs_file, final_logs_path)
shutil.rmtree(temp_logs_dir)

print(f" Export codes : {final_codes_path}")
print(f" Export complet : {final_logs_path}")

# -------------------------------------
# 15. Export au format CSV encodé UTF-8 (pour PostgreSQL)
# -------------------------------------
# Convertir le DataFrame Spark en DataFrame Pandas
logs_pd_df = logs_df.toPandas()

# Corriger les noms de colonnes si besoin (éviter conflit SQL)
logs_pd_df.columns = [c.lower().replace(" ", "_") for c in logs_pd_df.columns]
logs_pd_df.rename(columns={"date": "log_date"}, inplace=True)

# Créer le dossier si non existant
os.makedirs("outputs", exist_ok=True)

# Définir le nom du fichier
utf8_csv_path = "outputs/logs_parsed_utf8.csv"

# Sauvegarder en CSV avec encodage UTF-8
logs_pd_df.to_csv(utf8_csv_path, index=False, encoding='utf-8', errors='ignore')

print(f" Export CSV UTF-8 prêt pour PostgreSQL : {utf8_csv_path}")

# -----------------------------------
# 16. Stopper Spark
# -----------------------------------
spark.stop()
