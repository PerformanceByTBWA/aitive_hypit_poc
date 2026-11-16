# 03 화면변화후보

- 실행 주체: Hypit 로직(픽셀 차이)

## 설명
- 하는 일: 앞뒤 프레임 픽셀 차이가 기준(0.1)을 넘는 시각을 찍음
- 나온 데이터: 후보 11개(시각·점수)
- 왜 이렇게 나오나: 기계적 계산이라 컷 판단 아님 → 한 전환이 여러 개로 잡히고(12.567·12.6·12.633), 천천히 미끄러지는 카드는 못 잡음
- 왜 하나: 15초를 프레임마다 다 볼 수 없으니 「어디를 자세히 볼지」 표지 — 판정은 4단계 그림으로
- 후보판정.md: 에이전트가 모든 프레임 격자로 확인한 결과(Hypit 출력 아님)

## 지침 한국어 요약
- 지침_한국어.md (따른 절의 원문 핵심 문장 + 한국어 풀이 + 이번 적용)

## 지침(지침\ 폴더, 에이전트용 설명서 — hypit 프로그램이 읽지 않음)
- reference-video.md (skills/hypit/references/creation/reference-video.md) — 절 「Make time visible」 — boundaries locates abrupt visual changes worth inspecting

## 입력(입력\ 폴더)
- 명령.txt

## 출력(출력\ 폴더)
- 03_boundaries_r30.json
- 03_boundaries_r30.txt
- 후보판정.md
