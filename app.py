import os
import random
import json
import fitz  # PyMuPDF
from flask import Flask, jsonify, request, send_file, render_template, url_for
from io import BytesIO
import requests

app = Flask(__name__)
# Setup logging
logging.basicConfig(level=logging.INFO)

worksheet_data = {
    "grade_1": {
        "number_charts": {
            "printing_numbers_1_25": [
                "https://www.k5learning.com/worksheets/math/grade-1-write-numbers-1-5.pdf",
                "https://www.k5learning.com/worksheets/math/grade-1-write-numbers-6-10.pdf",
                "https://www.k5learning.com/worksheets/math/grade-1-write-numbers-11-15.pdf",
                "https://www.k5learning.com/worksheets/math/grade-1-write-numbers-16-20.pdf",
                "https://www.k5learning.com/worksheets/math/grade-1-write-numbers-21-25.pdf"
            ],
            "printing_numbers_26_50": [
                "https://www.k5learning.com/worksheets/math/grade-1-write-numbers-26-30.pdf",
                "https://www.k5learning.com/worksheets/math/grade-1-write-numbers-31-35.pdf",
                "https://www.k5learning.com/worksheets/math/grade-1-write-numbers-36-40.pdf",
                "https://www.k5learning.com/worksheets/math/grade-1-write-numbers-41-45.pdf",
                "https://www.k5learning.com/worksheets/math/grade-1-write-numbers-46-50.pdf"
            ],
            "printing_numbers_51_75": [
                "https://www.k5learning.com/worksheets/math/grade-1-write-numbers-51-55.pdf",
                "https://www.k5learning.com/worksheets/math/grade-1-write-numbers-56-60.pdf",
                "https://www.k5learning.com/worksheets/math/grade-1-write-numbers-61-65.pdf",
                "https://www.k5learning.com/worksheets/math/grade-1-write-numbers-66-70.pdf",
                "https://www.k5learning.com/worksheets/math/grade-1-write-numbers-71-75.pdf"
            ],
            "printing_numbers_76_100": [
                "https://www.k5learning.com/worksheets/math/grade-1-write-numbers-76-80.pdf",
                "https://www.k5learning.com/worksheets/math/grade-1-write-numbers-81-85.pdf",
                "https://www.k5learning.com/worksheets/math/grade-1-write-numbers-86-90.pdf",
                "https://www.k5learning.com/worksheets/math/grade-1-write-numbers-91-95.pdf",
                "https://www.k5learning.com/worksheets/math/grade-1-write-numbers-96-100.pdf"
            ],
            "Write_number_words_1_50": [
               "https://www.k5learning.com/worksheets/math/grade-1-write-number-words-a.pdf"
               "https://www.k5learning.com/worksheets/math/grade-1-write-number-words-b.pdf"
               "https://www.k5learning.com/worksheets/math/grade-1-write-number-words-c.pdf"
               "https://www.k5learning.com/worksheets/math/grade-1-write-number-words-d.pdf"
               "https://www.k5learning.com/worksheets/math/grade-1-write-number-words-e.pdf"
            ],
            "Write_number_words_51_100": [
                "https://www.k5learning.com/worksheets/math/grade-1-write-number-words-100-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-write-number-words-100-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-write-number-words-100-c.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-write-number-words-100-d.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-write-number-words-100-e.pdf"

            ],
            "Match_numbers_with_their_words": [
                "https://www.k5learning.com/worksheets/math/grade-1-numbers-words-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-numbers-words-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-numbers-words-c.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-numbers-words-d.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-numbers-words-e.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-numbers-words-f.pdf"
            ],
            "Ordinal_numbers": [
                "https://www.k5learning.com/worksheets/math/grade-1-ordinal-numbers-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-ordinal-numbers-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-ordinal-numbers-c.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-ordinal-numbers-d.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-ordinal-numbers-e.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-ordinal-numbers-f.pdf"
            ],
            "Counting_in_Sequence_1_10": [
                "https://www.k5learning.com/worksheets/math/grade-1-counting-sequence-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-sequence-b.pdf"
            ],
            "Circle_Number_Objects_1_10_1_20": [
                "https://www.k5learning.com/worksheets/math/1st-grade-counting-objects-1.pdf"
                "https://www.k5learning.com/worksheets/math/1st-grade-counting-objects-2.pdf"
                "https://www.k5learning.com/worksheets/math/1st-grade-counting-objects-4.pdf"
                "https://www.k5learning.com/worksheets/math/1st-grade-counting-objects-5.pdf"
            ],
            "Counting_writing_numbers_1_10": [
                "https://www.k5learning.com/worksheets/math/grade-1-counting-writing-numbers-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-writing-numbers-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-writing-numbers-c.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-writing-numbers-d.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-writing-numbers-e.pdf"
            ],
            "Count_objects_write_number_1_20": [
                "https://www.k5learning.com/worksheets/math/1st-grade-counting-objects-to-20-a.pdf"
                "https://www.k5learning.com/worksheets/math/1st-grade-counting-objects-to-20-b.pdf"
                "https://www.k5learning.com/worksheets/math/1st-grade-counting-objects-to-20-c.pdf"
                ""
            ],
            "Counting_questions": [
                "https://www.k5learning.com/worksheets/math/grade-1-counting-combining-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-combining-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-combining-d.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-combining-e.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-questions-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-questions-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-questions-c.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-questions-d.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-questions-e.pdf"
            ],
            "counting_1_20s": [
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-1-20-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-1-20-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-1-20-c.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-1-20-d.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-1-20-e.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-1-20-f.pdf"

            ],
            "counting_1_30s": [
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-1-30-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-1-30-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-1-30-c.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-1-30-d.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-1-30-e.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-1-30-f.pdf"
            ],
            "counting_1_50s": [
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-1-50-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-1-50-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-1-50-c.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-1-50-d.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-1-50-e.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-1-50-f.pdf"
            ],
            "Counting_practice_before_after": [
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-before-after-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-before-after-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-before-after-c.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-before-after-d.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-before-after-e.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-before-after-f.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-before-after-g.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-practice-before-after-h.pdf"
            ],
            "Counting_2": [
                "https://www.k5learning.com/worksheets/math/grade-1-counting-by-twos-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-by-twos-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-by-twos-c.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-by-twos-d.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-by-twos-e.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-by-twos-f.pdf"
            ],
            "Counting_5": [
                "https://www.k5learning.com/worksheets/math/grade-1-counting-by-fives-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-by-fives-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-by-fives-c.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-by-fives-d.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-by-fives-e.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-by-fives-f.pdf"
            ],
            "Counting_10": [
                "https://www.k5learning.com/worksheets/math/grade-1-counting-by-tens-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-by-tens-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-by-tens-d.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-counting-by-tens-e.pdf"
            ],
            "Number_charts_1_100": [
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-1-100-full.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-1-100-empty.pdf"
            ],
            "Number_charts_counting_counting_ones": [
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-1-100-half-full-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-1-100-half-full-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-1-100-half-full-c.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-1-100-quarter-full-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-1-100-quarter-full-b.pdf"
            ],
            "Number_charts_counting_counting_twos": [
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-by-2s-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-by-2s-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-by-2s-c.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-by-2s-odd-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-by-2s-odd-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-by-2s-odd-c.pdf"
            ],
            "Number_charts_counting_3": [
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-by-3s-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-by-3s-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-by-3s-c.pdf"
            ],
            "Number_charts_counting_4": [
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-by-4s-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-by-4s-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-by-4s-c.pdf"
            ],
            "Number_charts_counting_5": [
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-by-5s-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-by-5s-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-by-5s-c.pdf"
            ],
            "Number_charts_counting_10": [
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-by-10s-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-by-10s-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-by-10s-c.pdf"
            ],
            "Count_backwards_100_0": [
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-backwards-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-backwards-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-backwards-c.pdf"
            ],
            "Countbackwards_2s": [
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-backwards-by-2s-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-backwards-by-2s-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-backwards-by-2s-c.pdf"
            ],
            "Countbackwards_5s": [
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-backwards-by-5s-a.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-backwards-by-5s-b.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-number-chart-counting-backwards-by-5s-c.pdf"
            ],
            "Even_vs_odd_worksheets": [
                "https://www.k5learning.com/worksheets/math/grade-1-even-odd-numbers-1.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-even-odd-numbers-2.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-even-odd-numbers-3.pdf"
                "https://www.k5learning.com/worksheets/math/grade-1-even-odd-numbers-4.pdf"
            ],
            # Add more subtopics here as needed
        },
        # Add more topics here as needed
    },
    # Add more grades here as needed
}

