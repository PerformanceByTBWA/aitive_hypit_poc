import os, sys

OUT = sys.argv[1]  # 단계별 폴더

HEAD = '- 원문: 같은 폴더 지침\\ (영어, Hypit 0.3.1 스킬)\n- 구성: 따른 절 → 원문 핵심 문장(인용) → 한국어 풀이 → 이번 적용\n- 지침 = 에이전트용 설명서, hypit 프로그램은 읽지 않음\n'

G = {}

G['00_원본가져오기'] = '''# 00 원본 가져오기 — 지침 한국어 요약

{HEAD}
## video-downloads.md(이번엔 안 씀)

> Read this when a reference or source clip lives on a video page. `hypit download` saves the video as a project file through yt-dlp.

- 풀이: 참고 영상이 웹 페이지(링크)에 있을 때 `hypit download` 로 프로젝트 파일 저장(yt-dlp 사용)

> The command fetches one video, including its audio when available, even when the link also belongs to a playlist. It prefers H.264 and a resolution near 1080p

- 풀이: 재생목록 링크여도 영상 하나만, 소리 포함, H.264·1080p 근처 선호

## 이번 적용

- 사용자가 파일을 직접 줌 → 이 지침 안 씀
- 서버로 복사 후 SHA-256 지문으로 같은 파일 확인
'''

G['01_원본확인'] = '''# 01 원본 확인 — 지침 한국어 요약

{HEAD}
## reference-video.md › Make time visible

> The local `hypit media` commands expose the source at the scale needed: `probe` gives duration, dimensions, frame rate and audio presence;

- 풀이: 로컬 `hypit media` 명령으로 원본을 필요한 크기로 펼쳐 봄, probe = 길이·크기·프레임률·소리 유무

## 이번 적용

- `hypit media probe source.mp4 --json` → 15.015초 · 1920×1080 · 29.97fps · 소리 있음
'''

G['02_받아쓰기'] = '''# 02 받아쓰기 — 지침 한국어 요약

{HEAD}
## reference-video.md › Make time visible

> Use `hypit transcribe` when understanding a spoken reference. Its wording and word-level times give a strong starting point for following the argument and connecting speech to cuts, illustrations, reveals and emphasis.

- 풀이: 말이 있는 참고 영상은 `hypit transcribe` 사용, 낱말과 낱말별 시각이 「말 ↔ 컷·삽화·등장·강조」를 잇는 출발점

> Pass the reference's spoken language explicitly: `--language zh` for Chinese, `en` for English, `es` for Spanish, or `ko` for Korean.

- 풀이: 언어를 반드시 직접 지정(한국어 = ko)

> Small transcription errors can coexist with a clear understanding of what the passage means.

- 풀이: 작은 오인식이 있어도 뜻 이해는 가능, 화면 글자·맥락과 함께 해석

> WhisperX's recognized spelling reflects the recognizer's interpretation of the audio. Coined words and unfamiliar names are especially prone to substitutions, so a spelling difference alone cannot establish a pronunciation error.

- 풀이: 받아쓴 철자는 인식기의 해석, 만든 말·낯선 이름(상표명)은 잘못 적히기 쉬움, 철자 차이만으로 발음 오류라 단정 금지

## local-tools.md › Select local WhisperX explicitly

> Local and hosted WhisperX implement the same alignment capability. When local execution is chosen, merge this fragment into the Profile, retaining the other services the production uses

- 풀이: 로컬과 원격(HypiHub) WhisperX 는 같은 기능, 로컬을 고르면 프로필에 `whisperx.local` 조각 추가

## 이번 적용

- 11/05 프로필 그대로(large-v3 · CPU · int8 · en,ko, bindings 로 whisperx.local 지정) → 소리 외부 전송 없음
- `--language ko` 지정 → 22낱말 5문장
- 「애디렉트 → 애드렉트」「한정 → 안정」 = 지침이 말한 상표명·낯선 낱말 오인식 사례, 화면 글자로 바로잡아 해석
'''

