const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage();

    // Catch console logs to see what's failing
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));

    // We can intercept Supabase requests and provide mock data!
    await page.route('**/rest/v1/activities*', async route => {
        const json = [
            {
                id: '1',
                name: 'Mock Activity for Testing',
                type: 'Ride',
                distance: 25000,
                moving_time: 3600,
                elevation_gain: 150,
                start_date_local: '2023-10-15T10:00:00Z',
                coordinates: [
                    [43.6532, -79.3832], // Toronto start
                    [43.7000, -79.4000],
                    [43.7500, -79.4500]  // End
                ]
            }
        ];
        await route.fulfill({ json });
    });

    await page.goto('http://localhost:3000');

    // Wait for the mock activity to render
    await page.waitForSelector('.activity-item', { timeout: 10000 });

    // Click the mock activity
    await page.click('.activity-item');

    // Wait a moment for map to zoom and markers to appear
    await page.waitForTimeout(2000);

    // Take a screenshot
    await page.screenshot({ path: 'verification_mock.png' });

    console.log("Mock test completed and screenshot saved.");
    await browser.close();
})();
