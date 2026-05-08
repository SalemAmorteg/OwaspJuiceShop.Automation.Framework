using Microsoft.Playwright.NUnit;
using NUnit.Framework;
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

            // LOGIC TIP: Here we can add global 'Before' steps, 
            // like clearing cookies or logging the start of a test.
        }

        [TearDown]
        public async Task BaseTearDown()
        {
            // If a test fails, this is where we would trigger the screenshot logic
            // for your Reporting ownership.
            if (TestContext.CurrentContext.Result.Outcome.Status == NUnit.Framework.Interfaces.TestStatus.Failed)
            {
                await Page.ScreenshotAsync(new() 
                { 
                    Path = $"Failures/{TestContext.CurrentContext.Test.Name}.png",
                    FullPage = true 
                });
            }
        }
    }
}