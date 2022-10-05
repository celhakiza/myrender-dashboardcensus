import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import datetime
import json
import pandas as pd
import pandas_datareader.data as web

#read datasets
#---------------------------------------------------------------------------------------------------
df_pop=pd.read_excel(r'C:\Users\ENVY\Desktop\Data for second dash\Population_distribution.xlsx') #dataset for the population distribution
df_density=pd.read_excel(r'C:\Users\ENVY\Desktop\Data for second dash\Population_density.xlsx') #dataset for population density
df_migration=pd.read_excel(r'C:\Users\ENVY\Desktop\Data for second dash\migration.xlsx') #dataset for migration
df_labor=pd.read_excel(r'C:\Users\ENVY\Desktop\Data for second dash\Labor_force_participation.xlsx',skiprows=1) #dataset for labor participation
df_unem=pd.read_excel(r'C:\Users\ENVY\Desktop\Data for second dash\Unemployment.xlsx') #dataset for unemployment
df_primary=pd.read_excel(r'C:\Users\ENVY\Desktop\Data for second dash\Primary_education.xlsx') #dataset for primary education
df_secondary=pd.read_excel(r'C:\Users\ENVY\Desktop\Data for second dash\Secondary_education.xlsx') #dataset for secondary education
df_toilet=pd.read_excel(r'C:\Users\ENVY\Desktop\Data for second dash\Toilet.xlsx') #dataset for accessing to toilet
df_disability=pd.read_excel(r'C:\Users\ENVY\Desktop\Data for second dash\disability.xlsx') #dataset for disability
df_insurance=pd.read_excel(r'C:\Users\ENVY\Desktop\Data for second dash\medical_insurance.xlsx') #dataset for health insurance
df_lighting=pd.read_excel(r'C:\Users\ENVY\Desktop\Data for second dash\lighting.xlsx') #dataset for lighting

#explore datasets
#instantiate an app
app=dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],
              meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server=app.server
#app layout
#----------------------------------------------------------------------------------------------
app.layout=dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Census Interactive Report by District'),className="text-center text-primary mb-4 font-weight-bold",width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label('Select district to get census information',style={'fontSize':20, 'textAlign':'center'}),
            dcc.Dropdown(id='district-dropdown',
                         value='Bugesera',
                         options=[{'label':x,'value':x} for x in sorted(df_pop['Districts'].unique())]),
            dcc.Graph(id='graph-pop',figure={}),
            html.Div(id='output-sentence')
        ],width={'size':5,'offset':1}),

        dbc.Col([
            html.H2('Internal migration status',style={'fontSize':20, 'textAlign':'center'}),
            html.Div(id='output-migration'),
            dcc.Graph(id='pie-migration',figure={})

        ],width={'size':5,'offset':1})
    ]),

    dbc.Row([
        dbc.Col([
            html.H2('Education Status', style={'fontSize':20,'textAlign':'center'}),
            html.Div(id='out-education'),
            dcc.RadioItems(id='pri-sec-education',
                         value='Primary',
                         options=['Primary','Secondary'],labelClassName='m-3'),
            dcc.Graph(id='graph-education',figure={})
        ],width={'size':5,'offset':1}),

        dbc.Col([
            html.H2('Employment and Unemployment status',style={'fontSize':20,'textAlign':'center'}),
            dcc.RadioItems(id='empl-unemployed',
                           value='labor force participation',
                           options=['Unemployment','labor force participation'],labelClassName='m-3'),
            html.Div(id='out-employment'),
            dcc.Graph(id='graph-empl',figure={})
        ],width={'size':5,'offset':1}),



    ]),

    dbc.Row([
        dbc.Col([
            html.H2('Disability Status',style={'fontSize':20,'textAlign':'center'}),
            html.Div(id='out-disability'),
            dcc.Graph(id='graph-disability',figure={})

        ],width={'size':5,'offset':1}),

        dbc.Col([
            html.H2('Household Characteristics',style={'fontSize':20,'textAlign':'center'}),
            dcc.RadioItems(id='household-ch',
                           value='Lighting source',
                           options=['Lighting source','Toilet type'],labelClassName='m-3'),
            html.Div(id='household-sent'),
            dcc.Graph(id='graph-househ',figure={})
        ],width={'size':5,'offset':1})
    ])

])
@app.callback(
        [Output('graph-pop','figure'),
        Output('output-sentence','children')],
        Input('district-dropdown','value')
)
def update_bar(slctddistrict):
    dff_pop=df_pop[df_pop['Districts']==slctddistrict]
    fig=px.bar(dff_pop,
               x='Districts',
               y=['Female','Male'],
               barmode='group')
    fig.update_layout(xaxis_title='District',yaxis_title='Population',title='Population from 2012 Census for {} district'.format(slctddistrict))
    return (fig,('In {} district, the total population from 2012 Rwanda Population and housing census (RPHC4) is {},\n'
                 ' the female population is {} \n'
                 'and male population is {}.'.format(slctddistrict,dff_pop[df_pop['Districts']==slctddistrict].squeeze()[3],df_pop[df_pop['Districts']==slctddistrict].squeeze()[5],df_pop[df_pop['Districts']==slctddistrict].squeeze()[4])))

