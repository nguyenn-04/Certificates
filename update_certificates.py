import json
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def update_certificates():
    # Đọc thông tin xác thực từ secret
    credentials_info = json.loads(os.environ["GOOGLE_SHEETS_CREDENTIALS"])

    # Xác định phạm vi truy cập
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    # Xác thực và khởi tạo client
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        credentials_info, scope
    )
    client = gspread.authorize(credentials)

    # Mở Google Sheets bằng URL hoặc tên
    spreadsheet = client.open("My Certificates")
    sheet = spreadsheet.sheet1  # Mở sheet đầu tiên

    # Đọc dữ liệu từ sheet
    data = sheet.get_all_records()

    # Đảo ngược thứ tự dữ liệu để hiển thị từ mới nhất lên đầu
    data.reverse()

    # Tạo nội dung HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ha Trong Nguyen - Certificates</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }}
            .container {{
                max-width: 1200px;
                margin: auto;
                padding: 20px;
                background-color: white;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
            }}
            .profile-image {{
                width: 150px;
                height: 150px;
                border-radius: 50%;
                margin-bottom: 20px;
            }}
            .header {{
                text-align: center;
                margin-bottom: 40px;
            }}
            .header h1 {{
                margin: 0;
                font-size: 2.5em;
                color: #333;
            }}
            .header p {{
                margin: 10px 0;
                color: #777;
            }}
            .social-icons {{
                margin: 20px 0;
            }}
            .social-icons a {{
                margin: 0 10px;
                text-decoration: none;
            }}
            .social-icons img {{
                width: 30px;
                height: 30px;
            }}
            .badges {{
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
            }}
            .badge {{
                width: 45%;
                padding: 20px;
                margin-bottom: 20px;
                background-color: #f9f9f9;
                border: 2px solid #ddd;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s, border-color 0.3s;
            }}
            .badge:hover {{
                transform: translateY(-5px);
                border-color: #4285F4;
            }}
            .badge a {{
                text-decoration: none;
                color: #333;
                font-weight: bold;
                font-size: 1.2em;
            }}
            .badge a:hover {{
                text-decoration: underline;
            }}
            .badge p {{
                margin: 10px 0;
                color: #555;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="./Avatar.png" alt="Profile Image" class="profile-image">
                <h1>Mỹ Linh Phùng</h1>
                <p>This page displays the certificates and skills that I have achieved.</p>
                <div class="social-icons">
                    <a href="https://www.facebook.com/trongnguyen2304" target="_blank">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" alt="Facebook">
                    </a>
                    <a href="https://github.com/nguyenn-04" target="_blank">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub">
                    </a>
                    <a href="https://www.linkedin.com/in/htnguyen04/" target="_blank">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/e/e9/Linkedin_icon.svg" alt="LinkedIn">
                    </a>
                </div>
                <h2>Certificates</h2>
                <p>Total number of certificates: {len(data)}</p>
            </div>
            <div class="badges">
    """

    # Thêm thông tin chứng chỉ vào nội dung HTML
    for row in data:
        certificate_name = row["Certificate Name"]
        date_issued = row["Date Issued"]
        certificate_type = row["Certificate Type"]
        thumbnail_url = row["Thumbnail URL"]

        html_content += f"""
                    <div class="badge">
                        <a href="{thumbnail_url}" target="_blank">{certificate_name}</a>
                        <p>{certificate_type}</p>
                        <p>Date Issued: {date_issued}</p>
                    </div>
        """

    # Đóng thẻ HTML
    html_content += """
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    # Lưu nội dung HTML vào file với mã hóa utf-8
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    print("Certificates page created: index.html")


if __name__ == "__main__":
    update_certificates()
