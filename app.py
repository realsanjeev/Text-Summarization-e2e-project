import logging
from flask import Flask, render_template, request
from src.pipeline.estimator import PredictionPipeline

app = Flask(__name__)
# predict_pipeline = PredictionPipeline()

logging.disable(logging.CRITICAL)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        script = request.form.get('script')
        # summary_text = predict_pipeline.predict(script)
        summary_text = script
        return render_template('index.html',
                               summary=summary_text,
                               script=script)
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
