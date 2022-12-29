import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import datetime
import json
import pandas as pd
import plotly.graph_objs as go
#import pandas_datareader.data as web

#read datasets
#---------------------------------------------------------------------------------------------------
df_pop=pd.read_excel(r'C:\Users\ENVY\PycharmProjects\mydashboard\Data fro census dashboard\Pop_distribution.xlsx') #dataset for the population distribution
df_density=pd.read_excel(r'C:\Users\ENVY\PycharmProjects\mydashboard\assets\Population_density.xlsx') #dataset for population density
df_migration=pd.read_excel(r'C:\Users\ENVY\PycharmProjects\mydashboard\assets\migration.xlsx') #dataset for migration
df_labor=pd.read_excel(r'C:\Users\ENVY\PycharmProjects\mydashboard\Data fro census dashboard\LFS_Participation.xlsx') #dataset for labor participation
df_unem=pd.read_excel(r'C:\Users\ENVY\PycharmProjects\mydashboard\Data fro census dashboard\LFS_unempl.xlsx') #dataset for unemployment
df_primary=pd.read_excel(r'C:\Users\ENVY\PycharmProjects\mydashboard\Data fro census dashboard\primary_education_1.xlsx') #dataset for primary education
df_secondary=pd.read_excel(r'C:\Users\ENVY\PycharmProjects\mydashboard\Data fro census dashboard\secondary_education_1.xlsx') #dataset for secondary education
df_toilet=pd.read_excel(r'C:\Users\ENVY\PycharmProjects\mydashboard\Data fro census dashboard\toilet_type.xlsx') #dataset for accessing to toilet
df_disability=pd.read_excel(r'C:\Users\ENVY\PycharmProjects\mydashboard\Data fro census dashboard\disability_1.xlsx') #dataset for disability
df_insurance=pd.read_excel(r'C:\Users\ENVY\PycharmProjects\mydashboard\assets\medical_insurance.xlsx') #dataset for health insurance
df_lighting=pd.read_excel(r'C:\Users\ENVY\PycharmProjects\mydashboard\Data fro census dashboard\lighting_1.xlsx') #dataset for lighting
df_density_1=pd.read_excel(r'C:\Users\ENVY\PycharmProjects\mydashboard\assets\Population_density.xlsx') #dataset for population density
df_pop_distr=pd.read_excel(r'C:\Users\ENVY\PycharmProjects\mydashboard\assets\population_distr_.xlsx') #dataset for population distribution
df_pop_residence=pd.read_excel(r'C:\Users\ENVY\PycharmProjects\mydashboard\Data fro census dashboard\Pop_res.xlsx') #dataset for pop residence
df_pop_registration=pd.read_excel(r'C:\Users\ENVY\PycharmProjects\mydashboard\Data fro census dashboard\birth_registration_0_17.xlsx') #dataset for birth registration
df_pop_habitant=pd.read_excel(r'C:\Users\ENVY\PycharmProjects\mydashboard\Data fro census dashboard\type_habitant.xlsx') #dataset for type habitants
df_pop_internet=pd.read_excel(r'C:\Users\ENVY\PycharmProjects\mydashboard\Data fro census dashboard\internet_access.xlsx') #dataset internet
df_age_group=pd.read_excel(r'C:\Users\ENVY\PycharmProjects\mydashboard\Data fro census dashboard\Sex_age_group_1.xlsx')
df_age_group_urban=pd.read_excel(r'C:\Users\ENVY\PycharmProjects\mydashboard\Data fro census dashboard\Sex_age_group_urban.xlsx')
df_age_group_rural=pd.read_excel(r'C:\Users\ENVY\PycharmProjects\mydashboard\Data fro census dashboard\Sex_age_group_rural.xlsx')
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
        dbc.Col(html.H1('Census Interactive Report'),className="text-center text-primary mb-4 font-weight-bold",width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.P('From 2022 Rwanda Population and Housing Census, the total population were 13,244,754, \n'
                   'Female Population were 6,816,715 and Male Population were 6,428,039. Population in Rural area were 9,413,396, \n'
                   'represents 71.1 percent and Population in Urban area were 3,831,358, represents 28.9 percent.')
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='age_pyramid',
                value='Rwanda',
                options=['Rwanda','Rural','Urban']),
            dcc.Graph(id='graph-pyramid',figure={})
        ])
    ]),

    dbc.Row([
        dbc.Col([
            html.Label('Population Distribution by Province',className="text-center text-primary mb-4 font-weight-bold"),
            dcc.Dropdown(id='province',
                         value='City of Kigali',
                         options=[{'label':x,'value':x} for x in df_pop[1:]['Provinces'].unique()]),
            html.Div(id='province-sent')
            #dcc.Graph(id='province-graph',figure={})
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='province-graph',figure={})
        ],width=4),
        dbc.Col([
            dcc.Graph(id='province-res',figure={})
        ],width={'size':5,'offset':1})

    ]),
    dbc.Col(
        html.H4('Districts Report'),className="text-center text-primary mb-4 font-weight-bold",width=12),

    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.Label('Select district to get census information',style={'fontSize':20, 'textAlign':'center'},className="text-center text-primary mb-4 font-weight-bold"),
            dcc.Dropdown(id='district-dropdown',
                         value='Bugesera',
                         options=[{'label':x,'value':x} for x in sorted(df_pop['Districts'].unique())]),
            dcc.Graph(id='graph-pop',figure={}),
            html.Div(id='output-sentence')
        ],width={'size':5,'offset':1}),

        dbc.Col([
            html.H2('Birth registration',style={'fontSize':20, 'textAlign':'center'},className="text-center text-primary mb-4 font-weight-bold"),
            html.Div(id='output-registration'),
            dcc.Graph(id='graph-registration',figure={})

        ],width={'size':5,'offset':1}),
        html.Hr(),
    ]),
    dbc.Row([
        dbc.Col([
            html.H2('Education Status', style={'fontSize':20,'textAlign':'center'},className="text-center text-primary mb-4 font-weight-bold"),
            html.Div(id='out-education'),
            dcc.RadioItems(id='pri-sec-education',
                         value='Primary',
                         options=['Primary','Secondary'],labelClassName='m-3'),
            dcc.Graph(id='graph-education',figure={})
        ],width={'size':5,'offset':1}),
        dbc.Col([
            html.H2('Employment and Unemployment status',style={'fontSize':20,'textAlign':'center'},className="text-center text-primary mb-4 font-weight-bold"),
            dcc.RadioItems(id='empl-unemployed',
                           value='labor force participation',
                           options=['Unemployment','labor force participation'],labelClassName='m-3'),
            html.Div(id='out-employment'),
            dcc.Graph(id='graph-empl',figure={})
        ],width={'size':5,'offset':1}),
        html.Hr(),
    ]),
    dbc.Row([
        dbc.Col([
            html.H2('Disability Status',style={'fontSize':20,'textAlign':'center'},className="text-center text-primary mb-4 font-weight-bold"),
            html.Div(id='out-disability'),
            dcc.Graph(id='graph-disability',figure={})
        ],width={'size':5,'offset':1}),
        dbc.Col([
            html.H2('Household Characteristics',style={'fontSize':20,'textAlign':'center'},className="text-center text-primary mb-4 font-weight-bold"),
            dcc.RadioItems(id='household-ch',
                           value='Lighting source',
                           options=['Lighting source','Toilet type'],labelClassName='m-3'),
            html.Div(id='household-sent'),
            dcc.Graph(id='graph-househ',figure={})
        ],width={'size':5,'offset':1}),
        html.Hr()
    ]),
    dbc.Row([
        dbc.Col([
            html.H2('Habitants Status',style={'fontSize':20,'textAlign':'center'},className="text-center text-primary mb-4 font-weight-bold"),
            dcc.Graph(id='graph-habit',figure={}),
            html.Div(id='habit-sent'),
        ],width={'size':5,'offset':1}),

        dbc.Col([
            html.H2('Internet Access',style={'fontSize':20,'textAlign':'center'},className="text-center text-primary mb-4 font-weight-bold"),
            dcc.Graph(id='graph-internet',figure={}),
            html.Div(id='internet-sent'),
        ],width={'size':5,'offset':1})
    ])
])
@app.callback(
        Output('graph-pyramid','figure'),
        Input('age_pyramid','value'))
