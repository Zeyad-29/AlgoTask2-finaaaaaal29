import os
import json
from flask import Flask, render_template, request, session, jsonify
from MedicalDiagnosticAnalyzer import MedicalDiagnosticAnalyzer
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

@app.route('/', methods=['GET', 'POST'])
def home():
    # Load symptom weights and names from JSON file
    with open('conditions_and_symptoms.json') as f:
        data = json.load(f)
    medical_conditions = data['conditions']
    symptom_names = data['symptoms']
    
    # Initialize diagnostic analyzer
    diagnostic_analyzer = MedicalDiagnosticAnalyzer(medical_conditions)

    if request.method == 'POST':
        # Extract form data
        patient_name = request.form['name']
        patient_age = request.form['age']
        patient_sex = request.form['sex']  # Correct field name for gender
        
        # Extract selected symptoms from the textarea
        symptom_data = request.form['selectedSymptoms'].split("\n")
        
        # Process symptoms to include severity (divide severity by 10)
        patient_symptoms = {}
        for symptom in symptom_data:
            if symptom.strip():
                # Extract the symptom and severity
                symptom_name, severity = symptom.split(", Severity: ")
                severity = int(severity) / 10  # Divide severity by 10
                patient_symptoms[symptom_name.strip()] = severity

        # Store the patient data in the session
        patient_data = {
            "name": patient_name,
            "age": patient_age,
            "sex": patient_sex,
            "symptoms": patient_symptoms
        }
        
        # Save patient data in session
        session['patient_data'] = patient_data
        
        # Get the diagnosis results
        diagnosis = diagnostic_analyzer.diagnose_patient(patient_symptoms)

        # Generate the PDF with patient data and diagnosis
        pdf_path = generate_pdf(patient_data, diagnosis)

        # Respond back with diagnostic results and PDF path
        return render_template(
            'index.html',
            symptoms=symptom_names,
            patient_data=patient_data,
            diagnosis=diagnosis,
            pdf_path=pdf_path  # Send the path of the generated PDF
        )
    
    # If GET request, just render the form
    return render_template('index.html', symptoms=symptom_names)



def generate_pdf(patient_data, diagnosis):
    """
    Generate a PDF report for the patient with their diagnosis details.

    :param patient_data: Dictionary containing patient details (name, age, sex, symptoms).
    :param diagnosis: Dictionary containing diagnostic results.
    :return: Path to the generated PDF file.
    """
    try:
        # Create a PDF instance
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add title
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(0, 10, "Medical Diagnosis Report", ln=True, align="C")
        pdf.ln(10)

        # Add patient details
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Patient Name: {patient_data['name']}", ln=True)
        pdf.cell(0, 10, f"Patient Age: {patient_data['age']}", ln=True)
        pdf.cell(0, 10, f"Patient Sex: {patient_data['sex']}", ln=True)
        pdf.ln(10)

        # Add symptoms
        pdf.cell(0, 10, "Symptoms and Severity:", ln=True)
        for symptom, severity in patient_data['symptoms'].items():
            pdf.cell(0, 10, f"  - {symptom}: Severity {severity}", ln=True)
        pdf.ln(10)

        # Add diagnostic results
        pdf.cell(0, 10, "Diagnostic Results:", ln=True)
        for condition in diagnosis['top_conditions']:
            pdf.cell(0, 10, f"  - {condition['condition']}: {condition['confidence'] * 100:.2f}% confidence", ln=True)
        pdf.ln(10)
        pdf.cell(0, 10, f"Most Likely Condition: {diagnosis['max_confidence_condition']}", ln=True)

        # Ensure the static folder exists
        pdf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'pdfs')
        os.makedirs(pdf_dir, exist_ok=True)

        # Save the PDF to a file
        pdf_output_path = os.path.join(pdf_dir, f"{patient_data['name']}_diagnostic_report.pdf")
        pdf.output(pdf_output_path)

        print(f"PDF generated and saved to {pdf_output_path}")  # Debug
        return f"/static/pdfs/{patient_data['name']}_diagnostic_report.pdf"  # Serve it through the static folder
    except Exception as e:
        print(f"Error during PDF generation: {e}")  # Debug
        return None


if __name__ == "__main__":
    app.run(debug=True)