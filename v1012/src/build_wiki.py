import json, os, re, sys

D = sys.argv[1]
OUT = os.path.join(D, 'wiki', 'hypit-v1012-wiki.md')
os.makedirs(os.path.dirname(OUT), exist_ok=True)


def rd(rel):
    with open(os.path.join(D, rel), encoding='utf-8') as f:
        return f.read()


def clean(s):
    s = s.replace('\r\n', '\n')
    s = s.replace('쨌', '·').replace('횞', '×').replace('?ㅽ썑', '오후').replace('?ㅼ쟾', '오전')
    s = re.sub(r"--project '[^']*'", '', s)
    s = re.sub(r"--runtime '[^']*'", '', s)
    s = re.sub(r'C:\\Users\\llm\\AppData\\Local\\Hypit\\programs\\[^\s]+', '(서버 프로그램 로그)', s)
    s = re.sub(r'C:[\\/]Users[\\/]llm[\\/]\.cache[^\s"]+', '(서버의 헤드리스 크롬)', s)
    s = s.replace('D:\\oss_eval\\hypit\\proj_serum\\references\\v1012\\', '')
    s = s.replace('D:\\oss_eval\\hypit\\proj_serum\\out\\v1012\\', '')
    s = s.replace('D:\\oss_eval\\hypit\\proj_serum\\', '')
    s = s.replace('D:\\oss_eval\\hypit\\proj_serum', '(프로젝트 폴더)')
    s = s.replace('references\\v1012\\', '').replace('out\\v1012\\', '')
    s = re.sub(r'(?m)^(\s*)\?\?', r'\1✓ ', s)
    s = s.replace(' ??', ' → ').replace('??', '→')
    return s.rstrip()


def io(name):
    t = clean(rd('io/' + name)).split('\n')
    return t[0], (t[1] if len(t) > 1 else ''), '\n'.join(t[2:])


def code(s, lang=''):
    s = s.rstrip('\n')
    fence = '````' if '```' in s else '```'
    return f'{fence}{lang}\n{s}\n{fence}\n'


def cmds(*cs):
    return code('\n'.join('$ ' + c for c in cs), 'bash')


def q(path, en, ko):
    return f'- 지침: `{path}`\n\n> {en}\n\n{ko}\n'


tx = json.loads(rd('transcript.json'))
tx['source'] = 'source.mp4'
words = [w for p in tx['passages'] for w in p['words']]
lines = ['{', f' "format": "{tx["format"]}",', ' "source": "source.mp4",', f' "language": "{tx["language"]}",', f' "audio_seconds": {tx["audio_seconds"]},', ' "passages": [']
for i, p in enumerate(tx['passages']):
    lines += ['  {', f'   "text": {json.dumps(p["text"], ensure_ascii=False)},', f'   "start_seconds": {p["start_seconds"]},', f'   "end_seconds": {p["end_seconds"]},', '   "words": [']
    lines += ['    ' + json.dumps(w, ensure_ascii=False, separators=(',', ':')) + (',' if j < len(p['words']) - 1 else '') for j, w in enumerate(p['words'])]
    lines += ['   ]', '  }' + (',' if i < len(tx['passages']) - 1 else '')]
lines += [' ]', '}']
tx_text = '\n'.join(lines)

bnd = json.loads(rd('io/03_boundaries_r30.json')); bnd['path'] = 'source.mp4'
probe = json.loads(rd('io/01_probe.json')); probe['path'] = 'source.mp4'
align = json.loads(rd('out/alignment/value.json')); av = align['value']
bmap = {b['id']: b['frame'] for b in av['boundaries']}
align_text = json.dumps(align, ensure_ascii=False, separators=(',', ':')).replace('{"frame"', '\n  {"frame"').replace('{"endBoundaryId"', '\n  {"endBoundaryId"')
cap = json.loads(rd('out/caption-timing/value.json'))
cap_text = json.dumps(cap, ensure_ascii=False, separators=(',', ':')).replace('{"endFrameExclusive"', '\n  {"endFrameExclusive"')
extent_text = json.dumps(json.loads(rd('out/ad-media_extent/value.json')), ensure_ascii=False, separators=(',', ':'))
window_text = json.dumps(json.loads(rd('out/speech_ad/value.json')), ensure_ascii=False, separators=(',', ':'))

