- Client lists three requirements steps: retrieving data, storing it in a queryable format, and displaying it in graphs
- Client says he might be able to provide CVs in BibTex form, either a subset of staff or possibly universally mandated later on
- May want to be able to extract data to an Excel file as a temporary proof-of-concept
- Client willing to pay for APIs depending on price and terms
- More general is fine, just has to run on Mac
- Sample architecture: paper database → citation updates → data presentation
- First iteration should probably be about storing paper data
- Client can provide sample CVs on request
- DBLP digital library may be useful
- Lots of edge cases, finding data may need manual intervention (duplicate papers on CV, incorrect title on CV, etc.)
- Class-time is good for meetings (Wednesday, 9:35 AM, EB2 3265)
- No specific guidelines for documentation from client
- Should focus research on high-risk parts of the project early, like finding citation data

Possible Technologies:
- React is recommended over Angular for frontend application
- SimpleAPI/FastAPI/Flask for backend application API
- Should use a relational database, any DBMS works
- SQLAlchemy for database abstraction?

To-do:
- Provide calendar invitation for meetings