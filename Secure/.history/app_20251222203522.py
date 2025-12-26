"""
MediNomix - Advanced AI Medication Safety Platform
PROFESSIONAL UI with premium animations, gradients, and modern design
FUNCTIONALITY: 100% preserved with enhanced UI
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np
import time

# Page configuration - Premium
st.set_page_config(
    page_title="MediNomix | AI-Powered Medication Safety",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/precious-05/MediNomix',
        'Report a bug': "https://github.com/precious-05/MediNomix/issues",
        'About': "### MediNomix AI v3.0\nAdvanced Medication Safety Platform"
    }
)

# Backend URL
BACKEND_URL = "http://localhost:8000"

# Premium Healthcare AI Theme with Vibrant Gradients
COLORS = {
    "primary": "#4F46E5",        # Indigo
    "secondary": "#0EA5E9",      # Sky Blue
    "accent": "#8B5CF6",         # Violet
    "critical": "#EC4899",       # Pink-Magenta
    "high": "#F59E0B",           # Amber
    "medium": "#8B5CF6",         # Violet
    "low": "#10B981",           # Emerald
    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "surface": "linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)",
    "card_gradient": "linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%)",
    "text_primary": "#1e293b",
    "text_secondary": "#64748b",
    "button_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 50%, #8B5CF6 100%)",
}

# Base64 Encoded FontAwesome Icons (High Quality)
ICONS = {
    "logo": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDJMMiA3VjE3TDEyIDIyTDIyIDE3VjciIHN0cm9rZT0idXJsKCNncmFkaWVudDApIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8cGF0aCBkPSJNMiA3TDEyIDEyIiBzdHJva2U9InVybCgjZ3JhZGllbnQwKSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPHBhdGggZD0iTTEyIDEyTDIyIDciIHN0cm9rZT0idXJsKCNncmFkaWVudDApIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8cGF0aCBkPSJNMTIgMTJWMTYuNSIgc3Ryb2tlPSJ1cmwoI2dyYWRpZW50MCkiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+CjxwYXRoIGQ9Ik05IDE2LjVIMTUiIHN0cm9rZT0idXJsKCNncmFkaWVudDApIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8ZGVmcz4KPGxpbmVhckdyYWRpZW50IGlkPSJncmFkaWVudDAiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgo8c3RvcCBvZmZzZXQ9IjAlIiBzdG9wLWNvbG9yPSIjNjY3RUVBIi8+CjxzdG9wIG9mZnNldD0iMTAwJSIgc3RvcC1jb2xvcj0iIzc2NEJBMiIvPgo8L2xpbmVhckdyYWRpZW50Pgo8L2RlZnM+Cjwvc3ZnPgo=",
    "pill": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMTAiIGZpbGw9InVybCgjZ3JhZGllbnQwKSIvPgo8cGF0aCBkPSJNMTYgOEw4IDE2IiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+CjxwYXRoIGQ9Ik0xNSAxNUM5IDE1IDE1IDkgMTUgOSIgc3Ryb2tlPSIjZmZmZmZmIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8ZGVmcz4KPGxpbmVhckdyYWRpZW50IGlkPSJncmFkaWVudDAiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgo8c3RvcCBvZmZzZXQ9IjAlIiBzdG9wLWNvbG9yPSIjNjY3RUVBIi8+CjxzdG9wIG9mZnNldD0iMTAwJSIgc3RvcC1jb2xvcj0iIzc2NEJBMiIvPgo8L2xpbmVhckdyYWRpZW50Pgo8L2RlZnM+Cjwvc3ZnPgo=",
    "search": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMTEiIGN5PSIxMSIgcj0iOCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJ1cmwoI2dyYWRpZW50MCkiIHN0cm9rZS13aWR0aD0iMiIvPgo8cGF0aCBkPSJNMjEgMjFsLTQtNCIgc3Ryb2tlPSJ1cmwoI2dyYWRpZW50MCkiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+CjxkZWZzPgo8bGluZWFyR3JhZGllbnQgaWQ9ImdyYWRpZW50MCIgeDE9IjAlIiB5MT0iMCUiIHgyPSIxMDAlIiB5Mj0iMTAwJSI+CjxzdG9wIG9mZnNldD0iMCUiIHN0b3AtY29sb3I9IiM2NjdFRUEiLz4KPHN0b3Agb2Zmc2V0PSIxMDAlIiBzdG9wLWNvbG9yPSIjNzY0QkEyIi8+CjwvbGluZWFyR3JhZGllbnQ+CjwvZGVmcz4KPC9zdmc+Cg==",
    "dashboard": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3QgeD0iMyIgeT0iMyIgd2lkdGg9IjciIGhlaWdodD0iOSIgZmlsbD0idXJsKCNncmFkaWVudDApIiByeD0iMiIvPgo8cmVjdCB4PSIzIiB5PSIxMyIgd2lkdGg9IjciIGhlaWdodD0iNyIgZmlsbD0idXJsKCNncmFkaWVudDApIiByeD0iMiIvPgo8cmVjdCB4PSIxNCIgeT0iMyIgd2lkdGg9IjciIGhlaWdodD0iNSIgZmlsbD0idXJsKCNncmFkaWVudDApIiByeD0iMiIvPgo8cmVjdCB4PSIxNCIgeT0iMTAiIHdpZHRoPSI3IiBoZWlnaHQ9IjEwIiBmaWxsPSJ1cmwoI2dyYWRpZW50MCkiIHJ4PSIyIi8+CjxkZWZzPgo8bGluZWFyR3JhZGllbnQgaWQ9ImdyYWRpZW50MCIgeDE9IjAlIiB5MT0iMCUiIHgyPSIxMDAlIiB5Mj0iMTAwJSI+CjxzdG9wIG9mZnNldD0iMCUiIHN0b3AtY29sb3I9IiM2NjdFRUEiLz4KPHN0b3Agb2Zmc2V0PSIxMDAlIiBzdG9wLWNvbG9yPSIjNzY0QkEyIi8+CjwvbGluZWFyR3JhZGllbnQ+CjwvZGVmcz4KPC9zdmc+Cg==",
    "stats": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTE4IDIwVjEwIiBzdHJva2U9InVybCgjZ3JhZGllbnQwKSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KPHBhdGggZD0iTTEyIDIwVjQiIHN0cm9rZT0idXJsKCNncmFkaWVudDApIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8cGF0aCBkPSJNNiAyMFYxNCIgc3Ryb2tlPSJ1cmwoI2dyYWRpZW50MCkiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+CjxkZWZzPgo8bGluZWFyR3JhZGllbnQgaWQ9ImdyYWRpZW50MCIgeDE9IjAlIiB5MT0iMCUiIHgyPSIxMDAlIiB5Mj0iMTAwJSI+CjxzdG9wIG9mZnNldD0iMCUiIHN0b3AtY29sb3I9IiM2NjdFRUEiLz4KPHN0b3Agb2Zmc2V0PSIxMDAlIiBzdG9wLWNvbG9yPSIjNzY0QkEyIi8+CjwvbGluZWFyR3JhZGllbnQ+CjwvZGVmcz4KPC9zdmc+Cg==",
    "alert": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDlWMk0xMiAyMlYxOCIgc3Ryb2tlPSIjRjU5RTBCIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8cGF0aCBkPSJNNCAxMkgyMCIgc3Ryb2tlPSIjRjU5RTBCIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8cGF0aCBkPSJNMTcuNSA2LjVMNi41IDE3LjUiIHN0cm9rZT0iI0Y1OUUwQiIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPHBhdGggZD0iTTYuNSA2LjVMMTcuNSAxNy41IiBzdHJva2U9IiNGNTlFMEIiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=",
    "safety": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTkgMTJMMTEgMTRMMTUgMTAiIHN0cm9rZT0iIzEwQjk4MSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPHBhdGggZD0iTTEyIDJMMiA3VjEyQzMgMTcuNTUgNi44NCAyMi43NCAxMiAyM0MxNy4xNiAyMi43NCAyMSAxNy41NSAyMSAxMlY3TDEyIDJaIiBmaWxsPSJ1cmwoI2dyYWRpZW50MCkiIHN0cm9rZT0idXJsKCNncmFkaWVudDApIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8ZGVmcz4KPGxpbmVhckdyYWRpZW50IGlkPSJncmFkaWVudDAiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgo8c3RvcCBvZmZzZXQ9IjAlIiBzdG9wLWNvbG9yPSIjMTBCOTgxIiBzdG9wLW9wYWNpdHk9IjAuOCIvPgo8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0b3AtY29sb3I9IiMwRUE1RTkiIHN0b3Atb3BhY2l0eT0iMC42Ii8+CjwvbGluZWFyR3JhZGllbnQ+CjwvZGVmcz4KPC9zdmc+Cg==",
    "ai": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTkgM0g0LjVDNC4yMjM4NiAzIDQgMy4yMjM4NiA0IDMuNVY4LjVDNCA4Ljc3NjE0IDQuMjIzODYgOSA0LjUgOUg5QzkuMjc2MTQgOSA5LjUgOC43NzYxNCA5LjUgOC41VjMuNUM5LjUgMy4yMjM4NiA5LjI3NjE0IDMgOSAzWiIgZmlsbD0idXJsKCNncmFkaWVudDApIi8+CjxwYXRoIGQ9Ik0xOS41IDNIMTVDMTQuNzIzOSAzIDE0LjUgMy4yMjM4NiAxNC41IDMuNVY4LjVDMTQuNSA4Ljc3NjE0IDE0LjcyMzkgOSAxNSA5SDE5LjVDMTkuNzc2MSA5IDIwIDguNzc2MTQgMjAgOC41VjMuNUMyMCAzLjIyMzg2IDE5Ljc3NjEgMyAxOS41IDNaIiBmaWxsPSJ1cmwoI2dyYWRpZW50MCkiLz4KPHBhdGggZD0iTTkgMTVINC41QzQuMjIzODYgMTUgNCAxNS4yMjM5IDQgMTUuNVYyMC41QzQgMjAuNzc2MSA0LjIyMzg2IDIxIDQuNSAyMUg5QzkuMjc2MTQgMjEgOS41IDIwLjc3NjEgOS41IDIwLjVWMTUuNUM5LjUgMTUuMjIzOSA5LjI3NjE0IDE1IDkgMTVaIiBmaWxsPSJ1cmwoI2dyYWRpZW50MCkiLz4KPHBhdGggZD0iTTE5LjUgMTVIMTVDMTQuNzIzOSAxNSAxNC41IDE1LjIyMzkgMTQuNSAxNS41VjIwLjVDMTQuNSAyMC43NzYxIDE0LjcyMzkgMjEgMTUgMjFIMTkuNUMyMC43NzYxIDIxIDIxIDIwLjc3NjEgMjEgMjAuNVYxNS41QzIxIDE1LjIyMzkgMjAuNzc2MSAxNSAxOS41IDE1WiIgZmlsbD0idXJsKCNncmFkaWVudDApIi8+CjxkZWZzPgo8bGluZWFyR3JhZGllbnQgaWQ9ImdyYWRpZW50MCIgeDE9IjAlIiB5MT0iMCUiIHgyPSIxMDAlIiB5Mj0iMTAwJSI+CjxzdG9wIG9mZnNldD0iMCUiIHN0b3AtY29sb3I9IiM4QjVDRjYiLz4KPHN0b3Agb2Zmc2V0PSIxMDAlIiBzdG9wLWNvbG9yPSIjN0MzQUVEIi8+CjwvbGluZWFyR3JhZGllbnQ+CjwvZGVmcz4KPC9zdmc+Cg==",
    "hospital": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTMgMjFIMjEiIHN0cm9rZT0idXJsKCNncmFkaWVudDApIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8cGF0aCBkPSJNNSA4VjE4IiBzdHJva2U9InVybCgjZ3JhZGllbnQwKSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KPHBhdGggZD0iTTE5IDhWMTgiIHN0cm9rZT0idXJsKCNncmFkaWVudDApIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8cGF0aCBkPSJNMyAxMkgyMSIgc3Ryb2tlPSJ1cmwoI2dyYWRpZW50MCkiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+CjxwYXRoIGQ9Ik0xMiAyVjgiIHN0cm9rZT0idXJsKCNncmFkaWVudDApIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8cGF0aCBkPSJNOSA4SDE1IiBzdHJva2U9InVybCgjZ3JhZGllbnQwKSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KPHBhdGggZD0iTTEyIDE4VjIyIiBzdHJva2U9InVybCgjZ3JhZGllbnQwKSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KPGNpcmNsZSBjeD0iMTIiIGN5PSIxNSIgcj0iMS41IiBmaWxsPSJ1cmwoI2dyYWRpZW50MCkiLz4KPGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMSIgZmlsbD0idXJsKCNncmFkaWVudDApIi8+CjxkZWZzPgo8bGluZWFyR3JhZGllbnQgaWQ9ImdyYWRpZW50MCIgeDE9IjAlIiB5MT0iMCUiIHgyPSIxMDAlIiB5Mj0iMTAwJSI+CjxzdG9wIG9mZnNldD0iMCUiIHN0b3AtY29sb3I9IiM2NjdFRUEiLz4KPHN0b3Agb2Zmc2V0PSIxMDAlIiBzdG9wLWNvbG9yPSIjNzY0QkEyIi8+CjwvbGluZWFyR3JhZGllbnQ+CjwvZGVmcz4KPC9zdmc+Cg==",
    "refresh": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTIxIDEyQzIxIDE2Ljk3MTYgMTYuOTcxNiAyMSAxMiAyMUM3LjAyODQzIDIxIDMgMTYuOTcxNiAzIDEyQzMgNy4wMjg0MyA3LjAyODQzIDMgMTIgMyIgc3Ryb2tlPSJ1cmwoI2dyYWRpZW50MCkiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+CjxwYXRoIGQ9Ik0zIDEySDE1IiBzdHJva2U9InVybCgjZ3JhZGllbnQwKSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KPHBhdGggZD0iTTEyIDEyTDE1IDkiIHN0cm9rZT0idXJsKCNncmFkaWVudDApIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8cGF0aCBkPSJNMTIgMTJWMyIgc3Ryb2tlPSJ1cmwoI2dyYWRpZW50MCkiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+CjxkZWZzPgo8bGluZWFyR3JhZGllbnQgaWQ9ImdyYWRpZW50MCIgeDE9IjAlIiB5MT0iMCUiIHgyPSIxMDAlIiB5Mj0iMTAwJSI+CjxzdG9wIG9mZnNldD0iMCUiIHN0b3AtY29sb3I9IiM2NjdFRUEiLz4KPHN0b3Agb2Zmc2V0PSIxMDAlIiBzdG9wLWNvbG9yPSIjNzY0QkEyIi8+CjwvbGluZWFyR3JhZGllbnQ+CjwvZGVmcz4KPC9zdmc+Cg==",
    "database": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGVsbGlwc2UgY3g9IjEyIiBjeT0iNiIgcng9IjkiIHJ5PSIzIiBmaWxsPSJ1cmwoI2dyYWRpZW50MCkiLz4KPHBhdGggZD0iTTMgNlYxMiIgc3Ryb2tlPSJ1cmwoI2dyYWRpZW50MCkiIHN0cm9rZS13aWR0aD0iMiIvPgo8cGF0aCBkPSJNMjEgNlYxMiIgc3Ryb2tlPSJ1cmwoI2dyYWRpZW50MCkiIHN0cm9rZS13aWR0aD0iMiIvPgo8ZWxsaXBzZSBjeD0iMTIiIGN5PSIxMiIgcng9IjkiIHJ5PSIzIiBmaWxsPSJ1cmwoI2dyYWRpZW50MCkiLz4KPHBhdGggZD0iTTMgMTJWMThNMyAxOEgxMk0zIDE4SDIxTTIxIDE4VjEyIiBzdHJva2U9InVybCgjZ3JhZGllbnQwKSIgc3Ryb2tlLXdpZHRoPSIyIi8+CjxlbGxpcHNlIGN4PSIxMiIgY3k9IjE4IiByeD0iOSIgcnk9IjMiIGZpbGw9InVybCgjZ3JhZGllbnQwKSIvPgo8ZGVmcz4KPGxpbmVhckdyYWRpZW50IGlkPSJncmFkaWVudDAiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgo8c3RvcCBvZmZzZXQ9IjAlIiBzdG9wLWNvbG9yPSIjNjY3RUVBIi8+CjxzdG9wIG9mZnNldD0iMTAwJSIgc3RvcC1jb2xvcj0iIzc2NEJBMiIvPgo8L2xpbmVhckdyYWRpZW50Pgo8L2RlZnM+Cjwvc3ZnPgo=",
    "help": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMTAiIGZpbGw9InVybCgjZ3JhZGllbnQwKSIvPgo8cGF0aCBkPSJNMTIgMTZWMTJNMTIgOEgxMi4wMSIgc3Ryb2tlPSIjZmZmZmZmIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8ZGVmcz4KPGxpbmVhckdyYWRpZW50IGlkPSJncmFkaWVudDAiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgo8c3RvcCBvZmZzZXQ9IjAlIiBzdG9wLWNvbG9yPSIjNjY3RUVBIi8+CjxzdG9wIG9mZnNldD0iMTAwJSIgc3RvcC1jb2xvcj0iIzc2NEJBMiIvPgo8L2xpbmVhckdyYWRpZW50Pgo8L2RlZnM+Cjwvc3ZnPgo=",
}

# High-quality medical slider images (Base64)
SLIDER_IMAGES = {
    "hero1": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODAwIiBoZWlnaHQ9IjQwMCIgdmlld0JveD0iMCAwIDgwMCA0MDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI4MDAiIGhlaWdodD0iNDAwIiBmaWxsPSJ1cmwoI2dyYWRpZW50MCkiLz4KPGNpcmNsZSBjeD0iMjAwIiBjeT0iMTUwIiByPSI4MCIgZmlsbD0iI2ZmZmZmZiIgb3BhY2l0eT0iMC4xIi8+CjxjaXJjbGUgY3g9IjYwMCIgY3k9IjI1MCIgcj0iMTIwIiBmaWxsPSIjZmZmZmZmIiBvcGFjaXR5PSIwLjA1Ii8+Cjx0ZXh0IHg9IjQwMCIgeT0iMTgwIiBmaWxsPSJ3aGl0ZSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjQ4IiBmb250LXdlaWdodD0iNzAwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5BRC1Qb3dlcmVkPC90ZXh0Pgo8dGV4dCB4PSI0MDAiIHk9IjI0MCIgZmlsbD0id2hpdGUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSI2NCIgZm9udC13ZWlnaHQ9IjkwMCIgdGV4dC1hbmNob3I9Im1pZGRsZSI+TWVkaWNhdGlvbiBTYWZldHk8L3RleHQ+Cjx0ZXh0IHg9IjQwMCIgeT0iMzIwIiBmaWxsPSJ3aGl0ZSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjI0IiBvcGFjaXR5PSIwLjgiIHRleHQtYW5jaG9yPSJtaWRkbGUiPlByZXZlbnQgY29uZnVzaW9uIGVycm9ycyB3aXRoIGFkdmFuY2VkIEFJIGFuYWx5c2lzPC90ZXh0Pgo8ZGVmcz4KPGxpbmVhckdyYWRpZW50IGlkPSJncmFkaWVudDAiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgo8c3RvcCBvZmZzZXQ9IjAlIiBzdG9wLWNvbG9yPSIjNjY3RUVBIi8+CjxzdG9wIG9mZnNldD0iMTAwJSIgc3RvcC1jb2xvcj0iIzc2NEJBMiIvPgo8L2xpbmVhckdyYWRpZW50Pgo8L2RlZnM+Cjwvc3ZnPgo=",
    "hero2": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODAwIiBoZWlnaHQ9IjQwMCIgdmlld0JveD0iMCAwIDgwMCA0MDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI4MDAiIGhlaWdodD0iNDAwIiBmaWxsPSJ1cmwoI2dyYWRpZW50MCkiLz4KPHBhdGggZD0iTS0xMDAgMjAwTDMwMCA0MDBMOTAwIDBMNzAwIDQwMCIgZmlsbD0iI2ZmZmZmZiIgb3BhY2l0eT0iMC4wNSIvPgo8dGV4dCB4PSI0MDAiIHk9IjE2MCIgZmlsbD0id2hpdGUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSI0MiIgZm9udC13ZWlnaHQ9IjcwMCIgdGV4dC1hbmNob3I9Im1pZGRsZSI+UmVhbC1UaW1lIFJpc2sgU2NvcmluZzwvdGV4dD4KPHRleHQgeD0iNDAwIiB5PSIyMjAiIGZpbGw9IndoaXRlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMzYiIGZvbnQtd2VpZ2h0PSI2MDAiIHRleHQtYW5jaG9yPSJtaWRkbGUiPkRhdGEtRHJpdmVuIEFuYWx5dGljczwvdGV4dD4KPHRleHQgeD0iNDAwIiB5PSIyODAiIGZpbGw9IndoaXRlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMjQiIGZvbnQtd2VpZ2h0PSI0MDAiIHRleHQtYW5jaG9yPSJtaWRkbGUiPkFkdmFuY2VkIGhlYXRtYXBzLCByaXNrIGJyZWFrZG93bnMsIGFuZCBEcnVnIHBhaXIgYW5hbHlzaXM8L3RleHQ+CjxkZWZzPgo8bGluZWFyR3JhZGllbnQgaWQ9ImdyYWRpZW50MCIgeDE9IjAlIiB5MT0iMCUiIHgyPSIxMDAlIiB5Mj0iMTAwJSI+CjxzdG9wIG9mZnNldD0iMCUiIHN0b3AtY29sb3I9IiNGNTlFMEIiLz4KPHN0b3Agb2Zmc2V0PSIxMDAlIiBzdG9wLWNvbG9yPSIjRUM0ODk5Ii8+CjwvbGluZWFyR3JhZGllbnQ+CjwvZGVmcz4KPC9zdmc+Cg==",
    "hero3": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODAwIiBoZWlnaHQ9IjQwMCIgdmlld0JveD0iMCAwIDgwMCA0MDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI4MDAiIGhlaWdodD0iNDAwIiBmaWxsPSJ1cmwoI2dyYWRpZW50MCkiLz4KPGNpcmNsZSBjeD0iMTAwIiBjeT0iMTAwIiByPSI2MCIgZmlsbD0iI2ZmZmZmZiIgb3BhY2l0eT0iMC4xIi8+CjxjaXJjbGUgY3g9IjcwMCIgY3k9IjMwMCIgcj0iMTAwIiBmaWxsPSIjZmZmZmZmIiBvcGFjaXR5PSIwLjA1Ii8+Cjx0ZXh0IHg9IjQwMCIgeT0iMTUwIiBmaWxsPSJ3aGl0ZSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjQ4IiBmb250LXdlaWdodD0iNzAwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5QYXRpZW50LUNlbnRlcjwvdGV4dD4KPHRleHQgeD0iNDAwIiB5PSIyMjAiIGZpbGw9IndoaXRlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iNjQiIGZvbnQtd2VpZ2h0PSI5MDAiIHRleHQtYW5jaG9yPSJtaWRkbGUiPlNhZmV0eTwvdGV4dD4KPHRleHQgeD0iNDAwIiB5PSIzMDAiIGZpbGw9IndoaXRlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMjQiIG9wYWNpdHk9IjAuOCIgdGV4dC1hbmNob3I9Im1pZGRsZSI+RmRhLWNvbXBsaWFudCwgY2xpbmljYWxseSB2YWxpZGF0ZWQgcmlzayBhc3Nlc3NtZW50PC90ZXh0Pgo8ZGVmcz4KPGxpbmVhckdyYWRpZW50IGlkPSJncmFkaWVudDAiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgo8c3RvcCBvZmZzZXQ9IjAlIiBzdG9wLWNvbG9yPSIjMTBCOTgxIi8+CjxzdG9wIG9mZnNldD0iMTAwJSIgc3RvcC1jb2xvcj0iIzBFQTVFOSIvPgo8L2xpbmVhckdyYWRpZW50Pgo8L2RlZnM+Cjwvc3ZnPgo=",
}

# Initialize session state
for key in ['search_results', 'dashboard_data', 'selected_risk', 'heatmap_data', 'slider_index']:
    if key not in st.session_state:
        st.session_state[key] = None if key == 'heatmap_data' else ([] if key == 'search_results' else {} if key == 'dashboard_data' else ("all" if key == 'selected_risk' else 0))

# Helper functions - 100% SAME FUNCTIONALITY
def search_drug(drug_name):
    """Search for drug and analyze confusion risks"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/search/{drug_name}", timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            return None
    except Exception as e:
        st.error(f"Cannot connect to backend: {str(e)}\n\nMake sure backend is running: `python backend.py`")
        return None