@app.route('/')
def home():
    return render_template('index.html')

def crop_pdf(input_pdf_bytes):
    pdf_document = fitz.open(stream=input_pdf_bytes, filetype="pdf")
    
    crop_top = 50  # Number of points to crop from the top
    crop_bottom = 50  # Number of points to crop from the bottom
    
    for page in pdf_document:
        rect = page.rect
        page.set_cropbox(fitz.Rect(rect.x0, rect.y0 + crop_top, rect.x1, rect.y1 - crop_bottom))
    
    output_pdf_bytes = BytesIO()
    pdf_document.save(output_pdf_bytes)
    pdf_document.close()
    output_pdf_bytes.seek(0)
    
    return output_pdf_bytes

@app.route('/get-worksheet', methods=['POST'])
def get_worksheet():
    data = request.json
    grade = data['grade']
    topic = data['topic']
    subtopic = data['subtopic']
    
    pdf_urls = worksheet_data[grade][topic][subtopic]
    selected_pdf_url = random.choice(pdf_urls)
    
    response = requests.get(selected_pdf_url)
    cropped_pdf = crop_pdf(response.content)
    
    filename = f"cropped_{random.randint(1000, 9999)}.pdf"
    filepath = os.path.join('static', filename)
    
    with open(filepath, 'wb') as f:
        f.write(cropped_pdf.getbuffer())
    
    return jsonify({'url': url_for('static', filename=filename)})

if __name__ == '__main__':
    app.run(debug=True)
