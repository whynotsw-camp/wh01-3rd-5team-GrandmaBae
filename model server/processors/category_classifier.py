# 중분류 기준으로 상위 카테고리 지정 함수
def classify_main_category(sub_category, detail_category=None):
    """
    중분류와 세부 카테고리를 기반으로 상위 카테고리를 지정합니다.
    :param sub_category: 중분류 값
    :param detail_category: 세부 카테고리 값
    :return: 상위 카테고리 값 또는 None
    """
    # 카테고리 매핑
    category_mapping = {
        '빅사이즈': {
            '원피스': 'onepiece',
            '스커트/팬츠': 'bottom',
            '블라우스/셔츠': 'top',
            '티셔츠': 'top',
            '니트/가디건': 'outer',
            '자켓/점퍼/코트': 'outer'
        },
        'top': ['가디건', '티셔츠', '블라우스/셔츠', '니트', '니트/스웨터', '베스트/조끼', '셔츠/남방', '가디건/볼레로'],
        'bottom': ['스커트', '팬츠', '데님'],
        'outer': ['코트', '재킷', '점퍼', '가죽/모피'],
        'onepiece': ['원피스', '정장/세트/시즌아이템', '트레이닝복']
    }

    # 빅사이즈 특수 케이스 처리
    if sub_category == '빅사이즈':
        return category_mapping['빅사이즈'].get(detail_category, None)

    # 일반적인 중분류 처리
    for main_category, sub_categories in category_mapping.items():
        if isinstance(sub_categories, list) and sub_category in sub_categories:
            return main_category

    return '기타'  # 매핑되지 않는 값은 '기타'로 설정