import json, os, shutil, sys

V = sys.argv[1]            # v1012 폴더
SRV = sys.argv[2]          # 서버에서 받은 파일(hypit.runtime.json, kits\)
ORIG = sys.argv[3]         # 사용자 원본 mp4
SERUM = sys.argv[4]        # 11/05 serum.svml
OUT = os.path.join(V, '단계별')
SK = os.path.join(V, 'skill-ref', 'skills', 'hypit')

if os.path.exists(OUT):
    raise SystemExit('이미 있음: ' + OUT)
os.makedirs(OUT)


def cp(src, dst_dir, name=None):
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, name or os.path.basename(src.rstrip('\\/')))
    if os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        shutil.copyfile(src, dst)
    return dst


def wt(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text.rstrip() + '\n')


def io_cmd(name):
    with open(os.path.join(V, 'io', name), encoding='utf-8') as f:
        return f.readline().strip()


# ---------- 표 만들기 ----------
tx = json.load(open(os.path.join(V, 'transcript.json'), encoding='utf-8'))
words = [w for p in tx['passages'] for w in p['words']]
al = json.load(open(os.path.join(V, 'out', 'alignment', 'value.json'), encoding='utf-8'))['value']
bmap = {b['id']: b['frame'] for b in al['boundaries']}
cap = json.load(open(os.path.join(V, 'out', 'caption-timing', 'value.json'), encoding='utf-8'))['value']

align_md = ['# 받아쓰기(2단계)와 단어 정렬(8단계) 대조', '', '- 2단계 = 소리를 듣고 적은 글자와 초 단위 시각(원본 29.97fps 기준)',
            '- 8단계 = 우리가 쓴 대본 낱말을 소리에 맞춘 프레임 시각(결과 30fps 기준)', '- 「다름」 = 받아쓰기가 대본과 다르게 적은 낱말, 정렬은 대본 낱말에 시각을 붙임', '',
            '| # | 받아쓰기 | 시각(초) | 점수 | 대본 낱말 | 프레임 | 시각(초) | 비고 |', '| --- | --- | --- | --- | --- | --- | --- | --- |']
for i, t in enumerate(al['tokens']):
    s = bmap[t['startBoundaryId']]; e = bmap[t['endBoundaryId']]; w = words[i]
    note = '다름' if w['text'].rstrip('.!') != t['text'] else ''
    align_md.append(f'| {i+1} | {w["text"]} | {w["start_seconds"]:.2f}–{w["end_seconds"]:.2f} | {w["score"]} | {t["text"]} | {s}–{e} | {s/30:.2f}–{e/30:.2f} | {note} |')

cap_md = ['# 자막 시각표(caption-timing 풀이)', '', '- 자막 덩이 22개가 각각 몇 번째 프레임부터 몇 번째 프레임 앞까지 보이는지(30fps)', '',
          '| # | 낱말 | 프레임 | 시각(초) |', '| --- | --- | --- | --- |']
for i, u in enumerate(cap['units']):
    cap_md.append(f'| {i+1} | {al["tokens"][i]["text"]} | {u["startFrame"]}–{u["endFrameExclusive"]} | {u["startFrame"]/30:.2f}–{u["endFrameExclusive"]/30:.2f} |')

cuts_md = '''# 화면 변화 후보 판정(4단계 모든 프레임 격자로 에이전트가 확인)

| 후보(초) | 점수 | 판정 |
| --- | --- | --- |
| 1.333 | 0.276 | 하드 컷 1.301→1.335(제목 장면 → 제품 컷) |
| 2.967 | 0.306 | 하드 컷 2.936→2.970, 선택 상자·커서는 컷을 넘어 이어짐 |
| 4.667 | 0.472 | 하드 컷 4.638→4.671(AI generated → 업로드 화면) |
| 6.333 | 0.300 | 하드 컷(「깍」 부근, 업로드 화면 → 병 든 인물) |
| 7.233 | 0.283 | 하드 컷(인물 → 카드 화면) |
| 8.433 | 0.101 | 컷 아님 — 「AI 영상 생성」 카드 등장 |
| 10.200 · 10.233 | 0.133 · 0.198 | 한 번의 전환 — 카드 사진으로 확대 흐림 후 10.244 컷 |
| 12.567 · 12.600 · 12.633 | 0.147 · 0.190 · 0.160 | 한 번의 전환 — 로고 첫 글자 「애」가 크게 날아와 줄어들며 보라 배경으로 |
| 없음 | 0.1 미만 | 놓침 — 약 7.8초 「스토리보드 작성」, 약 9.4초 「전문가 검수」 카드가 미끄러져 들어옴 |
'''

