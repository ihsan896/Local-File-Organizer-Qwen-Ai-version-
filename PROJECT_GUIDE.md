# Proje Kılavuzu: Local File Organizer

Bu belge, **Local File Organizer** projesinin mimarisini, dosya yapısını, veri akışını, bağımlılıklarını ve kısıtlarını kaynak koda dayalı olarak açıklayan kapsamlı teknik referans rehberidir.

---

## 1. Genel Bakış

**Local File Organizer**, kullanıcının yerel cihazındaki dağınık dosyaları analiz ederek düzenli bir klasör hiyerarşisine yerleştiren, açık kaynaklı ve gizlilik odaklı bir dosya düzenleme aracıdır.

- **Giriş Noktası:** Projenin ana yürütme noktası `main.py` dosyasıdır.
- **Gizlilik İlkesi:** Dosyalar bulut API'lerine (OpenAI, Anthropic vb.) gönderilmez. İçerik analizi yerel çalışan modeller (Nexa SDK / GGUF) üzerinden gerçekleştirilir.
- **Sıralama Modları:** Sistem kullanıcıya üç farklı organizasyon yöntemi sunar:
  1. **İçeriğe Göre (By Content):** Metin dosyaları için dil modeli (LLM), görseller için görsel-dil modeli (VLM) kullanarak dosyanın anlamsal özetini çıkarır; bu özet üzerinden anlamlı bir dosya adı ve kategori klasörü türetir.
  2. **Tarihe Göre (By Date):** Dosyaların son değiştirilme zaman damgasını (`mtime`) okuyarak `Yıl/Ay` (örneğin: `2024/October`) klasör yapısı oluşturur. Yapay zekâ çıkarımı gerektirmez, kural tabanlıdır.
  3. **Türe Göre (By Type):** Dosyaları uzantılarına göre `image_files` ve `text_files` ana dizinleri altında `plain_text_files`, `doc_files`, `pdf_files`, `xls_files`, `ebooks`, `others` şeklinde alt dizinlere yerleştirir. Yapay zekâ çıkarımı gerektirmez.

---

## 2. Dizin Yapısı

Proje kök dizinindeki (`./`) tüm bileşenler, dosya türleri ve işlevleri aşağıda listelenmiştir.

### 2.1 Dosya ve Klasör Tablosu

