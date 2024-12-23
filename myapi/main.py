from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
import os

app = FastAPI()

CSV_FILE_PATH = "movies.csv"
def generate_movie_data():
    if os.path.exists(CSV_FILE_PATH):
        return pd.read_csv(CSV_FILE_PATH)
    else:
        raise FileNotFoundError(f"{CSV_FILE_PATH} 파일이 존재하지 않습니다.")

@app.get("/", response_class=HTMLResponse)
async def show_movies():
    try:
        df = generate_movie_data()
        
        table_html = df.to_html(index=False, escape=False, justify="center", border=1)
        html_content = f"""
        <html>
            <head>
                <title>영화 정보</title>
                <style>
                    body {{ font-family: Arial, sans-serif; text-align: center; }}
                    table {{ margin: 0 auto; border-collapse: collapse; width: 80%; }}
                    th, td {{ padding: 10px; border: 1px solid #ddd; text-align: center; }}
                    th {{ background-color: #f4f4f4; }}
                </style>
            </head>
            <body>
                <h1>영화 목록</h1>
                {table_html}
            </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    
    except FileNotFoundError as e:
        return HTMLResponse(content=f"<h1>{e}</h1>", status_code=404)
