# Coqui XTTS-v2 Text-to-Speech Demo

A web application that demonstrates text-to-speech capabilities using the Coqui XTTS-v2 model. The application features a React-based frontend with Material-UI components and WebSocket communication for real-time speech synthesis.

## Features

- Real-time text-to-speech conversion
- WebSocket-based communication
- Modern UI with Material-UI components
- Audio playback of generated speech
- Display of processing time for each conversion

## Tech Stack

- Frontend:
  - React.js
  - Material-UI
  - WebSocket API
- Backend:
  - WebSocket server (port 8000)
  - Coqui XTTS-v2 model

## Setup

1. Clone the repository:
```bash
git clone [your-repo-url]
cd [repo-name]
```

2. Install frontend dependencies:
```bash
cd react-ui
npm install
```

3. Start the frontend development server:
```bash
npm start
```

4. Make sure your WebSocket server is running on `localhost:8000`

## Usage

1. Enter text in the input field
2. Click "Generate Speech"
3. Wait for the audio to be generated
4. Play the generated audio using the audio controls

## Author

Created by [Shalabh Singh](https://www.linkedin.com/in/shalabh-singh/)

## License

MIT 