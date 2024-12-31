import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from S3upload import upload_to_s3


class HomeShoppingCrawler:
    def __init__(self):
        """WebDriver 초기화"""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    def close(self):
        """WebDriver 종료"""
        if self.driver:
            self.driver.quit()

    def open_schedule_page(self, url):
        """
        홈쇼핑 스케줄 페이지 열기 및 버튼 클릭
        :param url: 홈쇼핑 메인 URL
        """
        self.driver.get(url)
        time.sleep(2)

        # 첫 번째 버튼 클릭
        first_button_xpath = '//*[@id="schedule_top"]/div[1]/nav/div[1]/ul/li[1]/button'
        self._click_button(first_button_xpath, "첫 번째 버튼 클릭 완료")

        # 두 번째 버튼 클릭
        second_button_xpath = '//*[@id="schedule_wrap"]/div[2]/div[1]/div[1]/ul/li[1]'
        self._click_button(second_button_xpath, "두 번째 버튼 클릭 완료")

    def open_tv_page(self, url):
        """
        TV 홈쇼핑 페이지 열기 및 버튼 클릭
        :param url: TV 홈쇼핑 메인 URL
        """
        self.driver.get(url)
        time.sleep(2)

        try:
            button_xpath = '//*[@id="search_result_tab_info_11_"]/div/ul/li[2]/a'
            self._click_button(button_xpath, "TV 버튼 클릭 완료")
        except Exception as e:
            print(f"TV 페이지 열기 오류: {e}")

    def _click_button(self, xpath, success_message):
        """
        XPath를 사용해 버튼 클릭
        :param xpath: 버튼 XPath
        :param success_message: 클릭 성공 메시지
        """
        button = self.driver.find_element("xpath", xpath)
        button.click()
        print(success_message)
        time.sleep(2)

    def extract_product_list(self):
        """
        상품 리스트 추출
        :return: BeautifulSoup 상품 리스트
        """
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        product_list = soup.find("ul", class_="schedule_list")
        if not product_list:
            print("상품 리스트를 찾을 수 없습니다.")
            return []
        return product_list.find_all("li")

    def extract_tv_product_list(self):
        """
        TV 상품 리스트 추출
        :return: BeautifulSoup 상품 리스트
        """
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        # 상품 목록을 포함하는 wrap_unitlist 영역 찾기
        product_container = soup.find("div", class_="wrap_unitlist")
        if not product_container:
            print("TV 상품 리스트를 찾을 수 없습니다.")
            return []
        return product_container.find_all("li")

    def extract_product_info(self, product):
        """
        상품 정보 추출
        :param product: BeautifulSoup 상품 객체
        :return: 상품 정보 딕셔너리
        """
        try:
            # 방송 시간 추출
            program_box = product.find("div", class_="program_box")
            broadcast_time = (
                program_box.find("p", class_="schedule").get_text(strip=True)
                if program_box
                else "방송시간 없음"
            )

            # 제품명 추출
            info_box = product.find("div", class_="info_box")
            product_name = (
                info_box.find("p", class_="item_name").get_text(strip=True)
                if info_box
                else "제품명 없음"
            )

            # 제품 가격 추출
            price_tag = product.find("p", class_="item_price")
            product_price = price_tag.get_text().strip() if price_tag else None

            # 제품 URL 및 ID 추출
            additional_info_box = product.find("div", class_="additional_info_box")
            product_id = None
            product_url = "URL 없음"
            if additional_info_box:
                button = additional_info_box.find("button", class_="alert")
                if button and "data-bdct-classnm" in button.attrs:
                    product_id = button["data-bdct-classnm"].split("_")[-1]
                    product_url = f"https://www.lotteimall.com/goods/viewGoodsDetail.lotte?goods_no={product_id}"

            return {
                "broadcast_time": broadcast_time,
                "product_name": product_name,
                "product_price": product_price,
                "product_id": product_id,
                "product_url": product_url,
            }
        except Exception as e:
            print(f"상품 정보 추출 오류: {e}")
            return None

    def extract_tv_product_info(self, product):
        """
        TV 상품 정보 추출
        :param product: BeautifulSoup 상품 객체
        :return: 상품 정보 딕셔너리
        """
        try:
            # 상품명 추출
            title_tag = product.find("p", class_="title")  # 클래스 수정 필요
            title = title_tag.get_text().strip() if title_tag else "상품명 없음"

            # 가격 추출
            price_tag = product.find("strong", class_="final")  # 클래스 수정 필요
            price = price_tag.get_text().strip() if price_tag else "가격 없음"

            # 제품 ID 추출
            id_tag = product.find("a", class_="zzim")  # 클래스 수정 필요
            product_id = id_tag['id'].split('_')[-1] if id_tag else "ID 없음"

            # 상품 URL 생성
            product_url = f"https://www.lotteimall.com/goods/viewGoodsDetail.lotte?goods_no={product_id}" if product_id != "ID 없음" else "URL 없음"

            return {
                "product_name": title,
                "product_price": price,
                "product_id": product_id,
                "product_url": product_url
            }
        except Exception as e:
            print(f"TV 상품 정보 추출 오류: {e}")
            return None

    def extract_image_urls(self, product_id, bucket_name, ymd):
        """
        대표 이미지 및 추가 이미지 URL 생성 후 S3에 업로드
        :param product_id: 상품 ID
        :param bucket_name: S3 버킷 이름
        :param ymd: 업로드 경로에 사용될 날짜 정보
        :return: 대표 이미지 URL, 추가 이미지 URL 리스트
        """
        try:
            dir_path = f"{product_id[-2:]}/{product_id[-4:-2]}/{product_id[-6:-4]}"
            base_url = f"https://image2.lotteimall.com/goods/{dir_path}/{product_id}"

            # 대표 이미지 확인
            product_image_url_L = f"{base_url}_L.jpg"
            product_image_url_L1 = f"{base_url}_L1.jpg"
            additional_image_urls = []

            if requests.head(product_image_url_L).status_code == 200:
                product_image_url = product_image_url_L
                start_index = 1  # 추가 이미지는 L1부터 시작
            elif requests.head(product_image_url_L1).status_code == 200:
                product_image_url = product_image_url_L1
                start_index = 2  # 추가 이미지는 L2부터 시작
            else:
                product_image_url = "이미지 없음"
                start_index = 1

            if product_image_url != "이미지 없음":
                object_name = f"{ymd}/{product_id}_0.jpg"
                upload_to_s3(product_image_url, bucket_name, object_name)

            # 추가 이미지 URL 생성
            for i in range(start_index, start_index+10):
                additional_url = f"{base_url}_L{i}.jpg"
                if requests.head(additional_url).status_code == 200:
                    additional_image_urls.append(additional_url)
                    object_name = f"{ymd}/{product_id}_{i}.jpg"
                    upload_to_s3(additional_url, bucket_name, object_name)
                else:
                    break  # 더 이상 추가 이미지가 없으면 중단

            return product_image_url, additional_image_urls,  start_index

        except Exception as e:
            print(f"이미지 URL 생성 오류: {e}")
            return "이미지 없음", []

    def extract_category(self, product_url):
        """
        개별 상품 페이지에서 카테고리 정보 추출
        :param product_url: 상품 URL
        :return: 카테고리 문자열
        """
        try:
            self.driver.get(product_url)
            time.sleep(2)  # 페이지 로딩 대기
            category_soup = BeautifulSoup(self.driver.page_source, "html.parser")

            # 카테고리 정보 추출
            category_tags = category_soup.find_all("a", class_="one")
            if category_tags:
                return " -> ".join([cat.get_text().strip() for cat in category_tags])
            else:
                return "카테고리 없음"
        except Exception as e:
            print(f"카테고리 추출 오류: {e}")
            return "카테고리 없음"


