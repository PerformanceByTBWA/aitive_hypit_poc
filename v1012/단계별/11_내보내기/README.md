# 11 내보내기

- 실행 주체: Hypit 로직

## 설명
- 하는 일: Hypit 내부 결과 저장소에서 최종 영상과 필요한 값을 꺼냄, 런타임 끄기(runtime down + programs down)
- 나온 데이터:
  - v1012_replica.mp4 — 재현판(1920×1080 · 30fps · 15.0초 · 3.3MB)
  - v1012_gen.mp4 — 교체판(1920×1080 · 30fps · 15.0초 · 3.1MB)
  - compare_원본_교체판.mp4 — 왼쪽 원본 · 오른쪽 교체판(Hypit 밖 ffmpeg 로 붙인 확인용)
  - 11b_inspect · gen_11b_inspect — 빌드 출력 목록(재현판 14개 · 교체판 19개)
  - replica_05s · gen_05s(0.5초 격자) · replica_full · gen_full(원본 크기 낱장) — 확인용, hypit media tile·frames 로 뽑음
- 교체판 확인: 4자리가 생성 컷으로 바뀜, 원본에서 실사 위에 얹혀 있던 손글씨 제목 · 「AI generated」 · 선택 상자는 교체 구간에서 사라짐(코드로 다시 얹어야 함), 생성 컷 속 로고 · 흐린 문구 · 「딸」 「깍」은 남음, 품질은 사람이 아직 안 봄
- 왜 하나: 결과는 Hypit 저장소에 쌓여 있어 꺼내야 씀

## 지침 한국어 요약
- 지침_한국어.md (따른 절의 원문 핵심 문장 + 한국어 풀이 + 이번 적용)

## 지침(지침\ 폴더, 에이전트용 설명서 — hypit 프로그램이 읽지 않음)
- builds.md (skills/hypit/references/production/builds.md) — 절 「Browse and export project Results」 — get 은 영상=파일 하나, 값=value.json 폴더

## 입력(입력\ 폴더)
- 명령.txt

## 출력(출력\ 폴더)
- 11a_get_video.txt
- 11b_inspect.txt
- 11c_get_alignment.txt
- 11d_runtime-down.txt
- 11e_programs-down.txt
- compare_원본_교체판.mp4
- gen_05s.jpg
- gen_11a_get_video.txt
- gen_11b_inspect.txt
- gen_11d_get_caption_timing.txt
- gen_11e_runtime-down.txt
- gen_11f_programs-down.txt
- gen_full
- replica_05s.jpg
- replica_full
- v1012_gen.mp4
- v1012_replica.mp4
