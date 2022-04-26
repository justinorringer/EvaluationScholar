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
import PropTypes from 'prop-types';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import CheckBoxOutlineBlankIcon from '@mui/icons-material/CheckBoxOutlineBlank';
import CheckBoxIcon from '@mui/icons-material/CheckBox';

const icon = <CheckBoxOutlineBlankIcon fontSize="small" />;
const checkedIcon = <CheckBoxIcon fontSize="small" />;
const Separator = styled('div')(
    ({ theme }) => `
    height: ${theme.spacing(3)};
  `,
);
function a11yProps(index) {
    return {
        id: `simple-tab-${index}`,
        'aria-controls': `simple-tabpanel-${index}`,
    };
}

function Visualize() {

    const [aggAuthors, setAggAuthors] = useState(true);

    const [selectBy, setSelectBy] = useState("authors");

    const [range, setRange] = useState([1960, new Date().getFullYear()]);

    const [bounds, setBounds] = useState([1960, new Date().getFullYear()]);

    const [authors, setAuthors] = useState([]);

    const [selectedAuthors, setSelectedAuthors] = useState([]);

    const [authorsData, setAuthorsData] = useState([]);

    const [tags, setTags] = useState([]);

    const [selectedTags, setSelectedTags] = useState([]);

    const [indexType, setIndexType] = useState("");

    const [index, setIndex] = useState(0);

    const [tab, setTab] = useState(0);

    const [toggleOutliers, setToggleOutliers] = useState(true);

    const [boxData, setBoxData] = useState({
        categories: [],
        series: [
            {
                data: [],
                outliers: [],
            }
        ],
    });

    const theme = {
        chart: {
            fontFamily: 'Josefin Sans',
            backgroundColor: '#e7e3e4e8',
        },
        series: {
          colors: ['#CC0000'],
          dot: {
            radius: 5,
            borderWidth: 3,
            borderColor: '#000000',
            useSeriesColor: true,
          },
          rect: {
            borderWidth: 2,
            borderColor: '#000000',
          },
          line: {
            whisker: {
              lineWidth: 2,
              color: '#000000',
            },
            maximum: {
              lineWidth: 2,
              color: '#000000',
            },
            minimum: {
              lineWidth: 2,
              color: '#000000',
            },
            median: {
              lineWidth: 2,
              color: '#000000',
            },
          },
          hover: {
            color: '#ffdfdf',
            rect: { borderColor: '#000000', borderWidth: 2 },
            dot: { radius: 6 },
            shadowColor: 'rgba(0, 0, 0, 0.7)',
            shadowOffsetX: 4,
            shadowOffsetY: 4,
            shadowBlur: 6,
            line: {
              whisker: {
                lineWidth: 2,
                color: '#000000',
              },
              maximum: {
                lineWidth: 2,
                color: '#000000',
              },
              minimum: {
                lineWidth: 2,
                color: '#000000',
              },
              median: {
                lineWidth: 2,
                color: '#000000',
              },
            },
          },
        }
      };

    const options = {
        chart: { title: "", width: 700, height: 500 },
        yAxis: { scale: { min: 0 } },
        legend: { visible: false },
        theme: theme
    };

    /**
     * Function to sort alphabetically an array of objects by some specific key.
     * 
     * @param {String} property Key of the object to sort.
     * @author https://ourcodeworld.com/articles/read/764/how-to-sort-alphabetically-an-array-of-objects-by-key-in-javascript
     */
    function alphabeticSort(property) {
        let sortOrder = 1;

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

    function median(papers) {
        if (papers.length === 0) throw new Error("No inputs");

        let half = Math.floor(papers.length / 2);

        if (papers.length % 2)
            return papers[half];

        return (papers[half - 1] + papers[half]) / 2.0;
    }

    //get authors and their papers if selected
    useEffect(() => {
        let tempMin = new Date().getFullYear(); //current year starting min
        let tempMax = 0; //0 starting max
        const tempAuthorData = [];
        const mapAuthors = selectedAuthors.map(author => {
            return axios.get(`api/authors/${author.id}?include=papers`)
                .then(response => {
                    tempAuthorData.push(response.data);
                }).
                catch(err => {
                    console.log(err);
                }
                );
        });
        Promise.all(mapAuthors).then(() => {
            tempAuthorData.forEach(author => {
                author.papers.forEach(paper => {
                    if (paper.year > tempMax) {
                        tempMax = paper.year;
                    }
                    if (paper.year < tempMin) {
                        tempMin = paper.year;
                    }
                })
            })
            if (tempMax > 0) {
                setBounds([tempMin, tempMax]);
            }
            setAuthorsData(tempAuthorData);
        })
    }, [selectedAuthors]);

    //get authors and their papers given tag(s). group authors if aggAuthors === true
    useEffect(() => {
        let tempMin = new Date().getFullYear(); //current year starting min
        let tempMax = 0; //0 starting max
        axios.get(`api/authors?include=papers&tags=${selectedTags.map(tag => tag.id)}&min-${indexType}=${index}`)
            .then(response => {
                const papers = [];
                response.data.forEach(author => {
                    author.papers.forEach(paper => {
                        if (paper.year > tempMax) {
                            tempMax = paper.year;
                        }
                        if (paper.year < tempMin) {
                            tempMin = paper.year;
                        }
                        papers.push(paper);
                    });
                });
                if (tempMax > 0) {
                    setBounds([tempMin, tempMax]);
                }
                if (aggAuthors) {
                    setAuthorsData([{ name: selectedTags.map(tag => tag.name).join(", "), papers: papers }]);
                } else {
                    setAuthorsData(response.data);
                }
            }).
            catch(err => {
                console.log(err);
            }
            );
    }, [selectedTags, aggAuthors, index]);

    //reset graph
    useEffect(() => {
        const categories = [];
        const data = [];
        const outliers = [];

        let i = 0;
        authorsData.forEach(author => {
            categories.push(author.name);
            const papers = [];
            author.papers.forEach(paper => {
                if (paper.year >= range[0] && paper.year <= range[1]) {
                    papers.push(paper.latest_citation.num_cited);
                }
            });
            //sort the papers for the author
            papers.sort(function (a, b) {
                return a - b;
            });
            //check the sort

            let firstHalf = [];
            let secondHalf = [];
            let med = 0;
            let q1 = 0;
            let q3 = 0;
            try {
                if (papers.length > 0) {
                    med = median(papers); //get median
                }
                q1 = med; //set to median by default
                q3 = med; //set to median by default
                if (papers.length > 1) {
                    let half = Math.ceil(papers.length / 2);
                    firstHalf = papers.splice(0, half);
                    secondHalf = papers.splice(-half);
                    q1 = median(firstHalf); //reset to median of the first half
                    if (secondHalf.length > 0) {
                        q3 = median(secondHalf); //reset to median of the second half as long as the second half exists
                    }
                }
            } catch (e) { //something was length 0
                console.log(e);
            }

            const iqr = q3 - q1; //get IQR

            let min = q1;
            let max = q3;

            const minThreshold = q1 - (1.5 * iqr); //get outlier threshold for lower bound
            const maxThreshold = q3 + (1.5 * iqr); //get outlier threshold for higher bound

            for (let j = 0; j < firstHalf.length; j++) {
                let value = firstHalf[j];
                if (value < minThreshold) {
                    if (toggleOutliers) {
                        outliers.push([i, value]);
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
                        outliers.push([i, value]);
                    }
                } else {
                    max = value; //set max
                    break;
                }
            }

            data.push([min, q1, med, q3, max]);
            i++;
        });

        setBoxData({
            categories: categories,
            series: [
                {
                    name: "Author",
                    data: data,
                    outliers: outliers,
                }
            ],
        });
    }, [authorsData, toggleOutliers, range]);

    useEffect(() => {
        axios.get("api/authors")
            .then(response => {
                setAuthors(response.data.sort(alphabeticSort("name")));
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
                        <div className="container">
                            <h3>Visualize</h3>
                        </div>
                        <Separator />
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
                        <Separator />
                        {
                            selectBy === "tags" &&
                            <FormGroup>
                                <FormControlLabel control={
                                    <Switch
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
                            (tab === 0 || tab === 1) &&
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
                            <div className="row" style={{ margin: "0 0 0 0" }}>
                                <Box sx={{ width: 180 }}>
                                    <FormControl fullWidth>
                                        <InputLabel id="index-select-label">Index</InputLabel>
                                        <Select
                                            labelId="index-select-label"
                                            id="index-select"
                                            value={indexType}
                                            label="Index"
                                            onChange={(event) => { setIndexType(event.target.value); }}>
                                            <MenuItem value={"h"}>h-index</MenuItem>
                                            <MenuItem value={"i10"}>i10-index</MenuItem>
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
                        {
                            tab === 0 &&
                            <FormGroup>
                                <Separator />
                                <FormControlLabel control={
                                    <Switch
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
                    <div className="col-8 p-4">
                        <div id="chart-area" className="container">
                            <Box sx={{ width: '100%' }}>
                                <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                                    <Tabs value={tab} onChange={(event, value) => { setTab(value); }} aria-label="basic tabs example">
                                        <Tab label="Boxplot" {...a11yProps(0)} />
                                        <Tab label="Trend" {...a11yProps(1)} />
                                        <Tab label="h-index" {...a11yProps(2)} />
                                        <Tab label="i10-index" {...a11yProps(3)} />
                                    </Tabs>
                                </Box>
                            </Box>
                            {
                                boxData && options &&
                                <BoxPlotChart data={boxData} options={options}></BoxPlotChart>
                            }
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Visualize;