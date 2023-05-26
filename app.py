import pandas as pd
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

from sqlalchemy import create_engine

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient






app = Flask(__name__)

# Create a Key Vault SecretClient
key_vault_url = "https://flask-app-vault2.vault.azure.net/"  # Replace with your Key Vault URL
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=key_vault_url, credential=credential)

 # Retrieve the connection string from Azure Key Vault
secret_name = "DATABASE-URL2"  # Replace with the name of your secret in Key Vault
secret_value = secret_client.get_secret(secret_name).value
secret_value = secret_value.replace('\\','')
engine = create_engine(secret_value )
print(secret_value)
print(engine)

bootstrap = Bootstrap(app)
@app.route('/')
def index():
    # Retrieve the department number from the form submission
    dept_number = request.args.get('dept_number', default='', type=str)

    if dept_number:
        # Construct the SQL query with the department number
        query = "SELECT * FROM insee_dept WHERE dept_num = '%s'" % dept_number

        df = pd.read_sql_query(query, engine)

        # Convert the DataFrame to an HTML table
        table_html = df.to_html(index=False)

        return render_template('index.html', table_html=table_html, dept_number=dept_number)

    else:
        # Query the entire table with LIMIT 10
        query = "SELECT * FROM insee_dept LIMIT 10"

        df = pd.read_sql_query(query, engine)

        # Convert the DataFrame to an HTML table
        table_html = df.to_html(index=False)

        return render_template('index.html', table_html=table_html, dept_number='')



if __name__ == '__main__':
    app.run(debug=True)