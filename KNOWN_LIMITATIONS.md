# Bilinen Kısıtlar ve Teknik Özellikler (Known Limitations)

Bu doküman, Local File Organizer projesinin mevcut sürümündeki mimari, teknik ve işlevsel kısıtları açıklar:

---

### 1. Konsol / Terminal Sürümü (`main.py`)
- **Taşıma Davranışı:** Dosyalar taşınmaz veya silinmez. Orijinal dosyalar yerinde kalır; organize edilen hedef dizinde hardlink (`os.link`) bağlantıları oluşturulur.
- **Çapraz Sürücü Sınırı:** Farklı disk sürücüleri arasında (ör. `C:` $\rightarrow$ `D:`) hardlink oluşturulamaz. Bu dosyalar sessizce kopyalanmak yerine atlanır (`skipped_cross_device`) ve log dosyasına yazılır (terminalde gösterilmez).
- **Test Kapsamı:** Mod 2 (Tarih) ve Mod 3 (Tür) CLI üzerinde test edilmiştir. Mod 1 (AI) tek dosya üzerinde test edilmiştir; çoklu dosyalı AI modu uçtan uca CLI akışında yüksek zaman alabilir.
- **NLTK Bağımlılığı:** İlk çalıştırmada NLTK dil paketleri (`punkt`, `stopwords`, `wordnet`) internetten otomatik olarak indirilir.

---

### 2. Pencereli Masaüstü Düzenleyici (`gui.py` / `Masaustu-Duzenleyici.exe`)
- **Güvenli Taşıma (Safe Move):** CLI'dan farklı olarak dosyalar hedef klasöre gerçekten taşınır (move edilir). Taşıma işlemi geçici `.<ad>.part` dosyası oluşturma, boyut ve SHA-256 sağlama toplamı eşleşmesi doğrulandıktan sonra `os.replace` ve kaynak dosya silme adımlarıyla güvenle yürütülür.
- **Geri Alma (Undo) Desteği:** Her başarılı taşıma oturumu `LFO_undo/islem_<zaman>.json` dosyasına kaydedilir. Kullanıcı "Son işlemi geri al" düğmesine bastığında dosyalar SHA-256 doğrulaması yapılarak kaynak konumlarına eksiksiz geri taşınır.
- **Klasör Koruması:** Yalnızca kaynak klasörün doğrudan içindeki dosyalar taranır ve taşınır. Alt klasörlere girilmez ve alt klasörler taşınmaz.
- **Filtrelenen / Atlanan Öğeler:**
  - Gizli ve sistem dosyaları (örn. `desktop.ini`, `thumbs.db`, `.*`) atlanır.
  - Yasaklı uzantılar (`.lnk`, `.url`, `.exe`, `.msi`, `.bat`, `.cmd`, `.ps1`, `.ini`, `.sys`) güvenlik gerekçesiyle atlanır.

---

### 3. Yapay Zekâ (Ollama `qwen3.5:2b`) Çıkarım Kısıtları
- **Görsel Dosyaları:** `qwen3.5:2b` modelinin görsel analizi 120 saniyelik zaman aşımına uğradığı için görseller içerik analizi yapılmadan dosya uzantısına göre (`Resim`) kural tabanlı olarak kategorize edilir.
- **İşlem Süresi:** Yerel model çıkarımı CPU/GPU donanımına bağlı olarak metin/belge başına ortalama 15-40 saniye sürer. Masaüstünde çok sayıda belge varsa analiz süresi uzayabilir.
- **Servis Bağımlılığı ve Geri Dönüş (Fallback):** Yerel Ollama servisi (`ollama serve`) veya `qwen3.5:2b` modeli bulunamadığında uygulama çökmez; kullanıcıyı uyararak anında Hızlı Mod'a (uzantı tabanlı) döner.
- **Boş veya Okunamayan Belgeler:** Şifreli, boş veya 10 karakterden az metin barındıran belgeler otomatik olarak uzantı bazlı genel klasörlere (`PDF`, `Belge`, `Metin`) yönlendirilir.
