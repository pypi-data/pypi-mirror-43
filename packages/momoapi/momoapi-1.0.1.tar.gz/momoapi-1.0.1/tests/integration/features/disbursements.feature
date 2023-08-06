Feature: Disbursements
    Scenario: Transfer Money to another account
        Given I have a valid user_id, auth_secret, and disbursements subscription key
        When I transfer with the following payment details
            | note         | amount | message | mobile     | product_id |
            | test payment | 600    | message | 0782631873 | 0001       |

        And  I check for transaction Status
        Then It should be successful