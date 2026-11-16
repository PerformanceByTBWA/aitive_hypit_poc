import html, json, os, re, shutil, sys

D = sys.argv[1]
P = os.path.join(D, 'page')
M = os.path.join(P, 'media')
os.makedirs(M, exist_ok=True)


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
    s = s.replace('D:\\\\oss_eval\\\\hypit\\\\proj_serum\\\\references\\\\v1012\\\\', '')
    s = s.replace('D:\\oss_eval\\hypit\\proj_serum\\references\\v1012\\', '')
    s = s.replace('D:\\oss_eval\\hypit\\proj_serum\\out\\v1012\\', '')
    s = s.replace('D:\\oss_eval\\hypit\\proj_serum\\', '')
    s = s.replace('D:\\oss_eval\\hypit\\proj_serum', '(프로젝트 폴더)')
    s = s.replace('references\\v1012\\', '').replace('out\\v1012\\', '')
    s = re.sub(r'(?m)^(\s*)\?\?', r'\1✓ ', s)
    s = s.replace(' ??', ' → ').replace('??', '→')
    return s.rstrip()


def io(name, keep_cmd=True):
    t = clean(rd('io/' + name))
    lines = t.split('\n')
    cmd = lines[0]
    meta = lines[1] if len(lines) > 1 else ''
    body = '\n'.join(lines[2:])
    return cmd, meta, body


def esc(s):
    return html.escape(s, quote=False)


def pre(s, cls='code'):
    return f'<pre class="{cls}"><code>{esc(s)}</code></pre>'


def cmdline(s):
    return f'<pre class="cmd"><code>$ {esc(s)}</code></pre>'


IMGS = {
    'whole_1s.jpg': 'evidence/whole_1s.jpg',
    'words_05s.jpg': 'evidence/words_05s.jpg',
    'hook.jpg': 'evidence/hook.jpg',
    'cut_1333.jpg': 'evidence/cuts/001-c01_1333-p001.jpg',
    'cut_2967.jpg': 'evidence/cuts/002-c02_2967-p001.jpg',
    'cut_4667.jpg': 'evidence/cuts/003-c03_4667-p001.jpg',
    'cut_1020.jpg': 'evidence/cuts/007-c07_1020-p001.jpg',
    'cut_1260.jpg': 'evidence/cuts/008-c08_1260-p001.jpg',
    'ttalkkak.jpg': 'evidence/ttalkkak.jpg',
    'process.jpg': 'evidence/process.jpg',
    'endcard.jpg': 'evidence/endcard.jpg',
    'full_8200.jpg': 'evidence/full/frame-8_200s.jpg',
    'replica_05s.jpg': 'out/replica_05s.jpg',
    'source_web.mp4': 'out/v1012_source_web.mp4',
    'replica_web.mp4': 'out/v1012_replica_web.mp4',
}
for k, v in IMGS.items():
    shutil.copyfile(os.path.join(D, v), os.path.join(M, k))


def fig(name, cap):
    return (f'<figure><a href="media/{name}" target="_blank" rel="noopener"><img src="media/{name}" alt="{esc(cap)}" loading="lazy"></a>'
            f'<figcaption>{esc(cap)}</figcaption></figure>')


# ---------- data ----------
probe_json = clean(rd('io/01_probe.json'))
tx = json.loads(rd('transcript.json'))
tx['source'] = 'source.mp4'
words = [w for p in tx['passages'] for w in p['words']]


def tx_dump(t):
    out = ['{', f' "format": {json.dumps(t["format"])},', f' "source": {json.dumps(t["source"])},',
           f' "language": {json.dumps(t["language"])},', f' "audio_seconds": {t["audio_seconds"]},', ' "passages": [']
    for i, p in enumerate(t['passages']):
        out.append('  {')
        out.append(f'   "text": {json.dumps(p["text"], ensure_ascii=False)},')
        out.append(f'   "start_seconds": {p["start_seconds"]},')
        out.append(f'   "end_seconds": {p["end_seconds"]},')
        out.append('   "words": [')
        for j, w in enumerate(p['words']):
            out.append('    ' + json.dumps(w, ensure_ascii=False, separators=(',', ':')) + (',' if j < len(p['words']) - 1 else ''))
        out.append('   ]')
        out.append('  }' + (',' if i < len(t['passages']) - 1 else ''))
    out += [' ]', '}']
    return '\n'.join(out)


tx_text = tx_dump(tx)
bnd = json.loads(clean(rd('io/03_boundaries_r30.json')).replace('\\', '\\\\') if False else rd('io/03_boundaries_r30.json'))
bnd['path'] = 'source.mp4'
bnd_text = json.dumps(bnd, ensure_ascii=False, indent=1)
ranges_text = rd('io/04_ranges.json').strip()

align = json.loads(rd('out/alignment/value.json'))
av = align['value']
bmap = {b['id']: b['frame'] for b in av['boundaries']}
align_text = json.dumps(align, ensure_ascii=False, separators=(',', ':')).replace('{"frame"', '\n  {"frame"').replace('{"endBoundaryId"', '\n  {"endBoundaryId"')
cap = json.loads(rd('out/caption-timing/value.json'))
cap_text = json.dumps(cap, ensure_ascii=False, separators=(',', ':')).replace('{"endFrameExclusive"', '\n  {"endFrameExclusive"')
extent_text = json.dumps(json.loads(rd('out/ad-media_extent/value.json')), ensure_ascii=False, separators=(',', ':'))
window_text = json.dumps(json.loads(rd('out/speech_ad/value.json')), ensure_ascii=False, separators=(',', ':'))