| Ad | Tür | İşlev |
| :--- | :--- | :--- |
| `main.py` | Kaynak kod | Ana CLI giriş noktası; kullanıcı etkileşimi, mod seçimi, model başlatma ve operasyon onay akışını yönetir. |
| `gui.py` | Kaynak kod | Pencereli Masaüstü Düzenleyici grafik arayüzü (Tkinter); Hızlı Mod ve Yapay Zekâ Modu (Ollama `qwen3.5:2b`), güvenli taşıma ve 1 tıkla geri alma (`undo_last`) motoru. |
| `file_utils.py` | Kaynak kod | Dosya sistemini tarama, dizin ağacını yazdırma, farklı formatlardaki metinleri okuma ve dosya türü ayrıştırma fonksiyonları. |
| `data_processing_common.py` | Kaynak kod | İsim temizleme (`sanitize_filename`), tarihe/türe göre operasyon hesaplama ve disk üzerinde hardlink/symlink yürütme. |
| `text_data_processing.py` | Kaynak kod | Metin dosyalarını LLM ile özetleme, dosya adı ve kategori türetme, NLTK tabanlı metin temizleme işlevleri. |
| `image_data_processing.py` | Kaynak kod | Görselleri VLM ile betimleme, LLM ile dosya adı ve kategori türetme, NLTK tabanlı metin temizleme işlevleri. |
| `output_filter.py` | Kaynak kod | Model yükleme esnasında kütüphanelerin konsola bastığı gürültülü logları bastırmak için `contextmanager`. |
| `requirements.txt` | Yapılandırma | Projenin ihtiyaç duyduğu harici Python paketlerinin listesi. |
| `.gitignore` | Sürüm kontrolü | Git tarafından takip edilmeyecek önbellek, sanal ortam ve geçici log dosyalarını tanımlar. |
| `LICENSE` | Lisans | MIT Lisansı metni (Telif Hakkı 2026 İhsan / İhsanAi). |
| `NOTICE.md` | Dokümantasyon / Lisans | Telif, fork ve değişiklik bildirim belgesi. |
| `README.md` | Dokümantasyon | Projenin genel tanıtımı, kurulum adımları ve kullanım talimatları. |
| `PROJECT_GUIDE.md` | Dokümantasyon | Proje teknik referans kılavuzu. |
| `GOALS.md` | Dokümantasyon | Geliştirme hedefleri ve görev listesi. |
| `main.py.bak` | Yedek (.bak) | `main.py` dosyasının yedek kopyası. |
| `file_utils.py.bak` | Yedek (.bak) | `file_utils.py` dosyasının yedek kopyası. |
| `text_data_processing.py.bak` | Yedek (.bak) | `text_data_processing.py` dosyasının yedek kopyası. |
| `image_data_processing.py.bak` | Yedek (.bak) | `image_data_processing.py` dosyasının yedek kopyası. |
| `data_processing_common.py.bak` | Yedek (.bak) | `data_processing_common.py` dosyasının yedek kopyası. |
| `requirements.txt.bak` | Yedek (.bak) | `requirements.txt` dosyasının yedek kopyası. |
| `LICENSE.bak` | Yedek (.bak) | Orijinal `LICENSE` dosyasının yedek kopyası. |
| `sample_data/` | Veri/örnek | Test amaçlı örnek veri seti (Word, Excel, PDF, PPTX, metin ve resim dosyaları içerir). |
| `test_organizer/` | Test çıktısı / Veri | Düzenleme denemeleri için `sample_data` içeriğinin bir kopyasını barındıran çalışma/test klasörü. |
| `venv/` | Ortam (venv) | Python 3.13.6 tabanlı sanal ortam dizini ve kurulu paketler. |
| `__pycache__/` | Önbellek (__pycache__) | Python derlenmiş bayt kodları (`.pyc` dosyaları). |

### 2.2 Dizin Ağacı Görünümü

```text
.
├── .gitignore
├── LICENSE
├── LICENSE.bak
├── NOTICE.md
├── PROJECT_GUIDE.md
├── GOALS.md
├── README.md
├── requirements.txt
├── requirements.txt.bak
├── main.py
├── main.py.bak
├── file_utils.py
├── file_utils.py.bak
├── data_processing_common.py
├── text_data_processing.py
├── text_data_processing.py.bak
├── image_data_processing.py
├── image_data_processing.py.bak
├── output_filter.py
├── sample_data/
│   ├── 1.xlsx
│   ├── 12222_777.docx
│   ├── c8fed3572067159746e4b47eb2be7046.png
│   ├── go_bruin.pptx
│   ├── IMG_0967.PNG
│   ├── logo.png
│   ├── paper_1col.pdf
│   ├── sub_dir1/
│   │   ├── 1111_666.docx
│   │   └── animal.png
│   ├── sub_dir2/
│   │   └── BS.txt
│   └── text_files/
│       └── ccc.md
├── test_organizer/
│   └── [sample_data yapısının test kopyası]
├── venv/
│   └── [Python 3.13.6 sanal ortam dosyaları]
└── __pycache__/
    └── [Derlenmiş .pyc dosyaları]
```

---

## 3. Modül Bazında Teknik Detay

