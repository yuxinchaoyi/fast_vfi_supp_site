import os
import json

# --- Configuration ---
# Point to the 'videos' folder in the parent directory
base_video_dir = './static/videos' # <--- Path relative to the script location
datasets_to_scan = ['pexels', 'davis']
# Output directly to the current directory (fast_vfi_cli)
output_manifest_path = 'scenes_manifest.json' # <--- Output path relative to the script
# --- End Configuration ---

manifest_data = {"datasets": []}

print(f"Scanning base directory: {os.path.abspath(base_video_dir)}")

for dataset_name_lower in datasets_to_scan:
    dataset_dir = os.path.join(base_video_dir, dataset_name_lower)
    dataset_scenes = set() # Use a set to avoid duplicates

    print(f"  Scanning dataset: {dataset_name_lower} (Path: {dataset_dir})")

    if not os.path.isdir(dataset_dir):
        print(f"    Warning: Directory {dataset_dir} not found, skipping.")
        continue

    # Iterate through all items (files/folders) in the directory
    # Logic: Find scene names directly from GT files
    for item_name in os.listdir(dataset_dir):
        # Check if it's a GIF file following the GT naming convention (scene_name.gif)
        if item_name.endswith('.gif') and '_' not in item_name:
            scene_name = item_name[:-4] # Remove the .gif extension
            if scene_name: # Ensure scene name is not empty
                print(f"      Found scene (based on GT file): {scene_name}")
                dataset_scenes.add(scene_name)

    # Convert the set to a sorted list and add to manifest data
    manifest_data["datasets"].append({
        # Capitalize the first letter for display name
        "name": dataset_name_lower.capitalize(),
        "scenes": sorted(list(dataset_scenes))
    })

# No need to create the output directory as it's the current directory

# Write data to the JSON file
try:
    with open(output_manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest_data, f, ensure_ascii=False, indent=2)
    print(f"\nSuccessfully generated manifest file: {output_manifest_path}")
    print(json.dumps(manifest_data, indent=2)) # Print the generated JSON content
except IOError as e:
    print(f"\nError: Could not write manifest file {output_manifest_path}: {e}")
except Exception as e:
     print(f"\nAn unexpected error occurred while generating the manifest: {e}")