runtime_profile = clean(rd('src/hypit.runtime.json')) if os.path.exists(os.path.join(D, 'src/hypit.runtime.json')) else None

# ASR vs alignment table
rows = []
for i, t in enumerate(av['tokens']):
    s = bmap[t['startBoundaryId']]; e = bmap[t['endBoundaryId']]
    w = words[i]
    diff = '' if w['text'].rstrip('.!') == t['text'] else '다름'
    rows.append(f'<tr><td>{i+1}</td><td>{esc(w["text"])}</td><td class="num">{w["start_seconds"]:.2f}–{w["end_seconds"]:.2f}</td><td class="num">{w["score"]}</td>'
                f'<td>{esc(t["text"])}</td><td class="num">{s}–{e}</td><td class="num">{s/30:.2f}–{e/30:.2f}</td><td>{diff}</td></tr>')
align_table = ''.join(rows)

cap_rows = []
for i, u in enumerate(cap['value']['units']):
    t = av['tokens'][i]['text'] if i < len(av['tokens']) else ''
    cap_rows.append(f'<tr><td>{i+1}</td><td>{esc(t)}</td><td class="num">{u["startFrame"]}–{u["endFrameExclusive"]}</td><td class="num">{u["startFrame"]/30:.2f}–{u["endFrameExclusive"]/30:.2f}</td></tr>')
cap_table = ''.join(cap_rows)

svml = rd('src/v1012.svml'); svrun = rd('src/v1012.svrun'); svs = rd('src/recipes_v1012.svs')
analysis = rd('ANALYSIS.md'); timeline = rd('TIMELINE.md'); progress = rd('PROGRESS.md')

c_use, m_use, b_use = io('02a_runtime-use.txt')
c_up, m_up, b_up = io('02b_runtime-up.txt')
c_doc, m_doc, b_doc = io('02c_doctor.txt')
c_tr, m_tr, b_tr = io('02d_transcribe.txt')
c_dn, m_dn, b_dn = io('02e_runtime-down.txt')
c_pd, m_pd, b_pd = io('02f_programs-down.txt')
c_bt, m_bt, b_bt = io('03_boundaries_r30.txt')
tiles = [io(n) for n in ['04a_tile_words_05s.txt', '04b_tiles_cuts_everyframe.txt', '04c_tile_ttalkkak.txt', '04d_tile_hook.txt', '04e_tile_endcard.txt', '04f_frames_full.txt', '04g_tile_proc.txt']]
c_ck, m_ck, b_ck = io('07c_check.txt')
c_pl, m_pl, b_pl = io('07d_plan.txt')
c_up2, m_up2, b_up2 = io('07b_runtime-up.txt')
c_bd, m_bd, b_bd = io('08_build.txt')
c_gv, m_gv, b_gv = io('11a_get_video.txt')
c_in, m_in, b_in = io('11b_inspect.txt')
c_ga, m_ga, b_ga = io('11c_get_alignment.txt')

build_id = re.search(r'bld_[0-9A-Za-z_]+', b_bd).group(0)

tiles_cmds = '\n'.join('$ ' + c for c, _, _ in tiles)
tiles_out = '\n\n'.join(f'[{c.split(" --to ")[-1]}]  {m}\n{b}' for c, m, b in tiles)


def stage(num, name, where, out_chip, guide, inp, outp, sid=None):
    sid = sid or f's{num}'
    return f'''
<section class="stage" id="{sid}">
  <header class="stage-head">
    <span class="stage-num">{num}</span>
    <h3>{name}</h3>
    <span class="chip">{where}</span>
    <span class="chip {'chip-out' if out_chip[0] else 'chip-none'}">{out_chip[1]}</span>
  </header>
  <div class="blk"><div class="blk-label">따른 지침·쓴 기능</div><div class="blk-body">{guide}</div></div>
  <div class="blk"><div class="blk-label">입력</div><div class="blk-body">{inp}</div></div>
  <div class="blk"><div class="blk-label">출력</div><div class="blk-body">{outp}</div></div>
</section>'''


def quote(path, en, ko):
    return f'<div class="guide"><div class="gpath">{esc(path)}</div><blockquote lang="en">{esc(en)}</blockquote><p>{ko}</p></div>'


S = []
S.append(stage(0, '원본 가져오기', 'Hypit 밖', (False, '외부 전송 없음'),
    '<p>해당 지침 없음. 링크로 받을 때는 <code>references/production/video-downloads.md</code> 의 <code>hypit download</code> 를 쓴다. 이번에는 사용자가 파일을 직접 줘서 서버로 복사만 했다.</p>',
    '<p>사용자 파일 <code>20261012134955001.mp4</code> (27,940,874 바이트)</p>',
    pre('SHA-256  3b34fa82a45599867565189fd1446525c002b1ab4afa48f755ecb0cd34261489  (이 PC)\nSHA-256  3B34FA82A45599867565189FD1446525C002B1AB4AFA48F755ECB0CD34261489  (서버 source.mp4)\n→ 같은 파일')))

S.append(stage(1, '원본 확인', '로컬', (False, '외부 전송 없음'),
    quote('references/creation/reference-video.md › Make time visible', '`probe` gives duration, dimensions, frame rate and audio presence;', '길이·크기·프레임률·소리 유무를 먼저 확인한다.'),
    cmdline('hypit media probe source.mp4') + cmdline('hypit media probe source.mp4 --json'),
    pre(clean(rd('io/01_probe.txt')).split('\n', 2)[-1] if False else '15.015 s  1920×1080  29.97 fps  with audio') + pre(probe_json)))

