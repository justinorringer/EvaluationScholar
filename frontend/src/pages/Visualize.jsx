import React, { useState, useEffect } from 'react';
import axios from 'axios';
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

    const [range, setRange] = useState([1960, new Date().getFullYear()]);

    const [bounds, setBounds] = useState([1960, 2022]);

    const [authors, setAuthors] = useState([]);

    const [selectedAuthors, setSelectedAuthors] = useState([]);

    const [authorsData, setAuthorsData] = useState([]);

    const [tags, setTags] = useState([]);

    const [selectedTags, setSelectedTags] = useState([]);

    const [indexType, setIndexType] = useState("");

    const [index, setIndex] = useState(1);

    const [tab, setTab] = useState("boxplot");

    const [toggleOutliers, setToggleOutliers] = useState(true);

    const [data, setData] = useState({
        categories: [],
        series: [
            {
                data: [],
                outliers: [],
            }
        ],
    });

    const [options, setOptions] = useState({
        chart: { title: 'Citations', width: 700, height: 500 },
        legend: { visible: false }
    });

    /**
     * Function to sort alphabetically an array of objects by some specific key.
     * 
     * @param {String} property Key of the object to sort.
     * @author https://ourcodeworld.com/articles/read/764/how-to-sort-alphabetically-an-array-of-objects-by-key-in-javascript
     */
    function alphabeticSort(property) {
        var sortOrder = 1;

        if (property[0] === "-") {
            sortOrder = -1;
            property = property.substr(1);
        }

        return function (a, b) {
            if (sortOrder == -1) {
                return b[property].localeCompare(a[property]);
            } else {
                return a[property].localeCompare(b[property]);
            }
        }
    }

    useEffect(() => {
        setAuthorsData([]);
        selectedAuthors.forEach(author => {
            console.log("hello author");
            axios.get(`api/authors/${author.id}?include=papers`)
                .then(response => {
                    setAuthorsData([...authorsData, response.data]);
                    console.log(response.data);
                }).
                catch(err => {
                    console.log(err);
                }
                );
        });        
    }, [selectedAuthors]);

    useEffect(() => {        
        const tempData = {
            categories: [],
            series: [
                {
                    data: [],
                    outliers: [],
                }
            ],
        };
        console.log(tempData);
        let i = 0;
        authorsData.forEach(author => {
            console.log(author);
            tempData.categories.push(author.name);
            const papers = [];
            author.papers.forEach(paper => {
                papers.push(paper.latest_citation.num_cited);
            })
            //sort the papers for the author
            papers.sort(function (a, b) {
                return a - b;
            });
            //check the sort
            console.log(papers);

            var med = 0; //get median
            if (papers.length === 0) throw new Error("No inputs");
            var half2 = Math.floor(papers.length / 2);
            if (papers.length % 2) {
                med = papers[half2];
            } else {
                med = (papers[half2 - 1] + papers[half2]) / 2.0;
            }
            console.log(med);

            var half = Math.ceil(papers.length / 2);
            var firstHalf = papers.splice(0, half);
            var secondHalf = papers.splice(-half);

            console.log(papers);
            console.log(half);
            console.log(firstHalf);
            console.log(secondHalf);

            var q1 = 0; //get Q1
            if (firstHalf.length === 0) throw new Error("No inputs");
            half2 = Math.floor(firstHalf.length / 2);
            if (firstHalf.length % 2) {
                q1 = firstHalf[half2];
            } else {
                q1 = (firstHalf[half2 - 1] + firstHalf[half2]) / 2.0;
            }
            console.log(q1);

            var q3 = 0; //get Q3
            if (secondHalf.length === 0) throw new Error("No inputs");
            half2 = Math.floor(secondHalf.length / 2);
            if (secondHalf.length % 2) {
                q3 = secondHalf[half2];
            } else {
                q3 = (secondHalf[half2 - 1] + secondHalf[half2]) / 2.0;
            }
            console.log(q3);

            var iqr = q3 - q1; //get IQR
            console.log(iqr);
            var min = 0;
            var max = 0;

            const minThreshold = q1 - (1.5 * iqr); //get outlier threshold for lower bound
            const maxThreshold = q3 + (1.5 * iqr); //get outlier threshold for higher bound

            console.log(minThreshold);
            console.log(maxThreshold);

            for (let j = 0; j < firstHalf.length; j++) {
                let value = firstHalf[j];
                if (value < minThreshold) {
                    if (toggleOutliers) {
                        tempData.series[0].outliers.push([i, value]);
                    }
                } else {
                    min = value; //set min
                    break;
                }
            }
            for (let j = secondHalf.length - 1; j >= 0; j--) {
                let value = secondHalf[j];
                if (value > maxThreshold) {
                    if (toggleOutliers) {
                        tempData.series[0].outliers.push([i, value]);
                    }
                } else {
                    max = value; //set max
                    break;
                }
            }

            tempData.series[0].data.push([min, q1, med, q3, max]);
            i++;

            // function median(...papers) {
            //     console.log(papers);
        
            //     if (papers.length === 0) throw new Error("No inputs");
        
            //     var half = Math.floor(papers.length / 2);
        
            //     if (papers.length % 2)
            //         return papers[half];
        
            //     return (papers[half - 1] + papers[half]) / 2.0;
            // }
        });
        
        if (selectedAuthors.length > 0 && authorsData.length > 0) {
            console.log(tempData);
            setData(tempData);
            console.log(data);
        }
    }, [authorsData, toggleOutliers]);

    useEffect(() => {
        axios.get("api/authors?include=papers")
            .then(response => {
                setAuthors(response.data.sort(alphabeticSort("name")));
                console.log(response.data);
            }).
            catch(err => {
                console.log(err);
            }
        );
        axios.get("api/tags")
            .then(response => {
                setTags(response.data.sort(alphabeticSort("name")));
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
                                        />
                                        {option.name}
                                    </li>
                                )}
                                onChange={(event, value) => setSelectedAuthors(value)}
                                style={{ width: 300 }}
                                renderInput={(params) => (
                                    <TextField {...params} label="Authors" placeholder="Authors" />
                                )}
                            />
                        }
                        {
                            selectBy === "tags" &&
                            <Autocomplete
                                multiple
                                id="checkboxes-tags"
                                options={tags}
                                disableCloseOnSelect
                                getOptionLabel={(option) => option.name}
                                renderOption={(props, option, { selected }) => (
                                    <li {...props}>
                                        <Checkbox
                                            icon={icon}
                                            checkedIcon={checkedIcon}
                                            style={{ marginRight: 8 }}
                                            checked={selected}
                                        />
                                        {option.name}
                                    </li>
                                )}
                                onChange={(event, value) => setSelectedTags(value)}
                                style={{ width: 300 }}
                                renderInput={(params) => (
                                    <TextField {...params} label="Tags" placeholder="Tags" />
                                )}
                            />
                        }
                        <Separator/>
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
                        {
                            selectBy === "tags" &&
                            <div className="row" style={{ margin: "0 0 0 0"}}>
                                <Box sx={{ width: 180 }}>
                                    <FormControl fullWidth>
                                        <InputLabel id="index-select-label">Index</InputLabel>
                                        <Select
                                            labelId="index-select-label"
                                            id="index-select"
                                            value={indexType}
                                            label="Index"
                                            onChange={(event) => { setIndexType(event.target.value); }}>
                                            <MenuItem value={"h-index"}>h-index</MenuItem>
                                            <MenuItem value={"i10-index"}>i10-index</MenuItem>
                                        </Select>
                                    </FormControl>
                                </Box>
                                <Box sx={{ width: 20 }}></Box>
                                {
                                    indexType &&
                                    <Box sx={{ width: 100 }}>
                                        <FormControl fullWidth>
                                            <TextField
                                                label="Minimum Index"
                                                value={index}
                                                onChange={(event) => { const onlyNums = event.target.value.replace(/[^0-9]/g, ''); setIndex(onlyNums); }}
                                                inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                                                variant="standard"
                                            />
                                        </FormControl>
                                    </Box>
                                }
                            </div>
                        }
                    </div>
                    <div className="col-8">
                        <div id="chart-area" className="container pt-5">
                            {
                                data && options &&
                                <BoxPlotChart data={data} options={options}></BoxPlotChart>
                            }
                        </div>
                        {
                            tab === "boxplot" &&
                            <FormGroup>
                                <Separator />
                                <FormControlLabel control={
                                    <Switch
                                        defaultChecked
                                        checked={toggleOutliers}
                                        onChange={(event) => { setToggleOutliers(event.target.checked); }}
                                        inputProps={{ 'aria-label': 'controlled' }}>
                                    </Switch>
                                } label="Display Outliers">
                                </FormControlLabel>
                                <Separator />
                            </FormGroup>
                        }
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Visualize;