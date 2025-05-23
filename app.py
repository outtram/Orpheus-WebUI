import gradio as gr
import json
from typing import Dict, List, Optional
import os
import sys
import time
import tempfile
import wave
import numpy as np
from dotenv import load_dotenv

# Add the orpheus-tts-local directory to Python path
ORPHEUS_PATH = "/Users/touttram/CODER4LIFE/Orpheus-Test-V1/orpheus-tts-local"
sys.path.insert(0, ORPHEUS_PATH)

# Import the local Orpheus model
try:
    from gguf_orpheus import (
        generate_speech_from_api,
        AVAILABLE_VOICES,
        DEFAULT_VOICE,
        TEMPERATURE,
        TOP_P,
        REPETITION_PENALTY,
        MAX_TOKENS
    )
    ORPHEUS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import local Orpheus model: {e}")
    ORPHEUS_AVAILABLE = False
    AVAILABLE_VOICES = ["tara", "jess", "leo", "leah", "dan", "mia", "zac", "zoe"]
    DEFAULT_VOICE = "tara"
    TEMPERATURE = 0.0
    TOP_P = 0.15
    REPETITION_PENALTY = 1.8
    MAX_TOKENS = 1200

# Load environment variables
load_dotenv()

# Available emotions from the model
EMOTIONS = ["laugh", "chuckle", "sigh", "cough", "sniffle", "groan", "yawn", "gasp"]

