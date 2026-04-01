#!/bin/bash
# start.sh
# Set PYTHON path to the application directory to allow imports
export PYTHONPATH=.

echo "Initializing database..."
python scripts/init_db.py

echo "Seeding incident data..."
python scripts/seed_incidents.py

echo "Seeding log data..."
python scripts/seed_logs.py

# Optional: seed RAG examples if the file exists
if [ -f "scripts/seed_rag_examples.py" ]; then
    echo "Seeding RAG examples..."
    python scripts/seed_rag_examples.py
fi

echo "Starting backend agent runner..."
python app/runner.py &

echo "Starting Streamlit UI..."
streamlit run ui/streamlit_app.py --server.port=8501 --server.address=0.0.0.0