### 3.1 `main.py`
- **Sorumluluk:** Uygulamanın orkestrasyon merkezidir. NLTK veri kontrolünü yapar, kullanıcıdan yolları ve modu alır, modelleri başlatır, dizin ağacı simülasyonunu ekrana basar ve onay durumunda dosya işlemlerini tetikler.
- **Ana Fonksiyonlar:**
  - `ensure_nltk_data() -> None`: NLTK'nın `stopwords`, `punkt` ve `wordnet` veri paketlerini sessizce indirir.
  - `initialize_models() -> None`: `text_inference` (`qwen3.5:2b` via Ollama) modelini başlatır.
  - `simulate_directory_tree(operations: list, base_path: str) -> dict`: Gerçekleştirilecek operasyonlar için iç içe sözlük yapısında dizin ağacı oluşturur.
  - `print_simulated_tree(tree: dict, prefix: str = '') -> None`: Simüle edilmiş ağacı konsola hiyerarşik formatta yazdırır.
  - `get_yes_no(prompt: str) -> bool`: Kullanıcıdan evet/hayır (veya `/exit`) cevabı alır.
  - `get_mode_selection() -> str`: Kullanıcıdan `1` (content), `2` (date), `3` (type) veya `/exit` seçimi alır.
  - `main() -> None`: Ana yürütme döngüsünü koordine eder.
- **Çağırdığı Modüller:** `file_utils`, `data_processing_common`, `text_data_processing`, `image_data_processing`, `output_filter`, `ollama`, `os`, `time`, `nltk`.
- **Kim Tarafından Çağrılır:** Doğrudan kullanıcı tarafından komut satırından çalıştırılır (`python main.py`).

### 3.2 `file_utils.py`
- **Sorumluluk:** Dosya sistemindeki girdileri taramak, dizin ağacını yazdırmak ve farklı formatlardaki dosyaların metin içeriklerini uygun kütüphanelerle okumak.
- **Ana Fonksiyonlar:**
  - `read_text_file(file_path: str) -> str | None`: `.txt` ve `.md` dosyalarından ilk 3.000 karakteri okur.
  - `read_docx_file(file_path: str) -> str | None`: `.docx` paragraflarını birleştirir.
  - `read_pdf_file(file_path: str) -> str | None`: PyMuPDF (`fitz`) ile belgenin ilk 3 sayfasını okur.
  - `read_spreadsheet_file(file_path: str) -> str | None`: Pandas ile CSV veya Excel (`.xls`, `.xlsx`) okur ve metne dönüştürür.
  - `read_ppt_file(file_path: str) -> str | None`: `python-pptx` ile slayt içi metin kutularını okur.
  - `read_file_data(file_path: str) -> str | None`: Uzantıya göre uygun okuma fonksiyonuna yönlendirir.
  - `display_directory_tree(path: str) -> None`: Belirtilen dizin yapısını konsola ağaç olarak yazdırır.
  - `collect_file_paths(base_path: str) -> list[str]`: Gizli dosyalar hariç tüm dosya yollarını toplar.
  - `separate_files_by_type(file_paths: list[str]) -> tuple[list[str], list[str]]`: Dosyaları görsel ve metin tabanlı olarak iki listeye ayırır.
- **Çağırdığı Modüller:** `os`, `re`, `shutil`, `PIL.Image`, `pytesseract`, `fitz` (PyMuPDF), `docx`, `pandas`, `pptx.Presentation`.
- **Kim Tarafından Çağrılır:** `main.py`.

### 3.3 `data_processing_common.py`
- **Sorumluluk:** Dosya isimlerini temizlemek, kural tabanlı sınıflandırmaları (tarih ve tür) hesaplamak ve dosya sistemi operasyonlarını yürütmek.
- **Ana Fonksiyonlar:**
  - `sanitize_filename(name: str, max_length: int = 50, max_words: int = 5) -> str`: Dosya/klasör adından durak kelimeleri ve geçersiz karakterleri temizler, maksimum kelime ve uzunluk sınırına getirir.
  - `process_files_by_date(file_paths: list[str], output_path: str, dry_run: bool = False, silent: bool = False, log_file: str = None) -> list[dict]`: Dosyaları `os.path.getmtime` ile Yıl/Ay klasörlerine eşler.
  - `process_files_by_type(file_paths: list[str], output_path: str, dry_run: bool = False, silent: bool = False, log_file: str = None) -> list[dict]`: Dosyaları uzantılarına göre ilgili klasörlere eşler.
  - `compute_operations(data_list: list[dict], new_path: str, renamed_files: set, processed_files: set) -> list[dict]`: AI çıktılarından oluşan meta verileri dosya yolu operasyonlarına dönüştürür ve mükerrer isimleri `_1`, `_2` ile çözer.
  - `execute_operations(operations: list[dict], dry_run: bool = False, silent: bool = False, log_file: str = None) -> None`: Operasyon listesini `os.link` (hardlink) veya `os.symlink` ile diske yansıtır.
