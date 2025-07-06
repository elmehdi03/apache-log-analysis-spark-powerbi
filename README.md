# Log Analysis with Apache Spark, Power BI, and PostgreSQL

## 🚀 Project Overview

This project demonstrates a complete data engineering pipeline for analyzing simulated Apache web server logs. It covers all the stages from raw log parsing to advanced analytics and interactive dashboards.

Designed for production-like environments, the project is modular and can be scaled or integrated with real-time systems.

---

## 🤝 Use Case

Organizations need visibility into their web server traffic:

* Monitor HTTP errors (e.g., 500 Internal Server Errors)
* Identify the most active IP addresses
* Understand peak usage times
* Track the most visited pages

This project simulates such analysis using logs and helps derive actionable insights.

---

## 🛌 Tech Stack

| Tool       | Purpose                        |
| ---------- | ------------------------------ |
| Python     | Scripting & automation         |
| PySpark    | Scalable data processing       |
| Pandas     | Post-processing & CSV export   |
| PostgreSQL | Structured data storage        |
| Power BI   | Interactive data visualization |
| VS Code    | Development environment        |

---

## 📂 Project Structure

```
logs_analysis_project/
├── data/                    # Contains raw logs (web_logs.txt)
├── outputs/                 # Exported CSVs for analysis
├── scripts/                
│   └── analyze_logs.py     # Main Spark pipeline
├── dashboards/             # Power BI PBIX files or screenshots
├── README.md
└── requirements.txt
```

---

## 📊 Key Features

* **Log parsing** with regex and PySpark
* **Feature engineering**: IP, HTTP method, status code, page, date, time
* **Aggregation**: requests per day, per IP, per method
* **Export**: logs and KPIs to CSV and PostgreSQL (UTF-8 encoded)
* **Visuals**:

  * HTTP code distribution
  * Most requested pages
  * Heatmap by hour/day
  * Trend of 500 errors
  * Unique IPs count over time

---

## 🔄 Pipeline Summary

1. **Load** raw Apache logs from text file
2. **Parse** relevant fields using PySpark regex
3. **Clean & enrich** data (timestamp, date parts)
4. **Save** outputs to CSV and database
5. **Visualize** in Power BI with dynamic filters

---

## 📁 Data Sample

```
IP,Timestamp,Method,Page,Code,Date,Year,Month,Week,Day,Hour
214.14.133.23,15/Jun/2025:17:28:36,POST,/products,500,2025-06-15,2025,6,24,15,17
...
```

---

## 📦 Setup Instructions

1. **Install Python and Spark** (Spark 3.4+ and Java 17)
2. `pip install -r requirements.txt` (includes `pyspark`, `pandas`, `psycopg2-binary`)
3. Run the pipeline:

```bash
python scripts/analyze_logs.py
```

4. Launch Power BI and import `outputs/logs_parsed_utf8.csv`
5. \[Optional] Import to PostgreSQL using pgAdmin or programmatically

---

## 🔐 Author

Project built by [El Mehdi EL YOUBI RMICH](https://github.com/elmehdi03) as part of a professional learning journey in data engineering and analytics.

---

## 🌟 Future Enhancements

* Real-time ingestion (Spark Streaming)
* Alerting on spikes of errors (code 500)
* Integration with Apache Kafka or Airflow
* Dockerize the pipeline for portability

---
