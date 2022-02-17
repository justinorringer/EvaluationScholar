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
      <div class="container">
        <div class="row align-items-center my-5">
          <div class="col-lg-5">
            <h1 class="font-weight-light">Write a Query</h1>
            <p>
              Lorem Ipsum is simply dummy text of the printing and typesetting
              industry. Lorem Ipsum has been the industry's standard dummy text
              ever since the 1500s, when an unknown printer took a galley of
              type and scrambled it to make a type specimen book.
            </p>
          </div>
          <div class="col-lg-3">
              <table>
                  <tr>
                      <td>Test</td>
                      <td>----</td>
                      <td>
                          <input type="text" placeholder="test"></input>
                      </td>
                  </tr> 
              </table>
          </div>
          <div class="col-lg-3">
              <button class="btn btn-primary" onClick={test}>Search</button>
              <p id="test">{state.value}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Query;