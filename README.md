# 🎬 Netflix Streamlit Analiz Panosu

Bu proje, Netflix içerik veri setini analiz etmek için oluşturulmuş **profesyonel, çok sayfalı (multi-page) interaktif bir web uygulamasıdır.** Proje, "çalışan" bir prototipten öte, "kıdemli" (senior) yazılım geliştirme prensiplerine odaklanılarak inşa edilmiştir.

**Canlı Demo Linki:** https://netflix-app-dashboard-b.streamlit.app/

---

## ✨ Projenin "Profesyonel" Özellikleri

Bu projeyi "basit" bir dashboard'dan ayıran temel mimari kararları:

1.  **Modüler Mimari (SRP & DRY):**
    * Uygulama, "Tek Sorumluluk Prensibi" (SRP) ile tasarlanmıştır. Her `.py` dosyasının tek bir görevi vardır.
    * Veri yükleme ve filtreleme gibi paylaşılan mantıklar, kod tekrarını önlemek (DRY) için `utils.py` modülünde merkezileştirilmiştir.

2.  **Çok Sayfalı (Multi-Page) Tasarım:**
    * Kullanıcı deneyimini (UX) iyileştirmek için Streamlit'in yerleşik `pages/` klasör yapısı kullanılmıştır.
    * Ana sayfa (`1_Giriş_Sayfası.py`) **filtresiz** bir "Yönetici Özeti" sunarken, alt sayfalar ("Yıllık Analiz", "Coğrafi Analiz") **interaktif filtreleme** ve "derinlemesine analiz" (deep-dive) imkanı sunar.

3.  **Özel Görsel Tema (Netflix Dark Mode):**
    * Varsayılan Streamlit teması yerine, `.streamlit/config.toml` dosyası kullanılarak markaya özel (Netflix kırmızısı ve koyu gri) profesyonel bir "dark mode" tema uygulanmıştır.

4.  **Gelişmiş & İnteraktif Grafikler:**
    * "Statik" `matplotlib` grafikleri yerine, "canlı" ve "interaktif" `Plotly` kütüphanesi kullanılmıştır.
    * Grafikler, `px.bar` (çubuk) gibi temellerin yanı sıra, hiyerarşik veriyi göstermek için `px.treemap` (Ağaç Haritası) gibi gelişmiş analitik grafikleri de içerir.

5.  **Kullanıcı Odaklı Arayüz (UI/UX):**
    * `listed_in` gibi ham veritabanı etiketleri, `st.multiselect` içinde "Kategoriler" gibi kullanıcı dostu isimlere dönüştürülmüştür.
    * `st.tabs` (Sekmeler) kullanılarak, "okunabilirlik" (Detaylı Liste) ve "görsel etki" (Treemap) arasında kullanıcıya seçim hakkı tanınmıştır.

## 🚀 Kullanılan Ana Teknolojiler

* **Streamlit:** Web uygulamasını oluşturmak ve sunmak için.
* **Pandas:** Veri yükleme, temizleme, filtreleme ve manipülasyon için.
* **Plotly (Plotly Express):** Tüm interaktif grafikleri (Bar, Treemap, Area) çizdirmek için.

## 🏃‍♂️ Yerel (Local) Kurulum

1.  Bu repoyu klonlayın.
2.  Bir sanal ortam (virtual environment) oluşturun: `python -m venv venv`
3.  Aktive edin: `.\venv\Scripts\activate` (Windows) veya `source venv/bin/activate` (macOS/Linux)
4.  Gereksinimleri kurun: `pip install -r requirements.txt`
5.  Uygulamayı çalıştırın: `streamlit run 1_Giriş_Sayfası.py`
