# 3rd-template
whynotsw-camp 3rd-배할머니네 손주들 레포지토리입니다.

---------------------------------------

# 🛒 IPTV 홈쇼핑 - 실시간 AI 상품 추천 서비스 👍

---------------------------------------
## 🎯 프로젝트 개요
- **프로젝트명**: 실시간 AI 상품 추천 서비스
- **목표**: 시청 중인 TV 프로그램에서 **원하는 상품**을 즉시 구매할 수 있도록 IPTV 홈쇼핑 채널과 연계한 **고객 맞춤형 채널 추천 서비스** 구현
- **기간**: 2024년 11월 - 2024년 12월
<br>

## 📆 프로젝트 일정
- **분석 및 설계**: 2025년 1월 - 3월
- **개발**: 2025년 4월 - 8월
- **테스트 및 배포**: 2025년 9월 - 12월
<br>

## 😎 팀원 소개
<table style="width:100%; text-align:center; table-layout:fixed;">
  <colgroup>
    <!-- 전체 5열이므로 20%씩 -->
    <col style="width:20%;">
    <col style="width:20%;">
    <col style="width:20%;">
    <col style="width:20%;">
    <col style="width:20%;">
  </colgroup>
  <thead>
    <tr>
      <th>박시원</th>
      <th>이상민</th>
      <th>이지선</th>
      <th>임세연</th>
      <th>전서영</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>img</td>
      <td>img</td>
      <td>img</td>
      <td>img</td>
      <td>img</td>
    </tr>
    <tr>
      <td>PM<br>데이터 파이프라인</td>
      <td>DB구축<br>클라우드 관리</td>
      <td>AI<br>프론트엔드</td>
      <td>AI<br>백엔드</td>
      <td>AI<br>데이터 파이프라인</td>
    </tr>
    <tr>
      <td><a href="https://github.com/qkrcool" target="_blank">
          <img src="https://img.shields.io/badge/GitHub-Link-black?style=flat&logo=github&logoColor=white" />
        </a>
</td>
      <td><a href="https://github.com/strangem1n" target="_blank">
          <img src="https://img.shields.io/badge/GitHub-Link-black?style=flat&logo=github&logoColor=white" />
        </a></td>
      <td><a href="https://github.com/jisunclaralee" target="_blank">
          <img src="https://img.shields.io/badge/GitHub-Link-black?style=flat&logo=github&logoColor=white" />
        </a></td>
      <td><a href="https://github.com/saeyeonIm" target="_blank">
          <img src="https://img.shields.io/badge/GitHub-Link-black?style=flat&logo=github&logoColor=white" />
        </a></td>
      <td><a href="https://github.com/tjdud1199" target="_blank">
          <img src="https://img.shields.io/badge/GitHub-Link-black?style=flat&logo=github&logoColor=white" />
        </a></td>
    </tr>
  </tbody>
</table>
<br>

## 🛠 기술 스택
### Languages & Frameworks
- Programming Languages : <img src="https://img.shields.io/badge/python-%233776AB.svg?&style=flat&logo=python&logoColor=white" /> <img src="https://img.shields.io/badge/javascript-%23F7DF1E.svg?&style=flat&logo=javascript&logoColor=black" /> <img src="https://img.shields.io/badge/html5-%23E34F26.svg?&style=flat&logo=html5&logoColor=white" /> <img src="https://img.shields.io/badge/css3-%231572B6.svg?&style=flat&logo=css3&logoColor=white" />
- Web Frameworks : <img src="https://img.shields.io/badge/fastapi-%23009688.svg?&style=flat&logo=fastapi&logoColor=white" /> <img src="https://img.shields.io/badge/flask-%23000000.svg?&style=flat&logo=flask&logoColor=white" />

### Data Collection & Processing
- Libraries : <img src="https://img.shields.io/badge/BeautifulSoup-blue?style=flat" /> <img src="https://img.shields.io/badge/selenium-%2343B02A.svg?&style=flat&logo=selenium&logoColor=white" />

### Database & Infrastructure
- Database : <img src="https://img.shields.io/badge/postgresql-%23336791.svg?&style=flat&logo=postgresql&logoColor=white" />
- Cloud : <img src="https://img.shields.io/badge/amazon%20aws-%23232F3E.svg?&style=flat&logo=amazon%20aws&logoColor=white" /> <img src="https://img.shields.io/badge/Amazon%20S3-569A31?style=flat&logo=Amazon%20S3&logoColor=white"> <img src="https://img.shields.io/badge/Amazon%20EC2-FF9900?style=flat&logo=Amazon%20EC2&logoColor=white"> 

### AI / Machine Learning
- Object Detection : <img src="https://img.shields.io/badge/YOLO-00FFFF?style=flat" /> <img src="https://img.shields.io/badge/ResNet50_IBN_A-E34F26?style=flat" />
- Deep Learning Framework : <img src="https://img.shields.io/badge/pytorch-%23EE4C2C.svg?&style=flat&logo=pytorch&logoColor=white" />
<br>

