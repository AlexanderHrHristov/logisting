🚚 Logisting






Logisting is a web application for managing suppliers and contracts in the logistics sector. It provides secure, role-based access and a scalable architecture built with Django. Ideal for logistics companies that need structured supplier and contract management.

🌟 Features

📦 Suppliers Management – Registry of essential goods suppliers: medicines, medical devices, supplements, cosmetics, organic products, controlled substances.

📄 Contracts Management – Legal users can create/edit contracts; Logistics and Managers can view; deletion restricted to Superusers.

🛠 Custom Admin Interface – Enhanced Django admin with branding, filters, search, and role-based access.

👥 User Roles – Superuser, Staff (Logistics / Legal), Regular User.

💻 Tech Stack
Layer	Technology
Backend	Django, Python
Frontend	Django Templates, Bootstrap
Database	SQLite (default, switchable to PostgreSQL/MySQL)
Auth & Permissions	Django authentication system, groups, custom permissions
🚀 Quick Start
# Clone repository
git clone [https://github.com/username/logisting.git](https://github.com/AlexanderHrHristov/logisting.git)
cd logisting

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver


Visit http://127.0.0.1:8000 to see the app in action.

📸 Demo / Screenshots

You can screenshots in screenshots/ folder:

🛣 Roadmap

REST API integration for external systems

Advanced analytics and reporting

UI/UX enhancements

📄 License

MIT License
