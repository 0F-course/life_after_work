#!/usr/local/bin/python3

from os.path import exists
from os import mkdir
from pandas import read_csv, merge
from IPython.display import HTML
import plotly.express as px
from plotly.colors import DEFAULT_PLOTLY_COLORS as colors
from plotly.io import templates
templates.default = 'none'


def print_fig(name, width=1000, height=650):
    fig.update_layout(width=width, height=height, font_size=20)
    fig.write_image(f'images/{name}.png')
    with open(f'plots/{name}.html', 'w') as fh:
        fh.write(
f'''<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
    </head>
    <body style="background-color: #6aa4c8; height: 900px; display: flex; justify-content: center; align-items: center;">
        { fig.to_html(full_html=False, include_plotlyjs='cns') }
    </body>
</html>'''
        )

def select_countries(df, column):
    
    def get_3(sorted_entities):
        l = []
        for c in sorted_entities:
            if c not in countries:
                l += [c]
                if len(l) > 2:
                    return l
        
    latest = df[df.Year==df.Year.max()]
    countries = ['Portugal', 'Spain']
    sorted_entities = latest.sort_values(column).Entity.tolist()
    smallest = get_3(sorted_entities)
    largest = get_3(reversed(sorted_entities))
    
    return countries + smallest + largest

color_list = ['red','green',
              '#2346a6','#567fd9','#a2c8ff',
              '#ff7e26','#ff9c59','#ffc99d']
label_dic = {
    'Expectancy':'Life Expectancy (Years)',
    'Retirement':'Retirement Age',
    'Entity':'Country',
    'Sick':'Life Expectancy - HALE (Years)',
    'Retired':'Years spent in Retirement' 
}

# Create output folders if they don't exist
if not exists('images'):
    mkdir('images')
if not exists('plots'):
    mkdir('plot')

# Load retirement tables
retirement_w = read_csv('data/average-effective-retirement-women.csv')
retirement_m = read_csv('data/average-effective-retirement-men.csv')

# Entities without Code are not present in the life expectancy data,
# so it is safe to remove them
retirement_w.dropna(inplace=True)
retirement_m.dropna(inplace=True)

# Merge the two retirement tables and create a column with the average
# of the effective age of retirement from both tables
retirement = merge(retirement_w, retirement_m)
retirement.rename(
    columns={
        'Average effective age of retirement, women (OECD)':'Women',
        'Average effective age of retirement, men (OECD)':'Men'
    }, inplace=True )
retirement['Retirement'] = retirement.loc[:, ('Women','Men')].mean(axis=1)

# Print PT_Retirement plot for presentation intro
fig = px.line(
    retirement.loc[retirement.Entity=='Portugal'],
    x='Year', y=['Men','Women'],
    title='Average effective age of retirement in Portugal',
    labels={'value':'Age (Years)', 'variable':'Sex'}
)
print_fig('PT_Retirement')

# Load life expectancy tables
life_exp = read_csv('data/life-expectancy.csv')
life_exp.rename(
    columns={'Period life expectancy at birth - Sex: total - Age: 0':'Expectancy'},
    inplace=True
)

hale = read_csv('data/healthy-life-expectancy-at-birth.csv')
hale.rename(
    columns={'Healthy life expectancy (HALE) at birth (years) - Sex: both sexes':'HALE'},
    inplace=True
)

# Merge the two life expectancy DFs and creante a column with the life expectancy
# years left after the healthy life expectancy 
life = merge(life_exp, hale)
life['Sick'] = life.Expectancy - life.HALE

# Merge retirement and life expectancy DFs and calculate years in retirement
df = merge(retirement, life_exp)
df['Retired'] = df.Expectancy - df.Retirement

# Create Life Expectancy plot
countries = select_countries(life_exp,'Expectancy')
fig = px.line(
    life_exp.loc[life_exp.Entity.isin(countries)],
    x='Year', y='Expectancy', color='Entity',
    title='Life expectancy over the years',
    labels=label_dic,
    color_discrete_map=dict(zip(countries, color_list))
)
print_fig('LifeExpectancy')

# Create Retirement plot
countries = select_countries(retirement, 'Retirement')
fig = px.line(
    retirement.loc[retirement.Entity.isin(countries)],
    x='Year', y='Retirement', color='Entity',
    title='Effective age of retirement',
    labels=label_dic,
    color_discrete_map=dict(zip(countries, color_list))
)
print_fig('RetirementAge')

# Create HALE and LE plot
fig = px.box(
    life, x='Year', y='Sick',
    title='Years lived not in "full health"',
    labels=label_dic
)
fig.update_xaxes(type='category')
fig.update_layout(width=500, height=600)
print_fig('HALEvsLifeExpectancy', 500, 700)

# Create plot with expected years lived after retirement
fig = px.box(
    df, x='Year', y='Retired',
    title='Average years left after retirement',
    labels=label_dic             
)
print_fig('LifeAfterRetirement')

# Create plot with yars after retiremnt per country
countries = select_countries(df, 'Retired')
fig = px.line(
    df.loc[df.Entity.isin(countries)],
    x='Year', y='Retired', color='Entity',
    title='Life after retirement per country',
    labels=label_dic,
    color_discrete_map=dict(zip(countries, color_list))
)
print_fig('LAR_country')

# Create Retirement vs LE plot
fig = px.scatter(
    df, x='Retired', y='Expectancy', color='Year',
    marginal_x='histogram', marginal_y='histogram',
    title='Years after Retirement vs Life Expectancy',
    labels=label_dic,
    hover_name='Entity'
)
print_fig('Retirement_vs_Expectancy', height=700)

print('\n\U0001f389',
      'All good! Check the images and plot folders to see the figures.',
      '\U0001f389\n')