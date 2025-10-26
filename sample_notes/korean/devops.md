# DevOps와 CI/CD

개발과 운영을 통합하여 소프트웨어 배포를 자동화하는 방법론입니다.

## DevOps 문화

### 핵심 원칙

- **협업**: 개발팀과 운영팀의 긴밀한 협력
- **자동화**: 반복 작업의 자동화
- **지속적 개선**: 피드백을 통한 개선
- **책임 공유**: 코드와 인프라에 대한 공동 책임

## CI/CD 파이프라인

### CI (Continuous Integration)

코드 변경사항을 자동으로 통합하고 테스트합니다.

#### 주요 단계

1. **코드 커밋**: Git에 푸시
2. **빌드**: 소스코드 컴파일
3. **테스트**: 자동화된 테스트 실행
4. **피드백**: 결과 통보

### CD (Continuous Delivery/Deployment)

#### Continuous Delivery

프로덕션 배포 준비를 자동화합니다.

#### Continuous Deployment

모든 변경사항을 **자동으로 프로덕션**에 배포합니다.

## CI/CD 도구

### Jenkins

가장 인기 있는 오픈소스 자동화 서버입니다:

- **플러그인 생태계**
- Pipeline as Code (Jenkinsfile)
- 분산 빌드

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'make build'
            }
        }
        stage('Test') {
            steps {
                sh 'make test'
            }
        }
    }
}
```

### GitHub Actions

GitHub 통합 CI/CD 플랫폼입니다:

- YAML 기반 워크플로우
- **마켓플레이스** 액션
- 무료 공개 저장소

### GitLab CI/CD

GitLab 내장 CI/CD입니다.

### CircleCI

클라우드 기반 CI/CD 서비스입니다.

## 인프라 자동화

### Infrastructure as Code (IaC)

코드로 인프라를 정의하고 관리합니다.

#### Terraform

클라우드 독립적인 IaC 도구입니다:

```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  
  tags = {
    Name = "WebServer"
  }
}
```

#### Ansible

**에이전트리스** 구성 관리 도구입니다.

#### CloudFormation

AWS 전용 IaC 서비스입니다.

## 컨테이너화

### Docker

애플리케이션을 컨테이너로 패키징합니다:

- **Dockerfile**: 이미지 정의
- 경량화
- 일관된 환경

### Docker Compose

여러 컨테이너를 정의하고 실행합니다.

### Kubernetes

컨테이너 오케스트레이션 플랫폼입니다:

- **자동 스케일링**
- 로드 밸런싱
- 롤링 업데이트
- 자가 치유

## 모니터링과 로깅

### 모니터링 도구

- **Prometheus**: 메트릭 수집
- **Grafana**: 시각화
- Datadog
- New Relic

### 로깅

- **ELK Stack**: Elasticsearch, Logstash, Kibana
- Splunk
- CloudWatch Logs

### 알림

- PagerDuty
- Slack 통합
- 이메일 알림

## 보안 (DevSecOps)

개발 프로세스에 보안을 통합합니다:

- **정적 분석**: SAST
- **동적 분석**: DAST
- 의존성 스캔
- 컨테이너 이미지 스캔

## 배포 전략

### Blue-Green Deployment

두 개의 동일한 환경을 유지하며 전환합니다.

### Canary Deployment

일부 사용자에게만 먼저 배포합니다.

### Rolling Deployment

점진적으로 인스턴스를 업데이트합니다.

### Feature Flags

코드 배포와 기능 출시를 분리합니다.
