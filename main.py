import os
import json
import sys

CONFIG_FILE = "config.json"
MANIFEST_FILE = "manifest.json"

def load_config():
    """Load configuration from config.json"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_config(config):
    """Save configuration to config.json"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    print(f"✅ Configuration saved to {CONFIG_FILE}")

def clear_manifest():
    """Clear the manifest file"""
    if os.path.exists(MANIFEST_FILE):
        os.remove(MANIFEST_FILE)
        print(f"🧹 Manifest cleared")

def setup_config():
    """Interactive configuration setup"""
    print("\n" + "="*50)
    print("PAGEMASTER - Configuration Setup")
    print("="*50)
    
    config = load_config() or {}
    
    print("\nEnter the following paths (or press Enter to keep existing values):")
    print("Note: SOURCE_DIR should be a DIRECTORY containing .cbz files\n")
    
    # SOURCE_DIR
    default_source = config.get("SOURCE_DIR", "Manga")
    source_dir = input(f"SOURCE_DIR (directory with CBZ files) [{default_source}]: ").strip()
    config["SOURCE_DIR"] = source_dir if source_dir else default_source
    
    # EXTRACT_DIR
    default_extract = config.get("EXTRACT_DIR", "extracted")
    extract_dir = input(f"EXTRACT_DIR (where to extract images) [{default_extract}]: ").strip()
    config["EXTRACT_DIR"] = extract_dir if extract_dir else default_extract
    
    # OUTPUT_DIR
    default_output = config.get("OUTPUT_DIR", "organized")
    output_dir = input(f"OUTPUT_DIR (where to organize chapters) [{default_output}]: ").strip()
    config["OUTPUT_DIR"] = output_dir if output_dir else default_output
    
    save_config(config)
    return config

def display_menu(config):
    """Display main menu"""
    print("\n" + "="*50)
    print("PAGEMASTER - Main Menu")
    print("="*50)
    print(f"\nCurrent Configuration:")
    print(f"  SOURCE_DIR:  {config['SOURCE_DIR']}")
    print(f"  EXTRACT_DIR: {config['EXTRACT_DIR']}")
    print(f"  OUTPUT_DIR:  {config['OUTPUT_DIR']}")
    print("\nOptions:")
    print("  1. Extract CBZ files")
    print("  2. Organize chapters")
    print("  3. Create CBZ files")
    print("  4. Reconfigure paths")
    print("  5. Exit")
    print("-"*50)

def run_extract_cbz(config):
    """Run extract_cbz.py with config"""
    print("\n🔄 Running extract_cbz.py...")
    import extract_cbz
    extract_cbz.run(config)

def run_organize_chapters(config):
    """Run organize_chapters.py with config"""
    print("\n🔄 Running organize_chapters.py...")
    import organize_chapters
    organize_chapters.run(config)

def run_create_cbz(config):
    """Run create_cbz.py with config"""
    print("\n🔄 Running create_cbz.py...")
    import create_cbz
    create_cbz.run(config)

def main():
    """Main menu loop"""
    config = load_config()
    
    if not config:
        print("No configuration found. Running setup...\n")
        config = setup_config()
    
    while True:
        display_menu(config)
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            run_extract_cbz(config)
        elif choice == "2":
            run_organize_chapters(config)
        elif choice == "3":
            run_create_cbz(config)
        elif choice == "4":
            config = setup_config()
        elif choice == "5":
            print("\n👋 Goodbye!")
            clear_manifest()
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
