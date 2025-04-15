client = bigquery.Client(location="europe-west4")
# Flask setup
app = Flask(__name__)
@app.route("/", methods=['GET'])
def root():
    response = app.response_class(
        response="OK",
        status=200,
    )
    return response
@app.route("/metrics", methods=['GET'])
def metrics():
    query = "SELECT * FROM <PROJECT-ID>.vmCloud.data limit 10;"
    query_job = client.query(query)
    result = query_job.result()
    rows = list(result)
    response = app.response_class(
        response=format(rows),
        status=200,
    )
    return response
if __name__ == '__main__':
    app.run(port=8080, debug=True, host="0.0.0.0")