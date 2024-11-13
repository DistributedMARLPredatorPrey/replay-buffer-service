Feature: Replay Buffer
    Reinforcement Learning Replay Buffer Service.

    Scenario: Successful store of a data record
        Given The Replay Buffer is up and running
        When I prepare an valid data record
        And I request this data to be recorded
        Then I should receive a 200 as response status
        And the message should indicate successful operation

    Scenario: Unsuccessful store of a data record
        Given The Replay Buffer is up and running
        When I prepare an invalid data record
        And I request this data to be recorded
        Then I should receive a 200 as response status
        And the message should indicate unsuccessful operation


#   Scenario: Batching empty data
#        Given The Replay Buffer is up and running
#
#        When I request to receive a data batch of N rows
#        And data previously stored has fewer than N rows
#
#        Then I should receive a 200 as response status
#        And the received data batch should be empty
#
#   Scenario: Batching nonempty data
#        Given The Replay Buffer is up and running
#
#       When I request to receive a data batch of N rows
#        And data previously stored has N or more rows
#
#        Then I should receive a 200 as response status
#        And the received data batch should be nonempty
#        And the received data batch should have N rows
