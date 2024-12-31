import psycopg2
from psycopg2 import sql, extras
import numpy as np
from config.config import DATABASE_CONFIG

class DatabaseManager:
    def __init__(self, db_config=DATABASE_CONFIG):
        self.db_config = db_config

    def __enter__(self):
        """
        컨텍스트 매니저 시작 시 자동으로 연결
        """
        self.conn = psycopg2.connect(**self.db_config)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        컨텍스트 매니저 종료 시 연결 닫기
        """
        self.cursor.close()
        self.conn.close()

    def fetch_vectors(self):
        """
        PostgreSQL에서 벡터 데이터를 조회
        :return: [(product_id, vector_data), ...]
        """
        try:
            query = query = """
                SELECT 
                    vector_info.product_id, 
                    vector_info.vec_data, 
                    live_product_info.product_category AS class_id
                FROM 
                    vector_info
                JOIN 
                    live_product_info 
                ON 
                    vector_info.product_id = live_product_info.product_id
            """
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            vectors = [(row[0], np.array(row[1], dtype=np.float32), row[2]) for row in rows]
            return vectors
        except Exception as e:
            print(f"벡터 데이터 조회 실패: {e}")
            return []

    def insert_live_product_info(self, product):
        """
        live_product_info 테이블에 데이터 삽입 또는 업데이트
        :param product: {'product_id': str, 'image_vectors': list}
        """
        try:
            query = """
            INSERT INTO live_product_info (
                product_id, broadcast_time, product_name, product_price, webpage_url, product_category
             ) VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (product_id) DO UPDATE SET
                broadcast_time = EXCLUDED.broadcast_time,
                product_name = EXCLUDED.product_name,
                product_price = EXCLUDED.product_price,
                webpage_url = EXCLUDED.webpage_url,
                product_category = EXCLUDED.product_category;
            """
            self.cursor.execute(query, (
                    product['product_id'],
                    product['broadcast_time'],
                    product['product_name'],
                    product['product_price'],
                    product['product_url'],
                    product['main_category']
            ))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"live_product_info 삽입 실패: {e}")

    def insert_tv_product_info(self, product):
        """
        tv_product_info 테이블에 데이터 삽입 또는 업데이트
        :param product: {'product_id': str, 'image_vectors': list}
        """
        try:
            query = """
            INSERT INTO tv_product_info (
                tv_id, tv_name, tv_category, tv_price, webpage_url
             ) VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (tv_id) DO UPDATE SET
                tv_name = EXCLUDED.tv_name,
                tv_category = EXCLUDED.tv_category,
                tv_price = EXCLUDED.tv_price,
                webpage_url = EXCLUDED.webpage_url;
            """
            self.cursor.execute(query, (
                product['product_id'],
                product['product_name'],
                product['main_category'],
                product['product_price'],
                product['product_url']
            ))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"tv_product_info 삽입 실패: {e}")


    def insert_data(self, table_name, data):
        """
        임의의 테이블에 데이터 삽입
        :param table_name: 테이블 이름
        :param data: 딕셔너리 형태의 데이터
        """
        try:
            columns = data.keys()
            values = [data[column] for column in columns]

            query = sql.SQL("""
                INSERT INTO {table} ({fields})
                VALUES ({values})
                ON CONFLICT DO NOTHING
            """).format(
                table=sql.Identifier(table_name),
                fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
                values=sql.SQL(', ').join(sql.Placeholder() * len(values))
            )

            self.cursor.execute(query, values)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"{table_name} 테이블에 데이터 삽입 실패: {e}")

    def insert_vectors(self, vec_id: object, product_id: object, product_type: object, vec_data: object, s3_url: object, sequence_num: object) -> object:
        """
        URLs 테이블에 데이터 삽입
        :param product_id: 제품 ID
        :param product_type: 제품 유형 ('live', 'tv' 등)
        :param url_vec_data: URL 벡터 데이터 (리스트 형태)
        :param sequence_num: 시퀀스 번호
        """
        try:
            if isinstance(vec_data, np.ndarray):
                vec_data = vec_data.tolist()

            query = """
            INSERT INTO vector_info (
                vec_id, product_id, product_type, vec_data, s3_url, sequence_num
            ) VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
            """
            self.cursor.execute(query, (
                vec_id,
                product_id,
                product_type,
                vec_data, # 리스트 형태 그대로 전달
                s3_url,
                str(sequence_num)  # 시퀀스 번호를 문자열로 변환
            ))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"URLs 테이블에 데이터 삽입 실패: {e}")