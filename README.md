# Upload and Download file 

API upload file and download file converted to pdf 

# Cài đặt môi trường development

Requirements:
- Python 2.7
- Pip, Virtualenv, flask, urlparse
- gunicorn
- unoconv

- Trên Ubuntu

```
apt install unoconv libreoffice-script-provider-python
```

Khai báo báo env mới:

```
virtualenv .upload_env
source .upload_env/bin/activate
```

Cài các gói pip:

```
pip install -r requirements.txt
```

Khai báo File cấu hình:

```
cp app.yaml.example app.yaml
```

Sửa các giá trị trong file `app.yaml` theo đúng cấu hình cài đặt.


Run app ở chế độ `Development`:

```
python app.py
```

App được chạy ở port 5000.

# Cài đặt môi trường docker 

> Đảm bảo docker đã được cài đặt thành công.

Build image từ Dockerfile đã tạo:

```
sudo docker build -t doc-to-pdf .
```




Build và run ứng dụng với docker-compose:

```
sudo docker-compose up
```

