import os
import zipfile
import shutil
import json

MANIFEST_FILE = "manifest.json"

def load_manifest():
    """Load the manifest of processed archives"""
    if os.path.exists(MANIFEST_FILE):
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"extracted": []}

def run(config):
    """Create CBZ files using provided configuration"""
    OUTPUT_DIR = config["OUTPUT_DIR"]
    
    # Load manifest to get list of extracted archives
    manifest = load_manifest()
    
    if not manifest["extracted"]:
        print("❌ No extracted archives found in manifest")
        return
    
    print(f"Found {len(manifest['extracted'])} archive(s) to process\n")
    
    for archive_name in manifest["extracted"]:
        ORG_DIR = os.path.join(OUTPUT_DIR, archive_name)
        
        if not os.path.exists(ORG_DIR):
            print(f"⚠️  Skipping {archive_name}: folder not found in OUTPUT_DIR")
            continue
        
        print(f"📦 Creating CBZ files for {archive_name}...")
        
        # Track which volume folders contain images (for cleanup)
        image_volume_folders = []
        
        # Walk through volumes and chapters
        for volume_name in sorted(os.listdir(ORG_DIR)):
            volume_path = os.path.join(ORG_DIR, volume_name)
            
            if not os.path.isdir(volume_path):
                continue
            
            # Process each chapter in the volume
            for chapter_name in sorted(os.listdir(volume_path)):
                chapter_path = os.path.join(volume_path, chapter_name)
                
                if not os.path.isdir(chapter_path):
                    continue
                
                files = [f for f in os.listdir(chapter_path) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
                
                if not files:
                    continue
                
                # Track this volume folder for cleanup
                if volume_path not in image_volume_folders:
                    image_volume_folders.append(volume_path)
                
                # Use chapter folder name directly (already in "Chapter X" format)
                cbz_name = f"{chapter_name}.cbz"
                
                cbz_path = os.path.join(volume_path, cbz_name)
                
                print(f"Creating {cbz_path}")
                with zipfile.ZipFile(cbz_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
                    for f in sorted(files):
                        z.write(os.path.join(chapter_path, f), arcname=f)
        
        print(f"✅ {archive_name} complete.\n")
        
        # Clean up image folders
        print("🧹 Cleaning up image folders...")
        for volume_path in image_volume_folders:
            for chapter_name in os.listdir(volume_path):
                chapter_path = os.path.join(volume_path, chapter_name)
                
                if os.path.isdir(chapter_path):
                    # Check if it's an image folder (not a .cbz file)
                    if not chapter_name.endswith(".cbz"):
                        shutil.rmtree(chapter_path)
                        print(f"  Removed {os.path.relpath(chapter_path, ORG_DIR)}/")
        
        print("✅ Cleanup complete.\n")
    
    print("✅ All archives processed.")

# Allow standalone execution
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--standalone":
        ORG_DIR = "organized/Manga Title"
        OUT_DIR = "cbz_output/Manga Title"
        config = {"OUTPUT_DIR": "organized"}
        run(config)
    else:
        print("This script should be run from main.py")
