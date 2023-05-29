# Gunakan base image Python 3.9
FROM python:3.9

# Set working directory
WORKDIR /app

# Salin file requirements.txt ke dalam container
COPY requirements.txt .

# Install dependensi aplikasi
RUN pip install --no-cache-dir -r requirements.txt

# Salin kode aplikasi ke dalam container
COPY . .

# Jalankan aplikasi FastAPI ketika container dijalankan
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