S.append(stage(2, '받아쓰기', '로컬 WhisperX', (False, '외부 전송 없음 (HypiHub 로 묶으면 소리 업로드)'),
    quote('references/creation/reference-video.md › Make time visible', 'Pass the reference\'s spoken language explicitly: `--language zh` for Chinese, `en` for English, `es` for Spanish, or `ko` for Korean.', '말이 있는 참고 영상은 <code>hypit transcribe</code> 로 낱말 시각을 얻고, 언어를 반드시 지정한다. 로컬 WhisperX 준비는 <code>references/environment/local-tools.md</code> 담당(이번에는 11/05 준비본을 그대로 씀).')
    + '<p class="note">CLI 설명: <code>hypit transcribe</code> = 「Establish word times with the WhisperX alignment Endpoint selected by the Runtime Profile.」</p>',
    cmdline(c_use) + cmdline(c_up) + cmdline(c_doc) + cmdline(c_tr)
    + '<p>런타임 프로필(어느 기능을 어느 공급자가 맡는지) — 음성 정렬을 <code>whisperx.local</code> 에 묶어 원격 전송이 없게 함</p>'
    + pre('{"format":"hypit.runtime-local@1","dataRoot":".hypit/runtimes/local",\n "credentials":{"local":{"use":"@hypit/credential-store-local"}},\n "endpoints":{"media.local":{"use":"@hypit/media-local","config":{"defaultConcurrency":2}},\n  "html.local":{"use":"@hypit/provider-html-local","config":{"workers":4,"quality":"standard","defaultConcurrency":1,"chromePath":"(서버의 헤드리스 크롬)"}},\n  "whisperx.local":{"use":"@hypit/provider-whisperx-local","config":{"expectedModel":"large-v3","expectedDevice":"cpu","expectedCompute":"int8","alignmentLanguages":["en","ko"]}}},\n "bindings":{"@hypit/whisperx@1#whisperx-alignment":"whisperx.local"}}'),
    f'<p class="meta">런타임 준비 {m_up.replace("exit=0 sec=", "")}초 · 받아쓰기 {m_tr.replace("exit=0 sec=", "")}초 · 인식 점수 평균 {sum(w["score"] for w in words)/len(words):.3f} · 끝난 뒤 남은 프로세스 0개</p>'
    + pre(b_tr) + '<p>출력 원문 <code>transcript.json</code> (저장 위치만 지움)</p>' + pre(tx_text, 'code tall')
    + '<p class="note">화면 글자와 비교한 오인식: 「안정」→ 화면 「기간한정」, 「애드렉트」→ 화면 「애디렉트」. 「딸깍!」 점수 0.47.</p>'))

bt_rows = ''.join(f'<tr><td class="num">{a}</td><td class="num">{b}</td><td>{c}</td></tr>' for a, b, c in [
    ('1.333', '0.276', '하드 컷 1.301→1.335 (제목 장면 → 제품 컷)'),
    ('2.967', '0.306', '하드 컷 2.936→2.970, 선택 상자·커서는 컷을 넘어 이어짐'),
    ('4.667', '0.472', '하드 컷 4.638→4.671 (AI generated → 업로드 화면)'),
    ('6.333', '0.300', '하드 컷 (「깍」 부근, 업로드 화면 → 병 든 인물)'),
    ('7.233', '0.283', '하드 컷 (인물 → 카드 화면)'),
    ('8.433', '0.101', '컷 아님. 「AI 영상 생성」 카드 등장'),
    ('10.200 · 10.233', '0.133 · 0.198', '한 번의 전환. 카드 사진으로 확대 흐림 → 10.244 컷'),
    ('12.567 · 12.600 · 12.633', '0.147 · 0.190 · 0.160', '한 번의 전환. 로고 첫 글자 「애」가 크게 날아와 줄어들며 보라 배경으로'),
    ('(없음)', '0.1 미만', '놓침: 약 7.8초 「스토리보드 작성」, 약 9.4초 「전문가 검수」 카드가 미끄러져 들어옴')])
S.append(stage(3, '화면 변화 후보', '로컬', (False, '외부 전송 없음'),
    quote('references/creation/reference-video.md › Make time visible', '`boundaries` locates abrupt visual changes worth inspecting;', '갑작스러운 화면 변화 후보를 찾는다. CLI 설명: 「Mechanical adjacent-frame change candidates with scores; never editorial shot labels.」 — 컷 판정은 하지 않는다.'),
    cmdline(c_bt) + cmdline(c_bt + ' --json') + '<p>설정: 초당 30장, 기준값 기본 0.1</p>',
    pre(b_bt) + pre(bnd_text)
    + '<p>후보 11개를 4단계 모든 프레임 격자로 확인한 판정(에이전트)</p>'
    + f'<div class="tbl"><table><thead><tr><th>후보(초)</th><th>점수</th><th>판정</th></tr></thead><tbody>{bt_rows}</tbody></table></div>'))