G['03_화면변화후보'] = '''# 03 화면 변화 후보 — 지침 한국어 요약

{HEAD}
## reference-video.md › Make time visible

> `boundaries` locates abrupt visual changes worth inspecting;

- 풀이: 갑작스러운 화면 변화 중 「자세히 볼 가치가 있는 곳」 찾기(컷 판정 아님)

## reference-video.md › Read the whole through its details

> Camera boundaries help navigation; meaning and continuity determine which things belong together.

- 풀이: 화면 경계는 길 찾기용, 무엇이 한 덩어리인지는 의미·연속성으로 판단

> An object that survives a camera cut belongs to a system with a longer lifetime than that shot.

- 풀이: 컷을 넘어 살아남는 물체는 그 장면보다 오래 사는 장치

## 이번 적용

- 초당 30장 · 기준 0.1 → 후보 11개
- 4단계 모든 프레임 격자로 판정(출력\\후보판정.md): 실제 장면 바뀜 7번, 중복 4개, 놓친 카드 등장 2개
- 컷을 넘어 산 장치: 2.97초 컷을 넘은 선택 상자·커서, 10.24초부터 끝까지 남은 혜택 띠
'''

G['04_프레임격자'] = '''# 04 프레임 격자 — 지침 한국어 요약

{HEAD}
## reference-video.md › Make time visible

> `tile` and `tiles` arrange time-labeled frames for inspecting change, with optional word context;

- 풀이: tile·tiles = 시각이 적힌 프레임을 한 장에 모아 변화 확인, 낱말도 붙일 수 있음

> For a close reading of motion, `frames --every-frame` and `tiles --every-frame` retain every original frame in the selected interval.

- 풀이: 움직임을 자세히 볼 땐 구간의 모든 프레임 사용

> Use `--ranges` with `tiles` to visit several intervals, and `--transcript` to read their word context.

- 풀이: 여러 구간을 한 번에(--ranges), 그때 들리는 낱말 함께(--transcript)

> To inspect a spoken phrase, use `--around "the phrase" --transcript references/ad/transcript.json` in place of `--start` and `--end`.

- 풀이: 특정 말 앞뒤를 보려면 시각 대신 그 말로 지정(--around)

> Continuously adjust the viewed range, sampling interval and cell size to the question. Widen the range to understand an argument or a persistent system; narrow it and bring samples closer to trace an entrance, change or handoff; enlarge a frame to read its typography or spatial detail.

- 풀이: 질문에 맞춰 범위·간격·크기 계속 조정 — 흐름·오래 가는 장치는 넓게, 등장·변화·넘겨주기는 좁고 촘촘하게, 글자·위치는 크게

> Samples establish what appears at their times, with gaps between them. A wider overview can miss a brief event even when neighboring samples look unchanged.

- 풀이: 뽑은 그림은 그 순간만 증명, 간격 사이의 짧은 사건은 놓칠 수 있음

## 이번 적용

- 넓게: 전체 1초 · 0.5초(낱말 포함)
- 좁게: 0–3초 0.25초 · 「딸깍」 앞뒤 0.1초(--around) · 카드 구간 0.2초 · 끝 5초 0.25초
- 모든 프레임: 후보 8곳(--ranges, 04_ranges.json)
- 크게: 원본 해상도 낱장 11장(카드 글자 읽기)
- 넓은 격자에서 안 보이던 12.58–12.75초 「애」 글자 전환을 모든 프레임으로 확인 = 위 「놓칠 수 있음」 사례
'''

