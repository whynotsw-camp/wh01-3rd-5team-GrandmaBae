from annoy import AnnoyIndex

# Annoy 인덱스 생성
def build_annoy_index(vectors, dimension, metric='angular'):
    id_to_product = {idx: {"product_id": item_id, "class_id": class_id} for idx, (item_id, vector, class_id) in enumerate(vectors)}
    annoy_index = AnnoyIndex(dimension, metric)
    for idx, (_, vector, _) in enumerate(vectors):
        annoy_index.add_item(idx, vector)
    annoy_index.build(10)
    return annoy_index, id_to_product

# Annoy 유사도 검색
def search_similar_vectors(annoy_index, id_to_product, query_vector, top_n=10):
    similar_indices, distances = annoy_index.get_nns_by_vector(query_vector, top_n, include_distances=True)
    results = []
    for idx, distance in zip(similar_indices, distances):
        if idx in id_to_product:
            item_id = id_to_product[idx]
            results.append({"product_id": item_id["product_id"], "distance": distance})
    return results