- **Çağırdığı Modüller:** `os`, `re`, `datetime`, `rich.progress`.
- **Kim Tarafından Çağrılır:** `main.py`, `text_data_processing.py`, `image_data_processing.py`.

### 3.4 `text_data_processing.py`
- **Sorumluluk:** Metin tabanlı içeriklerin Ollama LLM (`qwen3.5:2b`) ile özetlenmesi, dosya ve kategori adlarının türetilmesi ve NLP süzgecinden geçirilmesi.
- **Ana Sınıflar ve Fonksiyonlar:**
  - `class OllamaTextInference(model_name="qwen3.5:2b", host=None)`: Ollama istemcisini sarmalar ve `create_completion(prompt, temperature=0.3)` arayüzü sunar (`think=False` ile hızlı çıkarım yapar).
  - `summarize_text_content(text: str, text_inference) -> str`: LLM'e metni verip en fazla 150 kelimelik özet üretir.
  - `generate_text_metadata(input_text: str, file_path: str, progress, task_id, text_inference) -> tuple[str, str, str]`: 3 aşamalı (özet -> dosya adı -> klasör adı) meta veri çıkarımını ve NLTK temizliğini yürütür. Model çıktısının boş kalması durumunda `doc_<basename>` güvenli geri dönüşü kullanılır.
  - `process_single_text_file(args: tuple, text_inference, silent: bool = False, log_file: str = None) -> dict`: Tek bir metin dosyasının meta verilerini çıkartır.
  - `process_text_files(text_tuples: list, text_inference, silent: bool = False, log_file: str = None) -> list[dict]`: Metin dosyalarını ardışık döngüyle işler.
- **Çağırdığı Modüller:** `re`, `os`, `time`, `nltk`, `ollama`, `rich.progress`, `data_processing_common.sanitize_filename`.
- **Kim Tarafından Çağrılır:** `main.py`.

### 3.5 `image_data_processing.py`
- **Sorumluluk:** Görsellerin VLM ile açıklanması, bu açıklamadan LLM ile dosya ve klasör isimlerinin türetilmesi.
- **Ana Fonksiyonlar:**
  - `get_text_from_generator(generator) -> str`: Model yanıt jeneratöründen metin akışını toplar.
  - `generate_image_metadata(image_path: str, progress, task_id, image_inference, text_inference) -> tuple[str, str, str]`: VLM betimlemesi ve LLM isim üretimini yönetir.
  - `process_single_image(image_path: str, image_inference, text_inference, silent: bool = False, log_file: str = None) -> dict`: Tek bir görselin analizini yürütür.
  - `process_image_files(image_paths: list[str], image_inference, text_inference, silent: bool = False, log_file: str = None) -> list[dict]`: Görselleri ardışık döngüyle işler.
- **Çağırdığı Modüller:** `re`, `os`, `time`, `nltk`, `rich.progress`, `data_processing_common.sanitize_filename`.
- **Kim Tarafından Çağrılır:** `main.py`.

