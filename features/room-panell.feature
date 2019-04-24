#now this is just copied and need to be modified

Feature: View Restaurant
  In order to know about a restaurant
  As a user
  I want to view the restaurant details including all its dishes and reviews

  Background: There is one restaurant with 2 dishes and another without
    Given Exists a user "user1" with password "password"
    And Exists a user "user2" with password "password"
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