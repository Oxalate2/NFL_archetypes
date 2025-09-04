# NFL_archetypes 🏈

This `NFL_archetypes` project leverages data collection and machine learning techniques to classify NFL players into distinct playstyles or "archetypes." These archetypes are based on various player stats such as passing, rushing, receiving, and defensive metrics.

## Overview

The project gathers comprehensive NFL player data for any season (default_season=2023), processes it, and generates features specific to different position groups, including:

- **Quarterbacks (QBs)**
- **Running Backs (RBs)**
- **Wide Receivers (WRs)**
- **Pass Catchers (TEs)**
- **Defensive Players**

These features are then used to analyze and cluster players into archetypes based on their playing style.

## Table of Contents

- [Data Collection](#data-collection)
- [Data Processing](#data-processing)
- [Feature Creation](#feature-creation)
- [Exploration](#exploration)
- [Archetypes](#archetypes)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Data Collection

Data is collected from [Pro Football Reference](https://www.pro-football-reference.com/), which provides a detailed breakdown of NFL player stats across different seasons.

### Data Collected:

- **Passing Stats**: Includes quarterback statistics like completions, yards, touchdowns, interceptions, etc.
- **Rushing Stats**: Includes running back statistics such as carries, yards, touchdowns, and more.
- **Receiving Stats**: Includes wide receiver and tight end statistics like receptions, yards, and targets.
- **Defensive Stats**: Includes individual defensive stats like sacks, interceptions, forced fumbles, etc.

The data is fetched using Python’s `requests` and `BeautifulSoup` libraries, allowing you to easily gather and parse the statistics.

---

## Data Processing

The collected data is processed using custom methods to clean and prepare it for analysis. These cleaning methods remove unnecessary rows and handle missing or malformed data, ensuring the resulting dataframes are ready for further analysis.

### Key Functions:
- **`_clean_passing_data()`**: Cleans quarterback passing statistics.
- **`_clean_rushing_data()`**: Cleans running back rushing statistics.
- **`_clean_receiving_data()`**: Cleans wide receiver and tight end receiving stats.
- **`_clean_defensive_data()`**: Cleans individual defensive player stats.

After cleaning the data, it’s organized into distinct position groups (`QB`, `RB`, `PASS_CATCHER`, `DEFENSE`).

---

## Feature Creation

Features are created specifically for each position group to facilitate archetype classification. The goal is to generate measurable characteristics that capture the player's playing style.

### Example Features:
- **Quarterbacks**: Passer rating, yards per attempt, deep ball ability, sack rate.
- **Running Backs**: Yards per carry, rushing touchdown rate, long run ability, fumble rate.
- **Wide Receivers / Tight Ends**: Catch rate, yards per reception, target share, red zone threat.

These features are calculated using key statistical categories like passing attempts, completions, rushing yards, receptions, etc.

---

## Exploration

Once features are created, the data can be explored using simple queries to identify top performers in each category.

For example, you can query the top 5 quarterbacks by passer rating, top 5 running backs by yards per carry, and top 5 wide receivers by yards per game.

### Example Output:
