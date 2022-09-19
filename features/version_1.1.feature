Feature: version 1.1 of vote modeling

	Scenario: Generated some work
		Given I create 10 works with ./test_configs.yml
		Then I see 10 elements in works