@app.callback(
        [Output('output-migration','children'),
         Output('pie-migration','figure')],
         Input('district-dropdown','value')
)
def update_migration(slctddistrict):
    dff_migration = df_migration[df_migration['Districts'] == slctddistrict]

    fig=px.bar(dff_migration,
               x='Districts',
               y=['Number of in-migrants','Number of out-migrants','Net Migration'],
               barmode='group')
    fig.update_layout(xaxis_title='District',yaxis_title='Migration',title='Migration status for {} district from 2012 census'.format(slctddistrict))
    return ('In {} district located in {} province, the In-migration, people who came to live there in five years preceding\n'
            ' the census is {}, the Out-migration, people who left the district five years preceding the census is {}. the net migration which \n'
            'is the difference between In-migration and Out-migration is {}.'.format(slctddistrict,df_migration[df_migration['Districts'] == slctddistrict].squeeze()[0],df_migration[df_migration['Districts'] == slctddistrict].squeeze()[3],df_migration[df_migration['Districts'] == slctddistrict].squeeze()[4],df_migration[df_migration['Districts'] == slctddistrict].squeeze()[5]),fig)
@app.callback(
        [Output('graph-education','figure'),
         Output('out-education','children')],
         [Input('pri-sec-education','value'),
         Input('district-dropdown','value')]
)
def education_update(educat,slctddistrict):
    if educat=="Primary":
        dff_pr=df_primary[df_primary['Districts']==slctddistrict]
        fig=px.bar(dff_pr,
                   x='Districts',
                   y=['Both sexes','Female','Male'],
                   barmode='group')
        fig.update_layout(xaxis_title='District',yaxis_title='Primary Education',title='Primary education status for {} district'.format(slctddistrict))
        return (fig,'In {} district, {} percent of children between\n'
                    ' 7-12 years enrolled in primary education, female are {}\n'
                    ' percent while male are {} percent.'.format(slctddistrict,df_primary[df_primary['Districts']==slctddistrict].squeeze()[2],df_primary[df_primary['Districts']==slctddistrict].squeeze()[4],df_primary[df_primary['Districts']==slctddistrict].squeeze()[3]))
    elif educat=="Secondary":
        dff_Sec=df_secondary[df_secondary['Districts']==slctddistrict]
        fig = px.bar(dff_Sec,
                     x='Districts',
                     y=['Both sexes', 'Female', 'Male'],
                     barmode='group')
        fig.update_layout(xaxis_title='District', yaxis_title='Primary Education',
                          title='Secondary education status for {} district'.format(slctddistrict))
        return (fig,'In {} district, {} percent of children between\n'
                    ' 13-18 years enrolled in secondary education, female are {}\n'
                    ' percent while male are {} percent'.format(slctddistrict,df_secondary[df_secondary['Districts']==slctddistrict].squeeze()[2],df_secondary[df_secondary['Districts']==slctddistrict].squeeze()[4],df_secondary[df_secondary['Districts']==slctddistrict].squeeze()[3]))
