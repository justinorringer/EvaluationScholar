import React, { useEffect, useState } from "react";

function Input() {
  const [getMessage, setGetMessage] = useState({})
  
  //Base file reading works!
  
  let fileInput = null;
  let lines = "";

  let data = {
    name: "",
    institution: ""
  }

  function getFile(){
    //console.log(document.getElementById("authName").value);

    let test = document.getElementById('myfile')
    fileInput = test.files[0];
    //console.log(fileInput)

    var fr = new FileReader();

    fr.addEventListener("load", () => {
      
      console.log(fr.result);
      fileInput = fr.result;
      let testing = "";
      //Branch to handle different operating system line endings (Windows v. Linux)
      if(fileInput.includes("\r")){
        testing = fileInput.split("\r\n");
        console.log(testing);
      } else {
        testing = fileInput.split("\n");
        console.log(testing);
      }
      lines = testing;

      document.getElementById("text").innerHTML = fileInput;

      makeAPICall();
    }, false);

    //This call activates the listener, and helps it to parse the file.
    fr.readAsText(fileInput);
  }

  //Example function to gather from Flask
  const makeAPICall = async () => {
    try {

      const response = await fetch('http://localhost:5000/api/authors', {
        method: "POST",
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Content-Type': 'application/json',

        },
      
        //make sure to serialize your JSON body
        body: JSON.stringify({
          name: document.getElementById("authName").value,
          institution: ""
        }), mode: 'cors'
      }, true);      
      
      console.log(response);
      
      const data = await response.json();
      //console.log({response, data})
      //return {response, data}
      setGetMessage({response, data})
      //console.log(getMessage.response.status)
    }
    catch (e) {
      console.log(e)
    }
  }
  useEffect(() => {
    makeAPICall();
  }, [])

  return (
    <div className="body">
      <div className="container pt-5">
        <div className="row">
            <div className="alert alert-success alert-dismissible" role="alert">
                <button className="close" type="button" data-dismiss="alert"><span>&times;</span></button> Articles scraped successfully
            </div>
        </div>
        <div className="row">
          <label>Author name: &nbsp;</label>
          <input type="text" id="authName"></input> 
        </div>
        <div className="row">
            <div className="justify-content-center page-header">Upload File <small>as a .CSV or .TXT file</small></div>
            <br/><br/>
        </div>
        <div className="row">
                <label for="myfile">Select a file:&nbsp;</label>
                <input type="file" id="myfile" name="myfile"/>
                <input type="submit" onClick={getFile}/>
        </div>
        <div className="row">
          <p id="text">{lines}</p>
        </div>
    </div>
    </div>
    
  );
}

export default Input;