### 3.6 `output_filter.py`
- **Sorumluluk:** Model yükleme esnasında C++ / GGUF motorunun doğrudan stdout'a bastığı gereksiz logları geçici olarak devre dışı bırakır.
- **Ana Fonksiyonlar:**
  - `filter_specific_output()`: `sys.stdout` nesnesini geçici olarak sahte `DummyFile` nesnesine yönlendiren bir `contextmanager`.
- **Çağırdığı Modüller:** `sys`, `contextlib`.
- **Kim Tarafından Çağrılır:** `main.py`.

### 3.7 Veri Akışı Diyagramı (Metin Tabanlı)

```text
[Girdi Dosyası]
       │
       ▼
[file_utils.py: read_file_data / separate_files_by_type]
       │
       ├────────────────────────────────────────┬───────────────────────────────────────┐
       ▼ (Metin Tabanlı)                        ▼ (Görsel Tabanlı)                      ▼ (Kural Tabanlı)
[text_data_processing.py]               [image_data_processing.py]              [data_processing_common.py]
       │                                        │                                       │
       │ (Metin İçeriği)                        │ (Görsel Yolu)                         │ (Dosya mtime / uzantı)
       ▼                                        ▼                                       ▼
[Llama3.2-3B: Özetleme]                 [LLaVA-v1.6: Betimleme]                 [Tarih / Tür Eşleme]
       │                                        │                                       │
       ▼                                        ▼                                       │
[Llama3.2-3B: Dosya Adı Üretimi]        [Llama3.2-3B: Dosya Adı Üretimi]                │
       │                                        │                                       │
       ▼                                        ▼                                       │
[Llama3.2-3B: Kategori Adı Üretimi]     [Llama3.2-3B: Kategori Adı Üretimi]             │
       │                                        │                                       │
       ▼                                        ▼                                       │
[NLTK & sanitize_filename Temizliği]    [NLTK & sanitize_filename Temizliği]            │
       │                                        │                                       │
       └────────────────────────────────────────┴───────────────────────────────────────┘
                                                │
                                                ▼
                             [data_processing_common.py: compute_operations]
                             (Hedef yol ve çakışma kontrolü: _1, _2)
                                                │
                                                ▼
                                    [Önizleme Ağacı Simülasyonu]
                                       (Kullanıcı Onayı: yes/no)
                                                │
                                                ▼
                             [data_processing_common.py: execute_operations]
                                    (os.link / Hardlink Oluşturma)
                                                │
                                                ▼
                                    [Organize Edilmiş Çıktı]
```

---

## 4. Bağımlılıklar

### 4.1 Güncel `requirements.txt` Dosyasındaki Paketlerin Kullanımı (T2 Sonrası)

| Paket | Asgari Sürüm | Kod İçindeki Yeri ve Kullanım Amacı |
| :--- | :--- | :--- |
| `PyMuPDF` | `>=1.24.0` | `file_utils.py` içinde `import fitz` olarak kullanılır. PDF belgelerinin ilk 3 sayfasındaki metinleri çıkarır. |
| `python-docx` | `>=1.0.0` | `file_utils.py` içinde `import docx` olarak kullanılır. Word (`.docx`) belgelerinin metin paragraflarını okur. |
| `python-pptx` | `>=1.0.0` | `file_utils.py` içinde `from pptx import Presentation` olarak kullanılır. PowerPoint sunumlarındaki metinleri okur. |
| `pandas` | `>=2.0.0` | `file_utils.py` içinde `import pandas as pd` olarak kullanılır. Excel ve CSV tablolarını okur. |
| `openpyxl` | `>=3.1.0` | Kodda doğrudan import edilmez. Pandas'ın `.xlsx` dosyalarını okuması için gerekli motordur. |
| `xlrd` | `>=2.0.1` | Kodda doğrudan import edilmez. Pandas'ın `.xls` dosyalarını okuması için eklenen motordur. |
| `nltk` | `>=3.8.0` | `main.py`, `text_data_processing.py` ve `image_data_processing.py` dosyalarında NLP temizleme için kullanılır. |
| `rich` | `>=13.0.0` | `data_processing_common.py`, `text_data_processing.py` ve `image_data_processing.py` dosyalarında terminal ilerleme çubukları (`Progress`) için kullanılır. |
| `Pillow` | `>=12.3.0` | `file_utils.py` içinde `from PIL import Image` olarak kullanılır. (T2/T3 ile güncellendi). |
| `ollama` | `>=0.6.3` | Yerel hafif yapay zeka çıkarımı (T3 hedefi) için eklendi. |

