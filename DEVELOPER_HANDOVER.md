# Orpheus WebUI Developer Handover Notes

## Project Overview
- **Purpose**: Web interface for OrpheusTTS using local GGUF model via LM Studio
- **Stack**: Gradio UI, Python backend, Local model integration
- **Platform**: M1 Mac (16GB RAM)
- **Status**: Migrated from Bastion API to Local Model

## Current State (2025-05-23 - Update #3)

### Completed Today - Latest
- [x] Fixed Python 3.13 compatibility issue with Gradio
- [x] Updated Gradio to version 5.9.1 for better compatibility
- [x] Fixed server launch configuration (localhost accessibility)
- [x] Added fallback launch configuration
- [x] Improved error handling for launch failures

### Completed Today - Earlier
- [x] Migrated from Bastion API to local Orpheus model
- [x] Integrated with `/Users/touttram/CODER4LIFE/Orpheus-Test-V1/orpheus-tts-local/gguf_orpheus.py`
- [x] Updated UI to support audio file output
- [x] Added model availability checking
- [x] Updated requirements for local model support
- [x] Added voice samples tab
- [x] Improved error handling for LM Studio connection

### Previous Completed
- [x] Created project directory structure
- [x] Initialized developer handover documentation
- [x] Built API client for Bastion integration
- [x] Created Gradio interface with voice/emotion controls
- [x] Set up environment configuration (.env)
- [x] Created launch script for easy startup
- [x] Added .gitignore for clean repository
- [x] GitHub repository setup and initial commit
- [x] Git initialized with main branch
- [x] Remote origin configured to https://github.com/outtram/Orpheus-WebUI.git

### In Progress
- [ ] Testing audio generation with local model
- [ ] Creating outputs directory structure

### Pending
- [ ] Long-form content processing
- [ ] Batch processing for multiple files
- [ ] Audio preview/playback enhancements
- [ ] Model parameter presets

## Key Changes from Bastion Version

### 1. Model Integration
- **FROM**: Remote Bastion API calls
- **TO**: Local Orpheus GGUF model via LM Studio
- **PATH**: `/Users/touttram/CODER4LIFE/Orpheus-Test-V1/orpheus-tts-local/gguf_orpheus.py`

### 2. Dependencies
- **ADDED**: `numpy`, `sounddevice`, `wave` for audio handling
- **REMOVED**: Bastion-specific authentication
- **KEPT**: `gradio`, `requests`, `python-dotenv`

### 3. Output Handling
- **NEW**: Generates WAV files locally in `outputs/` directory
- **NEW**: Audio playback component in UI
- **NEW**: File management for generated audio

### 4. Model Requirements
- **LM Studio**: Must be running on `http://127.0.0.1:1234`
- **Model**: `orpheus-3b-0.1-ft-q4_k_m` must be loaded
- **Memory**: ~4GB RAM for model + overhead

## Technical Architecture

### File Structure
```
Orpheus-WebUI/
├── app.py              # Main Gradio application (updated for local model)
├── requirements.txt    # Updated dependencies
├── .env               # Environment configuration (optional now)
├── .env.template      # Configuration template
├── launch.sh          # Quick start script
├── .gitignore         # Repository hygiene
├── DEVELOPER_HANDOVER.md  # This file
├── README.md          # User documentation
└── outputs/           # Generated audio files (created at runtime)
```

### Local Model Integration
- Imports from external path: `/Users/touttram/CODER4LIFE/Orpheus-Test-V1/orpheus-tts-local/`
- Uses LM Studio API on port 1234
- Generates 24kHz WAV files
- Supports 8 voices and 8 emotion tags

### Model Parameters
- **Temperature**: 0.0 (deterministic by default)
- **Top P**: 0.15 (narrow sampling)
- **Repetition Penalty**: 1.8 (high to prevent loops)
- **Max Tokens**: 1200 (default)
- **Sample Rate**: 24kHz (SNAC model standard)

## Environment Setup

### 1. Install Dependencies
```bash
cd /Users/touttram/CODER4LIFE/Orpheus-WebUI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Start LM Studio
- Launch LM Studio
- Load model: `orpheus-3b-0.1-ft-q4_k_m`
- Ensure server is running on port 1234

### 3. Run Application
```bash
./launch.sh
# OR
python app.py
```

## Available Voices (Best to Worst)
1. **tara** ⭐ (Default - most natural)
2. leah
3. jess
4. leo
5. dan
6. mia
7. zac
8. zoe

## Emotion Tags
- `<laugh>` - Laughter
- `<chuckle>` - Light laugh
- `<sigh>` - Sighing
- `<cough>` - Coughing
- `<sniffle>` - Sniffling
- `<groan>` - Groaning
- `<yawn>` - Yawning
- `<gasp>` - Gasping

## Troubleshooting

### Python 3.13 Compatibility Error
**Issue**: TypeError in gradio_client with Python 3.13
**Solution**: Updated Gradio to 5.9.1 and fixed launch configuration
**Alternative**: Use Python 3.11 or 3.12 if issues persist

### "Localhost not accessible" Error
**Issue**: ValueError when launching with server_name="0.0.0.0"
**Solution**: Changed to server_name="127.0.0.1" with fallback to "localhost"

### "Model not available" Error
1. Check LM Studio is running
2. Verify model is loaded
3. Test API: `curl http://127.0.0.1:1234/v1/models`

### Audio Generation Fails
1. Check console for token generation
2. Verify output directory permissions
3. Check available disk space

### Import Errors
1. Verify orpheus path exists
2. Check `gguf_orpheus.py` is present
3. Ensure `decoder.py` is in same directory

## Git Workflow

### Commit Conventions
```bash
git add .
git commit -m "type: description"
git push origin main
```

Types:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation
- `refactor:` Code restructuring
- `chore:` Maintenance

### Recent Commits
- `6c79691` fix: Python 3.13 compatibility and launch configuration (2025-05-23)
- `a04531b` refactor: migrate from Bastion API to local Orpheus model (2025-05-23)
- Previous commits from Bastion version preserved

## Testing Checklist
- [ ] LM Studio connection verified
- [ ] Text generation produces tokens
- [ ] Audio file created in outputs/
- [ ] UI displays audio player
- [ ] All voices tested
- [ ] Emotion tags working
- [ ] Error messages helpful

## Future Enhancements
1. **Presets**: Save common parameter combinations
2. **History**: Track generated files
3. **Batch**: Process multiple texts
4. **Export**: Different audio formats
5. **Preview**: Real-time parameter effects

## Notes for Next Developer
- Model path is hardcoded - consider making configurable
- Audio segments are processed in chunks of 7 tokens
- 27 tokens minimum before audio generation starts
- Outputs directory created automatically
- Consider adding progress indicators for long texts