c_use, _, _ = io('02a_runtime-use.txt'); c_up, m_up, _ = io('02b_runtime-up.txt'); c_doc, _, _ = io('02c_doctor.txt')
c_tr, m_tr, b_tr = io('02d_transcribe.txt'); c_bt, _, b_bt = io('03_boundaries_r30.txt')
tiles = [io(n) for n in ['04a_tile_words_05s.txt', '04b_tiles_cuts_everyframe.txt', '04c_tile_ttalkkak.txt', '04d_tile_hook.txt', '04e_tile_endcard.txt', '04f_frames_full.txt', '04g_tile_proc.txt']]
c_up2, _, _ = io('07b_runtime-up.txt'); c_ck, _, b_ck = io('07c_check.txt'); c_pl, _, b_pl = io('07d_plan.txt')
c_bd, _, b_bd = io('08_build.txt'); c_gv, _, b_gv = io('11a_get_video.txt'); c_in, _, b_in = io('11b_inspect.txt'); c_ga, _, b_ga = io('11c_get_alignment.txt')
build_id = re.search(r'bld_[0-9A-Za-z_]+', b_bd).group(0)
mean = sum(w['score'] for w in words) / len(words)

A = []
A.append('그림·영상이 들어간 원본 페이지: https://claude.ai/artifact/YQvnYNMrBGjjMjz6uqbnWd (비공개). 이 문서는 위키에 그림을 첨부할 수 없어 그림과 영상을 싣지 않는다. 이전 시험(세럼·오로나민C)은 「Hypit 단계별 데이터(입력·출력·외부 전송)」 페이지에 있다.\n')

A.append('## 1. 개요\n')
A.append('사용자가 준 애디렉트 「모두의 TV광고」 15초 영상을 Hypit 0.3.1 의 12단계(0–11)로 분석하고, 생성 모델 없이 원본 영상·소리에 낱말 맞춤 자막만 얹어 다시 렌더했다. 단계마다 따른 스킬 지침(md)과 쓴 명령, 실제 입력과 실제 출력 원문을 둔다. 진행 표시 로그와 서버 경로는 뺐다. 실행일은 2026-11-11, 실행 위치는 사내 GPU 서버(gpu103)이다.\n')
A.append('| 항목 | 값 |\n| --- | --- |\n| 원본 | 15.015초 · 1920×1080 · 29.97fps · 소리 있음 |\n| 받아쓰기 | 5구간 22어절, 인식 점수 평균 %.3f |\n| 화면 변화 후보 | 11개 → 실제 장면 바뀜 7번(장면 8개) |\n| 실행 요청 | 7개, 모두 로컬, 유료 0 |\n| 빌드 | %s, 56초, 450프레임 |\n| 결과 | 1920×1080 · 30fps · 15.0초 · 3,320,403 바이트 |\n' % (mean, build_id))

A.append('## 2. 전체 흐름\n')
A.append('| 순서 | 단계 | 이번 영상에서 한 일 | 실행 위치 |\n| --- | --- | --- | --- |\n'
         '| 1 읽기 | 0–4 | 15초 영상에서 낱말 22개의 시각, 화면 변화 후보 11개, 격자 그림 7장·모든 프레임 격자 10장·원본 해상도 낱장 11장을 뽑았다 | 로컬 |\n'
         '| 2 이해하기 | 5 | 에이전트가 자료를 보고 5박자 구성(브랜드 → 메타 훅 → 딸깍 → 자동 과정 → 혜택)과 유지할 관계 7개를 기록했다 | 에이전트 모델 |\n'
         '| 3 다시 적기 | 6 | 구조를 영상 코드(SVML)로 옮겼다. 이번에는 원본 그대로에 낱말 맞춤 자막만 얹었다 | 에이전트 모델 |\n'
         '| 4 비용 확인 | 7 | 요청 7개가 모두 로컬이고 요금은 0이다 | 로컬 |\n'
         '| 5 만들기 | 8–11 | 빌드 56초, 450프레임을 그려 15초 영상과 단어 정렬 22개를 얻었다 | 로컬(생성 0개) |\n')
