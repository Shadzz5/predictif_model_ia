import os
import time
import pandas as pd
import clickhouse_connect

start = time.time()
print("Début du traitement")
# Connexion à la base ClickHouse
client = clickhouse_connect.get_client(host='clickhouse', port=8123, username='clickhouse-user', password='secret')

# Création de la table dans ClickHouse (si elle n'existe pas)
client.command('''
CREATE TABLE IF NOT EXISTS solar_data (
    Date DateTime,
    Speed Nullable(Float32),
    Density Nullable(Float32),
    Bt Nullable(Float32),
    Bz Nullable(Float32),
    Mag Nullable(Float32)
) ENGINE = MergeTree()
ORDER BY Date;
''')

# Fonction pour lire et insérer les données d'un fichier CSV dans la base ClickHouse
def insert_data_from_csv(csv_file, mag_csv_file):
    # Lecture du fichier principal (avec Speed, Density, etc.)
    df = pd.read_csv(csv_file, sep=';', parse_dates=['Date'],
                     dtype={'Speed': 'float32', 'Density': 'float32', 'Bt': 'float32', 'Bz': 'float32'})

    # Lecture du fichier mag
    df_mag = pd.read_csv(mag_csv_file, sep=';', parse_dates=['Date'], dtype={'X': 'float32'})

    # Convertir la colonne 'Date' du fichier mag en format DateTime si nécessaire
    df_mag['Date'] = pd.to_datetime(df_mag['Date'], unit='s', errors='coerce')

    # Remplacer les NaN par None (qui devient NULL dans ClickHouse) pour les deux DataFrames
    df = df.where(pd.notnull(df), None)
    df_mag = df_mag.where(pd.notnull(df_mag), None)

    # Fusionner les deux DataFrames sur la colonne 'Date'
    df_merged = pd.merge(df, df_mag, on='Date', how='left')

    # Convertir les données fusionnées au format attendu par ClickHouse (liste de tuples)
    data = list(df_merged.itertuples(index=False, name=None))

    # Insertion dans ClickHouse avec la nouvelle colonne 'mag'
    client.insert('solar_data', data, column_names=['Date', 'Speed', 'Density', 'Bt', 'Bz', 'Mag'])


# Parcours des dossiers pour chaque année de 2016 à 2024
for year in range(2017, 2024):
    year_start = time.time()
    print(f"Traitement de l'année {year}")
    directory = f'/usr/src/app/data/solarwinds/solarwinds-dscovr-compiled/{year}' # Chemin vers le répertoire de l'année
    mag_directory = f'/usr/src/app/data/mag/mag-kiruna-compiled/{year}' # Chemin vers le répertoire de l'année

    if os.path.exists(directory):
        # Parcours des fichiers dans le répertoire
        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                csv_file = os.path.join(directory, filename)
                mag_csv_file = os.path.join(mag_directory, filename)
                file_start = time.time()
                print(f"Traitement du fichier {csv_file} et {mag_csv_file}")
                insert_data_from_csv(csv_file, mag_csv_file)
                file_end = time.time()
                print(f"Fin du traitement du fichier {csv_file} et {mag_csv_file}, durée : {file_end - file_start} secondes")

    year_end = time.time()
    print(f"Fin du traitement de l'année {year}, durée : {year_end - year_start} secondes")

# Exécuter les requêtes SQL pour mettre à jour les NaN en NULL dans chaque colonne
client.command("ALTER TABLE solar_data UPDATE Speed = NULL WHERE isNaN(Speed);")
client.command("ALTER TABLE solar_data UPDATE Density = NULL WHERE isNaN(Density);")
client.command("ALTER TABLE solar_data UPDATE Bt = NULL WHERE isNaN(Bt);")
client.command("ALTER TABLE solar_data UPDATE Bz = NULL WHERE isNaN(Bz);")

end = time.time()
print("Insertion terminée, durée totale :", end - start, "secondes")