### 4.2 Temizlenen Bağımlılıklar
- **`cmake`:** Python kodu olmadığı ve C++ derlemesi gereksinimi kaldırıldığı için `requirements.txt`'ten çıkarıldı.
- **`pytesseract`:** Kodda hiçbir fonksiyonu çağrılmadığı için `requirements.txt` ve `file_utils.py` importlarından çıkarıldı.

---

## 5. Model Katmanı

Projede metin işleme modeli olarak yerel çalışan **Ollama** servisi ve **`qwen3.5:2b`** modeli kullanılmaktadır (T3 kapsamında taşınmıştır).

### 5.1 Model Tanımları ve Başlatma (`main.py` & `text_data_processing.py`)
- **İstemci:** `OllamaTextInference` sınıfı (`text_data_processing.py`)
- **Modellerin İlklendirilmesi:** `initialize_models()` fonksiyonunda (`main.py`):
  - **Metin Modeli (LLM):**
    - Model Adı: `model_path_text = "qwen3.5:2b"`
    - Çağrı: `text_inference = OllamaTextInference(model_name=model_path_text)`
    - Özellik: `think=False` parametresi ile akıl yürütme (reasoning) döngüsü atlanarak doğrudan ve hızlı sonuç üretilir.
  - **Görsel Modeli / Stratejisi (T4):**
    - `qwen3.5:2b` modeli teknik özellik olarak CLIP tabanlı görsel girdi (vision) yeteneğine sahip olmakla birlikte, yerel Ollama servisi üzerinden görsel işleme testi zaman aşımına (>120s) uğradığı için mimari karar gereği görseller içerik analizi yapılmadan, kural ve uzantı tabanlı olarak hızlı ve hatasız biçimde `image_files/` klasörüne kategorize edilir (`image_data_processing.py`).

### 5.2 Metin İşleme Çağrıları (`text_data_processing.py`)
- `text_inference.create_completion(prompt)`:
  - **Özet:** Metin içeriğinden en fazla 150 kelimelik özet türetir (`summarize_text_content`).
  - **Dosya Adı:** Özete dayanarak en fazla 3 kelimelik isim odaklı dosya adı üretir.
  - **Kategori:** Özete dayanarak en fazla 2 kelimelik genel kategori/klasör adı üretir.

### 5.3 Görsel İşleme Çağrıları (`image_data_processing.py`)
- `image_inference._chat(description_prompt, image_path)`:
  - Görseli ve prompt'u alarak jeneratör üzerinden görsel betimleme metni üretir (Satır 71).
- `text_inference.create_completion(filename_prompt)`:
  - Görsel betimlemesini kullanarak dosya adı üretir (Satır 91).
- `text_inference.create_completion(foldername_prompt)`:
  - Görsel betimlemesini kullanarak kategori klasör adı üretir (Satır 119).

---

## 6. Çalışma Akışı

### 6.1 CLI Argümanları
Kaynak kod incelendiğinde `argparse`, `sys.argv` veya `click` gibi komut satırı bayrakları (flags) **kullanılmamaktadır**. Tüm parametreler terminal üzerinden etkileşimli (`input()`) olarak alınır:

