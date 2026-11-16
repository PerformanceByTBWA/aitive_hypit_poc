# v1012 · 애디렉트 「모두의 TV광고」 15초 Hypit 분석·재현 (2026-11-11)

- 원본: 20261012134955001.mp4 (15.015초 · 1920×1080 · 29.97fps, SHA-256 3b34fa82…261489) — 서버 proj_serum\references\v1012\source.mp4
- 페이지: https://claude.ai/artifact/YQvnYNMrBGjjMjz6uqbnWd (비공개, 단계별 지침·입력·출력), 같은 내용 별도 아티팩트 https://claude.ai/artifact/HeU6jRBLPUc8GHC6ZafKEP (page\hypit-v1012.html)
- 위키용 markdown: wiki\hypit-v1012-wiki.md (게시 안 함)
- 판단 기록: ANALYSIS.md · TIMELINE.md · PROGRESS.md
- 받아쓰기: transcript.json (ko, 22어절 5구간)
- 근거 그림: evidence\ (whole_1s · words_05s · hook · ttalkkak · process · endcard · cuts\ 모든 프레임 · full\ 원본 해상도)
- 명령 입력·출력 원문: io\ (번호 = 단계)
- 영상 코드: src\v1012.svml · v1012.svrun · recipes_v1012.svs, 서버 실행 스크립트 src\st*.ps1
- 결과: out\v1012_replica.mp4 (1920×1080 30fps 15.0초) · out\alignment\value.json · out\caption-timing\value.json
- 스킬 원문 사본: skill-ref\skills\hypit (hypit-ai/hypit v0.3.1, 서버 미설치라 공개 저장소에서 받음)
- 페이지 생성: page\ ← src\build_page.py, 위키 md ← src\build_wiki.py (인자 = 이 v1012 폴더 경로)
- 단계별 모음: 단계별\ (00~11 단계마다 지침\·입력\·출력\·README.md, 진입점 단계별\README.md, 생성 스크립트 src\collect_stages.py)
- ★입출력 설명용 합본: 단계별_입출력_설명.md (단계별\ 00~11 README 를 한 파일로, 맨 앞 큰 그림 표)
- 교체판(11/16): src\v1012_gen.svml · v1012_gen.svrun → out\v1012_gen\v1012_gen.mp4 (실사 4자리를 seedance480\seedance_raw.mp4 컷으로, Hypit 빌드 9요청·로컬 0원·61초), 서버 실행 src\st10.ps1, 기록 io\gen_*.txt
- 생성 시험(11/14): seedance480\ (Higgsfield Seedance 2.0 fast 480p 15초 1회, 15크레딧)
- 단계별 갱신(11/16): src\update_stages.py(서버 경로·깨진 기호 정리, 06 애디렉트 입력, 09 실제 생성, 07·08·10·11 교체판 출력) · src\write_readmes.py(06~11 README·맨 위 README·합본)
- ★콜드브루판(11/16, 전체 재생성): remake\ — BRIEF.md · prompts\ · gen\(참조 사진 2 · 실사 4컷 · 요청기록.json, 20크레딧) · packages\addirect-scenes\(Hypit 그래픽 부품) · src\remake.svml · out\remake.mp4 · compare_원본_콜드브루판.mp4, 입출력 문서 remake\단계별_입출력_콜드브루판.md