G['05_판단기록'] = '''# 05 판단 기록 — 지침 한국어 요약

{HEAD}
## SKILL.md › Understand and adapt

> Understand the whole reference and the designed behavior that makes it work. Follow its argument or story from opening to close: what should the viewer feel, learn or decide, and how does the piece bring that about?

- 풀이: 처음부터 끝까지 따라가며 「보는 사람이 무엇을 느끼고 알고 정하게 되나, 영상이 그걸 어떻게 해내나」 이해

> Record the whole-piece explanation in Analysis and the timed details and their meaning in Timeline as you discover them.

- 풀이: 전체 해석은 Analysis, 시각별 세부와 의미는 Timeline 에 발견하는 대로 기록

## reference-video.md › Read the whole through its details

> Each designed element deserves an account of its content and appearance, spatial relationship, entry, active behavior, persistence and exit.

- 풀이: 장치마다 내용·모양·위치·등장·움직임·지속·퇴장을 적음

> The useful result is an explanatory model for this commission: which relationships should remain when its person, product or wording changes, and which choices should be redesigned.

- 풀이: 결과물 = 사람·제품·문구가 바뀔 때 「유지할 관계」와 「다시 설계할 선택」을 설명하는 모델

> State what is visible or audible separately from what you infer it means.

- 풀이: 보이고 들리는 사실과 해석을 구분

## reference-video.md › Preserve a connected account · Turn understanding into new direction

> `ANALYSIS.md` carries the whole-piece model ... `TIMELINE.md` carries time-locatable realization. Organize it into sections named by source-media time and a meaningful phase.

- 풀이: ANALYSIS = 전체 모델, TIMELINE = 「원본 시각 · 단계 이름」 절로 나눈 시각별 실현

> Keep the current question, passages or systems still to examine, and next useful action in `PROGRESS.md`.

- 풀이: PROGRESS = 지금 질문 · 아직 볼 곳 · 다음 행동

## playbooks/index.md › Formats → formats/narration-led-demo.md

> Narration-led work — independent narration organizing products, hands, screens, demonstrations, montage, or MG

- 풀이: 형식 표에서 「독립 내레이션이 제품·손·화면·시연·몽타주·MG 를 이끄는 영상」 선택

> A narration-led passage is organized by accepted independent speech: audio-only A-roll. Its pictures are designed around that performance

- 풀이: 화면 밖 목소리(소리만 있는 A-roll)가 뼈대, 그림은 그 말에 맞춰 설계

> Build visual evidence, not noun illustration. Let each picture advance the argument.

- 풀이: 낱말마다 그림을 붙이지 말고 주장을 증명하는 그림으로

## craft 4종(도입·절 제목까지만 참고)

- screen-demonstrations.md: 「A screen can document an actual state, show an action with its consequence, or stage an explanation of a relationship.」 → 화면은 실제 상태 기록 / 동작과 결과 / 관계 설명 연출 중 하나
- motion-graphics.md: 절 「Direct the change, not just the entrance」 → 등장만이 아니라 바뀌는 과정을 연출
- graphic-compositions.md: 절 「Compose an idea, not a stack of decorations」 → 장식 쌓기가 아닌 생각 하나로 구성
- sound-mix.md: 절 「Start with the sound the material already carries」 → 재료가 이미 가진 소리부터 확인

## 이번 적용

- 형식 = 화면 밖 내레이션형, 핵심 해석 = 「광고 자신이 증거」(앞의 매끈한 화면을 커서가 집어 「AI generated」로 뒤집음)
- 업로드 화면·카드 = 실제 캡처보다 「관계 설명 연출」, 카드 쌓기·「무료」 테두리→채움 = 「바뀌는 상태」
- 사실/해석/새 방향(유지할 관계 7개) → ANALYSIS, 8구간 → TIMELINE, 남은 확인(배경 소리 정체 등) → PROGRESS
- 소리: Hypit 에 듣는 기능 없음 → ffmpeg 음량 측정으로 배경 소리 존재만 확인
'''

