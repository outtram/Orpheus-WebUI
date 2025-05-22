# Orpheus WebUI - Bastion Edition

Lightweight web interface for OrpheusTTS using remote Bastion-hosted model.

## Features

- 🎤 8 voice options (tara, jess, leo, leah, dan, mia, zac, zoe)
- 😊 Emotion tags support (laugh, chuckle, sigh, etc.)
- 🎛️ Full parameter control (temperature, top_p, repetition penalty)
- 🌐 Remote API integration (no local GPU needed)
- 🖥️ Simple Gradio interface

## Quick Start

```bash
# Clone the repo
git clone [your-repo-url]
cd Orpheus-WebUI

# Set up environment
cp .env.template .env
# Edit .env with your Bastion API details

# Launch
./launch.sh
```

## Requirements

- Python 3.10+
- macOS/Linux/Windows
- Bastion API access

## Configuration

Edit `.env` file:
```
BASTION_URL=https://your-bastion-instance.com/orpheus
BASTION_API_KEY=your-api-key
```

## Usage

1. Select voice from dropdown
2. Enter your text
3. Optionally add emotion tags
4. Adjust generation parameters
5. Click "Generate Speech"

## Development

See `DEVELOPER_HANDOVER.md` for detailed technical information.

## License

MIT
