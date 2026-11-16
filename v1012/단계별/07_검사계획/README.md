# 07 검사계획

- 실행 주체: Hypit 로직

## 설명
- 하는 일: 설계도 문법 검사, 할 일 목록·맡는 곳·요금 펼치기
- 나온 데이터:
  - 재현판(07a~07d): 「Run source is valid」 + 요청 7개, 전부 local, no Provider charge
  - 교체판(gen_07a~gen_07d): 요청 9개, 전부 local — 늘어난 2개 = 생성 영상 속성 읽기(inspect-media)·정규화(normalize-media)
- 왜 이렇게 나오나: 설계도의 관계를 따라 필요한 작업을 계산, 재료가 하나 늘면 그 재료의 읽기·정규화 작업이 늘어남
- 왜 하나: 실행 전에 돈 드는 작업이 있는지 확인 — 이번 생성은 Hypit 밖(Higgsfield)이라 계획에 유료 요청 없음, Hypit 안에서 생성하면 여기서 공급자·가격 페이지가 먼저 나옴

## 지침 한국어 요약
- 지침_한국어.md (따른 절의 원문 핵심 문장 + 한국어 풀이 + 이번 적용)

## 지침(지침\ 폴더, 에이전트용 설명서 — hypit 프로그램이 읽지 않음)
- builds.md (skills/hypit/references/production/builds.md) — 절 「Plan the selected Run」 — 실행 전 요청·공급자·요금 확인, 「Work within the agreed paid scope」

## 입력(입력\ 폴더)
- hypit.runtime.json
- 명령.txt

## 출력(출력\ 폴더)
- 07a_runtime-use.txt
- 07b_runtime-up.txt
- 07c_check.txt
- 07d_plan.txt
- gen_07a_runtime-use.txt
- gen_07b_runtime-up.txt
- gen_07c_check.txt
- gen_07d_plan.txt
