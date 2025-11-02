# pages/3_Detaylı_Tablo_Keşfi.py
import streamlit as st
import utils
import pandas as pd

# --- Sayfa Ayarları ---
st.set_page_config(page_title="Detaylı Tablo Keşfi", page_icon="🕵️")

# --- Veriyi ve Filtreleri Yükle ---
df = utils.load_data()
# BU SAYFA İNTERAKTİF, BU YÜZDEN FİLTRELERİ ÇAĞIRIYORUZ
selected_type, selected_years, df_final_filtered = utils.generate_sidebar_filters(df)

# --- Sayfa Başlığı ---
st.title("🕵️ Detaylı Tablo Keşfi")
st.write("Filtrelenmiş veri setinin ham detaylarını buradan inceleyebilir ve filtreleyebilirsiniz.")
st.write(f"Filtreler: **{selected_type}** | Yıl Aralığı: **{selected_years[0]} - {selected_years[1]}**")
st.divider()

# --- PROFESYONEL DOKUNUŞ 1 (Sizin Tespitiniz - P2): Sütun Seçici Düzeltmesi ---
st.subheader("Görmek İstediğiniz Sütunları Seçin")

# Kullanıcıya gösterilecek 'temiz' isimler ve veritabanındaki 'ham' isimler eşleşmesi
COLUMN_MAP = {
    'Başlık': 'title',
    'Tür': 'type',
    'Yönetmen': 'director',
    'Oyuncular': 'cast',
    'Ülke': 'country',
    'Eklendiği Yıl': 'added_year',
    'Yayın Yılı': 'release_year',
    'Reyting': 'rating',
    'Kategoriler': 'listed_in',
    'Açıklama': 'description'
}
# Sadece map'teki 'temiz' isimleri (key'leri) göster
clean_column_names = list(COLUMN_MAP.keys())
default_columns = ['Başlık', 'Tür', 'Yönetmen', 'Yayın Yılı', 'Reyting', 'Kategoriler']

selected_clean_names = st.multiselect(
    "Göstermek için sütunları seçin:",
    options=clean_column_names,
    default=default_columns
)

# PROFESYONEL DOKUNUŞ 2 (Sizin Tespitiniz - P3): Yardım Metni
st.caption("Kaldırdığınız bir sütunu geri eklemek için yukarıdaki seçim kutusunun içine tıklayın.")

# --- Veri Tablosu ---
st.header(f"Filtrelenmiş Veri: {len(df_final_filtered)} Satır")

# Kullanıcının seçtiği 'temiz' isimleri 'ham' isimlere geri çevir
selected_raw_names = [COLUMN_MAP[name] for name in selected_clean_names]

if not df_final_filtered.empty and selected_raw_names:
    df_display = df_final_filtered[selected_raw_names].copy()
    
    # 'Bilinmiyor' ile doldurma (Sizin 'Yönetmen' tespitiniz için)
    df_display = df_display.fillna('Bilinmiyor')
    
    # Sütunları yeniden adlandır (Gösterim için)
    df_display = df_display.rename(columns={v: k for k, v in COLUMN_MAP.items()})
    
    st.dataframe(df_display, use_container_width=True, height=500)
else:
    st.warning('Gösterilecek veri bulunamadı veya hiç sütun seçilmedi.')