vol_txt = '''Hypit 밖 보조 측정 — ffmpeg volumedetect (실행 스크립트: src\\st5.ps1)
목적: Hypit 에 소리를 듣는 기능이 없어 말 없는 구간에 배경 소리가 있는지 음량으로만 확인

구간(초)       평균 음량   최대 음량   비고
0.00-1.50     -23.5 dB    -6.7 dB    말 없음(오프닝)
1.70-4.30     -10.0 dB     0.0 dB    말 있음(비교 기준)
4.40-4.70     -22.9 dB   -12.4 dB    말 쉼
6.65-7.30     -20.4 dB    -6.1 dB    「딸깍」 뒤 쉼
9.70-10.35    -22.2 dB    -7.9 dB    말 쉼
12.30-12.60   -23.3 dB   -10.9 dB    말 쉼
14.50-15.00   -27.6 dB   -11.2 dB    끝(소리 줄어듦)

해석: 말 밑으로 배경 소리가 처음부터 끝까지 깔림, 끝에서 줄어듦. 음악인지 효과음인지는 구분 못 함.
'''

# ---------- 단계 정의 ----------
R = 'references/'
S = []


def stage(no, name, who, guides, inputs, outputs, readme):
    S.append(dict(no=no, name=name, who=who, guides=guides, inputs=inputs, outputs=outputs, readme=readme))


stage(0, '원본가져오기', 'Hypit 밖(파일 복사)',
      [(R + 'production/video-downloads.md', '링크로 받을 때의 지침(hypit download). 이번엔 파일을 직접 받아 사용 안 함')],
      [('원본', ORIG)],
      [('source.mp4', ORIG, 'source.mp4'), ('sha256.txt', None,
        'SHA-256 3b34fa82a45599867565189fd1446525c002b1ab4afa48f755ecb0cd34261489 (이 PC 원본)\nSHA-256 3B34FA82A45599867565189FD1446525C002B1AB4AFA48F755ECB0CD34261489 (서버 source.mp4)\n→ 같은 파일\n')],
      '''- 하는 일: 사용자 파일을 서버 프로젝트(references\\v1012\\source.mp4)로 복사, 지문(SHA-256) 비교
- 누가: 사람·에이전트(Hypit 명령 아님)
- 왜 하나: 이후 모든 시각(몇 초에 무엇)이 이 파일 하나 기준 → 같은 파일임을 지문으로 확인''')

stage(1, '원본확인', 'Hypit 로직(ffmpeg)',
      [(R + 'creation/reference-video.md', '절 「Make time visible」 — probe gives duration, dimensions, frame rate and audio presence')],
      [('명령.txt', 'hypit media probe references\\v1012\\source.mp4\nhypit media probe references\\v1012\\source.mp4 --json\n')],
      [('01_probe.txt', os.path.join(V, 'io', '01_probe.txt')), ('01_probe.json', os.path.join(V, 'io', '01_probe.json'))],
      '''- 하는 일: 영상 파일 머리 정보 읽기
- 나온 데이터: 15.015초 · 1920×1080 · 29.97fps · 소리 있음
- 왜 이렇게 나오나: 파일에 적힌 정보를 그대로 읽음
- 왜 하나: 다음 단계 기준값 — 소리가 있어 받아쓰기 가능, 마지막 프레임 14.98초라 격자 끝 시각 제한''')

