# Data Engineering Zoomcamp Project

This project ingests NYC Yellow Taxi data into a PostgreSQL database.

## Setup Instructions

1. Start the PostgreSQL database using Docker:
   `docker run -it -e POSTGRES_USER="root" -e POSTGRES_PASSWORD="root" -e POSTGRES_DB="ny_taxi" -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data -p 5432:5432 postgres:13`

2. Start Jupyter Notebook:
   `uv run jupyter notebook`

3. Run the notebook `Untitled.ipynb` to ingest the data.

## Technologies Used
- Python, Pandas, SQLAlchemy
- PostgreSQL
- Docker
- uv