def seed_database():
    """Seed database with common drugs"""
    try:
        response = requests.post(f"{BACKEND_URL}/api/seed-database")
        if response.status_code == 200:
            st.success("Database seeded successfully!")
            return True
        else:
            st.error("Failed to seed database")
            return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

def load_dashboard_data():
    """Load ALL dashboard data including heatmap"""
    try:
        # Load metrics
        metrics_response = requests.get(f"{BACKEND_URL}/api/metrics")
        if metrics_response.status_code == 200:
            st.session_state.dashboard_data['metrics'] = metrics_response.json()
        
        # Load top risks
        risks_response = requests.get(f"{BACKEND_URL}/api/top-risks?limit=10")
        if risks_response.status_code == 200:
            st.session_state.dashboard_data['top_risks'] = risks_response.json()
        
        # Load risk breakdown
        breakdown_response = requests.get(f"{BACKEND_URL}/api/risk-breakdown")
        if breakdown_response.status_code == 200:
            st.session_state.dashboard_data['breakdown'] = breakdown_response.json()
        
        # Load heatmap data
        heatmap_response = requests.get(f"{BACKEND_URL}/api/heatmap?limit=15")
        if heatmap_response.status_code == 200:
            st.session_state.dashboard_data['heatmap'] = heatmap_response.json()
            st.session_state.heatmap_data = heatmap_response.json()
            
    except Exception as e:
        st.error(f"Error loading dashboard data: {e}")