stage(2, '받아쓰기', '음성 인식 모델(WhisperX, 로컬)',
      [(R + 'creation/reference-video.md', '절 「Make time visible」 — 말 있는 영상은 hypit transcribe, 언어 반드시 지정(ko)'),
       (R + 'environment/local-tools.md', '로컬 WhisperX 준비·관리(이번엔 11/05 준비본 그대로)')],
      [('명령.txt', '\n'.join(io_cmd(n) for n in ['02a_runtime-use.txt', '02b_runtime-up.txt', '02c_doctor.txt', '02d_transcribe.txt', '02e_runtime-down.txt', '02f_programs-down.txt']) + '\n'),
       ('hypit.runtime.json', os.path.join(SRV, 'hypit.runtime.json'))],
      [('transcript.json', os.path.join(V, 'transcript.json'))] + [(n, os.path.join(V, 'io', n)) for n in ['02a_runtime-use.txt', '02b_runtime-up.txt', '02c_doctor.txt', '02d_transcribe.txt', '02e_runtime-down.txt', '02f_programs-down.txt']],
      '''- 하는 일: 소리를 듣고 글자로 적고, 낱말마다 시작·끝 초와 인식 점수를 붙임
- 나온 데이터: transcript.json — 5문장 22낱말, 인식 점수 평균 0.88
- 왜 이렇게 나오나: 음성 인식 모델(large-v3)이 듣고 적은 뒤 한국어 정렬 모델이 낱말 시각을 찍음 → 들은 대로라 오인식 섞임(「한정」→「안정」, 「애디렉트」→「애드렉트」)
- 왜 하나: 광고는 말에 맞춰 화면이 바뀜 → 「어느 말 때 무엇이 보이나」를 맞추려면 낱말별 시각 필요, 점수 낮은 곳(「딸깍」 0.47)은 다시 볼 곳 표시
- 입력의 hypit.runtime.json: 음성 정렬을 로컬 whisperx.local 에 묶은 설정 → 외부 전송 없음
- 출력의 02a~02f: 런타임 켜기·점검·받아쓰기·끄기 명령의 화면 출력''')

stage(3, '화면변화후보', 'Hypit 로직(픽셀 차이)',
      [(R + 'creation/reference-video.md', '절 「Make time visible」 — boundaries locates abrupt visual changes worth inspecting')],
      [('명령.txt', io_cmd('03_boundaries_r30.txt') + '\n' + io_cmd('03_boundaries_r30.txt') + ' --json\n(설정: 초당 30장, 기준값 기본 0.1)\n')],
      [('03_boundaries_r30.txt', os.path.join(V, 'io', '03_boundaries_r30.txt')), ('03_boundaries_r30.json', os.path.join(V, 'io', '03_boundaries_r30.json')),
       ('후보판정.md', None, cuts_md)],
      '''- 하는 일: 앞뒤 프레임 픽셀 차이가 기준(0.1)을 넘는 시각을 찍음
- 나온 데이터: 후보 11개(시각·점수)
- 왜 이렇게 나오나: 기계적 계산이라 컷 판단 아님 → 한 전환이 여러 개로 잡히고(12.567·12.6·12.633), 천천히 미끄러지는 카드는 못 잡음
- 왜 하나: 15초를 프레임마다 다 볼 수 없으니 「어디를 자세히 볼지」 표지 — 판정은 4단계 그림으로
- 후보판정.md: 에이전트가 모든 프레임 격자로 확인한 결과(Hypit 출력 아님)''')

