from google.cloud.recaptchaenterprise_v1 import Assessment
from google.cloud import recaptchaenterprise_v1
import os

class RecaptchaManager:
    def __init__(self):
        self.google_project_id = os.environ["GOOGLE_PROJECT_ID"]
        self.google_recaptcha_site_key = os.environ["RECAPTCHA_SITE_KEY"]
    
    def create_assessment(
        self,
        token: str,
        recaptcha_action: str,
        user_ip_address: str,
        user_agent: str,
        ja3: str,
    ) -> Assessment:
        """Create an assessment to analyze the risk of a UI action.
        Args:
            token: The token obtained from the client on passing the recaptchaSiteKey.
            recaptcha_action: Action name corresponding to the token.
            user_ip_address: IP address of the user sending a request.
            user_agent: User agent is included in the HTTP request in the request header.
            ja3: JA3 associated with the request.
        """
        client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

        # Set the properties of the event to be tracked.
        event = recaptchaenterprise_v1.Event()
        event.site_key = self.google_recaptcha_site_key
        event.token = token
        event.user_ip_address = user_ip_address
        event.user_agent = user_agent
        event.ja3 = ja3

        assessment = recaptchaenterprise_v1.Assessment()
        assessment.event = event

        project_name = f"projects/{self.google_project_id}"

        # Build the assessment request.
        request = recaptchaenterprise_v1.CreateAssessmentRequest()
        request.assessment = assessment
        request.parent = project_name

        response = client.create_assessment(request)

        # Check if the token is valid.
        if not response.token_properties.valid:
            print(
                "The CreateAssessment call failed because the token was "
                + "invalid for for the following reasons: "
                + str(response.token_properties.invalid_reason)
            )
            return

        # Check if the expected action was executed.
        if response.token_properties.action != recaptcha_action:
            print(
                "The action attribute in your reCAPTCHA tag does"
                + "not match the action you are expecting to score"
            )
            return
        else:
            # Get the risk score and the reason(s)
            # For more information on interpreting the assessment,
            # see: https://cloud.google.com/recaptcha-enterprise/docs/interpret-assessment
            for reason in response.risk_analysis.reasons:
                print(reason)
            print(
                "The reCAPTCHA score for this token is: "
                + str(response.risk_analysis.score)
            )
            # Get the assessment name (id). Use this to annotate the assessment.
            assessment_name = client.parse_assessment_path(response.name).get("assessment")
            print(f"Assessment name: {assessment_name}")
        return response