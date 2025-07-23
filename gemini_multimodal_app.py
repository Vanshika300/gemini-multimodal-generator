import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import tempfile
import os
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="Gemini Multimodal Generator",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = {}

def configure_gemini(api_key):
    """Configure Google Gemini API"""
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Error configuring Gemini API: {str(e)}")
        return False

def generate_text_with_gemini(prompt, model_name="gemini-1.5-flash"):
    """Generate text using Google Gemini"""
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating text: {str(e)}")
        return None

def generate_audio_from_text(text, language='en'):
    """Generate audio from text using gTTS"""
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
            return tmp_file.name
    except Exception as e:
        st.error(f"Error generating audio: {str(e)}")
        return None

def generate_image_prompt(user_prompt):
    """Generate detailed image prompts for external AI image generators"""
    try:
        enhanced_prompt = generate_text_with_gemini(
            f"""Create a detailed, professional image generation prompt based on this request: "{user_prompt}"

Please provide:
1. A detailed visual description (style, composition, lighting, colors)
2. Technical specifications (camera angle, art style, quality modifiers)
3. Mood and atmosphere details

Format the response as a single, comprehensive prompt that can be used directly in AI image generators like DALL-E, Midjourney, or Stable Diffusion.

Make it vivid, specific, and optimized for high-quality image generation."""
        )
        
        if enhanced_prompt:
            return enhanced_prompt
        else:
            return f"High-quality, detailed image of {user_prompt}, professional photography, 8K resolution, perfect lighting, vibrant colors"
    except Exception as e:
        st.error(f"Error generating image prompt: {str(e)}")
        return f"High-quality, detailed image of {user_prompt}, professional photography, 8K resolution, perfect lighting, vibrant colors"

