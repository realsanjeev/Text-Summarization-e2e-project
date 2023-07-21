from flask import Flask, render_template, request
from src.pipeline.estimator import PredictionPipeline

app = Flask(__name__)
predict_pipeline = PredictionPipeline()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        script = request.form.get('script')
        summary_text = predict_pipeline.predict(script)
    return render_template('index.html', Summary=summary_text)

if __name__ == "__main__":
    app.run(debug=True)
