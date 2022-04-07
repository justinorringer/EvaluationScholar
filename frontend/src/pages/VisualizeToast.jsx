import React, { useState } from 'react';
import axios from 'axios';
//import Chart from "react-apexcharts";
import Chart from '@toast-ui/chart';
//import BoxPlotChart from '@toast-ui/chart/boxPlot';
import { BoxPlotChart } from '@toast-ui/react-chart';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch from '@mui/material/Switch';

//Function to create an HTML representation for the visualization page of the app.
//Authors: Gage Fringer, Carter Thunes, Justin Orringer
function VisualizeToast() {

	const [aggAuthors, setAggAuthors] = useState(true);

	const [data, setData] = useState({
		categories: ['Rothermel', 'Williams', 'Singh', 'Ore'],
			series: [
			{
				name: '2020',
				data: [
				[10, 25, 37, 55, 70],
				[10, 27, 45, 52, 80],
				[30, 40, 47, 60, 70],
				[10, 22, 31, 47, 60],
				],
				outliers: [
				[0, 140],
				[0, 100],
				[2, 96],
				],
			}
			],
		});

	const [options, setOptions] = useState({
		chart: { title: 'Monthly Revenue', width: 900, height: 500 },
		series: {
	  		selectable: false,
		}
	})

	const containerStyle = {
		width: '600px',
		height: '600px',
	  };

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
			<BoxPlotChart
				data={data}
				options={options}
				style={containerStyle}
			/>
		</div>
		<p id="testvaluehere"></p>
		</div>
		
	);
}

export default VisualizeToast;