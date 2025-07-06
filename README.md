# 🔍 Web Logs Analytics & Visualization with Power BI & PostgreSQL

Ce projet propose une chaîne complète de traitement et de visualisation de logs web. Il s'articule autour de trois axes : parsing via PySpark, stockage structuré dans PostgreSQL, et dashboard interactif sous Power BI.

## 📁 Structure du projet

```
├── analyze_logs.py            # Script principal : parsing, export CSV
├── web_logs.txt               # Fichier brut de logs Apache
├── web_logs_postgreSQL        # Fichier brut de logs Apache
├── Logs_Visuals.pbix          # Fichier Power BI connecté à PostgreSQL
├── requirements.txt           # Dépendances Python
├── LICENSE
└── README.md
```

## 🔄 Pipeline de traitement

1. **Parsing** du fichier `web_logs.txt` avec PySpark  
2. **Export CSV** encodé UTF-8 pour compatibilité avec PostgreSQL  
3. **Import dans PostgreSQL** (table `logs_web`)  
4. **Connexion directe Power BI ↔ PostgreSQL**  
5. **Visualisation** dynamique (codes HTTP, heatmaps, top pages…)

## 🧠 Contenu de la table PostgreSQL

```sql
CREATE TABLE logs_web (
  ip TEXT,
  timestamp TEXT,
  method TEXT,
  page TEXT,
  code INTEGER,
  date DATE,
  source TEXT DEFAULT 'from_postgres'
);
```

## 📊 Visuels Power BI inclus

- ✅ Répartition des codes HTTP  
- 🌍 Top pages consultées  
- 🧠 IPs les plus actives  
- 🕒 Heatmap (heure vs jour)  
- 📉 Évolution temporelle des erreurs 500  
- 🧮 KPI : nombre total de requêtes, pages uniques, IPs uniques

## 🚀 Instructions d’utilisation

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Lancer le script de parsing/export

```bash
python analyze_logs.py
```

Ce script :
- nettoie et transforme les logs
- exporte les données dans `outputs/logs_parsed_utf8.csv`

### 3. Importer dans PostgreSQL

Dans pgAdmin ou en ligne de commande :

```sql
\COPY logs_web FROM 'chemin_absolu/outputs/logs_parsed_utf8.csv' DELIMITER ',' CSV HEADER;
```

### 4. Ouvrir Power BI

- Lancer `Logs_Visuals.pbix`
- Rafraîchir la connexion (PostgreSQL requis en local)

## 🧪 Export PostgreSQL (optionnel)

```sql
\COPY logs_web TO 'outputs/logs_from_postgres.csv' DELIMITER ',' CSV HEADER;
```

## ⚠️ Distinction fichiers

- `logs_parsed_utf8.csv` → Fichier généré par Spark
- `logs_from_postgres.csv` → Fichier exporté depuis PostgreSQL

## 🛠️ Commandes PostgreSQL utiles

```sql
ALTER TABLE logs_web ADD COLUMN source TEXT DEFAULT 'from_postgres';
UPDATE logs_web SET source = 'from_postgres' WHERE source IS NULL;
```

## 📌 À venir

- [ ] Connexion directe Spark → PostgreSQL  
- [ ] Cron pour automatiser l’ETL  
- [ ] Power BI Service pour rafraîchissement auto

## 📜 Licence

MIT License – libre d’utilisation et de modification.

## 🤝 Contributions

Pull requests bienvenues. Projet adapté aux étudiants en data/BI et aux ingénieurs en montée de compétence.
