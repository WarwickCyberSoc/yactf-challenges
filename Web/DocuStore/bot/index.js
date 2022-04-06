const puppeteer = require("puppeteer");

const browser_options = {
  headless: true,
  args: [
    "--no-sandbox",
    "--disable-background-networking",
    "--disable-default-apps",
    "--disable-extensions",
    "--disable-gpu",
    "--disable-sync",
    "--disable-translate",
    "--hide-scrollbars",
    "--metrics-recording-only",
    "--mute-audio",
    "--no-first-run",
    "--safebrowsing-disable-auto-update",
    "--js-flags=--noexpose_wasm,--jitless", // yoinking from strellic :sice:
  ],
  executablePath: "google-chrome-stable",
};

const adminCookie = "eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2VyX2lkIjoxfQ.YgKJgw.VHE33YpQe-RVNXjYYbgCkMqd36Q";
const websiteURL = "http://localhost";

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

const cachedDocuments = new Set();

(async () => {
  while (true) {
    console.log("Viewing submissions...");

    const browser = await puppeteer.launch(browser_options);
    const page = await browser.newPage();

    await page.goto(websiteURL, {
      waitUntil: "networkidle2",
      timeout: 15_000,
    });

    await page.setCookie({
      name: "session",
      value: adminCookie,
      httpOnly: true,
    });

    await page.goto(`${websiteURL}/documents/shared`, {
      waitUntil: "networkidle2",
      timeout: 15_000,
    });

    const documents = await page.$$eval(".document-link", (el) => el.map((x) => x.getAttribute("document-id")));

    for (const id of documents) {
      if (!id || cachedDocuments.has(id)) continue;
      console.log("Viewing", id);
      try {
        await page.goto(`${websiteURL}/viewdocument/${id}`, {
          waitUntil: "networkidle2",
          timeout: 10_000,
        });
        await sleep(2_500);
      } catch (err) {
        console.warn("Got error while reviewing ", url, err);
      }

      cachedDocuments.add(id);
    }

    await browser.close();

    console.log("Waiting for new submissions");
    await sleep(15_000);
  }
})();
