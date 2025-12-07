# 서버리스 컴퓨팅을 활용한 리뷰 데이터 처리 파이프라인 구축

[English version](https://www.notion.so/English-version-2bbc4f4d02878103ac28fdc1618e610d?pvs=21)

## 개요

- 고객 리뷰 데이터를 효과적으로 처리하는 서버리스 컴퓨팅 파이프라인을 AWS 서비스를 활용해 설계하고 구현한다.
- 이벤트 기반 데이터 처리의 기본 개념을 학습하고, 퍼블릭 클라우드 플랫폼(AWS)의 다양한 서버리스 관련 서비스를 통합하여 실제 애플리케이션과 유사한 시스템을 구축하는 것을 목표로 한다.

## 구현 항목

### **1. API Gateway 생성 및 구성**

- API 종류: Rest API
- API 이름: `ReviewProcessingAPI-{student number}`
    - e.g., `ReviewProcessingAPI-2026320001`
- 리소스: `/reviews`
- 메서드: HTTP `POST` 메서드 생성 및 Lambda 함수와 통합
- 배포: API Gateway를 `prod` 스테이지로 배포
- 엔드포인트 URL: 배포 후 생성된 엔드포인트 URL을 활용

---

### 2. docker 컨테이너 생성 및 AWS ECR에 이미지 업로드

- AWS ECR에 레포지토리를 생성
    - AWS ECR은 AWS에서 운영하는 컨테이너 레지스트리
    - CLI에서 ECR 레포지토리를 생성하기 위해서 AWS CLI 설치 및 로그인 필요
        - https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
    - 아래 명령어에서 `--repository-name` 의 값을 변경하고 실행 시 레포지토리 생성 가능
        - 명령어 실행 시 나오는 `repositoryURI` 를 복사해둘 것
            - e.g., `12345678.dkr.ecr.us-east-1.amazonaws.com/review-processing-2026320001`
        
        ```yaml
        aws ecr create-repository \
            --repository-name review-processing-{student number} \
            --region us-east-1 \
            --image-scanning-configuration scanOnPush=true
        ```
        
- 아래 명령어에서 `{repositoryURI}` 수정하여 실행 시 docker cli에서 AWS ECR 로그인 가능
    - `aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin {repositoryURI}`
- 제공된 `lambda_function.py` 과 필요한 라이브러리를 포함하여 `Dockerfile` 작성
- `Dockerfile` 을 사용하여 이미지 빌드
- 아래 명령어를 사용하여 이미지 태그 및 푸시
    - `docker tag {로컬이미지명} {repositoryURI}:{tag}`
    - `docker push {repositoryURI}:{tag}`

---

### **3. Lambda 함수 설정**

- Lambda 함수 이름: `review-processing-{student number}`.
- ‘컨테이너 이미지’ 옵션 사용하여 ECR 이미지 등록후 사용
    - `latest` 태그는 컨테이너 이미지가 아니라 Image index이므로, **`latest` 바로 아래에 있는 태그 선택**
- 아키텍처: docker engine으로 이미지를 빌드한 컴퓨터 아키텍처에 맞게 선택
    - e.g., Apple Silicon MacBook 시리즈는 arm64 선택
- 실행 역할: 명세를 확인 후 필요한 역할을 부여할 것
- 구성 - 환경변수 관련
    - `lambda_function.py` 에는 환경 변수로 설정되어 있는 값들이 존재
    - 확인 후 **알맞은 환경 변수 값을 입력**할 것

---

### **4. DynamoDB에 데이터 저장**:

- 분석된 리뷰 데이터를 DynamoDB 테이블에 저장
- DynamoDB 테이블 스키마(schema):
    - 테이블 이름: `reviews-{student number}`
        - e.g., reviews-2026320001
    - **Partition Key**: `user_name` (string)
    - **Sort Key**: `timestamp` (string)
- 저장 데이터 예시
    
    ```json
    {
        "user_name": "Patricia Stewart",
        "review": "The tool is fantastic. Far despite visit mind computer prevent.",
        "sentiment": "Positive",
        "polarity_score": "0.25"
        "timestamp": "2025-11-28T11:16:31.363902"
    }
    ```
    

---

### **5. AWS Simple Email Service(SES)를 활용한 이메일 전송**:

- 긍정적인 리뷰가 감지되면 관리자의 이메일로 알림을 전송
    - `“sentiment”: “Positive”`인 경우
- 이메일 전송을 위해 **송신 및 수신 이메일 모두 자격 증명이 되어야 함**
- 이메일 제목 및 본문 예시:
    
    ```
    **Subject**: [Positive] Review from Patricia Stewart
    **Body**: Review: The tool is fantastic. Far despite visit mind computer prevent.
    ```
    

## 제출물

### **1. 코드**:

- **완성된** Dockerfile + requirements.txt
→ `{student number}.zip` 파일로 첨부

### 2. 보고서 (PDF only)

- `{student number}_assignment3.pdf` 형식으로 제출
- 포함하는 자료:
    1. **API gateway** 리소스 스크린샷 
        - 제출물에는 좌측 패널에 **학번이 표현**되어야 함
        - e.g., API: ReviewProcessingAPI-2026320001
        
        ![스크린샷 2024-12-01 23.29.39.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/e9d26ae8-7eed-4c31-8484-795491da643b/3067adc8-7e39-45ca-94d0-ca220e8a94da/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2024-12-01_23.29.39.png)
        
    2. 완성된 **Lambda** 함수 스크린샷
        - 학번이 포함된 **함수 이름, 이미지 정보**가 드러나도록 할 것
            
            ![lambda 함수.png](attachment:57047be5-a91d-4dc7-be75-f0c40979ed67:lambda_함수.png)
            
    3. **DynamoDB** 테이블에 저장된 리뷰 데이터 스크린샷
        - 학번이 포함된 테이블 이름이 드러나도록 할 것
        - `request_generator.py`로 만들어진 리뷰 30개 보이도록 할 것
            - **sentiment로 정렬하여 전체 항목을 모두 다 볼 수 있도록 캡처할 것**
            
            ![dynamoDB capture.png](attachment:5dce36fe-681b-4fef-b4d4-c9c9777f6e7f:dynamoDB_capture.png)
            
    4. **이메일** 전송 증빙 스크린샷
        - DynamoDB에 표현된 `“sentiment”: “Positive”` 와 같은 개수임을 확인할 수 있도록 할 것
            
            ![image.png](attachment:e3ec429a-2314-41a9-9f57-ead096f29f8a:image.png)
            
- **파이프라인** 및 **코드** 설명
    1. **전체 파이프라인의 주요 구성요소**를  **작업 처리 순서대로 나열**하고 **각 구성요소의 역할을 설명**할 것
        - 전체 파이프라인의 **주요 구성요소를 나타내는 다이어그램 또는 흐름도**를 포함
            - 흐름도 예시 (source: https://en.wikipedia.org/wiki/Flowchart)
                
                ![image.png](attachment:5da629e3-e223-4827-9522-ab9b69da8233:image.png)
                
    2. `lambda_function.py` 의 코드 블록이 각각 무슨 역할을 하는지 설명할 것
        - e.g.,
            
            ```python
            dynamodb = boto3.resource('dynamodb')
            TABLE_NAME = os.environ.get("TABLE_NAME", "reviews")
            table = dynamodb.Table(TABLE_NAME)
            ses = boto3.client('ses')
            ```
            
            - **설명**: 라이브러리를 사용하여 DynamoDB 리소스와 SES 클라이언트를 초기화하고, 환경변수로부터 TABLE_NAME을 받아와 DynamoDB가 해당 테이블에 접근할 수 있게 한다.
    3. `Dockerfile` 의 각 line이 각각 무슨 역할을 하는지 설명할 것
        - e.g.,
            
            ```docker
            FROM public.ecr.aws/lambda/python:3.13
            ```
            
            - **설명**: AWS Lambda용 Python 3.13 베이스 이미지를 사용한다.

## 요청 생성기 사용 방법

- 가상 환경 생성 후 필요한 라이브러리 설치
- `.env` 파일에 API Gateway URL 입력
- `request_generator.py` 실행