S.append(stage(4, '프레임 격자', '로컬', (False, 'Hypit 는 보내지 않음 (그림은 5단계에서 에이전트 모델로 감)'),
    quote('references/creation/reference-video.md › Make time visible', 'For a close reading of motion, `frames --every-frame` and `tiles --every-frame` retain every original frame in the selected interval. ... Use `--ranges` with `tiles` to visit several intervals, and `--transcript` to read their word context.', '넓게(1초·0.5초) → 좁게(0.25·0.1초) → 모든 프레임 순으로 범위·간격을 바꿔 가며 본다. <code>--transcript</code> 로 그때 들리는 낱말을 그림 아래 붙이고, <code>--around</code> 로 특정 말 앞뒤를 연다.'),
    pre(tiles_cmds.replace('$ ', '$ ', 1), 'cmd') + '<p>범위 파일 <code>04_ranges.json</code> (후보 8곳 ±0.2초)</p>' + pre(ranges_text)
    + '<p class="note">처음 <code>--end 15.015</code> 로 돌렸을 때 「no video frame exists at or after 15 s」로 실패 → 마지막 프레임(14.98초)을 넘지 않게 <code>--end 15</code> 로 다시 실행.</p>',
    pre(tiles_out, 'code')
    + '<div class="figs">'
    + fig('whole_1s.jpg', '전체 1초 간격 (whole_1s.jpg)')
    + fig('words_05s.jpg', '전체 0.5초 간격 + 낱말 (words_05s.jpg)')
    + fig('hook.jpg', '0–3초 0.25초 간격 (hook.jpg)')
    + fig('cut_2967.jpg', '후보 2.967초 모든 프레임 — 선택 상자가 컷을 넘어 이어짐')
    + fig('ttalkkak.jpg', '--around 「딸깍!」 0.1초 간격')
    + fig('process.jpg', '7.2–10.4초 0.2초 간격 — 카드 4장')
    + fig('cut_1020.jpg', '후보 10.2초 모든 프레임 — 카드 사진으로 확대 흐림 → 컷')
    + fig('endcard.jpg', '10–15초 0.25초 간격 — 혜택·엔드카드')
    + fig('cut_1260.jpg', '후보 12.6초 모든 프레임 — 「애」 글자 전환')
    + fig('full_8200.jpg', '원본 해상도 8.2초 — 카드 글자 읽기용')
    + '</div>'))

S.append(stage(5, '판단 기록', '에이전트 모델 (Claude Opus 5.5)', (True, '받아쓰기 글·격자 그림·스킬 원문이 에이전트 모델로'),
    quote('SKILL.md › Understand and adapt', 'Record the whole-piece explanation in Analysis and the timed details and their meaning in Timeline as you discover them.', '전체 해석은 ANALYSIS, 시각별 세부는 TIMELINE, 남은 확인은 PROGRESS 에 적는다.')
    + quote('references/creation/reference-video.md › Preserve a connected account', '`ANALYSIS.md` carries the whole-piece model ... `TIMELINE.md` carries time-locatable realization. Organize it into sections named by source-media time and a meaningful phase.', '사실과 해석을 구분하고, TIMELINE 은 「원본 시각 · 단계 이름」 절로 나눈다.')
    + quote('references/playbooks/index.md › Formats → formats/narration-led-demo.md', 'Read this when independent spoken narration carries a work or substantial passage while products, hands, screens, demonstrations, B-roll, Typography, or MG carry the picture.', '화면 속 인물은 말하지 않고 화면 밖 목소리가 뼈대 → 「Narration-led work」 형식으로 읽음. 기술 지침은 <code>craft/screen-demonstrations.md</code> · <code>motion-graphics.md</code> · <code>graphic-compositions.md</code> · <code>sound-mix.md</code> 의 도입과 절 제목까지 참고.')
    + '<p class="note">Hypit 에는 이 단계를 하는 기능이 없다. 판단은 전부 에이전트 몫이고 Hypit 는 1–4단계 근거와 기록 양식만 준다. 서버에 스킬이 설치돼 있지 않아 공개 저장소 hypit-ai/hypit v0.3.1 의 <code>skills/hypit</code> 원문(71개 파일)을 읽었다.</p>',
    '<ul class="plain"><li><code>transcript.json</code> (2단계 출력)</li><li>후보 11개 (3단계 출력)</li><li>격자 그림 중 에이전트가 실제로 연 것 11장: whole_1s · words_05s · hook · 후보 1.333·2.967·4.667·10.2·12.6 모든 프레임 · ttalkkak · process · endcard</li>'
    '<li>Hypit 밖 보조 측정: ffmpeg volumedetect — 말 구간 평균 -10.0 dB, 말 없는 구간 -20.4 ~ -23.5 dB, 14.5–15초 -27.6 dB (배경 소리가 끝까지 깔림, 음악·효과음 구분 못 함)</li></ul>',
    '<p>출력 원문 <code>ANALYSIS.md</code></p>' + pre(analysis, 'code tall') + '<p>출력 원문 <code>TIMELINE.md</code></p>' + pre(timeline, 'code tall') + '<p>출력 원문 <code>PROGRESS.md</code></p>' + pre(progress)))