G['06_설계도작성'] = '''# 06 설계도 작성 — 지침 한국어 요약

{HEAD}
## script-syntax.md

> Correct a syntax error in the Source rather than changing authored wording or spaces.

- 풀이: 문법 오류는 문법으로 고치고, 적은 낱말·띄어쓰기는 바꾸지 않음

> Ordinary whitespace runs become one displayed/spoken space. ... `||` makes a Caption Cue handoff, and the Caption family controls visual line wrapping.

- 풀이: 여러 칸 공백은 한 칸, `||` = 자막 덩이 넘김, 줄바꿈은 자막 쪽이 결정

> `이건 3개월 동안 만든 영상이에요.` — Korean word spaces; no space inside `3개월`.

- 풀이: 한국어는 띄어쓰기 그대로 적음

> Do not ... infer Korean/English gaps from speech tokens. A space is display information, not an extra timed token.

- 풀이: 소리 토큰을 보고 띄어쓰기를 추측하지 않음, 공백은 표시 정보일 뿐 시각이 있는 토큰 아님

## media.md › Associate a performance with Script when its timing is consumed

> When Caption, semantic picture changes, sound events or another consumer needs their actual positions, alignment locates them on the accepted media's local domain

- 풀이: 자막·화면 변화·소리 사건이 실제 위치를 필요로 하면 정렬로 원본 위 위치를 찾음

> Combine the alignment, its complete local domain and the equal-length Window in one explicit semantic projection

- 풀이: 정렬 결과 + 원본 시간 영역 + 같은 길이의 시간 창을 하나의 투영(Projection)으로 묶음

## 이번 적용

- 대본 `지금 보시는 이 광고 || AI로 만들었어요. || …` 띄어쓰기 그대로, `||` 로 자막 덩이 10개, `@{ttalkkak}` · `@{offer}` 의미 구간
- 대본 낱말은 화면 글자 기준(「한정」 「애디렉트」) — 받아쓰기 오인식을 따르지 않음
- Normalize → whisperx:Alignment(language ko) → Timeline Window → semantic:Projection → 자막
- 틀은 11/05 세럼 재현 코드(입력\\틀_11월5일_serum.svml)
'''

G['07_검사계획'] = '''# 07 검사·계획 — 지침 한국어 요약

{HEAD}
## builds.md › Plan the selected Run

> `check` validates the self-described Sources and graph without executing them. `plan` freezes the demanded subgraph after applying the Run's Candidate selections and lists every external Need that would be sent. Planning starts no external work.

- 풀이: check = 실행 없이 설계도·연결 검사, plan = 실행할 작업을 확정하고 밖으로 나갈 요청을 전부 나열, 계획 단계에선 외부 작업 시작 안 함

> With a selected Runtime Profile, the plan also names the Endpoint behind each request ... and shows the Provider's declared price page or that its price source is unknown. Planning remains local and does not require a billing account to answer.

- 풀이: 프로필이 있으면 요청마다 맡는 곳과 가격 페이지(또는 「모름」)를 보여 줌, 계획은 로컬이라 결제 계정 없이도 됨

> `pricing` is an explicit read-only network operation. It creates no Build and submits no generation.

- 풀이: 가격 조회(`hypit pricing`)는 별도 명령, 읽기만 하고 생성 안 보냄

> Hypit itself calculates no total.

- 풀이: 총액은 Hypit 이 계산하지 않음 — 단가 × 길이·개수로 직접 계산

> A Caption or MG-only revision should keep its existing media generation satisfied

- 풀이: 자막·그래픽만 고칠 땐 이미 만든 생성 영상을 재사용해야 함(새 생성 요청이 보이면 실행 파일을 고침)

## builds.md › Work within the agreed paid scope

> Spending authority covers a described piece of work through the selected billing accounts and the cost or budget the user accepts.

- 풀이: 돈을 쓸 권한은 사용자가 받아들인 작업·계정·예산 안에서만

## 이번 적용

- check 통과, plan 요청 7개 전부 「local, no Provider charge」 → 유료 없음, pricing 안 돌림
'''