class OrpheusLocalClient:
    """Client for local Orpheus model"""
    
    def __init__(self):
        self.model_path = ORPHEUS_PATH
        self.check_model_availability()
    
    def check_model_availability(self):
        """Check if the local model is available"""
        if not ORPHEUS_AVAILABLE:
            return False, "Local Orpheus model not found at specified path"
        
        # Check if LM Studio is running
        import requests
        try:
            response = requests.get("http://127.0.0.1:1234/v1/models", timeout=2)
            if response.status_code == 200:
                return True, "Local model available and LM Studio is running"
            else:
                return False, "LM Studio is not responding correctly"
        except:
            return False, "LM Studio is not running. Please start LM Studio on port 1234"
    
    def generate_speech(
        self,
        text: str,
        voice: str = DEFAULT_VOICE,
        temperature: float = TEMPERATURE,
        top_p: float = TOP_P,
        repetition_penalty: float = REPETITION_PENALTY,
        max_tokens: int = MAX_TOKENS,
        emotion_tags: List[str] = None,
        output_file: Optional[str] = None
    ) -> Dict:
        """Generate speech using local Orpheus model"""
        
        # Add emotion tags to text if selected
        if emotion_tags:
            for emotion in emotion_tags:
                text = f"<{emotion}> {text}"
        
        # Generate unique output filename if not provided
        if not output_file:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f"{voice}_{timestamp}.wav")
        
        try:
            # Call the local model
            start_time = time.time()
            audio_segments = generate_speech_from_api(
                prompt=text,
                voice=voice,
                temperature=temperature,
                top_p=top_p,
                repetition_penalty=repetition_penalty,
                max_tokens=max_tokens,
                output_file=output_file
            )
            end_time = time.time()
            
            # Calculate duration
            duration = end_time - start_time
            
            return {
                "success": True,
                "output_file": output_file,
                "duration": duration,
                "voice": voice,
                "segments": len(audio_segments) if audio_segments else 0
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

# Initialize local client
client = OrpheusLocalClient()

def process_text(
    text: str,
    voice: str,
    temperature: float,
    top_p: float,
    repetition_penalty: float,
    max_tokens: int,
    add_emotions: List[str]
):
    """Process text and generate speech locally"""
    
    if not text.strip():
        return "Please enter some text", None, None
    
    # Check model availability
    available, status_msg = client.check_model_availability()
    if not available:
        return f"Model Error: {status_msg}", None, None
    
    # Generate speech
    result = client.generate_speech(
        text=text,
        voice=voice,
        temperature=temperature,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        max_tokens=max_tokens,
        emotion_tags=add_emotions
    )
    
    if result.get("success"):
        status = f"Generated successfully in {result['duration']:.2f}s"
        audio_file = result.get("output_file")
        return status, result, audio_file
    else:
        return f"Error: {result.get('error', 'Unknown error')}", result, None

def create_interface():
    """Create Gradio interface"""
    
    with gr.Blocks(title="Orpheus TTS WebUI - Local Model") as app:
        gr.Markdown("# Orpheus TTS WebUI - Local Model")
        gr.Markdown("Using local Orpheus model via LM Studio")
        
        with gr.Tabs():
            # Standard Generation Tab
            with gr.Tab("Text to Speech"):
                with gr.Row():
                    with gr.Column():
                        text_input = gr.Textbox(
                            label="Text",
                            placeholder="Enter text to convert to speech...",
                            lines=5
                        )
                        
                        voice_dropdown = gr.Dropdown(
                            choices=AVAILABLE_VOICES,
                            value=DEFAULT_VOICE,
                            label="Voice"
                        )
                        
                        emotion_checkboxes = gr.CheckboxGroup(
                            choices=EMOTIONS,
                            label="Emotions (optional)",
                            info="Add emotional expressions to the speech"
                        )
                        
                    with gr.Column():
                        temperature = gr.Slider(
                            minimum=0.0,
                            maximum=2.0,
                            value=TEMPERATURE,
                            step=0.1,
                            label="Temperature",
                            info="Controls randomness (0 = deterministic)"
                        )
                        
                        top_p = gr.Slider(
                            minimum=0.1,
                            maximum=1.0,
                            value=TOP_P,
                            step=0.05,
                            label="Top P",
                            info="Nucleus sampling threshold"
                        )
                        
                        repetition_penalty = gr.Slider(
                            minimum=1.0,
                            maximum=2.0,
                            value=REPETITION_PENALTY,
                            step=0.05,
                            label="Repetition Penalty",
                            info="Prevents repetitive output (>=1.1 recommended)"
                        )
                        
                        max_tokens = gr.Slider(
                            minimum=256,
                            maximum=2048,
                            value=MAX_TOKENS,
                            step=64,
                            label="Max Tokens",
                            info="Maximum output length"
                        )
                
                generate_btn = gr.Button("Generate Speech", variant="primary")
                
                with gr.Row():
                    status_output = gr.Textbox(label="Status", interactive=False)
                    audio_output = gr.Audio(label="Generated Audio", type="filepath")
                
                response_output = gr.JSON(label="Generation Details", visible=True)
                
                generate_btn.click(
                    fn=process_text,
                    inputs=[
                        text_input,
                        voice_dropdown,
                        temperature,
                        top_p,
                        repetition_penalty,
                        max_tokens,
                        emotion_checkboxes
                    ],
                    outputs=[status_output, response_output, audio_output]
                )
            
            # Long Form Tab
            with gr.Tab("Long Form Content"):
                gr.Markdown("### Coming Soon")
                gr.Markdown("Long-form content processing will be available after basic functionality is confirmed.")
            
            # Voice Samples Tab
            with gr.Tab("Voice Samples"):
                gr.Markdown("### Available Voices")
                gr.Markdown("Listed in order of conversational realism:")
                for i, voice in enumerate(AVAILABLE_VOICES):
                    marker = "★" if voice == DEFAULT_VOICE else "•"
                    gr.Markdown(f"{marker} **{voice}**" + (" (Recommended)" if voice == DEFAULT_VOICE else ""))
        
        # Info section
        with gr.Accordion("Model Configuration", open=False):
            available, status = client.check_model_availability()
            status_color = "green" if available else "red"
            
            gr.Markdown(f"""
            **Local Model Status:** <span style="color: {status_color}">{status}</span>
            
            **Configuration:**
            - Model Path: `{ORPHEUS_PATH}`
            - LM Studio URL: `http://127.0.0.1:1234`
            - Default Voice: `{DEFAULT_VOICE}`
            
            **Requirements:**
            1. LM Studio must be running on port 1234
            2. Orpheus model must be loaded in LM Studio
            3. Model: `orpheus-3b-0.1-ft-q4_k_m`
            
            **Emotion Tags:**
            You can add emotions by selecting them above or typing them directly:
            `<laugh>`, `<chuckle>`, `<sigh>`, `<cough>`, `<sniffle>`, `<groan>`, `<yawn>`, `<gasp>`
            """)
    
    return app

if __name__ == "__main__":
    # Check model availability on startup
    available, status = client.check_model_availability()
    print(f"Model Status: {status}")
    
    if not available:
        print("\n⚠️  WARNING: Model not available. Please ensure:")
        print("1. LM Studio is running on http://127.0.0.1:1234")
        print("2. The Orpheus model is loaded")
        print("\nThe interface will still start but generation will fail.\n")
    
    app = create_interface()
    try:
        # Try to launch with the fixed configuration
        app.launch(server_name="127.0.0.1", server_port=7860, share=False, quiet=False)
    except Exception as e:
        print(f"\nError launching app: {e}")
        print("\nTrying alternative launch configuration...")
        # Fallback launch configuration
        app.launch(server_name="localhost", server_port=7860, share=False, quiet=False)
