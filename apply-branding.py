#!/usr/bin/env python3

# Assisted by Gemini
import json
import os
import shutil
import sys

# Configuration
BRANDING_DIR = "branding"
SOURCE_REPO_DIR = "podman-desktop"
MAPPING_FILE = os.path.join(BRANDING_DIR, "mapping.json")

def apply_branding():
    # 1. Validation: Check if mapping file exists
    if not os.path.exists(MAPPING_FILE):
        print(f"❌ Error: Mapping file not found at {MAPPING_FILE}")
        sys.exit(1)

    # 2. Validation: Check if submodule exists
    if not os.path.exists(SOURCE_REPO_DIR):
        print(f"❌ Error: Submodule directory '{SOURCE_REPO_DIR}' not found.")
        print("   Did you forget to 'git submodule update --init'?")
        sys.exit(1)

    print(f"📂 Loading mapping from {MAPPING_FILE}...")
    
    try:
        with open(MAPPING_FILE, 'r') as f:
            mapping = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Failed to parse JSON: {e}")
        sys.exit(1)

    success_count = 0
    error_count = 0

    # 3. Iterate and Replace
    for source_filename, target_rel_path in mapping.items():
        # Construct full paths
        source_path = os.path.join(BRANDING_DIR, source_filename)
        target_path = os.path.join(SOURCE_REPO_DIR, target_rel_path)

        # Sanity Check: Does the new image exist?
        if not os.path.exists(source_path):
            print(f"⚠️  Skipping: Source image missing: {source_filename}")
            error_count += 1
            continue

        # Sanity Check: Does the destination folder exist?
        # (We don't check for the file itself, in case we are adding a NEW file,
        # but the directory structure must likely exist).
        target_dir = os.path.dirname(target_path)
        if not os.path.exists(target_dir):
            print(f"⚠️  Skipping: Target directory does not exist for: {target_rel_path}")
            error_count += 1
            continue

        try:
            shutil.copy2(source_path, target_path)
            print(f"✅ Replaced: {target_rel_path}")
            success_count += 1
        except Exception as e:
            print(f"❌ Failed to copy {source_filename}: {e}")
            error_count += 1

    # 4. Final Report
    print("-" * 40)
    print(f"Branding Complete: {success_count} files replaced.")
    if error_count > 0:
        print(f"⚠️  There were {error_count} errors. Check logs above.")
        sys.exit(1) # Fail the build if images were missing
    else:
        print("🚀 All assets updated successfully.")

if __name__ == "__main__":
    apply_branding()
