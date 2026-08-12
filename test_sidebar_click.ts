import { chromium } from 'playwright';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // Need to make sure the sidebar is wide enough to click without issue
  await page.setViewportSize({ width: 1280, height: 800 });

  // Log any console errors from the page
  page.on('console', msg => {
      if (msg.type() === 'error') {
          console.error(`PAGE LOG: ${msg.text()}`);
      } else {
          console.log(`PAGE LOG: ${msg.text()}`);
      }
  });

  await page.goto('http://localhost:3000');

  console.log("Waiting for .activity-item");
  try {
      await page.waitForSelector('.activity-item', { timeout: 10000 });
      console.log("Found .activity-item");
  } catch (e) {
      console.error("Timeout waiting for .activity-item");
      await page.screenshot({ path: 'verification1.png' });
      await browser.close();
      return;
  }

  // Click the 10th activity that is visible to make sure we get one with coordinates
  const activities = await page.$$('.activity-item');
  let clicked = false;
  let count = 0;
  for (const activity of activities) {
      if (await activity.isVisible()) {
          count++;
          if (count === 10) {
              await activity.click();
              console.log("Clicked activity " + count);
              clicked = true;
              break;
          }
      }
  }

  if (clicked) {
      // Wait for the markers to appear
      try {
          await page.waitForSelector('.start-marker', { timeout: 2000 });
          await page.waitForSelector('.end-marker', { timeout: 2000 });
          console.log("Markers found!");
          await page.screenshot({ path: 'verification.png' });
      } catch(e) {
          console.error("Markers not found after click.");
          await page.screenshot({ path: 'verification_failed.png' });
      }
  } else {
      console.log("Could not find a visible activity to click");
  }

  await browser.close();
})();
