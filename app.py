import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initialize API
from vipunen_api import VipunenAPI
api = VipunenAPI()

# Streamlit App Layout
st.title("Vipunen Dashboard")

# Sidebar filters
dataset = st.sidebar.selectbox("Select Dataset", [
   "erilliset_opinto_oikeudet", "opiskelijat_ja_tutkinnot",
   "lukio_opiskelijat_vuosi_tutkinto","yo_talous2","avoin_amk","amk_talous",
   "lukio_opiskelijat_kuukausi_maakunta","suorittanut55","harjoittelukoulut","tavoiteajassa_tutkinnon_suorittaneet",
   "henkilosto","amm_perusrahoituksen_kohdennukset","taydennyskoulutukset","opinnaytetyot","amm_rahoitus_opiskelijavuodet",
   "julkaisut","avoin_yliopisto","suoritteet","amk_opintopisteet_kuukausi","opiskelijat_ja_tutkinnot",
   "toimipisteet","amm_opiskelijat_ja_tutkinnot_kuukausi_maakunta","amm_rahoitusperusteet_ja_myonnetty_rahoitus",
   "korkeakoulutus_kv_liikkuvuus","yo_opintopisteet","amk_opintopisteet","koulutusluokitus","yo_talous","amk_talous2",
   "ytl_arvosanat","korkeakoulutus_hakeneet_ja_paikan_vastaanottaneet","alayksikkokoodisto","koulutuksenkustannukset",
   "toimitilat","muu_henkilosto_amk","yamk_tutkinnot","amm_opiskelijat_ja_tutkinnot_vuosi_tutkinto","yo_opintopisteet_kuukausi"
])

years = st.sidebar.multiselect("Statistical Year", options=list(range(2000, 2026)), default=[2020])

universities = [
    "All Universities",
    "Aalto-yliopisto",
    "Helsingin yliopisto",
    "Itä-Suomen yliopisto",
    "Jyväskylän yliopisto",
    "Lapin yliopisto",
    "Lappeenrannan-Lahden teknillinen yliopisto LUT",
    "Oulun yliopisto",
    "Svenska handelshögskolan",
    "Turun yliopisto",
    "Vaasan yliopisto",
    "Åbo Akademi"
]
selected_university = st.sidebar.selectbox("Choose a University", universities)

if st.sidebar.button("Search for information"):
    with st.spinner("🔄 Fetching data... Please wait"):
        all_data = []
        for year in years:
            try:
                filters = f"tilastovuosi=={year}"
                data = api.fetch_data(dataset, filters=filters)

                if not data.empty:
                    data["tilastovuosi"] = year  
                    all_data.append(data)
            
            except Exception as e:
                st.warning(f"⚠️ {year}: Error fetching data: {e}")

        if all_data:
            final_data = pd.concat(all_data, ignore_index=True)

            filter_columns = ["korkeakoulu", "yliopisto", "koulutuksenJarjestaja"]
            matched_column = next((col for col in filter_columns if col in final_data.columns), None)

            if selected_university != "All Universities" and matched_column:
                final_data[matched_column] = final_data[matched_column].str.strip().str.lower()
                filtered_data = final_data[final_data[matched_column] == selected_university.lower()]

                if filtered_data.empty:
                    st.warning(f"⚠️ No results found for '{selected_university}' for years {', '.join(map(str, years))}.")
                else:
                    st.success(f"✅ Retrieved {len(filtered_data)} records for {selected_university}")
                    display_data = filtered_data

            else:
                st.success(f"✅ Retrieved {len(final_data)} records without university-specific filtering.")
                display_data = final_data

            # Display Tables
            st.write(f"### 🔍 Table 1: Interactive DataFrame ({len(display_data)} records)")
            st.dataframe(display_data.head(100))  
            st.write("### 📋 Table 2: Static Table")
            st.table(display_data.head(20))  

            ### 📊 CHARTS SECTION ###
            st.write("## 📊 Data Visualizations")

            import matplotlib.pyplot as plt

           

            # Stacked Bar Chart: Students in Special Programs ("erillisillaOikOpkoulOpLkm") by University
            if "erillisillaOikOpkoulOpLkm" in display_data.columns and "yliopisto" in display_data.columns and "okmOhjauksenAla" in display_data.columns:
                df_stacked = display_data.groupby(["yliopisto", "okmOhjauksenAla"])["erillisillaOikOpkoulOpLkm"].sum().unstack().fillna(0)

                fig, ax = plt.subplots(figsize=(12, 7))
                fig.patch.set_alpha(0)  # Transparent background
                df_stacked.plot(kind="bar", stacked=True, ax=ax, colormap='viridis')
                ax.set_xlabel("University", color='white')
                ax.set_ylabel("Students in Special Programs", color='white')
                ax.set_title("Students in Special Programs by University and Area of Study", color='white')
                ax.tick_params(colors='white')
                ax.spines['bottom'].set_color('white')
                ax.spines['left'].set_color('white')
                ax.legend(title="Field of Study", facecolor='black', edgecolor='white', labelcolor='white', bbox_to_anchor=(1.05, 1), loc='upper left')
                st.pyplot(fig)

            
            # Bar Chart: Number of Students per University
            if "korkeakoulu" in final_data.columns and "opiskelijat" in final_data.columns:
                df_bar_uni = final_data.groupby("korkeakoulu")["opiskelijat"].sum().sort_values(ascending=False)
                fig, ax = plt.subplots(figsize=(12, 6))
                fig.patch.set_alpha(0)
                ax.barh(df_bar_uni.index, df_bar_uni.values, color='skyblue')
                ax.set_xlabel("Number of Students", color='white')
                ax.set_ylabel("University", color='white')
                ax.set_title("Number of Students per University", color='white')
                ax.tick_params(colors='white')
                ax.spines['bottom'].set_color('white')
                ax.spines['left'].set_color('white')
                st.pyplot(fig)

            # Stacked Bar Chart: Students by University and Field of Study
            if "korkeakoulu" in final_data.columns and "koulutusalaTaso1" in final_data.columns and "opiskelijat" in final_data.columns:
                df_stacked_field = final_data.groupby(["korkeakoulu", "koulutusalaTaso1"])["opiskelijat"].sum().unstack().fillna(0)
                fig, ax = plt.subplots(figsize=(12, 7))
                fig.patch.set_alpha(0)
                df_stacked_field.plot(kind="bar", stacked=True, ax=ax, colormap='viridis')
                ax.set_xlabel("University", color='white')
                ax.set_ylabel("Number of Students", color='white')
                ax.set_title("Students by University and Field of Study", color='white')
                ax.tick_params(colors='white')
                ax.spines['bottom'].set_color('white')
                ax.spines['left'].set_color('white')
                ax.legend(title="Field of Study", facecolor='black', edgecolor='white', labelcolor='white', bbox_to_anchor=(1.05, 1), loc='upper left')
                st.pyplot(fig)

            # # Histogram: Number of Degrees Distribution
            # if "tutkinnot" in final_data.columns:
            #     fig, ax = plt.subplots(figsize=(8, 6))
            #     fig.patch.set_alpha(0)
            #     ax.hist(final_data["tutkinnot"], bins=15, color='purple', alpha=0.7, edgecolor='white')
            #     ax.set_xlabel("Number of Degrees", color='white')
            #     ax.set_ylabel("Frequency", color='white')
            #     ax.set_title("Distribution of Number of Degrees", color='white')
            #     ax.tick_params(colors='white')
            #     ax.spines['bottom'].set_color('white')
            #     ax.spines['left'].set_color('white')
            #     st.pyplot(fig)



        else:
            st.warning("⚠️ No data found for the selected filters.")