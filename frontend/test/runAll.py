import testCreateAuthor
import testAuthor
import testTasks
import testTags

testCreateAuthor.run_tests()

testAuthor.sanity_check()

testTasks.runAll()

testTags.runAll()