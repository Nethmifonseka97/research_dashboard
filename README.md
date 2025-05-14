
# Vipunen Dashboard

**Vipunen Dashboard** is a Streamlit-based data exploration and visualization app that connects to Finland’s official Vipunen educational statistics API. It allows users to interactively query, filter, and visualize higher education data across Finnish universities.

---

##  Features

-  Select from datasets provided by Vipunen.
-  Filter data by statistical year (2000–2025).
-  Filter results by individual Finnish universities or explore all.
-  Visualize trends using:
  - Stacked bar charts (e.g., students by study field)
  - Horizontal bar charts (e.g., number of students per university)
  - Interactive data tables

---

##  Requirements

- Python 3.8+
- Streamlit
- Pandas
- Matplotlib
- Requests

Install dependencies with:

```bash
pip install -r requirements.txt
```


##  How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/vipunen-dashboard.git
   cd vipunen-dashboard
   ```

2. Launch the Streamlit app:
   ```bash
   streamlit run app.py
   ```


---

##  How It Works

- The dashboard uses a custom `VipunenAPI` class to send HTTP requests to the [Vipunen open API](https://vipunen.fi).
- Users select a dataset and apply filters (year, university).
- Data is fetched in paginated requests, then merged and visualized using Matplotlib.
- If applicable, charts display:
  - Number of students by field and institution
  - Special program participants
  - Degree completions (optional)

---

##  Project Structure

```bash
vipunen-dashboard/
├── app.py                # Main Streamlit app
├── vipunen_api.py        # VipunenAPI class for data fetching
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

##  Available Datasets

Includes datasets like:

- `opiskelijat_ja_tutkinnot`
- `yo_talous`
- `avoin_amk`
- `korkeakoulutus_kv_liikkuvuus`
- and many more...

See the full list in the sidebar dropdown of the app.

---

##  Notes

- API queries are subject to availability and may return empty results for unsupported filters.
- University names are standardized for string-matching. Use the full name as presented in the dropdown.
- Some charts may appear only when relevant data columns are present.

---

##  License

This project is released under the MIT License.

---

##  Acknowledgements

- [Vipunen – Finnish Education Statistics](https://vipunen.fi)
- [Streamlit](https://streamlit.io/)
- [Matplotlib](https://matplotlib.org/)
- [Pandas](https://pandas.pydata.org/)
