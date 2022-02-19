import React from "react";

function Input() {
  return (
    <div className="input">
      <div class="bg-color"></div>
      <div class="container">
        <div class="row">
            <div class="alert alert-success alert-dismissible" role="alert">
                <button class="close" type="button" data-dismiss="alert"><span>&times;</span></button> Articles scraped successfully
            </div>
        </div>
        <div class="row">
            <div class="justify-content-center page-header">Upload File <small>as a .CSV or .TXT file</small></div>
            <br/><br/>
        </div>
        <div class="row">
            <form action="/action_page.php">
                <label for="myfile">Select a file:</label>
                <input type="file" id="myfile" name="myfile" />
                <input type="submit" />
            </form>
        </div>
    </div>
    </div>
    
  );
}

export default Input;