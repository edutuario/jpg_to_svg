# Use the latest compatible Python image
FROM python:3.11

# Install necessary dependencies for building ImageMagick
RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libgif-dev \
    librsvg2-dev \
    potrace \
    && rm -rf /var/lib/apt/lists/*

# Set working directory to the 'app' folder
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install ImageMagick to a custom directory
RUN cd /tmp && \
    curl -L https://imagemagick.org/download/ImageMagick.tar.gz -o imagemagick.tar.gz && \
    tar -xvf imagemagick.tar.gz && \
    cd ImageMagick-* && \
    ./configure --prefix=/app/magick && \
    make && \
    make install

# Add the custom install folder to the PATH
ENV PATH="/app/magick/bin:${PATH}"

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory to 'app' folder inside the container
WORKDIR /app/app

# Expose port for Streamlit
EXPOSE 8501

# Define default command to run Streamlit app
CMD ["streamlit", "run", "app.py"]