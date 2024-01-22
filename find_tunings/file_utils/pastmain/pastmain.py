import glob

from find_tunings.file_utils.file_utils import convert_to_wsl_path
from find_tunings.file_utils.create_utils import create_fail_list_txt
from find_tunings.file_utils.remove_utils import remove_files
import json
import numpy as np


def worn_data():
    lists = glob.glob("./data/train/openpose_json/*.json")

    for x in lists:
        dirx = convert_to_wsl_path("C:\\잘못된 데이터")

        with open(x, "r") as t:

            pose_label = json.load(t)
            pose_data = pose_label['people'][0]['pose_keypoints_2d']

            pose_data = np.array(pose_data)
            pose_data = pose_data.reshape((-1, 3))[:, :2]

            named = x[x.rfind("/") + 1:x.rfind("_")]
            print(named)

            # uppder, hair
            if np.linalg.norm(pose_data[5] - pose_data[2]) <= 0.0:
                create_fail_list_txt(
                    dirx,
                    named,
                    "a_worn.txt",
                    True,
                    True
                )

            # bottom, bootom
            if np.linalg.norm(pose_data[12] - pose_data[9]) <= 0.0:
                create_fail_list_txt(
                    dirx,
                    named,
                    "b_worn.txt",
                    True,
                    True
                )


def removets():
    lists = []
    with open(convert_to_wsl_path("C:\\잘못된 데이터\\b_worn.txt"), "r") as l:
        for x in l:
            line = x.strip()
            lists.append(f"{line}_keypoints.json")
            lists.append(f"{line}_keypoints.json.Identifier")

        remove_files("./data/train/openpose_json", lists)


def delete_the_same_content():
    count = 0
    list_count = 0
    b_path = convert_to_wsl_path("C:\\잘못된 데이터\\b_worn.txt")
    t_path = convert_to_wsl_path("C:\\잘못된 데이터\\train_pairs_backup.txt")

    b_con = []
    with open(b_path, "r") as b_list:
        for b in b_list.readlines():
            b_con.append(b.strip() + ".jpg")

    new_lines = []
    with open(t_path, "r") as t_list:
        for t in t_list.readlines():
            list_count += 1
            if not any(b_txt in t for b_txt in b_con):
                new_lines.append(t)
                count += 1

    with open(convert_to_wsl_path("C:\\잘못된 데이터\\test.txt"), "w") as test:
        for new_line in new_lines:
            test.write(new_line)

    print(f"삭제된 데이터 :: {list_count - count}")
