Minutes:
- Meeting started with Abhinav introducing the agenda.
- Justin asked Dr. Rothermel about i10-index, h-index, and self-citations. Self-citations are not a problem to Dr. Rothermel (it can sometimes show a work’s relevance), but i10-index and h-index will create useful queries.
- Abhinav clarified Dr. Rothermel’s query case by the year.
- Tyler and Gage went through our API Endpoints, asking about if all the routes cover the query cases.
- Dr. Rothermel brought up adding a faculty’s position or field to our database for queries.
- Possible tags include: rank, area, a temporary “candidates” tag etc.
- The set could be filtered out in the front-end by whatever query type through the same API endpoints.
- He wants the option to tag based on a list of authors whose position data is null.
- Filtering by multiple tags is desired, too.
- Gage showed Dr. Rothermel a test coverage report, where our current code has 93% line coverage.
- Carter asks to go over his desired visualizations. There are three basic outputs.
- Box-plot is obvious, showing professor to citation in a mostly visual way.
  - Carter brings up the case of having a box for each professor over years.
  - Box plot could also show in year x, a number of cites of a professors papers over time, i.e. showing the impact of a professors work on that year.
    - This information would not immediately be available, and would needto be gathered over time.
  - Another option would be for a professor in a year, the number of citations of papers published in each year, i.e. the more impact of a paper in a given year.
  - Gage shows that google scholar uses the citations made of a faculty member’s work in a year, but the meaning is particularly vague.
  - Outlier removal, in extreme cases, should be considered.
  - Line or bar graph with time (years) to faculty member. This has a couple interpretations, so more research is needed. Line plot for articles’ citations over time.
  - Carter asks about the usefulness of non-cited articles.
  - Spreadsheet output is the most basic return. There seem to be 2 useful variants so far:
     - A column corresponds to a professor, and for that the citations per article per person should be an option. This may include a paper title column.
     - A raw data csv file would be useful for managing the data in excel or reporting to interested parties.

|Action Item | Person Responsible | Due Date |
|------------|--------------------|---------|
| Identify what the Google Scholar graph considers | Gage/Tyler/Abhinav | Monday (2/14) |
| Update on scraping | Carter/Justin | Monday (2/14) |