# 05 판단기록

- 실행 주체: 에이전트(Claude) — Hypit 기능 없음

## 설명
- 하는 일: 1~4단계 데이터를 보고 영상이 왜 잘 됐는지 해석해 기록
- 나온 데이터: ANALYSIS(전체 구조 5박자·유지할 관계 7개) · TIMELINE(구간별 말·화면·역할) · PROGRESS(남은 확인)
- 왜 이렇게 나오나: Hypit 기계가 아닌 에이전트가 지침(양식·읽는 법)대로 해석 → 모델·지침에 따라 내용 달라짐, 사람 검토 안 함
- 왜 하나: 다시 만들 때 「무엇을 지키고 무엇을 바꿀지」 정하는 근거
- 외부 전송: 받아쓰기 글·격자 그림·지침이 에이전트 모델(Claude)로 감

## 지침 한국어 요약
- 지침_한국어.md (따른 절의 원문 핵심 문장 + 한국어 풀이 + 이번 적용)

## 지침(지침\ 폴더, 에이전트용 설명서 — hypit 프로그램이 읽지 않음)
- SKILL.md (skills/hypit/SKILL.md) — 절 「Understand and adapt」 — 전체 해석은 Analysis, 시각별 세부는 Timeline
- reference-video.md (skills/hypit/references/creation/reference-video.md) — 절 「Preserve a connected account」·「Turn understanding into new direction」 — ANALYSIS·TIMELINE·PROGRESS 양식
- index.md (skills/hypit/references/playbooks/index.md) — 절 「Formats」 표 — 형식 고르기
- narration-led-demo.md (skills/hypit/references/playbooks/formats/narration-led-demo.md) — 고른 형식: 화면 밖 내레이션이 뼈대인 영상
- screen-demonstrations.md (skills/hypit/references/playbooks/craft/screen-demonstrations.md) — 화면 시연 읽기(도입·절 제목까지 참고)
- motion-graphics.md (skills/hypit/references/playbooks/craft/motion-graphics.md) — 모션그래픽 읽기(도입·절 제목까지 참고)
- graphic-compositions.md (skills/hypit/references/playbooks/craft/graphic-compositions.md) — 화면 구성 읽기(도입·절 제목까지 참고)
- sound-mix.md (skills/hypit/references/playbooks/craft/sound-mix.md) — 소리 읽기(도입·절 제목까지 참고)

## 입력(입력\ 폴더)
- 음량측정_hypit밖.txt
- 입력목록.txt

## 출력(출력\ 폴더)
- ANALYSIS.md
- PROGRESS.md
- TIMELINE.md