def main():
    st.title("🤖 Gemini Multimodal Content Generator")
    st.markdown("Generate text, image prompts, and audio using Google Gemini API and other services")
    
    # Sidebar for API configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        api_key = st.text_input("Google Gemini API Key", type="password", help="Enter your Google Gemini API key")
        
        if api_key:
            if configure_gemini(api_key):
                st.success("✅ Gemini API configured successfully!")
            else:
                st.error("❌ Failed to configure Gemini API")
        
        st.markdown("---")
        st.markdown("### 🎨 Recommended AI Image Generators")
        st.markdown("""
        **Free Options:**
        - [Pollinations AI](https://pollinations.ai/)
        - [Craiyon](https://www.craiyon.com/)
        - [Leonardo AI](https://leonardo.ai/) (Free tier)
        
        **Premium Options:**
        - [DALL-E 3](https://openai.com/dall-e-3)
        - [Midjourney](https://midjourney.com/)
        - [Stable Diffusion](https://stability.ai/)
        """)
        
        st.markdown("---")
        st.markdown("### 📋 Instructions")
        st.markdown("""
        1. Enter your Google Gemini API key
        2. Choose the content type to generate
        3. Enter your prompt
        4. Click generate to create content
        """)
    
    if not api_key:
        st.warning("⚠️ Please enter your Google Gemini API key in the sidebar to continue.")
        st.markdown("""
        ### How to get your API key:
        1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Create a new API key
        3. Copy and paste it in the sidebar
        """)
        return
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Text Generation", "🎨 Image Prompt Generator", "🎵 Audio Generation", "🔄 Multi-Modal"])
    
    with tab1:
        st.header("📝 Text Generation")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            text_prompt = st.text_area(
                "Enter your text prompt:",
                placeholder="Write a short story about a robot learning to paint...",
                height=100
            )
            
            model_choice = st.selectbox(
                "Choose Gemini Model:",
                ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"]
            )
        
        with col2:
            st.markdown("### Settings")
            max_tokens = st.slider("Max Tokens", 100, 2000, 500)
            temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
        
        if st.button("🚀 Generate Text", key="text_gen"):
            if text_prompt:
                with st.spinner("Generating text..."):
                    generated_text = generate_text_with_gemini(text_prompt, model_choice)
                    if generated_text:
                        st.session_state.generated_content['text'] = generated_text
                        st.success("✅ Text generated successfully!")
                        
                        st.markdown("### Generated Text:")
                        st.markdown(f"```\n{generated_text}\n```")
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Text",
                            data=generated_text,
                            file_name=f"generated_text_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain"
                        )
            else:
                st.warning("Please enter a text prompt.")
    
    with tab2:
        st.header("🎨 Image Prompt Generator")
        st.info("📌 Generate optimized prompts for AI image generators like DALL-E, Midjourney, or Stable Diffusion")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            image_idea = st.text_area(
                "Describe your image idea:",
                placeholder="A futuristic cityscape with flying cars at sunset...",
                height=100
            )
        
        with col2:
            st.markdown("### Style Options")
            art_style = st.selectbox(
                "Art Style:",
                ["Photorealistic", "Digital Art", "Oil Painting", "Watercolor", "Anime/Manga", "Sketch", "3D Render", "Abstract", "Vintage", "Minimalist"]
            )
            
            quality_level = st.selectbox(
                "Quality Level:",
                ["Standard", "High Quality", "Ultra High Quality", "Professional"]
            )
        
        if st.button("🎨 Generate Image Prompt", key="image_prompt_gen"):
            if image_idea:
                with st.spinner("Creating optimized image prompt..."):
                    # Create a comprehensive prompt including style preferences
                    full_prompt = f"{image_idea}, {art_style.lower()} style"
                    
                    if quality_level == "High Quality":
                        full_prompt += ", high resolution, detailed"
                    elif quality_level == "Ultra High Quality":
                        full_prompt += ", 8K resolution, ultra detailed, masterpiece"
                    elif quality_level == "Professional":
                        full_prompt += ", professional photography, studio lighting, award winning"
                    
                    enhanced_prompt = generate_image_prompt(full_prompt)
                    
                    if enhanced_prompt:
                        st.session_state.generated_content['image_prompt'] = enhanced_prompt
                        st.success("✅ Image prompt generated successfully!")
                        
                        st.markdown("### 🎯 Optimized Image Prompt:")
                        st.markdown(f"```\n{enhanced_prompt}\n```")
                        
                        # Copy to clipboard section
                        st.markdown("### 📋 Ready to Use:")
                        st.code(enhanced_prompt, language="text")
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Image Prompt",
                            data=enhanced_prompt,
                            file_name=f"image_prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain"
                        )
                        
                        # Quick links to image generators
                        st.markdown("### 🚀 Generate Your Image:")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown(f"[🎨 Pollinations AI](https://pollinations.ai/)")
                        with col2:
                            st.markdown(f"[🎨 Craiyon](https://www.craiyon.com/)")
                        with col3:
                            st.markdown(f"[🎨 Leonardo AI](https://leonardo.ai/)")
                        
                        # Instructions
                        st.markdown("### 💡 How to Use:")
                        st.markdown("""
                        1. **Copy** the generated prompt above
                        2. **Visit** one of the AI image generators
                        3. **Paste** the prompt into their input field
                        4. **Generate** your image!
                        
                        **Pro Tips:**
                        - For Midjourney: Add `--ar 16:9` for widescreen or `--ar 1:1` for square
                        - For DALL-E: The prompt works as-is
                        - For Stable Diffusion: You can add negative prompts to avoid unwanted elements
                        """)
            else:
                st.warning("Please describe your image idea.")
    
    with tab3:
        st.header("🎵 Audio Generation")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            audio_text = st.text_area(
                "Enter text to convert to audio:",
                placeholder="Hello! This is a text-to-speech demonstration using Google Text-to-Speech...",
                height=100
            )
        
        with col2:
            st.markdown("### Audio Settings")
            language = st.selectbox(
                "Language",
                [
                    ("English", "en"),
                    ("Spanish", "es"),
                    ("French", "fr"),
                    ("German", "de"),
                    ("Italian", "it"),
                    ("Portuguese", "pt"),
                    ("Russian", "ru"),
                    ("Japanese", "ja"),
                    ("Korean", "ko"),
                    ("Chinese", "zh")
                ],
                format_func=lambda x: x[0]
            )
        
        enhance_audio = st.checkbox("Enhance text with Gemini", key="enhance_audio")
        
        if st.button("🎤 Generate Audio", key="audio_gen"):
            if audio_text:
                with st.spinner("Generating audio..."):
                    final_text = audio_text
                    
                    # Optionally enhance the text with Gemini first
                    if enhance_audio:
                        enhanced_text = generate_text_with_gemini(
                            f"Improve this text for text-to-speech, making it more natural and engaging while keeping the same meaning: {audio_text}"
                        )
                        if enhanced_text:
                            final_text = enhanced_text
                            st.markdown("### Enhanced Text:")
                            st.write(final_text)
                    
                    audio_file = generate_audio_from_text(final_text, language[1])
                    
                    if audio_file:
                        st.session_state.generated_content['audio'] = audio_file
                        st.success("✅ Audio generated successfully!")
                        
                        st.markdown("### Generated Audio:")
                        st.audio(audio_file)
                        
                        # Read file for download
                        with open(audio_file, 'rb') as f:
                            audio_bytes = f.read()
                        
                        st.download_button(
                            label="📥 Download Audio",
                            data=audio_bytes,
                            file_name=f"generated_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3",
                            mime="audio/mpeg"
                        )
                        
                        # Clean up temporary file
                        try:
                            os.unlink(audio_file)
                        except:
                            pass
            else:
                st.warning("Please enter text to convert to audio.")
    
    with tab4:
        st.header("🔄 Multi-Modal Generation")
        st.markdown("Generate text, image prompt, and audio all at once from a single prompt!")
        
        multimodal_prompt = st.text_area(
            "Enter your multi-modal prompt:",
            placeholder="Create a story about a magical forest, with a description for an image and narration for audio...",
            height=120
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            generate_text_mm = st.checkbox("📝 Generate Text", value=True)
        with col2:
            generate_image_prompt_mm = st.checkbox("🎨 Generate Image Prompt", value=True)
        with col3:
            generate_audio_mm = st.checkbox("🎵 Generate Audio", value=True)
        
        if st.button("🚀 Generate All Content", key="multimodal_gen"):
            if multimodal_prompt:
                results = {}
                
                # Generate text content
                if generate_text_mm:
                    with st.spinner("Generating text content..."):
                        text_content = generate_text_with_gemini(multimodal_prompt)
                        if text_content:
                            results['text'] = text_content
                
                # Generate image prompt
                if generate_image_prompt_mm:
                    with st.spinner("Generating image prompt..."):
                        # Create image prompt from the main prompt
                        image_prompt_enhanced = generate_image_prompt(multimodal_prompt)
                        if image_prompt_enhanced:
                            results['image_prompt'] = image_prompt_enhanced
                
                # Generate audio
                if generate_audio_mm:
                    with st.spinner("Generating audio..."):
                        # Use the generated text or original prompt for audio
                        audio_text = results.get('text', multimodal_prompt)
                        audio_content = generate_audio_from_text(audio_text[:500])  # Limit length
                        if audio_content:
                            results['audio'] = audio_content
                
                # Display results
                if results:
                    st.success("✅ Multi-modal content generated!")
                    
                    if 'text' in results:
                        st.markdown("### 📝 Generated Text:")
                        st.markdown(results['text'])
                        
                        # Download button for text
                        st.download_button(
                            label="📥 Download Text",
                            data=results['text'],
                            file_name=f"multimodal_text_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            key="download_mm_text"
                        )
                    
                    if 'image_prompt' in results:
                        st.markdown("### 🎨 Generated Image Prompt:")
                        st.code(results['image_prompt'], language="text")
                        
                        # Download button for image prompt
                        st.download_button(
                            label="📥 Download Image Prompt",
                            data=results['image_prompt'],
                            file_name=f"multimodal_image_prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            key="download_mm_image_prompt"
                        )
                        
                        # Quick links for image generation
                        st.markdown("**🚀 Generate Image:** [Pollinations AI](https://pollinations.ai/) | [Craiyon](https://www.craiyon.com/) | [Leonardo AI](https://leonardo.ai/)")
                    
                    if 'audio' in results:
                        st.markdown("### 🎵 Generated Audio:")
                        st.audio(results['audio'])
                        
                        # Download button for audio
                        with open(results['audio'], 'rb') as f:
                            audio_bytes = f.read()
                        
                        st.download_button(
                            label="📥 Download Audio",
                            data=audio_bytes,
                            file_name=f"multimodal_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3",
                            mime="audio/mpeg",
                            key="download_mm_audio"
                        )
                        
                        # Clean up audio file
                        try:
                            os.unlink(results['audio'])
                        except:
                            pass
            else:
                st.warning("Please enter a multi-modal prompt.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🤖 Gemini Multimodal Content Generator | Built with Streamlit & Google Gemini API</p>
        <p>⚠️ Remember to keep your API keys secure and never share them publicly!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
