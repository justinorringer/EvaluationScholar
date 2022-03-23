// Each author has an Author page with their tags and articles listed.
function Author() {
    
    // HTML by Justin Orringer
    return (
      <div className="body">
        <div className="container pt-5">
            <div className="row" id="authorSidebar">
                <div className="col-3" id="authorSidebar">
                    <div className="row">
                        <img className="border" id="profile" src="frontend\src\generic.png" alt="" />
                    </div>
                    <div className="row pt-4" id="tagHeader">
                        <h4>Tags</h4>
                    </div>
                    <div className="row pt-2" id="Tags">
                        <div className="container">
                            <ul>
                                <li>Tag 1</li>
                                <li>Tag 2</li>
                                <li>Tag 3</li>
                            </ul>
                        </div>
                    </div>

                    <div className="row pt-2">
                        <form action="/action_page.php">
                            <h4 for="myfile">Upload Articles</h4>
                            <input type="file" id="myfile" name="myfile" />
                            <input type="submit" />
                        </form>
                    </div>
                </div>
                <div className="col-9" id="mainColumn">
                    <div className="row pt-5">
                        <h3 className="px-0">Author Name</h3>
                    </div>
                    <div className="row pt-2" id="articles">
                        <table className="table table-borderless table-striped">
                            <thead className="thead-dark">
                                <tr>
                                    <th scope="col-6">Article</th>
                                    <th scope="col-2">Year</th>
                                    <th scope="col-2">Citations</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <th scope="row">Lorem ipsum, dolor sit amet consectetur adipisicing elit.
                                    </th>
                                    <td>801</td>
                                    <td>100</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
      </div>
      
    );
  }
  
  export default Author;