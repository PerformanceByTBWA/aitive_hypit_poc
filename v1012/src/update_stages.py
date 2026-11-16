# update_stages.py — 단계별\ 폴더를 애디렉트 15초 기준으로 갱신(2026-11-16)
#   python -I update_stages.py <v1012 폴더> <ffmpeg.exe>
# - 서버 경로(D:\oss_eval\hypit\proj_serum…)·깨진 기호 정리(사본만, 원본 io\·out\ 은 그대로)
# - 06: 11/05 틀 파일 빼고 Hypit 예제·애디렉트 요청·생성 컷 자리표 넣음, 교체판 설계도(v1012_gen) 추가
# - 09: 이번없음 → 실제 생성(11/14 Higgsfield Seedance 2.0 fast 480p 15초 1회) 입력·출력
# - 07·08·10·11: 교체판 빌드(v1012_gen) 출력 추가
import json, os, re, shutil, subprocess, sys

V = sys.argv[1]
FF = sys.argv[2]
S = os.path.join(V, '단계별')
IO = os.path.join(V, 'io')
OUTD = os.path.join(V, 'out')
G = os.path.join(V, 'seedance480')
SK = os.path.join(V, 'skill-ref', 'skills', 'hypit')


def p(*a):
    return os.path.join(*a)


def rd(path):
    with open(path, 'rb') as f:
        b = f.read()
    if b[:2] in (b'\xff\xfe', b'\xfe\xff'):
        return b.decode('utf-16')
    return b.decode('utf-8-sig')


def wt(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text.rstrip() + '\n')