def pop_pyramid(slct_input):
    if slct_input=="Rwanda":
        y_age = df_age_group['age_cat']
        x_Male = df_age_group['Male']
        x_Female = df_age_group['Female'] * -1

        # instantiate figure
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=y_age,
            x=x_Male,
            name='Male',
            orientation='h'
        ))
        fig.add_trace(go.Bar(
            y=y_age,
            x=x_Female,
            name='Female',
            orientation='h'
        ))

        fig.update_layout(
            template='plotly_white',
            title='Rwanda Census Population Pyramid',
            title_font_size=24,
            barmode='relative',
            bargap=0.0,
            bargroupgap=0,
            plot_bgcolor='white',
            xaxis=dict(
                tickvals=[-800000, -600000, -400000, -200000, 0, 200000, 400000, 600000, 800000],
                ticktext=['800k', '600k', '400k', '200k', 0, '200k', '400k', '600k', '800k'],
                title='Population in Thousands'
            )
        )
        return fig

    elif slct_input=="Urban":
        y_age = df_age_group_urban['age_cat']
        x_Male = df_age_group_urban['Male']
        x_Female = df_age_group_urban['Female'] * -1

        # instantiate figure
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=y_age,
            x=x_Male,
            name='Male',
            orientation='h'
        ))
        fig.add_trace(go.Bar(
            y=y_age,
            x=x_Female,
            name='Female',
            orientation='h'
        ))

        fig.update_layout(
            template='plotly_white',
            title='Urban Census Population Pyramid',
            title_font_size=24,
            barmode='relative',
            bargap=0.0,
            bargroupgap=0,
            plot_bgcolor='white',
            xaxis=dict(
                tickvals=[-200000, -100000, 0, 100000, 200000],
                ticktext=['200k', '100k', 0, '100k', '200k'],
                title='Population in Thousands'
            )
        )

        return fig

    elif slct_input=="Rural":
        y_age = df_age_group_rural['age_cat']
        x_Male = df_age_group_rural['Male']
        x_Female = df_age_group_rural['Female'] * -1

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=y_age,
            x=x_Male,
            name='Male',
            orientation='h'
        ))
        fig.add_trace(go.Bar(
            y=y_age,
            x=x_Female,
            name='Female',
            orientation='h'
        ))

        fig.update_layout(
            template='plotly_white',
            title='Rural Census Population Pyramid',
            title_font_size=24,
            barmode='relative',
            bargap=0.0,
            bargroupgap=0,
            plot_bgcolor='white',
            xaxis=dict(
                tickvals=[-600000, -400000, -200000, 0, 200000, 400000, 600000],
                ticktext=['600k', '400k', '200k', 0, '200k', '400k', '600k'],
                title='Population in Thousands'
            )
        )
        return fig