stage(4, '프레임격자', 'Hypit 로직(ffmpeg)',
      [(R + 'creation/reference-video.md', '절 「Make time visible」 — tile·tiles·frames, --every-frame, --ranges, --around, --transcript, 넓게→좁게')],
      [('명령.txt', '\n'.join(io_cmd(n) for n in ['04a_tile_words_05s.txt', '04b_tiles_cuts_everyframe.txt', '04c_tile_ttalkkak.txt', '04d_tile_hook.txt', '04e_tile_endcard.txt', '04f_frames_full.txt', '04g_tile_proc.txt'])
        + '\n(전체 1초·0.5초 간격 whole_1s·whole_05s 는 낱말 없이 먼저 뽑음: hypit media tile ... --start 0 --end 15 --every 1|0.5)\n'),
       ('04_ranges.json', os.path.join(V, 'io', '04_ranges.json'))],
      [('evidence', os.path.join(V, 'evidence'))] + [(n, os.path.join(V, 'io', n)) for n in ['04a_tile_words_05s.txt', '04b_tiles_cuts_everyframe.txt', '04c_tile_ttalkkak.txt', '04d_tile_hook.txt', '04e_tile_endcard.txt', '04f_frames_full.txt', '04g_tile_proc.txt']],
      '''- 하는 일: 영상에서 프레임을 뽑아 한 장에 모으고 그 순간 들리는 낱말을 아래에 붙임
- 나온 데이터: evidence\\ — 전체 1초·0.5초(whole_1s·whole_05s·words_05s), 0–3초(hook), 「딸깍」 앞뒤 0.1초(ttalkkak), 카드 구간(process), 끝 5초(endcard), 후보 근처 모든 프레임(cuts\\), 원본 크기 낱장 11장(full\\)
- 왜 이렇게 나오나: 2단계 transcript.json 시각으로 낱말을 붙임 → 「말 붙은 그림」
- 왜 하나: 에이전트는 영상을 재생 못 하고 그림만 봄 → 영상을 볼 수 있는 형태로 바꿈, 넓게(흐름) → 좁게(전환 순간) 순서
- 입력: 2단계 transcript.json 도 씀(02_받아쓰기\\출력)''')

stage(5, '판단기록', '에이전트(Claude) — Hypit 기능 없음',
      [('SKILL.md', '절 「Understand and adapt」 — 전체 해석은 Analysis, 시각별 세부는 Timeline'),
       (R + 'creation/reference-video.md', '절 「Preserve a connected account」·「Turn understanding into new direction」 — ANALYSIS·TIMELINE·PROGRESS 양식'),
       (R + 'playbooks/index.md', '절 「Formats」 표 — 형식 고르기'),
       (R + 'playbooks/formats/narration-led-demo.md', '고른 형식: 화면 밖 내레이션이 뼈대인 영상'),
       (R + 'playbooks/craft/screen-demonstrations.md', '화면 시연 읽기(도입·절 제목까지 참고)'),
       (R + 'playbooks/craft/motion-graphics.md', '모션그래픽 읽기(도입·절 제목까지 참고)'),
       (R + 'playbooks/craft/graphic-compositions.md', '화면 구성 읽기(도입·절 제목까지 참고)'),
       (R + 'playbooks/craft/sound-mix.md', '소리 읽기(도입·절 제목까지 참고)')],
      [('입력목록.txt', '02_받아쓰기\\출력\\transcript.json\n03_화면변화후보\\출력\\03_boundaries_r30.json · 후보판정.md\n04_프레임격자\\출력\\evidence\\ 중 에이전트가 실제로 연 그림 11장: whole_1s · words_05s · hook · cuts\\001·002·003·007·008 · ttalkkak · process · endcard\n음량측정_hypit밖.txt (보조)\n'),
       ('음량측정_hypit밖.txt', vol_txt)],
      [('ANALYSIS.md', os.path.join(V, 'ANALYSIS.md')), ('TIMELINE.md', os.path.join(V, 'TIMELINE.md')), ('PROGRESS.md', os.path.join(V, 'PROGRESS.md'))],
      '''- 하는 일: 1~4단계 데이터를 보고 영상이 왜 잘 됐는지 해석해 기록
- 나온 데이터: ANALYSIS(전체 구조 5박자·유지할 관계 7개) · TIMELINE(구간별 말·화면·역할) · PROGRESS(남은 확인)
- 왜 이렇게 나오나: Hypit 기계가 아닌 에이전트가 지침(양식·읽는 법)대로 해석 → 모델·지침에 따라 내용 달라짐, 사람 검토 안 함
- 왜 하나: 다시 만들 때 「무엇을 지키고 무엇을 바꿀지」 정하는 근거
- 외부 전송: 받아쓰기 글·격자 그림·지침이 에이전트 모델(Claude)로 감''')

