#!/usr/bin/env python3
"""
Simple Flask API for collecting LLM Data Explorer feedback.
Stores feedback anonymously in a SQLite database.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration
DATABASE = 'feedback.db'

def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with the feedback table."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            satisfaction INTEGER NOT NULL,
            clarity INTEGER NOT NULL,
            llm_provider TEXT NOT NULL,
            questions_answered TEXT NOT NULL,
            improvements TEXT,
            conversation TEXT,
            user_agent TEXT,
            ip_address TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Database initialized at {DATABASE}")

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Handle feedback submission."""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['satisfaction', 'clarity', 'llm_provider', 'questions_answered']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Validate satisfaction and clarity are between 1-5
        if not (1 <= int(data['satisfaction']) <= 5):
            return jsonify({'error': 'Satisfaction must be between 1 and 5'}), 400
        if not (1 <= int(data['clarity']) <= 5):
            return jsonify({'error': 'Clarity must be between 1 and 5'}), 400

        # Get optional metadata
        user_agent = request.headers.get('User-Agent', '')
        ip_address = request.remote_addr

        # Insert into database
        conn = get_db_connection()
        cursor = conn.execute('''
            INSERT INTO feedback
            (satisfaction, clarity, llm_provider, questions_answered, improvements, conversation, user_agent, ip_address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['satisfaction'],
            data['clarity'],
            data['llm_provider'],
            data['questions_answered'],
            data.get('improvements', ''),
            data.get('conversation', ''),
            user_agent,
            ip_address
        ))
        conn.commit()
        feedback_id = cursor.lastrowid
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Feedback submitted successfully',
            'id': feedback_id
        }), 201

    except Exception as e:
        print(f"Error submitting feedback: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/feedback', methods=['GET'])
def get_feedback():
    """Retrieve all feedback (for admin use)."""
    try:
        conn = get_db_connection()
        feedback = conn.execute('SELECT * FROM feedback ORDER BY timestamp DESC').fetchall()
        conn.close()

        # Convert to list of dicts
        feedback_list = [dict(row) for row in feedback]

        return jsonify({
            'success': True,
            'count': len(feedback_list),
            'feedback': feedback_list
        }), 200

    except Exception as e:
        print(f"Error retrieving feedback: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/feedback/stats', methods=['GET'])
def get_stats():
    """Get feedback statistics."""
    try:
        conn = get_db_connection()

        # Get total count
        total = conn.execute('SELECT COUNT(*) as count FROM feedback').fetchone()['count']

        # Get average satisfaction and clarity
        averages = conn.execute('''
            SELECT
                AVG(satisfaction) as avg_satisfaction,
                AVG(clarity) as avg_clarity
            FROM feedback
        ''').fetchone()

        # Get LLM provider distribution
        providers = conn.execute('''
            SELECT llm_provider, COUNT(*) as count
            FROM feedback
            GROUP BY llm_provider
            ORDER BY count DESC
        ''').fetchall()

        # Get questions answered distribution
        answered = conn.execute('''
            SELECT questions_answered, COUNT(*) as count
            FROM feedback
            GROUP BY questions_answered
        ''').fetchall()

        conn.close()

        return jsonify({
            'success': True,
            'total_responses': total,
            'average_satisfaction': round(averages['avg_satisfaction'], 2) if averages['avg_satisfaction'] else 0,
            'average_clarity': round(averages['avg_clarity'], 2) if averages['avg_clarity'] else 0,
            'llm_providers': [dict(row) for row in providers],
            'questions_answered': [dict(row) for row in answered]
        }), 200

    except Exception as e:
        print(f"Error retrieving stats: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200

if __name__ == '__main__':
    # Initialize database on startup
    init_db()

    # Run the server
    print("Starting Feedback API server...")
    print("Access the API at http://localhost:5000")
    print("Endpoints:")
    print("  POST /api/feedback - Submit feedback")
    print("  GET  /api/feedback - View all feedback")
    print("  GET  /api/feedback/stats - View statistics")
    print("  GET  /api/health - Health check")

    app.run(debug=True, host='0.0.0.0', port=5000)
