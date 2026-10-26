# Bildirim ve Lisans Notu (NOTICE)

## Proje Bilgileri
- **Proje Adı:** Local File Organizer
- **Geliştirici / Yazar:** Ihsan-AI (https://github.com/ihsan896)
- **Orijinal Proje:** Local File Organizer
- **Orijinal Yazar:** QiuYannnn
- **Kaynak Depo:** https://github.com/QiuYannnn/Local-File-Organizer
- **Dağıtım Lisansı:** MIT License

---

## Telif Hakkı Bildirimi

```text
Copyright (c) 2026 Ihsan-AI (ihsan896). Tüm hakları saklıdır.
Yalnızca bu sürümde yapılan özelleştirmeler, eklemeler ve değişiklikler için geçerlidir.

Orijinal Kod Tabanı Telif Hakkı:
Copyright (c) 2024 Yanhao Qiu
```

---

## Proje Durumu ve Fork Notu

Bu proje, orijinal `QiuYannnn/Local-File-Organizer` deposunun bağımsız bir fork'u olarak yapılandırılmıştır ve kullanıcı odaklı yeni yeteneklerle geliştirilerek ayrı bir açık kaynak depo formatında yayınlanmaktadır.

### Başlıca Değişiklik ve Özelleştirme Alanları (GOALS.md Referanslı)
1. **Model Altyapısı Dönüşümü (T3 Tamamlandı, T4 Kısmen):**
   - Ağır bağımlılıklara sahip Nexa SDK tamamen kaldırıldı; metin işlemede yerel ve hafif **Ollama** (`qwen3.5:2b`) entegre edildi. Görsellerde ise donanım/zaman aşımı kısıtı nedeniyle görsel AI analizi yapılmayıp kural tabanlı fallback kullanıldı (T4 Kısmen).
2. **Bağımlılık Standardizasyonu (T2 Tamamlandı):**
   - `requirements.txt` ile kaynak kod arasındaki eksik ve atıl kütüphane tutarsızlıklarının giderilmesi.
3. **Çapraz Platform ve Disk Güvenliği (T5 Tamamlandı):**
   - Windows, macOS ve Linux uyumluluğu.
   - `os.link` (hardlink) çapraz sürücü sınırlamalarına karşı sessizce kopya oluşturulmayıp işlem atlanır (`skipped_cross_device`) ve loglanır.
4. **Test ve Doğrulama (T6 Kısmen):**
   - Mod 2 (Tarih) ve Mod 3 (Tür) CLI ile test edildi; Mod 1 (AI) yalnızca tek metin dosyası ile test edildi (çoklu dosyalı AI modu uçtan uca test edilmedi).
5. **Dokümantasyon ve Yönetim (T7 Tamamlandı):**
   - Detaylı teknik rehber (`PROJECT_GUIDE.md`), görev planı (`GOALS.md`), bilinen kısıtlar (`KNOWN_LIMITATIONS.md`) ve güncel `README.md` oluşturulması.
6. **Çapraz Platform Paketleme ve Dağıtım (T8 Tamamlandı):**
   - Windows (.exe) ve Linux (.deb ve run_linux.sh) için derleme/paketleme yapıldı; bağımsız dağıtım ZIP arşivi üretildi.
7. **Pencereli Masaüstü Düzenleyici ve Güvenli Taşıma (T9 Tamamlandı):**
   - Doğrudan masaüstünü hedefleyen Tkinter grafik arayüzü (`gui.py`) geliştirildi. Dosyaları sabit uzantılara veya yerel Ollama (`qwen3.5:2b`) içerik çıkarımına göre akıllı konu klasörlerine güvenli biçimde taşıma (geçici `.part`, SHA-256 doğrulama, kaynak silme) ve `LFO_undo` üzerinden tek tıkla geri alma yeteneği eklendi.
8. **Globalizasyon, Tema ve Sadeleştirilmiş Dağıtım (T10 Planlandı):**
   - Çoklu dil (Türkçe / English) ve Açık/Koyu Tema desteği ile Linux için `sudo` yetkisi alıp ortamı kuran ve masaüstünü açan tek taşınabilir kabuk betiği (`run_linux.sh`) ve Windows için tek `.exe` mimarisi.