stage(6, '설계도작성', '에이전트(Claude)',
      [(R + 'production/script-syntax.md', '한국어 대본은 띄어쓰기 그대로, || = 자막 덩이 경계, @{이름} = 의미 구간'),
       (R + 'production/media.md', 'Normalize → whisperx:Alignment → semantic:Projection 연결 구조')],
      [('요청.txt', '원본 영상·소리 그대로 + 내레이션 낱말에 맞춘 한국어 자막(생성 모델 없음, 무료 범위)\n대본은 화면 글자 기준 바른 낱말(「한정」 「애디렉트」)\n근거: 05_판단기록\\출력\\ANALYSIS.md · TIMELINE.md\n'),
       ('틀_11월5일_serum.svml', SERUM)],
      [('v1012.svml', os.path.join(V, 'src', 'v1012.svml')), ('v1012.svrun', os.path.join(V, 'src', 'v1012.svrun')), ('recipes_v1012.svs', os.path.join(V, 'src', 'recipes_v1012.svs'))],
      '''- 하는 일: 해석과 요청을 Hypit 이 실행할 수 있는 설계도로 옮김
- 나온 데이터: v1012.svml(대본·재료·시간 틀·화면/소리/자막 층·최종 영상) · recipes_v1012.svs(자막 모양) · v1012.svrun(무엇을 만들지)
- 왜 이렇게 나오나: 11/05 세럼 재현 코드를 틀로 쓰고 한국어 자막·16:9·보라 강조색만 바꿈
- 왜 하나: Hypit 은 설계도에 적힌 것만 실행''')

stage(7, '검사계획', 'Hypit 로직',
      [(R + 'production/builds.md', '절 「Plan the selected Run」 — 실행 전 요청·공급자·요금 확인, 「Work within the agreed paid scope」')],
      [('명령.txt', '\n'.join(io_cmd(n) for n in ['07a_runtime-use.txt', '07b_runtime-up.txt', '07c_check.txt', '07d_plan.txt']) + '\n입력 파일: 06_설계도작성\\출력\\v1012.svrun → v1012.svml + hypit.runtime.json\n'),
       ('hypit.runtime.json', os.path.join(SRV, 'hypit.runtime.json'))],
      [(n, os.path.join(V, 'io', n)) for n in ['07a_runtime-use.txt', '07b_runtime-up.txt', '07c_check.txt', '07d_plan.txt']],
      '''- 하는 일: 설계도 문법 검사, 할 일 목록 펼치기
- 나온 데이터: 「Run source is valid」 + 작업 7개(맡는 곳·요금) — 전부 local, no Provider charge
- 왜 이렇게 나오나: 설계도의 관계를 따라 필요한 작업을 계산
- 왜 하나: 실행 전에 돈 드는 작업이 있는지 확인 — 생성이 있으면 여기서 공급자·가격 페이지가 먼저 나옴''')

stage(8, '준비정렬', 'Hypit 로직 + 음성 모델(WhisperX)',
      [(R + 'production/media.md', 'NarrativeAlignment = 대본 낱말마다 원본 프레임 경계, 받아쓰기와 별개로 대본에 맞춤')],
      [('명령.txt', io_cmd('08_build.txt') + '\n(빌드 한 번 안에서 이 단계 요청 4개: inspect-media · normalize-media · project-speech-evidence-audio · whisperx-alignment(ko))\n')],
      [('08_build.txt', os.path.join(V, 'io', '08_build.txt')), ('ad-media_extent', os.path.join(V, 'out', 'ad-media_extent')),
       ('alignment', os.path.join(V, 'out', 'alignment')), ('받아쓰기_정렬_대조.md', None, '\n'.join(align_md))],
      '''- 하는 일: 원본을 30fps로 맞추고(450프레임), 16kHz 소리를 뽑고, 대본 낱말을 소리에 맞춤
- 나온 데이터: ad-media_extent\\value.json(길이 450프레임) · alignment\\value.json(대본 22낱말 각각 시작·끝 프레임, 경계 46개)
- 왜 이렇게 나오나: 2단계와 목적이 다름 — 2단계는 「무슨 말을 했나」, 여기는 「우리 대본을 소리에 맞추기」 → 소리가 「안정」이어도 대본 「한정」에 시각, 단위가 초→프레임인 건 결과가 30fps 로 그려지기 때문
- 왜 하나: 자막·강조를 정확한 프레임에 붙이려고
- 받아쓰기_정렬_대조.md: 두 결과를 나란히 놓은 표(에이전트가 만든 풀이)
- 08_build.txt: 빌드 전체(8·10단계) 진행 출력''')

