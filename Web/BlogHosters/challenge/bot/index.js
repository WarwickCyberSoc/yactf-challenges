const puppeteer = require("puppeteer");
const sqlite3 = require("sqlite3");
const { open } = require("sqlite");

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

const viewSubmission = async (url) => {
  const browser = await puppeteer.launch(browser_options);
  const page = await browser.newPage();

  try {
    await page.goto(url, {
      waitUntil: "networkidle2",
      timeout: 15_000,
    });

    const approveButton = await page.$$(".approve-button");
    if (approveButton.length == 1) {
      console.log("Approved!");
      approveButton[0].click();
    }
    await page.waitForTimeout(2500);
  } catch (err) {
    console.warn("Got error while reviewing ", url, err);
  }

  await browser.close();
};

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

(async () => {
  const db = await open({ filename: "../database.db", driver: sqlite3.Database });

  while (true) {
    console.log("Viewing new submissions...");
    const users = await db.all("SELECT * FROM users WHERE unapproved_blog_content != ''");

    for (const user of users) {
      const { magic_code } = await db.get("SELECT *  FROM users WHERE username = $username", ["support_katie"]);

      await db.run("UPDATE users SET being_reviewed = 1, last_review_time = $time WHERE id = $id", {
        $id: user.id,
        $time: new Date().toUTCString(),
      });
      console.log("Reviewing", user.username);
      try {
        await viewSubmission(`http://127.0.0.1:5000/blog/${user.username}?magic_code=${magic_code}&reviewing=1`);
      } catch (err) {
        console.warn("Got browser error when reviewing", user.username, err);
      }

      await db.run("UPDATE users SET being_reviewed = 0 WHERE id = $id", { $id: user.id });
    }

    console.log("Waiting for new submissions");
    await sleep(15_000);
  }
})();
