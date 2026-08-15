# WhatsApp Chat Analyzer

A lightweight Streamlit app for uploading and preprocessing WhatsApp chat exports and exploring the parsed data in a simple UI.

## Overview

This project reads a WhatsApp chat text export, cleans it into a structured dataframe, and prepares it for analysis. It is designed for quick local exploration of conversation patterns and message metadata.

## Features

- Upload a WhatsApp chat export file
- Parse message timestamps and sender information
- Identify group notifications separately
- Prepare a dataframe for downstream analysis
- Explore the cleaned data via a Streamlit sidebar UI

## Project Structure

- `app.py` - Streamlit application entry point
- `preprocessor.py` - message parsing and preprocessing logic
- `.gitignore` - excludes local environment and cache files from version control

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install streamlit pandas
   ```

3. Run the app:

   ```bash
   streamlit run app.py
   ```

4. Open the local URL shown in the terminal and upload your WhatsApp chat text file.

## Notes

- The app expects a standard WhatsApp chat export format with messages in the form:

  ```text
  01/01/2024, 10:30 - User Name: Hello world
  ```

- Group notifications are kept in the dataset under the `group_notification` label so they do not break the parsing flow.

## License

This project is for local use and experimentation.
