import json, os, shutil, sys

R = sys.argv[1]  # remake 폴더
OUT = os.path.join(R, 'higgsfield_전송')
os.makedirs(os.path.join(OUT, '참조그림'), exist_ok=True)

PERSON = '2a0c1762-e613-4492-a7ea-2432a601615c'
PRODUCT = 'd053da39-5f9b-4117-9ba8-9c54e32b8343'

# Higgsfield 작업 기록(show_generation_by_ids, 2026-11-16 조회)에서 옮긴 실제 전송 값 — 파일 주소(계정 경로)만 뺌
REQ = [
    dict(no='01', name='제품사진', tool='generate_image', job=PRODUCT, file='prompts\\img_product.txt',
         context='가상 음료 제품 광고 시험용 제품 참조 사진',
         params={'model(요청)': 'nano_banana_pro', 'model(서비스 기록)': 'nano_banana_2', 'aspect_ratio': '1:1', 'resolution': '1k',
                 'width': 1024, 'height': 1024, 'input_images': [], 'batch_size': 1},
         prompt='실사 제품 스튜디오 사진. 흰 무지 배경 위에 놓인 콜드브루 커피 유리병 한 병, 정면, 병 전체가 화면 가운데.\n투명한 원통형 유리병(500ml)에 진한 갈색 커피가 가득 차 있고, 검은 금속 캡.\n병 가운데 크라프트 종이 라벨에 굵은 검은 글씨로 "ONSAE" 와 그 아래 작은 글씨 "COLD BREW · ORIGINAL 500ml".\n부드러운 확산광, 바닥에 옅은 그림자, 깨끗하고 고급스러운 광고 사진. 라벨 외에 다른 글자 · 로고 없음.',
         refs=[], cost=2),
    dict(no='02', name='인물사진', tool='generate_image', job=PERSON, file='prompts\\img_person.txt',
         context='가상 음료 광고 시험용 가상 인물 참조 사진',
         params={'model(요청)': 'nano_banana_pro', 'model(서비스 기록)': 'nano_banana_2', 'aspect_ratio': '3:4', 'resolution': '1k',
                 'width': 896, 'height': 1200, 'input_images': [], 'batch_size': 1},
         prompt='실사 인물 사진. 20대 후반 한국인 여성, 어깨에 닿는 단발 갈색 머리, 크림색 리넨 셔츠, 자연스러운 옅은 화장, 편안한 미소.\n밝은 흰 벽 앞, 창가에서 들어오는 부드러운 자연광, 상반신 정면, 카메라를 바라봄.\n광고 촬영용 고급 실사 사진, 글자 · 로고 없음.',
         refs=[], cost=2),
    dict(no='03', name='컷1_창가뒷모습', tool='generate_video_batch', job='e67b1977-bdfa-4060-9756-67c4a7c7a1f5', file='prompts\\cut1_back.txt',
         context='가상 음료 광고 시험용 실사 1번 컷 재제출(제출 거절분)  ※ 첫 제출(거절, 과금 없음) 때는 「가상 음료 광고 시험용 실사 4컷 생성(컷별 4초)」',
         prompt='16:9 실사 광고 장면, 4초 한 컷. 아침 햇살이 비스듬히 들어오는 창가, 밝은 크림색 벽.\n<<<image_1>>> 의 여성이 창밖을 바라보는 뒷모습. 크림색 리넨 셔츠, 단발 갈색 머리카락이 창으로 들어온 바람에 가볍게 흩날리고 햇살에 반짝인다.\n따뜻한 역광, 허리 위 미디엄 샷, 카메라 고정. 화면에 글자 · 자막 · 로고 없음.',
         refs=[('image_1', PERSON, 'ref_person.png')], cost=4),
    dict(no='04', name='컷2_제품과커피', tool='generate_video_batch', job='4584cb84-31a0-4bed-9d93-9dd0bb019bdc', file='prompts\\cut2_product.txt',
         context='가상 음료 광고 시험용 실사 4컷 생성(컷별 4초)',
         prompt='16:9 실사 제품 광고 장면, 4초 한 컷. 따뜻한 베이지 배경, 밝은 나무 테이블.\n<<<image_1>>> 의 콜드브루 유리병이 화면 가운데 정면에 서 있고 크라프트 라벨이 또렷하게 보인다.\n병 옆 투명 유리잔의 큰 얼음 위로 진한 갈색 콜드브루가 천천히 부어지며 잔 안에 물결이 번진다.\n부드러운 확산광, 카메라가 병 쪽으로 천천히 다가간다. 라벨 외에 화면에 글자 · 자막 · 로고 없음.',
         refs=[('image_1', PRODUCT, 'ref_product.png')], cost=4),
    dict(no='05', name='컷3_인물과탁자위병', tool='generate_video_batch', job='59f57d3c-b636-4d3c-95a1-9f84aee803fd', file='prompts\\cut3_table.txt',
         context='가상 음료 광고 시험용 실사 4컷 생성(컷별 4초)',
         prompt='16:9 실사 광고 장면, 4초 한 컷. 밝은 회색 벽의 아침 카페, 나무 테이블.\n<<<image_1>>> 의 여성이 화면 오른쪽에서 테이블에 팔을 얹고 턱을 손등에 괴 채 카메라를 바라보며 옅게 미소 짓는다.\n테이블 위 화면 가운데에 <<<image_2>>> 의 콜드브루 병과 얼음이 든 커피 잔. 화면 왼쪽 위는 비어 있는 회색 벽.\n부드러운 창가 빛, 카메라 고정. 라벨 외에 화면에 글자 · 자막 · 로고 없음.',
         refs=[('image_1', PERSON, 'ref_person.png'), ('image_2', PRODUCT, 'ref_product.png')], cost=4,
         diff='파일 「괸 채」 → 실제 전송 「괴 채」(요청 작성 때 오타)'),
    dict(no='06', name='컷4_병든인물', tool='generate_video_batch', job='004bcba3-1039-4a21-80e3-e4e330ce9fcf', file='prompts\\cut4_hold.txt',
         context='가상 음료 광고 시험용 실사 4컷 생성(컷별 4초)',
         prompt='16:9 실사 광고 장면, 4초 한 컷. 흰 배경 스튜디오.\n<<<image_1>>> 의 여성이 <<<image_2>>> 의 콜드브루 병을 어깨 높이로 들고 정면을 보며 환하게 미소 짓는다. 단발 갈색 머리카락이 바람에 화면 오른쪽으로 흩날린다.\n인물은 화면 가운데, 양옆은 비어 있는 흰 배경. 카메라가 살짝 다가간다. 라벨 외에 화면에 글자 · 자막 · 로고 없음.',
         refs=[('image_1', PERSON, 'ref_person.png'), ('image_2', PRODUCT, 'ref_product.png')], cost=4,
         diff='파일 「휘날린다」 → 실제 전송 「흩날린다」'),
]
VIDEO_PARAMS = {'model(요청)': 'seedance_2_0', 'mode': 'fast', 'model(서비스 기록)': 'seedance_2_0_fast', 'aspect_ratio': '16:9', 'duration': 4,
                'resolution': '480p', 'width': 854, 'height': 480, 'generate_audio': False, 'genre': 'auto', 'bitrate_mode': 'standard',
                'multi_shots': False, 'speedramp': 'auto', 'prompt_language(서비스 기록값)': 'en'}

for r in REQ:
    d = os.path.join(OUT, f"{r['no']}_{r['name']}")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'prompt.txt'), 'w', encoding='utf-8') as f:
        f.write(r['prompt'] + '\n')
    params = r.get('params') or dict(VIDEO_PARAMS)
    rec = {'도구': r['tool'], '작업 번호': r['job'], '비용(크레딧)': r['cost'], 'params': params,
           'medias': [{'role(요청)': 'image_references', 'role(서비스 기록)': 'image', 'prompt 안 표시': tag, 'value(작업 번호)': job, '가리킨 그림': '..\\참조그림\\' + fn}
                      for tag, job, fn in r['refs']],
           'prompt': 'prompt.txt', 'context(분석용 칸)': r['context']}
    if 'diff' in r:
        rec['프롬프트 파일과 다른 점'] = r['diff']
    with open(os.path.join(d, '요청.json'), 'w', encoding='utf-8') as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)
for fn in ['ref_product.png', 'ref_person.png']:
    shutil.copyfile(os.path.join(R, 'gen', fn), os.path.join(OUT, '참조그림', fn))
print('ok', sorted(os.listdir(OUT)))
