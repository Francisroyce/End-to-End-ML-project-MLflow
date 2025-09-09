# End-to-End-ML-project-MLflow

## workflow

1. update config.yaml (after, define your constant)

2. update schema.yaml
3. update params.yaml
4. update the entity
5. update the configuration manager in src config
6. update the components
7. update the pipeline
8. update the main.py
9. update the app.py


mflow setup:


---

## **Step 0: Prerequisites**

Make sure you have **Python**, **pip**, and **git** installed, and you have access to your DagsHub repo:
`https://dagshub.com/Francisroyce/End-to-End-ML-project-MLflow`

---

## **Step 1: Install Dependencies**

Open a terminal and run:

```bash
pip install dagshub mlflow
```

This installs the DagsHub Python client and MLflow.

---

## **Step 2: Create a Personal Access Token (PAT) in DagsHub**

1. Go to [DagsHub Tokens](https://dagshub.com/user/settings/tokens)
2. Click **New Token** → Name it `"mlflow-token"`
3. Copy the token **somewhere safe**. You’ll use it as the password.

---

## **Step 3: Set up environment variables**

In your terminal, set your DagsHub username and token so MLflow can authenticate automatically:

```bash
export MLFLOW_TRACKING_USERNAME=Francisroyce
export MLFLOW_TRACKING_PASSWORD=your_token_here
```

> Replace `your_token_here` with the token you copied.

If you’re on **Windows Command Prompt**, use:

```cmd
set MLFLOW_TRACKING_USERNAME=Francisroyce
set MLFLOW_TRACKING_PASSWORD=your_token_here
```

---

## **Step 4: Initialize DagsHub in Python**

In a Python script or notebook:

```python
import dagshub

dagshub.init(
    repo_owner='Francisroyce',
    repo_name='End-to-End-ML-project-MLflow',
    mlflow=True
)
```

This connects MLflow tracking to your DagsHub repo.

---

## **Step 5: Log your first MLflow run**

```python
import mlflow

# Start a run
with mlflow.start_run():
    # Log parameters (hyperparameters)
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("optimizer", "adam")
    
    # Log metrics
    mlflow.log_metric("accuracy", 0.92)
    mlflow.log_metric("loss", 0.15)
```

---

## **Step 6: Log artifacts (optional, e.g., model file or plots)**

```python
# Example: logging a file
mlflow.log_artifact("example_model.pkl")  # Make sure this file exists
```

For saving and logging a **scikit-learn model**:

```python
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier()
# train your model here...
mlflow.sklearn.log_model(model, "random_forest_model")
```

---

## **Step 7: Check your runs on DagsHub**

Go to:
[https://dagshub.com/Francisroyce/End-to-End-ML-project-MLflow](https://dagshub.com/Francisroyce/End-to-End-ML-project-MLflow) → **Experiments**

You should see your run with parameters, metrics, and any artifacts you logged.

---

### Quick Test to Ensure Everything Works

```python
import mlflow

with mlflow.start_run():
    mlflow.log_param("test_param", 123)
    mlflow.log_metric("test_metric", 1.23)
print("Test run logged successfully!")
```

If you see it in DagsHub → Experiments, you’re fully set up.

---


# Wine Quality Prediction System

A professional, industrial-grade Flask web application for predicting wine quality based on physicochemical properties. This system uses machine learning to analyze wine characteristics and provide quality scores with confidence metrics.

## Features

### Core Functionality
- **Web Interface**: Professional, responsive web interface built with Bootstrap 5
- **Machine Learning Prediction**: Advanced prediction using trained Random Forest model
- **Real-time Validation**: Client-side and server-side input validation
- **Results Dashboard**: Comprehensive results display with quality metrics
- **API Endpoints**: RESTful API for programmatic access

### Professional Features
- **Industrial-grade Architecture**: Proper error handling, logging, and security
- **Responsive Design**: Mobile-first design with modern UI/UX
- **Accessibility**: WCAG compliant with keyboard navigation and screen reader support
- **Performance Optimized**: Efficient processing with caching and optimization
- **Production Ready**: Docker support, health checks, and monitoring

## Technical Stack

- **Backend**: Flask 2.3.3 with Python 3.9+
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript (ES6+)
- **Machine Learning**: scikit-learn, pandas, numpy
- **Deployment**: Docker, Gunicorn WSGI server
- **Security**: Input validation, CSRF protection, security headers

## Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager
- (Optional) Docker for containerized deployment

### Local Development Setup

1. **Clone the repository**:
```bash
git clone <repository-url>
cd wine-quality-prediction
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up directory structure**:
```
wine-quality-prediction/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── static/
│   ├── css/
│   │   └── styles.css    # Custom CSS styles
│   └── js/
│       └── script.js     # JavaScript functionality
├── templates/
│   ├── index.html        # Main prediction form
│   ├── result.html       # Results display
│   └── error.html        # Error pages
├── artifacts/
│   └── model_trainer/
│       └── randomforest.pkl  # Trained ML model
├── src/
│   └── my_project/
│       └── pipeline/
│           └── prediction.py  # Prediction pipeline
└── logs/                 # Application logs
```

5. **Configure environment variables** (optional):
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
export MODEL_PATH=artifacts/model_trainer/randomforest.pkl
```

6. **Run the application**:
```bash
python app.py
```

The application will be available at `http://localhost:8080`

### Docker Deployment

1. **Build Docker image**:
```bash
docker build -t wine-quality-predictor .
```

2. **Run container**:
```bash
docker run -p 8080:8080 wine-quality-predictor
```

3. **Run with volume mounting** (for persistent logs):
```bash
docker run -p 8080:8080 -v $(pwd)/logs:/app/logs wine-quality-predictor
```

## Usage

### Web Interface

1. **Access the application**: Navigate to `http://localhost:8080`
2. **Fill the form**: Enter wine characteristics in the prediction form
3. **Submit prediction**: Click "Predict Wine Quality" button
4. **View results**: Review the quality score, confidence metrics, and analysis

### API Usage

#### Prediction Endpoint
```bash
POST /api/predict
Content-Type: application/json

{
  "fixed_acidity": 7.4,
  "volatile_acidity": 0.7,
  "citric_acid": 0.0,
  "residual_sugar": 1.9,
  "chlorides": 0.076,
  "free_sulfur_dioxide": 11.0,
  "total_sulfur_dioxide": 34.0,
  "density": 0.9978,
  "pH": 3.51,
  "sulphates": 0.56,
  "alcohol": 9.4
}
```

#### Response Format
```json
{
  "prediction": 5.6,
  "confidence": 87.3,
  "processing_time_ms": 45.2,
  "quality_level": "Standard",
  "quality_description": "Acceptable - Below average quality",
  "timestamp": "2024-01-15T10:30:45",
  "status": "success"
}
```

#### Health Check
```bash
GET /health
```

#### API Information
```bash
GET /api/info
```

## Input Parameters

The system accepts the following wine characteristics:

| Parameter | Range | Unit | Description |
|-----------|-------|------|-------------|
| Fixed Acidity | 0-20 | g/dm³ | Non-volatile acids in wine |
| Volatile Acidity | 0-2 | g/dm³ | Amount of acetic acid |
| Citric Acid | 0-1 | g/dm³ | Freshness and flavor additive |
| Residual Sugar | 0-65 | g/dm³ | Sugar remaining after fermentation |
| Chlorides | 0-1 | g/dm³ | Amount of salt in wine |
| Free Sulfur Dioxide | 0-300 | mg/dm³ | Free form of SO2 |
| Total Sulfur Dioxide | 0-450 | mg/dm³ | Total SO2 content |
| Density | 0.9-1.1 | g/cm³ | Wine density |
| pH | 0-14 | pH | Acidity level |
| Sulphates | 0-2 | g/dm³ | Wine additive |
| Alcohol | 0-20 | % | Alcohol percentage |

## Quality Scoring

The system provides wine quality scores on a scale of 1-10:

- **9-10**: Outstanding/Excellent quality
- **7-8**: Very Good/Good quality  
- **5-6**: Fair/Average quality
- **3-4**: Poor/Bad quality
- **1-2**: Terrible/Awful quality

## Architecture

### Application Structure
```
├── Flask Application (app.py)
│   ├── Configuration Management
│   ├── Error Handling
│   ├── Logging System
│   ├── Security Headers
│   └── Route Handlers
├── Frontend (Templates + Static)
│   ├── Responsive UI Components
│   ├── Client-side Validation
│   ├── Interactive Features
│   └── Accessibility Support
├── Machine Learning Pipeline
│   ├── Input Validation
│   ├── Data Preprocessing
│   ├── Model Prediction
│   └── Result Processing
└── API Layer
    ├── RESTful Endpoints
    ├── JSON Response Format
    ├── Error Handling
    └── Documentation
```

### Security Features
- Input validation and sanitization
- CSRF protection
- Security headers (XSS, Content-Type, Frame Options)
- Rate limiting ready
- Error message sanitization
- Secure file handling

### Performance Features
- Efficient model loading
- Request/response logging
- Health monitoring
- Graceful error handling
- Optimized static assets
- Caching headers

## Configuration

### Environment Variables
- `FLASK_ENV`: Application environment (development/production)
- `FLASK_HOST`: Host address (default: 0.0.0.0)
- `FLASK_PORT`: Port number (default: 8080)
- `MODEL_PATH`: Path to ML model file
- `SECRET_KEY`: Flask secret key for sessions

### Production Configuration
For production deployment:
1. Set `FLASK_ENV=production`
2. Configure proper secret key
3. Set up reverse proxy (nginx/Apache)
4. Configure SSL/TLS certificates
5. Set up monitoring and logging aggregation
6. Configure backup and recovery procedures

## Monitoring & Logging

The application includes comprehensive logging:
- Request/response logging
- Error tracking
- Performance metrics
- Model prediction logging
- Health check endpoints

Log files are stored in the `logs/` directory and include:
- Application logs (`app.log`)
- Error logs (automatic)
- Access logs (when using gunicorn)

## Development

### Code Quality
The project follows Python best practices:
- PEP 8 style guide
- Type hints where appropriate
- Comprehensive error handling
- Docstring documentation
- Security considerations

### Testing
```bash
# Install development dependencies
pip install pytest pytest-flask

# Run tests
pytest tests/

# Run with coverage
pytest --cov=app tests/
```

### Contributing
1. Fork the repository
2. Create feature branch
3. Follow code style guidelines
4. Add tests for new features
5. Update documentation
6. Submit pull request

## Troubleshooting

### Common Issues

1. **Model file not found**:
   - Ensure `randomforest.pkl` exists in `artifacts/model_trainer/`
   - Check `MODEL_PATH` environment variable

2. **Import errors**:
   - Verify all dependencies are installed
   - Check Python path configuration
   - Ensure virtual environment is activated

3. **Port conflicts**:
   - Change port in configuration
   - Kill existing processes on port 8080

4. **Permission errors**:
   - Check file permissions
   - Run with appropriate user privileges
   - Verify directory creation permissions

### Debug Mode
Enable debug mode for development:
```bash
export FLASK_ENV=development
python app.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Check the troubleshooting section
- Review application logs
- Create an issue in the repository
- Contact the development team

## Version History

- **v1.0.0**: Initial release with core functionality
- **v1.1.0**: Added API endpoints and Docker support
- **v1.2.0**: Enhanced UI/UX and accessibility features
- **v2.0.0**: Professional industrial-grade implementation