A.append('데이터가 밖으로 나갈 수 있는 곳은 세 곳이다: 에이전트가 이해하고 적을 때(5·6단계), 음성 인식·정렬을 원격에 맡길 때(2·8단계), 재료를 생성할 때(9단계). 이번에는 첫 번째만 일어났다.\n')

A.append('## 3. 품질 확인 필요 사항\n')
A.append('이 문서는 무엇이 뽑히고 어디로 가는지를 보여 준다. 결과가 광고 제작에 쓸 만한지는 아래 항목을 사람이 확인해야 한다.\n')
A.append('| 항목 | 이번에 확인한 것 | 확인 방법 |\n| --- | --- | --- |\n'
         '| 받아쓰기 | 22개 중 2개 오인식(「안정」은 화면의 「한정」, 「애드렉트」는 「애디렉트」), 「딸깍!」 인식 점수 0.47. 대본 정렬은 바른 낱말에 맞게 붙었다 | 한국어 광고 여러 편을 사람이 대조 |\n'
         '| 컷 찾기 | 후보 11개 중 실제 장면 바뀜은 7번이고 4개는 같은 전환의 중복이다. 카드가 미끄러져 들어오는 변화 2번은 잡지 못했다 | 컷·전환이 많은 광고에서 놓친 것과 잘못 잡은 것을 집계 |\n'
         '| 판단 기록 | 사람이 검토하지 않았다. 배경 소리의 정체와 내레이션이 녹음인지 합성인지는 확인하지 못했다(Hypit 에 소리를 듣는 기능이 없다) | 제작 담당이 같은 영상을 보고 기록과 비교 |\n'
         '| 재현 영상 | 렌더는 됐다. 1.4–2.97초에는 원본 화면 글자 「지금 보시는 이 광고」와 같은 말이 자막으로 한 번 더 나온다. 광고로 쓸 수준인지는 평가하지 않았다 | 원본과 나란히 놓고 검수 기준으로 평가 |\n'
         '| 유료 생성 | 실행하지 않았다(요청 0개) | 비용 승인 후 한 편을 끝까지 생성 |\n')

A.append('## 4. 지침 지도\n')
A.append('모든 단계의 출발점은 스킬 `SKILL.md` 이고, 맨 아래 「Where the current question is answered」 표가 단계별 담당 md 를 가리킨다. 아래 지침 칸은 이번에 실제로 읽은 파일이다(경로는 `skills/hypit/references/` 아래). 서버에는 스킬이 설치돼 있지 않아 공개 저장소 hypit-ai/hypit 태그 v0.3.1 의 `skills/hypit` 원문(71개 파일)을 읽었다.\n')
A.append('| 단계 | 이름 | 지침(md) | 쓴 기능 |\n| --- | --- | --- | --- |\n'
         '| 0 | 원본 가져오기 | 해당 없음(파일을 직접 받음) | 파일 복사, SHA-256 대조 |\n'
         '| 1 | 원본 확인 | `creation/reference-video.md` | `hypit media probe` |\n'
         '| 2 | 받아쓰기 | `creation/reference-video.md`, `environment/local-tools.md` | `hypit runtime use`, `runtime up`, `doctor`, `transcribe --language ko` |\n'
         '| 3 | 화면 변화 후보 | `creation/reference-video.md` | `hypit media boundaries --rate 30` |\n'
         '| 4 | 프레임 격자 | `creation/reference-video.md` | `hypit media tile`, `tiles --every-frame --ranges`, `frames` |\n'
         '| 5 | 판단 기록 | `SKILL.md`(Understand and adapt), `creation/reference-video.md`, `playbooks/index.md`, `playbooks/formats/narration-led-demo.md`, craft 4종 | 에이전트 판단(Hypit 기능 없음), 보조로 ffmpeg 음량 측정 |\n'
         '| 6 | 대본·영상 코드 | `production/script-syntax.md`, `production/media.md`(11/05 코드 재사용) | SVML, SVRun, Recipe 작성 |\n'
         '| 7 | 검사·계획 | `production/builds.md` | `hypit check`, `hypit plan` |\n'
         '| 8 | 준비·정렬 | `production/media.md` | `hypit build` 안 요청 4개 |\n'
         '| 9 | 생성 | 이번에는 쓰지 않음 | 요청 0개 |\n'
         '| 10 | 렌더 | `production/rendering.md` | `hypit build` 안 요청 3개 |\n'
         '| 11 | 내보내기 | `production/builds.md` | `hypit get`, `inspect --verbose`, `runtime down`, `programs down` |\n')

