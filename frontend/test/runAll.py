import testCreateAuthor
import testAuthor
import testTasks

testCreateAuthor.run_tests()

testAuthor.sanity_check()

testTasks.runAll()