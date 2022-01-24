**Sponsor Background**
Dr. Rothermel is the Head of the Computer Science Department at NC State. In this position, he is called on to assess the performance of faculty members, and to compare the performance of our faculty with those at other institutions.

**Background and Problem Statement**
In any organization, management looks for ways to assess the performance of employees and to measure that performance against the performance of competitors. Assessing performance, however, is complicated and there are many different metrics that can be used.  In general, any particular metric one might choose has both advantages and drawbacks. Thus, it’s better to have multiple metrics.

In academia, one class of employees whose performance must be assessed is tenured and tenure-track faculty (hereafter, “TT faculty”.) TT faculty are typically expected to engage in several types of activities: these include teaching, research, and service (e.g., service to their profession or to their department).  Performance in each of these areas needs to be assessed. Where this project is concerned, however, we are interested solely in research performance.

Standard metrics used to assess a TT faculty member’s research performance include 1) numbers of peer reviewed scientific papers published, 2) numbers of grants received, 3) total expenditures of grant money on research activities, and 4) numbers of students mentored and graduated, among others. To see an example of “1” in action, go to “csrankings.org”, turn the toggle next to “All Areas” to “off”, and down below under “Systems”, check the box next to “Software Engineering”. You’ll see that NC State is ranked second in the USA for research in this area based solely on the numbers of publications (in a small set of top conferences) of its faculty members.

All of the foregoing metrics provide value, but they do not adequately capture one of the key attributes that motivates research in the first place: research is expected to have an impact – to result in some meaningful contribution to the world, such as addressing a problem found in that world. Faculty members can write papers all they want, but arguably, until their work results in something (directly or indirectly) tangible, it hasn’t had impact.

How do we measure the impact of research? One way is to assess the actual products of research (i.e. research that translates into practical processes or tools).  This is helpful, but it doesn’t account for the fact that when research leads to practical results, it is often over a long time period in which early results are adopted by other researchers to produce intermediate results (possibly with many iterations), which ultimately are adopted by other researchers into something directly applicable to addressing some problem in the world.

An alternative metric that can help account for the impact of research can be found by considering the ways in which a piece of published research is cited in subsequent papers by other researchers. The degree to which a published work is cited helps track the degree to which other researchers found that work to be meaningful in the context of their own work, and as such, indicates a form of “impact”. Ultimately, chains of citations connect initial conceptual research contributions to the real-world applications that the initial contributions made possible. While also not a perfect measurement in and of itself, citation data is already widely collected and used and accepted as a useful measure of impact. For an example, go to google and type “Google Scholar Gregg Rothermel” and you can see citation information presented in a few ways.  One citation-based metric is the “h-index”, and often you’ll find faculty noting their h-index in their resumes.

As a Department Head, I can easily compare and assess faculty in terms of their numbers of publications, their grants received, their students mentored.  But these metrics don’t capture impact. Comparing faculty in terms of citations could help with that, but doing so is more difficult.

The goal of this work is to provide Department Heads with a tool that can be used to compare and assess the impacts of faculty research (both within their own department and across departments) in terms of citations that research has received.

**Project Description**
I have been able to assess citations using a manual process, but it takes too much time for me to apply this process broadly. The process uses data provided by Google Scholar. Initially I attempted to just scrape Google scholar pages (via cut/paste) obtain information on publications and their citations and place the resulting data into a spreadsheet.  With extensive manipulation I could turn this into data that lists paper names, years of publication, and numbers of citations. Doing this for multiple TT faculty I could obtain data that can be compared, and I could then use tools for displaying data sets (e.g., boxplots that provide a view of the distributions of citation numbers per faculty member).

This turned out to be much more difficult than the foregoing paragraph makes evident.  For one thing, there can be a lot of “noise” in Google Scholar pages. For some faculty, lists of papers associated with them in Google Scholar include numerous papers that those faculty are not even co-authors of!  These had to be weeded out. Also, some papers listed in Google Scholar have not been refereed, have appeared only as preprints, or have appeared only in minor venues that should not be considered.

One potential solution to this problem was to take as input, for a given TT faculty member, a list of their refereed publications, such as is typically present in their CVs (Curriculum Vitae – the academic equivalent of resumes).  This is what I ended up doing in my manual process. Given a CV and a list of publications, I search for those publications in Google Scholar and record the information on their dates and citations, and I place the relevant information into a spreadsheet. Then I repeat this for each faculty member being considered. Depending on what I want to visualize of the data, I arrange the data in the spreadsheet such that it allows me to obtain specific visualizations.  For example, to obtain a figure providing boxplots presenting the distribution of citations for each TT faculty member among a group of faculty members, I create a spreadsheet in which each column lists a given faculty members’ citations, and use Excel’s boxplot tool on this spreadsheet.

This project needs to provide an automated method for doing the foregoing, but a method that “mimics” my manual process is not required – rather, a method that achieves the same results as that process is what we’re seeking.

The best way to describe what the proposed system needs to achieve is to first list a number of “queries” that I would like a system to be able to handle.  Examples are:

- Compare the citations for a given set of faculty members over their entire careers.
- Compare the citations for a given set of faculty members over the past 10 years.
- Compare the citations for a given set of faculty members over the period 2005-2015.
- Compare the citations for the 20 most highly cited papers for each faculty member in a given set of faculty members over (some period).
- Compare the trajectories in citations (i.e., the changes in citation numbers over time) for a given set of faculty members over (some period). A trajectory could consist of numbers per year, or rolling averages.

We could find a way to characterize the set of queries to be supported more generally, using parameters.

A second component of the description involves the interpretation of the word “compare”. To date my primary “comparison” method is to obtain boxplots that let me visualize the data. So “compare” translates to “provide a figure containing a boxplot that shows the citations….”.  Other results may be useful, however. For example, a “comparison of trajectories” suggests the use of line graphs that trace changes in numbers over time.  Another useful method would be to calculate h-indexes over the given sets of publications being considered.  We could explore other options, but to scope this project I suspect that identifying a small finite set would be appropriate.

Obviously, obtaining data and storing it in a manner that supports the types of queries required is a bit part of the project. Presumably the data would be stored in a database where it could be used to provide results for the queries. This could be performed by some front-end tool. Then a back-end tool would enable queries and visualizations.

As a Department Head, I would find a tool that facilitated the following comparisons useful in several ways. Here are some examples:

- To assess the relative impacts of the research of Full Professors within the CSC department at NC State, for use in annual evaluations.
- To assess the trajectories of the impacts of the research of Associate Professors seeking promotion to Full Professor in the CSC department.
- To assess the relative impacts of the research (or trajectories of those impacts) of a set of prospective faculty members who are applying for faculty positions with the CSC department.
- To assess the performance of CSC faculty in terms of impact, relative to the performance of other CSC departments that are thought of as comparable, or that are examples of what we “aspire” to as a department.

**Technologies and Other Constraints**
I do not have any suggestions for specific technologies to be used; I leave this up to the project team.

I do ask for a solution that can be utilized on common desktop PCs or laptops, without using any proprietary software that must be purchased.  Minimally, a first version should function on a recent version of an iMac or MacBook.

I don’t require students to sign over IP for this, but I do expect that the Department of Computer Science at NC State is given the rights to use the system free of charge.