| İstem Sırası | Parametre / Soru | Varsayılan Değer | İşlevi |
| :---: | :--- | :--- | :--- |
| 1 | `Would you like to enable silent mode? (yes/no): ` | Yok (Zorunlu girdi) | `yes` seçilirse loglar `operation_log.txt` dosyasına yönlendirilir; terminal temiz tutulur. |
| 2 | `Enter the path of the directory you want to organize: ` | Yok (Dizin doğrulanana kadar döngüde sorulur) | Düzenlenecek kaynak dizin yolu. |
| 3 | `Enter the path to store organized files and folders...: ` | Kaynak dizin ile aynı seviyede `organized_folder` | Düzenlenen dosyaların oluşturulacağı hedef dizin. |
| 4 | `Enter 1, 2, or 3 (or type '/exit' to exit): ` | Yok (Zorunlu girdi) | `1`: İçerik (AI), `2`: Tarih, `3`: Tür. |
| 5 | `Would you like to proceed with these changes? (yes/no): ` | Yok (Zorunlu girdi) | Simüle edilen ağaç onaylanırsa operasyonlar diske uygulanır. |
| 6 | `Would you like to organize another directory? (yes/no): ` | Yok (Zorunlu girdi) | Başka bir dizin düzenleme döngüsüne girilip girilmeyeceği. |

### 6.2 Dry-Run, Silent Mode ve Hardlink Davranışı
- **Dry-Run:** `main.py` satır 142'de `dry_run = True` tanımlanmış olsa da kod akışında `simulate_directory_tree` fonksiyonu ile operasyonlar önce hafızada ağaca dönüştürülür ve kullanıcı onayına sunulur. Onay verilirse `execute_operations(..., dry_run=False)` ile gerçek yazma yapılır.
- **Silent Mode:** Etkinleştirilirse `print` çıktıları yerine `operation_log.txt` dosyasına ekleme (`'a'`) yapılır.
- **Hardlink (`os.link`) ve Çapraz Sürücü Davranışı (T5):**
  - Dosyalar öncelikle kaynak dosyanın inode/dosya kaydına işaret eden bir hardlink (`os.link(source, destination)`) ile oluşturulur. Bu sayede diskte ek yer kaplamaz ve anında oluşur.
  - **Çapraz Sürücü Güvenliği (Atlama / Skip):** Eğer kaynak ile hedef farklı fiziksel disk bölümlerindeyse (`[WinError 17]` veya POSIX `EXDEV`) ya da dosya sistemi hardlink desteklemiyorsa, sessizce fiziksel kopya oluşturulmaz (disk alanını çift tüketmemek ve taşıma semantiğini korumak amacıyla); işlem atlanır (`skipped_cross_device`) ve log dosyasına kaydedilir. Orijinal dosyaya kesinlikle dokunulmaz.

---

## 7. Giderilen Tutarsızlıklar (Eski README vs. Güncel Mimari)

Orijinal depodan devralınan README dosyasındaki teknik tutarsızlıklar T1-T7 geliştirme döngüsünde tamamen giderilmiş ve güncel `README.md` kod tabanıyla %100 uyumlu hale getirilmiştir:

| Konu | Eski README İfadesi | Yapılan Düzeltme ve Güncel Durum |
| :--- | :--- | :--- |
| **İstem Dosyası Adı** | `data_processing.py` | Kodda dosya adı `data_processing_common.py` olup, prompt'lar `text_data_processing.py` ve `image_data_processing.py` içindedir. README buna göre güncellendi. |
| **Lisans Dosyası** | `LICENSE-MIT` ve Apache 2.0 | Projede yalnızca `LICENSE` (MIT) mevcuttur. Telif 2026 İhsan / İhsanAi olarak güncellendi ve `NOTICE.md` eklendi. |
| **Eksik / Atıl Paketler** | `pip install nexa Pillow pytesseract...` | `requirements.txt` dosyasından `nexa`/`cmake`/`pytesseract` temizlendi; `ollama>=0.6.3`, `Pillow>=12.3.0`, `xlrd>=2.0.1` eklendi. |
| **Python Sürümü** | Yalnızca "Python 3.12" | Python 3.10+ (Python 3.12 ve Python 3.13.6 sanal ortamı) tam uyumlu hale getirildi. |
| **Model İsimleri** | Nexa Llama3.2 3B & LLaVA-v1.6 | Yerel Ollama API ve `qwen3.5:2b` modeline taşındı. |
| **Multiprocessing İddiası** | "Uses multiprocessing..." | Asılsız iddia kaldırıldı; ardışık ve güvenli işlem akışı belgelendi. |
| **Tesseract Kullanımı** | Tesseract kurulum adımları | Kodda kullanılmayan `pytesseract` import'u ve Tesseract gereksinimi kaldırıldı. |

