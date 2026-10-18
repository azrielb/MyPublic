import json
import re
import urllib.request
import os

# הגדרת נתיב הקובץ במחשב שלך
file_path = r"C:\workspace\sdarim.json"
# הכתובת הרשמית של הקובץ המלא בגיטהאב של מסדירים
url = "https://raw.githubusercontent.com/bambiker/sdarim/refs/heads/main/sdarim.json"

def download_file_if_needed():
    """פונקציה שמורידה את הקובץ ישירות מהרשת אם הוא לא קיים"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    print("מוריד את קובץ התנ\"ך המלא ישירות מהשרת (זה עשוי לקחת כמה שניות)...")
    try:
        urllib.request.urlretrieve(url, file_path)
        print("ההורדה הסתיימה בהצלחה!")
    except Exception as e:
        print(f"שגיאה בהורדת הקובץ מהאינטרנט: {e}")

def remove_cantillation_and_punctuation(text):
    """פונקציה שמנקה ניקוד, טעמי מקרא וסימני פיסוק מהטקסט"""
    clean_text = re.sub(r'[\u0591-\u05C7]', '', text)
    clean_text = re.sub(r'[.,;:!\-?()\[\]"«»]', ' ', clean_text)
    return clean_text

def find_chapters_without_starting_vav():
    if not os.path.exists(file_path):
        download_file_if_needed()
        
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("נראה שהקובץ הקיים פגום או חסר. מנסה להוריד עותק נקי מחדש...")
        download_file_if_needed()
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
        except Exception as e:
            print(f"לא ניתן לקרוא את הקובץ גם לאחר הורדה מחדש: {e}")
            return

    print("מנתח את פרקי התנ\"ך, אנא המתן...")
    
    # התיקון החשוב: אם data הוא מילון, נשלוף מתוכו את הרשימה (בדרך כלל תחת המפתח 'values')
    verse_list = []
    if isinstance(data, dict):
        # מסדירים עשויים לשמור את הרשימה תחת מפתח כמו 'values' או דומה
        verse_list = data.get('values', [])
        if not verse_list:
            # אם אין מפתח values, נבדוק אם יש מפתח אחר שמכיל רשימה
            for val in data.values():
                if isinstance(val, list):
                    verse_list = val
                    break
    elif isinstance(data, list):
        verse_list = data

    chapters = {}
    
    for item in verse_list:
        if not isinstance(item, dict):
            continue
            
        book = item.get('bookchapter')
        chapter = item.get('chapter')
        text = item.get('versenonikud', '')
        
        if not book or not chapter:
            continue
            
        key = (book, chapter)
        if key not in chapters:
            chapters[key] = []
            
        clean_text = remove_cantillation_and_punctuation(text)
        words = clean_text.split()
        chapters[key].extend(words)

    found_chapters = []
    for (book, chapter), words in chapters.items():
        has_vav = False
        for word in words:
            if word.startswith('ו'):
                has_vav = True
                break
                
        if not has_vav:
            found_chapters.append(f"{book} פרק {chapter}")
    
    print("\n--- תוצאות הסריקה ---")
    if found_chapters:
        print(f"נמצאו {len(found_chapters)} פרקים שאין בהם אף מילה המתחילה באות ו':")
        max_print=10
        for ch in found_chapters:
            print(f"✨ {ch}")
            max_print-=1
            if max_print<1:
                return
    else:
        print("לא נמצא אף פרק בתנ\"ך שאין בו מילה המתחילה באות ו'.")

if __name__ == "__main__":
    find_chapters_without_starting_vav()