@app.callback(
        [Output('graph-empl','figure'),
         Output('out-employment','children')],
         [Input('empl-unemployed','value'),
          Input('district-dropdown','value')]
)
def employment(employ,slctddistrict):
    if employ=='Unemployment':
        dff_unemp=df_unem[df_unem['Districts']==slctddistrict]
        fig=px.bar(dff_unemp,
                   x='Districts',
                   y=['Both sexes','Male','Female'],
                   barmode='group')
        fig.update_layout(xaxis_title='District',yaxis_title='Unemployment rate',title='Unemployment Status {} district'.format(slctddistrict))
        return (fig,'In {} district, the unemployment rate from 2012 census is {} percent, female unemployment rate is {} percent, and male unemployment rate is {} percent.'.format(slctddistrict,df_unem[df_unem['Districts']==slctddistrict].squeeze()[2],df_unem[df_unem['Districts']==slctddistrict].squeeze()[4],df_unem[df_unem['Districts']==slctddistrict].squeeze()[3]))
    elif employ=='labor force participation':
        dff_labor=df_labor[df_labor['Districts']==slctddistrict]
        fig=px.bar(dff_labor,
                   x='Districts',
                   y=['Both sexes','Male','Female'],
                   barmode='group')
        fig.update_layout(xaxis_title='District',yaxis_title='Labor force participation rate',title='Labor force participation for {} district'.format(slctddistrict))
        return (fig,'In {} district, labor force participation rate from 2012 census is {} percent, female labor force participation rate is {} percent, and male labor force participation rate is {} percent.'.format(slctddistrict,df_labor[df_labor['Districts']==slctddistrict].squeeze()[2],df_labor[df_labor['Districts']==slctddistrict].squeeze()[4],df_labor[df_labor['Districts']==slctddistrict].squeeze()[3]))
@app.callback(
        [Output('graph-disability','figure'),
         Output('out-disability','children')],
         Input('district-dropdown','value')

)
def disability(slctddistrict):
    dff_dis=df_disability[df_disability['Districts']==slctddistrict]
    fig=px.bar(dff_dis,
               x='Districts',
               y=['Both sexes','Female','Male'],
               barmode='group')
    fig.update_layout(xaxis_title='District',yaxis_title='Number of people with disability',title='Disability status for {} district'.format(slctddistrict))
    return (fig,'In {} district, total population with disability is {}, Female population with disability is {} and Male population with disability is {}'.format(slctddistrict,df_disability[df_disability['Districts']==slctddistrict].squeeze()[2],df_disability[df_disability['Districts']==slctddistrict].squeeze()[4],df_disability[df_disability['Districts']==slctddistrict].squeeze()[3]))
@app.callback(
        [Output('household-sent','children'),
         Output('graph-househ','figure')],
         [Input('household-ch','value'),
          Input('district-dropdown','value')]
)
def household(char,slctddistrict):
    if char=='Lighting source':
        dff_lig=df_lighting[df_lighting['Districts']==slctddistrict]
        fig=px.bar(dff_lig,
                   x=['Electricity by EWSA','Other electricity source','Kero-sene lamp','Paraffin','Biogas','Candle','Fire-wood','Other','Not Stated'],
                   y='Districts',
                   barmode='group',
                   orientation='h')
        fig.update_layout(xaxis_title='Percentage',yaxis_title='district', title='Source of lighting for {} district'.format(slctddistrict))
        return ('the graph shows the main source of lighting from 2012 Rwanda Population and Housing Census in {}'.format(slctddistrict),fig)
    elif char=='Toilet type':
        dff_toil=df_toilet[df_toilet['Districts']==slctddistrict]
        fig = px.bar(dff_toil,
                     x=['Flush Toilet/ WC system', 'Private pit latrine', 'Shared pit latrine', 'Bush', 'Other','Not Stated'],
                     y='Districts',
                     barmode='group',
                     orientation='h')
        fig.update_layout(xaxis_title='Percentage', yaxis_title='district',title='Type of toilet for {} district'.format(slctddistrict))
        return ('the graph shows the type of toilet from 2012 Rwanda Population and Housing Census in {} district'.format(slctddistrict),fig)



app.run_server(debug=True)



# dff_lig=df_lighting[df_lighting['Districts']=='Gakenke'].squeeze()
# df_result_pie = pd.DataFrame(dff_lig)
# #df_result_pie['index'] = range(len(df_result_pie))
# #print(df_result_pie.columns)
# df_result_pie.rename(columns={'19':'Source of lighting'},inplace=True)
# print(df_result_pie.columns)
# #df_result_pie.columns=[['Source of lighting','percentage']]
# #print(df_result_pie)
# #print(df_result_pie.values)
# #print(df_result_pie.head())