---

## 8. Kısıtlar ve Teknik Sınırlar

1. **İşletim Sistemi ve Yol Kısıtları (Windows / POSIX):**
   - Kod genel olarak `os.path.join` kullanmaktadır; ancak bazı dosya yollarında konsol çıktı formatları (`os.sep`) platformlar arası farklılık gösterebilir.
   - Windows üzerinde açık veya kilitli dosyalar hardlink oluşturulurken veya taşınırken erişim engeli (`PermissionError`) oluşturabilir.
2. **Hardlink Çapraz Sürücü Sınırı (Cross-Device Link - WinError 17):**
   - `os.link` yalnızca aynı fiziksel disk bölümü (aynı NTFS/ext4 cildi) üzerinde geçerlidir. Farklı sürücüler arasında (örneğin harici diskten C sürücüsüne) çalışamaz.
3. **Python Sürümü Uyumu:**
   - Proje Python 3.13.6 sanal ortamında test edilmiştir. Diğer sürümler (Python 3.10+ veya 3.12) test edilmediği için [Belirsiz] olarak değerlendirilmelidir.
4. **Bağlam ve Karakter Sınırları:**
   - Metin dosyaları için `max_chars = 3000` sınırı uygulanır.
   - PDF dosyaları için `num_pages_to_read = 3` sınırı uygulanır. Bu sınırların dışındaki içerikler analize dahil edilmez.

---

## 9. Görev ve Geliştirme Durum Tablosu (GOALS.md Senkronizasyonu)

| ID | Başlık | Açıklama | Etkilenen Dosyalar | Kabul Kriteri | Öncelik | Durum |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
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

## 10. Masaüstü Düzenleyici Grafik Arayüz Mimarisi (`gui.py`)

Projenin konsol (CLI) yapısından bağımsız, kullanıcı dostu ve güvenli pencereli masaüstü düzenleme katmanıdır:

1. **Katmanlı Ayrık Mimari:**
   - **İş Mantığı Fonksiyonları:** Tkinter arayüzünden tamamen bağımsız çalışabilen `plan_moves()`, `execute_moves()`, `undo_last()` ve `infer_category_ai()` fonksiyonları.
   - **Kullanıcı Arayüzü:** `create_gui()` ile başlatılan dinamik Tkinter penceresi; arka plan `threading.Thread` ile UI donmalarını engeller.
2. **Güvenli Taşıma ve Geri Alma Sözleşmesi:**
   - Kaynak dosya doğrudan silinmez; önce hedefte `.<ad>.part` adıyla oluşturulur.
   - Boyut ve SHA-256 özetleri %100 uyuşursa `os.replace` ile nihai ada geçirilir ve kaynak silinir.
   - Tüm işlemler `LFO_undo/islem_<zaman>.json` kütüğüne yazılır ve `undo_last()` ile tek tıkla eski haline döndürülebilir.
3. **Yapay Zekâ ve Hızlı Mod Çift Motoru:**
   - **Hızlı Mod:** Milisaniyeler içinde uzantı sözlüğüyle anında sınıflandırma.
   - **Yapay Zekâ Modu:** `file_utils.read_file_data()` ile belgeleri okuyup yerel Ollama `qwen3.5:2b` ile anlamsal konu başlıklarına (`Academic_Papers`, `Bank_Statements`, vb.) göre sınıflandırma.
