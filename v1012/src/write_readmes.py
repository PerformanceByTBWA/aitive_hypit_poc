# write_readmes.py — 단계별\ 06~11 README·맨 위 README 다시 쓰기 + README 합본 만들기(2026-11-16)
#   python -I write_readmes.py <v1012 폴더>
import os, re, sys

V = sys.argv[1]
S = os.path.join(V, '단계별')
R = 'references/'


def wt(path, text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text.rstrip() + '\n')


def rd(path):
    with open(path, encoding='utf-8-sig') as f:
        return f.read()


def listing(d, sub):
    q = os.path.join(d, sub)
    return sorted(os.listdir(q)) if os.path.isdir(q) else []


GUIDES = {
    6: [(R + 'production/script-syntax.md', '한국어 대본은 띄어쓰기 그대로, || = 자막 덩이 경계, @{이름} = 의미 구간'),
        (R + 'production/media.md', 'Normalize → whisperx:Alignment → semantic:Projection 연결 구조, 소리 없는 영상은 audio="none"')],
    7: [(R + 'production/builds.md', '절 「Plan the selected Run」 — 실행 전 요청·공급자·요금 확인, 「Work within the agreed paid scope」')],
    8: [(R + 'production/media.md', 'NarrativeAlignment = 대본 낱말마다 원본 프레임 경계, 받아쓰기와 별개로 대본에 맞춤')],
    9: [(R + 'playbooks/craft/video-direction.md', '생성 영상 연출'), (R + 'playbooks/craft/image-direction.md', '생성 이미지 연출'),
        (R + 'playbooks/craft/generated-dependencies.md', '참조 파일 관계'), (R + 'production/prompt-kits.md', '프롬프트 틀 고르기·쓰기')],
    10: [(R + 'production/rendering.md', 'Film 이 층을 Composition 으로 묶고, Rendering 이 프레임 구간을 그려 영상으로')],
    11: [(R + 'production/builds.md', '절 「Browse and export project Results」 — get 은 영상=파일 하나, 값=value.json 폴더')],
}

