# Hedefler ve Görev Listesi: Local File Organizer

Bu doküman, Local File Organizer projesinin özelleştirilmesi, yerel Ollama altyapısına (`qwen3.5:2b`) geçirilmesi, platform uyumluluğunun sağlanması ve bağımsız bir açık kaynak fork olarak GitHub üzerinde yayınlanması sürecindeki hedefleri, sınırları, görev planını ve çalışma kurallarını tanımlar.

---

## 1. Ana Hedef

- **Özelleştirilmiş Yerel Dosya Yöneticisi:** Projeyi Windows, macOS ve Linux üzerinde sorunsuz çalışan; metin işleme ve dosya adlandırma motoru olarak Nexa SDK yerine yerel **Ollama** servisi ve **`qwen3.5:2b`** modelini kullanan hafif ve kararlı bir sürüme dönüştürmek.
- **Açık Kaynak Dağıtım:** Yapılan geliştirmelerin ardından projeyi kullanıcının kendi GitHub hesabında bağımsız bir fork/repo olarak açık kaynak lisansı ve kendi imzasıyla yayınlamak.

---

## 2. Kapsam Dışı (Out of Scope)

Aşağıdaki konular bu geliştirme döngüsünün kapsamı dışındadır:
- Nexa SDK mimarisinin veya C++ kütüphanelerinin yeniden derlenmesi / yazılması.
- README roadmap'inde bahsedilen yeni dosya formatlarının (e-kitap `.epub`/`.mobi`, ses `.mp3`, video `.mp4`) entegrasyonu.
- Docker konteynerizasyonu veya yeni bir grafiksel kullanıcı arayüzü (GUI / WebUI) geliştirilmesi.

---

## 3. Görev Listesi

| ID | Başlık | Açıklama | Etkilenen Dosyalar | Kabul Kriteri | Öncelik | Durum |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: |
| **T1** | Lisans ve Telif Planı | Projeyi kullanıcının kendi imzasıyla açık kaynak yayınlayabilmesi için mevcut `LICENSE` dosyasını analiz etmek, orijinal telif hakkı ile kullanıcının değişikliklerine ait telif hakkını ayıran net bir lisanslama ve `NOTICE.md` planı oluşturmak. | `LICENSE`, `NOTICE.md` | Orijinal telif korunarak kullanıcının imzası ve seçtiği lisans koşulları belgelenir. | Yüksek | Tamamlandı |
| **T2** | Bağımlılık Tutarlılığı | `requirements.txt` ile kodda fiilen import edilen (`nexa`/`ollama`, `Pillow` vb.) kütüphaneler arasındaki tutarsızlıkları gidermek; atıl paketleri (`pytesseract`, `cmake`) temizlemek. | `requirements.txt`, `file_utils.py` | Kodda import edilen tüm paketlerin `requirements.txt` içinde eksiksiz ve sürümleriyle yer alması. | Yüksek | Tamamlandı |
| **T3** | Metin Modeli (Ollama Entegrasyonu) | Nexa SDK tabanlı LLM çıkarım kodlarını kaldırıp, yerel çalışan Ollama API (`qwen3.5:2b`) istemcisine taşımak; özet, dosya adı ve kategori üretimini bu modele uyarlamak. | `main.py`, `text_data_processing.py` | Tek bir test metin dosyasında Ollama `qwen3.5:2b` modelinin başarılı şekilde özet ve ad üretmesi. | Yüksek | Tamamlandı |
| **T4** | Görsel İşleme Stratejisi | `qwen3.5:2b` modelinin görsel yeteneği test edildi; görsel AI analizi yapılmıyor, kural tabanlı fallback kullanılıyor. | `image_data_processing.py`, `main.py` | Model kabiliyetine göre görsel stratejisinin belirlenmesi ve mimari kararın koda yansıtılması. | Orta | Kısmen |
| **T5** | Çapraz Platform ve Disk Uyumu | Windows'a özgü yol ayrımlarını standartlaştırmak; hardlink (`os.link`) başarısız olduğunda (farklı sürücü / WinError 17) sessizce dosya kopyalamak yerine işlemi atlamak (`skipped_cross_device`) ve loglamak. | `data_processing_common.py`, `file_utils.py` | Farklı sürücüler arasında ve farklı işletim sistemlerinde hiçbir dosya kaybı olmadan ve sessiz kopyalama yapmadan operasyonun tamamlanması. | Yüksek | Tamamlandı |
| **T6** | Test ve Doğrulama | Mod 2 ve Mod 3 CLI ile test edildi; Mod 1 yalnızca tek metin dosyası ile test edildi. `sample_data` ve `test_organizer` dosyalarının SHA-256 hash bütünlüğü doğrulandı. | `test_organizer/` | Çıktıların eksiksiz, okunabilir olması ve hiçbir orijinal dosyanın bozulmaması/silinmemesi. | Yüksek | Kısmen |
| **T7** | Dokümantasyon ve Yayın Hazırlığı | `README.md` dosyasını yeni Ollama mimarisine göre baştan sona güncellendi; güncel kurulum rehberi, kısıtlar ve GitHub yayın belgeleri tamamlandı. | `README.md`, `PROJECT_GUIDE.md` | Yeni repo bağlantısı, güncel kurulum rehberi ve değişiklik listesinin hazır olması. | Orta | Tamamlandı |
| **T8** | Çapraz Platform Paketleme ve Dağıtım | Windows (.exe) ve Linux (.deb ve run_linux.sh) için derleme/paketleme yapıldı; requirements.txt, örnek veri ve lisans belgeleriyle birlikte temiz ZIP dağıtım arşivi (release bundle) üretildi. | `release/Local-File-Organizer-v1.0.0.zip` | Windows (.exe), Linux (.deb, .sh), requirements.txt, sample_data, README ve LICENSE içeren temiz ZIP paketinin başarıyla üretilmesi. | Yüksek | Tamamlandı |
| **T9** | Pencereli Masaüstü Düzenleyici (GUI & Yerel AI) | Tkinter tabanlı grafik masaüstü arayüzü (`gui.py`) geliştirildi. Hızlı Mod (uzantı) ve Yapay Zekâ Modu (Ollama `qwen3.5:2b` içerik analizi) eklendi; güvenli taşıma (`.part` + SHA-256 doğrulama) ve 1 tıkla geri alma (`undo_last`, `LFO_undo`) doğrulandı. Tek dosya `Masaustu-Duzenleyici.exe` derlendi. | `gui.py`, `dist/Masaustu-Duzenleyici.exe` | Masaüstü hedefli güvenli taşıma, geri alma ve Ollama yapay zekâ entegrasyonunun uçtan uca test edilmesi. | Yüksek | Tamamlandı |
| **T10** | Globalizasyon, Çift Dil, Tema ve Sadeleştirilmiş Dağıtım | Çoklu dil desteği (Türkçe / English), arayüz üzerinden Açık / Koyu Tema (Light / Dark Mode) geçişi, Linux için `sudo` ile ortamı hazırlayıp masaüstünü açan tek `run_linux.sh` kabuk betiği ve Windows için tek `.exe` içeren sade dağıtım arşivi. | `gui.py`, `run_linux.sh`, `release/Local-File-Organizer-v1.0.0.zip`, `*.md` | Çoklu dil (TR/EN), açık/koyu tema, Linux tek kabuk betiği ve Windows tek .exe mimarisinin eksiksiz doğrulanması. | Yüksek | Planlandı |

