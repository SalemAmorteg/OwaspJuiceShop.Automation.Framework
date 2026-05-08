using Microsoft.Playwright;
using System.Threading.Tasks;

namespace JuiceShopAutomation.Pages
{
    // LoginPage inherits from BasePage to access the _page instance and global Nav methods.
    public class LoginPage : BasePage
    {
        // 1. Define Locators
        // We use Playwright's 'GetBy' methods which are more resilient than XPaths.
        private ILocator EmailInput => _page.GetByLabel("Text field for the login email");
        private ILocator PasswordInput => _page.GetByLabel("Text field for the login password");
        private ILocator LoginButton => _page.GetByRole(AriaRole.Button, new() { Name = "Log in" });
        private ILocator ErrorMessage => _page.Locator(".error"); // Example for dynamic error messages
        private ILocator RegistrationLink => _page.GetByRole(AriaRole.Link, new() { Name = "Not yet a customer?" });

        // 2. Constructor
        // We pass the IPage from the test layer up to the BasePage.
        public LoginPage(IPage page) : base(page) { }

        // 3. Actions (Methods)
        
        // Method to perform the full login flow.
        // This is a "Composite Action" that simplifies our Test scripts.
        public async Task LoginAsync(string email, string password)
        {
            // Enter the email
            await EmailInput.FillAsync(email);
            
            // Enter the password
            await PasswordInput.FillAsync(password);
            
            // Click the Login button
            await LoginButton.ClickAsync();
        }

        // Method to navigate to the Registration page from the Login screen.
        public async Task GoToRegistrationAsync()
        {
            await RegistrationLink.ClickAsync();
        }

        // Helper to check if a login error is visible (Negative Testing)
        public async Task<bool> IsErrorMessageVisible()
        {
            // We use 'IsVisibleAsync' to return a boolean for assertions in the Test layer.
            return await ErrorMessage.IsVisibleAsync();
        }
    }
}