#!/usr/bin/env node
/*
 * slide-audit / measure.mjs
 *
 * Uses Playwright to report bounding rects of all layout-critical elements
 * in every slide of an HTML deck. Detects two classes of layout bugs that
 * visual subagents are unreliable at catching:
 *
 *   - children extending beyond their slide canvas (1080px height)
 *   - cards/columns overflowing .slide-content (grid clipping / content cut)
 *
 * Use this BEFORE or ALONGSIDE the visual (subagent) audit. Rect-based
 * diagnostics are deterministic — if they disagree with a subagent, trust
 * the rects.
 *
 * Usage:
 *   node measure.mjs <html-path>
 *
 * Output (stdout, JSON lines):
 *   { idx, issues: [...], content, children }
 * where issues is an array of strings like:
 *   "card[0] bottom=1213 exceeds content bottom=860 by 353"
 *   "col[1] bottom=1041 exceeds canvas 1080 by 0"
 *
 * Exit code 2 if any slide has issues.
 */

import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
import fs from 'node:fs/promises';

const [, , htmlArg] = process.argv;
if (!htmlArg) {
  console.error('Usage: node measure.mjs <html-path>');
  process.exit(1);
}
const htmlPath = path.resolve(htmlArg);
await fs.access(htmlPath);

const browser = await chromium.launch();
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
  reducedMotion: 'reduce',
});
const page = await context.newPage();
await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'networkidle' });

const count = await page.$$eval('.slide', (els) => els.length);

let hadIssue = false;
const report = [];

for (let i = 0; i < count; i++) {
  await page.evaluate((t) => {
    const slides = document.querySelectorAll('.slide');
    slides.forEach((s) => s.classList.remove('is-active'));
    slides[t].classList.add('is-active');
  }, i);
  await page.waitForTimeout(40);

  const measured = await page.evaluate(() => {
    const slide = document.querySelector('.slide.is-active');
    const toRect = (el, label) => {
      if (!el) return null;
      const r = el.getBoundingClientRect();
      return {
        label,
        top: Math.round(r.top),
        bottom: Math.round(r.bottom),
        right: Math.round(r.right),
        height: Math.round(r.height),
      };
    };
    const rects = [];
    const content = toRect(slide.querySelector('.slide-content'), 'content');
    const footer = toRect(slide.querySelector('.slide-footer'), 'footer');

    slide.querySelectorAll('.slide-content .card').forEach((el, i) =>
      rects.push(toRect(el, `card[${i}]`)),
    );
    slide.querySelectorAll('.slide-content .two-col > .col').forEach((el, i) =>
      rects.push(toRect(el, `col[${i}]`)),
    );
    slide.querySelectorAll('.slide-content .hero').forEach((el, i) =>
      rects.push(toRect(el, `hero[${i}]`)),
    );
    slide.querySelectorAll('.slide-content .timeline').forEach((el, i) =>
      rects.push(toRect(el, `timeline[${i}]`)),
    );

    return {
      idx: slide.getAttribute('data-index'),
      content,
      footer,
      children: rects,
    };
  });

  const issues = [];
  const contentBot = measured.content?.bottom ?? 860;
  const canvasBot = 1080;
  for (const c of measured.children) {
    if (c.bottom > contentBot + 1) {
      issues.push(
        `${c.label} bottom=${c.bottom} exceeds content bottom=${contentBot} by ${c.bottom - contentBot}`,
      );
    }
    if (c.bottom > canvasBot + 1) {
      issues.push(
        `${c.label} bottom=${c.bottom} exceeds canvas ${canvasBot} by ${c.bottom - canvasBot}`,
      );
    }
  }
  if (issues.length > 0) hadIssue = true;
  report.push({ idx: measured.idx, issues, content: measured.content, footer: measured.footer });
}

await browser.close();

for (const r of report) {
  const prefix = r.issues.length ? '✗' : '✓';
  const msg = r.issues.length ? r.issues.join('; ') : 'ok';
  console.log(`${prefix} slide ${r.idx}  ${msg}`);
}

console.log('');
const bad = report.filter((r) => r.issues.length > 0).length;
console.log(`${report.length - bad}/${report.length} slides clean, ${bad} with issues`);

process.exit(hadIssue ? 2 : 0);
