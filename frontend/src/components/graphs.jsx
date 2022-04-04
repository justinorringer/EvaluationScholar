import React from "react";

import axios from 'axios';
//import Chart from "react-apexcharts";
//import ApexCharts from "apexcharts";
import Chart from '@toast-ui/chart';
import {BoxPlotChart} from '@toast-ui/chart'

//Function to create an HTML representation for the Input page of the app.
//Authors: Gage Fringer, Carter Thunes, Justin Orringer
function Graphs() {

 //Variable to hold list of current authors in the system
 let authors = [];
 //Variable to hold list of papers related to an author
 let papers = [];


  //For some reason the 'getElementById' worked if I copied the query.jsx code to this page, but it doesn't for
  //This code. Not sure why.
  const testing = async () => {
    
    try {
      const response = await axios.get('/api/authors', {mode:'cors'});
      console.log(response.data);
      if (response.status === 200)
          authors = response.data;
      console.log({response, authors})
      }
      catch (e) {
          console.log(e.getMessage);
    }

    const el = document.getElementById("chart-area");
    console.log(el);

      console.log(document.getElementById("testvaluehere"));
      const data = {
        categories: ['Budget', 'Income', 'Expenses', 'Debt'],
        series: [
          {
            name: '2020',
            data: [
              [1000, 2500, 3714, 5500, 7000],
              [1000, 2750, 4571, 5250, 8000],
              [3000, 4000, 4714, 6000, 7000],
              [1000, 2250, 3142, 4750, 6000],
            ],
            outliers: [
              [0, 14000],
              [2, 10000],
              [3, 9600],
            ],
          },
          {
            name: '2021',
            data: [
              [2000, 4500, 6714, 11500, 13000],
              [3000, 5750, 7571, 8250, 9000],
              [5000, 8000, 8714, 9000, 10000],
              [7000, 9250, 10142, 11750, 12000],
            ],
            outliers: [[1, 14000]],
          },
        ],
      };
      const options = {
        chart: { title: 'Monthly Revenue', width: 900, height: 500 },
      };

      try{   const chart = new BoxPlotChart({ el, data, options } );
      } catch (e){
        console.log(e);
      }
  }

  testing();
  //console.log(document.getElementById("testvaluehere"));
  /*const data = {
    categories: ['Budget', 'Income', 'Expenses', 'Debt'],
    series: [
      {
        name: '2020',
        data: [
          [1000, 2500, 3714, 5500, 7000],
          [1000, 2750, 4571, 5250, 8000],
          [3000, 4000, 4714, 6000, 7000],
          [1000, 2250, 3142, 4750, 6000],
        ],
        outliers: [
          [0, 14000],
          [2, 10000],
          [3, 9600],
        ],
      },
      {
        name: '2021',
        data: [
          [2000, 4500, 6714, 11500, 13000],
          [3000, 5750, 7571, 8250, 9000],
          [5000, 8000, 8714, 9000, 10000],
          [7000, 9250, 10142, 11750, 12000],
        ],
        outliers: [[1, 14000]],
      },
    ],
  };
  const options = {
    chart: { title: 'Monthly Revenue', width: 900, height: 500 },
  };

  /*  try{   const chart = new BoxPlotChart({ el, data, options } );
  } catch (e){
    console.log(e);
  }*/
  //Return the related HTML of the page.
  return (
    <div className="body">
        <div id="chart-area" className="container pt-5"></div>
        <p id="testvaluehere"></p>
    </div>
  );
}

export default Graphs;