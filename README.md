# In-work at-risk-of-poverty in Europe (2005–2024)

**Author:** Candice Mamou  
**Stack:** Streamlit · pandas · matplotlib · plotly · pycountry

> Explore how employment and income inequality interact across Europe. The app visualizes the share of **employed people** whose **disposable income** is **below 60% of their country’s median** (EU-SILC / Eurostat).

##  Objectives / Story arc
- **Hook:** Working full-time doesn’t always protect from poverty.  
- **Context:** EU-SILC indicator “in-work at-risk-of-poverty” (% of employed below 60% median income).  
- **Key questions (tabs):**
  1) What are the main indicators?  
  2) How has in-work poverty evolved over time?  
  3) Countries vs EU average  
  4) Which countries are most/least affected?  
  5) Gender differences  
  6) Which age groups are most at risk?  
  7) Did crises worsen in-work poverty? (bands: 2008, 2020, 2022)  
  8) North–South / East–West divide  
  9) Map of Europe  
  10) Conclusions + “Did you know?” facts

**Takeaways:** Differences persist across regions; crises leave visible footprints; gender/age patterns suggest structural inequalities.

## Data
- **Source:** Eurostat (EU-SILC), open data via data.europa.eu.  
- **File used:** `estat_ilc_iw01_en.csv` (local path in the code).  
- **Granularity:** Annual; by country (`geo`), sex (`M/F/T`), age group (`TOTAL`, `Y18-24`, `Y25-54`, `Y55-64`).  
- **Unit:** Percent.  
- **License:** Open data license as provided by Eurostat (cite in app footer/caption).

## Features implemented (per brief)
- Sidebar **filters** (country, sex, age group, year).  
- **KPIs** header (EU vs country in selected year).  
- ≥ **3 interactive visuals** (time series, bar rankings, map).  
- **Map** (Plotly choropleth) with ISO3 conversion via `pycountry`.  
- **Data quality**: compact missingness view + column dictionary.  
- **Narrative structure** with **clickable tabs** (acts as a summary/TOC).  
- **Caching** with `@st.cache_data`.  
- **Annotations**: crisis bands.  
- **Fun facts** box in the conclusion.  
> Packaging items to complete for submission: short **demo video (2–4 min)**, and a **zip** containing dataset link, README, and code, per the assignment.

## Project structure (single-file app)
```
app.py                # your Streamlit script (code in the prompt)
requirements.txt
README.md
data/                 # (optional) place CSV here or update the path in app.py
```

## How to run locally
1. **Clone** or unzip the project.
2. (Recommended) Create a virtual env:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # on Windows: .venv\Scripts\activate
   ```
3. **Install deps**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Place the CSV** (or update the path in `app.py`):
   - Current path in code:  
     `C:\Users\Candice\Documents\projetDATAVIZ\estat_ilc_iw01_en.csv`
   - Tip: move the file to `./data/estat_ilc_iw01_en.csv` and update `path` accordingly.
5. **Run**:
   ```bash
   streamlit run app.py
   ```

## Data preparation (what the app does)
- Lower-cases and normalizes column names, drops EU aggregates (EA, EU, EFTA).  
- Fills `obs_value` missing values with series median (light imputation).  
- Converts `time_period` → `year`.  
- Keeps **valid ages** only; maps to friendly labels.  
- Drops unused metadata columns.  
- Maps `geo` codes to **country names** and **ISO3** (for the map).  
- Filters out countries with **<5 years** of data (stability).  

## Known limitations / caveats
- Imputing `obs_value` by median is conservative but may slightly bias variance.  
- “EU average” is computed as a **simple mean across available countries** (not population-weighted).  
- Regional buckets (North/West/South/East) are a **manual mapping** for storytelling; definitions can vary.  
- Some countries/years may be missing; results reflect available data.

## Submission checklist (course)
- [ ] Upload **URL** to deployed app (optional).  
- [x] Interactive **Streamlit app** with narrative & filters.  
- [ ] **Demo video (2–4 min)** walking through the tabs/story.  
- [ ] Zip with **dataset/link, README, Python code** (and requirements).  
- [ ] File naming per brief.

## Visual style & accessibility
- Clear titles, labeled axes/units, legend titles (“Sex”, etc.).  
- Neutral color palettes; gridlines and annotations for readability.  
- Screen-reader friendly text (section headings reflect the narrative).  

## Credits
- Data: Eurostat EU-SILC (data.europa.eu).  
- Libraries: Streamlit, pandas, matplotlib, plotly, pycountry, missingno, seaborn (for a tiny completeness view).