def create_heatmap_chart():
    """Create interactive drug confusion heatmap - Premium Design"""
    if not st.session_state.heatmap_data:
        return None
    
    heatmap_data = st.session_state.heatmap_data
    drug_names = heatmap_data.get("drug_names", [])
    risk_matrix = heatmap_data.get("risk_matrix", [])
    
    if not drug_names or not risk_matrix:
        return None
    
    # Premium heatmap with beautiful color scheme
    fig = go.Figure(data=go.Heatmap(
        z=risk_matrix,
        x=drug_names,
        y=drug_names,
        colorscale=[
            [0, '#10B981'],      # Emerald
            [0.2, '#0EA5E9'],    # Sky Blue
            [0.4, '#8B5CF6'],    # Violet
            [0.6, '#F59E0B'],    # Amber
            [0.8, '#EC4899'],    # Pink
            [1, '#BE185D']       # Rose
        ],
        zmin=0,
        zmax=100,
        text=[[f"{val:.0f}%" if val > 0 else "" for val in row] for row in risk_matrix],
        texttemplate="%{text}",
        textfont={"size": 11, "color": "#FFFFFF"},
        hoverongaps=False,
        hoverinfo="text",
        hovertemplate="<b>%{y}</b> ↔ <b>%{x}</b><br><b>Risk Score: %{z:.1f}%</b><br><extra></extra>",
        colorbar=dict(
            title="Risk Score %",
            titleside="right",
            titlefont=dict(size=14, color=COLORS["text_primary"]),
            tickfont=dict(size=12, color=COLORS["text_secondary"]),
            thickness=15,
            len=0.75,
            y=0.5,
            yanchor="middle"
        )
    ))
    
    fig.update_layout(
        title={
            "text": "Drug Confusion Risk Heatmap",
            "y":0.95,
            "x":0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 24, "color": COLORS["text_primary"], "family": "Inter"}
        },
        xaxis_title="<b>Drug Names</b>",
        yaxis_title="<b>Drug Names</b>",
        height=650,
        margin={"t": 100, "b": 100, "l": 120, "r": 50},
        plot_bgcolor="#ffffff",
        paper_bgcolor="#f8fafc",
        font=dict(family="Inter, sans-serif", size=12, color=COLORS["text_primary"]),
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=10),
            gridcolor='rgba(0,0,0,0.05)'
        ),
        yaxis=dict(
            tickfont=dict(size=10),
            gridcolor='rgba(0,0,0,0.05)'
        )
    )
    
    # Add annotations for high-risk cells
    for i in range(len(drug_names)):
        for j in range(len(drug_names)):
            if risk_matrix[i][j] > 70:
                fig.add_annotation(
                    x=j, y=i,
                    text="⚡",
                    showarrow=False,
                    font=dict(size=14, color="white"),
                    xref="x",
                    yref="y"
                )
    
    return fig

