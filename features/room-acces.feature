#now this is just copied and need to be modified

Feature: Acces Room
  In order to be able to acces the data of a room
  As an user
  I want to make sure everything is loaded correctly and without mistakes

  Background: There is a not full room with a product
    Given Exists a user "username" with password "password"
    And There is a product assigned to a room
    And The room is not full
    And Exists restaurant registered by "user1"
      | name            | city          | country       |
      | Famous          | London        | England       |
      | Unknown         | Paris         | France        |
    And Exists dish at restaurant "Famous" by "user1"
      | name            |
      | Fish and Chips  |
    And Exists dish at restaurant "Unknown" by "user2"
      | name            |
      | Apple Pie       |
    And Exists review at restaurant "Famous" by "user1"
      | rating          | comment       |
      | 4               | Quite good    |
    And Exists review at restaurant "Famous" by "user2"
      | rating          |
      | 2               |