BODY = {
    6: ('설계도작성', '에이전트(Claude)', '''- 하는 일: 5단계 해석과 요청을 Hypit 이 실행할 수 있는 설계도(SVML)로 옮김
- 나온 데이터: 설계도 두 벌
  - 재현판 v1012.svml — 원본 영상·소리 + 내레이션 낱말 맞춤 자막(대본 10덩이)
  - 교체판 v1012_gen.svml — 재현판 + 생성 영상(9단계)을 두 번째 재료로 넣고 실사 4자리(g1~g4)만 위층으로 덮음
  - recipes_v1012.svs(자막 모양: 위쪽 가운데·보라 강조) · v1012.svrun · v1012_gen.svrun(만들 것 = final.video)
- 왜 이렇게 나오나: 연결 순서는 Hypit 예제와 같음(정규화 → 정렬 → 시간 틀 → 투영 → 층 → Film), 대본은 화면 글자 기준 바른 낱말(「한정」 「애디렉트」), 교체 자리는 5단계 TIMELINE 장면 경계, 생성 영상 안 시작은 9단계 컷 시작 + 0.4초(자리표 = 입력\\생성컷_자리.txt)
- 왜 하나: Hypit 은 설계도에 적힌 것만 실행 — 무엇을 지키고 무엇을 바꿀지(5단계)를 실행 가능한 형태로 고정
- Hypit 기본 경로와 차이: 기본은 설계도 안 seedance 태그로 생성을 선언 → build 때 생성. 이번엔 Higgsfield 로 먼저 생성(9단계)해 파일을 asset:Video 재료로 넣음'''),
    7: ('검사계획', 'Hypit 로직', '''- 하는 일: 설계도 문법 검사, 할 일 목록·맡는 곳·요금 펼치기
- 나온 데이터:
  - 재현판(07a~07d): 「Run source is valid」 + 요청 7개, 전부 local, no Provider charge
  - 교체판(gen_07a~gen_07d): 요청 9개, 전부 local — 늘어난 2개 = 생성 영상 속성 읽기(inspect-media)·정규화(normalize-media)
- 왜 이렇게 나오나: 설계도의 관계를 따라 필요한 작업을 계산, 재료가 하나 늘면 그 재료의 읽기·정규화 작업이 늘어남
- 왜 하나: 실행 전에 돈 드는 작업이 있는지 확인 — 이번 생성은 Hypit 밖(Higgsfield)이라 계획에 유료 요청 없음, Hypit 안에서 생성하면 여기서 공급자·가격 페이지가 먼저 나옴'''),
    8: ('준비정렬', 'Hypit 로직 + 음성 모델(WhisperX)', '''- 하는 일: 재료 영상을 30fps 로 맞추고, 16kHz 소리를 뽑고, 대본 낱말을 소리에 맞춤
- 나온 데이터: ad-media_extent\\value.json(원본 450프레임) · alignment\\value.json(대본 22낱말 시작·끝 프레임, 경계 46개) · 받아쓰기_정렬_대조.md
- 교체판: 생성 영상(864×496 · 24fps · 15.04초 · 소리 없음)도 30fps 로 정규화(audio="none"), 정렬은 원본 소리 기준이라 재현판과 같은 값
- 왜 이렇게 나오나: 2단계와 목적이 다름 — 2단계는 「무슨 말을 했나」, 여기는 「우리 대본을 소리에 맞추기」 → 소리가 「안정」이어도 대본 「한정」에 시각, 단위가 초 → 프레임인 건 결과가 30fps 로 그려지기 때문
- 왜 하나: 자막·강조를 정확한 프레임에 붙이고, 24fps 생성 영상도 같은 30fps 프레임 단위로 맞춰야 정한 자리에 끼울 수 있음
- 08_build.txt · gen_08_build.txt: 빌드 전체(8·10단계) 진행 출력 — 재현판 56초, 교체판 61초'''),
    9: ('재료생성', '외부 생성 모델 — ByteDance Seedance 2.0 fast, Higgsfield MCP 경유(Hypit 밖, 2026-11-14)', '''- 하는 일: 원본의 실사 4컷(뒷모습 머리 · 제품과 액체 · 인물과 탁자 위 병 · 병 든 인물)을 Seedance 로 새로 생성
- 입력: prompt.txt(컷별 타임코드 · <<<image_N>>> 참조 순서 · 「글자·로고·커서·선택 상자 없음」 지시) · 참조그림\\ 4장(원본 정지 화면 0.00 · 1.34 · 3.05 · 6.90초) · 요청기록.json(15초 · 480p · 16:9 · 소리 없음 · 참조 역할 image ×4, Higgsfield 작업 기록에서 옮김)
- 나온 데이터: seedance_raw.mp4(864×496 · 24fps · 15.04초 · 소리 없음), 컷 시작 0 · 4.17 · 8.67 · 11.46초, 결과.md · sheet.jpg(참조 ↔ 생성 대조) · raw_05s.jpg · raw_cut23.jpg · 생성영상_probe.txt
- 비용: 15크레딧(사전 조회 값과 같음)
- 왜 이렇게 나오나: 참조 그림을 움직이는 방식(i2v 에 가까움)이라 인물·병·구도가 원본과 거의 같음, 참조에 있던 로고·흐린 문구·「딸」 「깍」 글자는 프롬프트로 지워지지 않고 남음, 2→3 컷은 하드 컷 지시에도 디졸브
- 왜 하나: 원본에 없는(또는 바꿀) 장면이 필요할 때만 — 이 단계에서만 돈이 들고 파일이 밖으로 나감
- 밖으로 나간 것: 프롬프트 글 · 참조 그림 4장(업로드) · 설정 값 → Higgsfield → ByteDance 모델
- Hypit 기본 경로와 차이: Hypit 안에서 생성하면 설계도의 seedance 태그 → build 때 HypiHub 로 요청, 프롬프트 틀(입력\\참고_seedance-kits) 고정 문장이 붙고 참조마다 사람 포함 표시가 감. 이번엔 틀 없이 직접 쓴 프롬프트
- 순서: 생성이 있으면 9 → 8 → 10 → 11(생성 영상도 정규화 뒤 렌더)'''),
    10: ('렌더', 'Hypit 로직(헤드리스 크롬 + ffmpeg)', '''- 하는 일: 층(원본 화면 · 생성 컷 · 소리 · 자막)을 프레임마다 겹쳐 그리고 소리와 합침
- 나온 데이터: caption-timing\\value.json(자막 22덩이 프레임 구간) · speech_ad\\value.json(결과 시간 틀 0–450프레임) · 자막시각표.md · gen_caption-timing(교체판, 재현판과 같은 값)
- 왜 이렇게 나오나: 8단계 정렬 프레임을 자막 레시피(앞뒤 2프레임 여유 등)로 자막 덩이 시각으로 바꿈, 교체판도 같은 대본·같은 원본 소리라 자막 시각이 같음
- 교체판 층: 원본(z=0, 0–450f) 위에 생성 컷 4개(z=1, 0–40 · 40–89 · 89–140 · 190–217f), 소리 = 원본
- 왜 하나: 여러 층을 영상 한 편으로 합침
- 빌드 안 요청 3개(두 빌드 같음): rasterize-visual 450프레임 · render-timeline-audio · mux-program-media, 프레임 그림 450장은 빌드 내부 작업 파일이라 따로 꺼내지 않음'''),
    11: ('내보내기', 'Hypit 로직', '''- 하는 일: Hypit 내부 결과 저장소에서 최종 영상과 필요한 값을 꺼냄, 런타임 끄기(runtime down + programs down)
- 나온 데이터:
  - v1012_replica.mp4 — 재현판(1920×1080 · 30fps · 15.0초 · 3.3MB)
  - v1012_gen.mp4 — 교체판(1920×1080 · 30fps · 15.0초 · 3.1MB)
  - compare_원본_교체판.mp4 — 왼쪽 원본 · 오른쪽 교체판(Hypit 밖 ffmpeg 로 붙인 확인용)
  - 11b_inspect · gen_11b_inspect — 빌드 출력 목록(재현판 14개 · 교체판 19개)
  - replica_05s · gen_05s(0.5초 격자) · replica_full · gen_full(원본 크기 낱장) — 확인용, hypit media tile·frames 로 뽑음
- 교체판 확인: 4자리가 생성 컷으로 바뀜, 원본에서 실사 위에 얹혀 있던 손글씨 제목 · 「AI generated」 · 선택 상자는 교체 구간에서 사라짐(코드로 다시 얹어야 함), 생성 컷 속 로고 · 흐린 문구 · 「딸」 「깍」은 남음, 품질은 사람이 아직 안 봄
- 왜 하나: 결과는 Hypit 저장소에 쌓여 있어 꺼내야 씀'''),
}

