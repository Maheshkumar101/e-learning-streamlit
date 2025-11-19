🚀 Features


👨‍🏫 Admin Features


Add new courses with detailed information

Upload course thumbnails (JPG/PNG format)

Upload course materials (PDF files)

Cloud upload through Backblaze (optional integration)

Automatically updates courses.csv database

👨‍🎓 Student Features


User registration & login system

Explore available courses with rich previews

Enroll into courses with one click

View "My Courses" personalized dashboard

Open or download course PDF files directly

✨ UI/UX Features


Clean light-mode theme for optimal readability

Responsive grid layout for course displays

Card-based interface with modern design

"No image available" fallback for missing thumbnails

Modern fonts and spacing for enhanced user experience


🔧 Installation & Setup


1️⃣ Clone the repository
bash
git clone https://github.com/<your-username>/e-learning-streamlit.git
cd e-learning-streamlit
2️⃣ Create virtual environment
bash
python -m venv .venv
Activate it:

Windows:


bash
.venv\Scripts\Activate.ps1
macOS/Linux:

bash
source .venv/bin/activate
3️⃣ Install dependencies
bash
pip install -r requirements.txt
4️⃣ Run the app
bash
streamlit run streamlit_app.py --server.fileWatcherType=poll
🔐 Optional: Backblaze B2 Cloud Setup
For cloud storage functionality, create a .env file in the project root:

env
B2_KEY_ID=your_key_id
B2_APP_KEY=your_app_key
B2_BUCKET=e-learning-streamlit
B2_ENDPOINT=https://s3.us-east-005.backblazeb2.com
APP_SECRET=replace-with-any-random-string
Note: If .env is missing, the app automatically stores files locally.

👥 Demo Login Accounts
Role	Username	Password
Admin	admin_user	adminpass
Student	student_user	studentpass
You can also create new users directly through the app's registration system.

📚 Default Course List


The platform comes pre-loaded with popular courses:

Data Science

Cloud Computing

Environmental Studies

Machine Learning

Machine Learning Lab

Research Methodology & IPR

Thumbnails & PDFs can be:

Uploaded via Admin Panel

Placed manually in assets/thumbnails/ and assets/pdfs/ directories

Auto-downloaded using provided scripts

🧪 Useful Scripts


Add default courses
bash
python scripts/add_courses.py
Set local thumbnails
bash
python scripts/set_local_thumbnails.py
Auto-download Unsplash thumbnails
bash
python scripts/auto_download_thumbnails.py
Add PDFs & update CSV
bash
python scripts/add_pdfs_and_update.py
🛡️ Security Notes


.env file is ignored by Git (do NOT upload your Backblaze keys)

CSV files act as the mini-database for user management

If you accidentally pushed sensitive files → rotate the keys immediately

📦 Technologies Used


Python - Core programming language

Streamlit - Web application framework

Pandas - Data manipulation and analysis

Backblaze B2 - Optional cloud storage

HTML/CSS - Custom UI components and styling



📝 License
This project is open-source and free for academic usage.




https://screenshots/admin.png
Admin panel for course management

Happy Learning! 🎉

