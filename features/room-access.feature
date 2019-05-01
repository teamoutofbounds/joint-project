#now this is just copied and need to be modified

Feature: Access Room
  In order to be able to access the data of a room
  As an user
  I want to make sure everything is loaded correctly and without mistakes

  Scenario: I access a room where everything is correct
    Given Exists a user "username" with password "password"
    And Exists a room named "room_name"
      | temp    | hum      | quantity   | limit    | room_status  |
      | 10      | 30       | 10         | 50       | 0            |
    And There is a container "container" assigned to that room
      | product_id | producer_id | limit | temp_min | temp_max  | hum_min  | hum_max | room      |
      | 1          | 2           | 50    | 5        | 50        | 10       | 40      | room_name |
    When I access to the data of room "room_name"
    Then All the data of room "room_name" is correct for container "container"

  Scenario: I access a room where there is a container that doesnt¡'t fit the room
    Given Exists a user "username" with password "password"
    And Exists a room named "room_name"
      | name     | temp    | hum      | quantity   | limit    | room_status  |
      | sala2    | 10      | 30       | 10         | 50       | 0            |
    And There is a container "container" assigned to that room
      | product_id | producer_id | limit | temp_min | temp_max  | hum_min  | hum_max | room      |
      | 1          | 2           | 50    | 5        | 50        | 10       | 40      | room_name |
    When I access to the data of room "room_name"
    Then All the data of room "room_name" is NOT correct for container "container"

  Scenario: I try to access a room when I'm not logged in
    Given I am not logged in
    When I access to the data of room "room_name"
    Then I'm redirected to the login form