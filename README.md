# Financial Health Score Calculator

## Description
This Django project serves as a Financial Health Calculator. It takes monthly income, assets, debt and expense as and inputs and give the calculation of the Financial Health Score.

## Installation

### Prerequisites
- Python 3.10
- Django 4.2.7

### Installation Steps
1. Clone the repository: 
    ```bash
    git clone https://github.com/the0therguy/financial_health_calculator.git
    ```
2. Navigate to the project directory:
    ```bash
    cd financial_health_calculator
    ```
3. Create a virtual environment:
    ```bash
    python -m venv env
    ```
4. Activate the virtual environment:
    - On Windows:
        ```bash
        env\Scripts\activate
        ```
    - On macOS and Linux:
        ```bash
        source env/bin/activate
        ```
5. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Database Setup
1. Make migrations:
    ```bash
    python manage.py makemigrations
    ```
2. Apply migrations:
    ```bash
    python manage.py migrate
    ```

### Environment Variables
Create a `.env` file in the project root and add necessary variables like `EMAIL_HOST`, `DEBUG`, etc.

## Usage
Run the development server:
```bash
python manage.py runserver
```
The server will start at `http://127.0.0.1:8000/`.

## Contact
For any inquiries, reach out to email: ifty545@gmail.com.
