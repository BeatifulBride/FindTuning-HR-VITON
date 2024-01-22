from __future__ import annotations
import os


def remove_extension(*txts):
    return [txt[:txt.rindex(".")] if "." in txt else txt for txt in txts]


def remove_files(target_dir: str, remove_data: str | list):
    dir_list = os.listdir(target_dir)
    not_detected = 0
    count = 0

    if not os.path.exists(target_dir):
        raise FileNotFoundError("폴더를 찾지 못했습니다.")

    for datum in remove_data:
        if datum not in dir_list:
            not_detected += 1

    for data in remove_data:
        try:
            os.remove(os.path.join(target_dir, data))
            count += 1
        except FileNotFoundError:
            pass

    print(f"삭제가 완료 되었습니다. 찾지 못한 데이터의 수는 {not_detected}개 입니다.")
    print(f"삭제한 데이터의 수는 {count}개 입니다.")


def delete_sub_folder_inconsistent_data(data: list, parent_dir: str, pattern: bool = True):
    """
    주어진 data와 부모 폴더 위치를 받아 하위 폴더를 방문하여 일치하는 데이터를 삭제하는 메서드
    개발 안됐습니다. 귀찮아.
    """
    pass


def remove_same_list(target_list: list, wrong_list: list):
    """단순 1차원 'target_list'에서 'wrong_list'를 제거후 반환하는 메서드 입니다."""
    wrong_set = set(wrong_list)
    return [item for item in target_list if item not in wrong_set]


def remove_arrangement_list(arrangement_list: list, wrong_list: list | set, extends: bool = True):
    """
    다차원 'arrangement_list'의 각 라인을 읽어 'wrong_list'와 동일한 값이 존재하면 삭제한 값을 반환하는 메서드 입니다.

    예시로 'arrangement_list'의 각 라인의 값이 'x1.jpg x2.jpg x3.jpg' 이며 "wrong_list"의 값이 'x2.jpg'가 존재하면
    해당 라인을 삭제가 삭제된 상태로 반환 됩니다.

    'extends' = True = 'arrangement_list'의 각 라인의 값들이 확장자를 가지고 있고,
    'wrong_list'는 확장자를 가지고 있지 않을경우 'arrangement_list'의 확장자를 제거 합니다.
    ex : 'arrangement_list' == 'cat.jpg dog.jpg' -> 'cat' 'dog' | 'wrong_list'
    """
    result = []
    wrong_set = set(wrong_list)
    for arrangement in arrangement_list:
        parts = []
        if extends:
            parts = remove_extension(*arrangement.split(" "))
        else:
            parts = arrangement.split(" ")

        if not any(part in wrong_set for part in parts):
            result.append(arrangement)
    return result
