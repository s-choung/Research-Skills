#!/usr/bin/env node
/*
 * slide-audit / screenshot.mjs
 *
 * Renders each slide in an HTML deck to a 1920x1080 PNG.
 *
 * Assumptions about the target deck:
 *   - Slides are <section class="slide" data-index="NN">
 *   - CSS default: .slide { opacity: 0 }, .slide.is-active { opacity: 1 }
 *   - Canvas is 1920x1080, center-anchored
 *
 * Usage:
 *   node screenshot.mjs <html-path> [outdir]
 *
 * Output:
 *   <outdir>/slide_NN.png  (one per slide)
 *   <outdir>/manifest.json (source + ordered slide list)
 */

import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
import fs from 'node:fs/promises';

const [, , htmlArg, outArg] = process.argv;

if (!htmlArg) {
  console.error('Usage: node screenshot.mjs <html-path> [outdir]');
  process.exit(1);
}

const htmlPath = path.resolve(htmlArg);
try {
  await fs.access(htmlPath);
} catch {
  console.error(`File not found: ${htmlPath}`);
  process.exit(1);
}

const baseName = path.basename(htmlPath, '.html');
const outDir = outArg
  ? path.resolve(outArg)
  : path.join(path.dirname(htmlPath), '_screenshots', baseName);

await fs.mkdir(outDir, { recursive: true });

console.log(`▸ source:  ${htmlPath}`);
console.log(`▸ outdir:  ${outDir}`);

const browser = await chromium.launch();
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
  reducedMotion: 'reduce',
});
const page = await context.newPage();

page.on('pageerror', (err) => console.warn(`  [page error] ${err.message}`));

await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'networkidle' });

// Hide fixed overlay hints (keyboard nav text etc.) so they don't leak into screenshots
await page.addStyleTag({
  content: '.progress, [data-screenshot-hide] { display: none !important; }',
});

const indices = await page.$$eval('.slide', (els) =>
  els.map((el, i) => ({ i, idx: el.getAttribute('data-index') || String(i + 1) })),
);

if (indices.length === 0) {
  console.error('No .slide elements found. Is this the right HTML?');
  await browser.close();
  process.exit(2);
}

console.log(`▸ slides:  ${indices.length}`);

const manifest = [];
for (const { i, idx } of indices) {
  await page.evaluate((target) => {
    const slides = document.querySelectorAll('.slide');
    slides.forEach((s) => s.classList.remove('is-active'));
    slides[target].classList.add('is-active');
  }, i);

  // small paint wait
  await page.waitForTimeout(80);

  const fname = `slide_${String(idx).padStart(2, '0')}.png`;
  const fpath = path.join(outDir, fname);
  await page.screenshot({
    path: fpath,
    clip: { x: 0, y: 0, width: 1920, height: 1080 },
  });
  manifest.push({ index: idx, file: fpath });
  process.stdout.write(`  ✓ ${fname}\n`);
}

await browser.close();

const manifestPath = path.join(outDir, 'manifest.json');
await fs.writeFile(
  manifestPath,
  JSON.stringify({ source: htmlPath, count: manifest.length, slides: manifest }, null, 2),
);

console.log(`▸ wrote ${manifest.length} screenshots`);
console.log(`▸ manifest: ${manifestPath}`);
