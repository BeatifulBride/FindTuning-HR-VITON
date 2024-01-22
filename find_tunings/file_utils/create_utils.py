from __future__ import annotations

from tqdm import tqdm

import os

from find_tunings.file_utils.file_utils import get_directory_if_exists, list_files_only, extension_check, \
    only_files_as_list


def create_list_txt(directory, save_directory=None, txt_name="list.txt", auto_path: bool = True):
    """파일 리스트를 텍스트화 하기 위한 메서드 입니다. 진행 상태를 체크 가능 합니다."""
    directory = get_directory_if_exists(directory)
    file_list = only_files_as_list(directory)

    save_directory = save_directory or directory

    if not txt_name.endswith(".txt"): txt_name += ".txt"

    with open(os.path.join(save_directory, txt_name), "w") as txt:
        with tqdm(file_list, "파일 작성중...") as tqdm_list:
            for file in tqdm_list:
                txt.write(file + "\n")

    print("파일 리스트 작성이 완료되었습니다.")
    print(f"파일 위치는 \"{os.path.join(save_directory, txt_name)}\" 입니다.")


def create_paris_list_txt(training_dir, validation_dir, save_dir, txt_name="paris.txt", auto_path: bool = True):
    training_dir, validation_dir, save_dir = (
        get_directory_if_exists(training_dir, validation_dir, save_dir)
    )

    training_list = list_files_only(training_dir)
    validation_list = list_files_only(validation_dir)

    if not txt_name.endswith(".txt"): txt_name += ".txt"

    # t = training_list | v = validation_list
    with open(os.path.join(save_dir, txt_name), "w") as txt:

        with tqdm(zip(training_list, validation_list), total=len(training_list)) as zips:
            for t, v in zips:
                txt.write((t + ", " + v + "\n"))

    print("파일 리스트 작성이 완료되었습니다.")
    print(f"파일 위치는 \"{save_dir}{txt_name}\" 입니다.")


def create_fail_list_txt(save_dir: str, write_data, txt_name="fail.txt",
                         check_already_exists: bool = True,
                         auto_path: bool = True):
    """실패 리스트를 작성하기 위한 메서드...지만 조금 손보면 그냥 데이터가 없을때 추가하는 메서드로도 활용가능."""
    save_dir = get_directory_if_exists(save_dir, auto_path)

    _, txt_name = extension_check(txt_name, ".txt", True)

    existing_data = None
    if check_already_exists and os.path.exists(os.path.join(save_dir, txt_name)):
        with open(os.path.join(save_dir, txt_name), "r") as txt:
            existing_data = txt.read().splitlines()

    with open(os.path.join(save_dir, txt_name), "a") as txt:
        if existing_data and write_data not in existing_data:
            txt.write(write_data + "\n")
        else:
            txt.write(write_data + "\n")