kits_dir = os.path.join(SRV, 'kits')
stage(9, '재료생성_이번없음', '외부 생성 모델(이번 요청 0개)',
      [(R + 'playbooks/craft/video-direction.md', '생성 영상 연출'), (R + 'playbooks/craft/image-direction.md', '생성 이미지 연출'),
       (R + 'playbooks/craft/generated-dependencies.md', '참조 파일 관계'), (R + 'production/prompt-kits.md', '프롬프트 틀 고르기·쓰기')],
      [('seedance-kits', kits_dir)],
      [('없음.txt', None, '이번 실행은 원본 영상을 그대로 써서 생성 요청 0개 — 출력 없음, 외부 전송·요금 없음\n')],
      '''- 하는 일(쓸 때): 원본에 없는 장면(다른 제품·사람)을 Seedance 등으로 생성
- 이번: 요청 0개 → 출력 없음
- 입력의 seedance-kits: Hypit 기본 제공 Seedance 프롬프트 틀 7종(서버 설치본 사본) — 고정 문장 + 선택지 + 빈칸(story), SVML 의 장면 설명과 합쳐 프롬프트가 됨
- 나가는 것(쓸 때): 프롬프트 글, 모델·길이·비율·해상도, 첫·끝 프레임, 참조 이미지·영상·소리, 사람 포함 표시
- 순서: 생성이 있으면 9 → 8 → 10(생성 영상도 정규화·정렬 뒤 렌더)''')

stage(10, '렌더', 'Hypit 로직(헤드리스 크롬 + ffmpeg)',
      [(R + 'production/rendering.md', 'Film 이 층을 Composition 으로 묶고, Rendering 이 프레임 구간을 그려 영상으로')],
      [('입력목록.txt', '08_준비정렬\\출력 (정규화 영상·단어 정렬)\n06_설계도작성\\출력\\recipes_v1012.svs (자막 모양)\n글꼴 Noto Sans KR 800\n(빌드 안 요청 3개: rasterize-visual 450프레임 · render-timeline-audio · mux-program-media)\n')],
      [('caption-timing', os.path.join(V, 'out', 'caption-timing')), ('speech_ad', os.path.join(V, 'out', 'speech_ad')), ('자막시각표.md', None, '\n'.join(cap_md))],
      '''- 하는 일: 원본 화면·소리·자막 층을 프레임마다 겹쳐 그리고 소리와 합침
- 나온 데이터: caption-timing\\value.json(자막 22덩이 프레임 구간) · speech_ad\\value.json(결과 시간 틀 0–450프레임)
- 왜 이렇게 나오나: 8단계 정렬 프레임을 자막 레시피(앞뒤 2프레임 여유 등)로 자막 덩이 시각으로 바꿈
- 왜 하나: 여러 층을 영상 한 편으로 합침
- 프레임 그림 450장은 빌드 내부 작업 파일이라 따로 꺼내지 않음''')

