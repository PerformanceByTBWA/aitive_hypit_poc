// compose.mjs — 시댄스 480p 결과를 원본 광고와 합치고 비교 영상 만들기
//   node compose.mjs <seedance_raw.mp4> <c1,c2,c3,c4 = 생성 영상 안 컷 시작(초)>
// - swap.mp4: 원본 15초 타임라인에서 실사 컷 4자리(0–1.335 · 1.335–2.970 · 2.970–4.671 · 6.333–7.233)만 생성 컷으로 교체, 소리 = 원본 그대로
// - compare.mp4: 왼쪽 원본 · 오른쪽 교체본(각 960×540) + 위 이름표, 소리 = 원본
// - sheet.jpg: 원본 참조 프레임 4장 ↔ 생성 컷 가운데 프레임 4장
import { createRequire } from 'node:module';
import { execFileSync } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
const require = createRequire('C:/Users/youngkwangnam/Desktop/claude/hypit-explainer/package.json');
const ff = require('ffmpeg-static');

const W = join(dirname(fileURLToPath(import.meta.url)), '..');
const SRC = 'C:/Users/youngkwangnam/Desktop/claude/shortform-test/oss_eval/hypit/v1012/단계별/00_원본가져오기/출력/source.mp4';
const RAW = process.argv[2];
const CUT = process.argv[3].split(',').map(Number); // 생성 영상 안 컷 시작
const FONT = 'C\\:/Windows/Fonts/malgunbd.ttf';
const run = (args) => execFileSync(ff, ['-y', '-loglevel', 'error', ...args], { stdio: ['ignore', 'inherit', 'inherit'] });

// 원본 자리(초) ← 생성 컷 번호 · 생성 컷 안에서 쓸 시작(컷 시작 + 여유)
const SLOTS = [
  { a: 0.0, b: 1.335, cut: 0 },
  { a: 1.335, b: 2.970, cut: 1 },
  { a: 2.970, b: 4.671, cut: 2 },
  { a: 6.333, b: 7.233, cut: 3 },
];
const PAD = 0.4; // 컷 경계 바로 뒤는 피함
const DUR = 15.015;

// 원본 구간 목록(교체 자리 사이는 원본)
const segs = [];
let t = 0;
for (const s of SLOTS) {
  if (s.a > t + 1e-3) segs.push({ src: 'orig', from: t, len: s.a - t });
  segs.push({ src: 'gen', from: CUT[s.cut] + PAD, len: s.b - s.a });
  t = s.b;
}
if (t < DUR) segs.push({ src: 'orig', from: t, len: DUR - t });

const fc = [];
segs.forEach((g, i) => {
  const inp = g.src === 'orig' ? 0 : 1;
  fc.push(`[${inp}:v]trim=start=${g.from.toFixed(3)}:duration=${g.len.toFixed(3)},setpts=PTS-STARTPTS,scale=1920:1080:flags=lanczos,fps=30,format=yuv420p[s${i}]`);
});
fc.push(`${segs.map((_, i) => `[s${i}]`).join('')}concat=n=${segs.length}:v=1:a=0[v]`);
run(['-i', SRC, '-i', RAW, '-filter_complex', fc.join(';'), '-map', '[v]', '-map', '0:a', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-shortest', join(W, 'swap.mp4')]);

// 나란히 비교
const label = (txt) => `drawtext=fontfile='${FONT}':text='${txt}':fontcolor=white:fontsize=30:x=(w-text_w)/2:y=18`;
run(['-i', SRC, '-i', join(W, 'swap.mp4'), '-filter_complex',
  `[0:v]scale=960:540,fps=30,pad=960:610:0:70:color=0x14141c,${label('원본')}[l];` +
  `[1:v]scale=960:540,fps=30,pad=960:610:0:70:color=0x14141c,${label('시댄스 480p 실사 4컷 교체')}[r];[l][r]hstack[v]`,
  '-map', '[v]', '-map', '0:a', '-c:v', 'libx264', '-crf', '20', '-preset', 'medium', '-c:a', 'aac', '-b:a', '160k', '-shortest', join(W, 'compare.mp4')]);

// 참조 ↔ 생성 대조 그림
const mids = CUT.map((c, i) => (i < 3 ? (c + CUT[i + 1]) / 2 : c + 2));
const ins = [];
['ref1_hair', 'ref2_product', 'ref3_table', 'ref4_bottle'].forEach((n) => ins.push('-i', join(W, 'ref', `${n}.jpg`)));
mids.forEach((m) => ins.push('-ss', m.toFixed(2), '-i', RAW));
const f2 = [];
for (let i = 0; i < 4; i++) f2.push(`[${i}:v]scale=640:360[r${i}]`, `[${i + 4}:v]scale=640:360,trim=end_frame=1[g${i}]`);
f2.push(`${[0, 1, 2, 3].map((i) => `[r${i}][g${i}]`).join('')}xstack=inputs=8:layout=0_0|w0_0|0_h0|w0_h0|0_h0+h0|w0_h0+h0|0_h0+h0+h0|w0_h0+h0+h0[v]`);
run([...ins, '-filter_complex', f2.join(';'), '-map', '[v]', '-frames:v', '1', '-q:v', '3', join(W, 'sheet.jpg')]);
console.log('swap.mp4 · compare.mp4 · sheet.jpg', JSON.stringify({ segs, mids }));
