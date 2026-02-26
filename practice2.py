# ============================================================
# Practice 2 — Running FastAPI via Python Script
# ============================================================
# In this practice you will:
#   1. Import FastAPI AND uvicorn
#   2. Create a FastAPI app instance
#   3. Use the __main__ block to start the server programmatically
#
# To run:
#   python practice2.py
#
# Then open your browser at: http://127.0.0.1:8080
# ============================================================


# TODO: Import the FastAPI class from the fastapi module
from fastapi import FastAPI
import uvicorn



app = FastAPI()
if __name__ == "__main__":
   uvicorn.run(app, host="127.0.0.1", port=8081)

   
