# SfePrapy

A probabilistic analysis tool that estimates the structural reliability for a given scenario (such as enclosure geometry, building type, window areas etc.) against equivalent time exposure to the ISO 834 fire curve.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Python 3.6.0 or later is required.

### Installation

#### pip

pip is a package management system for installing and updating Python packages. pip comes with Python, so you get pip simply by installing Python. On Ubuntu and Fedora Linux, you can simply use your system package manager to install the `python3-pip` package. [_The Hitchhiker's Guide to Python_ provides some guidance on how to install Python on your system if it isn't already](https://docs.python-guide.org/starting/installation/); you can also [install Python directly from python.org](https://www.python.org/getit/). You might want to [upgrade pip](https://pip.pypa.io/en/stable/installing/) before using it to install other programs.

SfePrapy uses Python, and as of July 2018 SfePrapy only works in Python3. 

1.	If you are using Windows with Python version 3.3 or higher, use the [Python Launcher for Windows](https://docs.python.org/3/using/windows.html?highlight=shebang#python-launcher-for-windows) to use `pip` with Python version 3:
    ```bash
    py -3 -m pip install SfePrapy
    ```
2.	If your system has a `python3` command (standard on Unix-like systems), install with:
    ```bash
    python3 -m pip install SfePrapy
    ```
3.	You can also just use the `python` command directly, but this will use the _current_ version of Python in your environment:
    ```bash
    python -m pip install SfePrapy
    ```

### Usage

To run SfePrapy Monte Carlo simulation routine in a terminal window:

```sh
python -m SfePrapy.mc
```

To run SfePrapy Monte Carlo simulation routine in Python:

```python
from sfeprapy.mc.__main__ import run
run()
```

A dialog box will pop out for you to select folders containing problem definition files. The dialog box will only let you select one folder at a time, but you can select more folders after you click **Select Folder** button. Click **Cancel** to finish selecting folders and the time equivalence analysis will proceed. The program will be paused when all problem definition files are complete. Example console output is shown below.

```
Work directory:          C:/Users/ian/Desktop/SfePrapy_test
Input file:              time_equivalence_version_0.0.3_1.txt
Total simulations:       1000
Number of threads:       8
████████████████████████ 115.1s
Press Enter to finish
```

The app will identify all input files contained in the folder directory and run them one by one until all input files are complete. Simulation output files will be saved under the input file directory.

#### `sfeprapy.mc` Required Input Parameters

The input parameters have been organised on this sheet and the units provided. The key parameters to adjust for each modelling case have been highlighted red. Other parameters will need to be adjusted for specific cases. Completing this table produces the output in the layout required for the csv input file on the sheet "Input for SfePrapy". This can then be copied into the csv file used as the input for SfePrapy - see misc folder for template. The third sheet of this document provides an example input file which if saved as a csv holds the data for three cases but would only run the first two (see "is_live" variable).

| PARAMETER                           | UNITS                                  | DESCRIPTION                                                  |
| ----------------------------------- | -------------------------------------- | ------------------------------------------------------------ |
| **Model Settings**                  |                                        |                                                              |
| is_live                             | -                                      | This is the trigger to tell SfePrapy to run the model for this set of input values. In the input CSV there can be multiple cases |
| simulations                         | -                                      | The number of simulations that will   be run. A sensitivity analysis should be carried out to determine the   appropriate number of simulations |
| **Compartment Geometry**            |                                        |                                                              |
| room_breadth                        | $m$                                    | Breadth of room                                              |
| room_depth                          | $m$                                    | Depth of room                                                |
| room_height                         | $m$                                    | Height of room                                               |
| room_window_width                   | $m$                                    | Total width of windows for   compartment                     |
| room_window_height                  | $m$                                    | Height of window (top of window to   bottom of window, not height from floor) |
| beam_loc_z                          | $m$                                    | Height of test beam within the   compartment. This can be altered to assess the influence of height in tall   compartments. Need to assess worst case height for columns. |
| beam_loc_ratio_lbound               | -                                      | Min beam location relative to   compartment length for TFM - Linear dist |
| beam_loc_ratio_ubound               | -                                      | Max beam location relative to   compartment length for TFM - Linear dist |
| **Windows/Natural Vent**            |                                        |                                                              |
| room_opening_fraction_std           | -                                      | Glazing fall-out fraction - 1-lognorm   - standard dev.      |
| room_opening_fraction_mean          | -                                      | Glazing fall-out fraction - 1-lognorm   - mean               |
| room_opening_fraction_ubound        | -                                      | Glazing fall-out fraction - 1-lognorm   - upper limit        |
| room_opening_fraction_lbound        | -                                      | Glazing fall-out fraction - 1-lognorm   - lower limit        |
| room_opening_permanent_fraction     | -                                      | Use this to force a ratio of open   windows. If there is a vent to the outside this can be included here. |
| **Fire inputs**                     |                                        |                                                              |
| time_start                          | $s$                                    | Start time of simulation. Use 0s                             |
| fire_tlim                           | $hour$                                 | *For parametric fire only*<br/>Time for maximum gas temperature in case of fuel controlled fire. Slow fire growth rate:0.417   Medium:0.333 Fast:0.25 (Annex A EN 1991-1-2) |
| time_step                           | $s$                                    | Time step used for the model.   Suggested time step 30s.     |
| time_duration                       | $s$                                    | End of simulation. This should be set   so that output data is produced allowing the target reliability to be   determined. Not always necessary to run for extended periods. |
| room_wall_thermal_inertia           | $\frac{J}{m^{2}\cdot K \cdot s^{0.5}}$ | Compartment thermal inertia                                  |
| fire_qfd_mean                       | $\frac{MJ}{m^{2}}$                     | Fire load density - Gumbel distribution - mean               |
| fire_qfd_std                        | $\frac{MJ}{m^{2}}$                     | Fire load density - Gumbel   distribution - standard dev     |
| fire_qfd_lbound                     | -                                      | Fire load density - Gumbel   distribution - lower limit      |
| fire_qfd_ubound                     | $\frac{MJ}{m^{2}}$                     | Fire load density - Gumbel   distribution - upper limit      |
| fire_hrr_density                    | $\frac{MW}{m^{2}}$                     | Heat release rate. This should be selected based on the fuel. See literature for typical values for different occupancies. |
| fire_spread_lbound                  | $\frac{MJ}{m^{2}}$                     | Min spread rate for TFM - Linear distribution                |
| fire_spread_ubound                  | $\frac{m}{s}$                          | Max spread rate for TFM - Linear distribution                |
| fire_nft_mean                       | $°C$                                   | TFM near field temperature - Norm   distribution - mean      |
| fire_com_eff_lbound                 | -                                      | Min combustion efficiency - Linear distribution              |
| fire_com_eff_ubound                 | -                                      | Max combustion efficiency - Linear distribution              |
| **Section Properties**              |                                        |                                                              |
| beam_cross_section_area             | $m²$                                   | Cross sectional area of beam                                 |
| beam_rho                            | $\frac{kg}{m^{3}}$                     | Density of beam                                              |
| beam_temperature_goal               | $K$                                    | Beam (steel) failure temperature in   kelvin for goal seek   |
| beam_protection_protected_perimeter | $m$                                    | Heated perimeter                                             |
| beam_protection_thickness           | $m$                                    | Thickness of protection                                      |
| beam_protection_k                   | $\frac{W}{m\cdot K}$                   | Protection conductivity                                      |
| beam_protection_rho                 | $\frac{kg}{m^{3}}$                     | Density of protection to beam                                |
| beam_protection_c                   | $\frac{J}{kg\cdot K}$                  | Specific heat of protection                                  |

A configuration file (.json) is also required to run the simulation

#### Example - Run a MC simulation with three scenarios

The following input parameters are adopted for this demo, saved as the `demo.csv` file.

| PARAMETERS                          | case_1 | case_2 | case_3 |
| ----------------------------------- | ------ | ------ | ------ |
| is_live                             | 1      | 1      | 1      |
| simulations_multiplier              | 0.333  | 0.333  | 0.333  |
| simulations                         | 1000   | 1000   | 1000   |
| time_step                           | 30     | 30     | 30     |
| time_start                          | 0      | 0      | 0      |
| time_duration                       | 18000  | 18000  | 18000  |
| fire_hrr_density                    | 0.25   | 0.25   | 0.25   |
| fire_qfd_std                        | 126    | 126    | 126    |
| fire_qfd_mean                       | 420    | 420    | 420    |
| fire_qfd_ubound                     | 0.001  | 0.001  | 0.001  |
| fire_qfd_lbound                     | 1500   | 1500   | 1500   |
| fire_spread_lbound                  | 0.0035 | 0.0035 | 0.0035 |
| fire_spread_ubound                  | 0.0193 | 0.0193 | 0.0193 |
| fire_nft_mean                       | 1050   | 1050   | 1050   |
| fire_com_eff_lbound                 | 0.75   | 0.75   | 0.75   |
| fire_com_eff_ubound                 | 0.999  | 0.999  | 0.999  |
| fire_tlim                           | 0.333  | 0.333  | 0.333  |
| room_breadth                        | 15.8   | 15.8   | 15.8   |
| room_depth                          | 31.6   | 31.6   | 31.6   |
| room_height                         | 3      | 3      | 3      |
| room_window_width                   | 72     | 72     | 72     |
| room_window_height                  | 2.8    | 2.8    | 2.8    |
| room_opening_fraction_std           | 0.2    | 0.2    | 0.2    |
| room_opening_fraction_mean          | 0.2    | 0.2    | 0.2    |
| room_opening_fraction_ubound        | 1      | 1      | 1      |
| room_opening_fraction_lbound        | 0      | 0      | 0      |
| room_opening_permanent_fraction     | 0      | 0      | 0      |
| room_wall_thermal_inertia           | 720    | 720    | 720    |
| beam_cross_section_area             | 0.017  | 0.017  | 0.017  |
| beam_rho                            | 7850   | 7850   | 7850   |
| beam_temperature_goal               | 893    | 893    | 893    |
| beam_protection_protected_perimeter | 2.14   | 2.14   | 2.14   |
| beam_protection_thickness           | 0.0125 | 0.0125 | 0.0125 |
| beam_protection_k                   | 0.2    | 0.2    | 0.2    |
| beam_protection_rho                 | 800    | 800    | 800    |
| beam_protection_c                   | 1700   | 1700   | 1700   |
| beam_loc_z                          | 2      | 4      | 6      |
| beam_loc_ratio_lbound               | 0.6    | 0.6    | 0.6    |
| beam_loc_ratio_ubound               | 0.999  | 0.999  | 0.999  |

`config.json` contains configurations for `SfePrapy.mc`.

```json
{
  "n_proc": 7,
  "plot_teq_xlim": 120,
  "reliability_target": 0.8
}
```

Activate Python virtual environment and run SfePrapy.

```bash
python -m SfePrapy.mc
```

##Limitations of SfePrapy

###Eurocode Parametric Fire

#### Maximum floor geometry

500 m^2

Travelling Fire

#### Beam/Column temperature measurement location

this is conservatively the same as ceiling height of the compartment. 

## Authors

* **Yan Fu** - *fuyans@gmail.com*
* **Danny Hopkin** - *danny.hopkin@ofrconsultants.com*
* **Ieuan Rickard** - *ieuan.rickard@ofrconsultants.com*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
