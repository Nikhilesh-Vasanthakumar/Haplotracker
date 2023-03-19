
# HaploTracker

Haplogroups are groups of individuals who share a common ancestor based on genetic markers. The study of haplogroups is useful for understanding population migration patterns, genetic diversity, and evolution. Haplogroup Tracker is a project aimed at providing a user-friendly web-based platform for individuals to track and analyze their haplogroup.


![GitHub commit activity](https://img.shields.io/github/commit-activity/y/Nikhilesh-Vasanthakumar/Haplotracker)![Website](https://img.shields.io/website?down_color=greeen&down_message=online&up_color=green&up_message=online&url=https%3A%2F%2Fnikhilesh-vasanthakumar-haplotracker-haplogroup-tracker-wqf8g7.streamlit.app%2F)


## Usage
Haplotracker can be accessed through this
[link](https://nikhilesh-vasanthakumar-haplotracker-haplogroup-tracker-wqf8g7.streamlit.app/)

Haplotracker can also be used by downloading the Haplotracker.py file
This requires the following packages.

### Installation for Manual run

To run the app, you will need Python 3.x and the following libraries:


```bash
pip install pandas
pip install plotly
pip install streamlit
pip install Pillow
```
Clone the repository from [here](https://github.com/Nikhilesh-Vasanthakumar/Haplotracker)

You will have to rename the file name in the code line **72** when using your own files

```python
data=pd.read_excel("Data/Eurasian.xlsx") 
```
You can then run the the following code in anaconda prompt to run the app.

```bash
streamlit run haplotracker.py
```

## Input
The app reads a data file Eurasian.xlsx located in the Data directory. The data file contains information about the location and migration patterns of various haplogroups.

The user can then select the mode of the app
- "MtDNA"-Uses all the mtdna in the data
- "MtDNA-Male"-Uses all the male mtdna in the data
- "MtDNA-Female"-Uses all the female mtdna in the data
- "Y-chromosome"-Uses all the male y-chromosome in the data

INSERT IMAGE HERE

The user has to select the haplogroups that they want to visualize using the multiselect box.

INSERT IMAGE HERE

The user then has to select a map type the ones available are
- USGS- United States Geological Survey
- Natural Earth- A clean looking map with major rivers.

INSERT IMAGE HERE

The user also needs to select the haplogroup which they would like to animate.The first option from the user is chosen as the default.

INSERT IMAGE HERE
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

