# Orpheus WebUI

A web interface for Orpheus TTS using local GGUF model via LM Studio.

## Features

- 🎙️ 8 different voices with varying naturalness
- 😊 Emotion tags for expressive speech
- 🎛️ Fine-tune generation parameters
- 🎵 Direct audio file output
- 💻 Local model - no internet required

## Prerequisites

1. **LM Studio** - Download from [lmstudio.ai](https://lmstudio.ai)
2. **Orpheus Model** - Load `orpheus-3b-0.1-ft-q4_k_m` in LM Studio
3. **Python 3.8+** - For running the web interface

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/outtram/Orpheus-WebUI.git
cd Orpheus-WebUI
```

2. Install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Start LM Studio and load the Orpheus model

4. Run the application:
```bash
./launch.sh
# OR
python app.py
```

5. Open http://localhost:7860 in your browser

## Usage

1. **Enter Text**: Type or paste your text
2. **Select Voice**: Choose from 8 available voices (Tara is recommended)
3. **Add Emotions**: Optionally add emotional expressions
4. **Adjust Parameters**: Fine-tune generation settings
5. **Generate**: Click to create speech
6. **Listen**: Play the generated audio directly in browser

## Voices

- **Tara** ⭐ - Most natural and recommended
- Leah, Jess, Leo, Dan, Mia, Zac, Zoe

## Emotion Tags

Add expressive elements to your speech:
- `<laugh>`, `<chuckle>`, `<sigh>`, `<cough>`
- `<sniffle>`, `<groan>`, `<yawn>`, `<gasp>`

## Troubleshooting

### "Model not available" error
- Ensure LM Studio is running on port 1234
- Verify the Orpheus model is loaded
- Check firewall settings

### No audio output
- Check the outputs/ directory for WAV files
- Verify sufficient disk space
- Check console for error messages

## Development

See [DEVELOPER_HANDOVER.md](DEVELOPER_HANDOVER.md) for technical details and contribution guidelines.

## License

This project is a web interface for the Orpheus TTS model. Please refer to the original Orpheus model license for usage terms.
