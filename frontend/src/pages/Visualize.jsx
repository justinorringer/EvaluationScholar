import React, { useState } from 'react';
import axios from 'axios';
import Chart from "react-apexcharts";
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch from '@mui/material/Switch';

//Function to create an HTML representation for the Input page of the app.
//Authors: Gage Fringer, Carter Thunes, Justin Orringer
function Visualize() {

  const [aggAuthors, setAggAuthors] = useState(true);

  const [options, setOptions] = useState({
    series: [
    {
      name: 'box',
      type: 'boxPlot',
      data: [
        {
          x: 1,
          y: [54, 66, 69, 75, 88]
        },
        {
          x: 2,
          y: [43, 65, 69, 76, 81]
        },
        {
          x: 3,
          y: [31, 39, 45, 51, 59]
        },
        {
          x: 4,
          y: [39, 46, 55, 65, 71]
        },
        {
          x: 5,
          y: [0, 3, 13, 16, 21]
        }
      ]
    },
    {
      name: 'outliers',
      type: 'scatter',
      data: [
        {
          x: 1,
          y: 31
        },
        {
          x: 2,
          y: 25
        },
        {
          x: 3,
          y: 64
        },
        {
          x: 4,
          y: 27
        },
        {
          x: 4,
          y: 141
        }
      ]
    }
  ],
  chart: {
    type: 'boxPlot',
    height: 350
  },
  colors: ['#008FFB', '#FEB019'],
  title: {
    text: 'BoxPlot - Scatter Chart',
    align: 'left'
  },
  xaxis: {
    type: 'category',
    categories: ["Rothermel", "Heil", "Williams", "Singh", "Ore"],
    tickPlacement: 'on'
  },
  tooltip: {
    shared: false,
    intersect: true
  }
  });

  //For some reason the 'getElementById' worked if I copied the query.jsx code to this page, but it doesn't for
  //This code. Not sure why.
  // const testing = async () => {
    
  //   try {
  //     const response = await axios.get('/api/authors', {mode:'cors'});
  //     console.log(response.data);
  //     if (response.status === 200)
  //         authors = response.data;
  //     console.log({response, authors})
  //     }
  //     catch (e) {
  //         console.log(e.getMessage);
  //   }
      
  // }

  //testing();

  const handleChange = (event) => {
    setAggAuthors(event.target.checked);
    console.log(event);
  };

  //Return the related HTML of the page.
  return (
    <div className="body">
      <FormGroup>
        <FormControlLabel control={<Switch defaultChecked checked={aggAuthors} onChange={handleChange} inputProps={{ 'aria-label': 'controlled' }}/>} label="Aggregate Authors" />
      </FormGroup>
      {
        aggAuthors && <p>Yuh</p>
      }
      <div id="chart-area" className="container pt-5">
        <Chart
          options={options}
          series={options.series}
          type="boxPlot"
        />
      </div>
      <p id="testvaluehere"></p>
    </div>
    
  );
}

export default Visualize;