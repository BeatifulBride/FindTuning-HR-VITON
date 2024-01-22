import gc
import json
import os.path
import random
import shutil
from itertools import combinations

import PIL.Image
import torch
import tqdm
from PIL import ImageDraw
from PIL import Image
from torchvision.transforms import transforms

import test_condition
import train_condition
from find_tunings.file_utils import converter_utils, file_utils, remove_utils, create_utils
from find_tunings.file_utils.file_utils import *
from find_tunings.file_utils.remove_utils import remove_arrangement_list, remove_extension

import numpy as np

data_dir = train_condition.data_root
dev_data_dir = "G:\\내 드라이브\\HR-VITON-FIND-TUNING\\hr-viton-find-tunings\\data\\zalando-hd-resized"


def wrong_paris_detection():
    true_paris_list = list()
    remove_extend_list = set()
    wrong_list = set()

    with open(os.path.join(dev_data_dir, 'train_pairs.txt'), 'r') as txt:
        paris_list = list()
        while True:
            line = txt.readline()
            if not line: break
            if not line == "":
                true_paris_list.append(line.strip())
                paris_list.append(line.strip())

        # 비교를 위해 확장자를 제거한것을 반환중
        separation = file_utils.paris_separation(paris_list)
        separation = remove_utils.remove_extension(*separation)
        for s in separation:
            remove_extend_list.add(s)

    wrong_list = (find_sub_folder_inconsistent_data(
        remove_extend_list, os.path.join(dev_data_dir, "train"), False
    ))

    x = remove_arrangement_list(true_paris_list, wrong_list, True)
    with open(os.path.join(dev_data_dir, 'test.txt'), 'w') as txt:
        for x in x:
            txt.write(x + "\n")


# 파일 이름 변경함수
def rename_files(imageparse_path, endswithname, replacename):
    # 해당 경로가 존재하는지 확인
    if not os.path.exists(imageparse_path):
        return "경로가 존재하지 않습니다."

    # 파일 이름 변경 과정
    for filename in os.listdir(imageparse_path):
        if filename.endswith(endswithname):
            # '.jpg' 확장자를 '_mask.jpg'로 변경
            new_name = filename.replace(endswithname, replacename)
            # 이전 및 새 파일의 전체 경로
            old_file = os.path.join(imageparse_path, filename)
            new_file = os.path.join(imageparse_path, new_name)
            # 파일 이름 변경
            os.rename(old_file, new_file)
            print(f"Renamed {old_file} to {new_file}")

    return "모든 파일의 이름이 성공적으로 변경되었습니다."


# train_paris.txt 작성 함수
def save_file_list_to_txt(imageparse_path, output_file):
    if not os.path.exists(imageparse_path):
        return "경로가 존재하지 않습니다."

    # 모든 파일 목록 가져오기
    files = os.listdir(imageparse_path)
    print(files)
    # 파일 목록 셔플
    shuffled_files = random.sample(files, len(files))

    with open(output_file, 'w') as f:
        for original, shuffled in zip(files, shuffled_files):
            f.write(f"{original} {shuffled}\n")

    return f"{output_file}에 파일 목록이 저장되었습니다."


def image_parse_v3_wrong():
    dir_ = file_utils.convert_to_wsl_path('D:\\Traing-Set\\train\\image-parse-v3')
    image_parse_v3_list = os.listdir(dir_)

    worn_list = list()
    for v3 in tqdm(image_parse_v3_list):
        im_parse_pil_big = Image.open(os.path.join(dir_, v3))
        im_parse_pil = transforms.Resize(192, interpolation=0)(im_parse_pil_big)
        parse = torch.from_numpy(np.array(im_parse_pil)).long()

        try:
            parse_map = torch.FloatTensor(20, 256, 192).zero_()
            parse_map = parse_map.scatter_(0, parse, 1.0)
        except RuntimeError:
            image_parse_v3_list.append(v3)

    with open(os.path.join(
            file_utils.convert_to_wsl_path('D:\\Traing-Set\\train'), 'dimension_error.txt'
    ), 'w') as txt:
        for worn in worn_list:
            txt.write(worn + "\n")


def converter_8bit():
    dir_ = file_utils.convert_to_wsl_path('D:\\Training-Set\\train\\image-parse-agnostic-v3.2')
    save_dir = file_utils.convert_to_wsl_path('D:\\Training-Set\\train\\image-parse-agnostic-v3.2')
    image_parse_v3_list = os.listdir(dir_)

    for v3 in tqdm(image_parse_v3_list):
        down_bit = Image.open(os.path.join(dir_, v3)).convert('P', palette=Image.ADAPTIVE, colors=256)
        down_bit.save(os.path.join(save_dir, v3))


