# 04 프레임격자

- 실행 주체: Hypit 로직(ffmpeg)

## 설명
- 하는 일: 영상에서 프레임을 뽑아 한 장에 모으고 그 순간 들리는 낱말을 아래에 붙임
- 나온 데이터: evidence\ — 전체 1초·0.5초(whole_1s·whole_05s·words_05s), 0–3초(hook), 「딸깍」 앞뒤 0.1초(ttalkkak), 카드 구간(process), 끝 5초(endcard), 후보 근처 모든 프레임(cuts\), 원본 크기 낱장 11장(full\)
- 왜 이렇게 나오나: 2단계 transcript.json 시각으로 낱말을 붙임 → 「말 붙은 그림」
- 왜 하나: 에이전트는 영상을 재생 못 하고 그림만 봄 → 영상을 볼 수 있는 형태로 바꿈, 넓게(흐름) → 좁게(전환 순간) 순서
- 입력: 2단계 transcript.json 도 씀(02_받아쓰기\출력)

## 지침 한국어 요약
- 지침_한국어.md (따른 절의 원문 핵심 문장 + 한국어 풀이 + 이번 적용)

## 지침(지침\ 폴더, 에이전트용 설명서 — hypit 프로그램이 읽지 않음)
- reference-video.md (skills/hypit/references/creation/reference-video.md) — 절 「Make time visible」 — tile·tiles·frames, --every-frame, --ranges, --around, --transcript, 넓게→좁게

## 입력(입력\ 폴더)
- 04_ranges.json
- 명령.txt

## 출력(출력\ 폴더)
- 04a_tile_words_05s.txt
- 04b_tiles_cuts_everyframe.txt
- 04c_tile_ttalkkak.txt
- 04d_tile_hook.txt
- 04e_tile_endcard.txt
- 04f_frames_full.txt
- 04g_tile_proc.txt
- evidence
