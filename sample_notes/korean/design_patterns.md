# 디자인 패턴

소프트웨어 설계에서 자주 발생하는 문제들의 해결책입니다.

## 생성 패턴 (Creational Patterns)

객체 생성 메커니즘을 다룹니다.

### 싱글톤 (Singleton)

클래스의 인스턴스가 **오직 하나만** 존재하도록 보장합니다.

```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### 팩토리 메서드 (Factory Method)

객체 생성 로직을 서브클래스에 위임합니다.

### 빌더 (Builder)

복잡한 객체를 단계적으로 생성합니다.

## 구조 패턴 (Structural Patterns)

클래스와 객체를 조합하여 더 큰 구조를 만듭니다.

### 어댑터 (Adapter)

호환되지 않는 인터페이스를 연결합니다.

### 데코레이터 (Decorator)

객체에 **동적으로 기능을 추가**합니다.

### 프록시 (Proxy)

다른 객체에 대한 대리자 역할을 합니다:

- 접근 제어
- 지연 로딩
- 로깅

## 행위 패턴 (Behavioral Patterns)

객체들 간의 책임 분배와 알고리즘을 다룹니다.

### 옵저버 (Observer)

객체의 상태 변화를 다른 객체들에게 통지합니다.

- 이벤트 핸들링
- MVC 패턴의 기반
- Pub/Sub 모델

### 전략 (Strategy)

알고리즘을 캡슐화하여 **교체 가능**하게 만듭니다.

### 커맨드 (Command)

요청을 객체로 캡슐화합니다.

## SOLID 원칙

좋은 객체지향 설계의 5가지 원칙:

- **S**ingle Responsibility: 단일 책임
- **O**pen/Closed: 개방/폐쇄
- **L**iskov Substitution: 리스코프 치환
- **I**nterface Segregation: 인터페이스 분리
- **D**ependency Inversion: 의존성 역전

## 안티패턴

피해야 할 나쁜 설계 사례들:

- 스파게티 코드
- God Object
- 순환 의존성
