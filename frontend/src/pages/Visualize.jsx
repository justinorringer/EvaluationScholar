import React, { useState } from 'react';
import axios from 'axios';
//import Chart from "react-apexcharts";
import {BoxPlotChart} from '@toast-ui/chart';
//import BoxPlotChart from '@toast-ui/chart/boxPlot';
//import { BoxPlotChart } from '@toast-ui/react-chart';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch from '@mui/material/Switch';

function Visualize() {

    const [aggAuthors, setAggAuthors] = useState(true);
    
/*
Apex charts code (use for Toast when using react charts instead)

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
                        y: 32
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
                        y: 78
                    },
                    {
                        x: 5,
                        y: 15
                    }
                    ]
                }],
            chart: {
                type: 'boxPlot',
                height: 350
            },
            colors: ['#CC2424', '#666666'],
            title: {
                text: 'BoxPlot',
                align: 'center'
            },
            xaxis: {
                type: 'category',
                categories: ["Rothermel", "Heil", "Williams", "Singh", "Ore"],
                tickPlacement: "between"
            },
            tooltip: {
                shared: false,
                intersect: true
            }
        });

*/

    const testing = async () => {
    
        try {
            const response = await axios.get('/api/authors', {mode:'cors'});
            console.log(response.data)
        }
        catch (e) {
            console.log(e.getMessage);
        }

        const el = document.getElementById("chart-area");
        console.log(el);

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

        try {   
            const chart = new BoxPlotChart({ el, data, options } );
        } catch (e) {
            console.log(e);
        }
    }

    testing();

    const handleChange = (event) => {
        setAggAuthors(event.target.checked);
        console.log(event);
    };

    return (
        <div className="body">
            <FormGroup>
                <FormControlLabel control={<Switch defaultChecked checked={aggAuthors} onChange={handleChange} inputProps={{ 'aria-label': 'controlled' }}/>} label="Aggregate Authors" />
            </FormGroup>
            {
                aggAuthors && <p>Yuh</p>
            }
            <div id="chart-area" className="container pt-5"></div>
            <p id="testvaluehere"></p>
        </div>
    );
}

export default Visualize;