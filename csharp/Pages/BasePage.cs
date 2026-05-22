using Microsoft.Playwright;
using Microsoft.Extensions.Configuration;
using System.Threading.Tasks;
using System;
using System.IO;

namespace JuiceShopAutomation.Pages
{
    // The BasePage is abstract because it should never be instantiated directly.
    // It exists only to be inherited by specific pages like LoginPage or RegisterPage.
    public abstract class BasePage
    {


        // Protected access allows derived classes (children) to use the Playwright Page instance.
        protected readonly IPage _page;
        private static readonly string _baseUrl;

        static BasePage()
        {
            // 1. Build a unified configuration matrix provider
            var configuration = new ConfigurationBuilder()
                .SetBasePath(Directory.GetCurrentDirectory()) // Point to execution output directory
                .AddJsonFile("appsettings.json", optional: true, reloadOnChange: true) // Load local JSON settings
                .AddEnvironmentVariables() // Overlays environment updates (e.g. from GitHub Actions)
                .Build();

            // 2. Extract configuration value safely using standard colon syntax
            // If both sources are missing, it defaults to localhost as a last resort
            _baseUrl = configuration["AutomationSettings:BaseUrl"] ?? "http://localhost:3000";
        }

        // The constructor initializes the page instance passed from the Test layer.
        public BasePage(IPage page)
        {
            _page = page;
        }

        // Shared locators for global elements found on every page.
        // We follow our Engineering Standard: Prioritize get_by_role and get_by_label.
        private ILocator NavAccountButton => _page.GetByRole(AriaRole.Button, new() { Name = "Account" });
        private ILocator NavLoginButton => _page.GetByRole(AriaRole.Button, new() { Name = "Login" });
        private ILocator SearchIcon => _page.GetByLabel("Show/hide search bar");
        private ILocator DismissBannerButton => _page.GetByRole(AriaRole.Button, new() { Name = "Close Welcome Banner" });

        // Common Action: Navigation to a specific URL.
        // This abstracts the Playwright GoToAsync method for cleaner test code.
        public async Task NavigateToAsync(string path = "")
        {
            // Clean handling of trailing slashes and hash prefixes
            string targetRoute = string.IsNullOrEmpty(path) ? "/#/" : $"/#/{path}";
            
            // Combines into: http://localhost:3000/#/register
            await _page.GotoAsync($"{_baseUrl.TrimEnd('/')}{targetRoute}");
        }

        // Common Action: Navigating to the Login Screen via the global Nav Bar.
        // This is a "Helper Method" that promotes reusability across different test flows[cite: 2].
        public async Task GoToLoginViaNav()
        {
            await NavAccountButton.ClickAsync();
            await NavLoginButton.ClickAsync();
        }

        // Global Verification: Check if a specific header is visible.
        // Note: We avoid putting business assertions here, but helper methods for visibility are acceptable[cite: 2].
        public async Task<bool> IsPageHeaderVisible(string headerText)
        {
            return await _page.GetByRole(AriaRole.Heading, new() { Name = headerText }).IsVisibleAsync();
        }
    }
}