stage(11, '내보내기', 'Hypit 로직',
      [(R + 'production/builds.md', '절 「Browse and export project Results」 — get 은 영상=파일 하나, 값=value.json 폴더')],
      [('명령.txt', '\n'.join(io_cmd(n) for n in ['11a_get_video.txt', '11b_inspect.txt', '11c_get_alignment.txt', '11d_runtime-down.txt', '11e_programs-down.txt']) + '\n')],
      [('v1012_replica.mp4', os.path.join(V, 'out', 'v1012_replica.mp4')), ('replica_05s.jpg', os.path.join(V, 'out', 'replica_05s.jpg')),
       ('replica_full', os.path.join(V, 'out', 'replica_full'))] + [(n, os.path.join(V, 'io', n)) for n in ['11a_get_video.txt', '11b_inspect.txt', '11c_get_alignment.txt', '11d_runtime-down.txt', '11e_programs-down.txt']],
      '''- 하는 일: Hypit 내부 결과 저장소에서 최종 영상과 필요한 값을 꺼냄, 런타임 끄기
- 나온 데이터: v1012_replica.mp4(1920×1080 · 30fps · 15.0초 · 3.3MB) · 11b_inspect(이 빌드의 출력 14개 목록)
- 왜 하나: 결과는 Hypit 저장소에 쌓여 있어 꺼내야 씀
- replica_05s.jpg · replica_full\\: 결과 확인용 격자·낱장(hypit media tile·frames 로 뽑음)''')

# ---------- 파일 쓰기 ----------
rows = []
for s in S:
    d = os.path.join(OUT, f'{s["no"]:02d}_{s["name"]}')
    gnames = []
    for rel, note in s['guides']:
        src = os.path.join(SK, rel.replace('/', os.sep))
        cp(src, os.path.join(d, '지침'))
        gnames.append(os.path.basename(rel))
    gl = '\n'.join(f'- {os.path.basename(rel)} (skills/hypit/{rel}) — {note}' for rel, note in s['guides'])
    for item in s['inputs']:
        name, val = item
        if val and os.path.exists(val):
            cp(val, os.path.join(d, '입력'), name)
        else:
            wt(os.path.join(d, '입력', name), val)
    for item in s['outputs']:
        if len(item) == 3:
            name, src, text = item
            if src:
                cp(src, os.path.join(d, '출력'), text)
            else:
                wt(os.path.join(d, '출력', name), text)
        else:
            name, src = item
            cp(src, os.path.join(d, '출력'), name)
    ins = sorted(os.listdir(os.path.join(d, '입력'))) if os.path.isdir(os.path.join(d, '입력')) else []
    outs = sorted(os.listdir(os.path.join(d, '출력')))
    wt(os.path.join(d, 'README.md'), f'''# {s["no"]:02d} {s["name"].replace("_", " ")}

- 실행 주체: {s["who"]}

## 설명
{s["readme"]}

## 지침(지침\\ 폴더, 에이전트용 설명서 — hypit 프로그램이 읽지 않음)
{gl}

## 입력(입력\\ 폴더)
{chr(10).join("- " + x for x in ins) if ins else "- 없음"}

## 출력(출력\\ 폴더)
{chr(10).join("- " + x for x in outs)}
''')
    rows.append(f'| {s["no"]:02d} | {s["name"].replace("_", " ")} | {s["who"]} | {", ".join(gnames)} | {", ".join(outs)} |')

wt(os.path.join(OUT, 'README.md'), '''# 단계별 지침·입력·출력 모음(애디렉트 15초, Hypit 0.3.1)

- 단계 폴더마다 지침\\(스킬 md 원문) · 입력\\ · 출력\\ · README.md(하는 일·왜 이렇게 나오나·왜 하나)
- 지침 = AI 에이전트용 작업 설명서(GitHub hypit-ai/hypit 태그 v0.3.1 skills/hypit 원문 사본), hypit 프로그램은 읽지 않음
- 출력 = 그 단계에서 실제로 나온 파일(io\\·out\\·evidence\\ 원본에서 복사, 원본은 그대로 둠)
- 0–5 = 분석(남의 영상 읽기), 6–11 = 제작(새 영상 만들기), 생성이 있으면 9 → 8 → 10 순서
- 원본 영상: 00_원본가져오기\\출력\\source.mp4

| 단계 | 이름 | 실행 주체 | 지침 파일 | 출력 |
| --- | --- | --- | --- | --- |
''' + '\n'.join(rows))
print('ok', OUT)
for s in S:
    d = os.path.join(OUT, f'{s["no"]:02d}_{s["name"]}')
    n = sum(len(f) for _, _, f in os.walk(d))
    print(f'{s["no"]:02d}_{s["name"]}: files={n}')
