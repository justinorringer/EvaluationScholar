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
    <div className="query">

      <div class="bg-color"></div>
      <div class="container">
          <div class="justify-content-center page-header">Search Author</div>
          <div class="form-group">
              <input type="author" class="form-control" placeholder="G. Rothermel" />
          </div>
          <div class="row">
              <div class="col-10 gx-4 gy-4">
                  <div class="form-group">
                      <br />
                      <select multiple class="form-control" id="exampleFormControlSelect1">
                        <option>G. Rothermel</option>
                        <option>P. Davis</option>
                        <option>B. Baggins</option>
                        <option>S. Smith</option>
                      </select>
                  </div>
              </div>
              <div class="col-2 gy-4 gx-4 justify-content-right">
                  <br />
                  <button type="button" class="btn btn-danger">Query</button>
              </div>
          </div>
      </div>
      <hr />

      <div class="container">
          <table class="table table-borderless table-striped">
              <thead class="thead-dark">
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
      <div class="container">
          
          <div class="col-lg-3">
              <button class="btn btn-primary" onClick={test}>Search</button>
              <p id="test">{state.value}</p>
          </div>
        </div>
    </div>
  );
}

export default Query;