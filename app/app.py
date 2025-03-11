import streamlit as st
from jpg_to_svg_converter import convert_image_to_svg  
import os
import time

def main():

    # Set the page title
    st.set_page_config(page_title="JPG to SVG Converter", page_icon="🖼️")

    # Title
    st.title("JPG to SVG Converter")
    st.write("Upload your JPG or JPEG image to convert it into an SVG.")

    # File uploader
    uploaded_file = st.file_uploader("Choose a JPG or JPEG file", type=["jpg", "jpeg"])

    if uploaded_file is not None:
        # Display image preview
        st.image(uploaded_file, caption="Uploaded Image.", use_container_width=True)

        # Save the uploaded file locally
        with open("temp_image.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Convert the image to SVG when the button is clicked
        if st.button("Convert to SVG"):
            # Set the file path
            input_path = "temp_image.jpg"
            output_image_name = "output_image"
            output_path = output_image_name  + ".svg"

            # List of files to remove after conversion
            files_to_remove = [
                "temp_image.jpg",
                "output_image.jpeg",
                "output_image.pbm",
                "output_image.svg"
            ]

            # Convert the image to SVG using the function you created
            try:
                convert_image_to_svg(input_path, output_image_name)
                st.success("Conversion successful! SVG saved as 'output_image.svg'.")

                # Offer the user a download link
                with open(output_path, "rb") as file:
                    btn = st.download_button(
                        label="Download SVG",
                        data=file,
                        file_name="output_image.svg",
                        mime="image/svg+xml"
                    )

                    # Wait some time before triggering temp file deletion
                    time.sleep(5)
                    # Clean up the temporary file after conversion
                    # Remove files only if they exist
                    for file in files_to_remove:
                        if os.path.exists(file):
                            os.remove(file)




            except Exception as e:
                for file in files_to_remove:
                    if os.path.exists(file):
                        os.remove(file)
                st.error(f"Error during conversion: {e}")

            
            

if __name__ == "__main__":
    main()
