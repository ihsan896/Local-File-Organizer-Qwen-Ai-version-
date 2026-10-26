import os
import sys
import shutil
import hashlib
import datetime
import json
import threading
import re
import socket
import time
import subprocess

# ==============================================================================
# Sabitler ve Yapılandırma
# ==============================================================================

EXTENSION_CATEGORIES = {
    # Resim
    '.png': 'Resim',
    '.jpg': 'Resim',
    '.jpeg': 'Resim',
    '.gif': 'Resim',
    '.bmp': 'Resim',
    '.tiff': 'Resim',
    # Metin
    '.txt': 'Metin',
    '.md': 'Metin',
    # Belge
    '.docx': 'Belge',
    '.doc': 'Belge',
    # PDF
    '.pdf': 'PDF',
    # Tablo
    '.xlsx': 'Tablo',
    '.xls': 'Tablo',
    '.csv': 'Tablo',
    # Sunum
    '.ppt': 'Sunum',
    '.pptx': 'Sunum',
}

AI_PROCESSABLE_EXTENSIONS = {
    '.txt', '.md', '.docx', '.doc', '.pdf', '.xlsx', '.xls', '.csv', '.ppt', '.pptx'
}

FORBIDDEN_EXTENSIONS = {
    '.lnk', '.url', '.exe', '.msi', '.bat', '.cmd', '.ps1', '.ini', '.sys'
}

DEFAULT_UNDO_DIR = os.path.join(os.path.expanduser("~"), "LFO_undo")
CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".lfo_config.json")


# ==============================================================================
# Çoklu Dil ve Çeviri Sözlüğü (i18n)
# ==============================================================================

TRANSLATIONS = {
    "tr": {
        "app_title": "Desktop Organizer (Ihsan-AI)",
        "folder_selection": " Klasör Seçimi ",
        "source_folder": "Kaynak Klasör:",
        "target_folder": "Hedef Klasör:",
        "browse": "Gözat...",
        "mode_selection": " Düzenleme Yöntemi ",
        "mode_fast": "🚀 Hızlı Mod (Uzantıya Göre - Anında)",
        "mode_ai": "🧠 Yapay Zekâ Modu (Ollama qwen3.5:2b - İçeriğe Göre)",
        "preview_table": " Önizleme Tablosu ",
        "col_name": "Dosya Adı",
        "col_size": "Boyut",
        "col_target": "Hedef Klasör",
        "col_status": "Durum",
        "btn_preview": "Önizleme",
        "btn_move": "Taşı",
        "btn_undo": "Son işlemi geri al",
        "btn_close": "Kapat",
        "btn_theme_dark": "🌙 Koyu Tema",
        "btn_theme_light": "☀️ Açık Tema",
        "btn_lang": "🌐 English",
        "status_ready": "Hazır. Kaynak klasörü seçip 'Önizleme' düğmesine basın.",
        "status_fast_ready": "Hızlı mod hazır: {move_count} dosya taşınacak, {skip_count} öğe atlandı.",
        "status_no_files": "Önizleme tamamlandı: Taşınacak dosya bulunamadı ({skip_count} öğe atlandı).",
        "status_no_ai_files": "Yapay zekâ ile incelenebilecek metin/belge bulunamadı. Genel kategoriler devrede.",
        "status_ai_analyzing": "Yapay zekâ analiz ediyor ({cur}/{tot}): {name}...",
        "status_ai_done": "Yapay zekâ analizi tamamlandı: {count} belge akıllı konulara eşlendi.",
        "status_moving": "Taşınıyor ({cur}/{tot}): {name}",
        "status_move_done": "İşlem tamamlandı: {count} dosya taşındı.",
        "status_move_warn": "Hatalarla tamamlandı: {count} dosya taşındı.",
        "status_undoing": "Geri alınıyor ({cur}/{tot}): {name}",
        "status_undo_done": "Son işlem geri alındı: {count} dosya geri taşındı.",
        "confirm_move_title": "Taşıma Onayı",
        "confirm_move_msg": "{count} dosya {mode} taşınacak.\nHedef: {dest}\n\nDevam etmek istiyor musunuz?",
        "mode_text_ai": "Yapay Zekâ Konu Başlıklarına",
        "mode_text_fast": "Tür Klasörlerine",
        "success_title": "Başarılı",
        "success_move_msg": "{count} dosya başarıyla taşındı.\nGeri alma kaydı oluşturuldu.",
        "undo_success_title": "Geri Alma Başarılı",
        "undo_success_msg": "{count} dosya kaynak konumuna geri taşındı.",
        "undo_warn_title": "Geri Alma Bildirimi",
        "status_ai_checking": "Sistem & Yapay Zekâ donanım kontrolleri yapılıyor...",
        "ollama_starting": "Ollama servisi arka planda otomatik başlatılıyor... Lütfen bekleyin...",
        "model_pulling": "qwen3.5:2b modeli yerel sisteme indiriliyor, lütfen bekleyin...",
        "ollama_not_installed_title": "Ollama Bulunamadı",
        "ollama_not_installed_msg": "Bilgisayarınızda Ollama kurulu bulunamadı.\n\nYapay zekâ ile içerik analizi yapabilmek için lütfen https://ollama.com adresinden Ollama'yı indirip kurunuz.\n\nŞimdilik Hızlı Mod devrede kalacaktır.",
        "ollama_conn_err_title": "Bağlantı Hatası",
        "ollama_conn_err_msg": "Ollama servisi başlatılamadı veya yanıt vermedi. Hızlı moda geçiliyor.",
        "ollama_model_missing_title": "Model Eksik",
        "ollama_model_missing_msg": "qwen3.5:2b modeli indirilemedi. Lütfen terminalden 'ollama pull qwen3.5:2b' komutunu çalıştırın.",
        "ai_badge_ready": "🟢 AI Hazır (qwen3.5:2b Aktif)",
        "ai_badge_starting": "🟡 AI Başlatılıyor...",
        "ai_badge_missing": "🔴 Ollama Eksik",
        "err_source_not_found": "Kaynak klasör bulunamadı:\n{path}",
        "info_no_files_to_move": "Taşınacak dosya yok.",
        "status_skip_folder": "Atlandı: Klasörler taşınmaz",
        "status_skip_hidden": "Atlandı: Gizli/sistem dosyası",
        "status_skip_forbidden": "Atlandı: Yasaklı uzantı ({ext})",
        "status_to_move": "Taşınacak",
        "status_to_move_ai": "Taşınacak (AI: {cat})",
        "welcome_title": "Dil Seçimi / Language Selection",
        "welcome_msg": "Lütfen tercih ettiğiniz dili seçiniz:\nPlease select your preferred language:"
    },
    "en": {
        "app_title": "Desktop Organizer (Ihsan-AI)",
        "folder_selection": " Folder Selection ",
        "source_folder": "Source Folder:",
        "target_folder": "Target Folder:",
        "browse": "Browse...",
        "mode_selection": " Organization Method ",
        "mode_fast": "🚀 Fast Mode (By Extension - Instant)",
        "mode_ai": "🧠 AI Mode (Ollama qwen3.5:2b - By Content)",
        "preview_table": " Preview Table ",
        "col_name": "File Name",
        "col_size": "Size",
        "col_target": "Target Folder",
        "col_status": "Status",
        "btn_preview": "Preview",
        "btn_move": "Move",
        "btn_undo": "Undo Last Action",
        "btn_close": "Close",
        "btn_theme_dark": "🌙 Dark Theme",
        "btn_theme_light": "☀️ Light Theme",
        "btn_lang": "🌐 Türkçe",
        "status_ready": "Ready. Select source folder and click 'Preview'.",
        "status_fast_ready": "Fast mode ready: {move_count} files to move, {skip_count} items skipped.",
        "status_no_files": "Preview finished: No files to move ({skip_count} items skipped).",
        "status_no_ai_files": "No readable documents found for AI analysis. General categories applied.",
        "status_ai_analyzing": "AI analyzing ({cur}/{tot}): {name}...",
        "status_ai_done": "AI analysis complete: {count} documents mapped to smart topics.",
        "status_moving": "Moving ({cur}/{tot}): {name}",
        "status_move_done": "Operation complete: {count} files moved.",
        "status_move_warn": "Completed with warnings: {count} files moved.",
        "status_undoing": "Restoring ({cur}/{tot}): {name}",
        "status_undo_done": "Last operation undone: {count} files restored.",
        "confirm_move_title": "Move Confirmation",
        "confirm_move_msg": "{count} files will be moved to {mode}.\nDestination: {dest}\n\nDo you want to continue?",
        "mode_text_ai": "AI Topic Folders",
        "mode_text_fast": "Type Folders",
        "success_title": "Success",
        "success_move_msg": "{count} files moved successfully.\nUndo record created.",
        "undo_success_title": "Undo Successful",
        "undo_success_msg": "{count} files restored to source location.",
        "undo_warn_title": "Undo Notice",
        "status_ai_checking": "Checking system & AI environment readiness...",
        "ollama_starting": "Automatically starting Ollama service in background... Please wait...",
        "model_pulling": "Downloading qwen3.5:2b model to local system, please wait...",
        "ollama_not_installed_title": "Ollama Not Found",
        "ollama_not_installed_msg": "Ollama was not found on your system.\n\nTo use AI content analysis, please download and install Ollama from https://ollama.com.\n\nFast Mode will remain active for now.",
        "ollama_conn_err_title": "Connection Error",
        "ollama_conn_err_msg": "Ollama service failed to start or did not respond. Switching to Fast Mode.",
        "ollama_model_missing_title": "Model Missing",
        "ollama_model_missing_msg": "Failed to pull qwen3.5:2b model. Please run 'ollama pull qwen3.5:2b' from terminal.",
        "ai_badge_ready": "🟢 AI Ready (qwen3.5:2b Active)",
        "ai_badge_starting": "🟡 AI Starting...",
        "ai_badge_missing": "🔴 Ollama Missing",
        "err_source_not_found": "Source folder not found:\n{path}",
        "info_no_files_to_move": "No files to move.",
        "status_skip_folder": "Skipped: Folders are not moved",
        "status_skip_hidden": "Skipped: Hidden/system file",
        "status_skip_forbidden": "Skipped: Forbidden extension ({ext})",
        "status_to_move": "To Move",
        "status_to_move_ai": "To Move (AI: {cat})",
        "welcome_title": "Language Selection",
        "welcome_msg": "Please select your preferred language:\nLütfen tercih ettiğiniz dili seçiniz:"
    }
}


