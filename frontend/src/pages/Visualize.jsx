import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Chart from "react-apexcharts";
//import {BoxPlotChart} from '@toast-ui/chart';
//import BoxPlotChart from '@toast-ui/chart/boxPlot';
import { BoxPlotChart } from '@toast-ui/react-chart';
import { styled } from '@mui/material/styles';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Typography from '@mui/material/Typography';
import Switch from '@mui/material/Switch';
import Select from '@mui/material/Select';
import Slider from '@mui/material/Slider';
import Checkbox from '@mui/material/Checkbox';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import CheckBoxOutlineBlankIcon from '@mui/icons-material/CheckBoxOutlineBlank';
import CheckBoxIcon from '@mui/icons-material/CheckBox';

const icon = <CheckBoxOutlineBlankIcon fontSize="small" />;
const checkedIcon = <CheckBoxIcon fontSize="small" />;
const Separator = styled('div')(
    ({ theme }) => `
    height: ${theme.spacing(3)};
  `,
  );

function Visualize() {

    const [aggAuthors, setAggAuthors] = useState(true);

    const [selectBy, setSelectBy] = useState("authors");

    const [range, setRange] = useState([1960, 2022]);

    const [bounds, setBounds] = useState([1960, 2022]);

    const [authors, setAuthors] = useState([]);

    const [selectedAuthors, setSelectedAuthors] = useState([]);

    const [tab, setTab] = useState("boxplot");

    const [data, setData] = useState({
        categories: ['Author 1', 'Author 2', 'Author 3', 'Author 4'],
        series: [
            {
                data: [
                    [1000, 2500, 3714, 5500, 7000],
                    [1000, 2750, 4571, 5250, 8000],
                    [3000, 4000, 4714, 6000, 7000],
                    [1000, 2250, 3142, 4750, 6000],
                ],
                outliers: [
                    [0, 14000],
                    [0, 10000],
                    [3, 9600],
                ],
            }
        ],
    });

    const [options, setOptions] = useState({
        chart: { title: 'Citations', width: 900, height: 500 },
        legend: { visible: false }
    });

    const handleChange = (event) => {
        setData({});
        console.log(event);
    };

    useEffect(() => {
        axios.get("api/authors")
            .then(response => {
                setAuthors(response.data);
            }).
            catch(err => {
                console.log(err);
            }
        );
    }, []);

    return (
        <div className="body">
            <div className="container">
                <div className="row d-flex">
                    <div className="col-4">
                        <Box sx={{ width: 300 }}>
                            <FormControl fullWidth>
                                <InputLabel id="filter-select-label">Filter</InputLabel>
                                <Select
                                    labelId="filter-select-label"
                                    id="filter-select"
                                    value={selectBy}
                                    label="Filter"
                                    onChange={(event) => { setSelectBy(event.target.value); }}>
                                    <MenuItem value={"authors"}>Authors</MenuItem>
                                    <MenuItem value={"tags"}>Tags</MenuItem>
                                </Select>
                            </FormControl>
                        </Box>
                        <Separator />
                        {
                            selectBy === "tags" &&
                            <FormGroup>
                                <FormControlLabel control={
                                    <Switch
                                        defaultChecked
                                        checked={aggAuthors}
                                        onChange={(event) => { setAggAuthors(event.target.checked); }}
                                        inputProps={{ 'aria-label': 'controlled' }}>
                                    </Switch>
                                } label="Aggregate Authors">
                                </FormControlLabel>
                                <Separator />
                            </FormGroup>
                        }
                        {
                            selectBy === "tags" && aggAuthors && <p>Yuh</p>
                        }
                        {
                            selectBy === "authors" &&
                            <Autocomplete
                                multiple
                                id="checkboxes-authors"
                                options={authors}
                                disableCloseOnSelect
                                getOptionLabel={(option) => option.name}
                                renderOption={(props, option, { selected }) => (
                                    <li {...props}>
                                        <Checkbox
                                            icon={icon}
                                            checkedIcon={checkedIcon}
                                            style={{ marginRight: 8 }}
                                            checked={selected}
                                            //next two lines fix
                                            value={option.id}
                                            onChange={(event) => { setSelectedAuthors([...selectedAuthors, event.target.value]); console.log(selectedAuthors); }}
                                        />
                                        {option.name}
                                    </li>
                                )}
                                style={{ width: 300 }}
                                renderInput={(params) => (
                                    <TextField {...params} label="Authors" placeholder="Authors" />
                                )}
                            />
                        }
                        {
                            (tab === "boxplot" || tab === "trend") &&
                            <Box sx={{ width: 300 }}>
                                <Typography id="year-range-id" gutterBottom>
                                    Year Range
                                </Typography>
                                <Slider
                                    aria-labelledby="year-range-id"
                                    value={range}
                                    onChange={(event) => { setRange(event.target.value); }}
                                    valueLabelDisplay="auto"
                                    min={bounds[0]}
                                    max={bounds[1]}>
                                </Slider>
                                <Separator />
                            </Box>
                        }
                    </div>
                    <div className="col-8">
                        <div id="chart-area" className="container pt-5">
                            <BoxPlotChart data={data} options={options}></BoxPlotChart>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Visualize;