using Microsoft.Playwright;
using Microsoft.Playwright.NUnit;
using NUnit.Framework;
using JuiceShopAutomation.Pages;
using System.Text.RegularExpressions;
using System;
using System.Threading.Tasks;
using Microsoft.VisualStudio.TestPlatform.Utilities;

namespace JuiceShopAutomation.Tests
{
    [TestFixture]
    public class RegistrationTests : BaseTest
    {
        private RegistrationPage _registrationPage;

        [SetUp]
        public void TestSetup()
        {
            _registrationPage = new RegistrationPage(Page);
        }

        [Test]
        [Category("Regression")]
        public async Task ShouldRegisterNewUserSuccessfully()
        {
            // 1. Arrange: Generate unique test data to ensure CI stability
            string uniqueEmail = $"qa_user_{Guid.NewGuid().ToString("N").Substring(0, 8)}@owasp-juice.shop";
            string validPassword = "ComplexPassword123!";
            string securityAnswer = "AutomatedAnswer";

            // 2. Act: Execute the business flow via POM
            await _registrationPage.NavigateToRegistrationAsync();
            await _registrationPage.RegisterUserAsync(uniqueEmail, validPassword, securityAnswer);
            Console.WriteLine(uniqueEmail);
            Console.WriteLine(validPassword);
            Console.WriteLine(securityAnswer);
            // 3. Assert: Validate application state and user expectations using web-first assertions
            
            // Verify the success toast appears
            await Expect(_registrationPage.SuccessToastMessage).ToBeVisibleAsync();
            
            // Verify Juice Shop redirects the user to the login page upon successful registration
            await Expect(Page).ToHaveURLAsync(new Regex(".*login"));
        }
    }
}