G['08_준비정렬'] = '''# 08 준비·정렬 — 지침 한국어 요약

{HEAD}
## media.md

> Normalization inspects the bytes and produces ... a SynchronizedMedia value with an exact local frame count, optional picture and optional audio on the chosen Clock. Audio is prepared as a 48 kHz render stem with its level preserved.

- 풀이: 정규화 = 파일을 검사해 정한 시계(30fps)로 정확한 프레임 수의 영상·소리 값 생성, 소리는 음량 그대로 48kHz

> WhisperX supplies timed evidence; deterministic alignment associates it with Script. The result ... is `NarrativeAlignment`: Segment and Token boundaries on the named local domain. It carries no media and no Timeline position.

- 풀이: WhisperX 는 시각 근거만 주고, 대본에 맞추는 건 결정적(같은 입력 = 같은 결과) 정렬 코드, 결과는 대본 토큰마다 원본 위 경계(영상도, 최종 시간 위치도 아님)

> Set `language` to the performed language supported by the selected WhisperX Endpoint.

- 풀이: 정렬 언어 = 실제로 말한 언어(ko)

## 이번 적용

- 원본 → 30fps 450프레임, 정렬용 소리 16kHz 모노(받아쓰기 증거용)
- 대본 22토큰 · 경계 46개, 소리가 「안정」이어도 대본 「한정」에 344–354프레임
- 2단계와의 차이: 2단계 = 무슨 말을 했나 알아내기, 8단계 = 우리 대본을 소리에 맞추기
'''

G['09_재료생성_이번없음'] = '''# 09 재료 생성(이번엔 안 씀) — 지침 한국어 요약

{HEAD}
- 이번 실행은 생성 요청 0개 → 아래는 「생성할 때 따를 지침」의 도입부 요약(본문 정독 안 함)

## video-direction.md(생성 영상 연출)

> Read this before writing or adapting a video prompt, performance Recipe or action. An image can establish who and where; generated video brings the Script and visual idea to life through speech, interaction, camera behavior or silent action.

- 풀이: 영상 프롬프트를 쓰기 전에 읽음, 이미지는 「누가·어디」, 생성 영상은 말·상호작용·카메라·무언 동작으로 대본을 살림
- 절 목록: 시간 흐름이 중요한 동작은 원본 영상이 운반 / 행동의 이유를 연출 / 절제에도 표현 목적 / 생성 장면 안에 행동 고정 / 인물 분리용 촬영 준비 / 입력마다 맡을 일 / 생성 관계 고르기 / 카메라·컷도 구간의 일부로 / 전달 길이에 맞춘 요청 길이

## image-direction.md(생성 이미지 연출)

> An image model can paint the visual world the work needs ... Each request directs a complete picture.

- 풀이: 이미지 모델은 필요한 세계를 그리는 화가, 요청마다 완성된 그림 한 장을 지시
- 절 목록: 문장마다 두 생각 / 네 문단 네 역할 / 발표자 이미지 7가지 질문 / 인물 캐스팅 / 대기 상태 / 쓰일 곳에 맞춘 구도 / 몇 가지 디테일로 장소 / 구체적 촬영 지시(phone-UGC 틀) / 참조가 맡을 사실

## generated-dependencies.md(참조 관계)

> Connected references bring useful visual memory into that request: a person's appearance, a product's form, a place's atmosphere and geometry, a camera relationship, or a physical state.

- 풀이: 참조는 사람 모습·제품 형태·장소 분위기와 구조·카메라 관계·물리 상태를 새 요청에 기억으로 가져옴

## prompt-kits.md(프롬프트 틀)

> A Prompt Kit is a data-only TextTemplate Source. It owns reusable wording and meaningful choices; it does not own a model, Provider, media reference, output size, or production workflow.

- 풀이: 프롬프트 틀 = 재사용 문장과 선택지만 가진 데이터 파일, 모델·공급자·참조·크기는 안 가짐
- Seedance 용 틀 = `@hypit/seedance-kits`(입력\\seedance-kits\\ 7종: 말하는 사람·팟캐스트·거리 인터뷰·영상 통화·무언 B-roll·움직임/카메라 따라 하기)

## 애디렉트에 쓸 때(예)

- 「병 든 인물」 컷 → video-direction 「입력마다 맡을 일」 + generated-dependencies 「새 그림마다 필요한 참조」, 틀 broll-v1(재질 product-beauty · 카메라 push-reveal 등)
'''

