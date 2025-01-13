from flask import Flask, request, jsonify
import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import base64
import io
from sklearn.decomposition import PCA
import plotly.express as px
from sklearn.preprocessing import StandardScaler

# Create Flask server
server = Flask(__name__)

# Create Dash app
app = dash.Dash(__name__, server=server, url_base_pathname='/')

app.layout = html.Div([
    html.H1("Omics Data Analyzer", style={"textAlign": "center"}),

    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    html.Div(id='output-data-upload'),

    html.Div([
        html.H4("Preprocessing Options:"),
        dcc.Checklist(
            id='preprocessing-options',
            options=[
                {'label': 'Fill Missing Values', 'value': 'fillna'}
            ],
            value=[]
        ),
        html.Div([
            html.Label("Select Columns to Normalize:"),
            dcc.Dropdown(
                id='normalize-columns',
                multi=True,
                placeholder="Select columns to normalize",
            )
        ], style={'marginTop': '10px'})
    ], style={'margin': '20px'}),

    
    html.Div([
    html.H4("PCA Analysis:"),
    html.Label("Select Variables for PCA:"),
    dcc.Dropdown(
        id='pca-variable-selection',
        multi=True,
        placeholder="Select numeric variables for PCA",
    ),
    html.Label("Number of Components:"),
    dcc.Slider(
        id='pca-components',
        min=2,
        max=10,
        step=1,
        value=2,
        marks={i: str(i) for i in range(2, 11)}
    ),
    html.Button("Run PCA", id='run-pca', n_clicks=0),
    html.Div(id='pca-output', style={'marginTop': '20px'})
    ], style={'margin': '20px'}),

    
    html.Div(id='preprocessing-output')
])


@app.callback(
    [dash.dependencies.Output('output-data-upload', 'children'),
     dash.dependencies.Output('normalize-columns', 'options'),
     dash.dependencies.Output('pca-variable-selection', 'options')],
    [dash.dependencies.Input('upload-data', 'contents')],
    [dash.dependencies.State('upload-data', 'filename')]
)
def update_file_preview(contents, filename):
    if contents:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            # Read file into DataFrame
            if filename.endswith('.csv'):
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            elif filename.endswith('.xlsx'):
                df = pd.read_excel(io.BytesIO(decoded))
            else:
                return html.Div(["Unsupported file format."]), [], []

            # Display file preview
            file_preview = html.Div([
                html.H5(f"Uploaded File: {filename}"),
                html.H6("Preview of Data:"),
                html.Table([
                    html.Thead(
                        html.Tr([html.Th(col) for col in df.columns])
                    ),
                    html.Tbody([
                        html.Tr([
                            html.Td(df.iloc[i][col]) for col in df.columns
                        ]) for i in range(min(len(df), 5))
                    ])
                ])
            ])

            # Generate column dropdown options
            column_options = [{'label': col, 'value': col} for col in df.columns]
            numeric_options = [{'label': col, 'value': col} for col in df.select_dtypes(include='number').columns]

            return file_preview, column_options, numeric_options
        except Exception as e:
            return html.Div([f"An error occurred: {str(e)}"]), [], []
    return html.Div(["No file uploaded yet."]), [], []



@app.callback(
    dash.dependencies.Output('preprocessing-output', 'children'),
    [dash.dependencies.Input('preprocessing-options', 'value'),
     dash.dependencies.Input('normalize-columns', 'value')],
    [dash.dependencies.State('upload-data', 'contents'),
     dash.dependencies.State('upload-data', 'filename')]
)
def preprocess_data(options, normalize_columns, contents, filename):
    if contents:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            # Read file into DataFrame
            if filename.endswith('.csv'):
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            elif filename.endswith('.xlsx'):
                df = pd.read_excel(io.BytesIO(decoded))
            else:
                return html.Div(["Unsupported file format."])

            # Apply preprocessing
            if normalize_columns:
                df[normalize_columns] = (df[normalize_columns] - df[normalize_columns].min()) / (df[normalize_columns].max() - df[normalize_columns].min())
            
            if 'fillna' in options:
                df = df.fillna(0)  # Fill missing values with 0

            # Display preprocessed data
            return html.Div([
                html.H5("Preprocessed Data Preview:"),
                html.Table([
                    html.Thead(
                        html.Tr([html.Th(col) for col in df.columns])
                    ),
                    html.Tbody([
                        html.Tr([
                            html.Td(df.iloc[i][col]) for col in df.columns
                        ]) for i in range(min(len(df), 5))
                    ])
                ])
            ])
        except Exception as e:
            return html.Div([f"An error occurred: {str(e)}"])
    return html.Div(["No file uploaded yet."])


# Update the parse_data function
def parse_data(contents, filename):
    if contents:
        # Decode the uploaded file
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            # Try to read the file as a CSV
            if filename.endswith('.csv'):
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            elif filename.endswith('.xlsx'):
                df = pd.read_excel(io.BytesIO(decoded))
            else:
                return html.Div(["Unsupported file format. Please upload a CSV or Excel file."])

            # Display first 5 rows as a preview
            return html.Div([
                html.H5(f"Uploaded File: {filename}"),
                html.H6("Preview of Data:"),
                html.Table([
                    html.Thead(
                        html.Tr([html.Th(col) for col in df.columns])
                    ),
                    html.Tbody([
                        html.Tr([
                            html.Td(df.iloc[i][col]) for col in df.columns
                        ]) for i in range(min(len(df), 5))
                    ])
                ])
            ])
        except Exception as e:
            return html.Div([f"An error occurred: {str(e)}"])
    return html.Div(["No file uploaded yet."])


@app.callback(
    dash.dependencies.Output('pca-output', 'children'),
    [dash.dependencies.Input('run-pca', 'n_clicks')],
    [dash.dependencies.State('upload-data', 'contents'),
     dash.dependencies.State('upload-data', 'filename'),
     dash.dependencies.State('pca-variable-selection', 'value'),
     dash.dependencies.State('pca-components', 'value')]
)
def perform_pca(n_clicks, contents, filename, selected_variables, n_components):
    if n_clicks > 0 and contents and selected_variables:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            # Read the file
            if filename.endswith('.csv'):
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            elif filename.endswith('.xlsx'):
                df = pd.read_excel(io.BytesIO(decoded))
            else:
                return html.Div(["Unsupported file format."])

            # Filter DataFrame for selected numeric variables
            numeric_df = df[selected_variables]

            # Standardize the data
            scaler = StandardScaler()
            standardized_data = scaler.fit_transform(numeric_df)

            # Perform PCA
            pca = PCA(n_components=n_components)
            pca_result = pca.fit_transform(standardized_data)

            # Create a DataFrame for PCA results
            pca_df = pd.DataFrame(pca_result, columns=[f"PC{i+1}" for i in range(n_components)])
            pca_df['Sample'] = numeric_df.index

            # Scatter plot for the first two components
            fig = px.scatter(
                pca_df, x='PC1', y='PC2',
                title=f"PCA Scatter Plot (First 2 Components)",
                labels={'PC1': 'Principal Component 1', 'PC2': 'Principal Component 2'},
                hover_data=['Sample']
            )

            return html.Div([
                dcc.Graph(figure=fig),
                html.H6("Explained Variance Ratios:"),
                html.Ul([html.Li(f"PC{i+1}: {var:.2f}") for i, var in enumerate(pca.explained_variance_ratio_)])
            ])
        except Exception as e:
            return html.Div([f"An error occurred during PCA: {str(e)}"])
    return html.Div(["Please select variables and click 'Run PCA'."])

if __name__ == '__main__':
    app.run_server(debug=True)