for no, (name, who, body) in BODY.items():
    d = os.path.join(S, f'{no:02d}_{name}')
    gl = '\n'.join(f'- {os.path.basename(r)} (skills/hypit/{r}) — {n}' for r, n in GUIDES[no])
    ins = listing(d, '입력'); outs = listing(d, '출력')
    wt(os.path.join(d, 'README.md'), f'''# {no:02d} {name}

- 실행 주체: {who}

## 설명
{body}

## 지침 한국어 요약
- 지침_한국어.md (따른 절의 원문 핵심 문장 + 한국어 풀이 + 이번 적용)

## 지침(지침\\ 폴더, 에이전트용 설명서 — hypit 프로그램이 읽지 않음)
{gl}

## 입력(입력\\ 폴더)
{chr(10).join("- " + x for x in ins) if ins else "- 없음"}

## 출력(출력\\ 폴더)
{chr(10).join("- " + x for x in outs) if outs else "- 없음"}''')

# ---------- 맨 위 README ----------
WHO = {}
for name in sorted(os.listdir(S)):
    d = os.path.join(S, name)
    if not os.path.isdir(d):
        continue
    m = re.search(r'- 실행 주체: (.+)', rd(os.path.join(d, 'README.md')))
    WHO[name] = m.group(1) if m else ''
rows = []
for name in sorted(WHO):
    d = os.path.join(S, name)
    gs = listing(d, '지침')
    rows.append(f'| {name[:2]} | {name[3:].replace("_", " ")} | {WHO[name]} | {", ".join(gs)} | {", ".join(listing(d, "출력"))} |')
TOP = '''# 단계별 지침·입력·출력 모음(애디렉트 15초, Hypit 0.3.1)

- 단계 폴더마다 지침\\(스킬 md 원문) · 지침_한국어.md · 입력\\ · 출력\\ · README.md(하는 일 · 나온 데이터 · 왜 이렇게 나오나 · 왜 하나)
- 지침 = AI 에이전트용 작업 설명서(GitHub hypit-ai/hypit 태그 v0.3.1 skills/hypit 원문 사본), hypit 프로그램은 읽지 않음
- 출력 = 그 단계에서 실제로 나온 파일(io\\ · out\\ · evidence\\ · seedance480\\ 원본에서 복사), 사본은 서버 경로 · 깨진 기호만 정리, 원본은 그대로
- 0–5 = 분석(남의 영상 읽기), 6–11 = 제작(새 영상 만들기)
- 제작은 두 벌: 재현판(v1012, 원본 + 자막, 생성 없음) · 교체판(v1012_gen, 실사 4자리를 Seedance 생성 컷으로)
- 생성은 Hypit 밖(Higgsfield MCP, 11/14, 15크레딧)에서 하고 결과를 재료로 넣음 → 실제 순서 9 → 6(교체판 설계도) → 7 → 8 → 10 → 11
- 원본 영상: 00_원본가져오기\\출력\\source.mp4 · 최종: 11_내보내기\\출력\\v1012_replica.mp4 · v1012_gen.mp4 · compare_원본_교체판.mp4
- 한 파일로 읽기: ..\\단계별_입출력_설명.md (단계 README 합본)

| 단계 | 이름 | 실행 주체 | 지침 파일 | 출력 |
| --- | --- | --- | --- | --- |
'''
wt(os.path.join(S, 'README.md'), TOP + '\n'.join(rows))

