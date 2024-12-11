import pandas as pd
import slugify
from pathlib import Path

csv_path = "~/handlo/data/hashtags/base.csv"
dir =  Path(f"~/handlo/data/hash_dir").expanduser()

df = pd.read_csv(csv_path)
for index, row in df.iterrows():
    print(index)
    file_name = slugify.slugify(row['label'])
    file_path = dir / f"{file_name}.txt"
    with file_path.open("w") as f:
        print(row["label"])
        f.write(row["label"])