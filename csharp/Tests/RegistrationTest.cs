using Microsoft.Playwright;
using NUnit.Framework;
using JuiceShopAutomation.Pages;
using System;
using System.Threading.Tasks;

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
            // 1. Arrange
            // We use a timestamp to ensure the email is always unique
            string uniqueEmail = $"C#user_{DateTime.Now.Ticks}@test.com";
            string password = "Password123!";
            
            await _registrationPage.NavigateToAsync("register");

            // 2. Act
            await _registrationPage.RegisterUserAsync(uniqueEmail, password, "My First Pet");
            
            Console.WriteLine(uniqueEmail, password);
            // 3. Assert
            // After successful registration, Juice Shop redirects back to Login
            await Expect(Page).ToHaveURLAsync(new System.Text.RegularExpressions.Regex(".*login"));
            
            // Senior Tip: Check for the success snackbar/toast message
            var successMessage = Page.GetByText("Registration completed successfully.");
            await Expect(successMessage).ToBeVisibleAsync();
        }
    }
}