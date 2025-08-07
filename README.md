# 🚀 VRP Solver Backend Project

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-1a1a1a?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
</p>

This is a backend API for the **Vehicle Routing Problem (VRP) Solver** application. This API is responsible for handling business logic, data management, user authentication, and integration with external services for geocoding and route optimization.

## 🔑 Key Features

* **User Authentication**: Secure login system using JSON Web Tokens (JWT).
* **Admin Management**: Dedicated endpoints for administrative tasks.
* **Package Management (CRUD)**: Operations to create, read, update, and delete data packages to be sent.
* **Geocoding**: Converting physical addresses into geographic coordinates (latitude, longitude) using an external service.
* **Route Optimization**: Calculating the most efficient route for multiple vehicles from one depot to multiple delivery destinations.
* **GraphHopper Integration**: Using the GraphHopper API to calculate distance and time matrices between locations.

## 🛠 Tech Stack

* **Backend**: Flask
* **Database**: MySQL
* **External Services**:
  * **GraphHopper API**: For routing and distance matrix.
  * **SerpApi**: For converting addresses to coordinates.

## ⚙️ Local Installation & Configuration

Follow these steps to run this project in your local environment.

1.  **Clone Repository**

    ```bash
    git clone https://github.com/risyady/Project-VRP-Backend.git
    cd Project-VRP-Backend
    ```

2.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables**

    Copy the `.env.example` file to `.env` and fill in all the required variables.

    ```bash
    cp .env.example .env
    ```

    Open the `.env` file and fill in the values.

4.  **Run the Application**

    ```bash
    flask run
    ```

## 💻 Variabel Lingkungan (.env)

Berikut adalah penjelasan untuk setiap variabel di dalam file `.env`:

* `SECRET_KEY`: Kunci rahasia untuk keamanan aplikasi (misalnya untuk sesi).
* `JWT_SECRET_KEY`: Kunci rahasia khusus untuk menandatangani token JWT.
* `GRAPHHOPPER_API_KEY`: API Key untuk layanan GraphHopper.
* `SERPAPI_API_KEY`: API Key untuk layanan SerpApi.
* `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_HOST`: Kredensial dan informasi koneksi ke database MySQL.
* `DEPOT_COORDS`: Koordinat (latitude,longitude) dari depot atau titik awal.

---