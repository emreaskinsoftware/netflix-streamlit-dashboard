# utils.py
import streamlit as st
import pandas as pd

# SRP 1: Veri yükleme ve önbelleğe alma
@st.cache_data
def load_data():
    """
    Netflix veri setini yükler, temel temizliği yapar ve önbelleğe alır.
    """
    try:
        df = pd.read_csv('netflix_titles.csv')
        df = df.dropna(subset=['date_added', 'rating'])
        df['date_added'] = pd.to_datetime(df['date_added'].str.strip())
        df['added_year'] = df['date_added'].dt.year
        return df
    except FileNotFoundError:
        return None

# SRP 2: Sadece interaktif sayfalarda çağrılacak olan filtreleme fonksiyonu
def generate_sidebar_filters(df):
    """
    Verilen DataFrame'e göre Streamlit kenar çubuğunda filtreler oluşturur
    ve seçilen değerleri döndürür.
    
    BU FONKSİYON, ANA SAYFADA (GİRİŞ) ÇAĞRILMAYACAKTIR.
    """
    st.sidebar.title('📊 Filtre Paneli')
    st.sidebar.write('Lütfen analiz etmek istediğiniz içerik türünü seçin:')

    # 1. Filtre: İçerik Türü
    type_options = ['Tümü', 'Movie', 'TV Show']
    selected_type = st.sidebar.selectbox('İçerik Türü Seçin:', type_options)

    if selected_type == 'Tümü':
        df_filtered = df
    elif selected_type == 'Movie':
        df_filtered = df[df['type'] == 'Movie']
    else: # 'TV Show'
        df_filtered = df[df['type'] == 'TV Show']

    # 2. Filtre: Yıl Aralığı (Slider)
    try:
        min_year = int(df_filtered['added_year'].min())
        max_year = int(df_filtered['added_year'].max())
        
        selected_years = st.sidebar.slider(
            'İçeriğin Eklendiği Yıl Aralığını Seçin:',
            min_year,
            max_year,
            (min_year, max_year) 
        )

        df_final_filtered = df_filtered[
            (df_filtered['added_year'] >= selected_years[0]) &
            (df_filtered['added_year'] <= selected_years[1])
        ]
    except ValueError:
        # Eğer filtre sonucu hiç veri kalmazsa (örn: hiç film yoksa)
        st.sidebar.error("Seçilen filtre için veri bulunamadı.")
        df_final_filtered = pd.DataFrame(columns=df.columns) # Boş bir dataframe döndür
        selected_years = (0, 0)
    
    return selected_type, selected_years, df_final_filtered