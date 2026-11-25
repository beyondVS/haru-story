# haru-story

하루 이야기의 데스크톱 앱, API 서버, 관리자 웹을 함께 개발하는 모노리포입니다.

| 경로 | 역할 |
| --- | --- |
| `apps/client` | Tauri 2, Vue 3, TypeScript, Rust 기반 데스크톱 앱 |
| `services/backend` | Litestar, Granian, Strawberry, Advanced Alchemy 기반 API |
| `services/admin` | Vue 3, TypeScript 기반 관리자 웹(CSR) |
| `contracts/graphql` | 백엔드에서 생성한 GraphQL 스키마 |
| `infra/local` | 로컬 PostgreSQL 17 실행 설정 |
| `tooling` | GraphQL 스키마 생성 및 검증 명령 |
| `docs` | 프로젝트 정책, 아키텍처 결정, 운영 문서 |

클라이언트의 업무 규칙과 사용 사례는 `src/domain`과 `src/application`에, Rust 연동은 `src/adapters/tauri`에 추가합니다. 백엔드의 업무 규칙, 사용 사례, 외부 시스템 연동은 각각 `domain`, `application`, `infrastructure`에 둡니다. DB 마이그레이션은 `services/backend/migrations`에 둡니다.

문서 배치와 작업 지침은 저장소의 문서 목차에서 찾을 수 있습니다. [프로젝트 문서 목차](docs/README.md)

## 로컬 실행

저장소 루트에서 실행합니다. Node.js 24, npm 11, Python 3.13, uv가 필요합니다. PostgreSQL 통합 검증에는 Docker Compose가 필요합니다.

```sh
npm ci
uv sync --project services/backend --locked
```

각 개발 서버를 별도 터미널에서 시작합니다.

| 명령 | 접속 |
| --- | --- |
| `npm run dev:backend` | `http://127.0.0.1:8000/health`, `POST /graphql` |
| `npm run dev:client:web` | `http://127.0.0.1:1420`에서 클라이언트 화면 확인 |
| `npm run dev:admin` | `http://127.0.0.1:5173` |
| `npm run dev:client` | Tauri 데스크톱 창 |

데스크톱 앱을 실행하려면 rustup과 [OS별 Tauri 선행 도구](https://v2.tauri.app/start/prerequisites/)를 설치합니다. Windows는 MSVC C++ Build Tools와 WebView2, macOS는 Xcode Command Line Tools를 사용합니다. `dev:client`가 포트 1420에서 Vite를 시작하므로 별도로 실행한 `dev:client:web`은 먼저 종료합니다.

두 Vite 개발 서버는 `/graphql`을 로컬 백엔드로 프록시합니다. 관리자 웹을 정적 호스팅에 배포할 때는 같은 호스트의 `/graphql`을 백엔드로 연결합니다. 빌드한 데스크톱 앱의 기본 GraphQL URL은 `http://127.0.0.1:8000/graphql`입니다. 다른 API 호스트를 사용할 때는 Vite 빌드 환경의 `VITE_GRAPHQL_URL`에 URL을 지정하고 Tauri CSP의 `connect-src` 및 서버 CORS 정책을 확인합니다.

## PostgreSQL 통합 검사

루트의 `.env.example`에는 로컬 개발용 접속 설정이 있습니다. 포트를 변경할 때는 이를 `.env`로 복사하고 `HARU_DB_PORT`와 `HARU_DATABASE_URL`의 포트를 함께 수정합니다. 기본 PostgreSQL 포트는 호스트의 `54329`입니다.

```sh
docker compose -f infra/local/compose.yaml up -d --wait
```

기본 API 상태 확인은 DB 연결 없이 실행됩니다. `HARU_TEST_DATABASE=1`을 설정하면 pytest가 PostgreSQL 연결도 확인합니다. 사용자 지정 설정 파일을 적용한 실행 예시는 다음과 같습니다.

```powershell
$env:HARU_TEST_DATABASE = '1'
uv run --project services/backend --env-file .env --locked python -m pytest
```

사용자 지정 DB 설정으로 서버를 실행할 때도 `uv run`에 `--env-file .env`를 전달합니다. 기본 설정이라면 `--env-file .env` 옵션을 생략할 수 있습니다.

## 검증과 빌드

`npm run lint`는 두 Vue 앱을 ESLint로, 백엔드와 GraphQL 스키마 도구를 Ruff로 검사합니다. `npm run format:check`는 Prettier와 Ruff의 서식 검사를 실행하고, `npm run format`은 같은 소스 범위에 서식을 적용합니다.

```sh
npm run check
npm run build
npm run build:client:desktop
```

GraphQL 스키마를 수정한 후에는 `npm run schema:export`를 실행합니다. `npm run schema:check`는 생성 결과가 저장된 스키마와 일치하는지 확인합니다.

GitHub Actions의 **Checks**는 기본 브랜치에 워크플로가 반영된 뒤 **Actions → Checks → Run workflow**에서 수동으로 실행합니다. 프런트엔드와 백엔드의 린트·서식 검사, Vue 앱 빌드, 백엔드와 PostgreSQL 테스트, Windows 및 macOS의 Tauri 컴파일을 실행합니다. Tauri 검사에는 `apps/client/src-tauri/Cargo.lock`이 필요합니다.
