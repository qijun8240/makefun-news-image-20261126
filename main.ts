// News-image entry (Node 22, standard library only): copies the
// pre-rendered entry.png beside this file to /output/entry.png.
// Validates the PNG signature, size (at most 1 MiB) and dimensions
// (at most 1024x1024) first, so a bad image fails loudly instead
// of submitting silently. Run twice, it writes the same bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in
// for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const SRC = new URL('./entry.png', import.meta.url);

const bytes = readFileSync(SRC);

// PNG signature: 89 50 4E 47 0D 0A 1A 0A.
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error('entry.png is not a PNG file');
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}

// IHDR width and height are big-endian uint32 at bytes 16 and 20.
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}

mkdirSync(OUT_DIR, { recursive: true });
const DEST = join(OUT_DIR, 'entry.png');
copyFileSync(SRC, DEST);

// Confirm the copy landed whole: same byte count as the source.
const written = readFileSync(DEST);
if (written.length !== bytes.length || !written.equals(bytes)) {
  throw new Error('entry.png copy does not match the source');
}
console.log(`wrote ${width}x${height} entry.png (${bytes.length} bytes) to ${OUT_DIR}`);