S.append(stage(6, '대본·영상 코드 작성', '에이전트 모델', (True, '분석 기록과 요청 내용이 에이전트 모델로'),
    quote('references/production/script-syntax.md', '`이건 3개월 동안 만든 영상이에요.` → Korean word spaces; no space inside `3개월`.', '한국어 대본은 띄어쓰기를 그대로 쓴다. <code>||</code> 는 자막 덩이 경계, <code>@{이름}…@{/이름}</code> 은 의미 구간(Selection).')
    + quote('references/production/media.md', 'WhisperX supplies timed evidence; deterministic alignment associates it with Script.', '원본을 Normalize → whisperx:Alignment → semantic:Projection 으로 잇는 구조.')
    + '<p class="note">틀은 11/05 세럼 재현 코드(serum.svml)를 그대로 쓰고 한국어 자막·16:9 캔버스·보라 강조색만 바꿨다. 대본에는 화면 글자 기준 바른 낱말(「한정」 「애디렉트」)을 적었다.</p>',
    '<ul class="plain"><li>ANALYSIS · TIMELINE (5단계 출력)</li><li>요청: 원본 영상·소리 그대로 + 내레이션 낱말에 맞춘 한국어 자막 (생성 모델 없음, 무료 범위)</li></ul>',
    '<p><code>v1012.svml</code></p>' + pre(svml, 'code tall') + '<p><code>v1012.svrun</code></p>' + pre(svrun) + '<p><code>recipes_v1012.svs</code></p>' + pre(svs, 'code tall')))

S.append(stage(7, '검사와 실행 계획', '로컬', (False, '외부 전송 없음 (유료 요청이 있으면 여기서 공급자·가격 페이지와 함께 나열)'),
    quote('references/production/builds.md › Plan the selected Run', '`hypit plan` inspects an authored Run\'s execution demands.', '실행 전에 요청 목록·맡는 공급자·요금 표시를 확인한다. 유료 요청이 있으면 비용 승인 범위 안에서만 진행(같은 문서 「Work within the agreed paid scope」).'),
    cmdline(c_up2) + cmdline(c_ck) + cmdline(c_pl) + '<p>입력 파일: <code>v1012.svrun</code> → <code>v1012.svml</code> + 런타임 프로필(2단계와 같음)</p>',
    pre(b_ck) + pre(b_pl, 'code tall')))

S.append(stage(8, '재료 준비와 단어 정렬', '로컬 (빌드 안 요청 4개)', (False, '외부 전송 없음 (정렬을 HypiHub 에 맡기면 소리 업로드)'),
    quote('references/production/media.md', 'The result `opening-semantic.alignment` is `NarrativeAlignment`: Segment and Token boundaries on the named local domain. It carries no media and no Timeline position.', '정렬 결과는 대본 낱말(토큰)마다 원본 프레임 경계를 단 값이다. 받아쓰기가 낱말을 다르게 적어도 대본 낱말에 맞춰진다(단조 동적 계획법, LLM 아님).'),
    cmdline(c_bd) + '<p>빌드가 이 단계에서 처리한 요청: inspect-media · normalize-media · project-speech-evidence-audio · whisperx-alignment (language ko)</p>',
    f'<p class="meta">빌드 {esc(build_id)} · 요청 7개 · 56초 · 정규화 결과 450프레임 30fps</p>'
    + '<p><code>ad-media.extent</code> 값</p>' + pre(extent_text)
    + '<p>받아쓰기(2단계)와 정렬 결과(8단계) 대조 — 정렬은 대본 낱말에 시각을 붙임</p>'
    + f'<div class="tbl"><table><thead><tr><th>#</th><th>받아쓰기</th><th>시각(초)</th><th>점수</th><th>대본 토큰</th><th>프레임</th><th>시각(초)</th><th>낱말</th></tr></thead><tbody>{align_table}</tbody></table></div>'
    + '<p>출력 원문 <code>ad-semantic.alignment</code> → <code>value.json</code> (토큰 22개, 경계 46개)</p>' + pre(align_text, 'code tall')))

S.append(stage(9, '재료 생성(선택)', '외부 유료', (False, '이번 실행 요청 0개 — 전송·요금 없음'),
    '<p>이번 재현은 원본 영상을 그대로 써서 생성 단계를 쓰지 않았다. 사람·제품을 바꾸려면 이 단계에서 <code>craft/image-direction.md</code> · <code>video-direction.md</code> · <code>generated-dependencies.md</code> 지침으로 생성 요청을 쓴다. 영상 참조에는 사람 포함 여부(<code>person-reference</code>)를 반드시 표시해야 하고, 표시가 없으면 업로드 전에 거절된다.</p>',
    '<p>없음</p>', '<p>없음</p>'))

S.append(stage(10, '렌더', '로컬 (빌드 안 요청 3개)', (False, '외부 전송 없음'),
    quote('references/production/rendering.md', 'Film assembles the selected contributions with Timeline and Canvas into a Composition. Rendering evaluates that composition over a frame interval and produces the encoded media.', '영상·소리·자막 트랙을 Film 으로 묶고, HTML 프로그램을 헤드리스 크롬으로 프레임마다 그려 H.264 로 합친다.'),
    '<p>빌드가 이 단계에서 처리한 요청: rasterize-visual (450프레임) · render-timeline-audio · mux-program-media</p><p>입력: 정규화 영상 · 단어 정렬 · 자막 레시피(<code>caption.top</code>) · 글꼴 Noto Sans KR 800</p>',
    '<p>출력 원문 <code>caption-timing</code> → <code>value.json</code> (자막 낱말 22개의 프레임 구간)</p>'
    + f'<div class="tbl"><table><thead><tr><th>#</th><th>낱말</th><th>프레임</th><th>시각(초)</th></tr></thead><tbody>{cap_table}</tbody></table></div>'
    + pre(cap_text, 'code') + '<p><code>speech.ad</code> 창 값</p>' + pre(window_text)))

