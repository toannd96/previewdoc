## Cài đặt môi trường development

Requirements:
- Python 2.7

- Trên Ubuntu

```
sudo apt install unoconv libreoffice-script-provider-python
```

Khai báo báo env mới:

```
virtualenv convert_env
source convert_env/bin/activate
```

Cài các gói phụ thuộc:

```
pip install -r requirements.txt
```

Sửa các giá trị trong file `app.yaml` theo cấu hình cài đặt.

Test app:

```
python test_resources.py
----------------------------------------------------------------------
Ran 3 tests in 1.068s

OK
```

Run app ở chế độ `Development`:

```
python app.py
```

App được chạy ở port 5000.

## Cài đặt môi trường docker 

> Đảm bảo docker đã được cài đặt thành công.

Build image từ Dockerfile đã tạo:

```
sudo docker build -t conv .
```

Build và run ứng dụng với docker-compose:

> Đảm bảo docker-compose đã được cài đặt thành công.

```
sudo docker-compose up
```

## Cách thức hoạt động:

GET:

- Get file from URL param
- Download file to folder upload
- Convert file to folder convert 
- Return view converted file on the browser

```
http://0.0.0.0:5000/uploads?file=http://home.actvn.edu.vn/Upload/document/don-hoan-thi.docx
```

POST:

- Get file upload via payload
- Download file to folder upload
- Convert file to folder convert 

``` 
Body: form-data key:file (Postman)
```