---------------------------------------

<details><summary>요구사항 정의서
</summary>
  
## 1. 기능적 요구사항
- 사용자 관리 기능: 사용자는 로그인/회원가입할 수 있다.
- 데이터 처리 기능: 클라우드 시스템에서 빅데이터 분석을 처리할 수 있어야 한다.
- 결과 출력 기능: 분석 결과를 그래픽 및 표로 출력할 수 있어야 한다.

## 2. 비기능적 요구사항
- 응답 시간: 시스템은 2초 이내에 요청에 응답해야 한다.
- 성능: 시스템은 1,000명의 동시 사용자 처리가 가능해야 한다.
- 보안: 모든 데이터는 암호화되어 저장되어야 한다.
</details>

<details><summary>WBS
</summary>

## 1. 프로젝트 분석
- 요구사항 수집
- 시스템 설계
- 아키텍처 설계

## 2. 시스템 개발
- 백엔드 개발
- 프론트엔드 개발
- 데이터베이스 설계 및 구축

## 3. 테스트 및 배포
- 단위 테스트
- 통합 테스트
- 성능 테스트
- 배포 준비

</details>

<details><summary>모델 정의서
</summary>

## 1. 데이터 모델
- **사용자 테이블**
  - `user_id` (Primary Key)
  - `username`
  - `password`
  - `email`
  - `role` (admin, user)

- **분석 결과 테이블**
  - `result_id` (Primary Key)
  - `user_id` (Foreign Key)
  - `analysis_type`
  - `timestamp`
  - `result_data` (JSON)

## 2. 객체 모델
- **사용자 객체**
  - 속성: `username`, `password`, `email`
  - 메소드: `login()`, `logout()`, `register()`

</details>


<details><summary>성능 평가 결과서
</summary>

## 1. 테스트 환경
- **서버**: AWS EC2 c5.large 인스턴스
- **DB**: MySQL 8.0
- **네트워크**: 1Gbps

## 2. 테스트 결과
- **응답 시간**: 1초 이내
- **동시 사용자 처리**: 5,000명
- **CPU 사용률**: 70%
- **메모리 사용률**: 60%

## 3. 성능 개선 필요 사항
- 데이터 처리 성능 향상을 위한 캐시 적용
- 서버 성능 개선을 위한 리소스 스케일링 필요

</details>

-----------------------------------------

# 📑 최종 보고서

## 1. 프로젝트 개요
- **목표**: 클라우드 기반 빅데이터 분석 시스템 구축
- **기간**: 2025년 1월 - 2025년 12월

## 2. 주요 성과
- 시스템 구축 완료 및 안정적인 운영
- 10,000명 이상의 사용자가 동시 접속 가능한 클라우드 서비스 제공

## 3. 향후 개선 사항
- 사용자 인터페이스 개선
- 성능 최적화 및 리소스 효율성 향상

-----------------------------------------

# ✨ 회고

## 1. 잘된 점
- **협업**: 팀원 간의 협업이 원활하게 이루어졌으며, 주기적인 피드백 세션이 유효했다.
- **일정 관리**: 프로젝트 일정에 맞춰 개발이 진행되었고, 큰 지연 없이 배포를 완료했다.

## 2. 개선할 점
- **초기 요구사항 정의 부족**: 초기 요구사항이 부족하여 개발 도중 변경 사항이 많았다.
- **테스트 시간 부족**: 프로젝트 후반부에 테스트 시간이 부족했으며, 더 많은 시간을 할애해야 했다.

## 3. 교훈
- **명확한 요구사항 정의**: 초기 단계에서 요구사항을 명확히 정리하는 것이 중요하다.
- **적절한 테스트 계획 수립**: 충분한 테스트와 성능 점검을 통해 출시 전에 문제를 해결할 수 있어야 한다.

-------------------------------------------

## 📌 Git Convention
- **<타입>(<범위>): <설명>**

### 타입(Type)

| 타입       | 설명                                                                 |
|------------|----------------------------------------------------------------------|
| `feat`     | 새로운 기능 추가                                                    |
| `fix`      | 버그 수정                                                           |
| `docs`     | 문서 변경 (예: README 수정)                                         |
| `style`    | 코드 스타일 변경 (포맷팅, 세미콜론 누락 등, 기능 변경 없음)         |
| `refactor` | 코드 리팩토링 (기능 추가나 버그 수정이 아닌 코드 구조 개선)         |
| `perf`     | 성능 개선                                                           |
| `test`     | 테스트 코드 추가 또는 수정                                          |
| `chore`    | 빌드 프로세스 또는 보조 도구 변경 (예: 패키지 매니저 설정 등)       |
