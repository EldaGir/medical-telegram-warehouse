from pathlib import Path

import pandas as pd
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

IMAGE_FOLDER = Path("data/raw/images")
image_files = list(IMAGE_FOLDER.rglob("*.jpg"))
print(f"Found {len(image_files)} images.")

results_list = []

PRODUCT_CLASSES = {
    "bottle",
    "cup",
    "bowl",
    "box",
}

for i, image_path in enumerate(image_files, start=1):
    print(f"[{i}/{len(image_files)}] Processing {image_path.name}...")
    results = model(image_path, verbose=False)

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            confidence = float(box.conf[0])

            results_list.append({
                "message_id": int(image_path.stem),
                "channel_name": image_path.parent.name,
                "detected_class": class_name,
                "confidence_score": confidence,
            })

df = pd.DataFrame(results_list)

grouped = (
    df.groupby(["message_id", "channel_name"])
      .agg({
        "detected_class": lambda x: list(set(x)),
        "confidence_score": "max"
      })
      .reset_index()
)

def classify_image(objects):
    has_person = "person" in objects
    has_product = any(obj in PRODUCT_CLASSES for obj in objects)

    if has_person and has_product:
        return "promotional"

    elif has_product:
        return "product_display"

    elif has_person:
        return "lifestyle"

    else:
        return "other"

grouped["image_category"] = grouped["detected_class"].apply(classify_image)

output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "yolo_detections.csv"

grouped.to_csv(output_file, index=False)
print(f"Saved {len(grouped)} classified images.")
print(f"Results saved to {output_file}")



