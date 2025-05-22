import gradio as gr
import httpx
import json
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OrpheusAPIClient:
    """Client for Bastion-hosted Orpheus model"""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.headers = {}
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'
    
    def generate_speech(
        self,
        text: str,
        voice: str = "tara",
        temperature: float = 0.9,
        top_p: float = 0.95,
        repetition_penalty: float = 1.1,
        max_tokens: int = 4096,
        emotion_tags: List[str] = None
    ) -> Dict:
        """Call Bastion API for speech generation"""
        
        # Format text with voice and emotion tags
        formatted_text = f"{voice}: {text}"
        
        payload = {
            "text": formatted_text,
            "temperature": temperature,
            "top_p": top_p,
            "repetition_penalty": repetition_penalty,
            "max_tokens": max_tokens
        }
        
        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(
                    f"{self.base_url}/generate",
                    json=payload,
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {"error": str(e)}

# Initialize API client
BASTION_URL = os.getenv("BASTION_URL", "https://bastion.example.com/orpheus")
API_KEY = os.getenv("BASTION_API_KEY", "")
client = OrpheusAPIClient(BASTION_URL, API_KEY)

# Available voices and emotions
VOICES = ["tara", "jess", "leo", "leah", "dan", "mia", "zac", "zoe"]
EMOTIONS = ["laugh", "chuckle", "sigh", "cough", "sniffle", "groan", "yawn", "gasp"]

def process_text(
    text: str,
    voice: str,
    temperature: float,
    top_p: float,
    repetition_penalty: float,
    max_tokens: int,
    add_emotions: List[str]
):
    """Process text and call API"""
    
    if not text.strip():
        return "Please enter some text", None
    
    # Add emotion tags to text if selected
    if add_emotions:
        for emotion in add_emotions:
            text = f"<{emotion}> {text}"
    
    # Call API
    result = client.generate_speech(
        text=text,
        voice=voice,
        temperature=temperature,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        max_tokens=max_tokens
    )
    
    if "error" in result:
        return f"Error: {result['error']}", None
    
    # Return response (audio processing would happen here)
    return f"Generated successfully for voice: {voice}", result

def create_interface():
    """Create Gradio interface"""
    
    with gr.Blocks(title="Orpheus TTS WebUI") as app:
        gr.Markdown("# Orpheus TTS WebUI")
        gr.Markdown("Connected to Bastion-hosted model")
        
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
                            choices=VOICES,
                            value="tara",
                            label="Voice"
                        )
                        
                        emotion_checkboxes = gr.CheckboxGroup(
                            choices=EMOTIONS,
                            label="Emotions (optional)"
                        )
                        
                    with gr.Column():
                        temperature = gr.Slider(
                            minimum=0.1,
                            maximum=2.0,
                            value=0.9,
                            step=0.1,
                            label="Temperature"
                        )
                        
                        top_p = gr.Slider(
                            minimum=0.1,
                            maximum=1.0,
                            value=0.95,
                            step=0.05,
                            label="Top P"
                        )
                        
                        repetition_penalty = gr.Slider(
                            minimum=1.0,
                            maximum=2.0,
                            value=1.1,
                            step=0.05,
                            label="Repetition Penalty"
                        )
                        
                        max_tokens = gr.Slider(
                            minimum=256,
                            maximum=8192,
                            value=4096,
                            step=256,
                            label="Max Tokens"
                        )
                
                generate_btn = gr.Button("Generate Speech", variant="primary")
                
                with gr.Row():
                    status_output = gr.Textbox(label="Status", interactive=False)
                    response_output = gr.JSON(label="API Response", visible=True)
                
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
                    outputs=[status_output, response_output]
                )
            
            # Long Form Tab
            with gr.Tab("Long Form Content"):
                gr.Markdown("### Coming Soon")
                gr.Markdown("Long-form content processing will be available after basic functionality is confirmed.")
        
        # Info section
        with gr.Accordion("API Configuration", open=False):
            gr.Markdown(f"""
            **Current Configuration:**
            - Bastion URL: `{BASTION_URL}`
            - API Key: {'Configured' if API_KEY else 'Not Set'}
            
            To change these, create a `.env` file with:
            ```
            BASTION_URL=your_bastion_url
            BASTION_API_KEY=your_api_key
            ```
            """)
    
    return app

if __name__ == "__main__":
    app = create_interface()
    app.launch(server_name="0.0.0.0", server_port=7860)
