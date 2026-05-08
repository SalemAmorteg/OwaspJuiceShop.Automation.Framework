using Microsoft.Playwright;
using System.Threading.Tasks;

namespace JuiceShopAutomation.Pages
{
    // The BasePage is abstract because it should never be instantiated directly.
    // It exists only to be inherited by specific pages like LoginPage or RegisterPage.
    public abstract class BasePage
    {

        public static string BaseUrl => "http://localhost:3000/#";


        // Protected access allows derived classes (children) to use the Playwright Page instance.
        protected readonly IPage _page;

        // Shared locators for global elements found on every page.
        // We follow our Engineering Standard: Prioritize get_by_role and get_by_label.
        private ILocator NavAccountButton => _page.GetByRole(AriaRole.Button, new() { Name = "Account" });
        private ILocator NavLoginButton => _page.GetByRole(AriaRole.Button, new() { Name = "Login" });
        private ILocator SearchIcon => _page.GetByLabel("Show/hide search bar");

        // The constructor initializes the page instance passed from the Test layer.
        protected BasePage(IPage page)
        {
            _page = page;
        }

        // Common Action: Navigation to a specific URL.
        // This abstracts the Playwright GoToAsync method for cleaner test code.
        public async Task NavigateToAsync(string path = "")
        {
            await _page.GotoAsync($"http://localhost:3000/#{path}");
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