def create_risk_breakdown_chart():
    """Create enhanced risk breakdown donut chart"""
    if 'breakdown' not in st.session_state.dashboard_data:
        return None
    
    breakdown = st.session_state.dashboard_data['breakdown']
    if not breakdown:
        return None
    
    categories = [item['category'].title() for item in breakdown]
    counts = [item['count'] for item in breakdown]
    
    color_map = {
        "Critical": "#EC4899",
        "High": "#F59E0B",
        "Medium": "#8B5CF6",
        "Low": "#10B981"
    }
    colors = [color_map.get(cat, "#8B5CF6") for cat in categories]
    
    # Create donut chart
    fig = go.Figure(data=[
        go.Pie(
            labels=categories,
            values=counts,
            hole=0.6,
            marker_colors=colors,
            textinfo='label+percent',
            textposition='inside',
            insidetextorientation='radial',
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>",
            textfont=dict(size=13, color="white"),
            marker=dict(line=dict(color="#ffffff", width=2))
        )
    ])
    
    fig.update_layout(
        title={
            "text": "Risk Distribution",
            "y":0.95,
            "x":0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 20, "color": COLORS["text_primary"], "family": "Inter"}
        },
        height=450,
        margin=dict(t=80, b=20, l=20, r=20),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.05,
            font=dict(size=12, family="Inter", color=COLORS["text_primary"])
        ),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#f8fafc",
        font=dict(family="Inter, sans-serif", size=12, color=COLORS["text_primary"]),
    )
    
    # Add center text
    fig.add_annotation(
        text=f"<b>Total</b><br>{sum(counts)}",
        x=0.5, y=0.5,
        font=dict(size=16, color=COLORS["text_primary"], family="Inter"),
        showarrow=False
    )
    
    return fig

def create_top_risks_chart():
    """Create enhanced top risks horizontal bar chart"""
    if 'top_risks' not in st.session_state.dashboard_data:
        return None
    
    top_risks = st.session_state.dashboard_data['top_risks']
    if not top_risks:
        return None
    
    pairs = [f"{item['drug1']} ↔ {item['drug2']}" for item in top_risks]
    scores = [item['risk_score'] for item in top_risks]
    categories = [item['risk_category'] for item in top_risks]
    reasons = [item['reason'] for item in top_risks]
    
    color_map = {
        "critical": "#EC4899",
        "high": "#F59E0B",
        "medium": "#8B5CF6",
        "low": "#10B981"
    }
    colors = [color_map.get(cat.lower(), "#8B5CF6") for cat in categories]
    
    fig = go.Figure(data=[
        go.Bar(
            x=scores,
            y=pairs,
            orientation='h',
            marker_color=colors,
            text=[f"{score:.0f}%" for score in scores],
            textposition='outside',
            textfont=dict(size=11, color=COLORS["text_primary"], family="Inter"),
            hovertemplate="<b>%{y}</b><br>Risk Score: <b>%{x:.1f}%</b><br>Category: %{customdata[0]}<br>%{customdata[1]}<extra></extra>",
            customdata=list(zip(categories, reasons)),
            marker=dict(line=dict(color="#ffffff", width=1))
        )
    ])
    
    fig.update_layout(
        title={
            "text": "Top 10 High-Risk Drug Pairs",
            "y":0.95,
            "x":0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 22, "color": COLORS["text_primary"], "family": "Inter"}
        },
        xaxis_title="<b>Risk Score (%)</b>",
        yaxis_title="<b>Drug Pairs</b>",
        height=500,
        margin=dict(t=80, b=50, l=220, r=50),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#f8fafc",
        font=dict(family="Inter, sans-serif", size=12, color=COLORS["text_primary"]),
        xaxis=dict(
            gridcolor='rgba(0,0,0,0.05)',
            range=[0, 105]
        ),
        yaxis=dict(
            tickfont=dict(size=11, family="Inter"),
            categoryorder='total ascending'
        )
    )
    
    # Add threshold lines
    fig.add_vline(x=75, line_dash="dash", line_color="#EC4899", opacity=0.3)
    fig.add_vline(x=50, line_dash="dash", line_color="#F59E0B", opacity=0.3)
    fig.add_vline(x=25, line_dash="dash", line_color="#8B5CF6", opacity=0.3)
    
    return fig