def grasp_dimensions():
    dir_ = file_utils.convert_to_wsl_path('D:\\FindTuning\\HR-VITON\\data\\train\\image-parse-v3')
    save_dir = file_utils.convert_to_wsl_path('D:\\Training-Set\\train')
    image_parse_v3_list = os.listdir(dir_)

    channels = dict()
    for v3 in tqdm(image_parse_v3_list):
        image = Image.open(os.path.join(dir_, v3))
        x = image.mode
        channels[v3] = x

    with open(os.path.join(save_dir, "v3_channels2.txt"), 'w') as txt:
        for key, value in channels.items():
            txt.write(f"{key} : {value} \n")


def rm_end_with():
    root = os.path.join(convert_to_wsl_path("D:\\Training-Set\\train\\image-parse-v3"))
    file_list = os.listdir(root)

    for file in tqdm(file_list):
        if file.endswith('Zone.Identifier'):
            os.remove(os.path.join(root, file))


def img_dimensions():
    root = os.path.join(convert_to_wsl_path("D:\\FindTuning\\HR-VITON\\data\\train\\image-parse-v3"))
    imgs = os.listdir(root)

    dims = dict()
    for img in tqdm(imgs):
        image = Image.open(os.path.join(root, img))
        image_tensor = torch.tensor(np.array(image))
        num_dimensions = image_tensor.dim()
        dims[img] = num_dimensions

    with open(os.path.join(convert_to_wsl_path("D:\\Training-Set\\train"), "origin_v3_dim.txt"), "w") as txt:
        for key, value in dims.items():
            txt.write(f"{key} :: {value} \n")


def shape_chw_test():
    dir_ = file_utils.convert_to_wsl_path('D:\\FindTuning\\HR-VITON\\data\\train\\image-parse-v3')
    # dir_ = file_utils.convert_to_wsl_path('D:\\Training-Set\\train\\image-parse-v3')
    image_parse_v3_list = os.listdir(dir_)

    worn_list = list()
    for v3 in tqdm(image_parse_v3_list):
        im_parse_pil_big = Image.open(os.path.join(dir_, v3))
        im_parse_pil = transforms.Resize(192, interpolation=0)(im_parse_pil_big)
        parse = torch.from_numpy(np.array(im_parse_pil)[None]).long()

        parse_map = torch.FloatTensor(20, 256, 192)
        parse_map = parse_map.scatter_(0, parse, 1.0)

        c1, h1, w1 = parse_map.shape
        if c1 > 21:
            for row in range(h1):
                for col in range(w1):
                    print(c1, row, col)
                    idx = parse[0, row, col]
                    parse_map[idx, row, col] = 1.0
        else:
            print("20보다 큼")
            break

        print("다시 시작")
        print("다시 시작")
        print("다시 시작")


def test_dataset():
    pass


def v3_2_converter_8bit_n():
    pass


def gc():
    gc.collect()


def parse():
    path = os.path.join('/mnt/d/Training-Set/train/cloth')
    save = os.path.join('/mnt/d/Training-Set')

    files = file_utils.only_files_as_list(path)
    paris = ["{} {}".format(file1, file2) for file1, file2 in combinations(files, 2)]
    random.shuffle(paris)

    with open(os.path.join(save, "train_pairs.txt"), "w") as txt:
        for p in paris:
            txt.write(p + '\n')


def del_sub_folder():
    path = file_utils.convert_to_wsl_path('D:\\Test-Set\\test')
    folder_list = file_utils.only_dir_as_list(path)

    for folder in folder_list:
        folder_path = os.path.join(path, folder)
        files = os.listdir(folder_path)
        for file in files:
            os.remove(os.path.join(folder_path, file))


def copy_files_by_prefix(source_dir, target_dir, prefixes):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            # 파일 이름이 주어진 접두사 중 하나로 시작하는지 확인
            if any(file.startswith(prefix[:prefix.find('_')]) for prefix in prefixes):
                source_file_path = os.path.join(root, file)
                target_file_path = os.path.join(target_dir, os.path.relpath(source_file_path, source_dir))

                # 타겟 경로에 해당하는 폴더 생성 (이미 존재할 경우 생성하지 않음)
                os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

                # 파일 복사
                shutil.copy2(source_file_path, target_file_path)
                print(f"위치: {source_file_path[:source_file_path.rfind(os.path.pathsep)]} 에서 {target_file_path} 삭제")


def del_file_by_prefix(source_dir, prefix):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            # 파일 이름이 주어진 접두사 중 하나로 시작하는지 확인
            if file.startswith(prefix[:prefix.find('_')]):
                source_file_path = os.path.join(root, file)

                # 삭제
                os.remove(os.path.join(source_file_path))
                print(f"위치: {source_file_path[:source_file_path.rfind(os.path.pathsep)]} 에서 {file} 삭제")


if __name__ == '__main__':
    source_dir = '/mnt/d/Training-Set/test'
    target_dir = '/mnt/d/More_Details/test'
    prefixes = os.listdir(convert_to_wsl_path('D:\\More_Details\\xxxxxxxxxxxxxxx\\test_use'))
    rig = os.listdir('/mnt/d/Training-Set/train/agnositc_mask')

    parse()
