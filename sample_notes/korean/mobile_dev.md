# 모바일 앱 개발

iOS와 Android 플랫폼을 위한 모바일 애플리케이션 개발입니다.

## 네이티브 개발

### iOS 개발

Apple 기기를 위한 앱 개발입니다.

#### Swift

Apple의 현대적인 프로그래밍 언어입니다:

```swift
struct ContentView: View {
    var body: some View {
        Text("Hello, World!")
            .padding()
    }
}
```

#### SwiftUI

선언적 UI 프레임워크입니다.

- **간결한 문법**
- 실시간 미리보기
- 크로스 플랫폼 (iOS, macOS, watchOS)

#### UIKit

전통적인 iOS UI 프레임워크입니다.

### Android 개발

Google의 Android OS를 위한 개발입니다.

#### Kotlin

Android 공식 언어로 Java보다 **간결하고 안전**합니다.

```kotlin
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }
}
```

#### Jetpack Compose

Android의 선언적 UI 툴킷입니다.

## 크로스 플랫폼 개발

하나의 코드베이스로 여러 플랫폼에 배포합니다.

### React Native

JavaScript와 React로 모바일 앱을 만듭니다:

- **큰 커뮤니티**
- 풍부한 라이브러리
- Hot Reload

### Flutter

Google의 UI 툴킷으로 아름다운 앱을 만듭니다:

- **Dart** 언어 사용
- 빠른 성능
- 풍부한 위젯
- Material Design과 Cupertino

### Xamarin

.NET과 C#을 사용한 크로스 플랫폼 개발입니다.

## 모바일 백엔드

### Firebase

Google의 모바일 백엔드 플랫폼:

- **실시간 데이터베이스**
- 인증
- 푸시 알림
- 분석
- 클라우드 스토리지

### AWS Amplify

AWS 기반 모바일 백엔드입니다.

## 앱 배포

### App Store (iOS)

- TestFlight로 베타 테스트
- 심사 과정 필요
- 연간 개발자 등록비

### Google Play (Android)

- 빠른 배포
- 단계적 출시 가능
- 일회성 등록비
