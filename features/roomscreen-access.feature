#now this is just copied and need to be modified

Feature: Access rooms screen
  In order to know which rooms are available
  As a user
  I want to see the list of all the rooms

  Scenario: There is only one room
    Given Exists a user "username" with password "password"
    And There is at least one room
    When I access the rooms screen
    Then There is "Sala 1" link available

  Scenario: There are no rooms yet
    Given Exists a user "username" with password "password"
    And There are no rooms
    When I access the rooms screen
    Then Server responds with page containing "No hi ha sales"
    Then There is no "Sala 1" link available

  Scenario: I try to access the room screen but I am not logged in
    Given I am not logged in
    When I access the rooms screen
    Then I'm redirected to the login form