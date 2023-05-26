import pandas as pd
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from os.path import join, dirname
from os import getenv
from sqlalchemy import create_engine



# Retrieve the database URL from the environment variables
database_url = getenv('DATABASE_URL')


engine = create_engine(database_url)

app = Flask(__name__)
bootstrap = Bootstrap(app)
@app.route('/')
def index():
    # Get the page parameter from the request query string
    page = request.args.get('page', default=1, type=int)
    offset = (page - 1) * 10  # Calculate the offset for pagination

    # Execute the SELECT query with LIMIT and OFFSET
    query = "SELECT * FROM insee_dept LIMIT 10 OFFSET %s" % offset
    df = pd.read_sql_query(query, engine)

    # Convert the DataFrame to an HTML table
    table_html = df.to_html(index=False)

    
    return render_template('index.html', table_html=table_html)

if __name__ == '__main__':
    app.run(debug=True)