S.append(stage(11, '내보내기', '로컬', (False, '외부 전송 없음'),
    quote('references/production/builds.md › Browse and export project Results', '`get` exports one named Output to one explicit destination: a Scalar becomes a JSON file; a Resource becomes one streamed file; a Composite becomes a directory containing `value.json` and its referenced Resources.', '영상은 파일 하나로, 정렬·자막 시각 같은 값은 <code>value.json</code> 폴더로 꺼낸다.'),
    cmdline(c_gv) + cmdline(c_in) + cmdline(c_ga) + cmdline('hypit runtime down') + cmdline('hypit programs down'),
    pre(b_gv) + pre(b_in, 'code') + pre('final.video  h264 1920×1080 30fps 450프레임 · aac · 15.000초 · 3,320,403 바이트')
    + '<div class="vids"><figure><video controls preload="metadata" src="media/replica_web.mp4"></video><figcaption>재현 결과(웹용 960 폭으로 다시 인코딩)</figcaption></figure></div>'
    + fig('replica_05s.jpg', '재현 결과 0.5초 간격 — 위쪽 가운데 자막')))

nav = ''.join(f'<li><a href="#s{n}"><span class="num">{n}</span>{t}</a></li>' for n, t in [
    (0, '원본 가져오기'), (1, '원본 확인'), (2, '받아쓰기'), (3, '화면 변화 후보'), (4, '프레임 격자'), (5, '판단 기록'),
    (6, '대본·영상 코드'), (7, '검사·계획'), (8, '준비·정렬'), (9, '생성(선택)'), (10, '렌더'), (11, '내보내기')])

guide_map = ''.join(f'<tr><td class="num">{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in [
    ('0', '원본 가져오기', '(해당 없음 — 파일 직접 받음)', '파일 복사·SHA-256 대조'),
    ('1', '원본 확인', 'creation/reference-video.md', '<code>hypit media probe</code>'),
    ('2', '받아쓰기', 'creation/reference-video.md · environment/local-tools.md', '<code>hypit runtime use/up</code> · <code>doctor</code> · <code>transcribe --language ko</code>'),
    ('3', '화면 변화 후보', 'creation/reference-video.md', '<code>hypit media boundaries --rate 30</code>'),
    ('4', '프레임 격자', 'creation/reference-video.md', '<code>hypit media tile</code> · <code>tiles --every-frame --ranges</code> · <code>frames</code>'),
    ('5', '판단 기록', 'SKILL.md › Understand and adapt · creation/reference-video.md · playbooks/index.md → formats/narration-led-demo.md · craft 4종', '에이전트 판단 (Hypit 기능 없음) + ffmpeg 음량 측정(보조)'),
    ('6', '대본·영상 코드', 'production/script-syntax.md · production/media.md (+11/05 코드 재사용)', 'SVML · SVRun · Recipe 작성'),
    ('7', '검사·계획', 'production/builds.md', '<code>hypit check</code> · <code>hypit plan</code>'),
    ('8', '준비·정렬', 'production/media.md', '<code>hypit build</code> 안 요청 4개'),
    ('9', '생성', '(이번엔 안 씀)', '요청 0개'),
    ('10', '렌더', 'production/rendering.md', '<code>hypit build</code> 안 요청 3개'),
    ('11', '내보내기', 'production/builds.md', '<code>hypit get</code> · <code>inspect --verbose</code> · <code>runtime down</code> · <code>programs down</code>')])

flow = ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in [
    ('1 읽기', '0–4', '15초 영상 → 낱말 22개의 시각, 화면 변화 후보 11개, 격자 그림 7장·모든 프레임 격자 10장·원본 해상도 11장', '로컬'),
    ('2 이해하기', '5', '에이전트가 자료를 보고 5박자 구성(브랜드 → 메타 훅 → 딸깍 → 자동 과정 → 혜택)과 유지할 관계 7개를 기록', '에이전트 모델'),
    ('3 다시 적기', '6', '구조를 영상 코드(SVML)로 옮김. 이번엔 원본 그대로 + 낱말 맞춤 자막', '에이전트 모델'),
    ('4 비용 확인', '7', '요청 7개 모두 로컬, 요금 0', '로컬'),
    ('5 만들기', '8–11', '빌드 56초, 450프레임 → 15초 1920×1080 영상 + 단어 정렬 22개', '로컬 (생성 0개)')])

quality = ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in [
    ('받아쓰기', '22개 중 2개 오인식(「안정」 「애드렉트」), 「딸깍!」 점수 0.47. 대본 정렬은 바른 낱말에 맞게 붙음', '한국어 광고 여러 편을 사람이 대조'),
    ('컷 찾기', '후보 11개 = 실제 장면 바뀜 7번 + 같은 전환의 중복 4개, 카드 등장 2번은 못 잡음', '컷·전환이 많은 광고에서 놓친 것·잘못 잡은 것 집계'),
    ('판단 기록', '사람 검토 없음. 배경 소리의 정체, 내레이션이 녹음인지 합성인지 확인 못 함(Hypit 에 소리 듣는 기능 없음)', '제작 담당이 같은 영상을 보고 기록과 비교'),
    ('재현 영상', '렌더는 됨. 1.4–2.97초에는 원본 화면 글자 「지금 보시는 이 광고」와 같은 말이 자막으로 한 번 더 나옴. 광고로 쓸 수준인지 평가 안 함', '원본과 나란히 놓고 검수 기준으로 평가'),
    ('유료 생성', '실행 안 함(요청 0개)', '비용 승인 후 한 편을 끝까지 생성')])

