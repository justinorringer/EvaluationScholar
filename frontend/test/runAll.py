import testCreateAuthor
import testAuthor
import testTasks
import testTags

"""
This file is used to run all of the Selenium tests on the system, and does so
by calling the necessary methods in each specific test file.

Author: Gage Fringer
"""

testCreateAuthor.run_tests()

testAuthor.sanity_check()

testTasks.runAll()

testTags.runAll()