def cp(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.isdir(src):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    else:
        shutil.copyfile(src, dst)


def clean(s):
    s = s.replace('\r\n', '\n')
    s = s.replace('쨌', '·').replace('횞', '×').replace('?ㅽ썑', '오후').replace('?ㅼ쟾', '오전')
    s = re.sub('\\?\ufffd전', '오전', s)
    s = re.sub('\\?\ufffd후', '오후', s)
    s = re.sub(r" ?--project '[^']*'", '', s)
    s = re.sub(r" ?--runtime '[^']*'", '', s)
    s = re.sub(r'C:\\Users\\llm\\AppData\\Local\\Hypit\\programs\\\S+', '(서버 프로그램 로그)', s)
    s = re.sub(r'C:[\\/]{1,2}Users[\\/]{1,2}llm[\\/]{1,2}\.cache[^\s"]+', '(서버의 헤드리스 크롬)', s)
    s = re.sub(r'D:(\\{1,2})oss_eval\1hypit\1proj_serum\1(?:(?:references|out)\1v1012(?:_gen)?\1(?:gen\1)?)?', '', s)
    s = re.sub(r'D:(\\{1,2})oss_eval\1hypit\1proj_serum', '(프로젝트 폴더)', s)
    s = re.sub(r'(?m)^(\s*)\?\?', r'\1✓ ', s)
    s = s.replace(' ??', ' → ').replace('??', '→')
    return s


# ---------- 1. 사본 정리(지침\ 제외) ----------
n_clean = 0
for root, dirs, files in os.walk(S):
    if '지침' in os.path.relpath(root, S).split(os.sep):
        continue
    for fn in files:
        if not fn.lower().endswith(('.txt', '.json', '.svml', '.svs', '.svrun')):
            continue
        fp = p(root, fn)
        t = rd(fp)
        c = clean(t)
        if c != t:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(c)
            n_clean += 1

# 00 원본.txt
wt(p(S, '00_원본가져오기', '입력', '원본.txt'),
   '사용자 원본 파일: 20261012134955001.mp4 (27,940,874 바이트)\n서버 복사 위치: Hypit 프로젝트 references\\v1012\\source.mp4\n복사본: 출력\\source.mp4')


def io_copy(name, dst_dir, new=None):
    src = p(IO, name)
    t = clean(rd(src))
    wt(p(dst_dir, new or name), t)
    return t.split('\n', 1)[0]


def io_cmd(name):
    return clean(rd(p(IO, name))).split('\n', 1)[0]


# ---------- 2. 06 설계도작성 ----------
d6 = p(S, '06_설계도작성')
old = p(d6, '입력', '틀_11월5일_serum.svml')
if os.path.exists(old):
    os.remove(old)
cp(p(SK, 'references', 'production', 'examples', 'production.svml'), p(d6, '입력', '예제_production.svml'))
wt(p(d6, '입력', '요청.txt'), '''요청 1 · 재현판(v1012): 원본 영상·소리 그대로 + 내레이션 낱말에 맞춘 한국어 자막(생성 모델 없음)
요청 2 · 교체판(v1012_gen): 재현판에서 실사 4자리만 Seedance 생성 컷으로 교체(생성 영상 = 09_재료생성\\출력\\seedance_raw.mp4)
대본은 화면 글자 기준 바른 낱말(「한정」 「애디렉트」) — 받아쓰기 오인식(「안정」 「애드렉트」)을 따르지 않음
근거: 05_판단기록\\출력\\ANALYSIS.md · TIMELINE.md (장면 8개·실사 4컷 위치)''')
wt(p(d6, '입력', '생성컷_자리.txt'), '''교체판 자리표 — 원본 타임라인의 실사 4자리 ↔ 생성 영상 안 컷
(원본 자리 = 05_판단기록 TIMELINE 장면 경계, 생성 컷 시작 = 09_재료생성\\출력\\결과.md, 생성 영상 안 시작 = 컷 시작 + 0.4초로 경계 직후 피함)

자리   원본 시각(초)      결과 프레임(30fps)   생성 컷   생성 영상 안 시작(초 → 30fps 프레임)
g1     0.000 – 1.335     0 – 40               Cut1 뒷모습 머리      0.40  → 12f
g2     1.335 – 2.970     40 – 89              Cut2 제품과 액체      4.57  → 137f
g3     2.970 – 4.671     89 – 140             Cut3 인물과 탁자 위 병 9.07  → 272f
g4     6.333 – 7.233     190 – 217            Cut4 병 든 인물       11.86 → 356f''')
for fn in ['v1012_gen.svml', 'v1012_gen.svrun']:
    cp(p(V, 'src', fn), p(d6, '출력', fn))
gk = p(d6, '지침_한국어.md')
t = rd(gk)
t = t.replace('- 틀은 11/05 세럼 재현 코드(입력\\틀_11월5일_serum.svml)',
              '- 연결 순서는 Hypit 스킬 예제와 같음(입력\\예제_production.svml: Normalize → Alignment → Timeline → Projection → Track → Film)\n'
              '- 교체판(v1012_gen.svml): 생성 영상을 두 번째 재료로 넣고(audio="none"), 4자리 시간 창(g1~g4)에 위층(z=1) Clip + visual:Map 으로 생성 영상 안 시작 프레임 지정, 자리표 = 입력\\생성컷_자리.txt')
wt(gk, t)

# ---------- 3. 07 검사계획 ----------
d7 = p(S, '07_검사계획')
gen7 = ['gen_07a_runtime-use.txt', 'gen_07b_runtime-up.txt', 'gen_07c_check.txt', 'gen_07d_plan.txt']
for n in gen7:
    io_copy(n, p(d7, '출력'))
m7 = rd(p(d7, '입력', '명령.txt')).rstrip()
if 'v1012_gen' not in m7:
    wt(p(d7, '입력', '명령.txt'), '# 재현판(v1012)\n' + m7 + '\n\n# 교체판(v1012_gen)\n' + '\n'.join(io_cmd(n) for n in gen7) +
       '\n입력 파일: 06_설계도작성\\출력\\v1012_gen.svrun → v1012_gen.svml + hypit.runtime.json')

# ---------- 4. 08 준비정렬 ----------
d8 = p(S, '08_준비정렬')
io_copy('gen_08_build.txt', p(d8, '출력'))
m8 = rd(p(d8, '입력', '명령.txt')).rstrip()
if 'v1012_gen' not in m8:
    wt(p(d8, '입력', '명령.txt'), '# 재현판(v1012)\n' + m8 + '\n\n# 교체판(v1012_gen)\n' + io_cmd('gen_08_build.txt') +
       '\n(빌드 한 번 안에서 이 단계 요청 6개: inspect-media ×2 · normalize-media ×2(원본·생성 영상) · project-speech-evidence-audio · whisperx-alignment(ko))\n'
       '생성 영상 입력: 09_재료생성\\출력\\seedance_raw.mp4')

# ---------- 5. 09 재료생성 ----------
old9 = p(S, '09_재료생성_이번없음')
d9 = p(S, '09_재료생성')
if os.path.exists(old9) and not os.path.exists(d9):
    os.rename(old9, d9)
if os.path.exists(p(d9, '입력', 'seedance-kits')):
    os.rename(p(d9, '입력', 'seedance-kits'), p(d9, '입력', '참고_seedance-kits'))
if os.path.exists(p(d9, '출력', '없음.txt')):
    os.remove(p(d9, '출력', '없음.txt'))
cp(p(G, 'prompt.txt'), p(d9, '입력', 'prompt.txt'))
for fn in ['ref1_hair.jpg', 'ref2_product.jpg', 'ref3_table.jpg', 'ref4_bottle.jpg', '_refs.jpg']:
    cp(p(G, 'ref', fn), p(d9, '입력', '참조그림', fn))
req = {
    '경로': 'Higgsfield MCP generate_video (Hypit 밖, 11/14)',
    '작업 번호': '02d27faf-a6d9-4c46-aeca-0172170935b3',
    'model': 'seedance_2_0_fast (요청 model=seedance_2_0 · mode=fast)',
    'aspect_ratio': '16:9', 'duration': 15, 'resolution': '480p', 'width': 854, 'height': 480,
    'generate_audio': False, 'multi_shots': False, 'genre': 'auto', 'speedramp': 'auto', 'bitrate_mode': 'standard',
    'prompt_language(서비스 기록값)': 'en',
    'medias': [{'role': 'image', 'media_id': i, '파일': f} for i, f in zip(
        ['e91c033a-308c-456e-ae54-c352446786b1', 'd04417cb-85b0-4166-8c43-4213ca03f6db', 'b8a90f88-7271-4bc0-93e1-b940f1a2c771', '92f22b59-4829-4a5d-a2c4-bdbb192052aa'],
        ['참조그림\\ref1_hair.jpg (원본 0.00초)', '참조그림\\ref2_product.jpg (원본 1.34초)', '참조그림\\ref3_table.jpg (원본 3.05초)', '참조그림\\ref4_bottle.jpg (원본 6.90초)'])],
    'prompt': '입력\\prompt.txt 와 같음',
    '비고': 'Higgsfield 작업 기록(job_display)에서 옮김, 파일 주소(계정 경로 포함)는 뺌',
}
wt(p(d9, '입력', '요청기록.json'), json.dumps(req, ensure_ascii=False, indent=2))
for fn in ['seedance_raw.mp4', 'raw_05s.jpg', 'raw_cut23.jpg', 'sheet.jpg']:
    cp(p(G, fn), p(d9, '출력', fn))
io_copy('gen_09_probe.txt', p(d9, '출력'), '생성영상_probe.txt')
wt(p(d9, '출력', '결과.md'), '''# 생성 결과(Seedance 2.0 fast · 480p · 15초 · 1회)

- 비용: 15크레딧(잔액 2,505.21 → 2,490.21), 사전 조회 get_cost 값과 같음
- 결과 파일: seedance_raw.mp4 — 864×496 · 24fps · 15.04초 · 소리 없음 · 2.6MB

| 항목 | 결과 |
| --- | --- |
| 컷 구성 | 4컷, 시작 0 · 4.17 · 8.67 · 11.46초(프롬프트 0 · 4 · 8 · 11초) |
| 전환 | 1→2 · 3→4 하드 컷, 2→3 은 8.25~8.6초 디졸브(프롬프트는 하드 컷) |
| 원본과 닮음 | 인물 · 병 · 배경 · 구도 거의 같음 — 참조 그림을 움직이는 방식(i2v 에 가까움) |
| 프롬프트로 지운 것 | 3번 컷 선택 상자 · 커서 사라짐 |
| 프롬프트에도 남은 것 | 왼쪽 위 「애디렉트」 로고(전 컷), 2번 컷 흐린 「지금 보시는 이 광고」, 4번 컷 「딸」 「깍」 큰 글자 — 참조 그림에 있던 글자 |
| 라벨 | 「LUNÉRA Hydra Repair Shampoo」 유지, 아래 작은 글씨는 뭉개짐 |
| 필터 | NSFW · IP 차단 없음(맨어깨 · 뒷모습 통과) |

- sheet.jpg: 참조 그림(왼쪽) ↔ 생성 컷 가운데 프레임(오른쪽) 4쌍
- raw_05s.jpg: 생성 영상 0.5초 격자 · raw_cut23.jpg: 2→3번 컷 전환(12fps)
- 다음에 바꿀 점: 글자 · 로고 없는 참조 그림 사용, 장면별 4초 4번 생성(컷 경계 제어), 최종본은 720p/1080p std 또는 gpu103 SeedVR2 업스케일''')
g9 = p(d9, '지침_한국어.md')
t = rd(g9)
t = t.replace('# 09 재료 생성(이번엔 안 씀) — 지침 한국어 요약', '# 09 재료 생성 — 지침 한국어 요약')
t = t.replace('- 이번 실행은 생성 요청 0개 → 아래는 「생성할 때 따를 지침」의 도입부 요약(본문 정독 안 함)',
              '- 이번 생성은 Hypit 밖(Higgsfield MCP)에서 1회 — 아래는 생성 요청을 쓸 때 따르는 지침의 도입부 요약(본문 정독 안 함)')
t = t.replace('(입력\\seedance-kits\\ 7종', '(입력\\참고_seedance-kits\\ 7종, 이번 Higgsfield 경로에선 안 씀')
if '## 이번 적용' not in t:
    t += '''
## 이번 적용(11/14 Higgsfield 경로)

- 참조 그림 4장 = 원본 정지 화면(0.00 · 1.34 · 3.05 · 6.90초) → generated-dependencies 「참조가 사람·제품·장소 모습을 기억으로 가져옴」
- 프롬프트 = 컷마다 타임코드 + `<<<image_N>>>` 로 참조 순서 지정 + 「화면에 글자 · 로고 · 커서 · 선택 상자 없음」 → 참조에 있던 글자는 일부 남음(결과.md)
- Hypit 기본 틀(seedance-kits)은 Hypit 이 요청을 만들 때 붙는 것이라 이번 Higgsfield 경로에선 쓰지 않음
- 받은 영상은 Hypit 에 재료(asset:Video)로 넣어 8 → 10 → 11 로 조립(06 v1012_gen.svml)'''
wt(g9, t)

# ---------- 6. 10 렌더 ----------
d10 = p(S, '10_렌더')
cp(p(OUTD, 'v1012_gen', 'caption-timing'), p(d10, '출력', 'gen_caption-timing'))
same = rd(p(OUTD, 'caption-timing', 'value.json')) == rd(p(OUTD, 'v1012_gen', 'caption-timing', 'value.json'))
wt(p(d10, '입력', '입력목록.txt'), '''재현판(v1012)
- 08_준비정렬\\출력 (정규화 영상·단어 정렬)
- 06_설계도작성\\출력\\recipes_v1012.svs (자막 모양), 글꼴 Noto Sans KR 800
- 빌드 안 요청 3개: rasterize-visual 450프레임 · render-timeline-audio · mux-program-media

교체판(v1012_gen)
- 위와 같음 + 정규화한 생성 영상(09_재료생성\\출력\\seedance_raw.mp4 → 30fps)
- 화면 층: 원본(z=0, 0–450f) 위에 생성 컷 4개(z=1, g1 0–40f · g2 40–89f · g3 89–140f · g4 190–217f), 소리 = 원본, 자막 = 재현판과 같음''')

# ---------- 7. 11 내보내기 ----------
d11 = p(S, '11_내보내기')
gen11 = ['gen_11a_get_video.txt', 'gen_11b_inspect.txt', 'gen_11d_get_caption_timing.txt', 'gen_11e_runtime-down.txt', 'gen_11f_programs-down.txt']
for n in gen11:
    io_copy(n, p(d11, '출력'))
cp(p(OUTD, 'v1012_gen', 'v1012_gen.mp4'), p(d11, '출력', 'v1012_gen.mp4'))
cp(p(OUTD, 'v1012_gen', 'gen_05s.jpg'), p(d11, '출력', 'gen_05s.jpg'))
cp(p(OUTD, 'v1012_gen', 'gen_full'), p(d11, '출력', 'gen_full'))
m11 = rd(p(d11, '입력', '명령.txt')).rstrip()
if 'v1012_gen' not in m11:
    wt(p(d11, '입력', '명령.txt'), '# 재현판(v1012)\n' + m11 + '\n\n# 교체판(v1012_gen)\n' + '\n'.join(io_cmd(n) for n in gen11))
cmpv = p(d11, '출력', 'compare_원본_교체판.mp4')
font = 'C\\:/Windows/Fonts/malgunbd.ttf'
lab = lambda s: f"drawtext=fontfile='{font}':text='{s}':fontcolor=white:fontsize=30:x=(w-text_w)/2:y=18"
subprocess.run([FF, '-y', '-loglevel', 'error', '-i', p(S, '00_원본가져오기', '출력', 'source.mp4'), '-i', p(d11, '출력', 'v1012_gen.mp4'),
                '-filter_complex', f"[0:v]scale=960:540,fps=30,pad=960:610:0:70:color=0x14141c,{lab('원본')}[l];"
                f"[1:v]scale=960:540,fps=30,pad=960:610:0:70:color=0x14141c,{lab('Hypit 교체판(생성 컷 4자리)')}[r];[l][r]hstack[v]",
                '-map', '[v]', '-map', '0:a', '-c:v', 'libx264', '-crf', '20', '-preset', 'medium', '-c:a', 'aac', '-b:a', '160k', '-shortest', cmpv], check=True)

print('cleaned files', n_clean, '| caption-timing same', same)