# Premium CSS with Animations and Modern Design
st.markdown(f"""
<style>
    /* Import Inter Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Modern Professional Theme */
    .stApp {{
        background: {COLORS["background"]};
        font-family: 'Inter', sans-serif;
        background-attachment: fixed;
    }}
    
    /* Hero Slider */
    .hero-slider {{
        width: 100%;
        height: 300px;
        border-radius: 20px;
        overflow: hidden;
        margin: 2rem 0;
        position: relative;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        animation: slideIn 1s ease-out;
    }}
    
    .hero-slider img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.5s ease;
    }}
    
    .hero-slider:hover img {{
        transform: scale(1.02);
    }}
    
    /* Header Styling */
    .main-header {{
        font-size: 3.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif;
        letter-spacing: -1px;
        animation: fadeInUp 0.8s ease-out;
        text-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);
    }}
    
    .sub-header {{
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.4rem;
        margin-bottom: 2rem;
        font-weight: 400;
        font-family: 'Inter', sans-serif;
        animation: fadeInUp 1s ease-out;
    }}
    
    /* Premium Card Styling with Gradient */
    .metric-card {{
        background: {COLORS["card_gradient"]};
        padding: 1.8rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        text-align: center;
        border: none;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        font-family: 'Inter', sans-serif;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        position: relative;
        overflow: hidden;
    }}
    
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: 0.5s;
    }}
    
    .metric-card:hover::before {{
        left: 100%;
    }}
    
    .metric-card:hover {{
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.25);
    }}
    
    /* Risk Card Styling */
    .risk-card {{
        background: {COLORS["card_gradient"]};
        padding: 1.8rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: none;
        position: relative;
        overflow: hidden;
        animation: slideInRight 0.6s ease-out;
        animation-delay: calc(var(--i) * 0.1s);
    }}
    
    .risk-card::after {{
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        width: 6px;
        transition: all 0.4s ease;
    }}
    
    .risk-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    }}
    
    .risk-card.critical::after {{ background: linear-gradient(180deg, #EC4899 0%, #BE185D 100%); }}
    .risk-card.high::after {{ background: linear-gradient(180deg, #F59E0B 0%, #D97706 100%); }}
    .risk-card.medium::after {{ background: linear-gradient(180deg, #8B5CF6 0%, #7C3AED 100%); }}
    .risk-card.low::after {{ background: linear-gradient(180deg, #10B981 0%, #059669 100%); }}
    
    /* Unified Premium Button Styling */
    .stButton > button {{
        position: relative !important;
        padding: 16px 32px !important;
        border: none !important;
        border-radius: 12px !important;
        cursor: pointer !important;
        overflow: hidden !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        min-height: 52px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 10px !important;
        letter-spacing: 0.5px !important;
        
        background: {COLORS["button_gradient"]} !important;
        color: white !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3) !important;
    }}
    
    .stButton > button::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: 0.5s;
    }}
    
    .stButton > button:hover::before {{
        left: 100%;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4) !important;
    }}
    
    .stButton > button:active {{
        transform: translateY(1px) scale(0.98) !important;
    }}
    
    /* Secondary button styling */
    .stButton > button[kind="secondary"] {{
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
        color: #4F46E5 !important;
        border: 2px solid transparent !important;
        background-clip: padding-box !important;
        position: relative !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }}
    
    .stButton > button[kind="secondary"]::before {{
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: {COLORS["button_gradient"]};
        border-radius: 14px;
        z-index: -1;
        opacity: 0;
        transition: opacity 0.4s;
    }}
    
    .stButton > button[kind="secondary"]:hover::before {{
        opacity: 1;
    }}
    
    .stButton > button[kind="secondary"]:hover {{
        color: white !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3) !important;
    }}
    
    /* Premium Tab Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.95) 100%);
        backdrop-filter: blur(10px);
        padding: 12px;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        font-family: 'Inter', sans-serif;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 60px;
        padding: 0 28px;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        font-family: 'Inter', sans-serif;
        color: {COLORS["text_secondary"]};
        border: 2px solid transparent;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background: rgba(102, 126, 234, 0.1) !important;
        color: {COLORS["primary"]} !important;
        transform: translateY(-2px);
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {COLORS["button_gradient"]} !important;
        color: white !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3) !important;
        transform: translateY(-2px);
    }}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        font-family: 'Inter', sans-serif;
        box-shadow: 5px 0 25px rgba(0,0,0,0.08);
    }}
    
    /* Input Styling */
    .stTextInput > div > div > input {{
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 14px 18px;
        font-size: 16px;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        background: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {COLORS["primary"]};
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15), 0 8px 25px rgba(102, 126, 234, 0.2);
        transform: translateY(-1px);
    }}
    
    /* Metric Styling */
    [data-testid="stMetricValue"] {{
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        font-family: 'Inter', sans-serif;
        background: {COLORS["button_gradient"]};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    
    [data-testid="stMetricLabel"] {{
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: {COLORS["text_primary"]} !important;
    }}
    
    /* Divider */
    .divider {{
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.3), transparent);
        margin: 2.5rem 0;
        opacity: 0.5;
    }}
    
    /* Badge Styling */
    .risk-badge {{
        padding: 8px 20px;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        font-family: 'Inter', sans-serif;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        color: white;
        position: relative;
        overflow: hidden;
        z-index: 1;
    }}
    
    .risk-badge::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: inherit;
        filter: brightness(0.9);
        z-index: -1;
    }}
    
    /* Info Box */
    .info-box {{
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        font-family: 'Inter', sans-serif;
        border: none;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.15);
        backdrop-filter: blur(10px);
        animation: fadeIn 0.8s ease-out;
    }}
    
    /* Section Header */
    .section-header {{
        color: {COLORS["text_primary"]};
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 1.8rem;
        font-family: 'Inter', sans-serif;
        position: relative;
        display: inline-block;
    }}
    
    .section-header::after {{
        content: '';
        position: absolute;
        bottom: -8px;
        left: 0;
        width: 60px;
        height: 4px;
        background: {COLORS["button_gradient"]};
        border-radius: 2px;
    }}
    
    /* Animations */
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes slideIn {{
        from {{
            opacity: 0;
            transform: translateX(-30px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    @keyframes slideInRight {{
        from {{
            opacity: 0;
            transform: translateX(30px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); }}
    }}
    
    /* Grid item styling */
    .grid-item {{
        background: {COLORS["card_gradient"]};
        border-radius: 16px;
        padding: 1.2rem;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    
    .grid-item:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }}
    
    /* Status indicators */
    .status-indicator {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        backdrop-filter: blur(10px);
    }}
    
    .status-healthy {{
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(14, 165, 233, 0.2));
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }}
    
    .status-warning {{
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(236, 72, 153, 0.2));
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }}
    
    .status-critical {{
        background: linear-gradient(135deg, rgba(236, 72, 153, 0.2), rgba(190, 24, 93, 0.2));
        color: #EC4899;
        border: 1px solid rgba(236, 72, 153, 0.3);
    }}
    
    /* Floating animation for cards */
    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
    }}
    
    .floating {{
        animation: float 3s ease-in-out infinite;
    }}
    
    /* Glow effect */
    .glow {{
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
    }}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: rgba(0,0,0,0.05);
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {COLORS["button_gradient"]};
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(135deg, #764ba2 0%, #8B5CF6 100%);
    }}
</style>
""", unsafe_allow_html=True)

