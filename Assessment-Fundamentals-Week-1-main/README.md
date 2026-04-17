# Shopping Basket

In this exercise, you will be creating a shopping basket application. The application will allow a user to add items to a shopping basket and calculate the total cost of the basket including any applicable discounts.

## Assessment Criteria

You will be assessed on three different metrics

1. The number of passing tests when run with `pytest` (90% of your score)
2. Your `pylint` code quality score (10% of your score)
3. Discretionary marks from coaches (can be any amount between -20% and +20%)

## Tips

- You **are** allowed to use the internet to help you with this assessment.
- You can format any number to two decimal places using the `:.2f` format specifier. For example, `f"{total:.2f}"` will format the `total` variable to two decimal places.
- When you have a failing test, it can be easier to view them individually by running `pytest test_[level]_task.py::test_name` where `test_name` is the name of the test you want to run.
  - Alternatively use `-k` to run tests that match a specific keyword. For example, `pytest -k test_name` will run all tests that contain `test_name` in their name.
- To view the entire output of the test rather than a truncated version, you can use the `-vv` flag. For example, `pytest -vv test_[level]_task.py` will show the full output of the tests.

## Setup

Please ensure you do every step below carefully. Not doing so will mean we can't assess your work and **will result in a score of zero**.

1. Create a repo named exactly `Assessment-Fundamentals-Week-1`
2. Invite your coaches to it (they'll let you know they Github usernames)
3. Push all the code in this folder to your created repository
4. On your created repo, click on `Actions` in the top menu bar
   - If it's there, click on `I understand my workflows, go ahead and enable them`
5. Complete the assessment
6. Commit & push your code regularly

## Files Explained

In each of the `Level` folders you will find the code and instructions for that level. **Each level will build on the one before it**, be sure to read the instructions carefully.

- `task_[level].py` - All of your code should be written in this file.
- `test_[level]_task.py` - This file contains some basic tasks for this level.
- `README.md` - This file contains the instructions for the level.
