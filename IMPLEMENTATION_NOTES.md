# Flowmatic Implementation Notes

- 작성일: 2026-07-14
- 기술 스택: 순수 정적 HTML/CSS/JavaScript, GitHub Pages 배포
- 배포 플랫폼: GitHub Pages + CNAME `flowmatic-os.com`
- 다국어 처리 방식: `/ko/`, `/en/`, `/ar/` 정적 HTML을 생성하며 각 HTML에는 해당 언어만 렌더링합니다. 기존 루트 URL과 `*.html` 제품 URL은 한국어 호환 페이지로 유지합니다.
- 데모 영상 파일: `flowmatic_nc_demo.mp4`, `flowmatic_ct_demo.mp4`; 두 제품 페이지의 `<video>`는 `controls`, `playsinline`, `preload="metadata"`, `poster`를 사용합니다.
- NC 공개 브라우저 데모: `/nc-demo-lite.js`, `/nc-demo-lite-worker.js`, `/demo-data/flowmatic-nc-sample.nc`; 업로드 없이 브라우저 내부에서 기본 G-code 이동시간만 계산합니다.
- 개발 프리뷰 제품: Work Standard, TMS, AMR은 빈 비디오 플레이어 없이 개발 상태 패널, 파일럿 입력, 확인 결과, 문의 CTA를 표시합니다.
- 실제 문의 목적지: 저장소에서 검증된 이메일, 폼 엔드포인트, 예약 링크를 찾지 못했습니다. 안전한 폴백으로 모든 CTA를 Contact 섹션과 `interest` query parameter로 연결했습니다.
- 적용한 안전한 폴백: 고객사, 성과 수치, 보안 인증, 배포 방식, 지원 컨트롤러, 회사 주소, 전화번호, 이메일은 추측해 표시하지 않았습니다.
- 사용자 확인 필요: 실제 문의 이메일 또는 폼 엔드포인트, 개인정보처리방침 URL, 법인명/주소/전화번호, 아랍어 최종 감수, Work Standard/TMS/AMR의 출시 상태.