A.append('## 5. 단계별 입력과 출력\n')

A.append('### 5.0 원본 가져오기(Hypit 밖, 외부 전송 없음)\n')
A.append('- 지침: 해당 없음. 링크로 받을 때는 `production/video-downloads.md` 의 `hypit download` 를 쓴다. 이번에는 사용자가 파일을 직접 줘서 서버로 복사만 했다.\n- 입력: 사용자 파일 `20261012134955001.mp4`(27,940,874 바이트)\n- 출력:\n')
A.append(code('SHA-256  3b34fa82a45599867565189fd1446525c002b1ab4afa48f755ecb0cd34261489  (이 PC)\nSHA-256  3B34FA82A45599867565189FD1446525C002B1AB4AFA48F755ECB0CD34261489  (서버 source.mp4)\n→ 같은 파일'))

A.append('### 5.1 원본 확인(로컬, 외부 전송 없음)\n')
A.append(q('creation/reference-video.md › Make time visible', '`probe` gives duration, dimensions, frame rate and audio presence;', '길이·크기·프레임률·소리 유무를 먼저 확인한다.'))
A.append('입력\n\n' + cmds('hypit media probe source.mp4', 'hypit media probe source.mp4 --json'))
A.append('출력\n\n' + code('15.015 s  1920×1080  29.97 fps  with audio') + code(json.dumps(probe, ensure_ascii=False, indent=2), 'json'))

A.append('### 5.2 받아쓰기(로컬 WhisperX, 외부 전송 없음)\n')
A.append(q('creation/reference-video.md › Make time visible', "Pass the reference's spoken language explicitly: `--language zh` for Chinese, `en` for English, `es` for Spanish, or `ko` for Korean.", '말이 있는 참고 영상은 `hypit transcribe` 로 낱말 시각을 얻고 언어를 반드시 지정한다. 로컬 WhisperX 준비는 `environment/local-tools.md` 담당이며, 이번에는 11/05 준비본을 그대로 썼다. CLI 설명은 「Establish word times with the WhisperX alignment Endpoint selected by the Runtime Profile.」이다.'))
A.append('입력\n\n' + cmds(c_use, c_up, c_doc, c_tr))
A.append('런타임 프로필(어느 기능을 어느 공급자가 맡는지). 음성 정렬을 `whisperx.local` 에 묶어 원격 전송이 없게 했다.\n\n')
A.append(code('{"format":"hypit.runtime-local@1","dataRoot":".hypit/runtimes/local",\n "credentials":{"local":{"use":"@hypit/credential-store-local"}},\n "endpoints":{"media.local":{"use":"@hypit/media-local","config":{"defaultConcurrency":2}},\n  "html.local":{"use":"@hypit/provider-html-local","config":{"workers":4,"quality":"standard","defaultConcurrency":1,"chromePath":"(서버의 헤드리스 크롬)"}},\n  "whisperx.local":{"use":"@hypit/provider-whisperx-local","config":{"expectedModel":"large-v3","expectedDevice":"cpu","expectedCompute":"int8","alignmentLanguages":["en","ko"]}}},\n "bindings":{"@hypit/whisperx@1#whisperx-alignment":"whisperx.local"}}', 'json'))
A.append(f'출력. 런타임 준비 {m_up.replace("exit=0 sec=", "")}초, 받아쓰기 {m_tr.replace("exit=0 sec=", "")}초, 인식 점수 평균 {mean:.3f}, 끝난 뒤 남은 프로세스 0개이다.\n\n' + code(b_tr))
A.append('출력 원문 `transcript.json`(저장 위치만 지움)\n\n' + code(tx_text, 'json'))
A.append('화면 글자와 비교한 오인식: 「안정」은 화면의 「기간한정」, 「애드렉트」는 「애디렉트」이다. 「딸깍!」 인식 점수는 0.47이다.\n')

