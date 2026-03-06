# Voice AI Hospital Appointment Agent

## Overview

This project implements a **Voice-based AI agent** that helps patients book, cancel, and reschedule hospital appointments through natural conversation.

The system uses speech recognition, an AI reasoning agent, and a scheduling backend to manage appointments automatically.

---

## Features

* Voice conversation interface
* AI-driven appointment booking
* Appointment cancellation
* Appointment rescheduling
* Conflict detection for double bookings
* Multilingual detection (English / Hindi / Tamil)
* Conversation memory
* Outbound reminder campaign
* Latency measurement
* FastAPI backend API

---

## System Architecture

Voice Input
↓
Speech-to-Text (Whisper)
↓
AI Agent (Gemini)
↓
Tool Execution
↓
SQLite Database
↓
Text-to-Speech
↓
Voice Response

---

## Project Structure

Voice-AI-Agent/

agent/
    voice_agent.py

backend/
    server.py

campaign/
    reminder_campaign.py

database/
    db.py
    init_db.py

memory/
    conversation_memory.py

tools/
    appointment_tools.py

voice/
    microphone_input.py
    speech_to_text.py
    text_to_speech.py
    test_voice_agent.py

clinic.db

requirements.txt

README.md

---

## Installation

Create virtual environment

pip install -r requirements.txt

---

## Run Voice Agent

python voice/test_voice_agent.py

Speak your request such as:

"Book cardiologist tomorrow at 10 for Imran"

---

## Run API Server

uvicorn backend.server:app --reload

Open:

http://127.0.0.1:8000/docs

---

## Run Reminder Campaign

python campaign/reminder_campaign.py

This simulates outbound reminder calls.

---

## Technologies Used

Python
FastAPI
Whisper Speech Recognition
Gemini AI
SQLite
Text-to-Speech

---

## Assignment Coverage

Voice conversation agent
Appointment lifecycle management
Conflict detection
Multilingual interaction
Contextual memory
Outbound reminder campaigns
Latency measurement

---

## Author

Mohammad Imtiyaz Khan
