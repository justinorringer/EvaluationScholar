import React, { useEffect, useState } from "react";

function Query() {
    const [getMessage, setGetMessage] = useState({})
    let state = {
        value: "",
    }
    
    //Method to link to a button
    function test(){
        //Test info
        console.log("hi")
        //Connect to the API
        makeAPICall();
        //setGetMessage(api_ret);
        console.log(getMessage);
        state.value = getMessage.data;
        document.getElementById("test").innerHTML = state.value;
    } 
    
    //Example function to gather from Flask
    const makeAPICall = async () => {
      try {
        const response = await fetch('http://localhost:5000/', {mode:'cors'});
        const data = await response.json();
        console.log({response, data})
        //return {response, data}
        setGetMessage({response, data})
        console.log(getMessage.response.status)
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
          <div className="justify-content-center page-header">Search Author</div>
          <div className="form-group">
              <input type="author" className="form-control" placeholder="G. Rothermel" />
          </div>
          <div className="row">
              <div className="col-10 gx-4 gy-4">
                  <div className="form-group">
                      <br />
                      <select multiple className="form-control" id="exampleFormControlSelect1">
                        <option>G. Rothermel</option>
                        <option>P. Davis</option>
                        <option>B. Baggins</option>
                        <option>S. Smith</option>
                      </select>
                  </div>
              </div>
              <div className="col-2 gy-4 gx-4 justify-content-right">
                  <br />
                  <button type="button" className="btn btn-danger">Query</button>
              </div>
          </div>
      </div>
      <hr />

      <div className="container">
          <table className="table table-borderless table-striped">
              <thead className="thead-dark">
                  <tr>
                      <th scope="col-6">Article</th>
                      <th scope="col-2">Year</th>
                      <th scope="col-4">Authors</th>
                      <th scope="col-2">Citations</th>
                  </tr>
              </thead>
              <tbody>
                  <tr>
                      <th scope="row">Lorem ipsum, dolor sit amet consectetur adipisicing elit.
                      </th>
                      <td>801</td>
                      <td>P. Picasso</td>
                      <td>100</td>
                  </tr>
              </tbody>
          </table>
      </div>
      <div className="container">
          
          <div className="col-lg-3">
              <button className="btn btn-primary" onClick={test}>Search</button>
              <p id="test">{state.value}</p>
          </div>
        </div>
    </div>
  );
}

export default Query;