# pages/4_Coğrafi_Analiz.py
import streamlit as st
import utils  # <-- Paylaşılan modülümüz
import plotly.express as px
import pandas as pd

# --- Sayfa Ayarları ---
st.set_page_config(page_title="Coğrafi Analiz", page_icon="🌍")

# --- Veriyi ve Filtreleri Yükle ---
df = utils.load_data()
selected_type, selected_years, df_final_filtered = utils.generate_sidebar_filters(df)

# --- Sayfa Başlığı ---
st.title("🌍 Coğrafi İçerik Analizi")
st.write("Hangi ülkelerin hangi türlerde içerik ürettiğini gösteren interaktif bir analiz.")
st.write(f"Filtreler: **{selected_type}** | Yıl Aralığı: **{selected_years[0]} - {selected_years[1]}**")
st.divider()

# --- PROFESYONEL DOKUNUŞ: Veriyi Hazırlama (Her iki sekme için ortak) ---
if not df_final_filtered.empty:
    df_map_data = df_final_filtered[['country', 'listed_in']].fillna('Bilinmiyor')
    df_map_data = df_map_data.assign(country=df_map_data['country'].str.split(',')).explode('country')
    df_map_data = df_map_data.assign(listed_in=df_map_data['listed_in'].str.split(',')).explode('listed_in')
    df_map_data['country'] = df_map_data['country'].str.strip()
    df_map_data['listed_in'] = df_map_data['listed_in'].str.strip()
    df_map_data = df_map_data[
        (df_map_data['country'] != 'Bilinmiyor') &
        (df_map_data['listed_in'] != 'Bilinmiyor')
    ]
    
    # Treemap için veriyi grupla
    df_grouped = df_map_data.groupby(['country', 'listed_in']).size().reset_index(name='count')
    
    # Sadece en çok içerik üreten ilk 20 ülkeyi al (Her iki sekmede de bunu kullanacağız)
    top_countries_list = df_grouped.groupby('country')['count'].sum().nlargest(20).index
    df_top_countries_grouped = df_grouped[df_grouped['country'].isin(top_countries_list)]

else:
    st.warning("Bu filtreler için veri bulunamadı.")
    df_top_countries_grouped = pd.DataFrame() # Boş dataframe
    top_countries_list = [] # Boş liste

# --- PROFESYONEL DOKUNUŞ: Kullanıcıya Seçim Sunan Sekmeler (Tabs) ---
tab1, tab2 = st.tabs(["📊 İnteraktif Harita (Treemap)", "📈 Detaylı Liste (Top 20 Ülke)"])

# --- SEKME 1: TREEMAP (Görsel Etki) ---
with tab1:
    st.subheader("Ülkelere ve Türlere Göre İçerik Dağılımı")
    
    # PROFESYONEL DOKUNUŞ (Sizin Tespitiniz - P2): Navigasyon Yardım Metni
    st.info("ℹ️ Grafikte bir ülkeye (örn: 'India') tıklayarak o ülkedeki türleri 'yakından' (zoom) görebilirsiniz. \n\n"
            "Geri çıkmak için grafiğin sol üst köşesinde beliren **'Tüm Ülkeler'** yazısına tıklayın.")

    if not df_top_countries_grouped.empty:
        fig = px.treemap(
            df_top_countries_grouped,
            path=[px.Constant("Tüm Ülkeler"), 'country', 'listed_in'], 
            values='count',
            title=f"İçerik Dağılımı: Top 20 Ülke ve Türler",
            color='count',
            color_continuous_scale='YlGnBu' 
        )
        fig.update_traces(hovertemplate='<b>%{label}</b><br>Toplam Adet: %{value}<extra></extra>')
        fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Bu filtreler için Treemap verisi bulunamadı.")

# --- SEKME 2: DETAYLI LİSTE (Okunabilirlik) ---
with tab2:
    st.subheader("İçerik Sayısına Göre İlk 20 Ülke (Filtrelenmiş)")
    
    # PROFESYONEL DOKUNUŞ (Sizin Tespitiniz - P1): Okunabilirlik Çözümü
    if not df_top_countries_grouped.empty:
        # Ülkeleri toplayıp sıralı bir liste yapalım
        country_summary = df_top_countries_grouped.groupby('country')['count'].sum().sort_values(ascending=False).reset_index()
        country_summary = country_summary.rename(columns={'country': 'Ülke', 'count': 'Toplam İçerik Sayısı'})
        
        st.write("Bu görünüm, 'Treemap' üzerindeki verilerin okunabilir, sıralı halidir.")
        
        # Temiz bir tablo olarak göster
        st.dataframe(
            country_summary,
            use_container_width=True,
            hide_index=True # Index (0, 1, 2...) sütununu gizle
        )
    else:
        st.warning("Bu filtreler için liste verisi bulunamadı.")