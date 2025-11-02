# 1_Giriş_Sayfası.py
import streamlit as st
import utils  # <-- Paylaşılan modülümüzü 'import' ediyoruz
import plotly.express as px

# --- Sayfa Ayarları ---
st.set_page_config(
    page_title="Netflix Analiz Panosu - Giriş",
    page_icon="🎬",
    layout="wide"
)

# --- Sadece Veriyi Yükle (FİLTRE ÇAĞIRMA!) ---
df = utils.load_data()

# --- ANA SAYFA (YÖNETİCİ ÖZETİ) ---
st.title('🎬 Netflix Analiz Panosu: Yönetici Özeti')
st.write("""
Hoş geldiniz! Bu pano, Netflix veri setinin interaktif bir analizidir. 
Bu ana sayfa, tüm veri setine dayalı **filtresiz** genel bir bakış sunmaktadır. 
**Detaylı ve interaktif analizler** için lütfen yandaki menüden ilgili sayfayı seçin.
""")
st.divider()

if df is not None:
    # --- 1. FİLTRESİZ KPI KARTLARI ---
    st.header('Tüm Veri Setine Genel Bakış')
    col1, col2, col3 = st.columns(3)

    total_content = len(df)
    col1.metric(label="Toplam İçerik (Tümü)", value=f"{total_content:,}")

    total_movies = len(df[df['type'] == 'Movie'])
    col2.metric(label="Toplam Film (Tümü)", value=f"{total_movies:,}")

    total_tv = len(df[df['type'] == 'TV Show'])
    col3.metric(label="Toplam Dizi (Tümü)", value=f"{total_tv:,}")
    
    st.divider()

    # --- 2. FİLTRESİZ ANA GRAFİK ---
    st.header('Tüm İçeriklerin Yıllara Göre Büyümesi (Filtresiz)')
    
    # Yıllara göre kümülatif (birikimli) büyümeyi hesapla
    df_cumulative = df.sort_values(by='date_added')
    df_cumulative['content_count'] = 1
    df_cumulative['cumulative_sum'] = df_cumulative['content_count'].cumsum()
    
    # Plotly ile bir "Alan Grafiği" (Area Chart) çiz
    fig = px.area(
        df_cumulative, 
        x='date_added', 
        y='cumulative_sum',
        title='Netflix Platformunun Yıllara Göre Kümülatif Büyümesi',
        labels={'date_added': '<b>Tarih</b>', 'cumulative_sum': '<b>Toplam İçerik Sayısı</b>'}
    )
    fig.update_traces(hovertemplate='Tarih: <b>%{x|%Y-%m-%d}</b><br>Toplam İçerik: <b>%{y}</b><extra></extra>')
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("Veri seti yüklenemedi. 'netflix_titles.csv' dosyasının ana dizinde olduğundan emin olun.")