css = r'''
:root{
  /* 레이아웃: 왼쪽 단계 목차(넓은 화면에서 고정) + 오른쪽 단계별 지침·입력·출력 */
  --bg:#F6F5F9; --surface:#FFFFFF; --ink:#1C1930; --muted:#5D5970; --line:#E2DFEA;
  --accent:#4A2FD0; --accent-weak:#ECE8FF; --code-bg:#F0EEF5; --out:#9A4A00; --out-weak:#FFF1E2;
  --f-body:"IBM Plex Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
  --f-mono:"IBM Plex Mono", ui-monospace, "Cascadia Mono", Consolas, monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#121019; --surface:#1A1724; --ink:#ECEAF4; --muted:#A7A2BB; --line:#2D2939;
  --accent:#A495FF; --accent-weak:#2A2448; --code-bg:#16131F; --out:#F0B060; --out-weak:#3A2A14; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#121019; --surface:#1A1724; --ink:#ECEAF4; --muted:#A7A2BB; --line:#2D2939;
  --accent:#A495FF; --accent-weak:#2A2448; --code-bg:#16131F; --out:#F0B060; --out-weak:#3A2A14; color-scheme:dark}
body{background:var(--bg);color:var(--ink);font-family:var(--f-body);font-size:15.5px;line-height:1.65}
.wrap{max-width:1180px;margin:0 auto;padding-block:28px 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;grid-template-columns:200px minmax(0,1fr);gap:36px}
nav.toc{position:sticky;top:calc(env(safe-area-inset-top,0px) + 16px);align-self:start;font-size:13.5px}
nav.toc h2{font-size:12px;letter-spacing:.08em;color:var(--muted);margin:0 0 8px;font-weight:500}
nav.toc ul{list-style:none;margin:0;padding:0;display:grid;gap:2px}
nav.toc a{display:flex;gap:10px;padding:5px 8px;border-radius:6px;color:var(--ink);text-decoration:none}
nav.toc a:hover,nav.toc a:focus-visible{background:var(--accent-weak);outline:none}
nav.toc .num{font-family:var(--f-mono);color:var(--accent);min-width:1.6em;font-variant-numeric:tabular-nums}
main{min-width:0}
.eyebrow{font-family:var(--f-mono);font-size:12.5px;color:var(--accent);letter-spacing:.04em;margin:0}
h1{font-size:30px;line-height:1.3;margin:6px 0 10px;text-wrap:balance;font-weight:700}
h2{font-size:21px;margin:44px 0 12px;text-wrap:balance}
h3{font-size:18px;margin:0}
p{margin:0 0 10px;max-width:72ch}
.lede{color:var(--muted);max-width:72ch}
.facts{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 4px;padding:0;list-style:none}
.facts li{font-family:var(--f-mono);font-size:13px;padding:5px 10px;border:1px solid var(--line);border-radius:6px;background:var(--surface);font-variant-numeric:tabular-nums}
.vids{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin:18px 0}
video{width:100%;max-width:100%;display:block;border-radius:8px;background:#000}
figure{margin:0}
figcaption{font-size:13px;color:var(--muted);margin-top:6px}
.tbl{overflow-x:auto;margin:8px 0 14px;border:1px solid var(--line);border-radius:8px;background:var(--surface)}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-weight:500;color:var(--muted);font-size:12.5px;white-space:nowrap;background:var(--code-bg)}
tr:last-child td{border-bottom:0}
td.num{font-family:var(--f-mono);font-variant-numeric:tabular-nums;white-space:nowrap}
code{font-family:var(--f-mono);font-size:.88em;background:var(--code-bg);padding:1px 5px;border-radius:4px}
pre{margin:8px 0 12px;background:var(--code-bg);border:1px solid var(--line);border-radius:8px;padding:12px 14px;overflow:auto;max-height:340px;font-size:12.8px;line-height:1.55}
pre code{background:none;padding:0;font-size:inherit;white-space:pre}
pre.tall{max-height:520px}
pre.cmd{max-height:none;border-left:3px solid var(--accent)}
.stage{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:20px 22px;margin:0 0 18px;scroll-margin-top:16px}
.stage-head{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;margin-bottom:14px}
.stage-num{font-family:var(--f-mono);font-size:15px;color:var(--accent);border:1.5px solid var(--accent);border-radius:6px;min-width:30px;text-align:center;padding:1px 6px;font-variant-numeric:tabular-nums}
.chip{font-size:12.5px;padding:3px 9px;border-radius:999px;background:var(--code-bg);color:var(--muted)}
.chip-out{background:var(--out-weak);color:var(--out)}
.blk{display:grid;grid-template-columns:120px minmax(0,1fr);gap:14px;padding:12px 0;border-top:1px dashed var(--line)}
.blk-label{font-size:13px;font-weight:500;color:var(--muted);padding-top:2px}
.blk-body{min-width:0}
.guide{margin:0 0 12px}
.gpath{font-family:var(--f-mono);font-size:12.5px;color:var(--accent);margin-bottom:4px;word-break:break-all}
blockquote{margin:0 0 6px;padding:6px 12px;border-left:3px solid var(--line);color:var(--muted);font-size:13.5px;font-style:italic}
.note{font-size:13.5px;color:var(--muted)}
.meta{font-family:var(--f-mono);font-size:13px}
ul.plain{margin:0;padding-left:18px}
ul.plain li{margin:2px 0}
.figs{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px;margin-top:12px}
.figs img,figure img{width:100%;height:auto;border-radius:6px;border:1px solid var(--line);display:block}
a{color:var(--accent)}
@media (max-width:920px){.wrap{grid-template-columns:minmax(0,1fr)}nav.toc{position:static}nav.toc ul{grid-template-columns:repeat(auto-fill,minmax(140px,1fr))}}
@media (max-width:560px){.blk{grid-template-columns:minmax(0,1fr);gap:4px}.stage{padding:16px 14px}h1{font-size:24px}}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto}}
html{scroll-behavior:smooth}
'''

