# 단계별 지침·입력·출력 모음(애디렉트 15초, Hypit 0.3.1)

- 단계 폴더마다 지침\(스킬 md 원문) · 지침_한국어.md · 입력\ · 출력\ · README.md(하는 일 · 나온 데이터 · 왜 이렇게 나오나 · 왜 하나)
- 지침 = AI 에이전트용 작업 설명서(GitHub hypit-ai/hypit 태그 v0.3.1 skills/hypit 원문 사본), hypit 프로그램은 읽지 않음
- 출력 = 그 단계에서 실제로 나온 파일(io\ · out\ · evidence\ · seedance480\ 원본에서 복사), 사본은 서버 경로 · 깨진 기호만 정리, 원본은 그대로
- 0–5 = 분석(남의 영상 읽기), 6–11 = 제작(새 영상 만들기)
- 제작은 두 벌: 재현판(v1012, 원본 + 자막, 생성 없음) · 교체판(v1012_gen, 실사 4자리를 Seedance 생성 컷으로)
- 생성은 Hypit 밖(Higgsfield MCP, 11/14, 15크레딧)에서 하고 결과를 재료로 넣음 → 실제 순서 9 → 6(교체판 설계도) → 7 → 8 → 10 → 11
- 원본 영상: 00_원본가져오기\출력\source.mp4 · 최종: 11_내보내기\출력\v1012_replica.mp4 · v1012_gen.mp4 · compare_원본_교체판.mp4
- 한 파일로 읽기: ..\단계별_입출력_설명.md (단계 README 합본)

| 단계 | 이름 | 실행 주체 | 지침 파일 | 출력 |
| --- | --- | --- | --- | --- |
| 00 | 원본가져오기 | Hypit 밖(파일 복사) | video-downloads.md | sha256.txt, source.mp4 |
| 01 | 원본확인 | Hypit 로직(ffmpeg) | reference-video.md | 01_probe.json, 01_probe.txt |
| 02 | 받아쓰기 | 음성 인식 모델(WhisperX, 로컬) | local-tools.md, reference-video.md | 02a_runtime-use.txt, 02b_runtime-up.txt, 02c_doctor.txt, 02d_transcribe.txt, 02e_runtime-down.txt, 02f_programs-down.txt, transcript.json |
| 03 | 화면변화후보 | Hypit 로직(픽셀 차이) | reference-video.md | 03_boundaries_r30.json, 03_boundaries_r30.txt, 후보판정.md |
| 04 | 프레임격자 | Hypit 로직(ffmpeg) | reference-video.md | 04a_tile_words_05s.txt, 04b_tiles_cuts_everyframe.txt, 04c_tile_ttalkkak.txt, 04d_tile_hook.txt, 04e_tile_endcard.txt, 04f_frames_full.txt, 04g_tile_proc.txt, evidence |
| 05 | 판단기록 | 에이전트(Claude) — Hypit 기능 없음 | SKILL.md, graphic-compositions.md, index.md, motion-graphics.md, narration-led-demo.md, reference-video.md, screen-demonstrations.md, sound-mix.md | ANALYSIS.md, PROGRESS.md, TIMELINE.md |
| 06 | 설계도작성 | 에이전트(Claude) | media.md, script-syntax.md | recipes_v1012.svs, v1012.svml, v1012.svrun, v1012_gen.svml, v1012_gen.svrun |
| 07 | 검사계획 | Hypit 로직 | builds.md | 07a_runtime-use.txt, 07b_runtime-up.txt, 07c_check.txt, 07d_plan.txt, gen_07a_runtime-use.txt, gen_07b_runtime-up.txt, gen_07c_check.txt, gen_07d_plan.txt |
| 08 | 준비정렬 | Hypit 로직 + 음성 모델(WhisperX) | media.md | 08_build.txt, ad-media_extent, alignment, gen_08_build.txt, 받아쓰기_정렬_대조.md |
| 09 | 재료생성 | 외부 생성 모델 — ByteDance Seedance 2.0 fast, Higgsfield MCP 경유(Hypit 밖, 2026-11-14) | generated-dependencies.md, image-direction.md, prompt-kits.md, video-direction.md | raw_05s.jpg, raw_cut23.jpg, seedance_raw.mp4, sheet.jpg, 결과.md, 생성영상_probe.txt |
| 10 | 렌더 | Hypit 로직(헤드리스 크롬 + ffmpeg) | rendering.md | caption-timing, gen_caption-timing, speech_ad, 자막시각표.md |
| 11 | 내보내기 | Hypit 로직 | builds.md | 11a_get_video.txt, 11b_inspect.txt, 11c_get_alignment.txt, 11d_runtime-down.txt, 11e_programs-down.txt, compare_원본_교체판.mp4, gen_05s.jpg, gen_11a_get_video.txt, gen_11b_inspect.txt, gen_11d_get_caption_timing.txt, gen_11e_runtime-down.txt, gen_11f_programs-down.txt, gen_full, replica_05s.jpg, replica_full, v1012_gen.mp4, v1012_replica.mp4 |
