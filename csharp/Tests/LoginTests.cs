using NUnit.Framework;
using Allure.NUnit;
using Allure.Net.Commons;
using Allure.NUnit.Attributes;
using JuiceShopAutomation.Pages;
using System;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace JuiceShopAutomation.Tests
{
    [TestFixture]
    [AllureNUnit]
    [AllureSuite("Authentication")]
    [AllureFeature("Login Capability")]
    public class LoginTests : BaseTest
    {
        private LoginPage _loginPage;
        private RegistrationPage _registrationPage;

        private string _suiteUserEmail;
        private string _suiteUserPassword;

        [SetUp]
        public async Task TestSetupAsync()
        {
            // Initialize page models
            _loginPage = new LoginPage(Page);
            _registrationPage = new RegistrationPage(Page);

            // 1. Generate clean, independent test credentials for this specific test run
            _suiteUserEmail = $"login_vitals_{Guid.NewGuid().ToString("N").Substring(0, 8)}@owasp-juice.shop";
            _suiteUserPassword = "SecurePassword789!";

            // 2. Execute programmatic pre-requisite registration via existing POM components
            await _registrationPage.NavigateToRegistrationAsync();
            await _registrationPage.RegisterUserAsync(_suiteUserEmail, _suiteUserPassword, "AutomatedAnswer");
        }

        [Test]
        [AllureStory("Valid User Login")]
        [AllureStep("Execute end-to-end login with valid credentials")]
        public async Task ShouldLoginSuccessfully()
        {
            // Arrange
            await _loginPage.NavigateToLoginAsync();
            await _loginPage.LoginAsync(_suiteUserEmail, _suiteUserPassword);

            // Assert: Validate application state shifts using web-first assertions[cite: 2]
            // Juice Shop changes the URL layout back to main storefront root hash upon authentication success


           await Expect(Page).ToHaveURLAsync(new Regex(".*search"));

            // Verification of state change (e.g., verifying your basket link or account menu shifts can go here)
            await Expect(_registrationPage.ShoppingCart).ToBeVisibleAsync();
        }
    }
}