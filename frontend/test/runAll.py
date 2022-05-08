import testCreateAuthor
import testAuthor
import testTasks
import testTags
import testIssues
import testPapers
import testVisualize

"""
This file is used to run all of the Selenium tests on the system, and does so
by calling the necessary methods in each specific test file.

Author: Gage Fringer
"""

full_rate = [0, 0]

creating = testCreateAuthor.run_tests()
full_rate[0] += creating[0]
full_rate[1] += creating[1]

author = testAuthor.sanity_check()
full_rate[0] += author[0]
full_rate[1] += author[1]

tasks = testTasks.runAll()
full_rate[0] += tasks[0]
full_rate[1] += tasks[1]

tags = testTags.runAll()
full_rate[0] += tags[0]
full_rate[1] += tags[1]

issues = testIssues.runAll()
full_rate[0] += issues[0]
full_rate[1] += issues[1]

papers = testPapers.runAll()
full_rate[0] += papers[0]
full_rate[1] += papers[1]

viz = testVisualize.runAll()
full_rate[0] += viz[0]
full_rate[1] += viz[1]

print("\n" + "-" * 10 + "Full Coverage Report" + "-" * 10 + "\n")
print("Passing: " + str(full_rate[0]) +"/"+ str(full_rate[0]+full_rate[1]))
print("Failing: " + str(full_rate[1]) +"/"+str(full_rate[0]+full_rate[1]))
print("% pass: " + str((full_rate[0] / (full_rate[0]+full_rate[1])) * 100) + "%")