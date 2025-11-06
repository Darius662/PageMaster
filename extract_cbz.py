import os
import zipfile
import json

MANIFEST_FILE = "manifest.json"

def load_manifest():
    """Load the manifest of processed archives"""
    if os.path.exists(MANIFEST_FILE):
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"extracted": []}

def save_manifest(manifest):
    """Save the manifest of processed archives"""
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

def run(config):
    """Extract CBZ files using provided configuration"""
    SOURCE_DIR = config["SOURCE_DIR"]
    EXTRACT_DIR = config["EXTRACT_DIR"]
    
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ SOURCE_DIR does not exist: {SOURCE_DIR}")
        return
    
    if not os.path.isdir(SOURCE_DIR):
        print(f"❌ SOURCE_DIR must be a directory, not a file: {SOURCE_DIR}")
        return
    
    os.makedirs(EXTRACT_DIR, exist_ok=True)
    
    cbz_files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith(".cbz")]
    if not cbz_files:
        print(f"⚠️  No CBZ files found in {SOURCE_DIR}")
        return
    
    manifest = load_manifest()
    
    for cbz in cbz_files:
        title = os.path.splitext(cbz)[0]
        outdir = os.path.join(EXTRACT_DIR, title)
        if os.path.exists(outdir):
            print(f"Skipping {cbz} (already extracted)")
            continue
    
        os.makedirs(outdir, exist_ok=True)
        print(f"Extracting {cbz} → {outdir}")
        try:
            with zipfile.ZipFile(os.path.join(SOURCE_DIR, cbz), "r") as z:
                z.extractall(outdir)
            
            # Add to manifest
            if title not in manifest["extracted"]:
                manifest["extracted"].append(title)
        except zipfile.BadZipFile as e:
            print(f"❌ Error extracting {cbz}: {e}")
            print(f"   The CBZ file may be corrupted. Skipping...")
            continue
        except Exception as e:
            print(f"❌ Unexpected error extracting {cbz}: {e}")
            continue
    
    # Save updated manifest
    save_manifest(manifest)
    print("✅ Extraction complete.")

# Allow standalone execution
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--standalone":
        SOURCE_DIR = "Manga"
        EXTRACT_DIR = "extracted"
        config = {"SOURCE_DIR": SOURCE_DIR, "EXTRACT_DIR": EXTRACT_DIR}
        run(config)
    else:
        print("This script should be run from main.py")
