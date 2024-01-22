from __future__ import annotations

import os.path

from tqdm import tqdm

from find_tunings.file_utils import file_utils, remove_utils

sep = os.sep


def extension_check(target_file: str, check_extend: str, add_try: bool = True) -> (bool, str):
    """
    'target_file'로 주어진 형태가 'check_extend'의 확장자인지 확인하며
    옵션에 따라 반환되는 값이 달라집니다.

    add_try = True = 만약 각각의 요소가 'target_file' == cat, 'check_extend' == .jpg 이라면
    반환값은 True, 'cat.jpg' 입니다.
    """
    if not target_file.endswith(check_extend) and add_try:
        return True, target_file + check_extend
    elif not target_file.endswith(check_extend):
        return False, target_file
    else:
        return True, target_file


def folder_create(directory):
    """폴더를 생성하는 메서드"""
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_directory_if_exists(*directories) -> list:
    """
    주어진 경로의 폴더가 존재하는지 확인하고 아닐 경우 에러를 반환 합니다.
    """
    valid_directories = []
    for directory in directories:
        if not os.path.exists(directory):
            raise FileNotFoundError("경로가 잘못 됐거나 찾지 못했습니다: ", f"{directory}")
        valid_directories.append(directory)
    return valid_directories


def list_files_only(directory) -> list:
    """지정된 디렉토리의 파일 목록만 반환합니다."""
    files = []
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file():
                files.append(entry.name)
    return files


def convert_to_wsl_path(win_dir: str) -> str:
    """
    윈도우의 절대 경로값을 wsl2에서 접근 가능한 형태로 변형 반환 합니다.
    'C:\\cat\\mackerel' -> '/mnt/c/cat/mackerel'
    """
    win_dir = win_dir.replace(":", "").replace("\\", "/")
    drive_name, rest_path = win_dir[0], win_dir[1:]
    return f"/mnt/{drive_name.lower()}{rest_path}"


def only_dir_as_list(parent_dir: str, not_empty_dir: bool = True) -> list:
    """
    'parent_dir'의 하위 항목들을 순회하고 폴더 형태의 리스만 반환합니다.
    'not_empty_folder' = True = 빈폴더를 반환하지 않습니다.
    """
    all_files_and_dirs = os.listdir(parent_dir)
    dirs = []
    for x in all_files_and_dirs:
        full_path = os.path.join(parent_dir, x)

        isdir = os.path.isdir(full_path)
        not_empty_dir = not_empty_dir and os.listdir(full_path)

        if not_empty_dir and isdir:
            dirs.append(x)
        elif isdir:
            dirs.append(x)

    return dirs


def only_files_as_list(parent_dir) -> list:
    """'parent_dir'의 하위 항목들을 순회하고 파일의 형태인 리스트만 반환 합니다."""
    all_files_and_dirs = os.listdir(parent_dir)
    dirs = []
    for x in all_files_and_dirs:
        full_path = os.path.join(parent_dir, x)
        if not os.path.isdir(full_path):
            dirs.append(x)
    return dirs


def not_exist_data_return(list_: list, data):
    """
    리스트에서 일치하지 않은 데이터를 추가하는 메서드 입니다.
    일반적인 상황에서는 일치하지 않은 데이터를 사용하지 않고자 할때는 Set으로 캐스팅 하는것이 적절하나
    예외적인 케이스를 위해 만들어졌습니다.
    """
    if data not in list_:
        return data.strip()


def paris_separation(paris: list) -> list:
    """
    각 리스트가 'x1.jpg, x2.jpg' 같은 형태일 경우 이를 분리해주는 메서드 입니다.
    """
    paris_separation_list = list()
    for p in paris:
        split = p.split(" ")
        for sp in split:
            paris_separation_list.append(sp.strip())
    return paris_separation_list


def find_sub_folder_inconsistent_data(datas: list | set, parent_dir_path: str, specific_pattern: bool = False) -> set:
    """
    'parent_dir_path' 로 주어진 부모 폴더의 하위 폴더를 순회하며
    'datas'로 주어진 파일이 존재 하지 않을 경우 해당 리스트를 반환하는 메서드 입니다.

    'specific_pattern' = True = 'datas'로 주어진 값이 정확히 일치할 경우 해당 값만 조회하여 순회를 줄입니다.
    'specific_pattern' = False = 'datas'로 주어진 값이 정확히 일치하지 않으나 해당 값으로 시작될 경우에 사용 됩니다.
    """
    inconsistent_data_set = set()
    sub_folder = only_dir_as_list(parent_dir_path, True)

    sub_progress = tqdm(sub_folder, desc="서브 폴더 진행률", position=0)
    with sub_progress as sub_progress:

        for sub in sub_progress:
            sub_dir_path = os.path.join(parent_dir_path, sub)
            files = only_files_as_list(sub_dir_path)

            desc = f"{sub} 폴더 내부의 파일들 확인중"
            datas_progress = tqdm(datas, desc=desc, leave=True, position=1)
            with datas_progress as datas:
                any_current_files = True

                for data in datas:
                    if data is None: continue
                    in_data = data in inconsistent_data_set

                    if not in_data:  # 성능을 위한 우선 체크 | # 서브 폴더에 파일 비교
                        if not specific_pattern:

                            any_current_files = (
                                any(file.startswith(data) for file in files)
                            )
                        else:
                            any_current_files = any(file == data for file in files)

                    if not any_current_files:
                        inconsistent_data_set.add(data)
    print("모든 작업 완료")
    return inconsistent_data_set


def read_text_file_as_list(dir_root, txt_name, separation: bool = False, remove_extends: bool = False) -> list:
    """
    텍스트 파일을 열고 리스트 형태로 반환 합니다.
    separation = True = file_utils.paris_separation()
    remove_extends = True = remove_utils.remove_extension()
    """
    txt_root = os.path.join(dir_root, txt_name)
    list_ = list()

    with open(txt_root, "r") as txt:
        while True:
            line = txt.readline()
            if not line: break
            if not line == "":
                list_.append(line.strip())

    assemble_list = list()
    if remove_extends:
        for ln in list_:
            check = separation or len(ln.split(" ")) > 1
            if check:
                line_assemble = ""
                parts = ln.split(" ")
                parts_no_extend = remove_utils.remove_extension(*parts)
                for p in parts_no_extend:
                    line_assemble += (p + " ")
                assemble_list.append(line_assemble)
            else:
                list_ = remove_utils.remove_extension(*list_)

    if len(assemble_list) > 0:
        list_ = assemble_list

    if separation:
        separation = file_utils.paris_separation(list_)
        list_ = list(separation)

    return list_