def load_config():
    """Kullanıcı tercihlerini (dil ve tema) yükler."""
    defaults = {"language": None, "theme": "light"}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                defaults.update(data)
        except Exception:
            pass
    return defaults


def save_config(cfg):
    """Kullanıcı tercihlerini diske kaydeder."""
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# ==============================================================================
# Tema Renk Paletleri
# ==============================================================================

THEMES = {
    "light": {
        "bg": "#f4f5f7",
        "fg": "#1e293b",
        "sub_fg": "#475569",
        "frame_bg": "#ffffff",
        "entry_bg": "#ffffff",
        "entry_fg": "#0f172a",
        "entry_border": "#cbd5e1",
        "btn_bg": "#e2e8f0",
        "btn_fg": "#1e293b",
        "btn_active_bg": "#cbd5e1",
        "primary_btn_bg": "#2563eb",
        "primary_btn_fg": "#ffffff",
        "tree_bg": "#ffffff",
        "tree_fg": "#1e293b",
        "tree_select_bg": "#3b82f6",
        "tree_select_fg": "#ffffff",
        "tree_head_bg": "#f1f5f9",
        "tree_head_fg": "#0f172a",
        "trough_bg": "#e2e8f0",
        "prog_bg": "#3b82f6"
    },
    "dark": {
        "bg": "#181825",
        "fg": "#cdd6f4",
        "sub_fg": "#a6adc8",
        "frame_bg": "#1e1e2e",
        "entry_bg": "#313244",
        "entry_fg": "#cdd6f4",
        "entry_border": "#45475a",
        "btn_bg": "#313244",
        "btn_fg": "#cdd6f4",
        "btn_active_bg": "#45475a",
        "primary_btn_bg": "#89b4fa",
        "primary_btn_fg": "#11111b",
        "tree_bg": "#11111b",
        "tree_fg": "#cdd6f4",
        "tree_select_bg": "#45475a",
        "tree_select_fg": "#ffffff",
        "tree_head_bg": "#313244",
        "tree_head_fg": "#cdd6f4",
        "trough_bg": "#313244",
        "prog_bg": "#89b4fa"
    }
}


# ==============================================================================
# Yardımcı Güvenlik ve Bütünlük Fonksiyonları
# ==============================================================================