G['10_렌더'] = '''# 10 렌더 — 지침 한국어 요약

{HEAD}
## rendering.md

> Components author the picture and sound contributions. Film assembles the selected contributions with Timeline and Canvas into a Composition. Rendering evaluates that composition over a frame interval and produces the encoded media.

- 풀이: 부품이 화면·소리 몫을 만들고, Film 이 시간 틀·화면 크기와 함께 하나로 묶고(Composition), 렌더가 프레임 구간을 그려 영상 파일로

> Include every wanted output explicitly: placing the same normalized media in a Visual Clip and an Audio Clip is what makes both its picture and its audio present.

- 풀이: 원하는 층은 모두 명시 — 같은 영상을 화면 클립과 소리 클립 둘 다에 넣어야 그림과 소리가 함께 나옴

> Pure A-roll may need only one Visual Clip and one Audio Clip, with Caption when wanted.

- 풀이: 원본 한 편이면 화면 클립 1 + 소리 클립 1 + (원하면) 자막이면 충분

## 이번 적용

- Film = picture(원본 화면) + mix(원본 소리) + captions(낱말 맞춤 자막) 3층 → html:Video final
- 450프레임을 헤드리스 크롬으로 그리고 소리와 합침
'''

G['11_내보내기'] = '''# 11 내보내기 — 지침 한국어 요약

{HEAD}
## builds.md › Browse and export project Results

> `inspect` shows one Result's Targets, highlighted Outputs and outcome. ... `--verbose` to browse all available names and receipts.

- 풀이: inspect = 결과의 목표·출력·성공 여부, --verbose 면 모든 출력 이름과 영수증

> `get` exports one named Output to one explicit destination: a Scalar becomes a JSON file; a Resource becomes one streamed file; a Composite becomes a directory containing `value.json` and its referenced Resources.

- 풀이: get = 이름 붙은 출력 하나를 꺼냄 — 값 하나는 JSON 파일, 파일은 파일 그대로, 묶음은 value.json 이 든 폴더

> The original Result stays in the project's `.hypit/results` directory on the machine running Hypit.

- 풀이: 원래 결과는 Hypit 을 돌린 컴퓨터의 `.hypit/results` 에 남음, get 은 복사본

## 이번 적용

- `get final.video` → v1012_replica.mp4, `inspect --verbose` → 출력 14개, `get ad-semantic.alignment` → alignment\\value.json
- 끝에 `runtime down` + `programs down`(11/05 경험: runtime down 만으론 WhisperX 서버가 남음 — 지침 문장 아님)
'''

for d, text in G.items():
    p = os.path.join(OUT, d, '지침_한국어.md')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(text.replace('{HEAD}', HEAD).strip() + '\n')
    rp = os.path.join(OUT, d, 'README.md')
    with open(rp, encoding='utf-8') as f:
        r = f.read()
    if '지침_한국어.md' not in r:
        r = r.replace('## 지침(지침\\ 폴더', '## 지침 한국어 요약\n- 지침_한국어.md (따른 절의 원문 핵심 문장 + 한국어 풀이 + 이번 적용)\n\n## 지침(지침\\ 폴더', 1)
        with open(rp, 'w', encoding='utf-8') as f:
            f.write(r)
    print(d, os.path.getsize(p))

tp = os.path.join(OUT, 'README.md')
with open(tp, encoding='utf-8') as f:
    t = f.read()
if '지침_한국어.md' not in t:
    t = t.replace('- 원본 영상:', '- 단계 폴더마다 지침_한국어.md = 영문 지침 중 실제로 따른 절만 원문 핵심 문장 + 한국어 풀이 + 이번 적용\n- 원본 영상:', 1)
    with open(tp, 'w', encoding='utf-8') as f:
        f.write(t)
print('top README updated')
