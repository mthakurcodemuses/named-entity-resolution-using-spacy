import xml.etree.ElementTree as ET

from app.data_ingestion.models.call_transcript import CallTranscript
from app.data_ingestion.models.question_answer_content import QuestionAnswerContent


class TranscriptProcessor:
    def __init__(self, transcript: str):
        self.transcript = transcript

    def process(self) -> CallTranscript:
        root = ET.fromstring(self.transcript)

        # Extracting the metadata
        transcript_id = root.attrib['id']
        title = root.find('./meta/title').text
        company_id = root.find('./meta/companies/company').text
        date = root.find('./meta/date').text

        # Extracting the participant profiles
        participant_profiles = []
        for participant in root.findall('./meta/participants/participant'):
            participant_profiles.append({
                'id': participant.attrib['id'],
                'type': participant.attrib['type'],
                'name': participant.text.strip(),
                'affiliated_company': participant.attrib.get('affiliation', ''),
                'affiliated_company_id': participant.attrib.get('affiliation_entity', ''),
                'designation': participant.attrib.get('title', ''),
            })

        # Extracting the management section
        management_section = root.find("./body/section[@name='MANAGEMENT DISCUSSION SECTION']")
        management_section_content = ' '.join([p.text for p in management_section.findall('.//p')])

        # Extracting the question and answer section
        question_and_answer_section = root.find("./body/section[@name='Q&A']")
        question_and_answer_content = []
        current_question = None
        current_answers = []
        for speaker in question_and_answer_section.findall('.//speaker'):
            speaker_id = speaker.attrib['id']
            speaker_statement_type = speaker.attrib.get('type', '')
            for speaker_statement in speaker.findall('.//p'):
                # If a new question is encountered, store the previous Q&A pair if it exists
                if speaker_statement_type == 'q':
                    if current_question:
                        question_and_answer_content.append(
                            QuestionAnswerContent(question=current_question, question_participant_id=speaker_id,
                                                  answer=current_answers))
                    current_question = speaker_statement.text
                    current_answers = []
                elif speaker_statement_type == 'a':
                    current_answers.append(speaker_statement.text)

        # Placeholder for sentiment analysis (not implemented)
        sentiment = "neutral"

        # Creating the CallTranscript object
        call_transcript = CallTranscript(
            id=transcript_id,
            title=title,
            company_id=company_id,
            date=date,
            management_section_content=management_section_content,
            management_section_tags="",  # Placeholder, as tags are not provided in the XML
            sentiment=sentiment,
            question_and_answer_content=question_and_answer_content,
            participant_profiles=participant_profiles
        )

        return call_transcript