def compute_sha256(filepath):
    """Dosyanın SHA-256 özetini hesaplar."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def is_hidden_or_system(file_path):
    """Gizli veya sistem dosyası olup olmadığını denetler."""
    name = os.path.basename(file_path)
    if name.startswith('.'):
        return True
    if name.lower() in ('desktop.ini', 'thumbs.db'):
        return True

    if sys.platform == 'win32':
        try:
            import ctypes
            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(file_path))
            if attrs != -1:
                FILE_ATTRIBUTE_HIDDEN = 0x2
                FILE_ATTRIBUTE_SYSTEM = 0x4
                if attrs & (FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM):
                    return True
        except Exception:
            pass
    return False


def format_size(size_bytes):
    """Bayt cinsinden dosya boyutunu okunabilir formata dönüştürür."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


# ==============================================================================
# Akıllı Sistem Denetimi ve Ollama Otomatik Başlatma Motoru
# ==============================================================================

def is_ollama_installed():
    """Ollama çalıştırılabilir dosyasının sistemde kurulu olup olmadığını denetler."""
    if shutil.which("ollama"):
        return True
    if sys.platform == 'win32':
        default_win_path = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama\ollama.exe")
        if os.path.exists(default_win_path):
            return True
    return False


def is_ollama_port_open(host="127.0.0.1", port=11434, timeout=0.8):
    """Ollama HTTP portunun (11434) açık olup olmadığını kontrol eder."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def start_ollama_service():
    """Ollama servisini sessizce arka planda başlatır (konsol penceresi açmadan)."""
    ollama_cmd = "ollama"
    if sys.platform == 'win32':
        if not shutil.which("ollama"):
            default_win_path = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama\ollama.exe")
            if os.path.exists(default_win_path):
                ollama_cmd = default_win_path
        CREATE_NO_WINDOW = 0x08000000
        try:
            subprocess.Popen(
                [ollama_cmd, "serve"],
                creationflags=CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return True
        except Exception:
            return False
    else:
        try:
            subprocess.Popen(
                [ollama_cmd, "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            return True
        except Exception:
            return False


def ensure_ollama_ready(model_name="qwen3.5:2b", status_callback=None):
    """
    Sistem & AI Donanım Kontrolü:
    1. Ollama kurulu mu?
    2. Servis çalışıyor mu? Değilse otomatik arka planda başlat.
    3. qwen3.5:2b modeli yüklü mü? Değilse otomatik indir.
    4. İstemci bağlantısını doğrula.
    Döner: (success: bool, status_code: str, client: OllamaClient or None)
    """
    # 1. Kurulum denetimi
    if not is_ollama_installed():
        return False, "ollama_not_installed", None

    # 2. Servis açık mı? Değilse otomatik başlat
    if not is_ollama_port_open():
        if status_callback:
            status_callback("ollama_starting")
        started = start_ollama_service()
        if not started:
            return False, "ollama_start_failed", None

        # Servisin açılması için bekle (maksimum 10 saniye)
        for _ in range(10):
            time.sleep(1)
            if is_ollama_port_open():
                break

        if not is_ollama_port_open():
            return False, "ollama_start_timeout", None

    # 3. İstemci bağlantısı ve model denetimi
    try:
        import ollama
        client = ollama.Client()
        models_info = client.list()
        avail = [m.model for m in models_info.models] if hasattr(models_info, 'models') else []

        has_model = any(model_name in m for m in avail)
        if not has_model:
            if status_callback:
                status_callback("model_pulling")
            try:
                client.pull(model_name)
                has_model = True
            except Exception:
                return False, "model_pull_failed", client

        return True, "ready", client
    except Exception:
        return False, "connection_error", None


def infer_category_ai(file_path, client, model_name="qwen3.5:2b"):
    """Dosya içeriğini okur ve Ollama qwen3.5:2b modeli ile anlamsal konu klasörü belirler."""
    try:
        from file_utils import read_file_data
        text = read_file_data(file_path)
        if not text or len(text.strip()) < 10:
            return None

        sample_text = text.strip()[:1500]
        prompt = f"""Based on the document text below, determine a single concise folder name (1 to 2 words, letters and underscore only) representing its topic.
Examples:
Bank_Statements
Academic_Papers
Invoices
Notes
Presentations

Document Text:
{sample_text}