@app.callback(
    [Output('province-sent','children'),
    Output('province-graph','figure')],
    #Input('rural-urban','value'),
     Input('province','value')
)
def update_province(slctprovince):
    #dff_distr=df_pop_distr[df_pop_distr['Provinces']==slctprovince]
    #dff_resid=df_pop_residence[df_pop_residence['Provinces']==slctprovince]
    dff_distr=df_pop[df_pop['Provinces'] == slctprovince].sum().squeeze()[3:5]
    #convert series to dataframes
    dff_distr_df=pd.DataFrame(dff_distr)
    # reset index of a dataframe
    dff_distr_df=dff_distr_df.reset_index()
    #rename the columns of dataframe
    dff_distr_df=dff_distr_df.rename(columns={'index': 'Gender', 0: 'Totals'})
    fig=px.pie(dff_distr_df,
               values='Totals',
               names='Gender',
               hole=0.4, title='Population by sex in {}'.format(slctprovince))
    fig.update_traces(textinfo='percent+label',showlegend=False,hoverinfo='label+percent')
    #fig.update_layout(xaxis_title='Districts',yaxis_title='Total Population',title='Population by sex in {} province'.format(slctprovince))
    return ('In {}, the total population from 2022 Rwanda Population and Housing Census \n'
                'was {}, the female was {} and male was {}. People in Rural area was {} \n'
                '. People in urban area was {}.'.format(slctprovince,df_pop[df_pop['Provinces']==slctprovince].sum().squeeze()[2],df_pop[df_pop['Provinces']==slctprovince].sum().squeeze()[4],df_pop[df_pop['Provinces']==slctprovince].sum().squeeze()[3],df_pop_residence[df_pop_residence['Provinces']==slctprovince].sum().squeeze()[4],df_pop_residence[df_pop_residence['Provinces']==slctprovince].sum().squeeze()[3]),fig)

