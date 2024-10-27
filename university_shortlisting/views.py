from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UniversityShortlistInputSerializer
from .models import UniversityShortlistRequest
import cohere
from django.conf import settings

# Initialize Cohere client
co = cohere.Client(settings.COHERE_API_KEY)

class UniversityShortlistView(APIView):
    def generate_prompt(self, data):
        prompt = f"""
        Please provide a shortlist of universities for a student with the following profile:
        - Current CGPA: {data['cgpa']}
        - Current College: {data['current_college']}
        - Current Country: {data['current_country']}
        - Destination Country: {data['destination_country']}
        - Field of Study: {data.get('field_of_study', 'Not specified')}
        - Estimated Budget: ${data['estimated_budget']}

        Please provide a list of 5 universities that would be suitable for this student, 
        considering their academic background, budget, and preferred destination. 
        For each university, include:
        1. University name
        2. Location
        3. A brief explanation of why it's a good fit
        4. Estimated tuition cost
        """
        return prompt

    def post(self, request):
        serializer = UniversityShortlistInputSerializer(data=request.data)
        if serializer.is_valid():
            # Generate prompt for the LLM
            prompt = self.generate_prompt(serializer.validated_data)

            # Call the Cohere API
            try:
                response = co.generate(
                    model='command',
                    prompt=prompt,
                    max_tokens=1000,
                    temperature=0.7,
                    k=0,
                    stop_sequences=[],
                    return_likelihoods='NONE'
                )
                shortlist = response.generations[0].text

                # Save the request and result to the database
                shortlist_request = UniversityShortlistRequest.objects.create(
                    cgpa=serializer.validated_data['cgpa'],
                    current_college=serializer.validated_data['current_college'],
                    current_country=serializer.validated_data['current_country'],
                    destination_country=serializer.validated_data['destination_country'],
                    field_of_study=serializer.validated_data.get('field_of_study', ''),
                    estimated_budget=serializer.validated_data['estimated_budget'],
                    shortlist_result=shortlist
                )

                return Response({"shortlist": shortlist, "request_id": shortlist_request.id}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
