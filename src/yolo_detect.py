from pathlib import Path

import pandas as pd
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

IMAGE_FOLDER = Path("data/raw/images")
image_files = list(IMAGE_FOLDER.rglob("*.jpg"))
print(f"Found {len(image_files)} images.")

results_list = []

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

output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "yolo_detections.csv"

df.to_csv(output_file, index=False)
print(f"Saved {len(df)} detections.")
print(f"Results saved to {output_file}")