# Hero Slider Section
st.markdown(f"""
<div class='hero-slider'>
    <img src='{list(SLIDER_IMAGES.values())[st.session_state.slider_index]}' />
</div>
""", unsafe_allow_html=True)

# Slider Navigation
col1, col2, col3 = st.columns([1, 8, 1])
with col1:
    if st.button("◀", use_container_width=True, type="secondary"):
        st.session_state.slider_index = (st.session_state.slider_index - 1) % len(SLIDER_IMAGES)
        st.rerun()
with col3:
    if st.button("▶", use_container_width=True, type="secondary"):
        st.session_state.slider_index = (st.session_state.slider_index + 1) % len(SLIDER_IMAGES)
        st.rerun()

# Premium Header
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem 0 1rem 0;'>
        <img src='{ICONS["logo"]}' width='80' style='margin-bottom: 20px; animation: pulse 2s ease-in-out infinite;'>
        <div class='main-header'>MediNomix</div>
        <div class='sub-header'>Advanced AI-Powered Medication Safety Platform</div>
    </div>
    """, unsafe_allow_html=True)

# Premium Action Buttons
st.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <div style='display: inline-flex; gap: 15px; background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.95) 100%); padding: 15px; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);'>
""", unsafe_allow_html=True)

action_cols = st.columns([1, 1, 1, 1])
with action_cols[0]:
    if st.button("**Seed Database**", use_container_width=True, type="secondary"):
        with st.spinner("Seeding database with sample drugs..."):
            if seed_database():
                load_dashboard_data()
                st.rerun()
with action_cols[1]:
    if st.button("**Refresh Data**", use_container_width=True, type="secondary"):
        with st.spinner("Refreshing dashboard data..."):
            load_dashboard_data()
            st.rerun()
with action_cols[2]:
    if st.button("**Quick Demo**", use_container_width=True):
        st.session_state.search_results = []
        with st.spinner("Testing with Metformin..."):
            result = search_drug("metformin")
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.rerun()
with action_cols[3]:
    if st.button("**Get Help**", use_container_width=True, type="secondary"):
        st.info("**Quick Tips:**\n1. Search any drug name to analyze confusion risks\n2. Use the heatmap to visualize risk patterns\n3. Check FDA alerts for known dangerous pairs")

st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Premium Navigation Tabs
tab1, tab2, tab3 = st.tabs([
    "**Drug Analysis**", 
    "**Analytics Dashboard**", 
    "**About & Resources**"
])

