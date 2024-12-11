import io
import requests
import asyncio
from PIL import Image
import streamlit as st

st.set_page_config(layout="wide")

class UI:
    def __init__(self):
        self.api_url = 'http://127.0.0.1:8000/{endpoint}'
        self.context_endpoint = 'get-context'
        self.caption_endpoint = 'get-caption'
        self.hashtags_endpoint = 'get-hashtags'

    async def get_context(self, uploaded_file):
        img_bytes = uploaded_file.read()
        img_str = img_bytes.decode('latin1')
        response = requests.post(self.api_url.format(endpoint=self.context_endpoint), json={'img_bytes': img_str})
        return response

    async def get_caption(self, context, mood_input):
        response = requests.post(self.api_url.format(endpoint=self.caption_endpoint), json={'context': context, 'mood': mood_input})
        return response

    async def get_hashtags(self, sentence):
        response = requests.post(self.api_url.format(endpoint=self.hashtags_endpoint), json={'sentence': sentence})
        return response

    def display(self):
        st.title("Handlo")
        st.markdown("### Upload an image, select your mood, and get personalized captions and hashtags!")

        left_col, right_col = st.columns([2, 3], gap="large")

        with left_col:
            uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
            process_file = uploaded_file
            mood_input = st.selectbox(
                "What's your mood?",
                ("Happy", "Sad", "Excited", "Angry", "Anxious", "Calm", "Confident", "Confused", "Frustrated", "Grateful", "Hopeful", "Bored", "Energetic", "Nervous", "Embarrassed", "Relaxed", "Lonely", "Curious", "Surprised", "Proud"),
                index=0
            )

            generate_caption_button = st.button("🎨 Generate Caption")


        if uploaded_file is not None:
            with right_col:
                with st.spinner('🔄 Uploading image...'):
                    # image = Image.open(uploaded_file)
                    # img_buffer = io.BytesIO()
                    # image.save(img_buffer, format="PNG")
                    # img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
                    try:
                        # image_html = f'''
                        #     <div id="image-container" style="width:100%; height:600px; overflow:auto; border:1px solid #ccc; padding:10px; display:flex; justify-content:center; align-items:center;">
                        #         <img id="scrollable-image" src="data:image/png;base64,{uploaded_file.read().decode('latin1')}" style="max-width:100%;"/>
                        #     </div>
                        #     <div style="text-align:center; margin-top:10px;">
                        #         <p>Uploaded Image.</p>
                        #     </div>
                        #     <script>
                        #         // Scroll to the center of the image when loaded
                        #         var container = document.getElementById('image-container');
                        #         var img = document.getElementById('scrollable-image');
                        #         img.onload = function() {{
                        #             container.scrollLeft = (img.width - container.clientWidth);
                        #         }};
                        #     </script>
                        # '''
                        # st.markdown(image_html, unsafe_allow_html=True)
                        # st.image(image, caption='Uploaded Image', use_column_width=True)
                        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
                    except Exception as e:
                        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

            with left_col:
                if generate_caption_button:
                    with st.spinner('💬 Generating caption...'):
                        context_response = asyncio.run(self.get_context(process_file))
                        if context_response.status_code == 200:
                            # st.write(context_response.json())   
                            context = context_response.json()['context']
                            st.session_state.context = context
                            caption_response = asyncio.run(self.get_caption(context, mood_input))
                            if caption_response.status_code == 200:
                                caption = caption_response.json()['captions'][0]
                                st.session_state.caption = caption 
                                st.markdown(f"### Generated Caption: \n**{st.session_state.caption }**")
                                
                                # if st.button("🏷️ Generate Hashtags"):
                                with st.spinner('🔗 Generating hashtags...'):
                                    hashtags_response = asyncio.run(self.get_hashtags(st.session_state.caption))
                                    # st.error(hashtags_response.json())
                                    if hashtags_response.status_code == 200:
                                        hashtags = hashtags_response.json()['hashtags']['response']
                                        st.markdown(f"""### Hashtags:
                                                        {hashtags}
                                                    """)
                                    
                                    else:
                                        st.error(f"Error: {hashtags_response.json()['error']}")
                            else:
                                st.error(f"Error: {caption_response.json()['error']}")
                        else:
                            st.error(f"Error: {context_response.json()['error']}")

        else:
            left_col.warning("Please upload an image file to proceed.")


if __name__ == '__main__':
    ui = UI()
    ui.display()
