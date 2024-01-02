# IVR Implementation : Blood Pressure

This repository contains the code for the Interactive Voice Response (IVR) implementation of the data pipeline to communicate Patient Generated Health Data (PGHD) pertaining to Blood Pressure (BP) to the VODAN-Africa data network. The details of the pipeline are described in Kievit et al., in prep. 

## Contents

/src
- /standard_responses
 - XML Responses to be sent to the Africa's Talking API Cloud. They describe what should be said during the call and what information should be collected.
- /vocab
 - Contains the relevant file(s) describing the FAIR-based vocabulary created for describing the PGHD for later interoperability.
- cedar_template.json
 - Empty CEDAR template instance based on the "Patient Generated Health Data: Blood Pressure" template available on CEDAR
- main.py
 - Handles incoming calls, routes users to the appropriate responses, and collects and sends the data
