class RecommendationEngine:

    def generate(self, result):

        recommendations = []

        if result.skill_score < 80:
            recommendations.append(
                "Add more job-specific skills to your resume."
            )

        if result.certification_score < 70:
            recommendations.append(
                "Highlight relevant certifications."
            )

        if result.experience_score < 70:
            recommendations.append(
                "Quantify achievements with measurable results."
            )

        if not recommendations:
            recommendations.append(
                "Excellent match. Only minor improvements are recommended."
            )

        return recommendations