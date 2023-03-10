@daily
Feature: Login

  Background:
    When I go to <global_host>/users/sign_in page

  @PCO-1058 @platform:web @browser:chrome @headless
  Scenario: Login - Login successful
    When I login with correct <user_name> and <password>
    Then I should login successful
