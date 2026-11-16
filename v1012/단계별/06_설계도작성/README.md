# 06 설계도작성

- 실행 주체: 에이전트(Claude)

## 설명
- 하는 일: 5단계 해석과 요청을 Hypit 이 실행할 수 있는 설계도(SVML)로 옮김
- 나온 데이터: 설계도 두 벌
  - 재현판 v1012.svml — 원본 영상·소리 + 내레이션 낱말 맞춤 자막(대본 10덩이)
  - 교체판 v1012_gen.svml — 재현판 + 생성 영상(9단계)을 두 번째 재료로 넣고 실사 4자리(g1~g4)만 위층으로 덮음
  - recipes_v1012.svs(자막 모양: 위쪽 가운데·보라 강조) · v1012.svrun · v1012_gen.svrun(만들 것 = final.video)
- 왜 이렇게 나오나: 연결 순서는 Hypit 예제와 같음(정규화 → 정렬 → 시간 틀 → 투영 → 층 → Film), 대본은 화면 글자 기준 바른 낱말(「한정」 「애디렉트」), 교체 자리는 5단계 TIMELINE 장면 경계, 생성 영상 안 시작은 9단계 컷 시작 + 0.4초(자리표 = 입력\생성컷_자리.txt)
- 왜 하나: Hypit 은 설계도에 적힌 것만 실행 — 무엇을 지키고 무엇을 바꿀지(5단계)를 실행 가능한 형태로 고정
- Hypit 기본 경로와 차이: 기본은 설계도 안 seedance 태그로 생성을 선언 → build 때 생성. 이번엔 Higgsfield 로 먼저 생성(9단계)해 파일을 asset:Video 재료로 넣음

## 지침 한국어 요약
- 지침_한국어.md (따른 절의 원문 핵심 문장 + 한국어 풀이 + 이번 적용)

## 지침(지침\ 폴더, 에이전트용 설명서 — hypit 프로그램이 읽지 않음)
- script-syntax.md (skills/hypit/references/production/script-syntax.md) — 한국어 대본은 띄어쓰기 그대로, || = 자막 덩이 경계, @{이름} = 의미 구간
- media.md (skills/hypit/references/production/media.md) — Normalize → whisperx:Alignment → semantic:Projection 연결 구조, 소리 없는 영상은 audio="none"

## 입력(입력\ 폴더)
- 생성컷_자리.txt
- 예제_production.svml
- 요청.txt

## 출력(출력\ 폴더)
- recipes_v1012.svs
- v1012.svml
- v1012.svrun
- v1012_gen.svml
- v1012_gen.svrun
