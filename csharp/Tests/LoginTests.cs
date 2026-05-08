using Microsoft.Playwright;
using NUnit.Framework;
using JuiceShopAutomation.Pages;
using System.Threading.Tasks;
using System.Text.RegularExpressions;

namespace JuiceShopAutomation.Tests
{
    [TestFixture]
    public class LoginTests : BaseTest
    {
        private LoginPage _loginPage;

        [SetUp]
        public void TestSetup()
        {
            // Initialize the LoginPage by passing the 'Page' object 
            // that BaseTest (via PageTest) provides automatically.
            _loginPage = new LoginPage(Page);
        }

        [Test]
        [Description("Verify that a registered user can access the system.")]
        public async Task ShouldLoginSuccessfully()
        {
            // Arrange
            await _loginPage.NavigateToAsync("login");

            // Act
            await _loginPage.LoginAsync("admin@juice-sh.op", "admin123");

            // Assert
            // 'Expect' is globally available thanks to PageTest inheritance.
            await Expect(Page).ToHaveURLAsync(new Regex(".*search"));
        }
    }
}