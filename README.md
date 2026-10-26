# Local File Organizer: Yerel ve Gizlilik Odaklı Akıllı Dosya Yöneticisi

[![Python 3.13.6](https://img.shields.io/badge/python-3.13.6-blue.svg)](https://www.python.org/downloads/)
[![Ollama](https://img.shields.io/badge/Ollama-qwen3.5:2b-black.svg)](https://ollama.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Dijital dağınıklıktan yoruldunuz mu? Bilgisayarınızın her köşesine dağılmış yüzlerce dosya arasında aradığınızı bulamıyor musunuz? 

**Local File Organizer**, dosyalarınızı analiz ederek kaynak dosyaları taşımadan veya silmeden, otomatik olarak düzenli ve anlamlı bir klasör hiyerarşisinde **hardlink ile bağlayan**, hafif, hızlı ve **tamamen yerel çalışan (100% On-Device)** bir dosya düzenleme asistanıdır.

Tüm içerik analizi ve akıllı adlandırma işlemleri cihazınızdaki **Ollama** altyapısı ve **`qwen3.5:2b`** modeli ile yerel olarak yürütülür. Hiçbir veriniz internete veya bulut sunucularına aktarılmaz; gizliliğiniz %100 güvence altındadır.

---

## Nasıl Çalışır? 💡

> **Önemli Not:** Dosyalar kaynak dizinden taşınmaz veya silinmez. Organize edilmiş hedef dizinde orijinal dosyaların dosya sistemi kayıtlarına işaret eden hardlink (`os.link`) bağlantıları oluşturulur. Kaynak dosyalarınız olduğu gibi korunur.

### Öncesi: Dağınık Kaynak Dizin
```text
C:\Users\User\Downloads\messy_folder\
├── 1.xlsx
├── 12222_777.docx
├── BS.txt
├── IMG_0967.PNG
├── c8fed35720671596882b0c6a2ad9586d.gif
├── go_bruin.pptx
├── logo.png
├── paper_1col.pdf
├── 1111_63.csv
├── animal.jpg
└── ccc.md

0 alt klasör, 11 dosya
```

### Sonrası: Organize Edilmiş Dizin (İçeriğe Göre - By Content)
```text
C:\Users\User\Downloads\organized_folder\
├── bank_account/
│   └── doc_bs.txt
├── academic_papers/
│   └── doc_paper_1col.pdf
├── spreadsheets/
│   ├── doc_1.xlsx
│   └── doc_1111_63.csv
├── presentations/
│   └── doc_go_bruin.pptx
├── image_files/
│   ├── img_animal.jpg
│   ├── img_logo.png
│   └── img_IMG_0967.PNG
└── doc_files/
    └── doc_12222_777.docx

6 alt klasör, 11 dosya
```

---

## Öne Çıkan Özellikler 🚀

- **100% Yerel Yapay Zekâ:** Harici API anahtarına veya internet bağlantısına gerek yoktur. Yerel **Ollama** servisi (`qwen3.5:2b`) ile çalışır.
- **Sıfır Ek Disk Alanı (Hardlink):** Dosyalar yeniden kopyalanarak diski doldurmaz; aynı fiziksel dosya kaydına işaret eden `hardlink` (`os.link`) bağlantıları oluşturulur.
- **Orijinal Dosya Güvenliği:** Kaynak dosyalar hiçbir zaman silinmez veya taşınmaz; orijinal yerlerinde kalır ve hedef dizinde hardlink ile bağlanır.
- **Çapraz Disk Güvenliği:** Farklı disk sürücüleri arasında (ör. `C:` $\rightarrow$ `D:`) hardlink oluşturulamadığında, disk alanını gereksiz çoğaltmamak için işlem güvenle atlanır (`skipped_cross_device`) ve loglanır.
- **Önizleme Ağacı (Dry-Run Simülasyonu):** Operasyonlar diske yazılmadan önce terminalde simüle edilen dizin ağacı gösterilir; kullanıcı onay vermedikçe hiçbir işlem yapılmaz.
- **Sessiz Mod (Silent Mode):** Terminal çıktısı istemeyen kullanıcılar için tüm işlem adımlarını `operation_log.txt` dosyasına yönlendirme imkânı.

---

## 3 Farklı Düzenleme Modu 🗂️

CLI başlatıldığında ihtiyacınıza uygun üç farklı organizasyon yönteminden birini seçebilirsiniz:

1. **İçeriğe Göre (By Content - AI Destekli):**
   - Metin tabanlı belgelerin içeriğini okur, `qwen3.5:2b` ile özetler ve anlamsal bir klasör adı ile dosya adı türetir.
   - Görseller kural tabanlı olarak hızlıca `image_files/` altında sınıflandırılır.
2. **Tarihe Göre (By Date):**
   - Dosyaların son değiştirilme zaman damgalarını (`mtime`) okuyarak `Yıl/Ay` (örn. `2024/October`) klasör hiyerarşisi oluşturur. Model gerektirmez, anlıktır.
3. **Türe Göre (By Type):**
   - Dosyaları uzantılarına göre kategorilere (`text_files/plain_text_files`, `doc_files`, `pdf_files`, `xls_files`, `image_files`, `others`) ayırır. Model gerektirmez, anlıktır.

---

## Desteklenen Dosya Formatları 📁

- **Metin & Belgeler:** `.txt`, `.docx`, `.pdf`, `.md`
- **Tablolar:** `.xlsx`, `.csv`, `.xls`
- **Sunumlar:** `.pptx`, `.ppt`
- **Görseller:** `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`

---

## Gereksinimler 💻

- **İşletim Sistemi:** Windows, macOS veya Linux
- **Python:** Yalnızca **Python 3.13.6** sürümünde test edilmiş ve doğrulanmıştır. (Python 3.10+ veya 3.12 sürümleri bu geliştirme döngüsünde kodla doğrulanmamıştır, [Belirsiz]).
- **Ollama:** Yerel model çıkarımı için [Ollama](https://ollama.ai) kurulu ve çalışır durumda olmalıdır.

---

## Kurulum ve Başlangıç 🛠️

### 1. Hızlı Başlangıç: Desktop Organizer (GUI) 🖥️
Masaüstünüzdeki dağınık dosyaları tek tıkla kategorilere ayırmak, yerel yapay zekâ (`qwen3.5:2b`) ile içeriklerine göre akıllı konu başlıklarına taşımak ve geri alma kaydı tutmak için:

* **Windows:**
  * Dağıtım arşivindeki `Desktop-Organizer.exe` uygulamasına çift tıklayın.
  * Açılışta dilediğiniz dili (🇹🇷 Türkçe veya 🇬🇧 English) ve temayı (☀️ Açık veya 🌙 Koyu) seçebilirsiniz.
  * **Hızlı Mod** (uzantıya göre anında) veya **Yapay Zekâ Modu** (Ollama `qwen3.5:2b` ile belge içeriğine göre) belirleyin.
  * Masaüstünüz taranır, önizleme tablosunda her dosyanın hedefi gösterilir.
  * **"Taşı"** butonuna basarak dosyalarınızı `Masaüstü\Duzenli` klasörüne güvenle taşıyın.
  * Dilediğiniz zaman **"Son işlemi geri al"** ile tüm dosyaları ilk yerine getirebilirsiniz.
* **Linux (Mint Cinnamon / Ubuntu / Debian):**
  * `bash run_linux.sh` komutunu çalıştırın.
  * Betik eksik sistem bağımlılıklarını (`python3-tk`, `python3-venv` vb.) kontrol edip gerekirse `sudo` yetkisi alarak tamamlar ve kullanıcı oturumunda masaüstü arayüzünü açar.

---

### 2. Gelişmiş Konsol ve Yapay Zekâ Modu (CLI) 🤖
Klasörleri içeriğine göre yapay zekâ (`qwen3.5:2b`), tarih veya dosya türüne göre düzenlemek için terminal üzerinden çalıştırabilirsiniz:

* **Windows / Linux:** `python main.py` veya Linux'ta `bash linux/run_linux.sh --cli` çalıştırın.

---

### 3. Kaynak Koddan Çalıştırma ve Geliştirme
```bash
git clone https://github.com/ihsan896/Local-File-Organizer.git
cd Local-File-Organizer
```

### 2. Sanal Ortamı Hazırlayın
```bash
# Sanal ortam oluşturun
python -m venv venv

# Sanal ortamı aktifleştirin:
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Linux / macOS:
source venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 4. Ollama Servisini ve Modeli Başlatın
Ollama kurulu değilse [ollama.ai](https://ollama.ai) üzerinden yükleyin. Ardından terminalde:
```bash
# Modeli indirin (yalnızca ilk seferde, ~1.3 GB)
ollama pull qwen3.5:2b

# Ollama arka planda çalışmıyorsa başlatın
ollama serve
```

### 5. Uygulamayı Çalıştırın 🎉
```bash
python main.py
```

CLI sizden sırasıyla şu bilgileri isteyecektir:
1. **Sessiz Mod:** `yes` veya `no`
2. **Düzenlenecek Dizin:** Organize etmek istediğiniz kaynak klasörün tam veya göreceli yolu (örn: `sample_data`).
3. **Hedef Dizin:** Organize edilmiş dosyaların oluşturulacağı hedef klasör (Enter'a basarak varsayılan `organized_folder` kullanılabilir).
4. **Mod Seçimi:** `1` (İçerik), `2` (Tarih) veya `3` (Tür).
5. **Onay:** Gösterilen önizleme ağacını onaylıyorsanız `yes`.

---

## Proje Dokümantasyonu 📚

Projenin iç yapısı, mimari kararları ve teknik kısıtları hakkında detaylı belgeler:

- [PROJECT_GUIDE.md](PROJECT_GUIDE.md): Kapsamlı teknik mimari rehberi, fonksiyon açıklamaları ve veri akış şemaları.
- [GOALS.md](GOALS.md): Geliştirme hedefleri, görev listesi ve doğrulama kayıtları.
- [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md): Bilinen teknik ve mimari kısıtlar.
- [NOTICE.md](NOTICE.md): Atıf, telif ve açık kaynak bildirim belgesi.

---

## Atıf ve Referans 🤝

Bu proje, **[Ihsan-AI](https://github.com/ihsan896)** tarafından geliştirilmiş ve özelleştirilmiştir. Projenin orijinal temel kaynağı [QiuYannnn/Local-File-Organizer](https://github.com/QiuYannnn/Local-File-Organizer) deposudur. Orijinal mimarideki Nexa SDK bağımlılıkları kaldırılarak yerel Ollama motoruna geçirilmiş, platform/disk uyumluluğu sağlanmış ve çapraz platform dağıtım paketleri oluşturulmuştur.

---

## Lisans 📄

Bu proje [MIT Lisansı](LICENSE) kapsamında lisanslanmıştır.  
Telif Hakkı (c) 2026 Ihsan-AI (ihsan896). Tüm hakları saklıdır.
Orijinal kod tabanı telif hakkı: Copyright (c) 2024 Yanhao Qiu (MIT Lisansı). Detaylar için [NOTICE.md](NOTICE.md) belgesine bakınız.