---

## 4. Çalışma Kuralları

1. **Tek Seferde Tek Görev:** Her aşamada yalnızca belirlenen bir görev uygulanır; kullanıcı onayı alınmadan diğer göreve geçilmez.
2. **3 Hata Kuralı:** Aynı komut veya işlem üst üste 3 kez başarısız olursa durulur; hata detayları, denenmiş adımlar ve çözüm seçenekleri kullanıcıya raporlanıp yönlendirme istenir.
3. **Tekrarlayan Durum Mesajı Yasağı:** "Bekleniyor", "İşleniyor" gibi gereksiz durum tekrarları yapılmaz. Uzun sürecek işlemlerde tahmini süre bir kez belirtilir, ardından sonuç bildirilir.
4. **Model Çalıştırma Öncesi Onay:** Ağır model çalıştırma (`ollama run`, model indirme, tüm veri seti üzerinde toplu işlem) adımları öncesinde kullanıcıdan açık onay istenir.
5. **Yedek Alma Zorunluluğu:** Değiştirilecek veya güncellenecek her dosyanın işlem öncesinde `.bak` uzantılı bir kopyası oluşturulur.
6. **Kritik Dizin Koruma Kuralı:** Kullanıcının Masaüstü (ana masaüstü dosyaları), Belgeler ve OneDrive klasörlerine kesinlikle dokunulmaz; yalnızca bu projenin çalışma dizini içinde kalınır.

---

## 5. Rapor Formatı (Her Görev Sonunda)

Tamamlanan her görevin ardından kullanıcıya aşağıdaki standart format ile durum raporu sunulur:

```markdown
### Görev Tamamlama Raporu: [GÖREV_ID]
- **Görev Durumu:** Tamamlandı / Başarısız
- **Değiştirilen Dosyalar:**
  - `dosya_adi.ext` (Yedek: `dosya_adi.ext.bak`)
- **Doğrulama Yöntemi ve Çıktısı:** [Çalıştırılan test ve elde edilen sonuç]
- **Açık Kalan Sorunlar / Notlar:** [Varsa kalan pürüzler veya bir sonraki adıma devreden maddeler]
```
