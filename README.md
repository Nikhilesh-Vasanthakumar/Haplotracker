
# HaploTracker

Haplogroups are groups of individuals who share a common ancestor based on genetic markers. The study of haplogroups is useful for understanding population migration patterns, genetic diversity, and evolution. Haplogroup Tracker is a project aimed at providing a user-friendly web-based platform for individuals to track and analyze their haplogroup.


![GitHub commit activity](https://img.shields.io/github/commit-activity/y/Nikhilesh-Vasanthakumar/Haplotracker)![Website](https://img.shields.io/website?down_color=greeen&down_message=online&up_color=green&up_message=online&url=https%3A%2F%2Fnikhilesh-vasanthakumar-haplotracker-haplogroup-tracker-wqf8g7.streamlit.app%2F)


## Usage
Haplotracker can be accessed through this
[link](https://nikhilesh-vasanthakumar-haplotracker-haplogroup-tracker-wqf8g7.streamlit.app/)

Haplotracker can also be run on your own computer.

### Installation for Manual run

You will need Python 3.11 or newer. Clone the repository from [here](https://github.com/Nikhilesh-Vasanthakumar/Haplotracker), then install the dependencies from the project folder:

```bash
pip install -r requirements.txt
```

Then start the app:

```bash
streamlit run Haplogroup_tracker.py
```

To use your own data, change `DATA_FILE` near the top of `Haplogroup_tracker.py`. The file must have the same column names as `Data/Eurasian.xlsx`.

```python
DATA_FILE = APP_DIR / "Data" / "Eurasian.xlsx"
```

## Input
The app reads a data file Eurasian.xlsx located in the Data directory. It lists ancient individuals with where they were found, how old they are, their sex, and their mtDNA and Y-chromosome haplogroups.

Ages are shown as years before today. Samples without coordinates, a date, or a haplogroup call (entries such as `..` or `n/a (<2x)`) are left out.

The user can then select the mode of the app
- "MtDNA"-Uses all the mtdna in the data
- "MtDNA-Male"-Uses all the male mtdna in the data
- "MtDNA-Female"-Uses all the female mtdna in the data
- "Y-Chromosome"-Uses all the male y-chromosome in the data

![image](https://user-images.githubusercontent.com/112621638/226195188-f6edb0b7-41a0-4f78-b9f2-58b2f91dd646.png)

The user has to select the haplogroups that they want to visualize using the multiselect box.

![image](https://user-images.githubusercontent.com/112621638/226195241-b03c875d-4aa5-4cba-82c3-cf115f0e55ab.png)

The user then has to select a map type the ones available are
- USGS- United States Geological Survey
- Natural Earth- A clean looking map with major rivers. The animation map uses a light street-map background in this mode.


![image](https://user-images.githubusercontent.com/112621638/226195278-8441361b-1af0-4854-9ef5-0ce2f8cbedfe.png)

The user also needs to select the haplogroup which they would like to animate.The first option from the user is chosen as the default.

## Example Output Maps
The map with all the selected Haplogroups which can be clicked to toggle view.
![newplot(4)](https://user-images.githubusercontent.com/112621638/226195334-82b4bd64-eb14-4a88-9f55-02e656023d55.png)

The trace map for the selected haplogroup.
![image](https://user-images.githubusercontent.com/112621638/226195642-269ac1a8-6e27-4747-860b-a75e450feb97.png)

![newplot(5)](https://user-images.githubusercontent.com/112621638/226195370-66ebef05-ff79-4745-8f53-28f59b1b9385.png)

The animation is played when the user presses the play button on the top left corner of the map. It steps through the samples of the chosen haplogroup from oldest to youngest, so the line shows where it was found over time rather than an exact migration route. Haplogroups with only one sample have nothing to animate, and the app says so.

![animate](https://user-images.githubusercontent.com/112621638/226197248-223884bc-6bc5-4606-b56a-3ce224c3dee4.mp4)

## Features

- Downloadable plots
- Fullscreen mode
- Various Map styles
- Animate the movement of the Haplogroup of your choice.


## Roadmap

- Add support to animate multiple traces

- User able to provide the input files.

- Tracking Haplogroups using existing phylogenetic databases

- Machine learning algorithm to use only sequence information to track predict haplogroups and even plot them on the map.


## 🔗 Links

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/nikhilesh23/)



## Support

For support, email ni2651va-s@student.lu.se

