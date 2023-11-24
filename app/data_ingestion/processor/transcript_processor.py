import xml.etree.ElementTree as ET
class TranscriptProcessor:
    def __init__(self, transcript: str):
        self.transcript = transcript

    def process(self):
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
        for speaker in question_and_answer_section.findall('.//speaker'):
            speaker_id = speaker.attrib['id']
            speaker_statement_type = speaker.attrib.get('type', '')
            for speaker_statement in speaker.findall('.//p'):
                if speaker_statement.type == 'q':
                    question = speaker_statement.text
                elif speaker_statement.type == 'a':
                    answer = speaker_statement.text
                    question_and_answer_content.append({
                        'question': question,
                        'question_participant_id': speaker_id,
                        'answer': answer,
                        'answer_participant_id': speaker_id,
                    })
