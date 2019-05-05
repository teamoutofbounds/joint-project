Feature: User authentication by role
  In order to start working with the application
  As a user
  I want to login into my landing page

  Background: There is a registered user
    Given Exists a user "user" with password "password"

  Scenario: Enter into the application as a Gestor
    Given Exists a role "Gestor"
    And I'm a user "user" with role is "Gestor"
    When I login as user "user" with password "password"
    Then As a user "user" I'm viewing the Gestor landing page