A.append('### 5.3 화면 변화 후보(로컬, 외부 전송 없음)\n')
A.append(q('creation/reference-video.md › Make time visible', '`boundaries` locates abrupt visual changes worth inspecting;', '갑작스러운 화면 변화 후보를 찾는다. CLI 설명은 「Mechanical adjacent-frame change candidates with scores; never editorial shot labels.」이며 컷 판정은 하지 않는다.'))
A.append('입력(초당 30장, 기준값 기본 0.1)\n\n' + cmds(c_bt, c_bt + ' --json'))
A.append('출력\n\n' + code(b_bt) + code(json.dumps(bnd, ensure_ascii=False, indent=1), 'json'))
A.append('후보 11개를 5.4 의 모든 프레임 격자로 확인한 판정(에이전트)\n\n| 후보(초) | 점수 | 판정 |\n| --- | --- | --- |\n'
         '| 1.333 | 0.276 | 하드 컷 1.301→1.335(제목 장면 → 제품 컷) |\n'
         '| 2.967 | 0.306 | 하드 컷 2.936→2.970, 선택 상자와 커서는 컷을 넘어 이어짐 |\n'
         '| 4.667 | 0.472 | 하드 컷 4.638→4.671(AI generated → 업로드 화면) |\n'
         '| 6.333 | 0.300 | 하드 컷(「깍」 부근, 업로드 화면 → 병 든 인물) |\n'
         '| 7.233 | 0.283 | 하드 컷(인물 → 카드 화면) |\n'
         '| 8.433 | 0.101 | 컷 아님. 「AI 영상 생성」 카드 등장 |\n'
         '| 10.200, 10.233 | 0.133, 0.198 | 한 번의 전환. 카드 사진으로 확대 흐림 후 10.244 컷 |\n'
         '| 12.567, 12.600, 12.633 | 0.147, 0.190, 0.160 | 한 번의 전환. 로고 첫 글자 「애」가 크게 날아와 줄어들며 보라 배경으로 넘어감 |\n'
         '| 없음 | 0.1 미만 | 놓침. 약 7.8초 「스토리보드 작성」, 약 9.4초 「전문가 검수」 카드가 미끄러져 들어옴 |\n')

