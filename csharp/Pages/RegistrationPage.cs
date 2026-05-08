using Microsoft.Playwright;
using System.Text.RegularExpressions;

namespace JuiceShopAutomation.Pages
{
    public class RegistrationPage : BasePage
    {
        // 1. Locators
        private ILocator EmailInput => _page.GetByLabel("Email address field");
        private ILocator PasswordInput => _page.GetByLabel("Field for the password");
        private ILocator RepeatPasswordInput => _page.GetByLabel("Field to confirm the password");

        // The security question involves clicking the dropdown then selecting an option
        private ILocator SecurityQuestionDropdown => _page.GetByRole(AriaRole.Combobox, new() { Name = "Security Question"});
        private ILocator SecurityAnswerInput => _page.GetByLabel("Field for the answer to the security question");

        private ILocator RegisterButton => _page.GetByRole(AriaRole.Button, new() { Name = "Register" });

        public RegistrationPage(IPage page) : base(page) { }

        // 2. Actions
        public async Task RegisterUserAsync(string email, string password, string answer)
        {
            await EmailInput.FillAsync(email);
            await PasswordInput.FillAsync(password);
            await RepeatPasswordInput.FillAsync(password);

            // Interaction with Material UI Dropdowns
            await SecurityQuestionDropdown.ClickAsync();
            // We pick the first option in the list for simplicity in this sprint
            await _page.GetByRole(AriaRole.Option).First.ClickAsync();

            await SecurityAnswerInput.FillAsync(answer);
            await RegisterButton.ClickAsync();
        }
    }
}