@app.callback(
        Output('province-res','figure'),
        Input('province','value')
)
def update_graph(slctprovince):
    #dff_resid = df_pop_residence[df_pop_residence['Provinces'] == slctprovince]
    dff_resid_df = df_pop_residence[df_pop_residence['Provinces'] == slctprovince].sum().squeeze()[3:5]
    # convert series into dataframe
    dff_residence_df = pd.DataFrame(dff_resid_df)
    # reset index
    dff_residence_df = dff_residence_df.reset_index()
    # rename columns
    dff_residence_df = dff_residence_df.rename(columns={'index': 'residence', 0: 'Totals'})

    fig=px.pie(dff_residence_df,values='Totals',
               names='residence',
               title='Population by area of residence in {}'.format(slctprovince),
               hole=0.4,
               color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_traces(textinfo='percent+label', showlegend=False,hoverinfo='percent+label')
    return fig

@app.callback(
        [Output('output-sentence','children'),
         Output('graph-pop','figure')],
         Input('district-dropdown','value')
)
def update_bar(slctddistrict):
    # create a subset for each district from dataset
    dff_pop = df_pop[df_pop['Districts']==slctddistrict].sum().squeeze()[3:5]
    # convert series into a dataframe
    dff_pop = pd.DataFrame(dff_pop)
    # reset index of a dataframe
    dff_pop = dff_pop.reset_index()
    # rename the columns of a dataframe
    dff_pop = dff_pop.rename(columns={'index':'Sex', 0:'Population'})
    #make a bar chart from the created dataframe
    fig=px.bar(dff_pop,
               x='Sex',
               y='Population',
               color='Sex',
               text='Population')
    fig.update_layout(xaxis_title='Sex',yaxis_title='Population in Thousands',title='Population from 2022 Census for {} district'.format(slctddistrict)),
    fig.update_layout(
                    title_font_color='blue',
                    font_color='blue',
                    font_family='Times New Roman',
                    legend_title_font_color='green',
                    title_font_family='Arial',
                    autotypenumbers='strict',
                    showlegend=False,
                    plot_bgcolor='white')
    return (('In {} district, the total population from 2022 Rwanda Population and housing census (RPHC5) is {},\n'
                 ' the female population is {} \n'
                 'and male population is {}.'.format(slctddistrict,df_pop[df_pop['Districts']==slctddistrict].squeeze()[2],df_pop[df_pop['Districts']==slctddistrict].squeeze()[4],df_pop[df_pop['Districts']==slctddistrict].squeeze()[3])),fig)

@app.callback(
        [Output('output-registration','children'),
         Output('graph-registration','figure')],
         Input('district-dropdown','value')
)
def update_registration(slctddistrict):
    dff_reg = df_pop_registration[df_pop_registration['Districts'] == slctddistrict].sum().squeeze()[2:]
    # convert series into Dataframe
    dff_reg = pd.DataFrame(dff_reg)
    # reset index to allow renaming the columns
    dff_reg = dff_reg.reset_index()
    # rename columns
    dff_reg = dff_reg.rename(columns={'index': 'Gender', 0: 'Percentage of children registered'})
    fig = px.bar(dff_reg,
                 x='Gender',
                 y='Percentage of children registered',
                 text='Percentage of children registered',
                 color='Gender')
    fig.update_layout(xaxis_title='Gender',yaxis_title='Percentage of people registered',title='Birth registration status for {} district from 2022 census'.format(slctddistrict)),
    fig.update_layout(
        title_font_color='blue',
        font_color='blue',
        font_family='Times New Roman',
        legend_title_font_color='green',
        title_font_family='Arial',
        showlegend=False,
        plot_bgcolor='white'
    )
    return ('In {} district located in {}, the registration for people under 17 is {} percent, male registration is {} percent\n'
            'Female registration is {} percent'.format(slctddistrict,df_pop_registration[df_pop_registration['Districts'] == slctddistrict].squeeze()[0],df_pop_registration[df_pop_registration['Districts'] == slctddistrict].squeeze()[2],df_pop_registration[df_pop_registration['Districts'] == slctddistrict].squeeze()[3],df_pop_registration[df_pop_registration['Districts'] == slctddistrict].squeeze()[4]),fig)
@app.callback(
        [Output('graph-education','figure'),
         Output('out-education','children')],
         [Input('pri-sec-education','value'),
         Input('district-dropdown','value')]
)
def education_update(educat,slctddistrict):
    if educat=="Primary":
        dff_ed = df_primary[df_primary['Districts'] == slctddistrict].sum().squeeze()[2:]
        # convert series into Dataframe
        dff_ed = pd.DataFrame(dff_ed)
        # reset index to allow renaming the columns
        dff_ed = dff_ed.reset_index()
        # rename columns
        dff_ed = dff_ed.rename(columns={'index': 'Gender', 0: 'Percentage of children at primary school'})
        fig = px.bar(dff_ed,
                     x='Gender',
                     y='Percentage of children at primary school',
                     text='Percentage of children at primary school',
                     color='Gender')
        fig.update_layout(xaxis_title='Gender',yaxis_title='Primary Education',title='Primary education status for {} district from 2022 census '.format(slctddistrict)),
        fig.update_layout(
            title_font_color='blue',
            font_color='blue',
            font_family='Times New Roman',
            legend_title_font_color='green',
            title_font_family='Arial',
            showlegend=False,
            plot_bgcolor='white'
        )
        return (fig,'In {} district, {} percent of children between\n'
                    ' 7-12 years enrolled in primary education, female are {}\n'
                    ' percent while male are {} percent.'.format(slctddistrict,df_primary[df_primary['Districts']==slctddistrict].squeeze()[2],df_primary[df_primary['Districts']==slctddistrict].squeeze()[4],df_primary[df_primary['Districts']==slctddistrict].squeeze()[3]))
    elif educat=="Secondary":
        dff_ed_sec = df_secondary[df_secondary['Districts'] == slctddistrict].sum().squeeze()[2:]
        # convert series into Dataframe
        dff_ed_sec = pd.DataFrame(dff_ed_sec)
        # reset index to allow renaming the columns
        dff_ed_sec = dff_ed_sec.reset_index()
        # rename columns
        dff_ed_sec = dff_ed_sec.rename(columns={'index': 'Gender', 0: 'Percentage of children at secondary school'})
        fig = px.bar(dff_ed_sec,
                     x='Gender',
                     y='Percentage of children at secondary school',
                     text='Percentage of children at secondary school',
                     color='Gender')
        fig.update_layout(xaxis_title='Gender', yaxis_title='Percentage of children at secondary school',
                          title='Secondary education status for {} district from 2022 census '.format(slctddistrict)),
        fig.update_layout(
            title_font_color='blue',
            font_color='blue',
            font_family='Times New Roman',
            legend_title_font_color='green',
            title_font_family='Arial',
            showlegend=False,
            plot_bgcolor='white'
        )
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
        dff_unemp = df_unem[df_unem['Districts'] == slctddistrict].sum().squeeze()[2:]
        # convert series into Dataframe
        dff_unemp = pd.DataFrame(dff_unemp)
        # reset index to allow renaming the columns
        dff_unemp = dff_unemp.reset_index()
        # rename columns
        dff_unemp = dff_unemp.rename(columns={'index': 'Gender', 0: 'Percentage of unemployed'})

        fig = px.bar(dff_unemp,
                     x='Gender',
                     y='Percentage of unemployed',
                     text='Percentage of unemployed',
                     color='Gender')
        fig.update_layout(xaxis_title='Gender',yaxis_title='Unemployment rate',title='Unemployment Status {} district from 2022 census '.format(slctddistrict)),
        fig.update_layout(
            title_font_color='blue',
            font_color='blue',
            font_family='Times New Roman',
            legend_title_font_color='green',
            title_font_family='Arial',
            showlegend=False,
            plot_bgcolor='white'
        )
        return (fig,'In {} district, the unemployment rate from 2022 census is {} percent, female unemployment rate is {} percent, and male unemployment rate is {} percent.'.format(slctddistrict,df_unem[df_unem['Districts']==slctddistrict].squeeze()[2],df_unem[df_unem['Districts']==slctddistrict].squeeze()[4],df_unem[df_unem['Districts']==slctddistrict].squeeze()[3]))
    elif employ=='labor force participation':
        dff_labor = df_labor[df_labor['Districts'] == slctddistrict].sum().squeeze()[2:]
        # convert series into Dataframe
        dff_labor = pd.DataFrame(dff_labor)
        # reset index to allow renaming the columns
        dff_labor = dff_labor.reset_index()
        # rename columns
        dff_labor = dff_labor.rename(columns={'index': 'Gender', 0: 'Labor force participation rate'})
        fig = px.bar(dff_labor,
                     x='Gender',
                     y='Labor force participation rate',
                     text='Labor force participation rate',
                     color='Gender')
        fig.update_layout(xaxis_title='Gender',yaxis_title='Labor force participation rate',title='Labor force participation for {} district from 2022 census '.format(slctddistrict)),
        fig.update_layout(
            title_font_color='blue',
            font_color='blue',
            font_family='Times New Roman',
            legend_title_font_color='green',
            title_font_family='Arial',
            showlegend=False,
            plot_bgcolor='white'
        )
        return (fig,'In {} district, labor force participation rate from 2022 census is {} percent, female labor force participation rate is {} percent, and male labor force participation rate is {} percent.'.format(slctddistrict,df_labor[df_labor['Districts']==slctddistrict].squeeze()[2],df_labor[df_labor['Districts']==slctddistrict].squeeze()[4],df_labor[df_labor['Districts']==slctddistrict].squeeze()[3]))
@app.callback(
        [Output('graph-disability','figure'),
         Output('out-disability','children')],
         Input('district-dropdown','value')

)
def disability(slctddistrict):
    # select subset from the dataset and convert into series
    dff_disab = df_disability[df_disability['Districts'] ==slctddistrict].sum().squeeze()[2:]
    # convert series into Dataframe
    dff_disab = pd.DataFrame(dff_disab)
    # reset index to allow renaming the columns
    dff_disab = dff_disab.reset_index()
    # rename columns
    dff_disab = dff_disab.rename(columns={'index': 'Gender', 0: 'Number of persons with disability'})
    fig = px.bar(dff_disab,
                 x='Gender',
                 y='Number of persons with disability',
                 text='Number of persons with disability',
                 color='Gender')
    fig.update_layout(xaxis_title='Gender',yaxis_title='Number of people with disability',title='Disability status for {} district from 2022 census '.format(slctddistrict)),
    fig.update_layout(
        title_font_color='blue',
        font_color='blue',
        font_family='Times New Roman',
        legend_title_font_color='green',
        title_font_family='Arial',
        showlegend=False,
        plot_bgcolor='white'
    )
    return (fig,'In {} district, total population with disability is {} from 2022 RPHC5, Female population with disability is {} and Male population with disability is {}'.format(slctddistrict,df_disability[df_disability['Districts']==slctddistrict].squeeze()[2],df_disability[df_disability['Districts']==slctddistrict].squeeze()[4],df_disability[df_disability['Districts']==slctddistrict].squeeze()[3]))
@app.callback(
        [Output('household-sent','children'),
         Output('graph-househ','figure')],
         [Input('household-ch','value'),
          Input('district-dropdown','value')]
)
def household(char,slctddistrict):
    if char=='Lighting source':
        dff_light = df_lighting[df_lighting['Districts'] == slctddistrict].sum().squeeze()[3:]
        # convert series into a dataframe
        dff_light = pd.DataFrame(dff_light)
        # reset index
        dff_light = dff_light.reset_index()
        # rename columns
        dff_light = dff_light.rename(columns={'index': 'Lighting type', 0: 'percentage'})

        fig = px.bar(dff_light,
                     x='Lighting type',
                     y='percentage',
                     text='percentage')
        fig.update_layout(xaxis_title='Source type',yaxis_title='Percentage in %', title='Source of lighting for {} district from 2022 census '.format(slctddistrict)),
        fig.update_traces(showlegend=False),
        fig.update_layout(
            title_font_color='blue',
            font_color='blue',
            font_family='Times New Roman',
            legend_title_font_color='green',
            title_font_family='Arial',
            plot_bgcolor='white'
        )
        return ('the graph shows the main source of lighting from 2022 Rwanda Population and Housing Census in {}'.format(slctddistrict),fig)
    elif char=='Toilet type':
        dff_toil=df_toilet[df_toilet['Districts']==slctddistrict]
        fig = px.bar(dff_toil,
                     x=['Flush Toilet/ WC system', 'Private Pit Latrine', 'Shared Pit Latrine', 'Bush', 'Other','Not Stated'],
                     y='Districts',
                     barmode='group',
                     orientation='h')
        fig.update_layout(xaxis_title='Percentage', yaxis_title='district',title='Type of toilet for {} district from 2022 census'.format(slctddistrict)),
        fig.update_traces(showlegend=False),
        fig.update_layout(
            title_font_color='blue',
            font_color='blue',
            font_family='Times New Roman',
            legend_title_font_color='green',
            title_font_family='Arial',
            plot_bgcolor='white'
        )
        return ('the graph shows the type of toilet from 2022 Rwanda Population and Housing Census in {} district'.format(slctddistrict),fig)

@app.callback(
    [Output('graph-habit','figure'),
     Output('habit-sent','children')],
     Input('district-dropdown','value'))

def update_habitant(slctddistrict):
    # select a subset for any district
    dff_habit = df_pop_habitant[df_pop_habitant['Districts'] ==slctddistrict].sum().squeeze()[3:]
    # convert a series into dataframe
    dff_habit = pd.DataFrame(dff_habit)
    # reset index to allows renaming
    dff_habit = dff_habit.reset_index()
    # rename columns
    dff_habit = dff_habit.rename(columns={'index': 'Type of habitants', 0: 'percentage'})
    fig = px.bar(dff_habit,
                 x='Type of habitants',
                 y='percentage',
                 text='percentage')
    fig.update_layout(xaxis_title='Type of habitants',yaxis_title='Percentage in %',title='type of habitant in {} district from 2022 census'.format(slctddistrict)),
    fig.update_traces(showlegend=False),
    fig.update_layout(
        title_font_color='blue',
        font_color='blue',
        font_family='Times New Roman',
        legend_title_font_color='green',
        title_font_family='Arial',
        plot_bgcolor='white'
    )
    return (fig,'this is the different type of habitants in {} district from Rwanda Population and Housing census 2022'.format(slctddistrict))

@app.callback(
     [Output('graph-internet','figure'),
      Output('internet-sent','children')],
      Input('district-dropdown','value'))

def update_internet(slctddistrict):
    # select subset from the dataset and convert into series
    dff_internet = df_pop_internet[df_pop_internet['Districts'] ==slctddistrict].sum().squeeze()[2:]
    # convert series into Dataframe
    dff_internet = pd.DataFrame(dff_internet)
    # reset index to allow renaming the columns
    dff_internet = dff_internet.reset_index()
    # rename columns
    dff_internet = dff_internet.rename(columns={'index': 'Gender', 0: 'Percentage of access to internet'})
    fig = px.bar(dff_internet,
                 x='Gender',
                 y='Percentage of access to internet',
                 text='Percentage of access to internet',
                 color='Gender')
    fig.update_layout(xaxis_title='Gender',yaxis_title='Percentage of access to internet', title='Internet access in {} district from 2022 census'.format(slctddistrict)),
    fig.update_traces(showlegend=False),
    fig.update_layout(
        title_font_color='blue',
        font_color='blue',
        font_family='Times New Roman',
        legend_title_font_color='green',
        title_font_family='Arial',
        #legend_groupclick='toggleitem',
        legend_itemclick="toggleothers",
        legend_bgcolor='orange',
        #paper_bgcolor='black'# st the background color where the graph is drawn
        plot_bgcolor='white'
    )
    return (fig,'In {} district, the percentage of people who are 10 years and above that have access to internet is {} percent, male is {} percent, female is {} percent'.format(slctddistrict,df_pop_internet[df_pop_internet['Districts']==slctddistrict].squeeze()[2],df_pop_internet[df_pop_internet['Districts']==slctddistrict].squeeze()[3],df_pop_internet[df_pop_internet['Districts']==slctddistrict].squeeze()[4]))


app.run_server(debug=True,port=3000)










dff_dis_pie=df_pop_distr[df_pop_distr['Provinces']=='Kigali City'].sum().squeeze()[3:5]
#convert series into dataframe
dff_dis_df=pd.DataFrame(dff_dis_pie)
#reset index of a dataframe
dff_dis_df=dff_dis_df.reset_index()
#rename columns of a series
dff_dis_df=dff_dis_df.rename(columns={'index':'Gender',0:'Totals'})
fig=px.pie(dff_dis_df,values='Totals',names='Gender',title='Population by sex',
           hole=0.3)
#print(dff_dis_df)
# #fig.show()
# dff_pop_df=df_pop[df_pop['Districts']=='Nyamasheke'].squeeze()
# dff_pop_dff=pd.DataFrame(dff_pop_df)
# dff_pop_dff=dff_pop_dff.reset_index()
# print(dff_pop_dff)
# dff_resid_df=df_pop_residence[df_pop_residence['Provinces']=='East'].sum().squeeze()[3:5]
# #convert series into datafram
# dff_residence_df=pd.DataFrame(dff_resid_df)
# #reset index
# dff_residence_df=dff_residence_df.reset_index()
# #rename columns
# dff_residence_df=dff_residence_df.rename(columns={'index':'residence',0:'Totals'})
#print(dff_residence_df)

#dff_habitants=df_pop_habitant[df_pop_habitant['Districts']==' Rwamagana']
#print(dff_habitants)
#df_hab=df_pop_habitant[df_pop_habitant['Districts']=='Nyamagabe'].squeeze()

# #print(dff_habitants.head())
# dff_pop=df_pop[df_pop['Provinces']=='City of Kigali'].sum().squeeze()[3:5]
#
# dff_pop=pd.DataFrame(dff_pop)
# dff_pop=dff_pop.reset_index()
# dff_pop=dff_pop.rename(columns={'index':'Gender',0:'values'})
# #print(dff_pop.columns)
# df_pop=df_pop[df_pop['Provinces']=='City of Kigali'].sum().squeeze()[2]
# #print(df_pop)

#creating a dataframe for each district

#create a subset for each district from dataset
dff_pop=df_pop[df_pop['Districts']=='Nyamagabe'].sum().squeeze()[3:5]
#convert series into a dataframe
dff_pop=pd.DataFrame(dff_pop)
#reset index of a dataframe
dff_pop=dff_pop.reset_index()
#rename the columns of a dataframe
dff_pop=dff_pop.rename(columns={'index':'Sex',0:'Population'})
#print(dff_pop)

dff_light=df_lighting[df_lighting['Districts']=='Gasabo'].sum().squeeze()[3:]
#convert series into a dataframe
dff_light=pd.DataFrame(dff_light)
#reset index
dff_light=dff_light.reset_index()
#rename columns
dff_light=dff_light.rename(columns={'index':'Lighting type',0:'percentage'})

fig=px.bar(dff_light,
           x='Lighting type',
           y='percentage')
# return fig
#select a subset for any district
dff_habit=df_pop_habitant[df_pop_habitant['Districts']=='Nyamagabe'].sum().squeeze()[3:]
#convert a series into dataframe
dff_habit=pd.DataFrame(dff_habit)
#reset index to allows renaming
dff_habit=dff_habit.reset_index()
#rename columns
dff_habit=dff_habit.rename(columns={'index':'Type of habitants',0:'percentage'})
fig=px.bar(dff_habit,
           x='Type of habitants',
           y='percentage',
           text='percentage')
#fig.show()
#select subset from the dataset and convert into series
dff_disab=df_disability[df_disability['Districts']=='Nyamagabe'].sum().squeeze()[2:]
#convert series into Dataframe
dff_disab=pd.DataFrame(dff_disab)
#reset index to allow renaming the columns
dff_disab=dff_disab.reset_index()
#rename columns
dff_disab=dff_disab.rename(columns={'index':'Gender',0:'Number of persons with disability'})
fig=px.bar(dff_disab,
           x='Gender',
           y='Number of persons with disability',
           text='Number of persons with disability',
           color='Gender')
#fig.show()

#print(dff_disab)
#select a subset district from dataset

#print(df_unem['Male'].round(decimals=3))

dff_unemp = df_unem[df_unem['Districts'] =='Nyamagabe'].sum().squeeze()[2:]
# convert series into Dataframe
dff_unemp = pd.DataFrame(dff_unemp)
# reset index to allow renaming the columns
dff_unemp = dff_unemp.reset_index()
# rename columns
dff_unemp = dff_unemp.rename(columns={'index': 'Gender', 0: 'Percentage of unemployed'})
dff_unemp= dff_unemp.round(decimals=3)
#print(dff_unemp)

#includes map
Rwanda_district=json.load(open(r'C:\Users\ENVY\PycharmProjects\mydashboard\Data fro census dashboard\Rwanda-districts-geojson.json','r'))
#print(Rwanda_district['features'][4]['properties'])
#create an empty dictionnary to allow putiing into my dataset
district_id_map={}
for feature in Rwanda_district['features']:
    feature['id']=feature['properties']['id']
    district_id_map[feature['properties']['adm2']]=feature['id']
#print(district_id_map)
#rename the keys in dictionnary
district_id_map['Ngoma']=district_id_map['Kibungo']
del district_id_map['Kibungo']
district_id_map['Gasabo']=district_id_map['Butamwa']
del district_id_map['Butamwa']
district_id_map['Nyarugenge']=district_id_map['Kigali']
del district_id_map['Kigali']
district_id_map['Gicumbi']=district_id_map['Byumba']
del district_id_map['Byumba']
district_id_map['Musanze']=district_id_map['Ruhengeri']
del district_id_map['Ruhengeri']
district_id_map['Huye']=district_id_map['Butare']
del district_id_map['Butare']
district_id_map['Ruhango']=district_id_map['Gatagara']
del district_id_map['Gatagara']
district_id_map['Nyamagabe']=district_id_map['Gikongoro']
del district_id_map['Gikongoro']
district_id_map['Ngororero']=district_id_map['Nogororero']
del district_id_map['Nogororero']
district_id_map['Muhanga']=district_id_map['Gitarama']
del district_id_map['Gitarama']
district_id_map['Rusizi']=district_id_map['Cyangugu']
del district_id_map['Cyangugu']
district_id_map['Nyabihu']=district_id_map['Gasiza']
del district_id_map['Gasiza']
district_id_map['Rubavu']=district_id_map['Gisenyi']
del district_id_map['Gisenyi']
district_id_map['Karongi']=district_id_map['Kibuye']
del district_id_map['Kibuye']
district_id_map['Lake Kivu']=district_id_map['Lake']
del district_id_map['Lake']
#print(district_id_map)

#assign the true id number to allow graphing

district_id_map['Bugesera']=3
district_id_map['Gatsibo']=10
district_id_map['Kayonza']=9
district_id_map['Kirehe']=6
district_id_map['Nyagatare']=36
district_id_map['Rwamagana']=24
district_id_map['Burera']=8
district_id_map['Rulindo']=15
district_id_map['Gakenke']=14
district_id_map['Gisagara']=2
district_id_map['Nyamasheke']=12
district_id_map['Kamonyi']=16
district_id_map['Nyanza']=20
district_id_map['Nyaruguru']=1
district_id_map['Rutsiro']=29
district_id_map['Ngoma']=11
district_id_map['Nyarugenge']=18
district_id_map['Gasabo']=23
district_id_map['Gicumbi']=7
district_id_map['Musanze']=37
district_id_map['Huye']=25
district_id_map['Nyamagabe']=13
district_id_map['Ruhango']=19
district_id_map['Ngororero']=35
district_id_map['Muhanga']=17
district_id_map['Rusizi']=39
district_id_map['Nyabihu']=4
district_id_map['Rubavu']=5
district_id_map['Karongi']=21
district_id_map['Kicukiro']=22
district_id_map['Lake Kivu']=38

#assign district_id to specific district

df_unem['district_id']=df_unem['Districts'].apply(lambda x:district_id_map[x])
#print(df_unem.head())
fig = px.choropleth(df_unem,
                    locations='district_id',
                    geojson=Rwanda_district,
                    color='Both sexes',
                    hover_name='Districts',
                    labels='Both sexes'
                    )

fig.update_geos(fitbounds='locations', visible=False),
fig.update_layout(title="Map of Rwanda: Population unemployment",
                  legend_itemclick="toggleothers"),
fig.update_traces(showlegend=False)
#fig.show()

#Population Pyramid
#print(df_age_group)
y_age=df_age_group['age_cat']
x_Male=df_age_group['Male']
x_Female=df_age_group['Female']*-1

#instantiate figure
fig = go.Figure()
fig.add_trace(go.Bar(
                y=y_age,
                x=x_Male,
                name='Male',
                orientation='h'
))
fig.add_trace(go.Bar(
                y=y_age,
                x=x_Female,
                name='Female',
                orientation='h'
))

fig.update_layout(
        template='plotly_white',
        title='Rwanda Census Population Pyramid',
        title_font_size=24,
        barmode='relative',
        bargap=0.0,
        bargroupgap=0,
        plot_bgcolor='white',
        xaxis=dict(
            tickvals=[-800000,-600000,-400000,-200000,0,200000,400000,600000,800000],
            ticktext=['800k','600k','400k','200k',0,'200k','400k','600k','800k'],
            title='Population in Thousands'
        )
)
#fig.show()
#Urban population population pyramid


y_age=df_age_group_urban['age_cat']
x_Male=df_age_group_urban['Male']
x_Female=df_age_group_urban['Female']*-1

#instantiate figure
fig = go.Figure()
fig.add_trace(go.Bar(
                y=y_age,
                x=x_Male,
                name='Male',
                orientation='h'
))
fig.add_trace(go.Bar(
                y=y_age,
                x=x_Female,
                name='Female',
                orientation='h'
))

fig.update_layout(
        template='plotly_white',
        title='Urban Census Population Pyramid',
        title_font_size=24,
        barmode='relative',
        bargap=0.0,
        bargroupgap=0,
        plot_bgcolor='white',
        xaxis=dict(
            tickvals=[-200000,-100000,0,100000,200000],
            ticktext=['200k','100k',0,'100k','200k'],
            title='Population in Thousands'
        )
)
#fig.show()

#rural population pyramid
y_age=df_age_group_rural['age_cat']
x_Male=df_age_group_rural['Male']
x_Female=df_age_group_rural['Female']*-1

fig = go.Figure()
fig.add_trace(go.Bar(
                y=y_age,
                x=x_Male,
                name='Male',
                orientation='h'
))
fig.add_trace(go.Bar(
                y=y_age,
                x=x_Female,
                name='Female',
                orientation='h'
))

fig.update_layout(
        template='plotly_white',
        title='Rural Census Population Pyramid',
        title_font_size=24,
        barmode='relative',
        bargap=0.0,
        bargroupgap=0,
        plot_bgcolor='white',
        xaxis=dict(
            tickvals=[-600000,-400000,-200000,0,200000,400000,600000],
            ticktext=['600k','400k','200k',0,'200k','400k','600k'],
            title='Population in Thousands'
        )
)
#fig.show()








