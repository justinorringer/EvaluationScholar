import React from "react";

function Input() {
  return (
    <div className="body">
      <div className="container pt-5">
        <div className="row">
            <div className="alert alert-success alert-dismissible" role="alert">
                <button className="close" type="button" data-dismiss="alert"><span>&times;</span></button> Articles scraped successfully
            </div>
        </div>
        <div className="row">
            <div className="justify-content-center page-header">Upload File <small>as a .CSV or .TXT file</small></div>
            <br/><br/>
        </div>
        <div className="row">
            <form action="/action_page.php">
                <label for="myfile">Select a file:&nbsp;</label>
                <input type="file" id="myfile" name="myfile" />
                <input type="submit" />
            </form>
        </div>
    </div>
    </div>
    
  );
}

export default Input;