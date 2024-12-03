import math
from typing import Dict, List
from fpdf import FPDF

class MedicalDiagnosticAnalyzer:
    def __init__(self, condition_data: Dict[str, Dict[str, float]]):
        """
        Initialize with condition data loaded from JSON.

        :param condition_data: A dictionary containing condition names as keys
                               and symptom-weight mappings as values.
        """
        self.symptom_weights = condition_data

        print("Condition data loaded successfully.")  # Debug message

    def divide_patient_data(self, patient_symptoms: Dict[str, int]) -> List[Dict[str, float]]:
        """
        Divide patient symptoms into condition-specific subgroups.

        :param patient_symptoms: Dictionary of patient symptoms with severity.
        :return: List of symptom subgroups for each condition.
        """
        divided_symptoms = []
        
        for condition, weights in self.symptom_weights.items():
            relevant_symptoms = {}
            for symptom, severity in patient_symptoms.items():
                for weight in weights:
                    if("Symptom: "+weight==symptom):
                        relevant_symptoms[weight] = severity
            divided_symptoms.append((condition, relevant_symptoms))


        print(divided_symptoms)
        return divided_symptoms


    def conquer_condition(self, condition: str, symptoms: Dict[str, int]) -> Dict[str, float]:
        """
        Analyze symptoms for a specific medical condition.

        :param condition: The medical condition to analyze.
        :param symptoms: Patient symptoms for this condition.
        :return: Diagnostic analysis for the condition.
        """
        condition_weights = self.symptom_weights.get(condition, {})
        
        # Calculate weighted symptom score
        weighted_score = sum(
            symptoms.get(symptom, 0) * weight
            for symptom, weight in condition_weights.items()
        )
        
        # Sigmoid function to calculate confidence
        def calculate_confidence(weighted_score: float) -> float:
            return 1 / (1 + math.exp(-2 * (weighted_score - 0.5)))
        
        confidence=0
        if(weighted_score!=0):
            confidence = calculate_confidence(weighted_score)
        
        return {
            "condition": condition,
            "weighted_symptom_score": weighted_score,
            "diagnostic_confidence": confidence,
            "matched_symptoms": list(symptoms.keys())
        }

    def combine_diagnostic_results(self, condition_analyses: List[Dict[str, float]]) -> Dict[str, float]:
        """
        Combine diagnostic results from different condition analyses.

        :param condition_analyses: List of diagnostic analyses for each condition.
        :return: Comprehensive diagnostic summary.
        """
        # Sort conditions by diagnostic confidence in descending order
        sorted_conditions = sorted(
            condition_analyses,
            key=lambda x: x['diagnostic_confidence'],
            reverse=True
        )
        
        return {
            "top_conditions": [
                {"condition": result["condition"], "confidence": result["diagnostic_confidence"]}
                for result in sorted_conditions[:3]
            ],
            "max_confidence_condition": sorted_conditions[0]["condition"]
        }

    def diagnose_patient(self, patient_symptoms: Dict[str, int]) -> Dict[str, float]:
        """
        Perform comprehensive medical diagnosis.

        :param patient_symptoms: Dictionary of patient symptoms with severity.
        :return: Comprehensive diagnostic analysis.
        """
        # Divide patient symptoms for analysis
        divided_symptoms = self.divide_patient_data(patient_symptoms)
        
        # Analyze each condition
        condition_analyses = [
            self.conquer_condition(condition, symptoms)
            for condition, symptoms in divided_symptoms
        ]
        
        # Combine results
        comprehensive_diagnosis = self.combine_diagnostic_results(condition_analyses)
        return comprehensive_diagnosis
