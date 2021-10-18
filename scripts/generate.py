from pathlib import Path
import argparse
import json
import pandas as pd
from tqdm import tqdm
import shutil

# args
parser = argparse.ArgumentParser()
parser.add_argument("--polyvore", type=str, required=True,
                    help="The path of Polyvore dataset")
parser.add_argument("--record", type=str, default="./record",
                    help='The path of interactive dataset id record')
parser.add_argument("--target", type=str, default="./polyvore-interactive",
                    help='The path where the generated dataset saves')
parser.add_argument("--move", type=bool, default=False,
                    help='Use "move" rather than "copy" operation to the images in the Polyvore dataset')
parser.add_argument("--override_category", type=bool, default=False,
                    help="Set true to sort the categories into 7 main groups")
args = parser.parse_args()

print(args)

# ----------------------------------------------------------------
# Check
# ----------------------------------------------------------------
# Polyvore dataset check
polyvore_dir = Path(args.polyvore)

polyvore_check_list = [
    "test_no_dup.json",
    "train_no_dup.json",
    "valid_no_dup.json",
    "images"
]

for item in polyvore_check_list:
    _item = polyvore_dir / item
    if not _item.exists():
        raise FileNotFoundError(f"'{item}' is not found in the polyvore directory.")

# Record check
record_dir = Path(args.record)

record_check_list = [
    "dataset.json",
    "category_table.csv"
]

for item in record_check_list:
    _item = record_dir / item
    if not _item.exists():
        raise FileNotFoundError(f"'{item}' is not found in the record directory.")

# Target initialization
target_dir = Path(args.target)
if target_dir.exists():
    shutil.rmtree(target_dir)
target_dir.mkdir()

target_image_dir = target_dir / "images"
target_image_dir.mkdir()

# ----------------------------------------------------------------
# Load Polyvore dataset
# ----------------------------------------------------------------
# image
image_dir = polyvore_dir / "images"

# category table
category_table = pd.read_csv(record_dir / "category_table.csv")

# outfit
original_outfits = dict()


def parse_outfit_data(path):
    with open(path, "r") as f:
        _data = json.load(f)

    data = dict()
    for outfit in _data:
        data[outfit["set_id"]] = outfit
        # cleanup
        del data[outfit["set_id"]]["set_url"]
        del data[outfit["set_id"]]["image"]
        for item in data[outfit["set_id"]]["items"]:
            del item["image"]
            del item["index"]

            if args.override_category:
                item["category"] = category_table[category_table["number"] == item["categoryid"]].group.item()
                del item["categoryid"]

    return data


original_outfits.update(parse_outfit_data(polyvore_dir / "test_no_dup.json"))
original_outfits.update(parse_outfit_data(polyvore_dir / "train_no_dup.json"))
original_outfits.update(parse_outfit_data(polyvore_dir / "valid_no_dup.json"))

# ----------------------------------------------------------------
# Generate
# ----------------------------------------------------------------
with open(record_dir / "dataset.json", "r") as f:
    record_data = json.load(f)

rich = {}

for question_set in tqdm(record_data):
    for question in question_set["questions"]:
        for item_id in question:
            if item_id in rich:
                continue

            [_outfit_id, _item_index] = item_id.split("_")

            _item_index = int(_item_index) - 1

            # image
            _image = image_dir / _outfit_id / (str(_item_index) + ".jpg")
            if _image.exists():
                if args.move:
                    shutil.move(_image, target_image_dir / (item_id + ".jpg"))
                else:
                    shutil.copy(_image, target_image_dir / (item_id + ".jpg"))
            else:
                raise FileNotFoundError("Image not found.")

            # text
            rich[item_id] = original_outfits[_outfit_id]["items"][_item_index]

with open(target_dir / "rich.json", "r") as f:
    json.dump(rich, f)
