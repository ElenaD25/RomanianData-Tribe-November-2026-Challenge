# THE BLACK FRIDAY EDIT — Python web app

A magazine-style, browser-based data story built with Streamlit and Plotly.

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create and activate a virtual environment (recommended).
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the app:

   ```bash
   streamlit run app.py
   ```

The app opens in your browser, usually at `http://localhost:8501`.

## Publish it online

The project is ready for deployment to Streamlit Community Cloud:

1. Create a GitHub repository.
2. Upload `app.py`, `requirements.txt`, the `.streamlit` folder and `Black_Friday_Trends_in_Romania.csv`.
3. Sign in to Streamlit Community Cloud using GitHub.
4. Create an app, select the repository, branch, and `app.py`.
5. Deploy. Streamlit will provide a public URL.

The public URL is created by the hosting service; it is not created by running the project locally.

## Project contents

- `app.py` — Streamlit application and magazine navigation.
- `Black_Friday_Trends_in_Romania.csv` — original supplied dataset.
- `requirements.txt` — Python dependencies.
- `.streamlit/config.toml` — light theme in the brand palette (keep this folder when deploying).

## Data handling notes

- Values are loaded directly from the supplied CSV.
- The app keeps units and metrics separate rather than aggregating unlike measures.
- Every page opens with a KPI strip; each chart sits beside a short written description that carries the narrative.
- NETOPIA payment indicators are presented separately from MKOR survey indicators.
- Some metrics only exist for one year; the app does not invent historical values.

## Page preview thumbnails
The hover thumbnails on the previous/next buttons are static images in `previews/`. After changing page content, regenerate them with `python tools/make_previews.py http://localhost:8501` while the app is running (needs `pip install playwright pillow` and `playwright install chromium`).