page = f'''<title>애디렉트 15초 Hypit 기록</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+KR:wght@400;500;700&display=swap">
<style>{css}</style>
<div class="wrap">
<nav class="toc" aria-label="단계 목차"><h2>단계</h2><ul>
<li><a href="#flow"><span class="num">·</span>쉬운 흐름</a></li><li><a href="#quality"><span class="num">·</span>품질 확인 필요</a></li><li><a href="#map"><span class="num">·</span>지침 지도</a></li>
{nav}<li><a href="#outbound"><span class="num">·</span>밖으로 나간 데이터</a></li></ul></nav>
<main>
<p class="eyebrow">Hypit 0.3.1 · 2026-11-11 · gpu103 로컬 실행</p>
<h1>애디렉트 15초 광고를 Hypit 흐름으로 읽고 다시 만든 기록</h1>
<p class="lede">사용자가 준 애디렉트 「모두의 TV광고」 15초 영상을 Hypit 의 12단계(0–11)로 분석하고, 생성 모델 없이 원본 + 낱말 맞춤 자막으로 다시 렌더했다. 단계마다 따른 스킬 지침(md)과 쓴 명령, 실제 입력과 실제 출력 원문을 둔다. 실행 로그 중 진행 표시와 서버 경로는 뺐다.</p>
<ul class="facts"><li>15.015초 · 1920×1080 · 29.97fps</li><li>낱말 22개 · 5구간</li><li>화면 변화 후보 11 → 장면 8</li><li>요청 7개 모두 로컬</li><li>유료 요청 0</li><li>빌드 56초</li></ul>
<div class="vids">
<figure><video controls preload="metadata" src="media/source_web.mp4"></video><figcaption>원본 (웹용 960 폭으로 다시 인코딩)</figcaption></figure>
<figure><video controls preload="metadata" src="media/replica_web.mp4"></video><figcaption>Hypit 재현 — 원본 영상·소리 + 낱말 맞춤 자막</figcaption></figure>
</div>

<h2 id="flow">쉬운 흐름</h2>
<div class="tbl"><table><thead><tr><th>순서</th><th>단계</th><th>이번 영상에서 한 일</th><th>실행 위치</th></tr></thead><tbody>{flow}</tbody></table></div>
<p class="note">데이터가 밖으로 나갈 수 있는 곳은 세 곳이다: 에이전트가 이해하고 적을 때(5·6단계), 음성 인식·정렬을 원격에 맡길 때(2·8단계), 재료를 생성할 때(9단계). 이번에는 첫 번째만 일어났다.</p>

<h2 id="quality">품질 확인 필요</h2>
<p>이 기록은 무엇이 뽑히고 어디로 가는지를 보여 준다. 결과가 광고 제작에 쓸 만한지는 아래 항목을 사람이 확인해야 한다.</p>
<div class="tbl"><table><thead><tr><th>항목</th><th>이번에 확인한 것</th><th>확인 방법</th></tr></thead><tbody>{quality}</tbody></table></div>

<h2 id="map">지침 지도</h2>
<p>모든 단계의 출발점은 스킬 <code>SKILL.md</code> 이고, 맨 아래 「Where the current question is answered」 표가 단계별 담당 md 를 가리킨다. 아래 「지침」 칸은 이번에 실제로 읽은 파일이다(경로는 <code>skills/hypit/references/</code> 아래).</p>
<div class="tbl"><table><thead><tr><th>단계</th><th>이름</th><th>지침(md)</th><th>쓴 기능</th></tr></thead><tbody>{guide_map}</tbody></table></div>

<h2>단계별 입력과 출력</h2>
{''.join(S)}

<h2 id="outbound">밖으로 나간 데이터</h2>
<div class="tbl"><table><thead><tr><th>지점</th><th>단계</th><th>나갈 수 있는 데이터</th><th>이번 실행</th></tr></thead><tbody>
<tr><td>에이전트 판단·코드 작성</td><td class="num">5 · 6</td><td>받아쓰기 글, 격자 그림, 분석 기록, 스킬 원문</td><td>Claude Opus 5.5 로 감 (그림 11장 · transcript · 기록)</td></tr>
<tr><td>음성 인식·정렬 원격 위탁</td><td class="num">2 · 8</td><td>소리 파일 업로드, 언어</td><td>없음 — 로컬 WhisperX 에 묶음</td></tr>
<tr><td>재료 생성</td><td class="num">9</td><td>프롬프트, 설정, 참조 이미지·영상·소리</td><td>없음 — 요청 0개</td></tr>
<tr><td>점검·가격 조회</td><td class="num">7</td><td>인증된 모델 목록·가격 조회</td><td>없음 — 로컬 프로필</td></tr>
</tbody></table></div>
</main></div>
'''
with open(os.path.join(P, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(page)
tot = sum(os.path.getsize(os.path.join(M, x)) for x in os.listdir(M)) + os.path.getsize(os.path.join(P, 'index.html'))
print('html', os.path.getsize(os.path.join(P, 'index.html')), 'total', tot)