A.append('### 5.4 프레임 격자(로컬, Hypit 는 보내지 않음)\n')
A.append(q('creation/reference-video.md › Make time visible', 'For a close reading of motion, `frames --every-frame` and `tiles --every-frame` retain every original frame in the selected interval. ... Use `--ranges` with `tiles` to visit several intervals, and `--transcript` to read their word context.', '넓게(1초·0.5초) 보고, 좁게(0.25·0.1초) 보고, 모든 프레임으로 보는 순서로 범위와 간격을 바꾼다. `--transcript` 로 그때 들리는 낱말을 그림 아래 붙이고, `--around` 로 특정 말 앞뒤를 연다. 격자 그림은 5단계에서 에이전트 모델로 간다.'))
A.append('입력\n\n' + cmds(*[c for c, _, _ in tiles]))
A.append('범위 파일 `04_ranges.json`(후보 8곳 앞뒤 0.2초)\n\n' + code(rd('io/04_ranges.json').strip(), 'json'))
A.append('처음 `--end 15.015` 로 돌렸을 때 「no video frame exists at or after 15 s」로 실패했다. 마지막 프레임(14.98초)을 넘지 않게 `--end 15` 로 다시 실행했다.\n\n')
A.append('출력(그림은 원본 페이지에 있다)\n\n' + code('\n\n'.join(f'[{c.split(" --to ")[-1]}]  {m}\n{b}' for c, m, b in tiles)))

A.append('### 5.5 판단 기록(에이전트 모델, 외부 전송 있음)\n')
A.append(q('SKILL.md › Understand and adapt', 'Record the whole-piece explanation in Analysis and the timed details and their meaning in Timeline as you discover them.', '전체 해석은 ANALYSIS, 시각별 세부는 TIMELINE, 남은 확인은 PROGRESS 에 적는다.'))
A.append(q('creation/reference-video.md › Preserve a connected account', '`ANALYSIS.md` carries the whole-piece model ... `TIMELINE.md` carries time-locatable realization. Organize it into sections named by source-media time and a meaningful phase.', '사실과 해석을 구분하고, TIMELINE 은 원본 시각과 단계 이름으로 절을 나눈다.'))
A.append(q('playbooks/index.md › Formats → playbooks/formats/narration-led-demo.md', 'Read this when independent spoken narration carries a work or substantial passage while products, hands, screens, demonstrations, B-roll, Typography, or MG carry the picture.', '화면 속 인물은 말하지 않고 화면 밖 목소리가 뼈대이므로 「Narration-led work」 형식으로 읽었다. 기술 지침은 `craft/screen-demonstrations.md`, `motion-graphics.md`, `graphic-compositions.md`, `sound-mix.md` 의 도입과 절 제목까지 참고했다.'))
A.append('Hypit 에는 이 단계를 하는 기능이 없다. 판단은 전부 에이전트(Claude Opus 5.5) 몫이고 Hypit 는 1–4단계 근거와 기록 양식만 준다.\n\n')
A.append('입력\n\n- `transcript.json`(5.2 출력)\n- 화면 변화 후보 11개(5.3 출력)\n- 격자 그림 중 에이전트가 실제로 연 것 11장: whole_1s, words_05s, hook, 후보 1.333·2.967·4.667·10.2·12.6 모든 프레임, ttalkkak, process, endcard\n- Hypit 밖 보조 측정(ffmpeg volumedetect): 말 구간 평균 -10.0 dB, 말 없는 구간 -20.4 – -23.5 dB, 14.5–15초 -27.6 dB. 배경 소리가 끝까지 깔리며 음악인지 효과음인지는 구분하지 못했다.\n\n')
A.append('출력 원문 `ANALYSIS.md`\n\n' + code(rd('ANALYSIS.md'), 'markdown'))
A.append('출력 원문 `TIMELINE.md`\n\n' + code(rd('TIMELINE.md'), 'markdown'))
A.append('출력 원문 `PROGRESS.md`\n\n' + code(rd('PROGRESS.md'), 'markdown'))