Folder Name:"""

        response = client.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            think=False,
            options={"temperature": 0.2}
        )
        raw = response.message.content.strip()
        cleaned = re.sub(r'^(Folder\s*Name|Category|Topic):\s*', '', raw, flags=re.IGNORECASE).strip()
        cleaned = re.sub(r'[^a-zA-Z0-9_ -]', '', cleaned).strip()
        cleaned = cleaned.replace(' ', '_')
        if cleaned and 2 <= len(cleaned) <= 30:
            return cleaned
        return None
    except Exception:
        return None


# ==============================================================================
# Planlama ve Taşıma İş Mantığı Katmanı
# ==============================================================================

def plan_moves(source_dir, target_dir, use_ai=False, progress_callback=None, lang="tr"):
    """
    Kaynak dizini tarar ve taşınacak / atlanacak dosyaların planını çıkarır.
    """
    t = TRANSLATIONS.get(lang, TRANSLATIONS["tr"])
    plan = []
    if not os.path.exists(source_dir) or not os.path.isdir(source_dir):
        return plan

    try:
        entries = sorted(os.listdir(source_dir))
    except Exception as e:
        return [{"name": "ERROR", "path": source_dir, "size": 0, "size_fmt": "-",
                 "target_category": "-", "target_path": "-",
                 "status": f"Error: {e}", "action": "skip", "reason": str(e)}]

    for entry in entries:
        item_path = os.path.join(source_dir, entry)

        # 1. Klasörler taşınmaz
        if os.path.isdir(item_path):
            plan.append({
                "name": entry,
                "path": item_path,
                "size": 0,
                "size_fmt": "-",
                "target_category": "-",
                "target_path": "-",
                "status": t["status_skip_folder"],
                "action": "skip",
                "reason": "Folder"
            })
            continue

        # 2. Gizli ve sistem dosyaları atlanır
        if is_hidden_or_system(item_path):
            size = os.path.getsize(item_path) if os.path.exists(item_path) else 0
            plan.append({
                "name": entry,
                "path": item_path,
                "size": size,
                "size_fmt": format_size(size),
                "target_category": "-",
                "target_path": "-",
                "status": t["status_skip_hidden"],
                "action": "skip",
                "reason": "Hidden/System"
            })
            continue

        # 3. Yasaklı uzantılar atlanır
        ext = os.path.splitext(entry)[1].lower()
        if ext in FORBIDDEN_EXTENSIONS:
            size = os.path.getsize(item_path) if os.path.exists(item_path) else 0
            plan.append({
                "name": entry,
                "path": item_path,
                "size": size,
                "size_fmt": format_size(size),
                "target_category": "-",
                "target_path": "-",
                "status": t["status_skip_forbidden"].format(ext=ext),
                "action": "skip",
                "reason": f"Forbidden ({ext})"
            })
            continue

        # 4. Temel Kategori
        category = EXTENSION_CATEGORIES.get(ext, 'Others')
        category_dir = os.path.join(target_dir, category)
        size = os.path.getsize(item_path) if os.path.exists(item_path) else 0

        plan.append({
            "name": entry,
            "path": item_path,
            "size": size,
            "size_fmt": format_size(size),
            "target_category": category,
            "target_dir": category_dir,
            "target_path": os.path.join(category_dir, entry),
            "status": t["status_to_move"],
            "action": "move",
            "reason": ""
        })

    # 5. Yapay Zekâ Analizi
    if use_ai:
        ok, reason, client = ensure_ollama_ready("qwen3.5:2b")
        if ok and client:
            ai_items = [
                it for it in plan
                if it.get("action") == "move" and os.path.splitext(it["name"])[1].lower() in AI_PROCESSABLE_EXTENSIONS
            ]
            total_ai = len(ai_items)
            for idx, item in enumerate(ai_items, 1):
                if progress_callback:
                    progress_callback(idx, total_ai, item["name"])
                ai_cat = infer_category_ai(item["path"], client, "qwen3.5:2b")
                if ai_cat:
                    item["target_category"] = ai_cat
                    item["target_dir"] = os.path.join(target_dir, ai_cat)
                    item["target_path"] = os.path.join(item["target_dir"], item["name"])
                    item["status"] = t["status_to_move_ai"].format(cat=ai_cat)

    return plan


def execute_moves(plan, undo_dir=DEFAULT_UNDO_DIR, progress_callback=None):
    """
    Planlanan taşımaları güvenli sıralamayla yürütür ve geri alma kaydı oluşturur.
    """
    to_move = [item for item in plan if item.get("action") == "move"]
    total = len(to_move)
    moved_records = []
    errors = []

    for idx, item in enumerate(to_move, 1):
        src_path = item["path"]
        category_dir = item["target_dir"]
        orig_name = item["name"]
        base, ext = os.path.splitext(orig_name)

        dest_filename = orig_name
        counter = 1
        while os.path.exists(os.path.join(category_dir, dest_filename)):
            dest_filename = f"{base}_{counter}{ext}"
            counter += 1
        final_dest_path = os.path.join(category_dir, dest_filename)

        os.makedirs(category_dir, exist_ok=True)
        part_path = os.path.join(category_dir, f".{dest_filename}.part")
        if os.path.exists(part_path):
            try:
                os.remove(part_path)
            except Exception:
                pass

        try:
            shutil.copy2(src_path, part_path)
        except Exception as e:
            errors.append(f"Copy error ({orig_name}): {e}")
            if os.path.exists(part_path):
                os.remove(part_path)
            if progress_callback:
                progress_callback(idx, total, orig_name)
            continue

        try:
            src_size = os.path.getsize(src_path)
            part_size = os.path.getsize(part_path)
            src_hash = compute_sha256(src_path)
            part_hash = compute_sha256(part_path)
        except Exception as e:
            errors.append(f"Integrity check error ({orig_name}): {e}")
            if os.path.exists(part_path):
                os.remove(part_path)
            if progress_callback:
                progress_callback(idx, total, orig_name)
            continue

        if src_size == part_size and src_hash == part_hash:
            try:
                os.replace(part_path, final_dest_path)
            except Exception as e:
                errors.append(f"Rename error ({orig_name}): {e}")
                if os.path.exists(part_path):
                    os.remove(part_path)
                if progress_callback:
                    progress_callback(idx, total, orig_name)
                continue

            try:
                os.remove(src_path)
            except Exception as e:
                errors.append(f"Source removal error ({orig_name}): {e}")

            moved_records.append({
                "kaynak": os.path.abspath(src_path),
                "hedef": os.path.abspath(final_dest_path),
                "sha256": src_hash
            })
        else:
            if os.path.exists(part_path):
                os.remove(part_path)
            errors.append(f"Hash/size mismatch ({orig_name}): Source untouched.")

        if progress_callback:
            progress_callback(idx, total, orig_name)

    undo_file = None
    if moved_records:
        os.makedirs(undo_dir, exist_ok=True)
        now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        undo_file = os.path.join(undo_dir, f"islem_{now_str}.json")
        with open(undo_file, 'w', encoding='utf-8') as f:
            json.dump(moved_records, f, ensure_ascii=False, indent=2)

    return {
        "success": len(errors) == 0,
        "total_planned": total,
        "moved_count": len(moved_records),
        "undo_file": undo_file,
        "errors": errors
    }


def undo_last(undo_dir=DEFAULT_UNDO_DIR, progress_callback=None):
    """
    En son başarılı taşıma işlemini geri alır.
    """
    if not os.path.exists(undo_dir):
        return {"success": False, "message": "Undo directory not found.", "restored": 0, "errors": []}

    candidates = []
    for f in os.listdir(undo_dir):
        if f.startswith("islem_") and f.endswith(".json") and not f.endswith("_geri_alindi.json"):
            candidates.append(os.path.join(undo_dir, f))

    if not candidates:
        return {"success": False, "message": "No active operation log found to undo.", "restored": 0, "errors": []}

    candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    latest_undo_file = candidates[0]

    with open(latest_undo_file, 'r', encoding='utf-8') as f:
        records = json.load(f)

    total = len(records)
    restored = 0
    errors = []

    for idx, rec in enumerate(records, 1):
        src_path = rec["kaynak"]
        dst_path = rec["hedef"]
        expected_hash = rec["sha256"]
        fname = os.path.basename(dst_path)

        if not os.path.exists(dst_path):
            errors.append(f"Target not found, skipped: {dst_path}")
            if progress_callback:
                progress_callback(idx, total, fname)
            continue

        try:
            current_hash = compute_sha256(dst_path)
            if current_hash != expected_hash:
                errors.append(f"Target content changed, skipped: {dst_path}")
                if progress_callback:
                    progress_callback(idx, total, fname)
                continue
        except Exception as e:
            errors.append(f"Hash error ({dst_path}): {e}")
            if progress_callback:
                progress_callback(idx, total, fname)
            continue

        if os.path.exists(src_path):
            errors.append(f"Source already exists, skipped: {src_path}")
            if progress_callback:
                progress_callback(idx, total, fname)
            continue

        src_dir = os.path.dirname(src_path)
        os.makedirs(src_dir, exist_ok=True)
        part_path = os.path.join(src_dir, f".{os.path.basename(src_path)}.part")

        try:
            if os.path.exists(part_path):
                os.remove(part_path)
            shutil.copy2(dst_path, part_path)

            part_size = os.path.getsize(part_path)
            dst_size = os.path.getsize(dst_path)
            part_hash = compute_sha256(part_path)

            if part_size == dst_size and part_hash == expected_hash:
                os.replace(part_path, src_path)
                os.remove(dst_path)
                restored += 1
            else:
                if os.path.exists(part_path):
                    os.remove(part_path)
                errors.append(f"Undo integrity failure ({dst_path})")
        except Exception as e:
            if os.path.exists(part_path):
                try:
                    os.remove(part_path)
                except Exception:
                    pass
            errors.append(f"Undo error ({dst_path} -> {src_path}): {e}")

        if progress_callback:
            progress_callback(idx, total, fname)

    renamed_undo_file = latest_undo_file.replace(".json", "_geri_alindi.json")
    try:
        os.replace(latest_undo_file, renamed_undo_file)
    except Exception as e:
        errors.append(f"Failed to rename undo file: {e}")

    return {
        "success": len(errors) == 0,
        "total": total,
        "restored": restored,
        "undo_file": renamed_undo_file,
        "errors": errors
    }


# ==============================================================================
# Grafik Kullanıcı Arayüzü (GUI - Tkinter)
# ==============================================================================

def create_gui():
    """Tkinter arayüzünü oluşturur, sistem kontrollerini ve dil/tema motorunu başlatır."""
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox

    cfg = load_config()

    # İlk çalıştırmada dil seçimi modal penceresi
    if cfg.get("language") not in ("tr", "en"):
        init_root = tk.Tk()
        init_root.title("Language / Dil")
        init_root.geometry("380x180")
        init_root.resizable(False, False)
        init_root.configure(bg="#f8f9fa")

        def choose_tr():
            cfg["language"] = "tr"
            save_config(cfg)
            init_root.destroy()

        def choose_en():
            cfg["language"] = "en"
            save_config(cfg)
            init_root.destroy()

        lbl_title = tk.Label(
            init_root,
            text="Welcome / Hoş Geldiniz",
            font=("Segoe UI", 12, "bold"),
            bg="#f8f9fa",
            fg="#1e293b"
        )
        lbl_title.pack(pady=(18, 6))

        lbl_sub = tk.Label(
            init_root,
            text="Please select your language / Lütfen dilinizi seçiniz:",
            font=("Segoe UI", 9),
            bg="#f8f9fa",
            fg="#475569"
        )
        lbl_sub.pack(pady=(0, 16))

        btn_box = tk.Frame(init_root, bg="#f8f9fa")
        btn_box.pack(pady=4)

        btn_tr = tk.Button(
            btn_box,
            text="🇹🇷 Türkçe",
            font=("Segoe UI", 10, "bold"),
            bg="#2563eb",
            fg="#ffffff",
            activebackground="#1d4ed8",
            activeforeground="#ffffff",
            width=13,
            pady=4,
            command=choose_tr
        )
        btn_tr.pack(side=tk.LEFT, padx=10)

        btn_en = tk.Button(
            btn_box,
            text="🇬🇧 English",
            font=("Segoe UI", 10, "bold"),
            bg="#0f172a",
            fg="#ffffff",
            activebackground="#1e293b",
            activeforeground="#ffffff",
            width=13,
            pady=4,
            command=choose_en
        )
        btn_en.pack(side=tk.LEFT, padx=10)

        init_root.mainloop()

    current_lang = cfg.get("language", "en")
    current_theme = cfg.get("theme", "light")
    if current_theme not in THEMES:
        current_theme = "light"

    root = tk.Tk()
    root.geometry("950x710")
    root.minsize(820, 570)

    # Değişkenler
    default_src = os.path.join(os.path.expanduser("~"), "Desktop")
    source_var = tk.StringVar(value=default_src)
    target_var = tk.StringVar(value=os.path.join(default_src, "Duzenli"))
    mode_var = tk.StringVar(value="fast")
    status_msg_var = tk.StringVar()
    ai_status_text = tk.StringVar(value="🟡 AI...")
    current_plan = []
    is_busy = False

    style = ttk.Style(root)
    style.theme_use('clam')

    widgets = {}

    def get_text(key, **kwargs):
        t = TRANSLATIONS.get(current_lang, TRANSLATIONS["en"])
        val = t.get(key, key)
        if kwargs:
            try:
                val = val.format(**kwargs)
            except Exception:
                pass
        return val

    # ==========================================================================
    # Tema Uygulama Motoru
    # ==========================================================================
    def apply_theme(theme_name):
        nonlocal current_theme
        current_theme = theme_name
        cfg["theme"] = theme_name
        save_config(cfg)
        palette = THEMES[theme_name]

        root.configure(bg=palette["bg"])

        style.configure('.', background=palette["bg"], foreground=palette["fg"])
        style.configure('TFrame', background=palette["bg"])
        style.configure('TLabelframe', background=palette["bg"])
        style.configure('TLabelframe.Label', background=palette["bg"], foreground=palette["fg"], font=("Segoe UI", 10, "bold"))
        style.configure('TLabel', background=palette["bg"], foreground=palette["fg"], font=("Segoe UI", 9))
        style.configure('TRadiobutton', background=palette["bg"], foreground=palette["fg"], font=("Segoe UI", 9))
        style.map('TRadiobutton', background=[('active', palette["bg"])])

        style.configure('TButton', background=palette["btn_bg"], foreground=palette["btn_fg"], font=("Segoe UI", 9), borderwidth=1)
        style.map('TButton', background=[('active', palette["btn_active_bg"]), ('disabled', palette["btn_bg"])],
                            foreground=[('disabled', palette["sub_fg"])])

        style.configure('Primary.TButton', background=palette["primary_btn_bg"], foreground=palette["primary_btn_fg"], font=("Segoe UI", 9, "bold"))
        style.map('Primary.TButton', background=[('active', palette["btn_active_bg"])])

        style.configure('TEntry', fieldbackground=palette["entry_bg"], foreground=palette["entry_fg"])
        style.configure('TProgressbar', background=palette["prog_bg"], troughcolor=palette["trough_bg"])

        style.configure('Treeview',
                        background=palette["tree_bg"],
                        foreground=palette["tree_fg"],
                        fieldbackground=palette["tree_bg"],
                        rowheight=26,
                        font=("Segoe UI", 9))
        style.map('Treeview',
                  background=[('selected', palette["tree_select_bg"])],
                  foreground=[('selected', palette["tree_select_fg"])])

        style.configure('Treeview.Heading',
                        background=palette["tree_head_bg"],
                        foreground=palette["tree_head_fg"],
                        font=("Segoe UI", 9, "bold"),
                        relief='flat')
        style.map('Treeview.Heading', background=[('active', palette["btn_active_bg"])])

        if "header_frame" in widgets:
            widgets["header_frame"].configure(bg=palette["bg"])
            widgets["app_title_lbl"].configure(bg=palette["bg"], fg=palette["fg"])
            widgets["theme_btn"].configure(text=get_text("btn_theme_light") if current_theme == "dark" else get_text("btn_theme_dark"),
                                           bg=palette["btn_bg"], fg=palette["btn_fg"])
            widgets["lang_btn"].configure(bg=palette["btn_bg"], fg=palette["btn_fg"])

    # ==========================================================================
    # Dil Güncelleme Motoru
    # ==========================================================================
    def update_ui_language():
        root.title(get_text("app_title"))
        widgets["top_frame"].configure(text=get_text("folder_selection"))
        widgets["lbl_src"].configure(text=get_text("source_folder"))
        widgets["lbl_dst"].configure(text=get_text("target_folder"))
        widgets["btn_browse_src"].configure(text=get_text("browse"))
        widgets["btn_browse_dst"].configure(text=get_text("browse"))

        widgets["mode_frame"].configure(text=get_text("mode_selection"))
        widgets["rb_fast"].configure(text=get_text("mode_fast"))
        widgets["rb_ai"].configure(text=get_text("mode_ai"))

        widgets["mid_frame"].configure(text=get_text("preview_table"))
        widgets["tree"].heading("name", text=get_text("col_name"))
        widgets["tree"].heading("size", text=get_text("col_size"))
        widgets["tree"].heading("category", text=get_text("col_target"))
        widgets["tree"].heading("status", text=get_text("col_status"))

        widgets["btn_preview"].configure(text=get_text("btn_preview"))
        widgets["btn_move"].configure(text=get_text("btn_move"))
        widgets["btn_undo"].configure(text=get_text("btn_undo"))
        widgets["btn_close"].configure(text=get_text("btn_close"))

        widgets["lang_btn"].configure(text=get_text("btn_lang"))
        widgets["theme_btn"].configure(text=get_text("btn_theme_light") if current_theme == "dark" else get_text("btn_theme_dark"))

        status_msg_var.set(get_text("status_ready"))

    def toggle_language():
        nonlocal current_lang
        current_lang = "en" if current_lang == "tr" else "tr"
        cfg["language"] = current_lang
        save_config(cfg)
        update_ui_language()
        if current_plan:
            on_preview()

    def toggle_theme():
        new_theme = "light" if current_theme == "dark" else "dark"
        apply_theme(new_theme)

    # 1. Header Toolbar
    header_frame = tk.Frame(root)
    header_frame.pack(fill=tk.X, padx=14, pady=(10, 4))
    widgets["header_frame"] = header_frame

    app_title_lbl = tk.Label(header_frame, text="Desktop Organizer", font=("Segoe UI", 12, "bold"))
    app_title_lbl.pack(side=tk.LEFT)
    widgets["app_title_lbl"] = app_title_lbl

    btn_tools_frame = tk.Frame(header_frame)
    btn_tools_frame.pack(side=tk.RIGHT)

    lang_btn = tk.Button(
        btn_tools_frame,
        text="🌐 English",
        font=("Segoe UI", 9),
        relief="groove",
        padx=8,
        pady=2,
        command=toggle_language
    )
    lang_btn.pack(side=tk.LEFT, padx=6)
    widgets["lang_btn"] = lang_btn

    theme_btn = tk.Button(
        btn_tools_frame,
        text="🌙 Dark Theme",
        font=("Segoe UI", 9),
        relief="groove",
        padx=8,
        pady=2,
        command=toggle_theme
    )
    theme_btn.pack(side=tk.LEFT, padx=2)
    widgets["theme_btn"] = theme_btn

    # 2. Klasör Seçimi Paneli
    top_frame = ttk.LabelFrame(root, text=" Folder Selection ", padding=10)
    top_frame.pack(fill=tk.X, padx=12, pady=4)
    widgets["top_frame"] = top_frame

    lbl_src = ttk.Label(top_frame, text="Source Folder:")
    lbl_src.grid(row=0, column=0, sticky=tk.W, pady=4)
    widgets["lbl_src"] = lbl_src

    src_entry = ttk.Entry(top_frame, textvariable=source_var, width=65)
    src_entry.grid(row=0, column=1, padx=6, pady=4, sticky=tk.EW)

    def browse_source():
        if is_busy:
            return
        chosen = filedialog.askdirectory(initialdir=source_var.get(), title=get_text("source_folder"))
        if chosen:
            source_var.set(chosen)
            target_var.set(os.path.join(chosen, "Duzenli"))
            on_preview()

    btn_browse_src = ttk.Button(top_frame, text="Browse...", command=browse_source)
    btn_browse_src.grid(row=0, column=2, padx=4, pady=4)
    widgets["btn_browse_src"] = btn_browse_src

    lbl_dst = ttk.Label(top_frame, text="Target Folder:")
    lbl_dst.grid(row=1, column=0, sticky=tk.W, pady=4)
    widgets["lbl_dst"] = lbl_dst

    dst_entry = ttk.Entry(top_frame, textvariable=target_var, width=65)
    dst_entry.grid(row=1, column=1, padx=6, pady=4, sticky=tk.EW)

    def browse_target():
        if is_busy:
            return
        chosen = filedialog.askdirectory(initialdir=target_var.get(), title=get_text("target_folder"))
        if chosen:
            target_var.set(chosen)
            if current_plan:
                on_preview()

    btn_browse_dst = ttk.Button(top_frame, text="Browse...", command=browse_target)
    btn_browse_dst.grid(row=1, column=2, padx=4, pady=4)
    widgets["btn_browse_dst"] = btn_browse_dst
    top_frame.columnconfigure(1, weight=1)

    # 3. Düzenleme Yöntemi ve Canlı AI Rozeti
    mode_frame = ttk.LabelFrame(root, text=" Organization Method ", padding=(10, 6))
    mode_frame.pack(fill=tk.X, padx=12, pady=4)
    widgets["mode_frame"] = mode_frame

    rb_fast = ttk.Radiobutton(
        mode_frame,
        text="🚀 Fast Mode (By Extension - Instant)",
        variable=mode_var,
        value="fast",
        command=lambda: on_mode_select()
    )
    rb_fast.pack(side=tk.LEFT, padx=10, pady=2)
    widgets["rb_fast"] = rb_fast

    rb_ai = ttk.Radiobutton(
        mode_frame,
        text="🧠 AI Mode (Ollama qwen3.5:2b - By Content)",
        variable=mode_var,
        value="ai",
        command=lambda: on_mode_select()
    )
    rb_ai.pack(side=tk.LEFT, padx=10, pady=2)
    widgets["rb_ai"] = rb_ai

    ai_badge = ttk.Label(mode_frame, textvariable=ai_status_text, font=("Segoe UI", 8, "bold"))
    ai_badge.pack(side=tk.RIGHT, padx=10, pady=2)
    widgets["ai_badge"] = ai_badge

    # 4. Önizleme Tablosu
    mid_frame = ttk.LabelFrame(root, text=" Preview Table ", padding=8)
    mid_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=4)
    widgets["mid_frame"] = mid_frame

    cols = ("name", "size", "category", "status")
    tree = ttk.Treeview(mid_frame, columns=cols, show="headings", selectmode="extended")
    tree.heading("name", text="File Name")
    tree.heading("size", text="Size")
    tree.heading("category", text="Target Folder")
    tree.heading("status", text="Status")

    tree.column("name", width=280, anchor=tk.W)
    tree.column("size", width=80, anchor=tk.E)
    tree.column("category", width=140, anchor=tk.W)
    tree.column("status", width=330, anchor=tk.W)

    scroll_y = ttk.Scrollbar(mid_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scroll_y.set)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    widgets["tree"] = tree

    # 5. İlerleme Çubuğu ve Durum Satırı
    prog_frame = ttk.Frame(root, padding=(12, 4))
    prog_frame.pack(fill=tk.X)
    progress_bar = ttk.Progressbar(prog_frame, orient=tk.HORIZONTAL, mode='determinate')
    progress_bar.pack(fill=tk.X, pady=2)
    status_label = ttk.Label(prog_frame, textvariable=status_msg_var, font=("Segoe UI", 9))
    status_label.pack(anchor=tk.W, pady=2)

    # 6. Düğmeler Paneli
    btn_frame = ttk.Frame(root, padding=12)
    btn_frame.pack(fill=tk.X)

    def set_ui_state(busy):
        nonlocal is_busy
        is_busy = busy
        state = tk.DISABLED if busy else tk.NORMAL
        btn_preview.config(state=state)
        btn_undo.config(state=state)
        rb_fast.config(state=state)
        rb_ai.config(state=state)
        lang_btn.config(state=state)
        theme_btn.config(state=state)
        if busy:
            btn_move.config(state=tk.DISABLED)

    def populate_tree_instant(plan):
        for row in tree.get_children():
            tree.delete(row)
        for idx, item in enumerate(plan):
            tree.insert("", tk.END, iid=str(idx), values=(
                item["name"],
                item["size_fmt"],
                item["target_category"],
                item["status"]
            ))

    # ==========================================================================
    # Otomatik Sistem Denetimi ve Mod Seçimi
    # ==========================================================================
    def run_hardware_check(silent=True, callback_when_ready=None):
        """Arka planda Ollama servis ve model denetimi yapar; gerekirse otomatik başlatır."""
        def worker():
            if not is_ollama_installed():
                root.after(0, lambda: ai_status_text.set(get_text("ai_badge_missing")))
                return

            if not is_ollama_port_open():
                root.after(0, lambda: ai_status_text.set(get_text("ai_badge_starting")))

            ok, reason, _ = ensure_ollama_ready(
                model_name="qwen3.5:2b",
                status_callback=lambda msg: root.after(0, lambda: status_msg_var.set(get_text(msg)))
            )

            def update_badge():
                if ok:
                    ai_status_text.set(get_text("ai_badge_ready"))
                    if callback_when_ready:
                        callback_when_ready(True, "")
                else:
                    if reason == "ollama_not_installed":
                        ai_status_text.set(get_text("ai_badge_missing"))
                    else:
                        ai_status_text.set("🟡 AI Off")
                    if callback_when_ready:
                        callback_when_ready(False, reason)

            root.after(0, update_badge)

        threading.Thread(target=worker, daemon=True).start()

    def on_mode_select():
        if is_busy:
            return
        if mode_var.get() == "ai":
            set_ui_state(True)
            status_msg_var.set(get_text("status_ai_checking"))
            progress_bar["mode"] = "indeterminate"
            progress_bar.start(12)

            def on_ready_result(ok, reason):
                progress_bar.stop()
                progress_bar["mode"] = "determinate"
                progress_bar["value"] = 0
                set_ui_state(False)
                if ok:
                    on_preview()
                else:
                    mode_var.set("fast")
                    if reason == "ollama_not_installed":
                        messagebox.showerror(
                            get_text("ollama_not_installed_title"),
                            get_text("ollama_not_installed_msg")
                        )
                    elif reason == "model_pull_failed":
                        messagebox.showwarning(
                            get_text("ollama_model_missing_title"),
                            get_text("ollama_model_missing_msg")
                        )
                    else:
                        messagebox.showwarning(
                            get_text("ollama_conn_err_title"),
                            get_text("ollama_conn_err_msg")
                        )
                    on_preview()

            run_hardware_check(silent=False, callback_when_ready=on_ready_result)
            return

        on_preview()

    def on_preview():
        if is_busy:
            return
        nonlocal current_plan
        src = source_var.get().strip()
        dst = target_var.get().strip()
        if not os.path.exists(src):
            messagebox.showerror("Error", get_text("err_source_not_found", path=src))
            return

        selected_mode = mode_var.get()

        base_plan = plan_moves(src, dst, use_ai=False, lang=current_lang)
        current_plan = base_plan
        populate_tree_instant(base_plan)

        move_count = sum(1 for it in base_plan if it.get("action") == "move")
        skip_count = len(base_plan) - move_count

        if selected_mode == "fast":
            progress_bar["value"] = 0
            if move_count > 0:
                btn_move.config(state=tk.NORMAL)
                status_msg_var.set(get_text("status_fast_ready", move_count=move_count, skip_count=skip_count))
            else:
                btn_move.config(state=tk.DISABLED)
                status_msg_var.set(get_text("status_no_files", skip_count=skip_count))
            return

        ai_candidates = [
            (idx, it) for idx, it in enumerate(base_plan)
            if it.get("action") == "move" and os.path.splitext(it["name"])[1].lower() in AI_PROCESSABLE_EXTENSIONS
        ]

        if not ai_candidates:
            if move_count > 0:
                btn_move.config(state=tk.NORMAL)
            status_msg_var.set(get_text("status_no_ai_files"))
            return

        set_ui_state(True)
        progress_bar["value"] = 0
        progress_bar["maximum"] = len(ai_candidates)

        def ai_worker():
            ok, reason, client = ensure_ollama_ready(
                model_name="qwen3.5:2b",
                status_callback=lambda msg: root.after(0, lambda: status_msg_var.set(get_text(msg)))
            )
            if not ok or not client:
                def on_error():
                    set_ui_state(False)
                    mode_var.set("fast")
                    status_msg_var.set(get_text("ollama_conn_err_msg"))
                    messagebox.showwarning(get_text("ollama_conn_err_title"), get_text("ollama_conn_err_msg"))
                root.after(0, on_error)
                return

            ai_categorized = 0
            for step, (row_id, item) in enumerate(ai_candidates, 1):
                def update_prog(s=step, name=item["name"]):
                    progress_bar["value"] = s
                    status_msg_var.set(get_text("status_ai_analyzing", cur=s, tot=len(ai_candidates), name=name))
                root.after(0, update_prog)

                ai_cat = infer_category_ai(item["path"], client, "qwen3.5:2b")
                if ai_cat:
                    item["target_category"] = ai_cat
                    item["target_dir"] = os.path.join(dst, ai_cat)
                    item["target_path"] = os.path.join(item["target_dir"], item["name"])
                    item["status"] = get_text("status_to_move_ai", cat=ai_cat)
                    ai_categorized += 1

                    def update_tree(r=str(row_id), it=item):
                        if tree.exists(r):
                            tree.item(r, values=(
                                it["name"],
                                it["size_fmt"],
                                it["target_category"],
                                it["status"]
                            ))
                    root.after(0, update_tree)

            def on_complete():
                set_ui_state(False)
                progress_bar["value"] = progress_bar["maximum"]
                if move_count > 0:
                    btn_move.config(state=tk.NORMAL)
                status_msg_var.set(get_text("status_ai_done", count=ai_categorized))
            root.after(0, on_complete)

        threading.Thread(target=ai_worker, daemon=True).start()

    def on_move():
        if is_busy or not current_plan:
            return

        to_move = [item for item in current_plan if item.get("action") == "move"]
        if not to_move:
            messagebox.showinfo("Info", get_text("info_no_files_to_move"))
            return

        dst = target_var.get().strip()
        mode_text = get_text("mode_text_ai") if mode_var.get() == "ai" else get_text("mode_text_fast")
        confirm = messagebox.askyesno(
            get_text("confirm_move_title"),
            get_text("confirm_move_msg", count=len(to_move), mode=mode_text, dest=dst),
            icon="question"
        )
        if not confirm:
            return

        set_ui_state(True)
        progress_bar["value"] = 0
        progress_bar["maximum"] = len(to_move)

        def worker():
            def prog_cb(current, total, filename):
                def update_ui():
                    progress_bar["value"] = current
                    status_msg_var.set(get_text("status_moving", cur=current, tot=total, name=filename))
                root.after(0, update_ui)

            res = execute_moves(current_plan, progress_callback=prog_cb)

            def done_ui():
                set_ui_state(False)
                progress_bar["value"] = progress_bar["maximum"]
                if res["success"]:
                    messagebox.showinfo(get_text("success_title"), get_text("success_move_msg", count=res['moved_count']))
                    status_msg_var.set(get_text("status_move_done", count=res['moved_count']))
                else:
                    err_msg = "\n".join(res["errors"][:5])
                    messagebox.showwarning("Warning", f"{res['moved_count']} moved.\nErrors:\n{err_msg}")
                    status_msg_var.set(get_text("status_move_warn", count=res['moved_count']))
                on_preview()

            root.after(0, done_ui)

        threading.Thread(target=worker, daemon=True).start()

    def on_undo():
        if is_busy:
            return
        set_ui_state(True)
        status_msg_var.set("Undoing last operation...")

        def worker():
            def prog_cb(current, total, filename):
                def update_ui():
                    status_msg_var.set(get_text("status_undoing", cur=current, tot=total, name=filename))
                root.after(0, update_ui)

            res = undo_last(progress_callback=prog_cb)

            def done_ui():
                set_ui_state(False)
                if res["success"]:
                    messagebox.showinfo(get_text("undo_success_title"), get_text("undo_success_msg", count=res['restored']))
                    status_msg_var.set(get_text("status_undo_done", count=res['restored']))
                else:
                    err_summary = "\n".join(res.get("errors", [])[:5])
                    messagebox.showwarning(get_text("undo_warn_title"), f"{res.get('message', '')}\nRestored: {res.get('restored', 0)}\nErrors:\n{err_summary}")
                    status_msg_var.set("Undo finished with warnings.")
                on_preview()

            root.after(0, done_ui)

        threading.Thread(target=worker, daemon=True).start()

    btn_preview = ttk.Button(btn_frame, text="Preview", command=on_preview, width=14)
    btn_preview.pack(side=tk.LEFT, padx=4)
    widgets["btn_preview"] = btn_preview

    btn_move = ttk.Button(btn_frame, text="Move", command=on_move, width=14, state=tk.DISABLED)
    btn_move.pack(side=tk.LEFT, padx=4)
    widgets["btn_move"] = btn_move

    btn_undo = ttk.Button(btn_frame, text="Undo Last Action", command=on_undo, width=18)
    btn_undo.pack(side=tk.LEFT, padx=4)
    widgets["btn_undo"] = btn_undo

    btn_close = ttk.Button(btn_frame, text="Close", command=root.destroy, width=12)
    btn_close.pack(side=tk.RIGHT, padx=4)
    widgets["btn_close"] = btn_close

    # Başlangıçta dil ve temayı uygula
    update_ui_language()
    apply_theme(current_theme)

    # Başlangıçta hızlı mod ile önizlemeyi hazırla
    root.after(100, on_preview)

    # Arka planda donanım / Ollama sağlık kontrolünü başlat ve hazır et
    root.after(500, lambda: run_hardware_check(silent=True))

    return root


if __name__ == '__main__':
    app = create_gui()
    app.mainloop()
