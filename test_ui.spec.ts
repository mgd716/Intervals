import { test, expect } from '@playwright/test';
import * as fs from 'fs';

test('verify sort toggle UI', async ({ page }) => {
    await page.goto('http://localhost:3000');

    // Wait for the map and activities to load
    await page.waitForSelector('.activity-item');

    // Take screenshot of default view
    await page.screenshot({ path: 'frontend_verification_default.png' });

    // Click the toggle sort direction button
    await page.click('#sort-dir-btn');

    // Wait a short moment for DOM re-order
    await page.waitForTimeout(500);

    // Take screenshot of toggled view
    await page.screenshot({ path: 'frontend_verification_toggled.png' });

    // Click the select box and pick "Sort: Distance"
    await page.selectOption('#sort-select', 'distance');

    // Wait a short moment for DOM re-order
    await page.waitForTimeout(500);

    // Take screenshot to show reset
    await page.screenshot({ path: 'frontend_verification_distance.png' });

    console.log('Screenshots generated successfully.');
});