A.append('### 5.6 대본·영상 코드 작성(에이전트 모델, 외부 전송 있음)\n')
A.append(q('production/script-syntax.md', '`이건 3개월 동안 만든 영상이에요.` — Korean word spaces; no space inside `3개월`.', '한국어 대본은 띄어쓰기를 그대로 쓴다. 대본의 `||` 는 자막 덩이 경계, `@{이름}…@{/이름}` 은 의미 구간(Selection)이다.'))
A.append(q('production/media.md', 'WhisperX supplies timed evidence; deterministic alignment associates it with Script.', '원본을 Normalize, whisperx:Alignment, semantic:Projection 순서로 잇는다.'))
A.append('틀은 11/05 세럼 재현 코드를 그대로 쓰고 한국어 자막, 16:9 캔버스, 보라 강조색만 바꿨다. 대본에는 화면 글자 기준 바른 낱말(「한정」 「애디렉트」)을 적었다.\n\n')
A.append('입력\n\n- ANALYSIS, TIMELINE(5.5 출력)\n- 요청: 원본 영상·소리 그대로 + 내레이션 낱말에 맞춘 한국어 자막(생성 모델 없음, 무료 범위)\n\n')
A.append('출력 `v1012.svml`\n\n' + code(rd('src/v1012.svml'), 'xml') + '출력 `v1012.svrun`\n\n' + code(rd('src/v1012.svrun'), 'xml') + '출력 `recipes_v1012.svs`\n\n' + code(rd('src/recipes_v1012.svs'), 'css'))

A.append('### 5.7 검사와 실행 계획(로컬, 외부 전송 없음)\n')
A.append(q('production/builds.md › Plan the selected Run', "`hypit plan` inspects an authored Run's execution demands.", '실행 전에 요청 목록, 맡는 공급자, 요금 표시를 확인한다. 유료 요청이 있으면 비용 승인 범위 안에서만 진행한다(같은 문서 「Work within the agreed paid scope」).'))
A.append('입력(`v1012.svrun` → `v1012.svml` + 런타임 프로필)\n\n' + cmds(c_up2, c_ck, c_pl))
A.append('출력\n\n' + code(b_ck) + code(b_pl))

A.append('### 5.8 재료 준비와 단어 정렬(로컬, 외부 전송 없음)\n')
A.append(q('production/media.md', 'The result `opening-semantic.alignment` is `NarrativeAlignment`: Segment and Token boundaries on the named local domain. It carries no media and no Timeline position.', '정렬 결과는 대본 낱말(토큰)마다 원본 프레임 경계를 단 값이다. 받아쓰기가 낱말을 다르게 적어도 대본 낱말에 맞춰진다(단조 동적 계획법, LLM 아님).'))
A.append('입력. 빌드가 이 단계에서 처리한 요청은 inspect-media, normalize-media, project-speech-evidence-audio, whisperx-alignment(language ko)이다.\n\n' + cmds(c_bd))
A.append(f'출력. 빌드 {build_id}, 요청 7개, 56초, 정규화 결과 450프레임 30fps.\n\n`ad-media.extent` 값\n\n' + code(extent_text, 'json'))
rows = ['| # | 받아쓰기 | 시각(초) | 점수 | 대본 토큰 | 프레임 | 시각(초) | 낱말 |', '| --- | --- | --- | --- | --- | --- | --- | --- |']
for i, t in enumerate(av['tokens']):
    s = bmap[t['startBoundaryId']]; e = bmap[t['endBoundaryId']]; w = words[i]
    rows.append(f'| {i+1} | {w["text"]} | {w["start_seconds"]:.2f}–{w["end_seconds"]:.2f} | {w["score"]} | {t["text"]} | {s}–{e} | {s/30:.2f}–{e/30:.2f} | {"다름" if w["text"].rstrip(".!") != t["text"] else ""} |')
A.append('받아쓰기(5.2)와 정렬 결과(5.8) 대조. 정렬은 대본 낱말에 시각을 붙인다.\n\n' + '\n'.join(rows) + '\n\n')
A.append('출력 원문 `ad-semantic.alignment` 의 `value.json`(토큰 22개, 경계 46개)\n\n' + code(align_text, 'json'))

