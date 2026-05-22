using Microsoft.Playwright.NUnit;
using Microsoft.Playwright;
using NUnit.Framework;
using NUnit.Framework.Interfaces;
using Allure.Net.Commons;
using System;
using System.IO;
using System.Threading.Tasks;

namespace JuiceShopAutomation.Tests
{
    // Inheriting from PageTest provides the 'Page' and 'Expect' objects automatically.
    public class BaseTest : PageTest
    {
        [SetUp]
        public async Task BaseSetup()
        {
            // Set a global timeout for all actions (10 seconds).
            // This is a Senior practice to prevent tests from hanging indefinitely.
            Page.SetDefaultTimeout(10000);
            await Context.Tracing.StartAsync(new()
            {
                Screenshots = true,
                Snapshots = true,
                Sources = true
            });

            // LOGIC TIP: Here we can add global 'Before' steps, 
            // like clearing cookies or logging the start of a test.
        }

        [TearDown]
        public async Task AttachArtifactsOnFailureAsync()
        {
            // Check if the current NUnit test failed
            if (TestContext.CurrentContext.Result.Outcome.Status == TestStatus.Failed)
            {
                // 1. Capture and attach Screenshot
                var screenshotPath = Path.Combine(Directory.GetCurrentDirectory(), $"screenshot_{Guid.NewGuid()}.png");
                await Page.ScreenshotAsync(new() { Path = screenshotPath, FullPage = true });
                AllureApi.AddAttachment("Failed Screenshot", "image/png", screenshotPath);

                // 2. Capture and attach Playwright Trace[cite: 2]
                var tracePath = Path.Combine(Directory.GetCurrentDirectory(), $"trace_{Guid.NewGuid()}.zip");
                await Context.Tracing.StopAsync(new() { Path = tracePath });
                AllureApi.AddAttachment("Playwright Trace Viewer", "application/zip", tracePath);
            }
            else
            {
                // If the test passed, stop tracing without saving to preserve disk space and CI speed
                await Context.Tracing.StopAsync();
            }
        }
    }
}