# 01 원본확인

- 실행 주체: Hypit 로직(ffmpeg)

## 설명
- 하는 일: 영상 파일 머리 정보 읽기
- 나온 데이터: 15.015초 · 1920×1080 · 29.97fps · 소리 있음
- 왜 이렇게 나오나: 파일에 적힌 정보를 그대로 읽음
- 왜 하나: 다음 단계 기준값 — 소리가 있어 받아쓰기 가능, 마지막 프레임 14.98초라 격자 끝 시각 제한

## 지침 한국어 요약
- 지침_한국어.md (따른 절의 원문 핵심 문장 + 한국어 풀이 + 이번 적용)

## 지침(지침\ 폴더, 에이전트용 설명서 — hypit 프로그램이 읽지 않음)
- reference-video.md (skills/hypit/references/creation/reference-video.md) — 절 「Make time visible」 — probe gives duration, dimensions, frame rate and audio presence

## 입력(입력\ 폴더)
- 명령.txt

## 출력(출력\ 폴더)
- 01_probe.json
- 01_probe.txt
