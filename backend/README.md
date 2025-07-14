# Backend README.md

# Text to Video Converter - Backend

This is the backend component of the Text to Video Converter project. It provides APIs for converting text to speech and generating videos based on the audio output.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/text-to-video-converter.git
   cd text-to-video-converter/backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the backend server, execute the following command:
```
python src/app.py
```
The server will start on `http://localhost:5000`.

## API Endpoints

### POST /api/tts

- **Description**: Converts text to speech and returns the audio file.
- **Request Body**:
  ```json
  {
    "text": "Your text here"
  }
  ```
- **Response**:
  - 200 OK: Returns the URL of the generated audio file.
  - 400 Bad Request: If the input text is missing or invalid.

### POST /api/video

- **Description**: Generates a video using the provided audio file and text.
- **Request Body**:
  ```json
  {
    "audio_file": "path/to/audio/file",
    "text": "Your text here"
  }
  ```
- **Response**:
  - 200 OK: Returns the URL of the generated video file.
  - 400 Bad Request: If the input is invalid.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.