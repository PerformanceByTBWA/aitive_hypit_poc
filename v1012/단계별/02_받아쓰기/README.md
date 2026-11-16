# 02 받아쓰기

- 실행 주체: 음성 인식 모델(WhisperX, 로컬)

## 설명
- 하는 일: 소리를 듣고 글자로 적고, 낱말마다 시작·끝 초와 인식 점수를 붙임
- 나온 데이터: transcript.json — 5문장 22낱말, 인식 점수 평균 0.88
- 왜 이렇게 나오나: 음성 인식 모델(large-v3)이 듣고 적은 뒤 한국어 정렬 모델이 낱말 시각을 찍음 → 들은 대로라 오인식 섞임(「한정」→「안정」, 「애디렉트」→「애드렉트」)
- 왜 하나: 광고는 말에 맞춰 화면이 바뀜 → 「어느 말 때 무엇이 보이나」를 맞추려면 낱말별 시각 필요, 점수 낮은 곳(「딸깍」 0.47)은 다시 볼 곳 표시
- 입력의 hypit.runtime.json: 음성 정렬을 로컬 whisperx.local 에 묶은 설정 → 외부 전송 없음
- 출력의 02a~02f: 런타임 켜기·점검·받아쓰기·끄기 명령의 화면 출력

## 지침 한국어 요약
- 지침_한국어.md (따른 절의 원문 핵심 문장 + 한국어 풀이 + 이번 적용)

## 지침(지침\ 폴더, 에이전트용 설명서 — hypit 프로그램이 읽지 않음)
- reference-video.md (skills/hypit/references/creation/reference-video.md) — 절 「Make time visible」 — 말 있는 영상은 hypit transcribe, 언어 반드시 지정(ko)
- local-tools.md (skills/hypit/references/environment/local-tools.md) — 로컬 WhisperX 준비·관리(이번엔 11/05 준비본 그대로)

## 입력(입력\ 폴더)
- hypit.runtime.json
- 명령.txt

## 출력(출력\ 폴더)
- 02a_runtime-use.txt
- 02b_runtime-up.txt
- 02c_doctor.txt
- 02d_transcribe.txt
- 02e_runtime-down.txt
- 02f_programs-down.txt
- transcript.json
