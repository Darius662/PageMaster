import os
import json
import re
import shutil
from collections import defaultdict

MANIFEST_FILE = "manifest.json"

def load_manifest():
    """Load the manifest of processed archives"""
    if os.path.exists(MANIFEST_FILE):
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"extracted": []}

def run(config):
    """Organize chapters using provided configuration"""
    EXTRACT_DIR = config["EXTRACT_DIR"]
    OUTPUT_DIR = config["OUTPUT_DIR"]
    
    # Load manifest to get list of extracted archives
    manifest = load_manifest()
    
    if not manifest["extracted"]:
        print("❌ No extracted archives found in manifest")
        return
    
    print(f"Found {len(manifest['extracted'])} archive(s) to organize\n")
    
    for archive_name in manifest["extracted"]:
        archive_path = os.path.join(EXTRACT_DIR, archive_name)
        archive_output_dir = os.path.join(OUTPUT_DIR, archive_name)
        JSON_PATH = os.path.join(archive_path, "index.json")
        
        os.makedirs(archive_output_dir, exist_ok=True)
        
        # Load metadata
        if not os.path.exists(JSON_PATH):
            print(f"⚠️  Skipping {archive_name}: JSON file not found at {JSON_PATH}")
            continue
        
        print(f"📚 Organizing {archive_name}...")
        
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        chapters = data["chapters"]
        
        # Group chapters by volume
        volumes = defaultdict(list)
        for ch_id, ch_data in chapters.items():
            volumes[ch_data["volume"]].append(ch_data)
        
        # Sort by chapter number
        for v in volumes.values():
            v.sort(key=lambda c: c["number"])
        
        images = sorted(os.listdir(archive_path))
        matched_images = set()
        
        for vol_num, ch_list in volumes.items():
            vol_dir = os.path.join(archive_output_dir, f"Volume {vol_num or 1}")
            os.makedirs(vol_dir, exist_ok=True)
        
            for ch_data in ch_list:
                # Extract chapter number from name field (e.g., "Ch. 14.5 - ..." -> "14.5")
                ch_full_name = ch_data.get("name", "").strip()
                match = re.search(r'(?:Ch\.?\s*|Chapter\s*)([0-9.]+)', ch_full_name)
                if match:
                    ch_num = match.group(1)
                else:
                    ch_num = ch_data["number"]
                
                ch_name = f"Chapter {ch_num}"
                ch_dir = os.path.join(vol_dir, ch_name)
                os.makedirs(ch_dir, exist_ok=True)
        
                pattern = ch_data["entries"].replace("\\\\", "\\")
                regex = re.compile(pattern)
        
                matched = [img for img in images if regex.match(os.path.splitext(img)[0])]
                for img in matched:
                    shutil.move(os.path.join(archive_path, img), os.path.join(ch_dir, img))
                    matched_images.add(img)
        
                print(f"  Moved {len(matched)} images → {ch_dir}")
        
        # Handle unmatched images - move them to Volume 1, Chapter 001
        unmatched = [img for img in images if img not in matched_images and not img.endswith('.json')]
        if unmatched:
            vol_dir = os.path.join(archive_output_dir, "Volume 1")
            ch_dir = os.path.join(vol_dir, "Chapter 001")
            os.makedirs(ch_dir, exist_ok=True)
            
            for img in unmatched:
                shutil.move(os.path.join(archive_path, img), os.path.join(ch_dir, img))
            
            print(f"  Moved {len(unmatched)} unmatched images → {ch_dir}")
        
        print(f"✅ {archive_name} organized.\n")
    
    print("✅ All archives organized complete.")
    
    # Clean up extracted folder
    print("\n🧹 Cleaning up extracted folder...")
    for item in os.listdir(EXTRACT_DIR):
        item_path = os.path.join(EXTRACT_DIR, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
            print(f"  Removed {item}/")
    print("✅ Cleanup complete.")

# Allow standalone execution
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--standalone":
        JSON_PATH = "index.json"
        EXTRACT_DIR = "extracted/Manga Title"
        OUTPUT_DIR = "organized/Manga Title"
        config = {
            "EXTRACT_DIR": "extracted",
            "OUTPUT_DIR": "organized"
        }
        run(config)
    else:
        print("This script should be run from main.py")