with tab1:
    # Premium Search Section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <img src='{ICONS["search"]}' width='60' style='margin-bottom: 15px; animation: pulse 2s ease-in-out infinite; animation-delay: 1s;'>
            <h2 class='section-header'>Drug Confusion Risk Analysis</h2>
            <p style='color: {COLORS["text_secondary"]}; font-size: 1.1rem;'>
                Enter a drug name to analyze potential confusion risks with other medications
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Premium Search Bar
    search_col1, search_col2, search_col3 = st.columns([1, 2, 1])
    with search_col2:
        drug_name = st.text_input(
            "",
            placeholder="Enter drug name (e.g., metformin, lamictal, celebrex...)",
            label_visibility="collapsed",
            key="search_input"
        )
        
        # Premium Search Buttons
        search_cols = st.columns([1, 1])
        with search_cols[0]:
            search_clicked = st.button("**Analyze Drug**", use_container_width=True, type="primary")
        with search_cols[1]:
            if st.button("**Show Examples**", use_container_width=True, type="secondary"):
                examples = ["metformin", "lamictal", "celebrex", "clonidine", "zyprexa"]
                st.info(f"**Try these drugs:** {', '.join(examples)}")
    
    if search_clicked and drug_name:
        with st.spinner(f"Analyzing '{drug_name}' for confusion risks..."):
            result = search_drug(drug_name)
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.success(f"Analysis complete! Found {len(st.session_state.search_results)} similar drugs.")
                st.balloons()
                st.rerun()
    
    # Results Section
    if st.session_state.search_results:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Premium Risk Filter Buttons
        st.markdown("### Filter Results")
        risk_filters = {
            "All Risks": "all",
            "Critical (≥75%)": "critical",
            "High (50-74%)": "high",
            "Medium (25-49%)": "medium",
            "Low (<25%)": "low"
        }
        
        filter_cols = st.columns(5)
        for i, (label, value) in enumerate(risk_filters.items()):
            btn_type = "primary" if st.session_state.selected_risk == value else "secondary"
            if filter_cols[i].button(label, use_container_width=True, type=btn_type):
                st.session_state.selected_risk = value
                st.rerun()
        
        # Filter results
        if st.session_state.selected_risk == "all":
            filtered_results = st.session_state.search_results
        else:
            filtered_results = [
                r for r in st.session_state.search_results 
                if r['risk_category'] == st.session_state.selected_risk
            ]
        
        # Premium Results Header
        st.markdown(f"""
        <div class='info-box'>
            <h3 style='color: {COLORS["text_primary"]}; margin: 0; font-size: 1.4rem;'>
                Found {len(filtered_results)} Similar Drugs
            </h3>
            <p style='color: {COLORS["text_secondary"]}; margin: 8px 0 0 0;'>
                Displaying {'all' if st.session_state.selected_risk == 'all' else st.session_state.selected_risk} risk levels
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Premium Drug Cards with Animation
        for idx, result in enumerate(filtered_results):
            risk_class = result['risk_category']
            risk_color = {
                "critical": "#EC4899",
                "high": "#F59E0B",
                "medium": "#8B5CF6",
                "low": "#10B981"
            }.get(risk_class, "#8B5CF6")
            
            with st.container():
                # Card Container with Animation Delay
                st.markdown(f"""
                <div class='risk-card {risk_class}' style='--i: {idx % 5};'>
                    <div style='display: flex; justify-content: space-between; align-items: start;'>
                        <div>
                            <h3 style='color: {COLORS["text_primary"]}; margin-bottom: 5px; font-size: 1.6rem;'>
                                <img src='{ICONS["pill"]}' width='24' style='vertical-align: middle; margin-right: 10px;'>
                                {result['target_drug']['brand_name']}
                            </h3>
                            <p style='color: {COLORS["text_secondary"]}; margin: 0; font-style: italic; font-size: 1rem;'>
                                {result['target_drug']['generic_name'] if result['target_drug']['generic_name'] else 'Generic name not available'}
                            </p>
                        </div>
                        <div style='text-align: right;'>
                            <span class='risk-badge' style='background: linear-gradient(135deg, {risk_color}, {risk_color}AA);'>
                                {risk_class.upper()}
                            </span>
                            <div style='margin-top: 10px; font-size: 2.2rem; font-weight: 800; background: linear-gradient(135deg, {risk_color}, {risk_color}80); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                                {result['combined_risk']:.0f}%
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Premium Metrics Grid
                cols = st.columns(4)
                metrics = [
                    ("Spelling Similarity", f"{result['spelling_similarity']:.1f}%"),
                    ("Phonetic Similarity", f"{result['phonetic_similarity']:.1f}%"),
                    ("Therapeutic Context", f"{result['therapeutic_context_risk']:.1f}%"),
                    ("Overall Risk", f"{result['combined_risk']:.1f}%")
                ]
                
                for col, (label, value) in zip(cols, metrics):
                    with col:
                        st.markdown(f"""
                        <div class='grid-item'>
                            <div style='font-size: 0.9rem; color: {COLORS["text_secondary"]}; margin-bottom: 8px; font-weight: 500;'>{label}</div>
                            <div style='font-size: 1.4rem; font-weight: 700; color: {COLORS["text_primary"]};'>{value}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Additional Details
                with st.expander("View Drug Details", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        if result['target_drug']['purpose']:
                            st.markdown("**Purpose:**")
                            st.info(result['target_drug']['purpose'][:200] + "..." if len(result['target_drug']['purpose']) > 200 else result['target_drug']['purpose'])
                    with col2:
                        if result['target_drug']['manufacturer']:
                            st.markdown("**Manufacturer:**")
                            st.text(result['target_drug']['manufacturer'])
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

with tab2:
    # Premium Dashboard
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <img src='{ICONS["dashboard"]}' width='60' style='margin-bottom: 15px; animation: pulse 2s ease-in-out infinite; animation-delay: 0.5s;'>
        <h2 class='section-header'>Medication Safety Analytics</h2>
        <p style='color: {COLORS["text_secondary"]}; font-size: 1.1rem;'>
            Real-time insights into drug confusion risks and patterns
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data if not loaded
    if 'metrics' not in st.session_state.dashboard_data:
        load_dashboard_data()
    
    # Premium Metrics Cards with Gradient
    if 'metrics' in st.session_state.dashboard_data:
        metrics = st.session_state.dashboard_data['metrics']
        metric_cols = st.columns(4)
        
        metric_data = [
            ("Total Drugs", metrics.get('total_drugs', 0), "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"),
            ("High/Critical Pairs", metrics.get('high_risk_pairs', 0), "linear-gradient(135deg, #F59E0B 0%, #EC4899 100%)"),
            ("Critical Pairs", metrics.get('critical_risk_pairs', 0), "linear-gradient(135deg, #EC4899 0%, #BE185D 100%)"),
            ("Avg Risk Score", f"{metrics.get('avg_risk_score', 0):.1f}%", "linear-gradient(135deg, #10B981 0%, #0EA5E9 100%)")
        ]
        
        for col, (title, value, gradient) in zip(metric_cols, metric_data):
            with col:
                st.markdown(f"""
                <div class='metric-card floating'>
                    <div style='font-size: 0.95rem; color: {COLORS["text_secondary"]}; margin-bottom: 10px; font-weight: 600;'>{title}</div>
                    <div style='font-size: 2.8rem; font-weight: 800; margin-bottom: 5px; background: {gradient}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>{value}</div>
                    <div style='font-size: 0.85rem; color: {COLORS["text_secondary"]}; opacity: 0.8;'>
                        {['Total medications in database', 'Pairs requiring attention', 'Extreme risk pairs', 'Average confusion risk'][metric_cols.index(col)]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Heatmap Section
    st.markdown("### Drug Confusion Heatmap")
    heatmap_chart = create_heatmap_chart()
    if heatmap_chart:
        st.plotly_chart(heatmap_chart, use_container_width=True)
        st.markdown("""
        <div class='info-box'>
            <p style='margin: 0; font-size: 1.05rem;'><b>How to read this heatmap:</b> Each cell shows confusion risk between two drugs. 
            Green cells indicate low risk (<25%), blue cells show moderate risk (25-50%), 
            purple cells indicate high risk (50-75%), and pink cells show critical risk (>75%). 
            Hover over any cell for detailed information.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No heatmap data available. Search for drugs or seed the database first.")
    
    # Premium Charts Section
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### Risk Analytics")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### Risk Distribution")
        breakdown_chart = create_risk_breakdown_chart()
        if breakdown_chart:
            st.plotly_chart(breakdown_chart, use_container_width=True)
        else:
            st.info("No risk breakdown data available.")
    
    with chart_col2:
        st.markdown("#### Top Risk Pairs")
        risks_chart = create_top_risks_chart()
        if risks_chart:
            st.plotly_chart(risks_chart, use_container_width=True)
        else:
            st.info("No top risk data available.")
    
    # FDA Alert Table
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### FDA High Alert Drug Pairs")
    
    risky_pairs = pd.DataFrame([
        {"Drug 1": "Lamictal", "Drug 2": "Lamisil", "Risk Level": "Critical", 
         "Medical Use": "Epilepsy vs Fungal infection", "Alert Type": "FDA Safety Warning", "Year": "2023"},
        {"Drug 1": "Celebrex", "Drug 2": "Celexa", "Risk Level": "Critical", 
         "Medical Use": "Arthritis vs Depression", "Alert Type": "ISMP High Alert", "Year": "2023"},
        {"Drug 1": "Metformin", "Drug 2": "Metronidazole", "Risk Level": "High", 
         "Medical Use": "Diabetes vs Antibiotic", "Alert Type": "Common Error", "Year": "2022"},
        {"Drug 1": "Clonidine", "Drug 2": "Klonopin", "Risk Level": "High", 
         "Medical Use": "Blood pressure vs Anxiety", "Alert Type": "Sound-alike", "Year": "2022"},
        {"Drug 1": "Zyprexa", "Drug 2": "Zyrtec", "Risk Level": "Medium", 
         "Medical Use": "Antipsychotic vs Allergy", "Alert Type": "Look-alike", "Year": "2021"},
        {"Drug 1": "Hydrocodone", "Drug 2": "Oxycodone", "Risk Level": "Critical", 
         "Medical Use": "Pain medication", "Alert Type": "FDA Black Box", "Year": "2023"},
    ])
    
    # Enhanced DataFrame Display
    st.dataframe(
        risky_pairs,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Risk Level": st.column_config.TextColumn(
                "Risk", 
                width="small",
                help="Risk level based on similarity analysis"
            ),
            "Alert Type": st.column_config.TextColumn("Alert", width="medium"),
            "Year": st.column_config.NumberColumn("Year", width="small", format="%d")
        }
    )

with tab3:
    # Premium About Section
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <img src='{ICONS["hospital"]}' width='60' style='margin-bottom: 15px; animation: pulse 2s ease-in-out infinite; animation-delay: 1.5s;'>
        <h2 class='section-header'>About MediNomix</h2>
        <p style='color: {COLORS["text_secondary"]}; font-size: 1.1rem;'>
            Advanced AI platform designed to prevent medication errors through real-time analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics with Icons
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <img src='{ICONS["alert"]}' width='40' style='margin-bottom: 15px;'>
            <div style='font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #F59E0B 0%, #EC4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>25%</div>
            <div style='font-size: 1rem; color: {COLORS["text_primary"]}; margin: 10px 0; font-weight: 600;'>Medication Errors</div>
            <div style='font-size: 0.85rem; color: {COLORS["text_secondary"]};'>involve name confusion</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <img src='{ICONS["stats"]}' width='40' style='margin-bottom: 15px;'>
            <div style='font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #EC4899 0%, #BE185D 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>1.5M</div>
            <div style='font-size: 1rem; color: {COLORS["text_primary"]}; margin: 10px 0; font-weight: 600;'>Annual Harm</div>
            <div style='font-size: 0.85rem; color: {COLORS["text_secondary"]};'>Americans affected</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <img src='{ICONS["ai"]}' width='40' style='margin-bottom: 15px;'>
            <div style='font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #10B981 0%, #0EA5E9 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>$42B</div>
            <div style='font-size: 1rem; color: {COLORS["text_primary"]}; margin: 10px 0; font-weight: 600;'>Annual Cost</div>
            <div style='font-size: 0.85rem; color: {COLORS["text_secondary"]};'>preventable expenses</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Problem & Solution Cards
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card' style='text-align: left;'>
            <div style='display: flex; align-items: center; margin-bottom: 20px;'>
                <img src='{ICONS["alert"]}' width='36' style='margin-right: 15px;'>
                <h3 style='margin: 0; background: linear-gradient(135deg, #EC4899 0%, #BE185D 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>The Problem</h3>
            </div>
            <ul style='padding-left: 20px; margin: 0; color: {COLORS["text_primary"]}; line-height: 1.6;'>
                <li><b>25% of medication errors</b> involve name confusion (FDA)</li>
                <li><b>1.5 million Americans</b> harmed annually</li>
                <li><b>$42 billion</b> in preventable costs</li>
                <li>Common pairs: <b style='color: #EC4899;'>Lamictal↔Lamisil</b>, <b style='color: #EC4899;'>Celebrex↔Celexa</b></li>
                <li>Current EHR systems offer <b>basic alerts only</b></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card' style='text-align: left;'>
            <div style='display: flex; align-items: center; margin-bottom: 20px;'>
                <img src='{ICONS["safety"]}' width='36' style='margin-right: 15px;'>
                <h3 style='margin: 0; background: linear-gradient(135deg, #10B981 0%, #0EA5E9 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Our Solution</h3>
            </div>
            <ul style='padding-left: 20px; margin: 0; color: {COLORS["text_primary"]}; line-height: 1.6;'>
                <li><b>Real-time FDA data</b> analysis</li>
                <li><b>Multi-algorithm</b> risk scoring</li>
                <li><b>Interactive visualizations</b> and heatmaps</li>
                <li><b>Actionable safety</b> recommendations</li>
                <li><b>Healthcare professional</b> focused design</li>
                <li><b>Context-aware</b> similarity detection</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # How It Works
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### How It Works")
    
    steps_cols = st.columns(4)
    step_data = [
        ("Search", "Enter drug name", "User inputs any medication name for analysis"),
        ("Analyze", "Calculate risks", "Advanced algorithms assess multiple similarity factors"),
        ("Visualize", "View results", "Interactive charts, heatmaps, and risk scores"),
        ("Prevent", "Take action", "Safety alerts and prevention recommendations")
    ]
    
    for col, (title, subtitle, desc) in zip(steps_cols, step_data):
        with col:
            st.markdown(f"""
            <div class='metric-card' style='height: 240px;'>
                <div style='text-align: center;'>
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                         color: white; width: 50px; height: 50px; border-radius: 15px; 
                         display: inline-flex; align-items: center; justify-content: center;
                         font-weight: bold; margin-bottom: 20px; font-size: 1.5rem; box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);'>
                         {steps_cols.index(col) + 1}
                    </div>
                    <h4 style='color: {COLORS["text_primary"]}; margin: 10px 0; font-size: 1.2rem;'>{title}</h4>
                    <p style='color: {COLORS["primary"]}; margin: 5px 0; font-size: 0.95rem; font-weight: 600;'>{subtitle}</p>
                    <p style='color: {COLORS["text_secondary"]}; font-size: 0.9rem; margin-top: 10px; line-height: 1.5;'>{desc}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Premium Sidebar
with st.sidebar:
    # Logo and Title
    st.markdown(f"""
    <div style='text-align: center; padding: 1.5rem 0;'>
        <img src='{ICONS["logo"]}' width='70' style='margin-bottom: 15px; animation: pulse 2s ease-in-out infinite;'>
        <h3 style='color: {COLORS["text_primary"]}; margin: 5px 0; font-family: Inter; font-weight: 800;'>MediNomix</h3>
        <p style='color: {COLORS["text_secondary"]}; font-size: 0.9rem; font-family: Inter;'>AI-Powered Medication Safety</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Quick Actions with Icons
    st.markdown("### Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Test", use_container_width=True, type="primary"):
            st.session_state.search_results = []
            with st.spinner("Testing with Metformin..."):
                result = search_drug("metformin")
                if result:
                    st.session_state.search_results = result.get('similar_drugs', [])
                    st.rerun()
    
    with col2:
        if st.button("Load Data", use_container_width=True, type="secondary"):
            if seed_database():
                load_dashboard_data()
                st.rerun()
    
    if st.button("Refresh All", use_container_width=True, type="secondary"):
        load_dashboard_data()
        st.rerun()
    
    if st.button("Get Help", use_container_width=True, type="secondary"):
        st.info("**Need assistance?**\n\n1. Check the About section\n2. Try Quick Demo\n3. Contact support")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Backend Status
    st.markdown("### System Status")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'healthy':
                st.markdown('<div class="status-indicator status-healthy">✅ Backend Connected</div>', unsafe_allow_html=True)
                status_cols = st.columns(2)
                with status_cols[0]:
                    st.metric("Drugs", data.get('drugs_in_database', 0))
                with status_cols[1]:
                    st.metric("Risks", data.get('risk_assessments', 0))
            else:
                st.markdown('<div class="status-indicator status-warning">⚠️ Backend Error</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-indicator status-critical">❌ Cannot Connect</div>', unsafe_allow_html=True)
    except:
        st.markdown('<div class="status-indicator status-critical">🔌 Backend Not Running</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(236, 72, 153, 0.1), rgba(190, 24, 93, 0.1)); padding: 12px; border-radius: 12px; margin-top: 10px; border: 1px solid rgba(236, 72, 153, 0.2);'>
            <p style='margin: 0; font-size: 0.85rem; color: {COLORS["text_secondary"]};'>
            <b>Fix:</b> Run in terminal:<br>
            <code style='background: rgba(0,0,0,0.05); padding: 6px 10px; border-radius: 6px; font-size: 0.8rem; display: block; margin-top: 5px;'>python backend.py</code>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Risk Categories Guide
    st.markdown("### Risk Categories")
    
    risk_categories = [
        ("Critical", "≥75%", "Immediate intervention required", "linear-gradient(135deg, #EC4899 0%, #BE185D 100%)"),
        ("High", "50-74%", "Review and verification needed", "linear-gradient(135deg, #F59E0B 0%, #D97706 100%)"),
        ("Medium", "25-49%", "Monitor closely", "linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%)"),
        ("Low", "<25%", "Low priority", "linear-gradient(135deg, #10B981 0%, #059669 100%)")
    ]
    
    for name, range_, desc, gradient in risk_categories:
        st.markdown(f"""
        <div style='display: flex; align-items: center; margin-bottom: 15px;'>
            <div style='width: 12px; height: 12px; border-radius: 50%; margin-right: 12px; background: {gradient};'></div>
            <div>
                <div style='font-weight: 700; color: {COLORS["text_primary"]};'>{name} {range_}</div>
                <div style='font-size: 0.8rem; color: {COLORS["text_secondary"]}; line-height: 1.3;'>{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Premium Footer
st.markdown(f"""
<style>
.medinomix-footer {{
    text-align: center;
    padding: 2.5rem 0;
    margin-top: 4rem;
    background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.95) 100%);
    border-top: 1px solid rgba(102, 126, 234, 0.2);
    border-radius: 20px 20px 0 0;
    color: {COLORS["text_secondary"]};
    font-size: 0.9rem;
    font-family: 'Inter', sans-serif;
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}}
.medinomix-footer::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: {COLORS["button_gradient"]};
}}
.medinomix-footer a {{
    color: {COLORS["primary"]};
    text-decoration: none;
    font-weight: 600;
    position: relative;
}}
.medinomix-footer a::after {{
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;
    height: 2px;
    background: {COLORS["button_gradient"]};
    transition: width 0.3s;
}}
.medinomix-footer a:hover::after {{
    width: 100%;
}}
</style>

<div class='medinomix-footer'>
    <div style='display: flex; justify-content: center; gap: 40px; margin-bottom: 20px; flex-wrap: wrap;'>
        <div style='display: flex; align-items: center; gap: 8px;'>
            <div style='width: 8px; height: 8px; border-radius: 50%; background: {COLORS["button_gradient"]};'></div>
            <span>AI-Powered Analytics</span>
        </div>
        <div style='display: flex; align-items: center; gap: 8px;'>
            <div style='width: 8px; height: 8px; border-radius: 50%; background: {COLORS["button_gradient"]};'></div>
            <span>Real-time Risk Scoring</span>
        </div>
        <div style='display: flex; align-items: center; gap: 8px;'>
            <div style='width: 8px; height: 8px; border-radius: 50%; background: {COLORS["button_gradient"]};'></div>
            <span>FDA-Compliant</span>
        </div>
    </div>
    
    <div style='margin: 20px 0 15px 0; font-size: 1.1rem; font-weight: 600; color: {COLORS["text_primary"]};'>
        © 2024 MediNomix • Advanced Medication Safety Platform
    </div>
    
    <div style='font-size: 0.85rem; opacity: 0.8; margin-top: 15px; line-height: 1.5;'>
        <b>Last Updated</b>: {datetime.now().strftime('%Y-%m-%d %H:%M')} • 
        Always consult healthcare professionals for medical decisions. 
        This application is designed to assist, not replace, professional judgment.
    </div>
</div>
""", unsafe_allow_html=True)