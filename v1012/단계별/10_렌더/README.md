# 10 렌더

- 실행 주체: Hypit 로직(헤드리스 크롬 + ffmpeg)

## 설명
- 하는 일: 층(원본 화면 · 생성 컷 · 소리 · 자막)을 프레임마다 겹쳐 그리고 소리와 합침
- 나온 데이터: caption-timing\value.json(자막 22덩이 프레임 구간) · speech_ad\value.json(결과 시간 틀 0–450프레임) · 자막시각표.md · gen_caption-timing(교체판, 재현판과 같은 값)
- 왜 이렇게 나오나: 8단계 정렬 프레임을 자막 레시피(앞뒤 2프레임 여유 등)로 자막 덩이 시각으로 바꿈, 교체판도 같은 대본·같은 원본 소리라 자막 시각이 같음
- 교체판 층: 원본(z=0, 0–450f) 위에 생성 컷 4개(z=1, 0–40 · 40–89 · 89–140 · 190–217f), 소리 = 원본
- 왜 하나: 여러 층을 영상 한 편으로 합침
- 빌드 안 요청 3개(두 빌드 같음): rasterize-visual 450프레임 · render-timeline-audio · mux-program-media, 프레임 그림 450장은 빌드 내부 작업 파일이라 따로 꺼내지 않음

## 지침 한국어 요약
- 지침_한국어.md (따른 절의 원문 핵심 문장 + 한국어 풀이 + 이번 적용)

## 지침(지침\ 폴더, 에이전트용 설명서 — hypit 프로그램이 읽지 않음)
- rendering.md (skills/hypit/references/production/rendering.md) — Film 이 층을 Composition 으로 묶고, Rendering 이 프레임 구간을 그려 영상으로

## 입력(입력\ 폴더)
- 입력목록.txt

## 출력(출력\ 폴더)
- caption-timing
- gen_caption-timing
- speech_ad
- 자막시각표.md
