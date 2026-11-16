# 09 재료생성

- 실행 주체: 외부 생성 모델 — ByteDance Seedance 2.0 fast, Higgsfield MCP 경유(Hypit 밖, 2026-11-14)

## 설명
- 하는 일: 원본의 실사 4컷(뒷모습 머리 · 제품과 액체 · 인물과 탁자 위 병 · 병 든 인물)을 Seedance 로 새로 생성
- 입력: prompt.txt(컷별 타임코드 · <<<image_N>>> 참조 순서 · 「글자·로고·커서·선택 상자 없음」 지시) · 참조그림\ 4장(원본 정지 화면 0.00 · 1.34 · 3.05 · 6.90초) · 요청기록.json(15초 · 480p · 16:9 · 소리 없음 · 참조 역할 image ×4, Higgsfield 작업 기록에서 옮김)
- 나온 데이터: seedance_raw.mp4(864×496 · 24fps · 15.04초 · 소리 없음), 컷 시작 0 · 4.17 · 8.67 · 11.46초, 결과.md · sheet.jpg(참조 ↔ 생성 대조) · raw_05s.jpg · raw_cut23.jpg · 생성영상_probe.txt
- 비용: 15크레딧(사전 조회 값과 같음)
- 왜 이렇게 나오나: 참조 그림을 움직이는 방식(i2v 에 가까움)이라 인물·병·구도가 원본과 거의 같음, 참조에 있던 로고·흐린 문구·「딸」 「깍」 글자는 프롬프트로 지워지지 않고 남음, 2→3 컷은 하드 컷 지시에도 디졸브
- 왜 하나: 원본에 없는(또는 바꿀) 장면이 필요할 때만 — 이 단계에서만 돈이 들고 파일이 밖으로 나감
- 밖으로 나간 것: 프롬프트 글 · 참조 그림 4장(업로드) · 설정 값 → Higgsfield → ByteDance 모델
- Hypit 기본 경로와 차이: Hypit 안에서 생성하면 설계도의 seedance 태그 → build 때 HypiHub 로 요청, 프롬프트 틀(입력\참고_seedance-kits) 고정 문장이 붙고 참조마다 사람 포함 표시가 감. 이번엔 틀 없이 직접 쓴 프롬프트
- 순서: 생성이 있으면 9 → 8 → 10 → 11(생성 영상도 정규화 뒤 렌더)

## 지침 한국어 요약
- 지침_한국어.md (따른 절의 원문 핵심 문장 + 한국어 풀이 + 이번 적용)

## 지침(지침\ 폴더, 에이전트용 설명서 — hypit 프로그램이 읽지 않음)
- video-direction.md (skills/hypit/references/playbooks/craft/video-direction.md) — 생성 영상 연출
- image-direction.md (skills/hypit/references/playbooks/craft/image-direction.md) — 생성 이미지 연출
- generated-dependencies.md (skills/hypit/references/playbooks/craft/generated-dependencies.md) — 참조 파일 관계
- prompt-kits.md (skills/hypit/references/production/prompt-kits.md) — 프롬프트 틀 고르기·쓰기

## 입력(입력\ 폴더)
- prompt.txt
- 요청기록.json
- 참고_seedance-kits
- 참조그림

## 출력(출력\ 폴더)
- raw_05s.jpg
- raw_cut23.jpg
- seedance_raw.mp4
- sheet.jpg
- 결과.md
- 생성영상_probe.txt