A.append('### 5.9 재료 생성(선택, 이번 실행 요청 0개)\n')
A.append('이번 재현은 원본 영상을 그대로 써서 생성 단계를 쓰지 않았다. 사람·제품을 바꾸려면 이 단계에서 `craft/image-direction.md`, `video-direction.md`, `generated-dependencies.md` 지침으로 생성 요청을 쓴다. 영상 참조에는 사람 포함 여부(`person-reference`)를 반드시 표시해야 하며, 표시가 없으면 업로드 전에 거절된다. 입력과 출력은 없다.\n\n')

A.append('### 5.10 렌더(로컬, 외부 전송 없음)\n')
A.append(q('production/rendering.md', 'Film assembles the selected contributions with Timeline and Canvas into a Composition. Rendering evaluates that composition over a frame interval and produces the encoded media.', '영상·소리·자막 트랙을 Film 으로 묶고, HTML 프로그램을 헤드리스 크롬으로 프레임마다 그려 H.264 로 합친다.'))
A.append('입력. 빌드가 이 단계에서 처리한 요청은 rasterize-visual(450프레임), render-timeline-audio, mux-program-media 이다. 재료는 정규화 영상, 단어 정렬, 자막 레시피(`caption.top`), 글꼴 Noto Sans KR 800 이다.\n\n')
crow = ['| # | 낱말 | 프레임 | 시각(초) |', '| --- | --- | --- | --- |']
for i, u in enumerate(cap['value']['units']):
    crow.append(f'| {i+1} | {av["tokens"][i]["text"]} | {u["startFrame"]}–{u["endFrameExclusive"]} | {u["startFrame"]/30:.2f}–{u["endFrameExclusive"]/30:.2f} |')
A.append('출력 원문 `caption-timing` 의 `value.json`(자막 낱말 22개의 프레임 구간)\n\n' + '\n'.join(crow) + '\n\n' + code(cap_text, 'json') + '`speech.ad` 창 값\n\n' + code(window_text, 'json'))

A.append('### 5.11 내보내기(로컬, 외부 전송 없음)\n')
A.append(q('production/builds.md › Browse and export project Results', '`get` exports one named Output to one explicit destination: a Scalar becomes a JSON file; a Resource becomes one streamed file; a Composite becomes a directory containing `value.json` and its referenced Resources.', '영상은 파일 하나로, 정렬·자막 시각 같은 값은 `value.json` 폴더로 꺼낸다.'))
A.append('입력\n\n' + cmds(c_gv, c_in, c_ga, 'hypit runtime down', 'hypit programs down'))
A.append('출력(재현 영상은 원본 페이지에 있다)\n\n' + code(b_gv) + code(b_in) + code('final.video  h264 1920×1080 30fps 450프레임 · aac · 15.000초 · 3,320,403 바이트'))

A.append('## 6. 밖으로 나간 데이터\n')
A.append('| 지점 | 단계 | 나갈 수 있는 데이터 | 이번 실행 |\n| --- | --- | --- | --- |\n'
         '| 에이전트 판단·코드 작성 | 5, 6 | 받아쓰기 글, 격자 그림, 분석 기록, 스킬 원문 | Claude Opus 5.5 로 감(그림 11장, transcript, 기록) |\n'
         '| 음성 인식·정렬 원격 위탁 | 2, 8 | 소리 파일 업로드, 언어 | 없음. 로컬 WhisperX 에 묶음 |\n'
         '| 재료 생성 | 9 | 프롬프트, 설정, 참조 이미지·영상·소리 | 없음. 요청 0개 |\n'
         '| 점검·가격 조회 | 7 | 인증된 모델 목록·가격 조회 | 없음. 로컬 프로필 |\n')

md = '\n'.join(A)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(md)

# 위키 markdown 함정 점검: 코드 블록 밖 물결표·별표
inside = False; bad = []
for n, line in enumerate(md.split('\n'), 1):
    if line.startswith('```'):
        inside = not inside; continue
    if not inside and (line.count('~') >= 1 or line.count('*') >= 2):
        bad.append((n, line[:100]))
print('chars', len(md), 'bad lines', len(bad))
for b in bad[:20]:
    print(b)
