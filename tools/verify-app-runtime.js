const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright-core");

const EDGE_PATHS = [
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
];

const BASE_URL = "http://127.0.0.1:5500/nanoin.html";
const TOPICS = ["nanoin", "xrf", "taver", "epma", "ir"];
const SECTIONS = ["intro", "principle", "concepts", "visual", "diagnosis", "ai", "mastery", "record"];

function findEdge() {
  for (const candidate of EDGE_PATHS) {
    if (fs.existsSync(candidate)) {
      return candidate;
    }
  }
  throw new Error("Microsoft Edge executable not found.");
}

async function assertNoFatalError(page, topic, section) {
  const text = await page.locator("body").innerText();
  if (text.includes("BOOT ERROR") || text.includes("RENDER ERROR")) {
    throw new Error(`${topic}:${section} fatal error detected`);
  }
}

async function validateSection(page, section) {
  if (section === "intro") {
    await page.locator("main section").first().waitFor();
    return { ok: true };
  }

  if (section === "principle") {
    await page.locator(".principle-grid, .principle-scene-card").first().waitFor();
    return { ok: true };
  }

  if (section === "concepts") {
    await page.locator(".concept-layout-stack, .concept-node-grid").first().waitFor();
    return { ok: true };
  }

  if (section === "visual") {
    await page.locator("#visualChart").waitFor();
    await page.waitForTimeout(500);
    const canvasInfo = await page.evaluate(() => {
      const canvas = document.querySelector("#visualChart");
      if (!canvas) {
        return null;
      }
      const ctx = canvas.getContext("2d", { willReadFrequently: true });
      if (!ctx) {
        return { width: canvas.width, height: canvas.height, nonTransparentPixels: 0 };
      }
      const image = ctx.getImageData(0, 0, canvas.width, canvas.height);
      let nonTransparentPixels = 0;
      for (let i = 3; i < image.data.length; i += 4) {
        if (image.data[i] !== 0) {
          nonTransparentPixels += 1;
          if (nonTransparentPixels > 200) {
            break;
          }
        }
      }
      return { width: canvas.width, height: canvas.height, nonTransparentPixels };
    });
    if (!canvasInfo || !canvasInfo.width || !canvasInfo.height || canvasInfo.nonTransparentPixels === 0) {
      throw new Error("visual chart did not render");
    }
    return canvasInfo;
  }

  if (section === "diagnosis") {
    await page.locator(".diagnosis-choice").first().waitFor();
    return { ok: true };
  }

  if (section === "ai") {
    await page.locator("#aiPrompt").waitFor();
    return { ok: true };
  }

  if (section === "mastery") {
    await page.locator('[data-action="answer-mastery"]').first().waitFor();
    return { ok: true };
  }

  if (section === "record") {
    await page.locator(".skill-card, .metric-card").first().waitFor();
    return { ok: true };
  }

  return { ok: true };
}

async function verifyTopic(browser, topic) {
  const context = await browser.newContext({
    viewport: { width: 1440, height: 1200 },
  });
  await context.addInitScript(() => {
    window.localStorage.clear();
  });

  const page = await context.newPage();
  const url = `${BASE_URL}?topic=${topic}`;
  const topicResult = { topic, sections: [], ok: true };

  try {
    await page.goto(url, { waitUntil: "networkidle", timeout: 45000 });
    await page.locator("main").waitFor({ timeout: 10000 });
    await assertNoFatalError(page, topic, "intro");

    for (const section of SECTIONS) {
      const selector = `[data-action="goto-section"][data-section="${section}"]`;
      const button = page.locator(selector).first();
      if (await button.count()) {
        await button.click();
        await page.waitForTimeout(350);
      }
      await assertNoFatalError(page, topic, section);
      const details = await validateSection(page, section);
      topicResult.sections.push({ section, ok: true, details });
    }
  } catch (error) {
    topicResult.ok = false;
    topicResult.error = error.message;
  } finally {
    await context.close();
  }

  return topicResult;
}

async function main() {
  const edgePath = findEdge();
  const browser = await chromium.launch({
    headless: true,
    executablePath: edgePath,
    args: ["--disable-gpu"],
  });

  const results = [];
  try {
    for (const topic of TOPICS) {
      results.push(await verifyTopic(browser, topic));
    }
  } finally {
    await browser.close();
  }

  const summary = {
    ok: results.every((item) => item.ok),
    topics: results,
  };

  const outputPath = path.join(process.cwd(), "tmp-runtime-verify.json");
  fs.writeFileSync(outputPath, JSON.stringify(summary, null, 2), "utf8");
  console.log(JSON.stringify(summary, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