# ---------- README 합본 ----------
FLOW = '''# Hypit 단계별 입력·출력 설명(애디렉트 15초)

- 기준: 애디렉트 「모두의 TV광고」 15초(20261012134955001.mp4, 15.015초 · 1920×1080 · 29.97fps · 소리 있음), Hypit 0.3.1, 2026-11-11 분석·재현 + 2026-11-14 Seedance 생성 + 2026-11-16 교체판 빌드
- 파일 위치: 단계별\\<단계 폴더>\\입력\\ · 출력\\ · 지침\\ (이 문서는 각 단계 README.md 를 순서대로 합친 것)

## 큰 그림

- 잘 된 광고를 숫자와 글로 바꿔 읽고(분석 0–5) → 그 구조를 설계도로 적고 → 설계도대로 다시 조립(제작 6–11)
- 데이터를 만드는 주체 셋: Hypit 기계 계산(로직) · 에이전트 판단(Claude) · 외부 모델(음성 인식 WhisperX 는 로컬, 생성 Seedance 는 외부)
- 제작 두 벌: 재현판(원본 + 자막, 생성 없음) · 교체판(실사 4자리를 생성 컷으로)
- 생성이 있을 때 실제 순서: 9 생성 → 6 교체판 설계도 → 7 계획 → 8 정규화·정렬 → 10 렌더 → 11 내보내기

| 단계 | 이름 | 실행 주체 | 핵심 입력 | 핵심 출력 |
| --- | --- | --- | --- | --- |
| 00 | 원본 가져오기 | Hypit 밖(파일 복사) | 사용자 mp4 | source.mp4 · SHA-256 |
| 01 | 원본 확인 | Hypit 로직 | source.mp4 | 15.015초 · 1920×1080 · 29.97fps · 소리 있음 |
| 02 | 받아쓰기 | 음성 인식 모델(로컬) | 소리 · 언어 ko | transcript.json(22낱말 시각·점수) |
| 03 | 화면 변화 후보 | Hypit 로직 | 영상 · 초당 30장 · 기준 0.1 | 후보 11개 → 장면 바뀜 7번 |
| 04 | 프레임 격자 | Hypit 로직 | 영상 · transcript · 구간·간격 | 말 붙은 그림(evidence) |
| 05 | 판단 기록 | 에이전트 | 1–4 데이터 · 스킬 지침 | ANALYSIS · TIMELINE · PROGRESS |
| 06 | 설계도 작성 | 에이전트 | 판단 기록 · 요청 · 생성 결과 | v1012.svml · v1012_gen.svml |
| 07 | 검사·계획 | Hypit 로직 | 설계도 · 런타임 설정 | 요청 7개 / 9개, 전부 로컬 0원 |
| 08 | 준비·정렬 | Hypit 로직 + 음성 모델 | 원본 · 생성 영상 · 대본 | 30fps 정규화 · 낱말 프레임 정렬 |
| 09 | 재료 생성 | 외부 모델(Higgsfield → Seedance) | 프롬프트 · 참조 그림 4장 · 설정 | seedance_raw.mp4(15크레딧) |
| 10 | 렌더 | Hypit 로직 | 정규화 재료 · 정렬 · 자막 레시피 | 자막 시각 · 프레임 450장 · 소리 |
| 11 | 내보내기 | Hypit 로직 | 빌드 번호 | v1012_replica.mp4 · v1012_gen.mp4 |
'''
parts = [FLOW]
for name in sorted(WHO):
    t = rd(os.path.join(S, name, 'README.md'))
    t = re.sub(r'(?m)^(#{1,5}) ', lambda m: '#' + m.group(1) + ' ', t)
    t = t.replace('(입력\\ 폴더)', f'(단계별\\{name}\\입력\\)').replace('(출력\\ 폴더)', f'(단계별\\{name}\\출력\\)')
    parts.append('---\n\n' + t.strip() + '\n')
wt(os.path.join(V, '단계별_입출력_설명.md'), '\n'.join(parts))
print('ok', len(WHO), 'stages')
