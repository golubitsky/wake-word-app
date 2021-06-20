from flask import request, render_template
from flask import current_app as app
from datetime import datetime
from .inference import get_category, plot_category


@app.route('/', methods=['GET', 'POST'])
def rock_paper_scissor():
    # Write the GET Method to get the index file
    if request.method == 'GET':
        return render_template('index.html')
    # Write the POST Method to post the results file
    if request.method == 'POST':
        print("processing POST request")
        print(request.files)
        if 'file' not in request.files:
            print('File Not Uploaded')
            return
        # Read file from upload
        file = request.files['file']
        # Get category of prediction
        category = get_category(img=file)
        # Plot the category
        now = datetime.now()
        current_time = now.strftime("%H-%M-%S")
        print("plotting category")
        plot_category(file, current_time)
        # Render the result template
        return render_template('result.html', category=category, current_time=current_time)
