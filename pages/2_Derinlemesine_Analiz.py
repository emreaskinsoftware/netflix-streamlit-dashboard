# pages/2_Yıllık_Analiz.py
import streamlit as st
import plotly.express as px
import utils  # <-- Paylaşılan modülümüzü 'import' ediyoruz

st.set_page_config(page_title="Yıllık Analiz", page_icon="📈")

# --- Veriyi ve Filtreleri Yükle (DRY Prensibi) ---
df = utils.load_data()
selected_type, selected_years, df_final_filtered = utils.generate_sidebar_filters(df)

# --- Sayfa Başlığı ---
st.title("📈 Yıllık ve Tür Bazlı Analizler")
st.write(f"Filtreler: **{selected_type}** | Yıl Aralığı: **{selected_years[0]} - {selected_years[1]}**")
st.divider()

# --- Grafikler ---
gcol1, gcol2 = st.columns(2)

with gcol1:
    st.subheader('Yıllara Göre Eklenen İçerik')
    if not df_final_filtered.empty:
        yearly_counts = df_final_filtered['added_year'].value_counts().sort_index()
        fig1 = px.bar(
            yearly_counts, x=yearly_counts.index, y=yearly_counts.values,
            title=f"'{selected_type}' Türündeki İçeriklerin Dağılımı",
            labels={'x': '<b>Yıl</b>', 'y': '<b>Toplam Adet</b>'}
        )
        fig1.update_traces(hovertemplate='Yıl: <b>%{x}</b><br>Adet: <b>%{y}</b><extra></extra>')
        fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.warning('Veri yok.')

with gcol2:
    st.subheader(f"En Popüler 10 Tür ({selected_type})")
    if not df_final_filtered.empty and 'listed_in' in df_final_filtered:
        top_10_genres = df_final_filtered['listed_in'].str.split(',') \
                        .explode().str.strip().value_counts().head(10).sort_values(ascending=True)
        fig2 = px.bar(
            top_10_genres, x=top_10_genres.values, y=top_10_genres.index, orientation='h',
            title=f"En Popüler 10 Tür",
            labels={'x': '<b>Toplam Adet</b>', 'y': '<b>Tür (Genre)</b>'}
        )
        fig2.update_traces(hovertemplate='Tür: <b>%{y}</b><br>Adet: <b>%{x}</b><extra></extra>')
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning('Veri yok.')