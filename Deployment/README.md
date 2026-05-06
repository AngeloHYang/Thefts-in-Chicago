# Deployment

## Virtual Environment

You can install Anaconda, then create a virtual environment with:

`conda create -n yourVirtualEnvironmentName python=3.8`

To activate the virtual environment, you can:

`conda activate yourVirtualEnvironmentName`

> By the way, to deactivate the virtual environment, you can:
>
> `conda deactivate`
>
> You can delete a virtual environment with:
>
> `conda remove -n yourVirtualEnvironmentName --all`

## Requirements

The python version should be lower than 3.9. That's why we chose `python=3.8` above.

Install fbprophet with:

`conda install -c conda-forge prophet`

Install gettext with:

`conda install gettext`

You can install required packages via:

`pip install -r Requirements.txt `

## Data Analysis Extra Requirementshere

The Jupyter Notebook about Data Analysis of Thefts in Chicago locates [here](../Data Analysis Code/). Obviously you'll need Jupiter Notebook in order to run it.