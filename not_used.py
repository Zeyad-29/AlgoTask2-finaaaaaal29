from typing import List, Dict, Tuple
import math

class MedicalDiagnosticAnalyzer:
    def __init__(self, medical_conditions: List[str]):
        """
        Initialize diagnostic decision support system
        
        :param medical_conditions: List of potential medical conditions to diagnose
        """
        self.medical_conditions = medical_conditions
        self.symptom_weights = self._initialize_symptom_weights()
    
    def _initialize_symptom_weights(self) -> Dict[str, Dict[str, float]]:
        """
        Initialize weighted importance of symptoms for different conditions
        
        :return: Dictionary of symptom weights for each condition
        """
        # Example symptom weights (would be based on medical expertise)
        return {
            'Cardiovascular Disease': {
                'chest_pain': 0.3,
                'shortness_breath': 0.25,
                'irregular_heartbeat': 0.2,
                'high_blood_pressure': 0.15,
                'fatigue': 0.1
            },
            'Respiratory Disorder': {
                'persistent_cough': 0.3,
                'shortness_breath': 0.25,
                'chest_congestion': 0.2,
                'fever': 0.15,
                'wheezing': 0.1
            },
            'Neurological Condition': {
                'headaches': 0.3,
                'memory_loss': 0.25,
                'coordination_issues': 0.2,
                'sensory_changes': 0.15,
                'fatigue': 0.1
            }
        }
    
    def divide_patient_data(self, patient_symptoms: Dict[str, float]) -> List[Tuple[str, Dict[str, float]]]:
        """
        Divide patient symptoms into condition-specific subgroups
        
        :param patient_symptoms: Dictionary of patient symptoms and their severity
        :return: List of symptom subgroups for each potential condition
        """
        divided_symptoms = []
        
        for condition in self.symptom_weights:
            # Create an empty dictionary to store matching symptoms for this condition
            condition_symptoms = {}

            # Loop through each symptom the patient has
            for symptom, severity in patient_symptoms.items():
                # If the symptom is relevant to the current condition, add it
                if symptom in self.symptom_weights[condition]:
                    condition_symptoms[symptom] = severity

            # Add the condition and its matched symptoms to the result
            divided_symptoms.append((condition, condition_symptoms))

        
        return divided_symptoms
    
    def conquer_condition(self, condition: str, symptoms: Dict[str, float]) -> Dict[str, float]:
        """
        Analyze symptoms for a specific medical condition
        
        :param condition: Name of the medical condition
        :param symptoms: Patient symptoms for this condition
        :return: Diagnostic analysis for the condition
        """
        condition_weights = self.symptom_weights[condition]
        
        # Calculate weighted symptom score
        weighted_score = sum(
            symptoms.get(symptom, 0) * weight 
            for symptom, weight in condition_weights.items()
        )
        
        # Diagnostic confidence calculation
        def calculate_confidence(weighted_score: float) -> float:
            """
            Convert weighted score to diagnostic confidence
            Uses sigmoid function for smooth confidence scaling
            """
            return 1 / (1 + math.exp(-weighted_score + 1))
        
        return {
            'condition': condition,
            'weighted_symptom_score': weighted_score,
            'diagnostic_confidence': calculate_confidence(weighted_score),
            'matched_symptoms': list(symptoms.keys())
        }
    
    def combine_diagnostic_results(self, condition_analyses: List[Dict[str, float]]) -> Dict[str, float]:
        """
        Combine diagnostic results from different condition analyses
        
        :param condition_analyses: List of diagnostic analyses
        :return: Comprehensive diagnostic summary
        """
        # Sort conditions by diagnostic confidence
        sorted_conditions = sorted(
            condition_analyses, 
            key=lambda x: x['diagnostic_confidence'], 
            reverse=True
        )
        
        return {
            'top_conditions': [
                {
                    'condition': result['condition'],
                    'confidence': result['diagnostic_confidence']
                } 
                for result in sorted_conditions[:3]
            ],
            'max_confidence_condition': sorted_conditions[0]['condition'],
            'total_diagnostic_confidence': sum(
                result['diagnostic_confidence'] for result in condition_analyses
            )
        }
    
    def diagnose_patient(self, patient_symptoms: Dict[str, float]) -> Dict[str, float]:
        """
        Perform comprehensive medical diagnosis
        
        :param patient_symptoms: Dictionary of patient symptoms and severity
        :return: Comprehensive diagnostic analysis
        """
        # Divide
        divided_symptoms = self.divide_patient_data(patient_symptoms)
        
        # Conquer (analyze each condition)
        condition_analyses = [
            self.conquer_condition(condition, symptoms)
            for condition, symptoms in divided_symptoms
        ]
        
        # Combine results
        comprehensive_diagnosis = self.combine_diagnostic_results(condition_analyses)
        
        return comprehensive_diagnosis

def main():
    # Initialize diagnostic analyzer
    conditions = [
        'Cardiovascular Disease', 
        'Respiratory Disorder', 
        'Neurological Condition'
    ]
    diagnostic_analyzer = MedicalDiagnosticAnalyzer(conditions)
    
    # Example patient symptom scenarios
    patient_scenarios = [
        {
            'chest_pain': 0.7,
            'shortness_breath': 0.6,
            'irregular_heartbeat': 0.5,
            'fatigue': 0.4
        },
        {
            'persistent_cough': 0.8,
            'shortness_breath': 0.7,
            'fever': 0.5,
            'chest_congestion': 0.6
        },
        {
            'headaches': 0.6,
            'memory_loss': 0.5,
            'coordination_issues': 0.4,
            'fatigue': 0.3
        }
    ]
    
    # Diagnose each patient scenario
    for i, patient_symptoms in enumerate(patient_scenarios, 1):
        print(f"\nPatient {i} Diagnostic Analysis:")
        diagnosis = diagnostic_analyzer.diagnose_patient(patient_symptoms)
        
        print("Top Potential Conditions:")
        for condition in diagnosis['top_conditions']:
            print(f"- {condition['condition']}: {condition['confidence']:.2%} confidence")
        
        print(f"\nMost Likely Condition: {diagnosis['max_confidence_condition']}")
        print(f"Total Diagnostic Confidence: {diagnosis['total_diagnostic_confidence']:.2f}")

if __name__ == "__main__":
    main()