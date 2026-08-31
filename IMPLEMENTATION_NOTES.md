# Flowmatic Implementation Notes

- 작성일: 2026-08-31
- 기술 스택: 순수 정적 HTML/CSS/JavaScript, GitHub Pages 배포
- 배포 플랫폼: GitHub Pages + CNAME `flowmatic-os.com`
- 다국어 처리 방식: `/ko/`, `/en/`, `/ar/` 정적 HTML을 생성하며 각 HTML에는 해당 언어만 렌더링합니다. 기존 루트 URL과 `*.html` 제품 URL은 한국어 호환 페이지로 유지합니다.
- 데모 영상 파일: `flowmatic_nc_demo.mp4`, `flowmatic_ct_demo.mp4`; 두 제품 페이지의 `<video>`는 `controls`, `playsinline`, `preload="metadata"`, `poster`를 사용합니다.
- NC 공개 브라우저 데모: `/nc-demo-lite.js`, `/nc-demo-lite-worker.js`, `/demo-data/flowmatic-nc-sample.nc`; 업로드 없이 브라우저 내부에서 기본 G-code 이동시간만 계산합니다.
- Quality Intelligence: `/ko/quality/`, `/en/quality/`, `/ar/quality/` 및 한국어 호환 URL `/quality.html`; Defect → Loss → Priority → Work → Verify → Recurrence 구조를 기준으로 하며 Inspection은 Evidence / Input Layer로 표시합니다.
- Machining Intelligence: Manufacturing Recipe, 기존 G-code 문맥 추론, safe assembly, 측정/보정, managed metadata, air-gapped USB 동기화를 V.Next 구조로 설명합니다. source-level 검증과 Active development / PoC 범위를 분리합니다.
- Manufacturing Intelligence Platform: Manufacturing Context → Engine Pool → Module Pool → Solution Profile 조합 구조를 `/{lang}/platform/`에서 설명합니다. Event Bus·Audit·Adapter는 독립 제품이 아닌 경량 공통 런타임으로 한정합니다.
- 신규 정식 URL: `/{lang}/machining-intelligence/`, `/{lang}/operations-intelligence/`, `/{lang}/logistics-intelligence/`, `/{lang}/platform/`; 기존 NC/CT/Quality/Work Standard/TMS/AMR URL은 하위 컴포넌트 페이지로 유지합니다.
- Operations Intelligence: Functional MVP / internal validation 상태로 표시하며, Tracked Operational Cost를 완전 제조원가나 회계원가로 표현하지 않습니다.
- 개발 프리뷰 제품: Work Standard, TMS, AMR은 빈 비디오 플레이어 없이 개발 상태 패널, 파일럿 입력, 확인 결과, 문의 CTA를 표시합니다.
- 공식 브랜드 마크: 좌상단 파랑, 좌하단 빨강, 우측 노랑 2칸의 2×2 마크를 `/assets/branding/`에서 단일 관리합니다. 헤더·푸터·파비콘·앱 아이콘·OG 이미지가 같은 원본을 사용합니다.
- 공식 QR 연락 시그니처: `https://flowmatic-os.com/`로 연결하며 `contact@flowmatic-os.com`을 함께 표시합니다. Contact 영역과 외부 자료에서 재사용할 SVG/PNG를 제공합니다.
- 공식 문의 목적지: `contact@flowmatic-os.com`. 문의 폼은 Formspree 엔드포인트를 통해 AJAX로 제출하며, 성공·실패 상태를 페이지 안에서 안내합니다.
- 문의 선택지는 네 Intelligence와 Platform / Engine-Module Composition만 노출하며 legacy component URL의 interest 값은 상위 Intelligence로 매핑합니다.
- 사용자 확인 필요: 개인정보처리방침 URL, 법인명/주소/전화번호, 아랍어 원어민 최종 감수, 실제 CNC/CMM 및 machine adapter 현장 검증 상태.
