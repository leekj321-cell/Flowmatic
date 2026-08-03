# Flowmatic Implementation Notes

- 작성일: 2026-08-03
- 기술 스택: 순수 정적 HTML/CSS/JavaScript, GitHub Pages 배포
- 배포 플랫폼: GitHub Pages + CNAME `flowmatic-os.com`
- 다국어 처리 방식: `/ko/`, `/en/`, `/ar/` 정적 HTML을 생성하며 각 HTML에는 해당 언어만 렌더링합니다. 기존 루트 URL과 `*.html` 제품 URL은 한국어 호환 페이지로 유지합니다.
- 데모 영상 파일: `flowmatic_nc_demo.mp4`, `flowmatic_ct_demo.mp4`; 두 제품 페이지의 `<video>`는 `controls`, `playsinline`, `preload="metadata"`, `poster`를 사용합니다.
- NC 공개 브라우저 데모: `/nc-demo-lite.js`, `/nc-demo-lite-worker.js`, `/demo-data/flowmatic-nc-sample.nc`; 업로드 없이 브라우저 내부에서 기본 G-code 이동시간만 계산합니다.
- Flowmatic Quality: `/ko/quality/`, `/en/quality/`, `/ar/quality/` 및 한국어 호환 URL `/quality.html`; 작동 프로토타입, Inspection–Dashboard 연동 진행 상태, 구현/연동/목표 아키텍처를 구분해 표시합니다.
- 개발 프리뷰 제품: Work Standard, TMS, AMR은 빈 비디오 플레이어 없이 개발 상태 패널, 파일럿 입력, 확인 결과, 문의 CTA를 표시합니다.
- 공식 브랜드 마크: 좌상단 파랑, 좌하단 빨강, 우측 노랑 2칸의 2×2 마크를 `/assets/branding/`에서 단일 관리합니다. 헤더·푸터·파비콘·앱 아이콘·OG 이미지가 같은 원본을 사용합니다.
- 공식 QR 연락 시그니처: `https://flowmatic-os.com/`로 연결하며 `contact@flowmatic-os.com`을 함께 표시합니다. Contact 영역과 외부 자료에서 재사용할 SVG/PNG를 제공합니다.
- 공식 문의 목적지: `contact@flowmatic-os.com`. 문의 폼은 Formspree 엔드포인트를 통해 AJAX로 제출하며, 성공·실패 상태를 페이지 안에서 안내합니다.
- 사용자 확인 필요: 개인정보처리방침 URL, 법인명/주소/전화번호, 아랍어 최종 감수, Quality의 실제 연동 상태, Work Standard/TMS/AMR의 출시 상태.
