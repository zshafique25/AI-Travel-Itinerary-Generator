import streamlit as st
from gemini_model import GeminiModel  # Placeholder for the actual import
from fpdf import FPDF
import datetime

# Custom CSS for the design system
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Overpass:wght@400;600&display=swap');

    body {
        font-family: 'Overpass', sans-serif;
        background-color: #2B2D42;
        color: #FA3E01;
    }
    .title {
        font-size: 2.5em;
        color: #FA3E01;
        text-align: center;
    }
    .subtitle {
        font-size: 1.5em;
        background: linear-gradient(90deg, #FF490E 0%, #FF7B02 100%);
        -webkit-background-clip: text;
        color: transparent;
        text-align: left;
        margin-bottom: 20px;
    }
    .container {
        padding: 20px;
        border-radius: 10px;
        background-color: #FF7B02;
    }
    .stButton>button {
        background: linear-gradient(90deg, #FF490E 0%, #FF7B02 100%);
        border: none;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
    }
    .stDownloadButton>button {
        background: linear-gradient(90deg, #FF490E 0%, #FF7B02 100%);
        border: none;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
    }
    .itinerary {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        color: #2B2D42;
    }
    .itinerary h3 {
        color: #FA3E01;
    }
    .itinerary h4 {
        color: #1B435A;
    }
    .itinerary p {
        font-style: italic;
    }
    .question {
        font-size: 1.3em;
        color: #FA3E01;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0F1116;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 0.9em;
    }
    .error {
        border: 2px solid red;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the logo
st.image("logo/hunza.ai.png", use_column_width=False, width=75)

# Title and Subtitle
#st.markdown('<div class="title">Hunza.ai</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Let 3M AI create your travel checklist in seconds</div>', unsafe_allow_html=True)


# Instructions
with st.expander("Instructions"):
    st.write("""
    1. Enter the travel destination.
    2. Provide the starting date.
    3. Provide the number of nights.
    4. Specify the trip type.
    5. Enter the group size.
    6. Provide any special considerations.
    """)

placeholder = st.empty()

# Initialize session state
if 'checklist' not in st.session_state:
    st.session_state['checklist'] = ""

gemini_model = GeminiModel()

# Function to infer season based on date
def infer_season(date):
    if date.month in [12, 1, 2]:
        return "Winter"
    elif date.month in [3, 4, 5]:
        return "Spring"
    elif date.month in [6, 7, 8]:
        return "Summer"
    elif date.month in [9, 10, 11]:
        return "Autumn"

# Generate PDF
def generate_pdf(checklist_text, logo_path):
     # Replace unsupported characters with alternatives
    checklist_text = checklist_text.replace('\u2013', '-').replace('\u2014', '--')

    subtitle = "\n\nNote: This checklist is AI-generated and may be subject to change."
    complete_text = checklist_text + subtitle
    
    class PDF(FPDF):
        def header(self):
            self.image(logo_path, 10, 8, 33)  # Adjust the position and size as needed
            self.set_font("Arial", 'B', 12)
            self.cell(0, 10, 'Itinerary', ln=True, align='C')
            self.ln(20)
    
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, complete_text.encode('latin-1', 'replace').decode('latin-1'))
    
    return pdf.output(dest='S').encode('latin-1')

def format_checklist(checklist):
    # Splitting the generated checklist by lines and reformatting it as HTML
    items = checklist.split('##')
    formatted_checklist = ""
    for item in items:
        if item.strip():
            formatted_checklist += f"<div class='itinerary'>{item.strip()}</div>"
    formatted_checklist += "<div class='itinerary'><p><em>Note: This checklist is AI-generated and may be subject to change.</em></p></div>"
    return formatted_checklist

# Function to make a field blink red
def blink_field(field_key):
    js_code = f"""
    <script>
    var field = document.querySelectorAll('[key="{field_key}"]');
    if (field.length > 0) {{
        for (var i = 0; i < 3; i++) {{
            setTimeout(function() {{ field[0].classList.add('error'); }}, i * 300);
            setTimeout(function() {{ field[0].classList.remove('error'); }}, i * 600 + 300);
        }}
    }}
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)

## Only show the form if the checklist hasn't been generated
if not st.session_state['checklist']:
    with placeholder.form(key='travel_form'):
        st.markdown('<div class="question">Where are you planning to travel in Pakistan?</div>', unsafe_allow_html=True)
        destination = st.text_input("", key="destination", label_visibility="hidden")

        st.markdown('<div class="question">When will your trip start?</div>', unsafe_allow_html=True)
        start_date = st.date_input("", key="start_date", label_visibility="hidden")

        st.markdown('<div class="question">How many nights will you be staying?</div>', unsafe_allow_html=True)
        nights = st.number_input("", key="nights", label_visibility="hidden", min_value=1)

        st.markdown('<div class="question">What type of trip are you planning?</div>', unsafe_allow_html=True)
        trip_type = st.selectbox("", ["Adventure", "Leisure", "Family", "Business"], key="trip_type", label_visibility="hidden")

        st.markdown('<div class="question">How many people are traveling with you?</div>', unsafe_allow_html=True)
        group_size = st.number_input("", key="group_size", label_visibility="hidden", min_value=1)

        st.markdown('<div class="question">Any special considerations?</div>', unsafe_allow_html=True)
        special_considerations = st.selectbox("", [
            "None",
            "I have a child with me",
            "I have a motor disability",
            "I have dietary restrictions (e.g., vegetarian, halal, gluten-free)",
            "I require wheelchair access",
            "I need medical assistance (e.g., carrying medications, first aid)",
            "I prefer low-altitude destinations",
            "I am traveling with a pet",
            "I have a fear of heights",
            "I prefer shorter walking distances",
            "I need quiet or noise-sensitive environments"
        ], key="special_considerations", label_visibility="hidden")

        submit_button = st.form_submit_button(label='Imagine Checklist')

    if submit_button:
        # Check for missing fields
        missing_fields = []
        if not destination:
            missing_fields.append("destination")
        if not start_date:
            missing_fields.append("start_date")
        if not nights:
            missing_fields.append("nights")
        if not trip_type:
            missing_fields.append("trip_type")
        if not group_size:
            missing_fields.append("group_size")
        if not special_considerations:
            missing_fields.append("special_considerations")

        if missing_fields:
            st.error("Missing information. Please fill in all fields.")
        else:
            responses = {
                'destination': destination,
                'start_date': start_date,
                'nights': nights,
                'trip_type': trip_type,
                'group_size': group_size,
                'special_considerations': special_considerations
            }
            st.session_state['responses'] = responses

            # Calculate the number of days based on start date and nights
            start_date = responses['start_date']
            nights = int(responses['nights'])
            end_date = start_date + datetime.timedelta(days=nights)
            num_days = (end_date - start_date).days + 1

            # Infer season based on start date
            inferred_season = infer_season(start_date)

            # Display the customizing message while generating the checklist
            st.write("Musafir AI is customizing your travel checklist.")

            st.session_state['prompt'] = gemini_model.create_checklist_prompt(responses, num_days, inferred_season)
            st.session_state['checklist'] = gemini_model.generate_checklist(st.session_state['prompt'])
            st.session_state['num_days'] = num_days
            st.session_state['inferred_season'] = inferred_season

            placeholder.empty()  # Clear the form once the checklist is generated


            

# Display the checklist if it has been generated
if st.session_state.get('checklist'):
    responses = st.session_state['responses']
    num_days = st.session_state['num_days']
    inferred_season = st.session_state['inferred_season']
    formatted_checklist = format_checklist(st.session_state['checklist'])
    
    # Display the checklist
    st.markdown(f'<div class="itinerary"><h4>Travel Checklist for {responses["destination"]} ({num_days} days, {inferred_season})</h4>{formatted_checklist}</div>', unsafe_allow_html=True)

    # Generate and provide a download link for the PDF
    logo_path = "logo/logo.png"
    pdf_content = generate_pdf(st.session_state['checklist'], logo_path)
    st.download_button(
        label="Download Checklist as PDF",
        data=pdf_content,
        file_name=f"checklist_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        mime="application/pdf"
    )


# Footer
st.markdown('<div class="footer">All rights reserved | Created by ADev</div>', unsafe_allow_html=True)

