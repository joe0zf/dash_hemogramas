# HemoVet Dashboard

An interactive Streamlit dashboard built on 500 veterinary blood count (CBC) samples, exploring anemia and other hematological findings across dogs, cats, and other species.

## Installation

Make sure you have Python 3.13+ installed.

1. **Clone the repository**
```bash
   git clone https://github.com/joe0zf/dash_hemogramas.git
   cd dash_hemogramas
```

2. **Create a virtual environment** (named `.venv`, at the project root)
```bash
   python -m venv .venv
```

3. **Activate the virtual environment**

   On Windows:
```bash
   .venv\Scripts\activate
```

   On macOS / Linux:
```bash
   source .venv/bin/activate
```

4. **Install the dependencies**
```bash
   pip install -r requirements.txt
```

5. **Run the app**
```bash
   streamlit run app.py
```

   The dashboard will open in your browser at `http://localhost:8501`.

## Folder Structure

```
hemovet-dashboard/
├── .venv/        # Virtual environment (not tracked by Git)
├── data/         # Raw dataset (read-only)
├── src/          # Shared, importable logic (data loading, transforms, components)
├── pages/        # Dashboard sections — one file per collaborator
└── assets/       # Static files (logo, images, styles)
```

## Data Sources
| File Name                                   | Source                      | Source Link                                              |
|---------------------------------------------|-----------------------------|----------------------------------------------------------|
| hemogramas_vet.csv| | |