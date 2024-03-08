from flask import Flask, request, send_file
import requests
import os

app = Flask(__name__)

# Set your Clipdrop API key here
CLIPDROP_API_KEY = '5ec050c2f0a57ef6d5cfad7e302479fa745275e79f0d9b0ecd73ccae383787e2054ed81a78f59ac3e416c066952f3f02'
# CLIPDROP_API_KEY = '3fde43c5cecba030f11187fe643e619576f7eea915500515b8aba9305531bf4ab8746698fdf948e51e6c4960722ec1bd'
apikeys =[['5ec050c2f0a57ef6d5cfad7e302479fa745275e79f0d9b0ecd73ccae383787e2054ed81a78f59ac3e416c066952f3f02', 0], ['3fde43c5cecba030f11187fe643e619576f7eea915500515b8aba9305531bf4ab8746698fdf948e51e6c4960722ec1bd', 0], ['c6fb1234b35760e4066a0697d3aa56a0496659b291f2a75964e1db878c5f63f405ce297d608a81dc234b1d03ade379ae', 0], ['2016d1ded6010b5718311a20ca9e5017727ac888f7d4c4441674c41dba1d080a0f0c60d155ea630621af07637507be5d', 0], ['b144e92c1a54880a6baed0df98ee961ac517f1716420dbf70e74912f6d87bb12a353a36cf6a9f8b432d90a133866b631', 0], ['c2c0c9c69bb41db87950aafc3b6d621257a07d775bd833b1dfb99cd0eb183ccaae72fcadcf6834003fa0687cc6824690', 0], ['ca2435020432c953e130fd0d51193f626495658739cbcc6b838a3a179c0e7b157d0c2820cc8a203b8720763e93fb7fb8', 0], ['7747b575dea0ac4a954da1cabc2ec330606819b5fd6e4ae58bb670e1862a7e35d2f86acee3fdc81565df31e4665fdc4e', 53], ['224c85e9309d7001bbe7ac3026a0222ed58b1d76c88a609085cc022e452e663e9e22b6078a0a6bc2db47cd36efe51b43', 100]]


# Directory for saving temporary files
TEMP_DIR = './temp'
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)


@app.route('/cleanup', methods=['POST'])
def cleanup():
    # Check if the request has the required files
    if 'image_file' not in request.files or 'mask_file' not in request.files:
        return {'error': 'Please provide both image_file and mask_file'}, 400

    image_file = request.files['image_file']
    mask_file = request.files['mask_file']
    mode = request.form.get('mode', 'fast')  # Default mode is 'fast'

    # Save temporary files
    image_path = os.path.join(TEMP_DIR, image_file.filename)
    mask_path = os.path.join(TEMP_DIR, mask_file.filename)
    image_file.save(image_path)
    mask_file.save(mask_path)

    # Prepare files for the API request
    files = {
        'image_file': (image_file.filename, open(image_path, 'rb'), 'image/jpeg'),
        'mask_file': (mask_file.filename, open(mask_path, 'rb'), 'image/png')
    }

    CLIPDROP_API_KEY = apikeys[0][0]
    index = 0
    while(apikeys[index][1]<1):
        index += 1
        CLIPDROP_API_KEY = apikeys[index][0]
    
    apikeys[index][1] -= 1

    # Prepare headers
    headers = {
        'x-api-key': CLIPDROP_API_KEY
    }

    # Prepare data
    data = {
        'mode': mode
    }

    # Make the API request
    response = requests.post('https://clipdrop-api.co/cleanup/v1',
                             headers=headers,
                             files=files,
                             data=data)

    # Clean up the temporary files
    os.remove(image_path)
    os.remove(mask_path)

    print(apikeys)

    if response.status_code == 200:
        # Save the resulting image
        result_path = os.path.join(TEMP_DIR, 'result.png')
        with open(result_path, 'wb') as f:
            f.write(response.content)

        # Send the resulting image back to the client
        return send_file(result_path, mimetype='image/png')
    else:
        # Return the error from the API
        return response.json(), response.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)