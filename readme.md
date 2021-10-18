# Interactive Fashion Recommendation Dataset

A new interactive dataset for fashion recommendation tasks.

## Introduction
This dataset is build upon Polyvore dataset. Concerning of the possible copyright issue, we provide a script to generate the dataset with modifying the original data.

![](https://github.com/fang2hou/polyvore-interactive/raw/doc/workflow.svg)

## Preparation

1. Python 3.5+ with `pandas`, `tqdm`
2. Polyvore dataset [[original repo]](https://github.com/xthan/polyvore-dataset) 
   - [dataset](https://raw.githubusercontent.com/xthan/polyvore-dataset/master/polyvore.tar.gz) ~ 8 MB
   - [images](https://drive.google.com/file/d/0B4Eo9mft9jwoNm5WR3ltVkJWX0k/view?resourcekey=0-U-30d1POF7IlnAE5bzOzPA) ~ 13GB
   - Gather the above two parts into a directory:
      ```
      polyvore
      ├─images
      │  ├─123456(outfit id)
      │  └─...
      ├─test_no_dup.json
      ├─train_no_dup.json
      └─valid_no_dup.json

      ```   

## Usage

Use `python scripts/generate.py -h` to check the help message anytime.

```
usage: generate.py [-h] --polyvore POLYVORE [--record RECORD] [--target TARGET] [--move MOVE]
                   [--override_category OVERRIDE_CATEGORY]

optional arguments:
  -h, --help            show this help message and exit
  --polyvore POLYVORE   The path of Polyvore dataset
  --record RECORD       The path of interactive dataset id record
  --target TARGET       The path where the generated dataset saves
  --move MOVE           Use "move" rather than "copy" operation to the images in Polyvore dataset
  --override_category OVERRIDE_CATEGORY
                        Set true to sort the categories into 7 main groups
```

We also provide example file in `generate.sh.example`(for Linux & macOS) and `generate.bat.example` (for Windows NT). Before running the shell / batch file, do not forget to remove the `.example` extension from the file name and add your python environment commands.

## Citation
Feel free to cite our paper of this dataset:

```
bibtex code

```

