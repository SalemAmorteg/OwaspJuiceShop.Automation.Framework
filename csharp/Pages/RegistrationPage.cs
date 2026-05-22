using Microsoft.Playwright;
using System.Threading.Tasks;

namespace JuiceShopAutomation.Pages
{
    public class RegistrationPage : BasePage
    {
        // 1. Locators

        private ILocator DismissBannerButton => _page.GetByRole(AriaRole.Button, new() { Name = "Close Welcome Banner" });
        private ILocator AccountMenuButton => _page.GetByRole(AriaRole.Button, new() { Name = "Show/hide account menu" });
        private ILocator LoginMenuItem => _page.GetByRole(AriaRole.Menuitem, new() { Name = "Go to login page" });
        private ILocator NewCustomerLink => _page.GetByRole(AriaRole.Link, new() { Name = "Not yet a customer?" });

        // Form Locators
        private ILocator EmailInput => _page.GetByRole(AriaRole.Textbox, new() { Name = "Email address field" });
        private ILocator PasswordInput => _page.GetByRole(AriaRole.Textbox, new() { Name = "Field for the password" });
        private ILocator ConfirmPasswordInput => _page.GetByRole(AriaRole.Textbox, new() { Name = "Field to confirm the password" });
        private ILocator SecurityQuestionDropdown => _page.GetByText("Security Question");
        private ILocator SecurityQuestionOption => _page.GetByText("Your eldest siblings middle");
        private ILocator SecurityAnswerInput => _page.GetByRole(AriaRole.Textbox, new() { Name = "Field for the answer to the" });
        private ILocator RegisterButton => _page.GetByRole(AriaRole.Button, new() { Name = "Button to complete the" });

        // Public locator specifically exposed for the Test layer to assert against
        public ILocator SuccessToastMessage => _page.Locator("simple-snack-bar").Filter(new() { HasText = "Registration completed successfully" });
        public ILocator ShoppingCart => _page.GetByRole(AriaRole.Button, new() { Name = "Show the shopping cart" });

        public RegistrationPage(IPage page) : base(page) { }

        // 2. Actions

        public async Task NavigateToRegistrationAsync()
        {
            // Note: Base URL should ideally be managed by environment configuration, not hardcoded.
            await NavigateToAsync("register");
            
            // Dismiss banner to prevent click interception on the account menu
            if (await DismissBannerButton.IsVisibleAsync())
            {
                await DismissBannerButton.ClickAsync();
            }

            await AccountMenuButton.ClickAsync();
            await LoginMenuItem.ClickAsync();
            await NewCustomerLink.ClickAsync();
        }
        public async Task RegisterUserAsync(string email, string password, string securityAnswer)
        {
            await EmailInput.FillAsync(email);
            await PasswordInput.FillAsync(password);
            await ConfirmPasswordInput.FillAsync(password);

            // Handle the Material UI dropdown interaction
            await SecurityQuestionDropdown.ClickAsync();
            await SecurityQuestionOption.ClickAsync();

            await SecurityAnswerInput.FillAsync(securityAnswer);

            await RegisterButton.ClickAsync();
        }
    }
}